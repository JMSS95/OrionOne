# Guia de Implementação Detalhado do Sprint 2: Incidentes & Rich Text (Essential)

## Visão Geral do Sprint

**Objetivo:**
Implementar sistema completo de gestão de incidentes com Rich Text (Tiptap) e filtros básicos.

**User Stories:**

-   [Em Curso] US2.1: Criar Incidente com Rich Text (Essential)
-   [Em Curso] US2.2: Pesquisa Simples (PostgreSQL ILIKE)
-   [Em Curso] US2.3: Listagem com Filtros Básicos
-   [Em Curso] US2.4: Atualizar Incidente

**Pré-requisitos:**
Sprint 1 completo (Autenticação funcionando, Docker containers a correr)

---

## Aplicando as Tecnologias Fundamentais (Sprint 0)

Neste sprint, ao criar o módulo de incidentes, vamos aplicar várias das tecnologias configuradas no Sprint 0 para garantir que a nova funcionalidade é robusta, segura e bem documentada.

### 1. Documentação de API com Swagger

**Objetivo:** Documentar todos os novos endpoints do CRUD de incidentes.

**Ações:**
No ficheiro `incidents.controller.ts`, use os decoradores `@ApiTags`, `@ApiOperation`, `@ApiBearerAuth` e `@ApiQuery` para agrupar, descrever, proteger e documentar os parâmetros de todos os endpoints de incidentes, incluindo filtros e paginação.

**Documentação:**
[Guia Oficial do Nest.js sobre OpenAPI (Swagger)](https://docs.nestjs.com/openapi/introduction)

### 2. Logging com Winston

**Objetivo:** Registar eventos importantes no ciclo de vida dos incidentes.

**Ações:**
No `incidents.service.ts`, injete o `LoggerService` e adicione logs para operações chave: criação e atualização de incidentes, pesquisas efetuadas pelos utilizadores e quaisquer erros que ocorram durante o processo.

**Documentação:**
[Guia Oficial do `nest-winston`](https://github.com/gremo/nest-winston)

### 3. Autorização com CASL

**Objetivo:** Controlar quem pode criar, ver, editar e apagar incidentes.

**Ações:**

-   **Definir Habilidades:** No `casl-ability.factory.ts`, defina as permissões para o `subject` 'Incident', diferenciando as ações permitidas para os roles `ADMIN`, `AGENT` e `USER`.
-   **Verificar Permissões:** Nos métodos do `incidents.service.ts`, utilize a `CaslAbilityFactory` para verificar as permissões do utilizador antes de executar qualquer lógica de acesso ou modificação de dados, lançando uma `ForbiddenException` se a ação não for permitida.

**Documentação:**
[Guia Oficial do CASL](https://casl.js.org/v6/en/guide/intro)
[Integração do CASL com Nest.js](https://docs.nestjs.com/security/authorization#casl)

### 4. Validação de DTOs

**Objetivo:** Garantir que os dados de entrada para criar e atualizar incidentes são válidos.

**Ações:**
Utilize os decoradores do `class-validator` nos DTOs (`CreateIncidentDto`, `UpdateIncidentDto`, e DTOs de filtro) para garantir a integridade dos dados. Valide tipos, enums, e a presença ou opcionalidade dos campos.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação](https://docs.nestjs.com/techniques/validation)

### 5. Compressão e Configuração

-   **Compressão (Gzip):** Esta funcionalidade, ativa globalmente desde o Sprint 0, irá comprimir automaticamente as respostas JSON da listagem de incidentes. Isto é especialmente útil para grandes volumes de dados, reduzindo o tempo de carregamento no frontend.
-   **ConfigModule:** Utilize o `ConfigService` para gerir configurações relacionadas com incidentes que possam necessitar de ajuste, como o número de itens por página na paginação. Ex: `this.configService.get<number>('PAGINATION_LIMIT', 25)`.

**Documentação:**
[Guia Oficial do Nest.js sobre Configuration](https://docs.nestjs.com/techniques/configuration)

### 6. Editor de Rich Text com Tiptap

**Objetivo:** Implementar o editor Tiptap para o campo `description` dos incidentes, permitindo formatação essencial.

**Ações:**

-   **Instalação (Frontend):** Instale o Tiptap e as extensões necessárias (`@tiptap/react`, `@tiptap/starter-kit`) no projeto Next.js.
-   **Configuração:** Configure o editor com funcionalidades essenciais: **negrito**, **itálico**, **listas** (ordenadas/não ordenadas), **blocos de código**, **links** e **headings**.
-   **Markdown Shortcuts:** Ative os atalhos de Markdown (ex: `##` para headings, `**` para negrito, `--` para listas).
-   **Armazenamento:** O conteúdo do Tiptap deve ser armazenado como **JSON** no campo `description` do modelo `Incident` (tipo `Json` no Prisma).
-   **Limitações MVP:** **Excluir** funcionalidades avançadas como paste de imagens, tabelas, embeds e mentions (movidas para Post-MVP P2).

**Documentação:**
[Guia Oficial do Tiptap](https://tiptap.dev/docs/editor/introduction)
[Tiptap React Guide](https://tiptap.dev/docs/editor/getting-started/install/react)

---

## Funcionalidade 2.1, 2.3, 2.4: CRUD de Incidentes, Rich Text & Filtros

### Fase 1: Base de Dados (Prisma & PostgreSQL)

#### 1.1. Localizar e Editar o Schema

**Ficheiro:** `nest-backend/prisma/schema.prisma`

**Ação:**
Abra o ficheiro para definir os modelos relacionados com incidentes.

#### 1.2. Definir o Modelo Incident

**Objetivo:**
Adicione o modelo `Incident` com os tipos de dados apropriados.

**Campos Essenciais:**

-   `id`, `incidentNumber` (use `@unique` e lógica customizada no backend para geração)
-   `title` (com `@db.VarChar(255)`)
-   **Rich Text:** `description` do tipo **`Json`** - crucial para preservar a estrutura do Tiptap
-   **Enums:** Crie e use os enums `IncidentStatus` (NEW, IN_PROGRESS, RESOLVED, CLOSED) e `IncidentPriority` (P1, P2, P3, P4)
-   **Relações:** Crie as relações `requester` e `assignee` com o modelo `User` (muitos-para-um) e a relação `category` com o modelo `Category` (muitos-para-um)

**Documentação:**
[Guia Oficial do Prisma sobre Modelos de Dados, Enums e Tipos JSON](https://www.prisma.io/docs/orm/prisma-schema/data-model)

#### 1.3. Definir Modelo Category

**Objetivo:**
Crie o `model Category` (para categorização de incidentes).

**Descrição:**
Categoria simples com campos: `id`, `name` (Hardware, Software, Network, Access, etc.), `description`.

**NOTA:** `SavedFilter` foi movido para Post-MVP P3. No MVP, usamos apenas quick filters (All, My Incidents, Unassigned, Open, Closed).

#### 1.4. Executar a Migração

**Comando:**

```bash
npm run prisma:migrate:dev -- --name add_incident_tables
```

**Documentação:**
[Guia Oficial do Prisma sobre Migrações](https://www.prisma.io/docs/orm/prisma-migrate/getting-started)

#### 1.5. Criar Seeds

**Ficheiro:** `nest-backend/prisma/seed.ts`

**Objetivo:**
Edite o ficheiro para criar categorias iniciais e mais de 50 incidentes de teste com dados realistas (incluindo JSON na descrição).

**Documentação:**
[Guia Oficial do Prisma sobre Seeding](https://www.prisma.io/docs/orm/prisma-migrate/workflows/seeding)

### Fase 2: Backend (Nest.js)

#### 2.1. Gerar o Recurso e DTOs

**Comando:**

```bash
nest g resource incidents --no-spec
```

**Ação:**
Crie os ficheiros `CreateIncidentDto.ts` e `UpdateIncidentDto.ts` dentro de `nest-backend/src/incidents/dto/`.

**`CreateIncidentDto.ts`:**
Defina a estrutura de dados para criar um novo incidente. Os validadores (`class-validator`) garantem a integridade dos dados na entrada da API.

-   `title`: Deve ser uma `string` e não pode estar vazio. A API deve rejeitar pedidos sem título.
-   `description`: Deve ser um objeto JSON, preparado para receber a estrutura de dados do editor Tiptap.
-   `priority`: Deve corresponder a um dos valores definidos no enum `IncidentPriority` do Prisma (ex: `P1`, `P2`).
-   `categoryId`: Deve ser o ID (`string`) de uma categoria existente.

**`UpdateIncidentDto.ts`:**
Defina os campos que podem ser atualizados num incidente existente. Todos os campos devem ser opcionais, permitindo atualizações parciais.

-   `title`: Opcional, para renomear o incidente.
-   `description`: Opcional, para editar o conteúdo rich text.
-   `status`: Opcional, para mudar o estado do incidente (ex: de `NEW` para `IN_PROGRESS`).
-   `priority`: Opcional, para re-priorizar o incidente.
-   `assigneeId`: Opcional, para atribuir ou reatribuir o incidente a um utilizador.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação (class-validator)](https://docs.nestjs.com/techniques/validation)

#### 2.2. Implementar o IncidentsService - Geração do Número de Incidente (US2.1)

**Ficheiro:** `nest-backend/src/incidents/incidents.service.ts`

**Objetivo:**
No método `create()` do `IncidentsService`, implementar a lógica para gerar um número de incidente sequencial e único, formatado como `INC-YYYYMMDD-NNNN`.

**Descrição da Lógica:**

1. **Encontrar o Último Incidente do Dia:**

-   Antes de criar o novo incidente, faça uma consulta à base de dados para encontrar o último incidente registado no dia corrente.
-   Isto pode ser feito com uma query que filtra os registos por `createdAt` (maior ou igual ao início do dia e menor que o fim do dia) e ordena por data de criação descendente.

2. **Calcular o Novo Número Sequencial:**

-   Se não houver incidentes registados hoje, o novo número sequencial é `1`.
-   Se existirem, extraia o número sequencial do `incidentNumber` do último incidente (ex: `INC-20251114-0005` extrai `5`), e incremente esse valor.

3. **Formatar o `incidentNumber`:**

-   Construa o número final juntando o prefixo "INC-", a data no formato `YYYYMMDD`, e o novo número sequencial formatado com 4 dígitos (ex: `0001`, `0012`).

4. **Criar o Incidente:**

-   Execute a operação de criação na base de dados, passando todos os dados do DTO e o `incidentNumber` recém-gerado.

**Documentação:**
[Guia Oficial do Prisma sobre Consultas Avançadas](https://www.prisma.io/docs/orm/prisma-client/queries/filtering-and-sorting)

#### 2.3. Implementar Listagem e Paginação (US2.3)

**Objetivo:**
A função `findAll()` deve aceitar **query parameters** para filtros e paginação.

**Descrição:**
Construa dinamicamente o objeto `where` do Prisma e aplique a paginação baseada em **cursor** (mais eficiente para grandes datasets).

**Documentação:**
[Guia Oficial do Prisma sobre Filtragem e Paginação por Cursor](https://www.prisma.io/docs/orm/prisma-client/queries/pagination#cursor-based-pagination)

#### 2.4. Implementar Filtros Básicos (US2.3)

**Objetivo:**
Implemente **quick filters** (All, My Incidents, Unassigned, Open, Closed) e **single-select filters** (Status, Priority, Assignee).

**Descrição:**
No `findAll()`, aceite query params: `status`, `priority`, `assigneeId`, `search`. Construa o objeto `where` do Prisma dinamicamente.

**NOTA:** Saved filters (persistir filtros personalizados) movido para Post-MVP P3.

#### 2.5. Configurar o IncidentsController

**Ficheiro:** `nest-backend/src/incidents/incidents.controller.ts`

**Ação:**
Defina as rotas `POST`, `GET`, `PATCH` e `DELETE`.

**Segurança:**
Proteja _todos_ os endpoints com o `JwtAuthGuard` (do Sprint 1).

#### 2.5. Escrever Testes (TDD)

**Ficheiro:** `nest-backend/src/incidents/incidents.service.spec.ts`

**Testes Essenciais:**

```typescript
describe("IncidentsService - CRUD", () => {
    it("deve criar incidente com número único", async () => {
        const dto = {
            title: "Test Incident",
            description: { type: "doc", content: [] },
            priority: "P3",
            categoryId: "cat-123",
        };
        const result = await service.create(dto, "user-123");
        expect(result.incidentNumber).toMatch(/^INC-\d{8}-\d{4}$/);
    });

    it("deve aplicar filtros básicos corretamente", async () => {
        const filters = { status: ["NEW", "IN_PROGRESS"], priority: ["P1"] };
        await service.findAll(filters);
        expect(prisma.incident.findMany).toHaveBeenCalledWith(
            expect.objectContaining({
                where: expect.objectContaining({
                    status: { in: ["NEW", "IN_PROGRESS"] },
                    priority: { in: ["P1"] },
                }),
            })
        );
    });
});
```

**Executar:**

```bash
npm run test -- incidents.service.spec.ts
```

**Documentação:**
[Nest.js Testing Guide](https://docs.nestjs.com/fundamentals/testing)

---

### Fase 3: Frontend (Next.js)

#### 3.1. Instalar Dependências do Editor

**Comando:**

```bash
npm install @tiptap/react @tiptap/starter-kit @tiptap/extension-link
```

**Objetivo:**
Instale o Tiptap e as extensões **essenciais** para o MVP.

**NOTA:** Extensões de imagem (`@tiptap/extension-image`) serão adicionadas no Post-MVP P2.

**Documentação:**
[Guia Oficial do Tiptap sobre Instalação (React)](https://tiptap.dev/docs/editor/installation/react)

#### 3.2. Criar o Componente RichTextEditor

**Ficheiro:** `components/ui/rich-text-editor.tsx`

**Objetivo:**
Crie um componente de cliente (`"use client";`) para o editor com formatação **essencial**.

**Extensões a Incluir:**

-   Bold, Italic, Strike (StarterKit)
-   BulletList, OrderedList (StarterKit)
-   Link (extensão separada)
-   CodeBlock, Heading (StarterKit)
-   Placeholder

**Integração com Formulário:**
Use o componente **`Controller`** do `React Hook Form` para ligar o estado complexo do Tiptap ao estado simples do formulário.

**Documentação:**
[Guia Oficial do React Hook Form sobre o componente `Controller`](https://react-hook-form.com/get-started#IntegratingwithUIlibraries)

#### 3.3. Criar a Página de Listagem (US2.3)

**Ficheiro:** `next-frontend/app/incidents/page.tsx`

**Busca de Dados:**
Use a biblioteca **`TanStack Query`** (`useQuery`) para gerir o estado de carregamento, cache e erro da listagem.

**Tabela e Filtros:**
Use a **`DataTable`** (shadcn/ui) e crie uma UI de filtros **básicos**:

-   **Quick filters** (sidebar): All, My Incidents, Unassigned, Open, Closed
-   **Single-select filters**: Status dropdown, Priority dropdown, Assignee dropdown
-   **Simple search**: Input para buscar por número ou título

O estado dos filtros deve ser gerido no frontend e incluído na `queryKey` do `TanStack Query` para que a tabela atualize automaticamente quando os filtros mudarem.

**Documentação:**
[Guia Oficial do TanStack Query (Query Keys)](https://tanstack.com/query/latest/docs/react/guides/query-keys)

#### 3.4. Testar o Fluxo Completo

**Testes Manuais:**

1. **Criar Incidente:**

-   Navegue para `http://localhost:3000/incidents/create`
-   Preencha título, selecione categoria e prioridade
-   Use Rich Text Editor:
-   Adicione texto formatado (bold, italic, listas)
-   Adicione heading (H2, H3)
-   Adicione link (selecione texto, clique link, cole URL)
-   Adicione code block
-   Submeta → verifique PostgreSQL: incident criado
-   **NOTA:** Image paste será testado em Post-MVP P2

2. **Testar Pesquisa Simples:**

-   Navegue para `/incidents`
-   Digite número de incidente na search bar → deve filtrar
-   Digite parte do título → deve buscar (case-insensitive)
-   Verifique: PostgreSQL ILIKE funcionando
-   **NOTA:** Meilisearch (typo tolerance, highlights) será testado em Sprint 4

3. **Testar Filtros Básicos:**

-   Navegue para `/incidents`
-   **Quick filters** (sidebar):
-   Clique "My Incidents" → deve mostrar apenas seus incidents
-   Clique "Unassigned" → deve mostrar incidents sem assignee
-   Clique "Open" → deve mostrar NEW + IN_PROGRESS
-   **Single-select filters**:
-   Selecione status (dropdown) → tabela atualiza
-   Selecione prioridade (dropdown) → tabela atualiza
-   Selecione assignee (dropdown) → tabela atualiza
-   URL deve refletir filtros: `?status=NEW&priority=P1&assigneeId=user-123`
-   **NOTA:** Saved filters serão testados em Post-MVP P3

4. **Testar Atualização:**

-   Abra um incident existente
-   Edite título, descrição (rich text), status, priority
-   Verifique: activity log registra mudanças
-   Verifique: email enviado (se assignee mudou ou status mudou)

**Teste E2E (Opcional):**

```typescript
// next-frontend/e2e/incidents/create.spec.ts
test("criar incidente com rich text", async ({ page }) => {
    await page.goto("/incidents/create");

    await page.fill('[name="title"]', "Test Incident");

    // Rich text
    const editor = page.locator(".tiptap");
    await editor.click();
    await editor.type("This is a **bold** test");

    await page.selectOption('[name="priority"]', "P2");
    await page.selectOption('[name="categoryId"]', { label: "Hardware" });

    await page.click('button[type="submit"]');

    await expect(page.getByText(/incident created/i)).toBeVisible();
    await expect(page).toHaveURL(/\/incidents\/INC-\d{8}-\d{4}/);
});
```

**Documentação:**
[Playwright Testing Guide](https://playwright.dev/)

---

## Funcionalidade 2.2: Pesquisa Simples (PostgreSQL)

**NOTA:** A integração completa do Meilisearch foi movida para o Sprint 4.

### Fase 1: Backend - Pesquisa Simples

#### 1.1. Atualizar o FilterDto

**Ficheiro:** `nest-backend/src/incidents/dto/filter.dto.ts`

**Objetivo:**
Adicione o campo `search` ao DTO de filtros.

**Descrição:**

-   Adicione a propriedade `search?: string` (opcional)
-   Use o decorador `@IsOptional()` e `@IsString()`

**Documentação:**
[Class Validator - Validação de DTOs](https://github.com/typestack/class-validator)

#### 1.2. Implementar Pesquisa no IncidentsService

**Ficheiro:** `nest-backend/src/incidents/incidents.service.ts`

**Objetivo:**
No método `findAll()`, adicione suporte para o parâmetro `search` que busca por Incident Number e Title.

**Descrição:**

-   Se `filters.search` existir, adicione ao objeto `where` do Prisma:
-   `OR` com dois critérios:
-   `incidentNumber` contains search term
-   `title` contains search term (mode: 'insensitive')
-   Mantenha os filtros existentes (status, priority, assigneeId)
-   Use `orderBy: { createdAt: 'desc' }` para resultados mais recentes primeiro

**Documentação:**
[Prisma - Filtering and Sorting](https://www.prisma.io/docs/orm/prisma-client/queries/filtering-and-sorting)

#### 1.3. Atualizar o Endpoint GET /incidents

**Ficheiro:** `nest-backend/src/incidents/incidents.controller.ts`

**Objetivo:**
Certifique-se que o endpoint aceita o query parameter `search`.

**Descrição:**

-   O decorador `@Query()` já deve mapear automaticamente `?search=termo`
-   Valide que o `FilterDto` está a ser usado corretamente

**Documentação:**
[NestJS - Controllers](https://docs.nestjs.com/controllers)

---

### Fase 2: Frontend - Barra de Pesquisa

#### 2.1. Criar o Componente de Pesquisa

**Ficheiro:** `next-frontend/components/search-bar.tsx`

**Objetivo:**
Criar uma barra de pesquisa simples na lista de incidentes.

**Descrição:**

-   Use o componente `Input` do shadcn/ui
-   Implemente debounce de 300ms para evitar chamadas excessivas à API
-   Ao digitar, faça fetch para `GET /api/incidents?search=termo`
-   Atualize a lista de incidentes com os resultados

**Documentação:**
[shadcn/ui - Input Component](https://ui.shadcn.com/docs/components/input)

#### 2.2. Integrar na Página de Incidentes

**Ficheiro:** `next-frontend/app/incidents/page.tsx`

**Objetivo:**
Adicione a barra de pesquisa acima da tabela de incidentes.

**Descrição:**

-   Posicione o componente `SearchBar` no topo da página
-   Gerencie o estado de pesquisa (search term, loading, resultados)
-   Mostre loading state durante a pesquisa
-   Combine pesquisa com filtros existentes

**Documentação:**
[Next.js - Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)

---

## Funcionalidade 2.3: Filtros Básicos de Incidentes

npm run test:watch

# Coverage

npm run test:cov

# E2E

npm run test:e2e

````

**Frontend:**

```bash
# Component tests
npm test

# E2E com Playwright
npm run test:e2e

# E2E com UI
npm run test:e2e -- --ui
````

### Coverage Mínimo Recomendado

-   **Backend Services:** > 80%
-   **Backend Controllers:** > 70%
-   **Frontend Components:** > 70%
-   **E2E Critical Flows:** 100% (Criar Incidente, Pesquisa)

### Estrutura de Testes

```
nest-backend/
 src/
 incidents/
 incidents.service.spec.ts # Unit tests
 incidents.controller.spec.ts # Unit tests
 meilisearch.service.spec.ts # Unit tests
 test/
 incidents.e2e-spec.ts # Integration tests

next-frontend/
 __tests__/
 components/
 rich-text-editor.test.tsx
 incident-form.test.tsx
 incident-filters.test.tsx
 e2e/
 incidents/
 create-incident.spec.ts
 search-incidents.spec.ts
```

### Template: Unit Test (Backend - IncidentsService)

```typescript
describe("IncidentsService", () => {
    let service: IncidentsService;
    let prisma: PrismaService;
    let meilisearch: MeilisearchService;

    beforeEach(async () => {
        const module = await Test.createTestingModule({
            providers: [
                IncidentsService,
                { provide: PrismaService, useValue: mockPrisma },
                { provide: MeilisearchService, useValue: mockMeilisearch },
            ],
        }).compile();

        service = module.get<IncidentsService>(IncidentsService);
        prisma = module.get<PrismaService>(PrismaService);
        meilisearch = module.get<MeilisearchService>(MeilisearchService);
    });

    it("deve criar incidente com número único", async () => {
        // Arrange
        const dto = {
            title: "Test Incident",
            description: { type: "doc", content: [] },
            priority: "P3",
            categoryId: "cat-123",
        };

        // Act
        const result = await service.create(dto, "user-123");

        // Assert
        expect(result.incidentNumber).toMatch(/^INC-\d{8}-\d{4}$/);
        expect(meilisearch.syncIncident).toHaveBeenCalledWith(result);
    });

    it("deve filtrar incidentes por status", async () => {
        // Arrange
        const filters = { status: "NEW" };

        // Act
        const result = await service.findAll(filters);

        // Assert
        expect(prisma.incident.findMany).toHaveBeenCalledWith(
            expect.objectContaining({ where: { status: "NEW" } })
        );
    });
});
```

### Template: E2E Test (Backend)

```typescript
describe("Incidents API (e2e)", () => {
    let app: INestApplication;
    let accessToken: string;

    beforeAll(async () => {
        const moduleFixture = await Test.createTestingModule({
            imports: [AppModule],
        }).compile();

        app = moduleFixture.createNestApplication();
        await app.init();

        // Login to get token
        const loginResponse = await request(app.getHttpServer())
            .post("/auth/login")
            .send({ email: "test@example.com", password: "Test123!@" });

        accessToken = loginResponse.body.accessToken;
    });

    it("POST /incidents - deve criar incidente", () => {
        return request(app.getHttpServer())
            .post("/incidents")
            .set("Authorization", `Bearer ${accessToken}`)
            .send({
                title: "Test Incident",
                description: { type: "doc", content: [] },
                priority: "P3",
                categoryId: "cat-123",
            })
            .expect(201)
            .expect((res) => {
                expect(res.body.incidentNumber).toBeDefined();
            });
    });

    it("GET /incidents/search - deve pesquisar com typo tolerance", () => {
        return request(app.getHttpServer())
            .get("/incidents/search?q=tset") // typo: "test"
            .set("Authorization", `Bearer ${accessToken}`)
            .expect(200)
            .expect((res) => {
                expect(res.body.hits).toBeDefined();
            });
    });

    afterAll(async () => {
        await app.close();
    });
});
```

### Template: Component Test (Frontend - RichTextEditor)

```typescript
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { RichTextEditor } from "./rich-text-editor";

describe("RichTextEditor", () => {
    it("deve renderizar toolbar com botões de formatação", () => {
        render(<RichTextEditor value="" onChange={() => {}} />);

        expect(
            screen.getByRole("button", { name: /bold/i })
        ).toBeInTheDocument();
        expect(
            screen.getByRole("button", { name: /italic/i })
        ).toBeInTheDocument();
        expect(
            screen.getByRole("button", { name: /heading/i })
        ).toBeInTheDocument();
    });

    it("deve aplicar formatação bold ao texto selecionado", async () => {
        const onChange = jest.fn();
        render(<RichTextEditor value="" onChange={onChange} />);

        const editor = screen.getByRole("textbox");
        fireEvent.input(editor, { target: { textContent: "test text" } });

        // Simular seleção e click no bold
        const boldButton = screen.getByRole("button", { name: /bold/i });
        fireEvent.click(boldButton);

        await waitFor(() => {
            expect(onChange).toHaveBeenCalled();
        });
    });

    it("deve fazer upload de imagem por drag & drop", async () => {
        const mockUpload = jest
            .fn()
            .mockResolvedValue({ url: "https://s3.amazonaws.com/image.jpg" });
        render(
            <RichTextEditor
                value=""
                onChange={() => {}}
                onImageUpload={mockUpload}
            />
        );

        const editor = screen.getByRole("textbox");
        const file = new File(["image"], "test.jpg", { type: "image/jpeg" });

        fireEvent.drop(editor, {
            dataTransfer: { files: [file] },
        });

        await waitFor(() => {
            expect(mockUpload).toHaveBeenCalledWith(file);
        });
    });
});
```

### Template: E2E Test (Frontend - Playwright)

```typescript
import { test, expect } from "@playwright/test";

test.describe("Criar Incidente", () => {
    test.beforeEach(async ({ page }) => {
        // Login
        await page.goto("/login");
        await page.fill('[name="email"]', "test@example.com");
        await page.fill('[name="password"]', "Test123!@");
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL("/dashboard");
    });

    test("deve criar incidente com rich text", async ({ page }) => {
        await page.goto("/incidents/create");

        // Preencher formulário
        await page.fill('[name="title"]', "Test Incident");

        // Rich text editor
        const editor = page.locator(".tiptap");
        await editor.click();
        await editor.type("This is a **bold** description");

        // Selecionar prioridade
        await page.selectOption('[name="priority"]', "P2");

        // Selecionar categoria
        await page.selectOption('[name="categoryId"]', { label: "Hardware" });

        // Submeter
        await page.click('button[type="submit"]');

        // Verificar sucesso
        await expect(page.getByText(/incident created/i)).toBeVisible();
        await expect(page).toHaveURL(/\/incidents\/INC-\d{8}-\d{4}/);
    });

    test("deve pesquisar incidentes com typo tolerance", async ({ page }) => {
        await page.goto("/incidents");

        // Pesquisar com typo
        const searchBox = page.locator('[placeholder*="Search"]');
        await searchBox.fill("hardwre"); // typo: "hardware"

        // Esperar resultados
        await page.waitForTimeout(300); // debounce

        // Verificar highlights
        await expect(page.locator(".search-result").first()).toBeVisible();
        await expect(page.locator("mark")).toHaveCount({ gte: 1 }); // highlights
    });

    test("deve aplicar filtros avançados", async ({ page }) => {
        await page.goto("/incidents");

        // Abrir filtros
        await page.click('button:has-text("Filters")');

        // Aplicar filtro de status
        await page.check('[value="NEW"]');
        await page.check('[value="IN_PROGRESS"]');

        // Aplicar filtro de prioridade
        await page.check('[value="P1"]');

        // Fechar modal
        await page.click('button:has-text("Apply")');

        // Verificar URL atualizada
        await expect(page).toHaveURL(/status=NEW,IN_PROGRESS/);
        await expect(page).toHaveURL(/priority=P1/);

        // Verificar resultados filtrados
        const statusBadges = page.locator(".status-badge");
        await expect(statusBadges.first()).toHaveText(/NEW|IN_PROGRESS/);
    });
});
```

---

## Configuração de Ambiente

### Variáveis de Ambiente

#### Backend (.env)

**Ficheiro:** `nest-backend/.env`

```env
# Database (do Sprint 1)
DATABASE_URL="postgresql://orionone:secret@localhost:5432/orionone?schema=public"

# JWT (do Sprint 1)
JWT_SECRET="your-super-secret-key-change-in-production"
JWT_EXPIRES_IN="15m"
REFRESH_TOKEN_EXPIRES_IN="7d"

# Meilisearch (NOVO)
MEILISEARCH_HOST="http://localhost:7700"
MEILISEARCH_KEY="masterKey"

# AWS S3 (para upload de imagens)
AWS_REGION="eu-west-1"
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"
AWS_S3_BUCKET="orionone-uploads"
AWS_S3_PRESIGNED_URL_EXPIRES=3600 # 1 hora

# App
NODE_ENV="development"
PORT=8000
FRONTEND_URL="http://localhost:3000"
```

**Importante:**

-   **Meilisearch:** `MEILISEARCH_HOST` deve apontar para o container Docker (localhost:7700 em dev)
-   **AWS S3:** Configurar credenciais IAM com permissões S3 (PutObject, GetObject)
-   **Presigned URLs:** Expiram em 1 hora por segurança

---

#### Frontend (.env.local)

**Ficheiro:** `next-frontend/.env.local`

```env
# API (do Sprint 1)
NEXT_PUBLIC_API_URL="http://localhost:8000"

# Meilisearch (NOVO - acesso direto do browser)
NEXT_PUBLIC_MEILISEARCH_HOST="http://localhost:7700"
NEXT_PUBLIC_MEILISEARCH_KEY="masterKey"

# App
NEXT_PUBLIC_APP_NAME="OrionOne ITSM"
NEXT_PUBLIC_APP_URL="http://localhost:3000"

# Upload Settings
NEXT_PUBLIC_MAX_FILE_SIZE=5242880 # 5MB
NEXT_PUBLIC_ALLOWED_IMAGE_TYPES="image/jpeg,image/png,image/webp"
```

**Importante:**

-   **Meilisearch no Frontend:** Permite pesquisa instantânea direta do browser
-   **Security:** Em produção, use API key com permissões limitadas (search-only)

---

### Configuração Meilisearch

#### Inicializar Índice

**Ficheiro:** `nest-backend/src/meilisearch/meilisearch.service.ts`

```typescript
import { Injectable, OnModuleInit } from "@nestjs/common";
import { MeiliSearch } from "meilisearch";

@Injectable()
export class MeilisearchService implements OnModuleInit {
    private client: MeiliSearch;
    private readonly indexName = "incidents";

    constructor() {
        this.client = new MeiliSearch({
            host: process.env.MEILISEARCH_HOST,
            apiKey: process.env.MEILISEARCH_KEY,
        });
    }

    async onModuleInit() {
        // Criar índice se não existir
        try {
            await this.client.getIndex(this.indexName);
        } catch {
            await this.client.createIndex(this.indexName, { primaryKey: "id" });
        }

        // Configurar índice
        const index = this.client.index(this.indexName);

        await index.updateSettings({
            searchableAttributes: [
                "incidentNumber",
                "title",
                "description", // texto simples convertido do JSON
            ],
            filterableAttributes: [
                "status",
                "priority",
                "categoryId",
                "assigneeId",
                "createdAt",
            ],
            sortableAttributes: ["createdAt", "updatedAt", "priority"],
            rankingRules: [
                "words",
                "typo",
                "proximity",
                "attribute",
                "sort",
                "exactness",
            ],
            typoTolerance: {
                enabled: true,
                minWordSizeForTypos: {
                    oneTypo: 5,
                    twoTypos: 9,
                },
            },
        });
    }

    async syncIncident(incident: any) {
        // Converter Tiptap JSON para texto simples
        const description = this.tiptapToPlainText(incident.description);

        const document = {
            id: incident.id,
            incidentNumber: incident.incidentNumber,
            title: incident.title,
            description,
            status: incident.status,
            priority: incident.priority,
            categoryId: incident.categoryId,
            assigneeId: incident.assigneeId,
            createdAt: incident.createdAt.toISOString(),
            updatedAt: incident.updatedAt.toISOString(),
        };

        const index = this.client.index(this.indexName);
        await index.addDocuments([document]);
    }

    async search(query: string, filters?: any) {
        const index = this.client.index(this.indexName);

        const searchParams: any = {
            attributesToHighlight: ["title", "description"],
            highlightPreTag: "<mark>",
            highlightPostTag: "</mark>",
            limit: 20,
        };

        if (filters) {
            searchParams.filter = this.buildFilters(filters);
        }

        return index.search(query, searchParams);
    }

    private tiptapToPlainText(json: any): string {
        if (!json || !json.content) return "";

        return json.content
            .map((node: any) => {
                if (node.type === "paragraph" && node.content) {
                    return node.content.map((c: any) => c.text || "").join("");
                }
                return "";
            })
            .join(" ");
    }

    private buildFilters(filters: any): string {
        const conditions = [];

        if (filters.status) {
            conditions.push(
                `status IN [${filters.status
                    .map((s: string) => `"${s}"`)
                    .join(",")}]`
            );
        }

        if (filters.priority) {
            conditions.push(
                `priority IN [${filters.priority
                    .map((p: string) => `"${p}"`)
                    .join(",")}]`
            );
        }

        return conditions.join(" AND ");
    }
}
```

---

### Configuração AWS S3

#### Instalar SDK

```bash
cd nest-backend
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

#### Criar Service

**Ficheiro:** `nest-backend/src/upload/upload.service.ts`

```typescript
import { Injectable } from "@nestjs/common";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

@Injectable()
export class UploadService {
    private s3Client: S3Client;
    private bucketName: string;

    constructor() {
        this.s3Client = new S3Client({
            region: process.env.AWS_REGION,
            credentials: {
                accessKeyId: process.env.AWS_ACCESS_KEY_ID,
                secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
            },
        });
        this.bucketName = process.env.AWS_S3_BUCKET;
    }

    async getPresignedUploadUrl(
        filename: string,
        contentType: string
    ): Promise<{ uploadUrl: string; fileUrl: string }> {
        const key = `incidents/${Date.now()}-${filename}`;

        const command = new PutObjectCommand({
            Bucket: this.bucketName,
            Key: key,
            ContentType: contentType,
        });

        const uploadUrl = await getSignedUrl(this.s3Client, command, {
            expiresIn: parseInt(process.env.AWS_S3_PRESIGNED_URL_EXPIRES),
        });

        const fileUrl = `https://${this.bucketName}.s3.${process.env.AWS_REGION}.amazonaws.com/${key}`;

        return { uploadUrl, fileUrl };
    }
}
```

#### Criar Endpoint

**Ficheiro:** `nest-backend/src/incidents/incidents.controller.ts`

```typescript
@Post('upload-url')
@UseGuards(JwtAuthGuard)
async getUploadUrl(
 @Body() body: { filename: string; contentType: string },
) {
 return this.uploadService.getPresignedUploadUrl(
 body.filename,
 body.contentType,
 );
}
```

---

## Tratamento de Erros

### Exception Filters (Nest.js)

**Meilisearch Unavailable:**

```typescript
// nest-backend/src/incidents/incidents.service.ts

async findAll(filters: any) {
 try {
 // Tentar pesquisa no Meilisearch primeiro
 if (filters.q) {
 const results = await this.meilisearchService.search(filters.q, filters);
 return results;
 }
 } catch (error) {
 // Fallback para PostgreSQL se Meilisearch falhar
 console.warn('Meilisearch unavailable, falling back to PostgreSQL', error);
 }

 // Pesquisa tradicional no PostgreSQL
 return this.prisma.incident.findMany({
 where: this.buildWhereClause(filters),
 include: {
 requester: { select: { id: true, name: true, email: true } },
 assignee: { select: { id: true, name: true, email: true } },
 category: true,
 },
 });
}
```

**S3 Upload Errors:**

```typescript
// nest-backend/src/upload/upload.service.ts

async getPresignedUploadUrl(filename: string, contentType: string) {
 try {
 const key = `incidents/${Date.now()}-${filename}`;

 const command = new PutObjectCommand({
 Bucket: this.bucketName,
 Key: key,
 ContentType: contentType,
 });

 const uploadUrl = await getSignedUrl(this.s3Client, command, {
 expiresIn: parseInt(process.env.AWS_S3_PRESIGNED_URL_EXPIRES),
 });

 const fileUrl = `https://${this.bucketName}.s3.${process.env.AWS_REGION}.amazonaws.com/${key}`;

 return { uploadUrl, fileUrl };
 } catch (error) {
 throw new InternalServerErrorException(
 'Failed to generate upload URL. Check AWS credentials.',
 );
 }
}
```

---

### Error Handling (Frontend)

**Ficheiro:** `next-frontend/lib/api/error-handler.ts`

```typescript
export function handleApiError(error: any): string {
    if (error.response) {
        const message = error.response.data?.message;

        if (Array.isArray(message)) {
            return message.join(", ");
        }

        // Erros específicos do Sprint 2
        switch (error.response.status) {
            case 413:
                return "Ficheiro demasiado grande. Máximo: 5MB";
            case 415:
                return "Tipo de ficheiro não suportado. Use: JPG, PNG, WEBP";
            case 503:
                return "Pesquisa temporariamente indisponível. Tente novamente.";
            default:
                return message || "Erro no servidor";
        }
    } else if (error.request) {
        return "Servidor não responde. Verifique a ligação.";
    } else {
        return error.message || "Erro desconhecido";
    }
}
```

**Upload Error Handling:**

```typescript
// next-frontend/components/rich-text-editor.tsx

const handleImageUpload = async (file: File) => {
    try {
        // Validar tamanho
        if (file.size > parseInt(process.env.NEXT_PUBLIC_MAX_FILE_SIZE)) {
            toast({
                title: "Erro",
                description: "Imagem demasiado grande (máx: 5MB)",
                variant: "destructive",
            });
            return null;
        }

        // Validar tipo
        const allowedTypes =
            process.env.NEXT_PUBLIC_ALLOWED_IMAGE_TYPES.split(",");
        if (!allowedTypes.includes(file.type)) {
            toast({
                title: "Erro",
                description: "Tipo de ficheiro não suportado",
                variant: "destructive",
            });
            return null;
        }

        // 1. Obter presigned URL
        const { uploadUrl, fileUrl } = await api.post("/incidents/upload-url", {
            filename: file.name,
            contentType: file.type,
        });

        // 2. Upload direto para S3
        await fetch(uploadUrl, {
            method: "PUT",
            body: file,
            headers: {
                "Content-Type": file.type,
            },
        });

        return fileUrl;
    } catch (error) {
        const errorMessage = handleApiError(error);
        toast({
            title: "Erro no upload",
            description: errorMessage,
            variant: "destructive",
        });
        return null;
    }
};
```

---

## Troubleshooting Comum

### Problema 1: Meilisearch não indexa

**Sintomas:**

-   Pesquisa não retorna resultados
-   Console: "MeiliSearchApiError: Index not found"

**Diagnóstico:**

```bash
# Verificar se Meilisearch está a correr
docker ps | grep meilisearch

# Testar conexão
curl http://localhost:7700/health

# Ver índices
curl http://localhost:7700/indexes \
 -H "Authorization: Bearer masterKey"
```

**Soluções:**

1. **Container não está a correr:**

```bash
docker-compose up -d orionone-meilisearch
```

2. **Índice não foi criado:**

```bash
# Reiniciar backend para executar onModuleInit
cd nest-backend
npm run start:dev
```

3. **Master key errada:**

```env
# nest-backend/.env
MEILISEARCH_KEY=masterKey
```

---

### Problema 2: Upload de imagens falha

**Sintomas:**

-   Erro 403 Forbidden ao fazer upload
-   Imagens não aparecem no editor

**Diagnóstico:**

```bash
# Verificar credenciais AWS
aws s3 ls s3://orionone-uploads/

# Testar presigned URL manualmente
curl -X PUT "PRESIGNED_URL" \
 --upload-file test.jpg \
 -H "Content-Type: image/jpeg"
```

**Soluções:**

1. **Credenciais AWS inválidas:**

```env
# nest-backend/.env
AWS_ACCESS_KEY_ID="your-valid-key"
AWS_SECRET_ACCESS_KEY="your-valid-secret"
```

2. **Bucket não existe:**

```bash
aws s3 mb s3://orionone-uploads --region eu-west-1
```

3. **CORS do S3 não configurado:**

```json
{
    "CORSRules": [
        {
            "AllowedOrigins": ["http://localhost:3000"],
            "AllowedMethods": ["PUT", "GET"],
            "AllowedHeaders": ["*"],
            "MaxAgeSeconds": 3000
        }
    ]
}
```

---

### Problema 3: Rich Text não guarda formatação

**Sintomas:**

-   Editor funciona mas ao guardar perde formatação
-   JSON retornado está vazio

**Diagnóstico:**

```typescript
// Verificar o que está a ser enviado
console.log(JSON.stringify(editor.getJSON(), null, 2));
```

**Soluções:**

1. **Controller não aceita Json:**

```typescript
// CreateIncidentDto
@IsObject()
description: any; // Aceita qualquer JSON
```

2. **Prisma não reconhece Json:**

```prisma
// schema.prisma
description Json // Não String!
```

3. **Frontend não usa Controller do React Hook Form:**

```tsx
<Controller
    name="description"
    control={control}
    render={({ field }) => (
        <RichTextEditor value={field.value} onChange={field.onChange} />
    )}
/>
```

---

### Problema 4: Filtros não funcionam

**Sintomas:**

-   Selecionar filtros não atualiza tabela
-   URL não muda quando aplica filtros

**Diagnóstico:**

```tsx
// Verificar queryKey do TanStack Query
console.log(queryKey); // ['incidents', { status: 'NEW', priority: 'P1' }]
```

**Soluções:**

1. **QueryKey não inclui filtros:**

```tsx
const { data } = useQuery({
    queryKey: ["incidents", filters], // ← Importante!
    queryFn: () => fetchIncidents(filters),
});
```

2. **Estado dos filtros não atualiza:**

```tsx
const [filters, setFilters] = useState({});

// Atualizar filtros
const handleFilterChange = (newFilters) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
};
```

3. **Backend não processa filtros:**

```typescript
// incidents.controller.ts
@Get()
async findAll(@Query() query: FilterIncidentsDto) {
return this.incidentsService.findAll(query);
}
```

---

### Problema 5: Pesquisa muito lenta (>200ms)

**Sintomas:**

-   Delay visível ao digitar na search box
-   Meilisearch retorna resultados mas demora

**Diagnóstico:**

```bash
# Ver stats do índice
curl http://localhost:7700/indexes/incidents/stats \
 -H "Authorization: Bearer masterKey"

# Ver tamanho do índice
# numberOfDocuments deve ser < 100k para performance óptima
```

**Soluções:**

1. **Demasiados documentos:**

```typescript
// Implementar paginação
const searchParams = {
    limit: 20, // ← Reduzir
    offset: page * 20,
};
```

2. **searchableAttributes muito extensos:**

```typescript
// Reduzir campos pesquisáveis
searchableAttributes: [
    "title", // ← Manter
    "incidentNumber", // ← Manter
    // 'description', // ← Remover se muito grande
];
```

3. **Ranking rules desnecessários:**

```typescript
rankingRules: [
    "words",
    "typo",
    "proximity", // ← Remover se não necessário
];
```
---
