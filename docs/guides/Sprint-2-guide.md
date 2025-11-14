# Guia de Implementação Detalhado do Sprint 2: Incidentes, Rich Text & Meilisearch

## Visão Geral do Sprint

**Objetivo:**
Implementar sistema completo de gestão de incidentes com Rich Text (Tiptap), pesquisa inteligente (Meilisearch) e filtros avançados.

**User Stories:**

- [Em Curso] US2.1: Criar Incidente com Rich Text
- [Em Curso] US2.2: Pesquisa com Meilisearch
- [Em Curso] US2.3: Listagem com Filtros Avançados
- [Em Curso] US2.4: Atualizar Incidente

**Pré-requisitos:**
Sprint 1 completo (Autenticação funcionando, Docker containers a correr)

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

- `id`, `incidentNumber` (use `@unique` e lógica customizada no backend para geração)
- `title` (com `@db.VarChar(255)`)
- **Rich Text:** `description` do tipo **`Json`** - crucial para preservar a estrutura do Tiptap
- **Enums:** Crie e use os enums `IncidentStatus` (NEW, IN_PROGRESS, RESOLVED, CLOSED) e `IncidentPriority` (P1, P2, P3, P4)
- **Relações:** Crie as relações `requester` e `assignee` com o modelo `User` (muitos-para-um) e a relação `category` com o modelo `Category` (muitos-para-um)

**Documentação:**
[Guia Oficial do Prisma sobre Modelos de Dados, Enums e Tipos JSON](https://www.prisma.io/docs/orm/prisma-schema/data-model)

#### 1.3. Definir Modelos de Suporte

**Objetivo:**
Crie o `model Category` (para categorização de incidentes) e o `model SavedFilter` (para a US2.3).

**Descrição:**
`SavedFilter` deve ter uma relação com o `User` e um campo `filters` do tipo `Json` para armazenar a configuração dos filtros aplicados pelo utilizador.

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
nest g resource incidents
```

**DTOs:**
Crie `CreateIncidentDto.ts` e `UpdateIncidentDto.ts`. Use `@IsString()`, `@IsEnum()`, e `@IsObject()` (para o campo Rich Text) com `class-validator`.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação (class-validator)](https://docs.nestjs.com/techniques/validation)

#### 2.2. Implementar o IncidentsService - Geração do Número de Incidente (US2.1)

**Ficheiro:** `nest-backend/src/incidents/incidents.service.ts`

**Objetivo:**
No `create()` do `IncidentsService`, implemente a lógica para gerar um número sequencial único (ex: `INC-YYYYMMDD-0001`).

**Descrição:**
Isto requer uma transação ou uma consulta que obtenha a última contagem do dia.

#### 2.3. Implementar Listagem e Paginação (US2.3)

**Objetivo:**
A função `findAll()` deve aceitar **query parameters** para filtros e paginação.

**Descrição:**
Construa dinamicamente o objeto `where` do Prisma e aplique a paginação baseada em **cursor** (mais eficiente para grandes datasets).

**Documentação:**
[Guia Oficial do Prisma sobre Filtragem e Paginação por Cursor](https://www.prisma.io/docs/orm/prisma-client/queries/pagination#cursor-based-pagination)

#### 2.4. Implementar Filtros Salvos (US2.3)

**Objetivo:**
Implemente o CRUD para o modelo `SavedFilter` (criar, listar por utilizador, apagar) no `IncidentsService`.

#### 2.5. Implementar o Upload de Imagens (US2.1)

**Endpoint:** `POST /api/incidents/upload-image`

**Objetivo:**
Crie um endpoint que gera **URLs pré-assinadas** para o S3.

**Descrição:**
Este endpoint _não_ carrega a imagem. Ele devolve uma URL temporária onde o frontend _irá_ carregar a imagem diretamente. Isto descarrega o backend. Utilize o SDK da AWS.

**Documentação:**
[Guia Oficial da AWS SDK sobre URLs Pré-Assinadas (S3)](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/s3-example-presigned-urls.html)

#### 2.6. Configurar o IncidentsController

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

 it("deve sincronizar com Meilisearch após criar", async () => {
 const incident = await service.create(dto, "user-123");
 expect(meilisearchService.syncIncident).toHaveBeenCalledWith(incident);
 });

 it("deve aplicar filtros corretamente", async () => {
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
npm install @tiptap/react @tiptap/starter-kit
```

**Objetivo:**
Instale o Tiptap e as extensões necessárias (Image, Link, etc.).

**Documentação:**
[Guia Oficial do Tiptap sobre Instalação (React)](https://tiptap.dev/docs/editor/installation/react)

#### 3.2. Criar o Componente RichTextEditor

**Ficheiro:** `components/ui/rich-text-editor.tsx`

**Objetivo:**
Crie um componente de cliente (`"use client";`) para o editor.

**Integração com Formulário:**
Use o componente **`Controller`** do `React Hook Form` para ligar o estado complexo do Tiptap ao estado simples do formulário.

**Documentação:**
[Guia Oficial do React Hook Form sobre o componente `Controller`](https://react-hook-form.com/get-started#IntegratingwithUIlibraries)

#### 3.3. Implementar o Upload de Imagens no Editor

**Objetivo:**
Configure a extensão de imagem do Tiptap para intercetar o evento de "paste" (colar) ou "drop" (arrastar).

**Fluxo:**

1. Obter o ficheiro colado/arrastado
2. Chamar o backend para obter a URL pré-assinada (passo 2 da Fase 2)
3. Fazer um `PUT` (upload direto) para o S3 usando a URL pré-assinada
4. Inserir a URL final da imagem no Tiptap

**Documentação:**
[Guia Oficial do Tiptap sobre Upload de Ficheiros](https://tiptap.dev/docs/editor/storage-and-collaboration/file-upload)

#### 3.4. Criar a Página de Listagem (US2.3)

**Ficheiro:** `next-frontend/app/incidents/page.tsx`

**Busca de Dados:**
Use a biblioteca **`TanStack Query`** (`useQuery`) para gerir o estado de carregamento, cache e erro da listagem.

**Tabela e Filtros:**
Use a **`DataTable`** (shadcn/ui) e crie uma UI de filtros avançada. O estado dos filtros (status, assignee, priority) deve ser gerido no frontend e incluído na `queryKey` do `TanStack Query` para que a tabela atualize automaticamente quando os filtros mudarem.

**Documentação:**
[Guia Oficial do TanStack Query (Query Keys)](https://tanstack.com/query/latest/docs/react/guides/query-keys)

#### 3.5. Testar o Fluxo Completo

**Testes Manuais:**

1. **Criar Incidente:**

 - Navegue para `http://localhost:3000/incidents/create`
 - Preencha título, selecione categoria e prioridade
 - Use Rich Text Editor:
 - Adicione texto formatado (bold, italic, listas)
 - Cole uma imagem → deve fazer upload para S3
 - Adicione link
 - Submeta → verifique PostgreSQL: incident criado
 - Verifique Meilisearch: documento indexado

2. **Testar Upload de Imagens:**

 - No editor, arraste uma imagem
 - Verifique console: presigned URL gerada
 - Verifique S3: imagem guardada
 - Imagem deve aparecer no editor com URL do S3

3. **Testar Filtros:**

 - Navegue para `/incidents`
 - Aplique filtro de status (NEW, IN_PROGRESS)
 - Aplique filtro de prioridade (P1)
 - Tabela deve atualizar automaticamente
 - URL deve refletir filtros: `?status=NEW,IN_PROGRESS&priority=P1`

4. **Guardar Filtros:**
 - Com filtros aplicados, clique "Save Filter"
 - Dê nome ao filtro
 - Verifique BD: SavedFilter criado
 - Recarregue página → filtro salvo deve aparecer no dropdown

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

## Funcionalidade 2.2: Integração da Pesquisa Meilisearch

### Fase 1: Backend (Nest.js)

#### 1.1. Instalar e Configurar o Cliente

**Comando:**

```bash
npm install meilisearch
```

**Objetivo:**
Crie um `MeilisearchModule` e `MeilisearchService` (Singleton) e injete o cliente (inicializado com as variáveis de ambiente do seu Docker).

**Documentação:**
[Guia Oficial do Meilisearch sobre SDKs (Quick Start)](https://www.meilisearch.com/docs/learn/getting_started/quick_start)

#### 1.2. Configurar o Índice

**Ficheiro:** `nest-backend/src/meilisearch/meilisearch.service.ts`

**Objetivo:**
Defina as configurações iniciais do índice `incidents`.

**Descrição:**
Defina `searchableAttributes` (ex: `title`, `incidentNumber`, `description`) e `filterableAttributes` (ex: `status`, `priority`) para otimizar a pesquisa.

**Documentação:**
[Guia Oficial do Meilisearch sobre Configuração de Índice](https://www.meilisearch.com/docs/learn/configuration/settings)

#### 1.3. Implementar a Sincronização

**Objetivo:**
Implemente a função `syncIncident(incident)` no `MeilisearchService`.

**Descrição:**
Esta função deve:

1. Receber o objeto `Incident` (que inclui a `description` como JSON)
2. **Conversão de Dados:** Converter o Tiptap JSON para **texto simples** antes de o enviar para o Meilisearch
3. Chamar `meilisearchClient.index('incidents').addDocuments([documento])`
4. No `IncidentsService`, chame `this.meilisearchService.syncIncident(novoIncidente)` nas funções `create` e `update`. Para ser um "background job", faça a chamada de forma assíncrona ("fire-and-forget") para não bloquear o utilizador

**Documentação:**
[Guia Oficial do Meilisearch sobre Adicionar Documentos](https://www.meilisearch.com/docs/learn/indexation/documents)

#### 1.4. Criar o Endpoint de Pesquisa

**Endpoint:** `GET /api/incidents/search`

**Objetivo:**
Recebe a query do utilizador (`?q=termo`). Chama o `MeilisearchService.search(query)` para aproveitar a **typo-tolerance** e a **pesquisa instantânea**.

**Descrição:**
Ative a opção de **highlights** para realçar os termos encontrados nos resultados.

**Documentação:**
[Guia Oficial do Meilisearch sobre Pesquisa (Typo-Tolerance e Highlights)](https://www.meilisearch.com/docs/learn/search/search_parameters)

#### 1.5. Testar Meilisearch (TDD)

**Ficheiro:** `nest-backend/src/meilisearch/meilisearch.service.spec.ts`

**Testes Essenciais:**

```typescript
describe("MeilisearchService", () => {
 it("deve sincronizar incidente com Meilisearch", async () => {
 const incident = {
 id: "inc-123",
 incidentNumber: "INC-20241114-0001",
 title: "Test Incident",
 description: {
 type: "doc",
 content: [
 {
 type: "paragraph",
 content: [{ type: "text", text: "Test description" }],
 },
 ],
 },
 };

 await service.syncIncident(incident);

 expect(meilisearchClient.index).toHaveBeenCalledWith("incidents");
 expect(addDocuments).toHaveBeenCalledWith([
 expect.objectContaining({
 id: "inc-123",
 description: "Test description", // Convertido para texto
 }),
 ]);
 });

 it("deve pesquisar com typo tolerance", async () => {
 // Mock de resultados
 mockSearch.mockResolvedValue({
 hits: [
 {
 id: "inc-123",
 title: "Hardware Issue",
 _formatted: {
 title: "<mark>Hardware</mark> Issue",
 },
 },
 ],
 });

 const result = await service.search("hardwre"); // typo

 expect(mockSearch).toHaveBeenCalledWith(
 "hardwre",
 expect.objectContaining({
 attributesToHighlight: ["title", "description"],
 })
 );
 expect(result.hits).toHaveLength(1);
 });

 it("deve converter Tiptap JSON para texto simples", () => {
 const json = {
 type: "doc",
 content: [
 {
 type: "paragraph",
 content: [
 { type: "text", text: "Hello " },
 {
 type: "text",
 marks: [{ type: "bold" }],
 text: "world",
 },
 ],
 },
 ],
 };

 const text = service.tiptapToPlainText(json);
 expect(text).toBe("Hello world");
 });
});
```

**Executar:**

```bash
npm run test -- meilisearch.service.spec.ts
```

---

### Fase 2: Frontend (Next.js)

#### 2.1. Instalar Clientes de Pesquisa

**Comando:**

```bash
npm install @meilisearch/instant-meilisearch react-instantsearch-hooks-web
```

**Objetivo:**
Instalar bibliotecas recomendadas para melhor UX de pesquisa.

#### 2.2. Criar o Componente de Pesquisa Global

**Ficheiro:** `components/global-search.tsx`

**Objetivo:**
Crie um componente de barra de pesquisa centralizado.

**UX:**
Use o componente `Command` do `shadcn/ui` para criar uma experiência de pesquisa rápida (tipo barra de comando).

#### 2.3. Implementar a Lógica de Pesquisa Instantânea

**Objetivo:**
Ligue a sua UI de pesquisa ao Meilisearch.

**Descrição:**
Use os hooks do `react-instantsearch-hooks-web` (ex: `useSearchBox`, `useHits`) para gerir o estado de pesquisa. Esta biblioteca gere o _debounce_ e a latência de forma otimizada para obter resultados em menos de **50ms**.

**Documentação:**
[Guia Oficial do Meilisearch sobre Integração Frontend (React InstantSearch)](https://www.meilisearch.com/docs/learn/front_end_integration/react)

#### 2.4. Renderizar Resultados com Highlights

**Objetivo:**
Apresente os resultados da pesquisa.

**Descrição:**
Os resultados do InstantSearch incluem os campos formatados (`_formatted`). Renderize os snippets de texto do Meilisearch que contêm as tags de destaque, garantindo que o utilizador vê exatamente onde o termo de pesquisa foi encontrado.

#### 2.5. Testar Pesquisa Instantânea

**Testes Manuais:**

1. **Pesquisa Básica:**

 - Navegue para `/incidents`
 - Digite na search box: "hardware"
 - Resultados devem aparecer em <50ms
 - Termos encontrados devem estar destacados (highlights)

2. **Typo Tolerance:**

 - Digite: "hardwre" (falta 'a')
 - Deve retornar resultados de "hardware"
 - Digite: "sofware" (falta 't')
 - Deve retornar resultados de "software"

3. **Pesquisa por Número:**

 - Digite: "INC-20241114-0001"
 - Deve retornar incidente exato
 - Digite apenas: "0001"
 - Deve retornar incidentes com esse número

4. **Search + Filtros:**

 - Digite: "issue"
 - Aplique filtro: status=NEW
 - Resultados devem combinar pesquisa + filtro

5. **Verificar Highlights:**
 - Pesquise: "network problem"
 - Verifique HTML: `<mark>network</mark>` e `<mark>problem</mark>`
 - Highlights devem ter estilo visual (background amarelo)

**Teste E2E (Opcional):**

```typescript
// next-frontend/e2e/incidents/search.spec.ts
test("pesquisa com typo tolerance", async ({ page }) => {
 await page.goto("/incidents");

 const searchBox = page.locator('[placeholder*="Search"]');
 await searchBox.fill("hardwre"); // typo: "hardware"

 // Esperar debounce
 await page.waitForTimeout(300);

 // Verificar resultados
 await expect(page.locator(".search-result").first()).toBeVisible();

 // Verificar highlights
 const highlights = page.locator("mark");
 await expect(highlights).toHaveCount({ gte: 1 });

 // Verificar texto destacado contém termo similar
 const firstHighlight = await highlights.first().textContent();
 expect(firstHighlight.toLowerCase()).toContain("hardw");
});

test("pesquisa instantânea (<50ms)", async ({ page }) => {
 await page.goto("/incidents");

 const searchBox = page.locator('[placeholder*="Search"]');

 const startTime = Date.now();
 await searchBox.fill("test");
 await page.waitForSelector(".search-result", { timeout: 100 });
 const endTime = Date.now();

 const responseTime = endTime - startTime;
 expect(responseTime).toBeLessThan(100); // <100ms (inclui debounce)
});
```

**Documentação:**
[Playwright Performance Testing](https://playwright.dev/docs/clock)

---

## Conclusão do Sprint

> **Nota:** Testes práticos devem ser integrados em cada fase durante o desenvolvimento (TDD).

### Comandos Úteis

**Backend:**

```bash
# Unit tests
npm run test

# Specific file
npm run test -- incidents.service.spec.ts

# Watch mode
npm run test:watch

# Coverage
npm run test:cov

# E2E
npm run test:e2e
```

**Frontend:**

```bash
# Component tests
npm test

# E2E com Playwright
npm run test:e2e

# E2E com UI
npm run test:e2e -- --ui
```

### Coverage Mínimo Recomendado

- **Backend Services:** > 80%
- **Backend Controllers:** > 70%
- **Frontend Components:** > 70%
- **E2E Critical Flows:** 100% (Criar Incidente, Pesquisa)

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

- **Meilisearch:** `MEILISEARCH_HOST` deve apontar para o container Docker (localhost:7700 em dev)
- **AWS S3:** Configurar credenciais IAM com permissões S3 (PutObject, GetObject)
- **Presigned URLs:** Expiram em 1 hora por segurança

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

- **Meilisearch no Frontend:** Permite pesquisa instantânea direta do browser
- **Security:** Em produção, use API key com permissões limitadas (search-only)

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

- Pesquisa não retorna resultados
- Console: "MeiliSearchApiError: Index not found"

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

- Erro 403 Forbidden ao fazer upload
- Imagens não aparecem no editor

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

- Editor funciona mas ao guardar perde formatação
- JSON retornado está vazio

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

- Selecionar filtros não atualiza tabela
- URL não muda quando aplica filtros

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

- Delay visível ao digitar na search box
- Meilisearch retorna resultados mas demora

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
