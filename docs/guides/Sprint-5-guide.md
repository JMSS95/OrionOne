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
