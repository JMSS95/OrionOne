# Guia de Implementação Detalhado do Sprint 1: Autenticação & Gestão de Utilizadores

## Visão Geral do Sprint

**Objetivo:**
Implementar sistema completo de autenticação com gestão de utilizadores e RBAC.

**User Stories:**

- [Completa] US1.1: Registo de Utilizador
- [Completa] US1.2: Login de Utilizador
- [Em Curso] US1.3: Reset de Password
- [Em Curso] US1.4: Gestão de Perfil
- [Em Curso] US1.5: Controlo de Acesso Baseado em Roles (RBAC)

**Pré-requisitos:**
Sprint 0 completo (Docker a funcionar, Next.js + Nest.js inicializados)

---

## Funcionalidade 1.1: Registo de Utilizador (US1.1)

**Objetivo:** Implementar o primeiro "vertical slice". Um utilizador anónimo deve conseguir submeter um formulário, ter os dados validados e guardados no backend, e receber um email de verificação para ativar a conta.

---

### Fase 1: Base de Dados (Prisma & PostgreSQL)

#### 1.1. Localizar e Editar o Schema

**Ficheiro:** `nest-backend/prisma/schema.prisma`

**Ação:**
Abra o ficheiro `nest-backend/prisma/schema.prisma`. Este ficheiro é a única fonte de verdade para a estrutura da sua base de dados PostgreSQL.

#### 1.2. Definir o Modelo User

**Objetivo:**
Escrever a definição do `model User` que irá mapear diretamente para uma tabela `users` na BD.

**Campos Obrigatórios:**

- `email` - use `@unique` para garantir que não há duplicados
- `password` - será armazenada como hash
- `name` - nome do utilizador

**Campos de Suporte:**

- `role` - Para o RBAC (US1.5). Crie um `enum Role` com valores `ADMIN`, `AGENT`, `USER`
- `isActive` - `Boolean` com `@default(false)` para controlar a ativação da conta após verificação do email

**Documentação:**
[Guia Oficial do Prisma sobre Modelos de Dados e Tipos](https://www.prisma.io/docs/orm/prisma-schema/data-model)

#### 1.3. Definir o Modelo VerificationToken

**Objetivo:**
Criar modelo `VerificationToken` crucial para US1.1 (verificação de email) e US1.3 (reset de password).

**Campos Necessários:**

- `token` - único, identificador do token
- `email` - ou uma relação com o `User`
- `expiresAt` - `DateTime` para controlar expiração
- `type` - enum `TokenType` com `EMAIL_VERIFICATION` e `PASSWORD_RESET`

**Documentação:**
[Guia Oficial do Prisma sobre Relações](https://www.prisma.io/docs/orm/prisma-schema/data-model/relations)

#### 1.4. Executar a Migração

**Comando:**

```bash
cd nest-backend
npm run prisma:migrate:dev -- --name init_auth_tables
```

**O que acontece:**

1. Guarda o seu schema
2. Gera um ficheiro SQL com as alterações
3. Aplica esse ficheiro SQL à base de dados PostgreSQL, criando fisicamente as tabelas

**Documentação:**
[Guia Oficial do Prisma sobre Migrações](https://www.prisma.io/docs/orm/prisma-migrate/getting-started)

#### 1.5. Criar Seeds (Opcional, mas Recomendado)

**Ficheiro:** `nest-backend/prisma/seed.ts`

**Objetivo:**
Criar um utilizador ADMIN inicial para testar o RBAC (US1.5). O seeding permite ter dados consistentes no desenvolvimento.

**Documentação:**
[Guia Oficial do Prisma sobre Seeding](https://www.prisma.io/docs/orm/prisma-migrate/workflows/seeding)

---

### Fase 2: Backend (Nest.js)

#### 2.1. Gerar a Estrutura do Módulo

**Comando:**

```bash
nest g resource auth --no-spec
```

**Resultado:**
Cria automaticamente `auth.module.ts`, `auth.controller.ts`, `auth.service.ts` e a pasta `dto`, poupando trabalho manual.

**Documentação:**
[Guia Oficial do Nest.js sobre Geração de Recursos](https://docs.nestjs.com/cli/generators#resource-generator)

#### 2.2. Definir o DTO (Data Transfer Object)

**Ficheiro:** `nest-backend/src/auth/dto/register-user.dto.ts`

**Objetivo:**
Definir a "forma" dos dados que o endpoint de registo espera. É a primeira camada de validação.

**Validação Necessária:**

- `@IsEmail()` - valida formato do email
- `@IsString()` - valida tipo string
- `@MinLength(8)` - password mínima de 8 caracteres
- `@Matches()` - força da password (maiúscula, minúscula, número)

**Documentação:**
[Guia Oficial do Nest.js sobre Validação](https://docs.nestjs.com/techniques/validation)

#### 2.3. Implementar o Hashing de Password

**Ficheiro:** `nest-backend/src/auth/auth.service.ts`

**Ação:**

1. Injete o `PrismaService` para comunicar com a BD
2. Implemente a função `register()`
3. Use a biblioteca `bcrypt` para fazer hash da password antes de guardar

**Nota:**
O `AuthService` é o local correto para esta lógica de negócio.

**Documentação:**
[Guia Oficial do Nest.js sobre Hashing](https://docs.nestjs.com/security/authentication#implementing-hashing)

#### 2.4. Implementar o Serviço de Email

**Configuração:**
Configure o `NodemailerModule` (@nestjs/nodemailer) no `AppModule`.

**Implementação:**

1. Injete o `MailerService` no `AuthService`
2. Crie função privada `sendVerificationEmail` que:
 - Gera token aleatório seguro (`crypto.randomBytes`)
 - Guarda token na tabela `VerificationToken`
 - Envia email com link de verificação (`http://localhost:3000/verify-email?token=...`)

**Documentação:**
[Guia Oficial do Nest.js sobre Email](https://docs.nestjs.com/techniques/email)

#### 2.5. Criar o Endpoint de Registo

**Rota:** `POST /api/auth/register`

**Ficheiro:** `nest-backend/src/auth/auth.controller.ts`

**Implementação:**

- Use decorador `@Body()` para receber `RegisterUserDto`
- O `ValidationPipe` (em `main.ts`) valida automaticamente o body
- Se válido, chama `this.authService.register(dto)`

**Documentação:**
[Guia Oficial do Nest.js sobre Controllers](https://docs.nestjs.com/controllers)

#### 2.6. Criar o Endpoint de Verificação

**Rota:** `POST /api/auth/verify-email/:token`

**Implementação:**

1. Recebe `token` via `@Param()`
2. Chama função `activateAccount` no `AuthService`
3. Procura token na BD e verifica se não expirou
4. Define `user.isActive = true`
5. Apaga o token usado

**Documentação:**
[Guia Oficial do Nest.js sobre Parâmetros de Rota](https://docs.nestjs.com/controllers#route-parameters)

#### 2.7. Escrever Testes (TDD)

**Ficheiro:** `nest-backend/src/auth/auth.service.spec.ts`

**Testes Essenciais:**

```typescript
describe("AuthService - Registo", () => {
 it("deve criar utilizador com dados válidos", async () => {
 const dto = {
 email: "test@example.com",
 password: "Test123!@",
 name: "Test",
 };
 const result = await service.register(dto);
 expect(result.userId).toBeDefined();
 });

 it("deve lançar ConflictException se email existe", async () => {
 // Criar user primeiro
 await expect(service.register(dto)).rejects.toThrow(ConflictException);
 });

 it("deve fazer hash da password", async () => {
 // Verificar que password guardada != password original
 });
});
```

**Executar:**

```bash
npm run test -- auth.service.spec.ts
```

**Documentação:**
[Nest.js Testing](https://docs.nestjs.com/fundamentals/testing)

---

### Fase 3: Frontend (Next.js)

#### 3.1. Criar a Página de Registo

**Ficheiro:** `next-frontend/app/register/page.tsx`

**Estrutura:**

- Esta é uma Rota do App Router por defeito
- O formulário TEM de ser um Componente de Cliente
- Crie ficheiro separado `register-form.tsx` com `"use client";` no topo
- Importe-o na `page.tsx`

**Documentação:**
[Guia Oficial do Next.js sobre Componentes de Cliente vs. Servidor](https://nextjs.org/docs/app/building-your-application/rendering/client-components)

#### 3.2. Definir o Schema de Validação (Frontend)

**Biblioteca:** Zod

**Objetivo:**
Criar schema `registerSchema` que espelha as regras do DTO do Nest.js.

**Benefício:**
Validação instantânea no browser, melhorando UX antes de qualquer chamada à API.

**Documentação:**
[Guia Oficial do Zod - Basics](https://zod.dev/?id=basics)

#### 3.3. Configurar o Formulário

**Biblioteca:** React Hook Form

**Implementação:**

1. Use `useForm` do React Hook Form
2. Importe e use `zodResolver` para ligar schema Zod ao formulário
3. Isto automatiza a validação no cliente

**Documentação:**
[Guia Oficial do React Hook Form](https://react-hook-form.com/get-started)

#### 3.4. Construir a UI do Formulário

**Componentes:** shadcn/ui

**Componentes Necessários:**

- `Form` - wrapper do formulário
- `FormField` - campo individual (integra com React Hook Form)
- `FormControl` - controlo do input
- `FormMessage` - mensagens de erro
- `Input` - campos de texto
- `Button` - botão de submissão

**Documentação:**
[Guia Oficial do shadcn/ui sobre Form](https://ui.shadcn.com/docs/components/form)

#### 3.5. Implementar a Submissão

**Função:** `onSubmit`

**Fluxo:**

1. Função é passada para `form.handleSubmit(onSubmit)`
2. Recebe dados já validados pelo Zod
3. Use `Axios` ou `fetch` para fazer `POST` para `http://localhost:8000/api/auth/register`

**Documentação:**
[Guia Oficial do Axios - POST](https://axios-http.com/docs/post_example)

#### 3.6. Gerir Feedback (Toast)

**Hook:** `useToast` do shadcn/ui

**Implementação:**

```javascript
try {
 // chamada API
 toast({ title: "Sucesso", ... })
} catch {
 toast({ title: "Erro", variant: "destructive", ... })
}
```

**Documentação:**
[Guia Oficial do shadcn/ui sobre Toast](https://ui.shadcn.com/docs/components/toast)

#### 3.7. Testar o Fluxo Completo

**Testes Manuais:**

1. Navegue para `http://localhost:3000/register`
2. Teste validações:
 - Submeta formulário vazio → deve mostrar erros
 - Email inválido → erro de formato
 - Password fraca → erro de requisitos
3. Registo válido:
 - Preencha todos os campos corretamente
 - Submeta → mensagem de sucesso
 - Verifique PostgreSQL: user criado com `isActive: false`
 - Console backend: token de verificação
4. Verificação:
 - Copie URL de verificação do console
 - Abra no browser
 - Verifique BD: `isActive: true`

**Teste E2E (Opcional):**

```typescript
// next-frontend/e2e/register.spec.ts
test("fluxo completo de registo", async ({ page }) => {
 await page.goto("/register");
 await page.fill('[name="name"]', "Test User");
 await page.fill('[name="email"]', `test-${Date.now()}@example.com`);
 await page.fill('[name="password"]', "Test123!@");
 await page.click('button[type="submit"]');
 await expect(page.getByText(/check your email/i)).toBeVisible();
});
```

---

## Funcionalidade 1.2: Login de Utilizador (US1.2)

**Objetivo:**
Permitir que um utilizador ativado (da US1.1) faça login e receba um JWT seguro num cookie `httpOnly`.

---

### Fase 1: Base de Dados (Prisma)

#### 1.1. Definir o Modelo Session (Opcional, mas Recomendado)

**Ficheiro:** `nest-backend/prisma/schema.prisma`

**Objetivo:**
Implementar "Remember Me" com refresh tokens de 30 dias e permitir "logout de todos os dispositivos" seguro.

**Implementação:**
Guardar refresh tokens na BD ligados ao `User`.

**Documentação:**
Reutilize os links do Prisma da Fase 1.1

#### 1.2. Executar Migração

**Comando:**

```bash
npm run prisma:migrate:dev -- --name add_sessions_table
```

---

### Fase 2: Backend (Nest.js)

#### 2.1. Instalar Dependências

**Comando:**

```bash
npm install @nestjs/passport @nestjs/jwt passport passport-local passport-jwt
```

**Estratégias a Implementar:**

1. `LocalStrategy` - Valida email e password no momento do login
2. `JwtStrategy` - Valida JWT do cookie em todos os pedidos subsequentes

**Documentação:**
[Guia Oficial do Nest.js sobre Autenticação](https://docs.nestjs.com/security/authentication)

#### 2.2. Implementar a LocalStrategy

**Ficheiro:** `nest-backend/src/auth/strategies/local.strategy.ts`

**Implementação:**

1. Injete o `AuthService`
2. Implemente função `validate()`
3. Recebe `email` e `password`
4. Procura utilizador e usa `bcrypt.compare()` para verificar password
5. Se válida, retorna objeto `user`

**Documentação:**
[Guia Oficial do Nest.js sobre LocalStrategy](https://docs.nestjs.com/security/authentication#implementing-localstrategy)

#### 2.3. Implementar a JwtStrategy

**Ficheiro:** `nest-backend/src/auth/strategies/jwt.strategy.ts`

**Responsabilidade:**
Ler e validar JWT em TODOS os pedidos futuros.

**Fluxo:**

1. Extrai token do cookie `httpOnly`
2. Valida assinatura e expiração
3. Anexa payload (`userId`, `role`) ao `request.user`

**Documentação:**
[Guia Oficial do Nest.js sobre JwtStrategy](https://docs.nestjs.com/security/authentication#implementing-jwt)

#### 2.4. Atualizar o AuthService (Login)

**Função:** `login(user: any)`

**Quando é Chamada:**
Depois da `LocalStrategy` ser bem-sucedida.

**Responsabilidade:**

1. Recebe objeto `user`
2. Gera tokens JWT:
 - `accessToken` - 15 minutos
 - `refreshToken` - 7-30 dias
3. Guarda `refreshToken` na tabela `Session`

#### 2.5. Criar o Endpoint de Login

**Rota:** `POST /api/auth/login`

**Implementação:**

1. Proteja com `@UseGuards(AuthGuard('local'))` - ativa `LocalStrategy`
2. Injete `Response` usando `@Res()`
3. Use `response.cookie()` para definir tokens como `httpOnly`

**Documentação:**
[Guia Oficial do Nest.js sobre Cookies](https://docs.nestjs.com/techniques/cookies)

#### 2.6. Criar o Endpoint /me

**Rota:** `GET /api/auth/me`

**Implementação:**

1. Proteja com `@UseGuards(AuthGuard('jwt'))` - ativa `JwtStrategy`
2. Função simples: `return request.user;`
3. A `JwtStrategy` já validou e anexou o utilizador

**Documentação:**
[Guia Oficial do Nest.js sobre Guards](https://docs.nestjs.com/guards)

#### 2.7. Criar o Endpoint de Logout

**Rota:** `POST /api/auth/logout`

**Implementação:**

1. Protegida por JWT
2. Apaga `refreshToken` da tabela `Session`
3. Instrui browser a limpar cookies

#### 2.8. Testar Endpoints

**Testes com Postman/Insomnia:**

1. **POST** `/auth/login`

 - Body: `{ "email": "admin@orionone.com", "password": "Admin123!" }`
 - Verificar: cookies `access_token` e `refresh_token` definidos
 - Status: 200

2. **GET** `/auth/me`

 - Usar cookies do passo anterior
 - Verificar: dados do utilizador retornados
 - Status: 200

3. **GET** `/auth/me` (sem cookies)
 - Não enviar cookies
 - Verificar: erro de autenticação
 - Status: 401

**Testes Automatizados:**

```typescript
// auth.service.spec.ts
describe("AuthService - Login", () => {
 it("deve validar credenciais corretas", async () => {
 const user = await service.validateUser(
 "admin@orionone.com",
 "Admin123!"
 );
 expect(user).toBeDefined();
 expect(user.email).toBe("admin@orionone.com");
 });

 it("deve retornar null para password incorreta", async () => {
 const user = await service.validateUser("admin@orionone.com", "wrong");
 expect(user).toBeNull();
 });

 it("deve gerar tokens JWT", async () => {
 const tokens = await service.login(mockUser);
 expect(tokens.accessToken).toBeDefined();
 expect(tokens.refreshToken).toBeDefined();
 });
});
```

---

### Fase 3: Frontend (Next.js)

#### 3.1. Criar Página e Formulário de Login

**Ficheiro:** `next-frontend/app/login/page.tsx`

**Processo:**
Siga EXATAMENTE o mesmo processo da Funcionalidade 1.1 (passos 3.1-3.6):

- "use client"
- Schema Zod
- React Hook Form
- shadcn/ui
- Função `onSubmit` que faz `POST` para `/api/auth/login`

#### 3.2. Configurar o Cliente Axios (CRÍTICO)

**Ficheiro:** `lib/api/client.ts`

**Configuração Obrigatória:**

```javascript
withCredentials: true;
```

**Importante:**
Sem isto, o browser NUNCA irá enviar os cookies `httpOnly` para o backend Nest.js, e a autenticação irá falhar silenciosamente.

**Documentação:**
[Guia Oficial do Axios sobre withCredentials](https://axios-http.com/docs/config_defaults)

#### 3.3. Criar o AuthContext

**Ficheiro:** `context/auth-context.tsx`

**Objetivo:**
Gerir estado global da autenticação.

**Estados:**

- `user` - objeto com dados do utilizador
- `isAuthenticated` - boolean
- `isLoading` - boolean

**Documentação:**
[Guia Oficial do React sobre Context](https://react.dev/reference/react/createContext)

#### 3.4. Implementar o AuthProvider

**Localização:** Envolve aplicação em `app/layout.tsx`

**Implementação:**

1. `useEffect` na montagem (`[]`)
2. Chama endpoint `/api/auth/me`
3. Se 200 OK: define `user` e `isAuthenticated = true`
4. Se 401: define `isAuthenticated = false`
5. Sempre: define `isLoading = false`

#### 3.5. Implementar Rotas Protegidas

**Ficheiro:** `components/require-auth.tsx`

**Lógica:**

- Se `isLoading` → mostra spinner
- Se `!isAuthenticated` e `!isLoading` → redireciona para `/login`
- Se `isAuthenticated` → renderiza `children`

**Alternativa:**
Use Middleware do Next.js para verificação no servidor.

**Documentação:**
[Guia Oficial do Next.js sobre Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware)

#### 3.6. Validar Autenticação

**Fluxo de Teste Manual:**

1. **Login bem-sucedido:**

 - Aceda a `/login`
 - Use credenciais do seed (admin@orionone.com / Admin123!)
 - Verifique redirecionamento para dashboard
 - Console: cookies definidos

2. **AuthContext funcionando:**

 - Após login, verifique `user` no React DevTools
 - `isAuthenticated` deve ser `true`
 - `isLoading` deve ser `false`

3. **Rotas protegidas:**

 - Tente aceder `/dashboard` sem login
 - Deve redirecionar para `/login`
 - Após login, `/dashboard` deve ser acessível

4. **Logout:**

 - Clique botão logout
 - Cookies devem ser limpos (ver DevTools > Application > Cookies)
 - Deve redirecionar para `/login`
 - Tentar aceder `/dashboard` → redireciona novamente

5. **Token expirado:**
 - Login
 - Espere 16+ minutos (accessToken expira)
 - Tente aceder recurso protegido
 - Deve redirecionar para login (ou renovar com refresh token)

---

## Funcionalidades 1.3, 1.4, 1.5: Tarefas Restantes do Sprint 1

Siga o mesmo padrão vertical para as restantes funcionalidades do sprint.

---

### US1.3: Reset de Password

**Backend:**

Endpoints:

- `POST /api/auth/forgot-password` - gera token
- `POST /api/auth/reset-password/:token` - valida e altera password

Fluxo idêntico à verificação de email, mas usa tipo `PASSWORD_RESET` no `VerificationToken`.

**Frontend:**

Páginas:

- `app/forgot-password/page.tsx` - formulário para pedir reset
- `app/reset-password/[token]/page.tsx` - formulário para nova password

---

### US1.4: Gestão de Perfil

**Backend:**

Endpoints protegidos por JWT:

- `PATCH /api/users/me` - atualiza nome/timezone
- `PATCH /api/users/me/password` - altera password

Importante: Endpoint de mudança de password deve verificar `oldPassword` com `bcrypt.compare()`

**Frontend:**

Página:

- `app/profile/page.tsx` - interface com Tabs (shadcn/ui)
- Separar "Perfil" de "Segurança"

---

### US1.5: Controlo de Acesso Baseado em Roles (RBAC)

**Backend:**

Implementação:

1. Crie `RolesGuard`
2. Lê metadados (ex: `@Roles('ADMIN')`)
3. Compara com `request.user.role` (injetado pela `JwtStrategy`)
4. Proteja endpoints: `@UseGuards(JwtAuthGuard, RolesGuard)` e `@Roles('ADMIN')`

**Documentação:**
[Guia Oficial do Nest.js sobre RBAC](https://docs.nestjs.com/security/authorization#basic-rbac-implementation)

**Frontend:**

Implementação:

1. Exponha `user.role` no `AuthContext`
2. Renderização condicional de elementos UI
3. Exemplo: mostrar link "Admin" apenas se `user.role === 'ADMIN'`

**Documentação:**
[Guia Oficial do React sobre Renderização Condicional](https://react.dev/learn/conditional-rendering)

---

## Referência Rápida: Testes

> **Nota:** Testes práticos estão integrados em cada fase:
>
> - **US1.1 Backend:** Fase 2.7 (Unit tests)
> - **US1.1 Frontend:** Fase 3.7 (Validação manual + E2E)
> - **US1.2 Backend:** Fase 2.8 (Testes de endpoints)
> - **US1.2 Frontend:** Fase 3.6 (Validação de autenticação)

### Comandos Úteis

**Backend:**

```bash
# Unit tests
npm run test

# Specific file
npm run test -- auth.service.spec.ts

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
- **E2E Critical Flows:** 100% (Login, Registo)

### Estrutura de Testes

```
nest-backend/
 src/
 auth/
 auth.service.spec.ts # Unit tests
 auth.controller.spec.ts # Unit tests
 test/
 auth.e2e-spec.ts # Integration tests

next-frontend/
 __tests__/
 components/
 register-form.test.tsx
 login-form.test.tsx
 e2e/
 auth/
 register.spec.ts
 login.spec.ts
```

### Template: Unit Test (Backend)

```typescript
describe("AuthService", () => {
 let service: AuthService;
 let prisma: PrismaService;

 beforeEach(async () => {
 const module = await Test.createTestingModule({
 providers: [
 AuthService,
 { provide: PrismaService, useValue: mockPrisma },
 ],
 }).compile();

 service = module.get<AuthService>(AuthService);
 prisma = module.get<PrismaService>(PrismaService);
 });

 it("deve criar utilizador", async () => {
 // Arrange
 const dto = {
 email: "test@example.com",
 password: "Test123!@",
 name: "Test",
 };

 // Act
 const result = await service.register(dto);

 // Assert
 expect(result.userId).toBeDefined();
 });
});
```

### Template: E2E Test (Backend)

```typescript
describe("Auth API (e2e)", () => {
 let app: INestApplication;

 beforeAll(async () => {
 const moduleFixture = await Test.createTestingModule({
 imports: [AppModule],
 }).compile();

 app = moduleFixture.createNestApplication();
 await app.init();
 });

 it("POST /auth/register", () => {
 return request(app.getHttpServer())
 .post("/auth/register")
 .send({
 email: "test@example.com",
 password: "Test123!@",
 name: "Test",
 })
 .expect(201);
 });

 afterAll(async () => {
 await app.close();
 });
});
```

### Template: Component Test (Frontend)

```typescript
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { RegisterForm } from "./register-form";

describe("RegisterForm", () => {
 it("deve mostrar erros de validação", async () => {
 render(<RegisterForm />);

 fireEvent.click(screen.getByRole("button", { name: /register/i }));

 await waitFor(() => {
 expect(screen.getByText(/email is required/i)).toBeInTheDocument();
 });
 });
});
```

### Template: E2E Test (Frontend)

```typescript
import { test, expect } from "@playwright/test";

test("fluxo de registo completo", async ({ page }) => {
 await page.goto("/register");

 await page.fill('[name="email"]', "test@example.com");
 await page.fill('[name="password"]', "Test123!@");
 await page.fill('[name="name"]', "Test User");

 await page.click('button[type="submit"]');

 await expect(page.getByText(/check your email/i)).toBeVisible();
});
```

---

## Configuração de Ambiente

### Variáveis de Ambiente

#### Backend (.env)

**Ficheiro:** `nest-backend/.env`

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/orionone_dev?schema=public"

# JWT
JWT_SECRET="your-super-secret-jwt-key-change-in-production"
JWT_EXPIRES_IN="15m"
JWT_REFRESH_EXPIRES_IN="7d"

# Email (Nodemailer)
MAIL_HOST="smtp.gmail.com"
MAIL_PORT=587
MAIL_USER="your-email@gmail.com"
MAIL_PASSWORD="your-app-specific-password"
MAIL_FROM="noreply@orionone.com"

# App
NODE_ENV="development"
PORT=8000
FRONTEND_URL="http://localhost:3000"

# CORS
CORS_ORIGIN="http://localhost:3000"
```

**Importante:**

- NUNCA commitar `.env` para Git
- Usar `.env.example` como template
- Em produção, usar Azure Key Vault ou similar

---

#### Frontend (.env.local)

**Ficheiro:** `next-frontend/.env.local`

```env
# API
NEXT_PUBLIC_API_URL="http://localhost:8000"

# App
NEXT_PUBLIC_APP_NAME="OrionOne ITSM"
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

---

### Configuração CORS

**Ficheiro:** `nest-backend/src/main.ts`

```typescript
async function bootstrap() {
 const app = await NestFactory.create(AppModule);

 // CORS crítico para cookies httpOnly
 app.enableCors({
 origin: process.env.CORS_ORIGIN || "http://localhost:3000",
 credentials: true, // IMPORTANTE!
 methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
 allowedHeaders: ["Content-Type", "Authorization"],
 });

 // Global Validation Pipe
 app.useGlobalPipes(
 new ValidationPipe({
 whitelist: true,
 forbidNonWhitelisted: true,
 transform: true,
 })
 );

 await app.listen(process.env.PORT || 8000);
}
```

---

## Tratamento de Erros

### Exception Filters (Nest.js)

**Ficheiro:** `nest-backend/src/common/filters/http-exception.filter.ts`

```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
 catch(exception: HttpException, host: ArgumentsHost) {
 const ctx = host.switchToHttp();
 const response = ctx.getResponse();
 const status = exception.getStatus();
 const exceptionResponse = exception.getResponse();

 const error = {
 statusCode: status,
 timestamp: new Date().toISOString(),
 message:
 typeof exceptionResponse === "string"
 ? exceptionResponse
 : (exceptionResponse as any).message ||
 "Internal server error",
 errors: (exceptionResponse as any).errors || [],
 };

 response.status(status).json(error);
 }
}
```

**Uso no main.ts:**

```typescript
app.useGlobalFilters(new HttpExceptionFilter());
```

---

### Error Handling (Frontend)

**Ficheiro:** `next-frontend/lib/api/error-handler.ts`

```typescript
export function handleApiError(error: any): string {
 if (error.response) {
 // Backend retornou erro
 const message = error.response.data?.message;

 if (Array.isArray(message)) {
 return message.join(", ");
 }

 return message || "Erro no servidor";
 } else if (error.request) {
 // Pedido feito mas sem resposta
 return "Servidor não responde. Verifique a ligação.";
 } else {
 // Erro ao configurar pedido
 return error.message || "Erro desconhecido";
 }
}
```

**Uso:**

```typescript
try {
 await registerAction(data);
} catch (err) {
 const errorMessage = handleApiError(err);
 toast({ title: "Erro", description: errorMessage, variant: "destructive" });
}
```
