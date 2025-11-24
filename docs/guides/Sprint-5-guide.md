# Guia de Implementação Detalhado do Sprint 5: Rastreamento Básico de SLA (24/7)

## Visão Geral do Sprint

**Objetivo:**
Implementar um sistema de rastreamento de Service Level Agreement (SLA) que calcula os tempos de resposta e resolução com base na prioridade do incidente. O cálculo será baseado num modelo 24/7, sem considerar horários de expediente ou feriados.

**User Stories:**

-   [Em Curso] US5.1: Criar e Gerir Políticas de SLA
-   [Em Curso] US5.2: Aplicar Automaticamente Políticas de SLA a Novos Incidentes
-   [Em Curso] US5.3: Exibir o Status do SLA na UI de Incidentes

**Pré-requisitos:**

-   Sprints 1 a 4 completos.

---

## Aplicando as Tecnologias Fundamentais

Neste sprint, o foco é a implementação do rastreamento de SLAs, uma funcionalidade crítica para a gestão de serviços. Vamos utilizar as tecnologias da nossa stack para garantir que os cálculos são precisos, performáticos e bem geridos.

### 1. Cache de Cálculos com Redis

**Objetivo:** Melhorar a performance ao evitar cálculos repetitivos e dispendiosos do tempo restante do SLA.

**Ações:**

-   **Instalação:** Se ainda não estiver configurado, instale e configure o `nestjs-redis` ou um cliente Redis similar no `nest-backend`.
-   **Cache Service:** Crie um `SlaCacheService` ou adicione a lógica ao `SlaService`.
-   **Lógica de Cache:**
    -   Após calcular o tempo restante de um SLA, armazene o resultado no Redis com um TTL (Time-To-Live) curto (ex: 1 minuto). A chave pode ser algo como `sla:incident-id:countdown`.
    -   Antes de recalcular, verifique sempre se o valor existe na cache. Se existir, retorne o valor da cache.
    -   Invalide a cache de um incidente sempre que o seu estado de SLA mudar (ex: quando é pausado ou resolvido).

**Documentação:**
[Documentação Oficial do Redis](https://redis.io/docs/)
[Guia Oficial do Nest.js sobre Caching](https://docs.nestjs.com/techniques/caching)

### 2. Gestão de Configuração de SLA com ConfigModule

**Objetivo:** Permitir que os tempos de SLA e limiares de aviso sejam facilmente configuráveis através de variáveis de ambiente.

**Ações:**

-   **Variáveis de Ambiente:** Adicione as configurações de tempo para cada prioridade no ficheiro `.env` (ex: `SLA_P1_RESOLUTION_HOURS=4`, `SLA_P2_RESOLUTION_HOURS=8`). Adicione também um limiar para avisos (ex: `SLA_WARNING_THRESHOLD=0.8` para 80%).
-   **Acesso via ConfigService:** No `SlaService`, injete o `ConfigService` para obter estes valores, em vez de os ter "hardcoded" no código. Isto permite ajustes rápidos sem necessidade de um novo deploy.

**Documentação:**
[Guia Oficial do Nest.js sobre Configuration](https://docs.nestjs.com/techniques/configuration)

### 3. Logging de Eventos de SLA com Winston

**Objetivo:** Manter um registo detalhado de todos os eventos de SLA para fins de auditoria e análise de performance.

**Ações:**

-   No `SlaService`, injete o `LoggerService` (Winston).
-   **Eventos a Registar:**
    -   `SLA BREACH`: Quando um SLA de resposta ou resolução é violado. Registe o ID do incidente e por quanto tempo foi violado.
    -   `SLA WARNING`: Quando um incidente atinge o limiar de aviso (ex: 80% do tempo de SLA).
    -   `SLA CALCULATION`: Opcionalmente, registe os cálculos para depuração.

**Documentação:**
[Guia Oficial do `nest-winston`](https://github.com/gremo/nest-winston)

### 4. Monitorização Automática de SLA com Cron Jobs

**Objetivo:** Implementar uma tarefa agendada que verifica periodicamente se algum incidente violou o SLA e envia notificações automáticas.

**Ações:**

-   **Instalação:** Instale o pacote `@nestjs/schedule`:
    ```bash
    cd nest-backend
    npm install @nestjs/schedule
    ```
-   **Configuração:** Importe `ScheduleModule` no `AppModule`:

    ```typescript
    import { ScheduleModule } from "@nestjs/schedule";

    @Module({
        imports: [
            ScheduleModule.forRoot(),
            // ... outros módulos
        ],
    })
    export class AppModule {}
    ```

-   **Criar Cron Job:** No `SlaService`, adicione um método com o decorator `@Cron()`:

    ```typescript
    import { Cron, CronExpression } from '@nestjs/schedule';

    @Cron(CronExpression.EVERY_5_MINUTES)
    async checkSlaBreaches() {
      const now = new Date();

      // Encontrar incidentes que violaram SLA de resposta
      const responseBreaches = await this.prisma.incident.findMany({
        where: {
          status: { notIn: ['RESOLVED', 'CLOSED'] },
          firstRespondedAt: null,
          slaResponseDue: { lt: now },
        },
        include: { assignedTo: true, createdBy: true },
      });

      // Encontrar incidentes que violaram SLA de resolução
      const resolutionBreaches = await this.prisma.incident.findMany({
        where: {
          status: { notIn: ['RESOLVED', 'CLOSED'] },
          resolvedAt: null,
          slaResolutionDue: { lt: now },
        },
        include: { assignedTo: true, createdBy: true },
      });

      // Enviar notificações para cada breach
      for (const incident of responseBreaches) {
        this.logger.error(`SLA BREACH: Incident #${incident.number} - Response time exceeded`, {
          incidentId: incident.id,
          dueDate: incident.slaResponseDue,
          breachTime: Math.floor((now.getTime() - incident.slaResponseDue.getTime()) / 60000),
        });

        // Enviar email/notificação (integração com EmailService do Sprint 6)
        // await this.emailService.sendSlaBreachNotification(incident);
      }

      for (const incident of resolutionBreaches) {
        this.logger.error(`SLA BREACH: Incident #${incident.number} - Resolution time exceeded`, {
          incidentId: incident.id,
          dueDate: incident.slaResolutionDue,
          breachTime: Math.floor((now.getTime() - incident.slaResolutionDue.getTime()) / 60000),
        });

        // await this.emailService.sendSlaBreachNotification(incident);
      }
    }
    ```

-   **Avisos Preventivos (80% do tempo):** Adicione outro cron job para enviar avisos quando o SLA atinge 80%:

    ```typescript
    @Cron(CronExpression.EVERY_10_MINUTES)
    async checkSlaWarnings() {
      const now = new Date();
      const warningThreshold = parseFloat(this.configService.get('SLA_WARNING_THRESHOLD') || '0.8');

      const incidents = await this.prisma.incident.findMany({
        where: {
          status: { notIn: ['RESOLVED', 'CLOSED'] },
          OR: [
            { firstRespondedAt: null, slaResponseDue: { gte: now } },
            { resolvedAt: null, slaResolutionDue: { gte: now } },
          ],
        },
        include: { slaPolicy: true },
      });

      for (const incident of incidents) {
        const createdAt = incident.createdAt.getTime();
        const responseDue = incident.slaResponseDue?.getTime();
        const resolutionDue = incident.slaResolutionDue?.getTime();

        // Verificar se atingiu limiar de aviso para resposta
        if (responseDue && !incident.firstRespondedAt) {
          const timeElapsed = now.getTime() - createdAt;
          const totalTime = responseDue - createdAt;
          const percentageUsed = timeElapsed / totalTime;

          if (percentageUsed >= warningThreshold && percentageUsed < 1) {
            this.logger.warn(`SLA WARNING: Incident #${incident.number} - ${Math.round(percentageUsed * 100)}% of response time used`);
            // await this.emailService.sendSlaWarningNotification(incident, 'response');
          }
        }

        // Verificar se atingiu limiar de aviso para resolução
        if (resolutionDue && !incident.resolvedAt) {
          const timeElapsed = now.getTime() - createdAt;
          const totalTime = resolutionDue - createdAt;
          const percentageUsed = timeElapsed / totalTime;

          if (percentageUsed >= warningThreshold && percentageUsed < 1) {
            this.logger.warn(`SLA WARNING: Incident #${incident.number} - ${Math.round(percentageUsed * 100)}% of resolution time used`);
            // await this.emailService.sendSlaWarningNotification(incident, 'resolution');
          }
        }
      }
    }
    ```

**Notas Importantes:**

-   Os cron jobs correm em background e não bloqueiam requests HTTP.
-   Use `CronExpression.EVERY_5_MINUTES` para breaches críticos e `EVERY_10_MINUTES` para avisos.
-   Os comentários de `emailService` serão implementados no Sprint 6.
-   Considere adicionar um mecanismo de "debounce" para evitar enviar múltiplas notificações do mesmo breach.

**Documentação:**
[Guia Oficial do Nest.js sobre Task Scheduling](https://docs.nestjs.com/techniques/task-scheduling)
[Documentação do cron-expression](https://github.com/kelektiv/node-cron#cron-ranges)

### 5. Autorização de Configuração de SLA com CASL

**Objetivo:** Garantir que apenas administradores podem criar ou modificar as políticas de SLA.

**Ações:**

-   **Definir Habilidades:** No `casl-ability.factory.ts`, defina as permissões para o `subject` 'SlaPolicy'. Apenas o role `ADMIN` deve ter a ação `manage`.
-   **Proteger Endpoints:** No `slapolicies.controller.ts`, proteja os endpoints de criação (`POST`), atualização (`PATCH`) e eliminação (`DELETE`) com um `RolesGuard` ou verificando a permissão diretamente no service.

**Documentação:**
[Guia Oficial do CASL](https://casl.js.org/v6/en/guide/intro)
[Integração do CASL com Nest.js](https://casl.js.org/v6/en/package/casl-nestjs)

### 6. Validação e Documentação

-   **Validação:** Use `class-validator` nos DTOs de `SlaPolicy` para garantir que os tempos inseridos são números válidos e dentro de um intervalo razoável (ex: `@Min(1)`, `@Max(168)` para horas).
-   **Swagger:** Documente os endpoints de gestão de SLA no `slapolicies.controller.ts` e explique a lógica de cálculo nos `descriptions` do `@ApiOperation`.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação](https://docs.nestjs.com/techniques/validation)
[Guia Oficial do Nest.js sobre OpenAPI (Swagger)](https://docs.nestjs.com/openapi/introduction)

---

## Funcionalidade 5.1 & 5.2: Gestão e Aplicação de Políticas de SLA

**Objetivo:** Implementar um "vertical slice" para criar políticas de SLA e aplicá-las automaticamente aos incidentes com base na sua prioridade.

---

### Fase 1: Base de Dados (Prisma & PostgreSQL)

#### 1.1. Definir o Modelo `SlaPolicy`

**Ficheiro:** `nest-backend/prisma/schema.prisma`

**Ação:**
Adicione o modelo `SlaPolicy` para definir as regras de tempo para cada prioridade de incidente.

**Modelo `SlaPolicy`:**

-   **Campos:**
    -   `id`: Identificador único.
    -   `priority`: Do tipo `IncidentPriority` (P1, P2, P3, P4), com `@unique` para garantir uma única política por prioridade.
    -   `responseTimeInMinutes`: `Int` - Tempo máximo para a primeira resposta.
    -   `resolutionTimeInMinutes`: `Int` - Tempo máximo para a resolução do incidente.
-   **Relações:**
    -   Crie uma relação um-para-muitos com o modelo `Incident`.

**Documentação:**
[Guia Oficial do Prisma sobre Relações um-para-muitos](https://www.prisma.io/docs/orm/prisma-schema/data-model/relations#one-to-many-relations)

#### 1.2. Atualizar o Modelo `Incident`

**Ficheiro:** `nest-backend/prisma/schema.prisma`

**Ação:**
Adicione campos ao modelo `Incident` para rastrear os prazos e o status do SLA.

**Novos Campos no `Incident`:**

-   `slaPolicyId`: `String?` - Chave estrangeira para a `SlaPolicy` aplicada.
-   `slaResponseDue`: `DateTime?` - Timestamp de quando a resposta é devida.
-   `slaResolutionDue`: `DateTime?` - Timestamp de quando a resolução é devida.
-   `firstRespondedAt`: `DateTime?` - Timestamp da primeira resposta (ex: primeiro comentário de um agente).
-   `resolvedAt`: `DateTime?` - Timestamp de quando o status mudou para `RESOLVED`.

#### 1.3. Executar a Migração

**Comando:**

```bash
cd nest-backend
npm run prisma:migrate:dev -- --name add_sla_tracking
```

**O que acontece:**
O Prisma gera e aplica um ficheiro SQL que cria a tabela `SlaPolicy` e adiciona as novas colunas à tabela `Incident`.

**Documentação:**
[Guia Oficial do Prisma sobre Migrações](https://www.prisma.io/docs/orm/prisma-migrate/getting-started)

**Code Examples:**

```prisma
// nest-backend/prisma/schema.prisma
model SlaPolicy {
  id                      String   @id @default(uuid())
  priority                IncidentPriority @unique
  responseTimeInMinutes   Int      @map("response_time_in_minutes")
  resolutionTimeInMinutes Int      @map("resolution_time_in_minutes")
  createdAt               DateTime @default(now()) @map("created_at")
  updatedAt               DateTime @updatedAt @map("updated_at")

  incidents Incident[]

  @@map("sla_policies")
}

model Incident {
  // ... campos existentes ...
  slaPolicyId      String?   @map("sla_policy_id")
  slaResponseDue   DateTime? @map("sla_response_due")
  slaResolutionDue DateTime? @map("sla_resolution_due")
  firstRespondedAt DateTime? @map("first_responded_at")
  resolvedAt       DateTime? @map("resolved_at")

  slaPolicy SlaPolicy? @relation(fields: [slaPolicyId], references: [id])

  @@index([slaPolicyId])
  @@index([slaResponseDue])
  @@index([slaResolutionDue])
  @@map("incidents")
}
```

```bash
# Executar migração
cd nest-backend
npm run prisma:migrate:dev -- --name add_sla_tracking
npm run prisma:generate
```

---

### Fase 2: Backend (Nest.js)

#### 2.1. Gerar o Recurso `slapolicies`

**Comando:**

```bash
cd nest-backend
nest g resource slapolicies --no-spec
```

**Resultado:**
Cria automaticamente `slapolicies.module.ts`, `slapolicies.controller.ts`, `slapolicies.service.ts` e a pasta `dto`, poupando trabalho manual.

**Documentação:**
[Guia Oficial do Nest.js sobre Geração de Recursos](https://docs.nestjs.com/cli/generators#resource-generator)

#### 2.2. Definir DTOs para Políticas de SLA

**Ficheiros:** `create-slapolicy.dto.ts`, `update-slapolicy.dto.ts`

**Objetivo:**
Definir a "forma" dos dados que os endpoints de políticas de SLA esperam. É a primeira camada de validação.

**`CreateSlaPolicyDto`:**
Define a estrutura de dados para criar uma nova política de SLA. Os validadores (`class-validator`) garantem a integridade dos dados na entrada da API.

-   `priority`: Deve corresponder a um dos valores do enum `IncidentPriority` (P1, P2, P3, P4). Use `@IsEnum(IncidentPriority)`.
-   `responseTimeInMinutes`: Tempo de resposta em minutos. Deve ser um inteiro positivo. Use `@IsInt()` e `@Min(1)`.
-   `resolutionTimeInMinutes`: Tempo de resolução em minutos. Deve ser um inteiro positivo. Use `@IsInt()` e `@Min(1)`.

**`UpdateSlaPolicyDto`:**
Define os campos que podem ser atualizados numa política existente. Todos os campos devem ser opcionais.

-   `responseTimeInMinutes`: Opcional, para ajustar o tempo de resposta.
-   `resolutionTimeInMinutes`: Opcional, para ajustar o tempo de resolução.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação (class-validator)](https://docs.nestjs.com/techniques/validation)

**Code Examples:**

```typescript
// nest-backend/src/slapolicies/dto/create-slapolicy.dto.ts
import { IsEnum, IsInt, Min, Max } from "class-validator";
import { ApiProperty } from "@nestjs/swagger";
import { IncidentPriority } from "@prisma/client";

export class CreateSlaPolicyDto {
    @ApiProperty({
        enum: IncidentPriority,
        description: "Prioridade do incidente (P1, P2, P3, P4)",
        example: "P1",
    })
    @IsEnum(IncidentPriority)
    priority: IncidentPriority;

    @ApiProperty({
        description: "Tempo de resposta em minutos",
        example: 60,
        minimum: 1,
        maximum: 10080, // 1 semana
    })
    @IsInt()
    @Min(1)
    @Max(10080)
    responseTimeInMinutes: number;

    @ApiProperty({
        description: "Tempo de resolução em minutos",
        example: 240,
        minimum: 1,
        maximum: 10080,
    })
    @IsInt()
    @Min(1)
    @Max(10080)
    resolutionTimeInMinutes: number;
}
```

```typescript
// nest-backend/src/slapolicies/dto/update-slapolicy.dto.ts
import { PartialType } from "@nestjs/swagger";
import { CreateSlaPolicyDto } from "./create-slapolicy.dto";
import { OmitType } from "@nestjs/swagger";

export class UpdateSlaPolicyDto extends PartialType(
    OmitType(CreateSlaPolicyDto, ["priority"] as const)
) {}
```

#### 2.3. Implementar o `SlaPoliciesService`

**Ficheiro:** `nest-backend/src/slapolicies/slapolicies.service.ts`

**Objetivo:**
Implementar a lógica de negócio para gestão de políticas de SLA.

**Ações:**

1.  **`create()`**:

    -   Recebe o `CreateSlaPolicyDto`.
    -   Verifica se já existe uma política para a prioridade especificada usando `findUnique({ where: { priority } })`.
    -   Se existir, lança uma `ConflictException`.
    -   Se não existir, cria a nova política na base de dados.

2.  **`findAll()`**:

    -   Retorna todas as políticas de SLA, ordenadas por prioridade (P1, P2, P3, P4).

3.  **`findOne(priority)`**:

    -   Procura uma política específica pela sua prioridade.
    -   Se não encontrar, lança uma `NotFoundException`.

4.  **`update(priority)`**:

    -   Permite atualizar os tempos de resposta e resolução de uma política existente.
    -   Verifica se a política existe antes de atualizar.

5.  **`remove(priority)`**:
    -   Remove uma política de SLA da base de dados.
    -   Considere soft delete ou verifique se existem incidentes associados antes de remover.

**Documentação:**
[Guia Oficial do Prisma sobre Consultas CRUD](https://www.prisma.io/docs/orm/prisma-client/queries/crud)

**Code Examples:**

```typescript
// nest-backend/src/slapolicies/slapolicies.service.ts
import {
    Injectable,
    ConflictException,
    NotFoundException,
    Inject,
} from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { CreateSlaPolicyDto } from "./dto/create-slapolicy.dto";
import { UpdateSlaPolicyDto } from "./dto/update-slapolicy.dto";
import { IncidentPriority } from "@prisma/client";
import { WINSTON_MODULE_NEST_PROVIDER } from "nest-winston";
import { Logger } from "winston";

@Injectable()
export class SlaPoliciesService {
    constructor(
        private readonly prisma: PrismaService,
        @Inject(WINSTON_MODULE_NEST_PROVIDER) private readonly logger: Logger
    ) {}

    async create(createSlaPolicyDto: CreateSlaPolicyDto) {
        // Verificar se já existe política para esta prioridade
        const existing = await this.prisma.slaPolicy.findUnique({
            where: { priority: createSlaPolicyDto.priority },
        });

        if (existing) {
            throw new ConflictException(
                `Política de SLA já existe para prioridade ${createSlaPolicyDto.priority}`
            );
        }

        const policy = await this.prisma.slaPolicy.create({
            data: createSlaPolicyDto,
        });

        this.logger.info(
            `SLA Policy criada: ${policy.priority} - Resposta: ${policy.responseTimeInMinutes}min, Resolução: ${policy.resolutionTimeInMinutes}min`,
            { context: "SlaPoliciesService" }
        );

        return policy;
    }

    async findAll() {
        return this.prisma.slaPolicy.findMany({
            orderBy: { priority: "asc" }, // P1, P2, P3, P4
        });
    }

    async findOne(priority: IncidentPriority) {
        const policy = await this.prisma.slaPolicy.findUnique({
            where: { priority },
        });

        if (!policy) {
            throw new NotFoundException(
                `Política de SLA não encontrada para prioridade ${priority}`
            );
        }

        return policy;
    }

    async update(
        priority: IncidentPriority,
        updateSlaPolicyDto: UpdateSlaPolicyDto
    ) {
        // Verificar se existe
        await this.findOne(priority);

        const updated = await this.prisma.slaPolicy.update({
            where: { priority },
            data: updateSlaPolicyDto,
        });

        this.logger.info(`SLA Policy atualizada: ${priority}`, {
            context: "SlaPoliciesService",
        });

        return updated;
    }

    async remove(priority: IncidentPriority) {
        // Verificar se existe
        await this.findOne(priority);

        // Verificar se há incidentes associados
        const incidentsCount = await this.prisma.incident.count({
            where: { slaPolicy: { priority } },
        });

        if (incidentsCount > 0) {
            throw new ConflictException(
                `Não é possível remover a política. Existem ${incidentsCount} incidentes associados.`
            );
        }

        await this.prisma.slaPolicy.delete({
            where: { priority },
        });

        this.logger.info(`SLA Policy removida: ${priority}`, {
            context: "SlaPoliciesService",
        });

        return { message: "Política removida com sucesso" };
    }
}
```

#### 2.4. Configurar o `SlaPoliciesController`

**Ficheiro:** `nest-backend/src/slapolicies/slapolicies.controller.ts`

**Objetivo:**
Definir as rotas da API para gerir políticas de SLA.

**Ações:**

-   **`POST /slapolicies`**: Rota para criar uma nova política. Protegida com `@UseGuards(JwtAuthGuard)` e restrita a admins.
-   **`GET /slapolicies`**: Rota para listar todas as políticas. Protegida com `@UseGuards(JwtAuthGuard)`.
-   **`GET /slapolicies/:priority`**: Rota para visualizar uma política específica.
-   **`PATCH /slapolicies/:priority`**: Rota para editar uma política. Restrita a admins.
-   **`DELETE /slapolicies/:priority`**: Rota para remover uma política. Restrita a admins.

**Documentação:**
[Guia Oficial do Nest.js sobre Controllers](https://docs.nestjs.com/controllers)

**Code Examples:**

```typescript
// nest-backend/src/slapolicies/slapolicies.controller.ts
import {
    Controller,
    Get,
    Post,
    Body,
    Patch,
    Param,
    Delete,
    UseGuards,
} from "@nestjs/common";
import { SlaPoliciesService } from "./slapolicies.service";
import { CreateSlaPolicyDto } from "./dto/create-slapolicy.dto";
import { UpdateSlaPolicyDto } from "./dto/update-slapolicy.dto";
import { JwtAuthGuard } from "../auth/guards/jwt-auth.guard";
import { RolesGuard } from "../auth/guards/roles.guard";
import { Roles } from "../auth/decorators/roles.decorator";
import { Role } from "@prisma/client";
import {
    ApiTags,
    ApiBearerAuth,
    ApiOperation,
    ApiResponse,
    ApiParam,
} from "@nestjs/swagger";
import { IncidentPriority } from "@prisma/client";

@ApiTags("SLA Policies")
@ApiBearerAuth()
@Controller("slapolicies")
@UseGuards(JwtAuthGuard, RolesGuard)
export class SlaPoliciesController {
    constructor(private readonly slaPoliciesService: SlaPoliciesService) {}

    @Post()
    @Roles(Role.ADMIN)
    @ApiOperation({ summary: "Criar nova política de SLA (apenas Admin)" })
    @ApiResponse({ status: 201, description: "Política criada com sucesso" })
    @ApiResponse({
        status: 409,
        description: "Política já existe para esta prioridade",
    })
    create(@Body() createSlaPolicyDto: CreateSlaPolicyDto) {
        return this.slaPoliciesService.create(createSlaPolicyDto);
    }

    @Get()
    @ApiOperation({ summary: "Listar todas as políticas de SLA" })
    @ApiResponse({ status: 200, description: "Lista de políticas" })
    findAll() {
        return this.slaPoliciesService.findAll();
    }

    @Get(":priority")
    @ApiOperation({ summary: "Buscar política específica por prioridade" })
    @ApiParam({ name: "priority", enum: IncidentPriority })
    @ApiResponse({ status: 200, description: "Política encontrada" })
    @ApiResponse({ status: 404, description: "Política não encontrada" })
    findOne(@Param("priority") priority: IncidentPriority) {
        return this.slaPoliciesService.findOne(priority);
    }

    @Patch(":priority")
    @Roles(Role.ADMIN)
    @ApiOperation({ summary: "Atualizar política de SLA (apenas Admin)" })
    @ApiParam({ name: "priority", enum: IncidentPriority })
    @ApiResponse({ status: 200, description: "Política atualizada" })
    @ApiResponse({ status: 404, description: "Política não encontrada" })
    update(
        @Param("priority") priority: IncidentPriority,
        @Body() updateSlaPolicyDto: UpdateSlaPolicyDto
    ) {
        return this.slaPoliciesService.update(priority, updateSlaPolicyDto);
    }

    @Delete(":priority")
    @Roles(Role.ADMIN)
    @ApiOperation({ summary: "Remover política de SLA (apenas Admin)" })
    @ApiParam({ name: "priority", enum: IncidentPriority })
    @ApiResponse({ status: 200, description: "Política removida" })
    @ApiResponse({
        status: 409,
        description: "Política tem incidentes associados",
    })
    remove(@Param("priority") priority: IncidentPriority) {
        return this.slaPoliciesService.remove(priority);
    }
}
```

#### 2.5. Escrever Testes para `SlaPoliciesService`

**Ficheiro:** `nest-backend/src/slapolicies/slapolicies.service.spec.ts`

**Testes Essenciais:**

```typescript
describe("SlaPoliciesService - CRUD", () => {
    it("deve criar uma política de SLA com dados válidos", async () => {
        const dto = {
            priority: "P1",
            responseTimeInMinutes: 60,
            resolutionTimeInMinutes: 240,
        };
        const result = await service.create(dto);
        expect(result.priority).toBe("P1");
        expect(result.responseTimeInMinutes).toBe(60);
        expect(result.resolutionTimeInMinutes).toBe(240);
    });

    it("deve lançar ConflictException se política já existe para a prioridade", async () => {
        const dto = {
            priority: "P1",
            responseTimeInMinutes: 60,
            resolutionTimeInMinutes: 240,
        };
        await service.create(dto);
        await expect(service.create(dto)).rejects.toThrow(ConflictException);
    });

    it("deve listar todas as políticas ordenadas por prioridade", async () => {
        const policies = await service.findAll();
        expect(policies).toBeInstanceOf(Array);
        // Verificar ordenação: P1, P2, P3, P4
        const priorities = policies.map((p) => p.priority);
        expect(priorities).toEqual(["P1", "P2", "P3", "P4"]);
    });

    it("deve encontrar uma política específica por prioridade", async () => {
        const policy = await service.findOne("P2");
        expect(policy.priority).toBe("P2");
        expect(policy.responseTimeInMinutes).toBeDefined();
    });

    it("deve atualizar os tempos de uma política existente", async () => {
        const updated = await service.update("P3", {
            resolutionTimeInMinutes: 720,
        });
        expect(updated.resolutionTimeInMinutes).toBe(720);
    });
});
```

**Executar:**

```bash
npm run test -- slapolicies.service.spec.ts
```

**Documentação:**
[Nest.js Testing](https://docs.nestjs.com/fundamentals/testing)

#### 2.6. Atualizar o `IncidentsService` para Aplicar SLAs

**Ficheiro:** `nest-backend/src/incidents/incidents.service.ts`

**Objetivo:**
Modificar o serviço de incidentes para calcular e guardar os prazos de SLA na criação de um incidente.

**Ação no método `create()`:**

1.  Após criar o incidente, mas antes de o retornar, encontre a `SlaPolicy` correspondente à `priority` do incidente.
2.  Se uma política for encontrada:
    -   Calcule `slaResponseDue` = `incident.createdAt` + `policy.responseTimeInMinutes`.
    -   Calcule `slaResolutionDue` = `incident.createdAt` + `policy.resolutionTimeInMinutes`.
    -   Atualize o incidente na base de dados com estes novos timestamps e o `slaPolicyId`.

**Ação no `CommentsService` (para `firstRespondedAt`):**

-   Quando um comentário é adicionado a um incidente, verifique se é o primeiro comentário de um agente (`role !== 'USER'`). Se for, e se `incident.firstRespondedAt` for nulo, atualize-o com o `createdAt` do comentário.

**Code Examples:**

```typescript
// nest-backend/src/incidents/incidents.service.ts (atualização do método create)
import { Injectable, NotFoundException, Inject } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { CreateIncidentDto } from "./dto/create-incident.dto";
import { WINSTON_MODULE_NEST_PROVIDER } from "nest-winston";
import { Logger } from "winston";

@Injectable()
export class IncidentsService {
    constructor(
        private readonly prisma: PrismaService,
        @Inject(WINSTON_MODULE_NEST_PROVIDER) private readonly logger: Logger
    ) {}

    async create(createIncidentDto: CreateIncidentDto, userId: string) {
        // 1. Criar o incidente
        const incident = await this.prisma.incident.create({
            data: {
                ...createIncidentDto,
                requesterId: userId,
                status: "NEW",
            },
        });

        // 2. Aplicar política de SLA automaticamente
        const slaPolicy = await this.prisma.slaPolicy.findUnique({
            where: { priority: createIncidentDto.priority },
        });

        if (slaPolicy) {
            // Calcular os timestamps de vencimento
            const now = incident.createdAt;
            const slaResponseDue = new Date(
                now.getTime() + slaPolicy.responseTimeInMinutes * 60000
            );
            const slaResolutionDue = new Date(
                now.getTime() + slaPolicy.resolutionTimeInMinutes * 60000
            );

            // Atualizar o incidente com os dados de SLA
            await this.prisma.incident.update({
                where: { id: incident.id },
                data: {
                    slaPolicyId: slaPolicy.id,
                    slaResponseDue,
                    slaResolutionDue,
                },
            });

            this.logger.info(
                `SLA aplicado ao incidente ${
                    incident.incidentNumber
                }: Resposta até ${slaResponseDue.toISOString()}, Resolução até ${slaResolutionDue.toISOString()}`,
                { context: "IncidentsService" }
            );

            // Retornar incidente atualizado
            return this.prisma.incident.findUnique({
                where: { id: incident.id },
                include: {
                    requester: true,
                    assignee: true,
                    category: true,
                    slaPolicy: true,
                },
            });
        }

        // Se não houver política de SLA, retornar o incidente sem SLA
        this.logger.warn(
            `Nenhuma política de SLA encontrada para prioridade ${createIncidentDto.priority}`,
            { context: "IncidentsService" }
        );

        return this.prisma.incident.findUnique({
            where: { id: incident.id },
            include: {
                requester: true,
                assignee: true,
                category: true,
            },
        });
    }

    // Método auxiliar para atualizar firstRespondedAt
    async updateFirstResponse(incidentId: string) {
        const incident = await this.prisma.incident.findUnique({
            where: { id: incidentId },
            select: { firstRespondedAt: true },
        });

        // Só atualizar se ainda não tiver sido respondido
        if (!incident?.firstRespondedAt) {
            await this.prisma.incident.update({
                where: { id: incidentId },
                data: { firstRespondedAt: new Date() },
            });

            this.logger.info(
                `Primeira resposta registada para incidente ${incidentId}`,
                {
                    context: "IncidentsService",
                }
            );
        }
    }
}
```

```typescript
// nest-backend/src/comments/comments.service.ts (adicionar ao método create)
@Injectable()
export class CommentsService {
    constructor(
        private readonly prisma: PrismaService,
        private readonly incidentsService: IncidentsService,
        @Inject(WINSTON_MODULE_NEST_PROVIDER) private readonly logger: Logger
    ) {}

    async create(createCommentDto: CreateCommentDto, userId: string) {
        // Buscar informações do usuário para verificar role
        const user = await this.prisma.user.findUnique({
            where: { id: userId },
            select: { role: true },
        });

        // Criar o comentário
        const comment = await this.prisma.comment.create({
            data: {
                ...createCommentDto,
                userId,
            },
            include: {
                user: {
                    select: { id: true, name: true, email: true, role: true },
                },
            },
        });

        // Se for primeiro comentário de um agente, atualizar firstRespondedAt
        if (user?.role !== "USER") {
            await this.incidentsService.updateFirstResponse(
                createCommentDto.incidentId
            );

            this.logger.info(
                `Agente respondeu ao incidente ${createCommentDto.incidentId} pela primeira vez`,
                { context: "CommentsService" }
            );
        }

        return comment;
    }
}
```

#### 2.7. Escrever Testes para Lógica de SLA no IncidentsService

**Ficheiro:** `nest-backend/src/incidents/incidents.service.spec.ts`

**Testes Essenciais:**

```typescript
describe('IncidentsService - Lógica de SLA', () => {
    it('deve aplicar a política de SLA correta e calcular os prazos na criação do incidente', async () => {
        // Mock da SlaPolicy para P1: 60 min resposta, 240 min resolução
        const p1Policy = { priority: 'P1', responseTimeInMinutes: 60, resolutionTimeInMinutes: 240 };
        prisma.slaPolicy.findUnique.mockResolvedValue(p1Policy);

        const dto = { title: 'Servidor Crítico Offline', priority: 'P1', ... };
        const result = await service.create(dto, 'user-123');

        const expectedResponseDue = new Date(result.createdAt.getTime() + 60 * 60000);
        const expectedResolutionDue = new Date(result.createdAt.getTime() + 240 * 60000);

        expect(result.slaPolicyId).toBe(p1Policy.id);
        expect(result.slaResponseDue).toEqual(expectedResponseDue);
        expect(result.slaResolutionDue).toEqual(expectedResolutionDue);
    });

    it('não deve aplicar SLA se não existir política para a prioridade', async () => {
        prisma.slaPolicy.findUnique.mockResolvedValue(null);
        const dto = { title: 'Incidente de baixa prioridade', priority: 'P4', ... };
        const result = await service.create(dto, 'user-123');

        expect(result.slaPolicyId).toBeNull();
        expect(result.slaResponseDue).toBeNull();
    });
});
```

**Documentação:**
[Nest.js Testing](https://docs.nestjs.com/fundamentals/testing)

---

### Fase 3: Frontend (Next.js)

#### 3.1. Criar a UI de Gestão de Políticas de SLA

**Página:** `next-frontend/app/admin/settings/sla/page.tsx`

**Objetivo:**
Criar uma interface administrativa para visualizar e gerir as políticas de SLA.

**Descrição:**

1.  **Listagem de Políticas:**

    -   Use uma `DataTable` (shadcn/ui) para exibir todas as políticas organizadas por prioridade.
    -   Mostre colunas: Prioridade, Tempo de Resposta (em horas/minutos), Tempo de Resolução (em horas/minutos), Ações.

2.  **Edição Inline:**

    -   Permita a edição dos tempos diretamente na tabela ou através de um modal/dialog.
    -   Use `React Hook Form` + `Zod` para validação.

3.  **Fetching e Mutações:**
    -   Use `TanStack Query` para o fetching (`useQuery`) e atualizações (`useMutation`).
    -   Invalide a query após uma atualização bem-sucedida para refletir as mudanças na UI.

**Documentação:**
[Guia Oficial do TanStack Query sobre Mutations](https://tanstack.com/query/latest/docs/react/guides/mutations)

**Code Examples:**

```typescript
// next-frontend/app/admin/settings/sla/page.tsx
"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { Button } from "@/components/ui/button";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { toast } from "sonner";

const slaPolicySchema = z.object({
    responseTimeInMinutes: z.number().min(1).max(10080),
    resolutionTimeInMinutes: z.number().min(1).max(10080),
});

type SlaPolicyFormData = z.infer<typeof slaPolicySchema>;

interface SlaPolicy {
    id: string;
    priority: string;
    responseTimeInMinutes: number;
    resolutionTimeInMinutes: number;
}

export default function SlaSettingsPage() {
    const [editingPolicy, setEditingPolicy] = useState<SlaPolicy | null>(null);
    const queryClient = useQueryClient();

    // Fetch SLA policies
    const { data: policies, isLoading } = useQuery<SlaPolicy[]>({
        queryKey: ["sla-policies"],
        queryFn: async () => {
            const response = await axios.get("/api/slapolicies");
            return response.data;
        },
    });

    // Update mutation
    const updateMutation = useMutation({
        mutationFn: async (data: {
            priority: string;
            updates: SlaPolicyFormData;
        }) => {
            await axios.patch(
                `/api/slapolicies/${data.priority}`,
                data.updates
            );
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["sla-policies"] });
            toast.success("Política de SLA atualizada com sucesso");
            setEditingPolicy(null);
        },
        onError: () => {
            toast.error("Erro ao atualizar política de SLA");
        },
    });

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<SlaPolicyFormData>({
        resolver: zodResolver(slaPolicySchema),
    });

    const onSubmit = (data: SlaPolicyFormData) => {
        if (editingPolicy) {
            updateMutation.mutate({
                priority: editingPolicy.priority,
                updates: data,
            });
        }
    };

    const handleEdit = (policy: SlaPolicy) => {
        setEditingPolicy(policy);
        reset({
            responseTimeInMinutes: policy.responseTimeInMinutes,
            resolutionTimeInMinutes: policy.resolutionTimeInMinutes,
        });
    };

    const formatTime = (minutes: number) => {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
    };

    if (isLoading) return <div>Carregando...</div>;

    return (
        <div className="container mx-auto py-10">
            <h1 className="text-3xl font-bold mb-6">Políticas de SLA</h1>

            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Prioridade</TableHead>
                        <TableHead>Tempo de Resposta</TableHead>
                        <TableHead>Tempo de Resolução</TableHead>
                        <TableHead>Ações</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {policies?.map((policy) => (
                        <TableRow key={policy.id}>
                            <TableCell className="font-medium">
                                {policy.priority}
                            </TableCell>
                            <TableCell>
                                {formatTime(policy.responseTimeInMinutes)}
                            </TableCell>
                            <TableCell>
                                {formatTime(policy.resolutionTimeInMinutes)}
                            </TableCell>
                            <TableCell>
                                <Dialog>
                                    <DialogTrigger asChild>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => handleEdit(policy)}
                                        >
                                            Editar
                                        </Button>
                                    </DialogTrigger>
                                    <DialogContent>
                                        <DialogHeader>
                                            <DialogTitle>
                                                Editar Política de SLA -{" "}
                                                {policy.priority}
                                            </DialogTitle>
                                        </DialogHeader>
                                        <form
                                            onSubmit={handleSubmit(onSubmit)}
                                            className="space-y-4"
                                        >
                                            <div>
                                                <Label htmlFor="responseTimeInMinutes">
                                                    Tempo de Resposta (minutos)
                                                </Label>
                                                <Input
                                                    id="responseTimeInMinutes"
                                                    type="number"
                                                    {...register(
                                                        "responseTimeInMinutes",
                                                        { valueAsNumber: true }
                                                    )}
                                                />
                                                {errors.responseTimeInMinutes && (
                                                    <p className="text-sm text-red-500">
                                                        {
                                                            errors
                                                                .responseTimeInMinutes
                                                                .message
                                                        }
                                                    </p>
                                                )}
                                            </div>
                                            <div>
                                                <Label htmlFor="resolutionTimeInMinutes">
                                                    Tempo de Resolução (minutos)
                                                </Label>
                                                <Input
                                                    id="resolutionTimeInMinutes"
                                                    type="number"
                                                    {...register(
                                                        "resolutionTimeInMinutes",
                                                        { valueAsNumber: true }
                                                    )}
                                                />
                                                {errors.resolutionTimeInMinutes && (
                                                    <p className="text-sm text-red-500">
                                                        {
                                                            errors
                                                                .resolutionTimeInMinutes
                                                                .message
                                                        }
                                                    </p>
                                                )}
                                            </div>
                                            <Button
                                                type="submit"
                                                disabled={
                                                    updateMutation.isPending
                                                }
                                            >
                                                {updateMutation.isPending
                                                    ? "Guardando..."
                                                    : "Guardar"}
                                            </Button>
                                        </form>
                                    </DialogContent>
                                </Dialog>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
}
```

```typescript
// next-frontend/lib/hooks/use-sla-policies.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";

export interface SlaPolicy {
    id: string;
    priority: string;
    responseTimeInMinutes: number;
    resolutionTimeInMinutes: number;
}

export function useSlaPolicies() {
    return useQuery<SlaPolicy[]>({
        queryKey: ["sla-policies"],
        queryFn: async () => {
            const response = await axios.get("/api/slapolicies");
            return response.data;
        },
    });
}

export function useUpdateSlaPolicy() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (data: {
            priority: string;
            responseTimeInMinutes?: number;
            resolutionTimeInMinutes?: number;
        }) => {
            const { priority, ...updates } = data;
            const response = await axios.patch(
                `/api/slapolicies/${priority}`,
                updates
            );
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["sla-policies"] });
        },
    });
}
```

#### 3.2. Testar o Fluxo de Gestão de SLA

**Testes Manuais:**

1.  Navegue para a página de definições de SLA.
2.  Verifique se as políticas padrão (se existirem) são exibidas.
3.  Edite o tempo de resolução de uma política P2.
4.  Verifique se a alteração é guardada e refletida na UI.
5.  Crie um novo incidente com prioridade P2 e verifique na base de dados se o novo tempo de resolução foi aplicado.

---

## Funcionalidade 5.3: Exibir Status do SLA na UI

**Objetivo:** Fornecer feedback visual claro sobre o status do SLA em tempo real nas listas e detalhes dos incidentes.

---

### Fase 1: Backend (Nest.js)

#### 1.1. Adicionar um Campo Virtual para Status do SLA

**Ficheiro:** `nest-backend/src/incidents/entities/incident.entity.ts`

**Objetivo:**
Calcular dinamicamente o status do SLA (`Ok`, `DueSoon`, `Breached`) no backend para evitar lógica complexa no frontend.

**Ação:**

-   No `IncidentsService`, ao fazer `find` ou `findAll`, adicione uma propriedade virtual `slaStatus` a cada incidente.
-   A lógica para `slaStatus` deve considerar `slaResponseDue`, `slaResolutionDue`, `firstRespondedAt` e `resolvedAt`.

---

### Fase 2: Frontend (Next.js)

#### 2.1. Criar o Componente `SlaStatusBadge`

**Ficheiro:** `next-frontend/components/incidents/sla-status-badge.tsx`

**Objetivo:**
Criar um componente reutilizável que exibe o status do SLA de forma visual e informativa.

**Descrição:**

1.  **Props:**

    -   Recebe o objeto do incidente completo (incluindo `slaStatus`, `slaResponseDue`, `slaResolutionDue`).

2.  **Visual do Badge:**

    -   Renderiza um `Badge` (shadcn/ui) com cores semânticas:
        -   **Verde:** SLA cumprido (`Met`) - "✓ SLA Cumprido"
        -   **Laranja:** SLA a expirar em breve (`DueSoon`) - "⚠ Expira em 1h 30m"
        -   **Vermelho:** SLA violado (`Breached`) - "✗ SLA Violado (2h atraso)"
        -   **Cinzento:** SLA em dia (`Ok`) - "⏱ 3h 45m restantes"

3.  **Tooltip Informativo:**

    -   Use o componente `Tooltip` (shadcn/ui) para mostrar informações detalhadas:
        -   Tempo restante/atrasado para resposta e resolução.
        -   Timestamps dos prazos.
        -   Timestamps de quando respondeu/resolveu (se aplicável).

4.  **Lógica de Cálculo:**
    -   Calcule o tempo restante no frontend usando `Date.now()` e os timestamps do backend.
    -   Use uma biblioteca como `date-fns` para formatação amigável (ex: "2 horas 15 minutos").

**Documentação:**
[Guia Oficial do shadcn/ui sobre Badge](https://ui.shadcn.com/docs/components/badge)
[Guia Oficial do shadcn/ui sobre Tooltip](https://ui.shadcn.com/docs/components/tooltip)

**Code Examples:**

```typescript
// next-frontend/components/incidents/sla-status-badge.tsx
"use client";

import { Badge } from "@/components/ui/badge";
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from "@/components/ui/tooltip";
import { formatDistanceToNow, isPast } from "date-fns";
import { pt } from "date-fns/locale";

type SlaStatus = "Ok" | "DueSoon" | "Breached" | "Met";

interface Incident {
    id: string;
    slaResponseDue?: string | null;
    slaResolutionDue?: string | null;
    firstRespondedAt?: string | null;
    resolvedAt?: string | null;
    status: string;
}

export function SlaStatusBadge({ incident }: { incident: Incident }) {
    if (!incident.slaResponseDue && !incident.slaResolutionDue) {
        return <Badge variant="secondary">Sem SLA</Badge>;
    }

    const { status, badge, tooltip } = calculateSlaStatus(incident);

    return (
        <TooltipProvider>
            <Tooltip>
                <TooltipTrigger>
                    <Badge variant={badge.variant} className={badge.className}>
                        {badge.icon} {badge.text}
                    </Badge>
                </TooltipTrigger>
                <TooltipContent>
                    <div className="space-y-2 text-sm">
                        <p className="font-semibold">{tooltip.title}</p>
                        {tooltip.lines.map((line, i) => (
                            <p key={i}>{line}</p>
                        ))}
                    </div>
                </TooltipContent>
            </Tooltip>
        </TooltipProvider>
    );
}

function calculateSlaStatus(incident: Incident) {
    const now = new Date();
    const responseDue = incident.slaResponseDue
        ? new Date(incident.slaResponseDue)
        : null;
    const resolutionDue = incident.slaResolutionDue
        ? new Date(incident.slaResolutionDue)
        : null;
    const firstResponded = incident.firstRespondedAt
        ? new Date(incident.firstRespondedAt)
        : null;
    const resolved = incident.resolvedAt ? new Date(incident.resolvedAt) : null;

    // Se incidente está resolvido
    if (resolved && resolutionDue) {
        const metSla = resolved <= resolutionDue;
        return {
            status: "Met" as SlaStatus,
            badge: {
                variant: metSla ? "default" : "destructive",
                className: metSla ? "bg-green-500" : "",
                icon: metSla ? "✓" : "✗",
                text: metSla ? "SLA Cumprido" : "SLA Violado",
            },
            tooltip: {
                title: metSla ? "SLA Cumprido" : "SLA Violado",
                lines: [
                    `Resolvido: ${formatDistanceToNow(resolved, {
                        addSuffix: true,
                        locale: pt,
                    })}`,
                    `Prazo: ${formatDistanceToNow(resolutionDue, {
                        addSuffix: true,
                        locale: pt,
                    })}`,
                    metSla
                        ? `Dentro do prazo por ${formatDuration(
                              resolutionDue.getTime() - resolved.getTime()
                          )}`
                        : `Atrasado por ${formatDuration(
                              resolved.getTime() - resolutionDue.getTime()
                          )}`,
                ],
            },
        };
    }

    // Verificar resposta
    if (responseDue && !firstResponded) {
        const isBreached = isPast(responseDue);
        const timeRemaining = responseDue.getTime() - now.getTime();
        const isDueSoon = !isBreached && timeRemaining < 60 * 60 * 1000; // < 1 hora

        if (isBreached) {
            return {
                status: "Breached" as SlaStatus,
                badge: {
                    variant: "destructive",
                    className: "",
                    icon: "✗",
                    text: `Resposta Atrasada (${formatDuration(
                        now.getTime() - responseDue.getTime()
                    )})`,
                },
                tooltip: {
                    title: "SLA de Resposta Violado",
                    lines: [
                        `Prazo: ${formatDistanceToNow(responseDue, {
                            addSuffix: true,
                            locale: pt,
                        })}`,
                        `Atrasado por: ${formatDuration(
                            now.getTime() - responseDue.getTime()
                        )}`,
                        "Primeira resposta ainda não registada",
                    ],
                },
            };
        }

        if (isDueSoon) {
            return {
                status: "DueSoon" as SlaStatus,
                badge: {
                    variant: "warning",
                    className: "bg-orange-500",
                    icon: "⚠",
                    text: `Expira em ${formatDuration(timeRemaining)}`,
                },
                tooltip: {
                    title: "SLA a Expirar em Breve",
                    lines: [
                        `Tempo restante: ${formatDuration(timeRemaining)}`,
                        `Prazo: ${formatDistanceToNow(responseDue, {
                            addSuffix: true,
                            locale: pt,
                        })}`,
                    ],
                },
            };
        }
    }

    // Verificar resolução
    if (resolutionDue) {
        const isBreached = isPast(resolutionDue);
        const timeRemaining = resolutionDue.getTime() - now.getTime();
        const isDueSoon = !isBreached && timeRemaining < 2 * 60 * 60 * 1000; // < 2 horas

        if (isBreached) {
            return {
                status: "Breached" as SlaStatus,
                badge: {
                    variant: "destructive",
                    className: "",
                    icon: "✗",
                    text: `Resolução Atrasada (${formatDuration(
                        now.getTime() - resolutionDue.getTime()
                    )})`,
                },
                tooltip: {
                    title: "SLA de Resolução Violado",
                    lines: [
                        `Prazo: ${formatDistanceToNow(resolutionDue, {
                            addSuffix: true,
                            locale: pt,
                        })}`,
                        `Atrasado por: ${formatDuration(
                            now.getTime() - resolutionDue.getTime()
                        )}`,
                    ],
                },
            };
        }

        if (isDueSoon) {
            return {
                status: "DueSoon" as SlaStatus,
                badge: {
                    variant: "warning",
                    className: "bg-yellow-500",
                    icon: "⚠",
                    text: `Resolução em ${formatDuration(timeRemaining)}`,
                },
                tooltip: {
                    title: "SLA de Resolução a Expirar",
                    lines: [
                        `Tempo restante: ${formatDuration(timeRemaining)}`,
                        `Prazo: ${formatDistanceToNow(resolutionDue, {
                            addSuffix: true,
                            locale: pt,
                        })}`,
                    ],
                },
            };
        }

        // SLA OK
        return {
            status: "Ok" as SlaStatus,
            badge: {
                variant: "secondary",
                className: "",
                icon: "⏱",
                text: `${formatDuration(timeRemaining)} restantes`,
            },
            tooltip: {
                title: "SLA em Dia",
                lines: [
                    `Tempo restante para resolução: ${formatDuration(
                        timeRemaining
                    )}`,
                    `Prazo: ${formatDistanceToNow(resolutionDue, {
                        addSuffix: true,
                        locale: pt,
                    })}`,
                ],
            },
        };
    }

    return {
        status: "Ok" as SlaStatus,
        badge: {
            variant: "secondary",
            className: "",
            icon: "",
            text: "SLA OK",
        },
        tooltip: {
            title: "SLA em Dia",
            lines: [],
        },
    };
}

function formatDuration(ms: number): string {
    const hours = Math.floor(ms / (1000 * 60 * 60));
    const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));

    if (hours > 0) {
        return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
}
```

```typescript
// next-frontend/app/incidents/components/columns.tsx
import { ColumnDef } from "@tanstack/react-table";
import { SlaStatusBadge } from "@/components/incidents/sla-status-badge";
import { Incident } from "@/lib/types/incident";

export const columns: ColumnDef<Incident>[] = [
    // ... outras colunas ...
    {
        accessorKey: "slaStatus",
        header: "SLA Status",
        cell: ({ row }) => <SlaStatusBadge incident={row.original} />,
    },
    // ... restantes colunas ...
];
```

#### 2.2. Integrar o Badge na UI

**Ficheiros:**

-   `next-frontend/app/incidents/components/columns.tsx` (para a `DataTable`)
-   `next-frontend/app/incidents/[id]/page.tsx` (para a página de detalhes)

**Ação:**

-   Adicione uma nova coluna "SLA Status" à `DataTable` de incidentes e renderize o `SlaStatusBadge`.
-   Na página de detalhes do incidente, exiba o `SlaStatusBadge` de forma proeminente perto do título ou do status do incidente.

#### 2.3. Testar a Exibição do Status do SLA

**Testes Manuais:**

1.  **SLA OK:**
    -   Crie um incidente P1. Verifique se o badge de SLA está cinzento/verde com o tempo restante.
2.  **SLA de Resposta Violado:**
    -   Aguarde o tempo de resposta expirar sem adicionar um comentário.
    -   Verifique se o badge fica vermelho e o tooltip indica "Resposta em atraso".
3.  **SLA de Resposta Cumprido:**
    -   Adicione um comentário (como agente).
    -   Verifique se o badge de resposta desaparece ou fica verde.
4.  **SLA de Resolução Violado:**
    -   Deixe o tempo de resolução expirar sem mudar o status para `RESOLVED`.
    -   Verifique se o badge fica vermelho com a indicação "Resolução em atraso".
5.  **SLA Cumprido:**
    -   Resolva o incidente antes do prazo.
    -   Verifique se o badge fica verde com a indicação "Cumprido".

**Teste E2E (Opcional):**

```typescript
// next-frontend/e2e/incidents/sla-status.spec.ts
test("deve exibir o status do SLA corretamente na lista de incidentes", async ({
    page,
}) => {
    await page.goto("/incidents");

    // Encontrar a linha de um incidente com SLA em risco
    const incidentRow = page.locator(
        '.incident-row:has-text("INC-20260110-0005")'
    );

    // Verificar se o badge de SLA está visível e tem a cor esperada
    const slaBadge = incidentRow.locator(".sla-badge-due-soon");
    await expect(slaBadge).toBeVisible();
    await expect(slaBadge).toHaveText(/Expira em/);
});

test("deve atualizar o badge quando o incidente é respondido", async ({
    page,
}) => {
    await page.goto("/incidents/INC-20260110-0001");

    // Verificar badge inicial (sem resposta)
    await expect(page.locator(".sla-badge-breached")).toBeVisible();

    // Adicionar comentário como agente
    await page.fill('[name="content"]', "Estamos a investigar o problema.");
    await page.click('button:has-text("Adicionar Comentário")');

    // Verificar que badge de resposta muda
    await expect(page.locator(".sla-response-met")).toBeVisible();
});

test("deve mostrar tooltip com informação detalhada do SLA", async ({
    page,
}) => {
    await page.goto("/incidents");

    const slaBadge = page.locator(".sla-badge").first();
    await slaBadge.hover();

    // Verificar tooltip
    await expect(page.locator('[role="tooltip"]')).toBeVisible();
    await expect(page.locator('[role="tooltip"]')).toContainText(
        "Resposta devida em"
    );
});
```

**Documentação:**
[Playwright Testing Guide](https://playwright.dev/)

---

## Referência Rápida: Testes

### Comandos para Executar Testes

**Backend:**

```bash
# Executar todos os testes unitários e de integração
npm test

# Executar testes em modo watch
npm run test:watch

# Gerar relatório de coverage
npm run test:cov

# Executar testes E2E
npm run test:e2e
```

**Frontend:**

```bash
# Testes de componentes com Jest/RTL
npm test

# Testes E2E com Playwright
npm run test:e2e

# E2E com UI
npm run test:e2e -- --ui
```

### Template: E2E Test (Backend)

```typescript
describe("SLA Policies API (e2e)", () => {
    let app: INestApplication;
    let accessToken: string;

    beforeAll(async () => {
        const moduleFixture = await Test.createTestingModule({
            imports: [AppModule],
        }).compile();

        app = moduleFixture.createNestApplication();
        await app.init();

        // Login como admin para obter token
        const loginResponse = await request(app.getHttpServer())
            .post("/auth/login")
            .send({ email: "admin@example.com", password: "Admin123!@" });

        accessToken = loginResponse.body.accessToken;
    });

    it("POST /slapolicies - deve criar uma política de SLA", () => {
        return request(app.getHttpServer())
            .post("/slapolicies")
            .set("Authorization", `Bearer ${accessToken}`)
            .send({
                priority: "P1",
                responseTimeInMinutes: 60,
                resolutionTimeInMinutes: 240,
            })
            .expect(201)
            .expect((res) => {
                expect(res.body.priority).toBe("P1");
                expect(res.body.responseTimeInMinutes).toBe(60);
            });
    });

    it("GET /slapolicies - deve listar todas as políticas", () => {
        return request(app.getHttpServer())
            .get("/slapolicies")
            .set("Authorization", `Bearer ${accessToken}`)
            .expect(200)
            .expect((res) => {
                expect(res.body).toBeInstanceOf(Array);
                expect(res.body.length).toBeGreaterThan(0);
            });
    });

    it("POST /incidents - deve aplicar SLA automaticamente ao criar incidente", () => {
        return request(app.getHttpServer())
            .post("/incidents")
            .set("Authorization", `Bearer ${accessToken}`)
            .send({
                title: "Teste SLA",
                priority: "P1",
                categoryId: "cat-123",
            })
            .expect(201)
            .expect((res) => {
                expect(res.body.slaPolicyId).toBeDefined();
                expect(res.body.slaResponseDue).toBeDefined();
                expect(res.body.slaResolutionDue).toBeDefined();
            });
    });

    afterAll(async () => {
        await app.close();
    });
});
```
