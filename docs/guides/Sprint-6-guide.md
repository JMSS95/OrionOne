# Guia de Implementação - Sprint 6

**Sprint:** 6
**Período:** 16 de Janeiro a 31 de Janeiro de 2026
**Foco:** Dashboard de Métricas, Notificações por Email e Polimento Geral
**Status:** Planeado

---

## 1. Visão Geral

Este sprint final do MVP concentra-se em fornecer visibilidade sobre as operações de ITSM e em melhorar a comunicação da equipa através de duas features principais: um **Dashboard de Métricas** e **Notificações por Email**.

O **Dashboard** fornecerá aos gestores e agentes uma visão geral e em tempo real das principais métricas de incidentes, como o número de incidentes abertos, a distribuição por prioridade e o estado atual. Utilizaremos gráficos e cartões de estatísticas para uma visualização clara e eficaz.

As **Notificações por Email** garantirão que as partes interessadas sejam informadas sobre eventos importantes, como a criação de um novo incidente, a atribuição a um agente ou a adição de um novo comentário.

Adicionalmente, este sprint inclui um período de **polimento e buffer** para refinar a UX/UI geral da aplicação, corrigir bugs menores e garantir que a plataforma está estável e pronta para o lançamento.

## 2. User Stories / Requisitos

### Dashboard de Métricas

-   **[Em Curso] US6.1:** Como gestor de TI, quero ver um dashboard com as principais métricas de incidentes (total, abertos, fechados, por prioridade, por estado) para poder avaliar rapidamente a carga de trabalho e o estado das operações.
-   **[Em Curso] US6.2:** Como agente de suporte, quero ter acesso a um dashboard para visualizar os incidentes que me foram atribuídos e a sua prioridade, para que eu possa gerir o meu trabalho de forma mais eficiente.
-   **[Em Curso] US6.3:** Como gestor, quero ver um gráfico de barras ou circular que mostre a distribuição de incidentes por prioridade e por estado, para identificar tendências e alocar recursos adequadamente.
-   **[Em Curso] US6.4:** Como gestor, quero ver uma lista dos 5 incidentes atualizados mais recentemente no dashboard, para acompanhar a atividade recente da equipa.

### Notificações por Email

-   **[Em Curso] US6.5:** Como agente, quero receber uma notificação por email quando um novo incidente me for atribuído, para que eu possa começar a trabalhar nele o mais rápido possível.
-   **[Em Curso] US6.6:** Como criador de um incidente, quero receber um email de confirmação quando o meu incidente for registado, para saber que o meu pedido foi recebido.
-   **[Em Curso] US6.7:** Como participante de um incidente (criador ou atribuído), quero receber uma notificação por email quando um novo comentário for adicionado, para me manter atualizado sobre a discussão.
-   **[Em Curso] US6.8:** Como utilizador, quero que os emails de notificação tenham um formato profissional e incluam links diretos para os incidentes, para facilitar o acesso rápido.

**Pré-requisitos:**

-   Sprints 1 a 5 completos (autenticação, incidentes, comentários, anexos, KB e SLA).
-   Configuração de SMTP disponível para envio de emails.

## 3. Plano de Implementação

A implementação será dividida em fases, começando pelo backend para expor os dados e a lógica de notificação, seguido pelo frontend para visualização. Este sprint não requer alterações na base de dados, pois utilizaremos os modelos existentes.

---

## Funcionalidade 6.1 & 6.2: Dashboard de Métricas e Notificações por Email

**Objetivo:** Implementar um dashboard com métricas em tempo real e um sistema de notificações por email para melhorar a visibilidade e comunicação da equipa.

---

### **Fase 1: Backend (Nest.js)**

A implementação do backend será focada em duas áreas: criar um endpoint para servir os dados do dashboard e configurar um serviço para enviar notificações por email.

#### **3.1. Módulo de Dashboard**

Primeiro, vamos criar a estrutura para o novo módulo de dashboard.

1.  **Gerar Módulo, Controller e Service:**
    Use o Nest CLI para gerar os ficheiros necessários.

    ```bash
    nest generate module dashboard
    nest generate controller dashboard --no-spec
    nest generate service dashboard --no-spec
    ```

2.  **Definir o DTO de Resposta (`DashboardStatsDto`)**

    **Ficheiro:** `nest-backend/src/dashboard/dto/dashboard-stats.dto.ts`

    **Objetivo:**
    Definir a estrutura de dados que o nosso endpoint de estatísticas irá retornar. Este DTO não necessita de validações do `class-validator`, pois é apenas um contrato de resposta (não aceita input do utilizador).

    **Campos do `DashboardStatsDto`:**

    -   `totalIncidents`: `number` - O número total de incidentes no sistema, independentemente do estado.
    -   `openIncidents`: `number` - O número de incidentes que não estão nos estados `CLOSED` ou `RESOLVED`. Esta métrica ajuda a identificar a carga de trabalho atual.
    -   `closedIncidents`: `number` - O número de incidentes fechados ou resolvidos. Calculado como `totalIncidents - openIncidents`.
    -   `incidentsByStatus`: `Array<{ status: string; count: number }>` - Uma lista de objetos, cada um contendo um `status` (ex: OPEN, IN_PROGRESS, etc.) e a contagem de incidentes nesse estado. Útil para gráficos de distribuição.
    -   `incidentsByPriority`: `Array<{ priority: string; count: number }>` - Uma lista de objetos, cada um contendo uma `priority` (P1, P2, P3, P4) e a contagem de incidentes nessa prioridade. Permite identificar quais prioridades têm mais volume.
    -   `recentlyUpdated`: `Array<{ id: string; title: string; updatedAt: Date }>` - Uma lista dos 5 incidentes atualizados mais recentemente. Fornece visibilidade sobre a atividade recente da equipa.

    **Documentação:**
    [Guia Oficial do Nest.js sobre DTOs](https://docs.nestjs.com/openapi/types-and-parameters)

3.  **Implementar a Lógica no `DashboardService`**
    O serviço será responsável por consultar o banco de dados e agregar as métricas.

    -   **`getStats()`**:
        -   Use `this.prisma.incident.count()` para obter o `totalIncidents`.
        -   Use `this.prisma.incident.count({ where: { status: { notIn: [Status.CLOSED, Status.RESOLVED] } } })` para obter `openIncidents`.
        -   Calcule `closedIncidents` subtraindo `openIncidents` de `totalIncidents`.
        -   Use `this.prisma.incident.groupBy({ by: ['status'], _count: { id: true } })` para agregar incidentes por estado. Mapeie o resultado para o formato esperado.
        -   Use `this.prisma.incident.groupBy({ by: ['priority'], _count: { id: true } })` para agregar incidentes por prioridade. Mapeie o resultado.
        -   Use `this.prisma.incident.findMany({ orderBy: { updatedAt: 'desc' }, take: 5 })` para obter os 5 incidentes atualizados mais recentemente.
        -   Retorne o objeto `DashboardStatsDto` completo.

4.  **Expor o Endpoint no `DashboardController`**
    Crie um endpoint `GET /api/dashboard/stats` que seja protegido e chame o serviço.

    -   Adicione o decorador `@UseGuards(JwtAuthGuard)` ao controller para garantir que apenas utilizadores autenticados possam aceder.
    -   Crie um método `getStats()` com o decorador `@Get('stats')` que simplesmente chama e retorna o resultado de `this.dashboardService.getStats()`.

#### **3.2. Módulo de Notificações por Email**

Vamos integrar o `nodemailer` para o envio de emails transacionais.

1.  **Instalar Dependências:**

    ```bash
    npm install --save @nestjs-modules/mailer nodemailer
    npm install --save-dev @types/nodemailer
    ```

2.  **Configurar o `MailerModule`**
    No `app.module.ts`, importe e configure o `MailerModule` para se conectar ao seu provedor de SMTP usando variáveis de ambiente.

    ```typescript
    // nest-backend/src/app.module.ts
    import { MailerModule } from "@nestjs-modules/mailer";
    // ...
    @Module({
        imports: [
            // ...
            MailerModule.forRoot({
                transport: {
                    host: process.env.EMAIL_HOST,
                    port: parseInt(process.env.EMAIL_PORT, 10),
                    secure: process.env.EMAIL_SECURE === "true",
                    auth: {
                        user: process.env.EMAIL_USER,
                        pass: process.env.EMAIL_PASS,
                    },
                },
                defaults: {
                    from: `"OrionOne" <${process.env.EMAIL_FROM}>`,
                },
            }),
        ],
        // ...
    })
    export class AppModule {}
    ```

    Adicione as variáveis correspondentes ao seu ficheiro `.env`.

3.  **Criar e Implementar o `EmailService`**
    Crie um módulo e serviço dedicados para encapsular a lógica de envio de emails.

    ```bash
    nest generate module email
    nest generate service email --no-spec
    ```

    -   **`sendIncidentCreationConfirmation(user: User, incident: Incident)`**: Envia um email para o `user.email` a confirmar que o `incident` foi criado.
    -   **`sendIncidentAssignmentNotification(assignee: User, incident: Incident)`**: Envia um email para o `assignee.email` a notificá-lo de que o `incident` lhe foi atribuído.
    -   **`sendNewCommentNotification(user: User, incident: Incident, comment: Comment)`**: Envia um email para o `user.email` (que pode ser o criador ou o agente) a informar que um novo `comment` foi adicionado ao `incident`.

4.  **Integrar o `EmailService` nos Fluxos Existentes**
    -   Injete o `EmailService` no `IncidentsService`.
        -   Após a criação de um incidente, chame `sendIncidentCreationConfirmation`.
        -   Ao atualizar o `assignedToId` de um incidente, chame `sendIncidentAssignmentNotification`.
    -   Injete o `EmailService` no `CommentsService`.
        -   Após a criação de um comentário, chame `sendNewCommentNotification` para o criador do incidente e para o agente atribuído (se existirem e forem diferentes de quem comentou).

---

### **Fase 2: Frontend (Next.js)**

#### **3.3. Página e Componentes do Dashboard**

1.  **Criar a Página do Dashboard:**
    Crie a estrutura da página em `next-frontend/app/dashboard/page.tsx`. Esta página será a principal consumidora dos dados do backend.

2.  **Instalar Biblioteca de Gráficos:**
    `shadcn/charts` é uma excelente opção que se integra bem com o resto do UI kit.

    ```bash
    npx shadcn-ui@latest add charts
    ```

3.  **Criar Hook de Fetch de Dados com TanStack Query:**
    Em `next-frontend/lib/hooks/use-dashboard-stats.ts`, crie um hook para buscar os dados do endpoint `/api/dashboard/stats` de forma eficiente, com caching.

    ```typescript
    // next-frontend/lib/hooks/use-dashboard-stats.ts
    import { useQuery } from "@tanstack/react-query";
    import axios from "axios";
    import { DashboardStatsDto } from "@/lib/dto/dashboard-stats.dto"; // Crie este DTO no frontend também

    const fetchDashboardStats = async (): Promise<DashboardStatsDto> => {
        const { data } = await axios.get("/api/dashboard/stats");
        return data;
    };

    export const useDashboardStats = () => {
        return useQuery<DashboardStatsDto, Error>({
            queryKey: ["dashboardStats"],
            queryFn: fetchDashboardStats,
        });
    };
    ```

4.  **Criar Componentes de Visualização:**

    Divida a UI em componentes reutilizáveis dentro de `next-frontend/components/dashboard/` para garantir manutenibilidade e reutilização de código.

    **`StatCard.tsx`**:
    Um componente de cartão para exibir métricas individuais de forma destacada.

    -   **Props**: `title` (string), `value` (number), `icon` (React.ReactNode), `trend` (opcional, para mostrar aumento/diminuição).
    -   **Layout**: Utilize `Card` do shadcn/ui. Exiba o ícone no topo, o valor em fonte grande e o título por baixo.
    -   **Exemplo de uso**: `<StatCard title="Incidentes Abertos" value={42} icon={<AlertCircle />} />`

    **`IncidentsByPriorityChart.tsx`**:
    Um gráfico de rosca (donut chart) para visualizar a distribuição de incidentes por prioridade.

    -   **Props**: `data` (array de `{ priority: string; count: number }`).
    -   **Implementação**: Use o componente `DonutChart` do shadcn/charts. Configure cores distintas para cada prioridade (P1: vermelho, P2: laranja, P3: amarelo, P4: verde).
    -   **Tooltip**: Mostre a prioridade e o número de incidentes ao passar o cursor.

    **`IncidentsByStatusChart.tsx`**:
    Um gráfico de barras para mostrar a distribuição de incidentes por estado.

    -   **Props**: `data` (array de `{ status: string; count: number }`).
    -   **Implementação**: Use o componente `BarChart` do shadcn/charts. Ordene os estados numa sequência lógica (OPEN, IN_PROGRESS, RESOLVED, CLOSED).
    -   **Eixos**: O eixo X representa os estados, o eixo Y representa a contagem.

    **`RecentActivityFeed.tsx`**:
    Uma lista de atividade recente que exibe os últimos incidentes atualizados.

    -   **Props**: `incidents` (array de `{ id: string; title: string; updatedAt: Date }`).
    -   **Implementação**: Renderize cada incidente num item de lista com o título como link para `/incidents/[id]` e a data relativa (ex: "há 5 minutos") usando `date-fns`.
    -   **Estado vazio**: Se não houver incidentes recentes, mostre uma mensagem "Nenhuma atividade recente".

5.  **Montar o Layout do Dashboard:**
    Em `next-frontend/app/dashboard/page.tsx`, use o hook `useDashboardStats` para obter os dados. Apresente um estado de `loading` e de `error`. Se os dados forem carregados com sucesso, organize os componentes de visualização numa grelha (grid) para uma apresentação clara e moderna.

---

### **Fase 3: Testes**

#### **3.4. Testes de Backend**

-   **Testes Unitários (`DashboardService`)**
    Crie `dashboard.service.spec.ts` para isolar e testar a lógica de agregação de dados.

    ```typescript
    // nest-backend/src/dashboard/dashboard.service.spec.ts
    import { Test, TestingModule } from "@nestjs/testing";
    import { DashboardService } from "./dashboard.service";
    import { PrismaService } from "../prisma/prisma.service";
    import { Status, Priority } from "@prisma/client";

    const mockPrismaService = {
        incident: {
            count: jest.fn(),
            groupBy: jest.fn(),
            findMany: jest.fn(),
        },
    };

    describe("DashboardService", () => {
        let service: DashboardService;
        let prisma: typeof mockPrismaService;

        beforeEach(async () => {
            const module: TestingModule = await Test.createTestingModule({
                providers: [
                    DashboardService,
                    { provide: PrismaService, useValue: mockPrismaService },
                ],
            }).compile();

            service = module.get<DashboardService>(DashboardService);
            prisma = module.get(PrismaService);
        });

        it("should calculate and return dashboard stats correctly", async () => {
            // Mock das chamadas do Prisma
            prisma.incident.count
                .mockResolvedValueOnce(100) // totalIncidents
                .mockResolvedValueOnce(40); // openIncidents

            prisma.incident.groupBy
                .mockResolvedValueOnce([
                    // incidentsByStatus
                    { status: Status.OPEN, _count: { id: 30 } },
                    { status: Status.IN_PROGRESS, _count: { id: 10 } },
                ])
                .mockResolvedValueOnce([
                    // incidentsByPriority
                    { priority: Priority.HIGH, _count: { id: 50 } },
                    { priority: Priority.MEDIUM, _count: { id: 50 } },
                ]);

            prisma.incident.findMany.mockResolvedValueOnce([
                // recentlyUpdated
                { id: "1", title: "Recent Incident", updatedAt: new Date() },
            ]);

            const stats = await service.getStats();

            expect(stats.totalIncidents).toBe(100);
            expect(stats.openIncidents).toBe(40);
            expect(stats.closedIncidents).toBe(60);
            expect(stats.incidentsByStatus).toHaveLength(2);
            expect(stats.incidentsByStatus[0].count).toBe(30);
            expect(stats.incidentsByPriority).toHaveLength(2);
            expect(stats.recentlyUpdated).toHaveLength(1);
        });
    });
    ```

-   **Testes Unitários (`EmailService`)**

    **Ficheiro:** `nest-backend/src/email/email.service.spec.ts`

    **Objetivo:**
    Garantir que o serviço de email tenta enviar os emails com os dados corretos e que os métodos são chamados nas condições apropriadas.

    **Testes Essenciais:**

    ```typescript
    // nest-backend/src/email/email.service.spec.ts
    import { Test, TestingModule } from "@nestjs/testing";
    import { EmailService } from "./email.service";
    import { MailerService } from "@nestjs-modules/mailer";
    import { User, Incident } from "@prisma/client";

    const mockMailerService = {
        sendMail: jest.fn(),
    };

    describe("EmailService", () => {
        let service: EmailService;
        let mailerService: typeof mockMailerService;

        beforeEach(async () => {
            const module: TestingModule = await Test.createTestingModule({
                providers: [
                    EmailService,
                    { provide: MailerService, useValue: mockMailerService },
                ],
            }).compile();

            service = module.get<EmailService>(EmailService);
            mailerService = module.get(MailerService);
            mailerService.sendMail.mockClear();
        });

        it("deve enviar email de confirmação de criação de incidente", async () => {
            const user = { email: "test@user.com", name: "Test User" } as User;
            const incident = {
                id: "inc-123",
                title: "Test Incident",
            } as Incident;

            await service.sendIncidentCreationConfirmation(user, incident);

            expect(mailerService.sendMail).toHaveBeenCalledWith(
                expect.objectContaining({
                    to: "test@user.com",
                    subject: expect.stringContaining(
                        "Incidente #inc-123 Criado"
                    ),
                })
            );
        });

        it("deve enviar email de atribuição de incidente ao agente", async () => {
            const assignee = {
                email: "agent@example.com",
                name: "Agent",
            } as User;
            const incident = {
                id: "inc-456",
                title: "Urgent Issue",
            } as Incident;

            await service.sendIncidentAssignmentNotification(
                assignee,
                incident
            );

            expect(mailerService.sendMail).toHaveBeenCalledWith(
                expect.objectContaining({
                    to: "agent@example.com",
                    subject: expect.stringContaining(
                        "Novo Incidente Atribuído"
                    ),
                })
            );
        });

        it("deve incluir o título do incidente no corpo do email", async () => {
            const user = { email: "test@user.com", name: "Test User" } as User;
            const incident = {
                id: "inc-789",
                title: "Network Down",
            } as Incident;

            await service.sendIncidentCreationConfirmation(user, incident);

            const callArgs = mailerService.sendMail.mock.calls[0][0];
            expect(callArgs.html).toContain("Network Down");
        });
    });
    ```

-   **Testes E2E (`DashboardController`)**
    Adicione um novo teste ao ficheiro `test/app.e2e-spec.ts` para verificar o comportamento do endpoint do dashboard.

    ```typescript
    // Em test/app.e2e-spec.ts
    describe("DashboardController (e2e)", () => {
        // ... (setup existente com app, prisma, etc.)

        it("/api/dashboard/stats (GET) - should return dashboard statistics for authenticated user", async () => {
            // Crie dados de teste
            await prisma.incident.create({
                data: {
                    title: "E2E Test Incident",
                    description: "...",
                    status: "OPEN",
                    priority: "HIGH",
                    reporterId: defaultUser.id,
                },
            });

            const response = await request(app.getHttpServer())
                .get("/dashboard/stats")
                .set("Authorization", `Bearer ${accessToken}`);

            expect(response.status).toBe(200);
            expect(response.body).toBeDefined();
            expect(response.body).toHaveProperty("totalIncidents");
            expect(response.body.totalIncidents).toBeGreaterThan(0);
            expect(response.body).toHaveProperty("incidentsByStatus");
            expect(response.body).toHaveProperty("incidentsByPriority");
        });
    });
    ```

#### **3.5. Testes de Frontend (Playwright)**

-   **Teste E2E da Página do Dashboard:**

    **Ficheiro:** `tests/e2e/dashboard.spec.ts`

    **Objetivo:**
    Validar que a página do dashboard carrega corretamente, exibe as métricas esperadas e renderiza os componentes de visualização.

    **Testes Essenciais:**

    ```typescript
    // tests/e2e/dashboard.spec.ts
    import { test, expect } from "@playwright/test";

    test.describe("Dashboard Page", () => {
        test.beforeEach(async ({ page }) => {
            // Faça login antes de cada teste
            await page.goto("/login");
            await page.fill('input[name="email"]', "admin@orionone.io");
            await page.fill('input[name="password"]', "password");
            await page.click('button[type="submit"]');
            await expect(page).toHaveURL("/dashboard");
        });

        test("deve exibir cartões de estatísticas com números corretos", async ({
            page,
        }) => {
            // Mock da resposta da API
            await page.route("/api/dashboard/stats", async (route) => {
                await route.fulfill({
                    status: 200,
                    contentType: "application/json",
                    body: JSON.stringify({
                        totalIncidents: 10,
                        openIncidents: 5,
                        closedIncidents: 5,
                        incidentsByStatus: [{ status: "OPEN", count: 5 }],
                        incidentsByPriority: [{ priority: "HIGH", count: 10 }],
                        recentlyUpdated: [
                            {
                                id: "1",
                                title: "Mocked Incident",
                                updatedAt: new Date(),
                            },
                        ],
                    }),
                });
            });

            await page.goto("/dashboard");

            // Verifique se os cartões de estatísticas exibem os números corretos
            await expect(page.getByText("Total Incidents")).toBeVisible();
            await expect(page.getByText("10")).toBeVisible();

            await expect(page.getByText("Open Incidents")).toBeVisible();
            await expect(page.getByText("5")).toBeVisible();

            await expect(page.getByText("Closed Incidents")).toBeVisible();
            await expect(page.getByText("5")).toBeVisible();
        });

        test("deve renderizar gráficos de distribuição", async ({ page }) => {
            await page.route("/api/dashboard/stats", async (route) => {
                await route.fulfill({
                    status: 200,
                    contentType: "application/json",
                    body: JSON.stringify({
                        totalIncidents: 20,
                        openIncidents: 10,
                        closedIncidents: 10,
                        incidentsByStatus: [
                            { status: "OPEN", count: 8 },
                            { status: "IN_PROGRESS", count: 2 },
                        ],
                        incidentsByPriority: [
                            { priority: "P1", count: 5 },
                            { priority: "P2", count: 15 },
                        ],
                        recentlyUpdated: [],
                    }),
                });
            });

            await page.goto("/dashboard");

            // Verifique se os títulos dos gráficos estão visíveis
            await expect(page.getByText("Incidents by Status")).toBeVisible();
            await expect(page.getByText("Incidents by Priority")).toBeVisible();
        });

        test("deve exibir lista de atividade recente", async ({ page }) => {
            await page.route("/api/dashboard/stats", async (route) => {
                await route.fulfill({
                    status: 200,
                    contentType: "application/json",
                    body: JSON.stringify({
                        totalIncidents: 10,
                        openIncidents: 5,
                        closedIncidents: 5,
                        incidentsByStatus: [],
                        incidentsByPriority: [],
                        recentlyUpdated: [
                            {
                                id: "inc-1",
                                title: "Server Down",
                                updatedAt: new Date(),
                            },
                            {
                                id: "inc-2",
                                title: "Network Issue",
                                updatedAt: new Date(),
                            },
                        ],
                    }),
                });
            });

            await page.goto("/dashboard");

            // Verifique se a secção de atividade recente é renderizada
            await expect(page.getByText("Recent Activity")).toBeVisible();
            await expect(page.getByText("Server Down")).toBeVisible();
            await expect(page.getByText("Network Issue")).toBeVisible();
        });

        test("deve redirecionar para login se não autenticado", async ({
            page,
        }) => {
            // Limpe os cookies de autenticação
            await page.context().clearCookies();
            await page.goto("/dashboard");

            // Deve redirecionar para a página de login
            await expect(page).toHaveURL("/login");
        });
    });
    ```

    **Documentação:**
    [Guia Oficial do Playwright sobre Mocking de APIs](https://playwright.dev/docs/mocking)

## 4. Documentação de Referência

-   **Nest.js Mailer:** [https://docs.nestjs.com/techniques/mailer](https://docs.nestjs.com/techniques/mailer)
-   **Nodemailer:** [https://nodemailer.com/](https://nodemailer.com/)
-   **Prisma `groupBy`:** [https://www.prisma.io/docs/reference/api-reference/prisma-client-reference#groupby](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference#groupby)
-   **shadcn/charts:** [https://ui.shadcn.com/charts](https://ui.shadcn.com/charts)
-   **TanStack Query (React):** [https://tanstack.com/query/latest/docs/react/overview](https://tanstack.com/query/latest/docs/react/overview)
-   **Playwright Mocking:** [https://playwright.dev/docs/mocking](https://playwright.dev/docs/mocking)

## 5. Testes Manuais e Casos de Uso

-   **Dashboard:**
    1.  Aceda à página do dashboard sem estar autenticado. Deve ser redirecionado para o login.
    2.  Após o login, navegue para `/dashboard`. Verifique se todos os componentes carregam sem erros.
    3.  Crie, atualize e feche alguns incidentes. Volte ao dashboard e verifique se as métricas (total, abertos, fechados) são atualizadas.
    4.  Verifique se os gráficos refletem a distribuição correta de incidentes por estado e prioridade.
    5.  Verifique se a lista de "Atividade Recente" mostra os últimos 5 incidentes modificados.
-   **Notificações por Email:**
    1.  Crie um novo incidente. Verifique se o criador recebe um email de confirmação.
    2.  Atribua o incidente a um agente. Verifique se o agente atribuído recebe um email de notificação.
    3.  Adicione um comentário a um incidente. Verifique se o criador e o agente atribuído recebem uma notificação por email.
    4.  Verifique o formato e o conteúdo dos emails para garantir que são claros e profissionais.

## 6. Definição de "Feito" (Definition of Done)

### Backend

-   [ ] O módulo de dashboard (`DashboardModule`, `Service`, `Controller`) está implementado no backend.
-   [ ] O endpoint `GET /api/dashboard/stats` está funcional, protegido com `JwtAuthGuard` e retorna os dados corretos no formato `DashboardStatsDto`.
-   [ ] O módulo de email (`EmailModule`, `EmailService`) está implementado e configurado com o `MailerModule`.
-   [ ] As notificações por email são enviadas corretamente nos seguintes eventos:
    -   Criação de incidente (confirmação para o criador)
    -   Atribuição de incidente (notificação para o agente)
    -   Novo comentário (notificação para criador e agente atribuído)
-   [ ] Os emails têm um formato profissional e incluem links diretos para os incidentes.
-   [ ] Testes unitários para `DashboardService` foram criados e cobrem:
    -   Cálculo correto de `totalIncidents`, `openIncidents`, `closedIncidents`
    -   Agregação correta de `incidentsByStatus` e `incidentsByPriority`
    -   Retorno dos 5 incidentes atualizados mais recentemente
-   [ ] Testes unitários para `EmailService` foram criados e cobrem:
    -   Envio de email de confirmação de criação
    -   Envio de email de atribuição
    -   Envio de email de novo comentário
    -   Validação do conteúdo dos emails (destinatário, assunto, corpo)
-   [ ] Testes E2E para o endpoint `/api/dashboard/stats` foram criados e passam.

### Frontend

-   [ ] A página do dashboard (`/dashboard`) existe no frontend e está acessível através do menu de navegação.
-   [ ] A página do dashboard busca e exibe as métricas do backend usando TanStack Query.
-   [ ] Estados de `loading`, `error` e `success` são tratados corretamente na UI.
-   [ ] Os componentes de visualização foram criados:
    -   [ ] `StatCard.tsx` - Exibe métricas individuais
    -   [ ] `IncidentsByPriorityChart.tsx` - Gráfico de rosca
    -   [ ] `IncidentsByStatusChart.tsx` - Gráfico de barras
    -   [ ] `RecentActivityFeed.tsx` - Lista de atividade recente
-   [ ] Os gráficos de distribuição por estado e prioridade são exibidos corretamente e são responsivos.
-   [ ] A lista de atividade recente mostra os 5 incidentes atualizados mais recentemente com links funcionais.
-   [ ] Testes E2E (Playwright) para a página do dashboard foram criados e cobrem:
    -   [ ] Exibição correta dos cartões de estatísticas
    -   [ ] Renderização dos gráficos
    -   [ ] Exibição da lista de atividade recente
    -   [ ] Redirecionamento para login se não autenticado

### Geral

-   [ ] A documentação (`Sprint-6-guide.md`) está completa e alinhada com os outros sprints.
-   [ ] Todos os casos de teste manual foram executados e aprovados.
-   [ ] O código foi revisto (code review) e integrado na branch principal.
-   [ ] Foi realizado um ciclo de polimento geral na UI/UX da aplicação:
    -   [ ] Revisão de espaçamentos e alinhamentos
    -   [ ] Consistência de cores e tipografia
    -   [ ] Testes de responsividade em diferentes dispositivos
    -   [ ] Validação de acessibilidade (contraste, navegação por teclado)
-   [ ] A aplicação foi testada end-to-end num ambiente de staging.
-   [ ] Toda a cobertura de testes está acima de 80% (backend e frontend).
