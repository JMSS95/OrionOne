# Guia de Implementação Detalhado do Sprint 3: Comentários & Anexos

## Visão Geral do Sprint

**Objetivo:**
Permitir a colaboração em incidentes através de um sistema de comentários e a capacidade de anexar ficheiros para fornecer contexto adicional.

**User Stories:**

- [Em Curso] US3.1: Adicionar e Visualizar Comentários num Incidente
- [Em Curso] US3.2: Anexar e Listar Ficheiros num Incidente

**Pré-requisitos:**

- Sprint 1 completo (Autenticação)
- Sprint 2 completo (CRUD de Incidentes)

---

## Funcionalidade 3.1: Sistema de Comentários

**Objetivo:** Implementar um "vertical slice" que permita a um utilizador autenticado adicionar um comentário de texto simples a um incidente e visualizar todos os comentários associados a esse incidente, ordenados cronologicamente.

---

### Fase 1: Base de Dados (Prisma & PostgreSQL)

#### 1.1. Localizar e Editar o Schema

**Ficheiro:** `nest-backend/prisma/schema.prisma`

**Ação:**
Abra o ficheiro para adicionar o modelo de dados para os comentários.

#### 1.2. Definir o Modelo `Comment`

**Objetivo:**
Adicionar o `model Comment` para armazenar o conteúdo dos comentários e a sua relação com utilizadores e incidentes.

**Descrição:**

- **Campos Essenciais:**
 - `id`: Identificador único.
 - `content`: Do tipo `String`, para armazenar o texto do comentário.
 - `createdAt`, `updatedAt`: Timestamps automáticos.
- **Relações:**
 - Crie uma relação `author` com o modelo `User` (muitos-para-um).
 - Crie uma relação `incident` com o modelo `Incident` (muitos-para-um).

**Documentação:**
[Guia Oficial do Prisma sobre Relações](https://www.prisma.io/docs/orm/prisma-schema/data-model/relations)

#### 1.3. Executar a Migração

**Comando:**

```bash
cd nest-backend
npm run prisma:migrate:dev -- --name add_comments_table
```

**O que acontece:**
O Prisma gera e aplica um ficheiro SQL que cria a nova tabela `comments` na base de dados, com as colunas e relações definidas.

**Documentação:**
[Guia Oficial do Prisma sobre Migrações](https://www.prisma.io/docs/orm/prisma-migrate/getting-started)

---

### Fase 2: Backend (Nest.js)

#### 2.1. Gerar o Recurso `comments`

**Comando:**

```bash
cd nest-backend
nest g resource comments --no-spec
```

**Resultado:**
Cria a estrutura base para o módulo de comentários, incluindo controller, service e DTOs.

**Documentação:**
[Guia Oficial do Nest.js sobre Geração de Recursos](https://docs.nestjs.com/cli/generators#resource-generator)

#### 2.2. Definir o `CreateCommentDto`

**Ficheiro:** `nest-backend/src/comments/dto/create-comment.dto.ts`

**Objetivo:**
Definir a estrutura de dados para a criação de um comentário.

**Validação (usando `class-validator`):**

- `@IsString()` e `@IsNotEmpty()` para o campo `content`.
- `@IsString()` e `@IsNotEmpty()` para o campo `incidentId`, que será usado para associar o comentário.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação](https://docs.nestjs.com/techniques/validation)

#### 2.3. Implementar o `CommentsService`

**Ficheiro:** `nest-backend/src/comments/comments.service.ts`

**Ações:**

1. **`create()`**:
 - Recebe o `CreateCommentDto` e o `userId` do utilizador autenticado.
 - Cria um novo registo na tabela `Comment`, associando o `authorId` e o `incidentId`.
2. **`findAllForIncident()`**:
 - Recebe um `incidentId`.
 - Retorna todos os comentários para esse incidente, incluindo os dados do autor (`include: { author: true }`).
 - Ordene os resultados por `createdAt` em ordem ascendente para mostrar os mais antigos primeiro.

**Documentação:**
[Guia Oficial do Prisma sobre Criação de Registos](https://www.prisma.io/docs/orm/prisma-client/queries/crud#create)

#### 2.4. Configurar o `CommentsController`

**Ficheiro:** `nest-backend/src/comments/comments.controller.ts`

**Objetivo:**
Definir as rotas da API para gerir comentários.

**Ações:**

- **`POST /`**: Rota para criar um novo comentário. Protegida com `@UseGuards(JwtAuthGuard)`.
- **`GET /incident/:incidentId`**: Rota para listar todos os comentários de um incidente específico. Protegida com `@UseGuards(JwtAuthGuard)`.

**Documentação:**
[Guia Oficial do Nest.js sobre Controllers](https://docs.nestjs.com/controllers)

#### 2.5. Escrever Testes (TDD)

**Ficheiro:** `nest-backend/src/comments/comments.service.spec.ts`

**Testes Essenciais:**

```typescript
describe("CommentsService", () => {
 it("deve criar comentário com dados válidos", async () => {
 const dto = {
 content: "Este é um comentário de teste",
 incidentId: "incident-123",
 };
 const userId = "user-456";
 const result = await service.create(dto, userId);
 expect(result.id).toBeDefined();
 expect(result.authorId).toBe(userId);
 });

 it("deve listar comentários de um incidente ordenados por data", async () => {
 const incidentId = "incident-123";
 const comments = await service.findAllForIncident(incidentId);
 expect(comments).toBeInstanceOf(Array);
 // Verificar ordenação ascendente
 for (let i = 1; i < comments.length; i++) {
 expect(comments[i].createdAt >= comments[i - 1].createdAt).toBe(
 true
 );
 }
 });

 it("deve incluir dados do autor nos comentários", async () => {
 const incidentId = "incident-123";
 const comments = await service.findAllForIncident(incidentId);
 expect(comments[0].author).toBeDefined();
 expect(comments[0].author.name).toBeDefined();
 });
});
```

**Executar:**

```bash
npm run test -- comments.service.spec.ts
```

**Documentação:**
[Nest.js Testing](https://docs.nestjs.com/fundamentals/testing)

---

### Fase 3: Frontend (Next.js)

#### 3.1. Criar Componentes de Comentários

**Ficheiros:**

- `next-frontend/components/comments/comment-list.tsx`
- `next-frontend/components/comments/comment-item.tsx`
- `next-frontend/components/comments/comment-form.tsx`

**Objetivo:**
Criar os componentes de UI para exibir e adicionar comentários.

**Descrição:**

- **`CommentList`**: Faz o fetch dos dados de `GET /api/comments/incident/:id` e mapeia os resultados, renderizando um `CommentItem` para cada um.
- **`CommentItem`**: Exibe o avatar do autor, nome, data e o conteúdo do comentário.
- **`CommentForm`**: Um formulário simples com uma `Textarea` (shadcn/ui) e um botão de submissão.

**Documentação:**
[Guia Oficial do React sobre Composição de Componentes](https://react.dev/learn/passing-props-to-a-component)

#### 3.2. Integrar na Página de Detalhes do Incidente

**Ficheiro:** `next-frontend/app/incidents/[id]/page.tsx`

**Objetivo:**
Adicionar a secção de comentários à página de detalhes de um incidente.

**Ações:**

- Abaixo dos detalhes principais do incidente, renderize o componente `CommentList`.
- Abaixo da lista de comentários, renderize o componente `CommentForm`.
- Use `TanStack Query` para gerir o estado dos comentários, incluindo o re-fetching da lista após a submissão de um novo comentário.

**Documentação:**
[Guia do TanStack Query sobre Invalidação de Queries](https://tanstack.com/query/latest/docs/react/guides/query-invalidation)

#### 3.3. Testar o Fluxo de Comentários

**Testes Manuais:**

1. **Adicionar Comentário:**

 - Navegue para `http://localhost:3000/incidents/[id]` (um incidente existente)
 - Localize a secção de comentários na parte inferior da página
 - Digite um comentário no formulário
 - Submeta → comentário deve aparecer instantaneamente na lista
 - Verifique: nome do autor, avatar e timestamp estão corretos
 - Atualize a página → comentário persiste
 - Verifique PostgreSQL: registo criado na tabela `comments`

2. **Listar Comentários:**
 - Abra um incidente que já tenha vários comentários
 - Verifique: comentários aparecem ordenados cronologicamente (mais antigos primeiro)
 - Verifique: cada comentário mostra o avatar e nome do autor
 - Verifique: timestamps formatados corretamente

**Teste E2E (Opcional):**

```typescript
// next-frontend/e2e/incidents/comments.spec.ts
test("adicionar e visualizar comentário", async ({ page }) => {
 await page.goto("/incidents/INC-20251114-0001");

 // Adicionar comentário
 const commentText = "Teste de comentário E2E";
 await page.fill('[name="content"]', commentText);
 await page.click('button:has-text("Adicionar Comentário")');

 // Verificar se aparece na lista
 await expect(page.getByText(commentText)).toBeVisible();
 await expect(page.locator(".comment-item").first()).toContainText(
 commentText
 );
});
```

**Documentação:**
[Playwright Testing Guide](https://playwright.dev/)

---

## Funcionalidade 3.2: Anexos de Ficheiros (Armazenamento Local)

**Objetivo:** Permitir que os utilizadores façam upload de ficheiros (ex: logs, screenshots) para um incidente. No MVP, usaremos o **sistema de ficheiros local do servidor Nest.js**. O upload para um serviço de cloud (S3) é uma melhoria para o pós-MVP.

---

### Fase 1: Base de Dados (Prisma)

#### 1.1. Definir o Modelo `Attachment`

**Ficheiro:** `nest-backend/prisma/schema.prisma`

**Objetivo:**
Adicionar o `model Attachment` para rastrear os ficheiros anexados.

**Descrição:**

- **Campos:** `id`, `filename`, `filepath`, `mimetype`, `size`.
- **Relações:** Crie uma relação `incident` com o modelo `Incident` e `uploadedBy` com o modelo `User`.

#### 1.2. Executar a Migração

**Comando:**

```bash
cd nest-backend
npm run prisma:migrate:dev -- --name add_attachments_table
```

---

### Fase 2: Backend (Nest.js)

#### 2.1. Configurar o `MulterModule`

**Ficheiro:** `nest-backend/src/app.module.ts`

**Objetivo:**
Configurar o Nest.js para aceitar uploads de ficheiros.

**Ação:**

- Importe o `MulterModule` e registe-o de forma global.
- Configure o destino (`dest`) para uma pasta no servidor (ex: `./uploads`). Crie esta pasta na raiz do projeto Nest.js e adicione-a ao `.gitignore`.

**Documentação:**
[Guia Oficial do Nest.js sobre Upload de Ficheiros](https://docs.nestjs.com/techniques/file-upload)

#### 2.2. Criar o Endpoint de Upload

**Ficheiro:** `nest-backend/src/incidents/incidents.controller.ts`

**Objetivo:**
Criar uma rota para receber o ficheiro e associá-lo a um incidente.

**Ação:**

- Crie um endpoint `POST /:id/attachments`.
- Use os decoradores `@UseInterceptors(FileInterceptor('file'))` e `@UploadedFile()`.
- No service, crie um registo na tabela `Attachment` com os metadados do ficheiro (`file.originalname`, `file.path`, etc.) e o `incidentId`.

#### 2.3. Criar Endpoint para Servir Ficheiros

**Ficheiro:** `nest-backend/src/main.ts`

**Objetivo:**
Permitir que o frontend aceda aos ficheiros que foram guardados localmente.

**Ação:**

- Use o `app.useStaticAssets()` para expor a pasta `./uploads` publicamente.
- Isto cria uma rota virtual (ex: `http://localhost:8000/uploads/filename.txt`) que serve os ficheiros.

**Documentação:**
[Guia Oficial do Nest.js sobre Servir Ativos Estáticos](https://docs.nestjs.com/recipes/serve-static)

#### 2.4. Escrever Testes

**Ficheiro:** `nest-backend/src/incidents/incidents.service.spec.ts` (adicionar testes para anexos)

**Testes Essenciais:**

```typescript
describe("IncidentsService - Anexos", () => {
 it("deve guardar metadados do ficheiro na BD", async () => {
 const file = {
 originalname: "test.pdf",
 path: "./uploads/test-123.pdf",
 mimetype: "application/pdf",
 size: 1024,
 };
 const incidentId = "incident-123";
 const userId = "user-456";

 const result = await service.createAttachment(file, incidentId, userId);
 expect(result.filename).toBe("test.pdf");
 expect(result.filepath).toBe("./uploads/test-123.pdf");
 expect(result.size).toBe(1024);
 });

 it("deve listar anexos de um incidente", async () => {
 const incidentId = "incident-123";
 const attachments = await service.findAttachments(incidentId);
 expect(attachments).toBeInstanceOf(Array);
 expect(attachments[0].filename).toBeDefined();
 });

 it("deve incluir informação do utilizador que fez upload", async () => {
 const incidentId = "incident-123";
 const attachments = await service.findAttachments(incidentId);
 expect(attachments[0].uploadedBy).toBeDefined();
 expect(attachments[0].uploadedBy.name).toBeDefined();
 });
});
```

**Executar:**

```bash
npm run test -- incidents.service.spec.ts
```

---

### Fase 3: Frontend (Next.js)

#### 3.1. Criar Componente de Upload

**Ficheiro:** `next-frontend/components/attachments/attachment-uploader.tsx`

**Objetivo:**
Criar uma UI para o upload de ficheiros.

**Descrição:**

- Use um `<input type="file">` estilizado como um botão ou uma área de "arrastar e soltar" (drag-and-drop).
- Ao selecionar um ficheiro, use `FormData` para o enviar para o endpoint `POST /api/incidents/:id/attachments`.
- Mostre uma barra de progresso durante o upload.

**Documentação:**
[MDN - Usando FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects)

#### 3.2. Integrar na Página de Detalhes do Incidente

**Ficheiro:** `next-frontend/app/incidents/[id]/page.tsx`

**Ação:**

- Adicione uma secção "Anexos".
- Liste os anexos existentes, com links para download que apontam para a rota estática do backend.
- Renderize o componente `AttachmentUploader` para permitir novos uploads.

#### 3.3. Testar o Fluxo de Anexos

**Testes Manuais:**

1. **Fazer Upload de Ficheiro:**

 - Navegue para `http://localhost:3000/incidents/[id]`
 - Localize a secção "Anexos"
 - Clique no botão de upload ou arraste um ficheiro para a área de drop
 - Selecione um ficheiro (ex: `.txt`, `.pdf`, `.png`, `.log`)
 - Verifique: barra de progresso durante o upload
 - Verifique: ficheiro aparece na lista de anexos com nome e tamanho corretos
 - Verifique: ícone apropriado para o tipo de ficheiro

2. **Download de Ficheiro:**

 - Clique no link de um anexo existente
 - Verifique: download inicia corretamente ou ficheiro abre em nova aba (para PDFs/imagens)
 - Verifique: ficheiro baixado é idêntico ao original

3. **Verificar Armazenamento:**

 - Navegue para a pasta `nest-backend/uploads/`
 - Verifique: ficheiro foi guardado fisicamente no servidor
 - Verifique: nome do ficheiro no sistema (pode ser diferente do nome original)

4. **Validações:**
 - Tente fazer upload de um ficheiro muito grande (> 10MB)
 - Verifique: mensagem de erro apropriada
 - Tente fazer upload sem selecionar ficheiro
 - Verifique: botão de submissão desabilitado ou mensagem de erro

**Teste E2E (Opcional):**

```typescript
// next-frontend/e2e/incidents/attachments.spec.ts
test("fazer upload e download de anexo", async ({ page }) => {
 await page.goto("/incidents/INC-20251114-0001");

 // Upload
 const fileInput = page.locator('input[type="file"]');
 await fileInput.setInputFiles("test-files/sample.pdf");

 // Verificar se aparece na lista
 await expect(page.getByText("sample.pdf")).toBeVisible();

 // Testar download
 const downloadPromise = page.waitForEvent("download");
 await page.click('a:has-text("sample.pdf")');
 const download = await downloadPromise;
 expect(download.suggestedFilename()).toBe("sample.pdf");
});
```

**Documentação:**
[Playwright - Downloads](https://playwright.dev/docs/downloads)

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
describe("Comments API (e2e)", () => {
 let app: INestApplication;
 let accessToken: string;

 beforeAll(async () => {
 const moduleFixture = await Test.createTestingModule({
 imports: [AppModule],
 }).compile();

 app = moduleFixture.createNestApplication();
 await app.init();

 // Login para obter token
 const loginResponse = await request(app.getHttpServer())
 .post("/auth/login")
 .send({ email: "test@example.com", password: "Test123!@" });

 accessToken = loginResponse.body.accessToken;
 });

 it("POST /comments - deve criar comentário", () => {
 return request(app.getHttpServer())
 .post("/comments")
 .set("Authorization", `Bearer ${accessToken}`)
 .send({
 content: "Teste de comentário",
 incidentId: "incident-123",
 })
 .expect(201)
 .expect((res) => {
 expect(res.body.id).toBeDefined();
 expect(res.body.content).toBe("Teste de comentário");
 });
 });

 it("GET /comments/incident/:id - deve listar comentários", () => {
 return request(app.getHttpServer())
 .get("/comments/incident/incident-123")
 .set("Authorization", `Bearer ${accessToken}`)
 .expect(200)
 .expect((res) => {
 expect(res.body).toBeInstanceOf(Array);
 expect(res.body[0].author).toBeDefined();
 });
 });

 afterAll(async () => {
 await app.close();
 });
});
```
