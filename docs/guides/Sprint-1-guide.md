# Guia de Implementação Detalhado do Sprint 1: Autenticação & Gestão de Utilizadores

## Visão Geral do Sprint

**Objetivo:**
Implementar sistema completo de autenticação com gestão de utilizadores e RBAC.

**User Stories:**

-   [Completa] US1.1: Registo de Utilizador
-   [Completa] US1.2: Login de Utilizador
-   [Em Curso] US1.3: Reset de Password
-   [Em Curso] US1.4: Gestão de Perfil
-   [Em Curso] US1.5: Controlo de Acesso Baseado em Roles (RBAC)

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

-   `email` - use `@unique` para garantir que não há duplicados
-   `password` - será armazenada como hash
-   `name` - nome do utilizador

**Campos de Suporte:**

-   `role` - Para o RBAC (US1.5). Crie um `enum Role` com valores `ADMIN`, `AGENT`, `USER`
-   `isActive` - `Boolean` com `@default(false)` para controlar a ativação da conta após verificação do email

**Documentação:**
[Guia Oficial do Prisma sobre Modelos de Dados e Tipos](https://www.prisma.io/docs/orm/prisma-schema/data-model)

#### 1.3. Definir o Modelo VerificationToken

**Objetivo:**
Criar modelo `VerificationToken` crucial para US1.1 (verificação de email) e US1.3 (reset de password).

**Campos Necessários:**

-   `token` - único, identificador do token
-   `email` - ou uma relação com o `User`
-   `expiresAt` - `DateTime` para controlar expiração
-   `type` - enum `TokenType` com `EMAIL_VERIFICATION` e `PASSWORD_RESET`

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

-   `@IsEmail()` - valida formato do email
-   `@IsString()` - valida tipo string
-   `@MinLength(8)` - password mínima de 8 caracteres
-   `@Matches()` - força da password (maiúscula, minúscula, número)

**Documentação:**
[Guia Oficial do Nest.js sobre Validação](https://docs.nestjs.com/techniques/validation)

#### 2.3. Implementar o Hashing e Logging

**Ficheiro:** `nest-backend/src/auth/auth.service.ts`

**Ação:**

<<<<<<< HEAD

1. Injete o `PrismaService` para comunicar com a BD.
2. Injete o `Logger` (`@Inject(WINSTON_MODULE_NEST_PROVIDER)`) para usar o Winston.
3. Implemente a função `register()`.
4. Use a biblioteca `bcrypt` para fazer hash da password antes de guardar.
5. # Adicione logs com Winston para sucesso (`.info()`) e falha (`.error()`) no registo.
6. Injete o `PrismaService` para comunicar com a BD.
7. Injete o `Logger` (`@Inject(WINSTON_MODULE_NEST_PROVIDER)`) para usar o Winston.
8. Implemente a função `register()`.
9. Use a biblioteca `bcrypt` para fazer hash da password antes de guardar.
10. Adicione logs com Winston para sucesso (`.info()`) e falha (`.error()`) no registo.
    > > > > > > > origin/main

**Nota:**
O `AuthService` é o local correto para esta lógica de negócio.

**Documentação:**
<<<<<<< HEAD
[Guia Oficial do Nest.js sobre Encryption e Hashing](https://docs.nestjs.com/security/encryption-and-hashing)
=======
[Guia Oficial do Nest.js sobre Hashing](https://docs.nestjs.com/security/authentication#implementing-hashing)

> > > > > > > origin/main

#### 2.4. Implementar o Serviço de Email

**Configuração:**
O `ConfigModule` já está global. Use o `ConfigService` para obter as credenciais do email a partir do `.env`.

**Implementação:**

<<<<<<< HEAD

1. Injete o `MailerService` e o `ConfigService` no `AuthService`.
2. Crie uma função privada `sendVerificationEmail` que:

-   Gera um token aleatório seguro (`crypto.randomBytes`).
-   Guarda o token na tabela `VerificationToken`.
-   Envia um email com um link de verificação (`http://localhost:3000/verify-email?token=...`).
-   # Regista o envio do email com o Winston para auditoria.

1.  Injete o `MailerService` e o `ConfigService` no `AuthService`.
2.  Crie uma função privada `sendVerificationEmail` que: - Gera um token aleatório seguro (`crypto.randomBytes`). - Guarda o token na tabela `VerificationToken`. - Envia um email com um link de verificação (`http://localhost:3000/verify-email?token=...`). - Regista o envio do email com o Winston para auditoria.
    > > > > > > > origin/main

**Documentação:**
[Guia Oficial do Nest.js sobre Email](https://docs.nestjs.com/techniques/email)
[Guia Oficial do Nest.js sobre Configuração](https://docs.nestjs.com/techniques/configuration)

#### 2.5. Criar e Documentar o Endpoint de Registo

**Rota:** `POST /api/auth/register`

**Ficheiro:** `nest-backend/src/auth/auth.controller.ts`

**Implementação:**

-   Adicione decoradores do Swagger para documentar o endpoint: `@ApiTags`, `@ApiOperation`, `@ApiResponse`.
-   Use o decorador `@Body()` para receber o `RegisterUserDto`.
-   O `ValidationPipe` (configurado globalmente em `main.ts`) valida automaticamente o body.
-   Se a validação for bem-sucedida, o controller chama o método `register` do `AuthService`.

**Documentação:**
[Guia Oficial do Nest.js sobre Controllers](https://docs.nestjs.com/controllers)
[Guia Oficial do Nest.js sobre OpenAPI (Swagger)](https://docs.nestjs.com/openapi/introduction)

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

<<<<<<< HEAD

### Exemplo de Código Completo: Registo de Utilizador (Backend)

#### Schema Prisma - User Model

```prisma
// nest-backend/prisma/schema.prisma
model User {
 id String @id @default(cuid())
 email String @unique
 password String
 name String
 role Role @default(USER)
 isActive Boolean @default(false)
 avatar String?
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt

 sessions Session[]
 verificationTokens VerificationToken[]
}

enum Role {
 ADMIN
 AGENT
 USER
}

model VerificationToken {
 id String @id @default(cuid())
 token String @unique
 email String
 type TokenType
 expiresAt DateTime
 createdAt DateTime @default(now())

 user User @relation(fields: [email], references: [email], onDelete: Cascade)

 @@index([token])
 @@index([email])
}

enum TokenType {
 EMAIL_VERIFICATION
 PASSWORD_RESET
}
```

#### DTO - RegisterUserDto

```typescript
// nest-backend/src/auth/dto/register-user.dto.ts
import { ApiProperty } from "@nestjs/swagger";
import { IsEmail, IsString, MinLength, Matches } from "class-validator";

export class RegisterUserDto {
    @ApiProperty({ example: "john.doe@example.com" })
    @IsEmail({}, { message: "Email inválido" })
    email: string;

    @ApiProperty({ example: "John Doe" })
    @IsString()
    @MinLength(2, { message: "Nome deve ter pelo menos 2 caracteres" })
    name: string;

    @ApiProperty({ example: "StrongPass123!", minLength: 8 })
    @IsString()
    @MinLength(8, { message: "Password deve ter pelo menos 8 caracteres" })
    @Matches(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
        {
            message:
                "Password deve conter maiúscula, minúscula, número e símbolo",
        }
    )
    password: string;
}
```

#### Service - AuthService (Register)

```typescript
// nest-backend/src/auth/auth.service.ts
import { Injectable, ConflictException, Inject, Logger } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { WINSTON_MODULE_NEST_PROVIDER } from "nest-winston";
import * as bcrypt from "bcrypt";
import * as crypto from "crypto";
import { RegisterUserDto } from "./dto/register-user.dto";
import { MailerService } from "@nestjs-modules/mailer";
import { ConfigService } from "@nestjs/config";

@Injectable()
export class AuthService {
    constructor(
        private prisma: PrismaService,
        @Inject(WINSTON_MODULE_NEST_PROVIDER) private readonly logger: Logger,
        private mailerService: MailerService,
        private configService: ConfigService
    ) {}

    async register(dto: RegisterUserDto) {
        this.logger.log(
            `Tentativa de registo para: ${dto.email}`,
            "AuthService"
        );

        // Verificar se email já existe
        const existingUser = await this.prisma.user.findUnique({
            where: { email: dto.email },
        });

        if (existingUser) {
            this.logger.warn(`Email já registado: ${dto.email}`, "AuthService");
            throw new ConflictException("Email já está registado");
        }

        // Hash da password
        const hashedPassword = await bcrypt.hash(dto.password, 12);

        // Criar utilizador
        const user = await this.prisma.user.create({
            data: {
                email: dto.email,
                name: dto.name,
                password: hashedPassword,
                isActive: false,
            },
            select: {
                id: true,
                email: true,
                name: true,
                role: true,
                isActive: true,
                createdAt: true,
            },
        });

        this.logger.log(`Utilizador criado: ${user.id}`, "AuthService");

        // Enviar email de verificação
        await this.sendVerificationEmail(user.email);

        return {
            userId: user.id,
            message: "Registo bem-sucedido. Verifique o seu email.",
        };
    }

    private async sendVerificationEmail(email: string) {
        // Gerar token seguro
        const token = crypto.randomBytes(32).toString("hex");

        // Guardar token na BD (expira em 1 hora)
        await this.prisma.verificationToken.create({
            data: {
                token,
                email,
                type: "EMAIL_VERIFICATION",
                expiresAt: new Date(Date.now() + 3600000), // 1 hora
            },
        });

        const verificationUrl = `${this.configService.get(
            "FRONTEND_URL"
        )}/verify-email?token=${token}`;

        // Enviar email
        await this.mailerService.sendMail({
            to: email,
            subject: "Verificação de Email - OrionOne",
            html: `
 <h2>Bem-vindo ao OrionOne!</h2>
 <p>Clique no link abaixo para verificar o seu email:</p>
 <a href="${verificationUrl}">${verificationUrl}</a>
 <p>Este link expira em 1 hora.</p>
 `,
        });

        this.logger.log(
            `Email de verificação enviado para: ${email}`,
            "AuthService"
        );
    }

    async verifyEmail(token: string) {
        const verificationToken =
            await this.prisma.verificationToken.findUnique({
                where: { token },
            });

        if (!verificationToken || verificationToken.expiresAt < new Date()) {
            throw new ConflictException("Token inválido ou expirado");
        }

        // Ativar utilizador
        await this.prisma.user.update({
            where: { email: verificationToken.email },
            data: { isActive: true },
        });

        // Apagar token usado
        await this.prisma.verificationToken.delete({
            where: { token },
        });

        this.logger.log(
            `Email verificado: ${verificationToken.email}`,
            "AuthService"
        );

        return { message: "Email verificado com sucesso" };
    }
}
```

#### Controller - AuthController (Register)

```typescript
// nest-backend/src/auth/auth.controller.ts
import { Controller, Post, Body, Param } from "@nestjs/common";
import { ApiTags, ApiOperation, ApiResponse } from "@nestjs/swagger";
import { AuthService } from "./auth.service";
import { RegisterUserDto } from "./dto/register-user.dto";

@ApiTags("auth")
@Controller("auth")
export class AuthController {
    constructor(private authService: AuthService) {}

    @Post("register")
    @ApiOperation({ summary: "Registar novo utilizador" })
    @ApiResponse({ status: 201, description: "Utilizador criado com sucesso" })
    @ApiResponse({ status: 409, description: "Email já registado" })
    @ApiResponse({ status: 400, description: "Dados inválidos" })
    async register(@Body() dto: RegisterUserDto) {
        return this.authService.register(dto);
    }

    @Post("verify-email/:token")
    @ApiOperation({ summary: "Verificar email com token" })
    @ApiResponse({ status: 200, description: "Email verificado" })
    @ApiResponse({ status: 409, description: "Token inválido ou expirado" })
    async verifyEmail(@Param("token") token: string) {
        return this.authService.verifyEmail(token);
    }
}
```

---

=======

> > > > > > > origin/main

### Fase 3: Frontend (Next.js)

#### 3.1. Criar a Página de Registo

**Ficheiro:** `next-frontend/app/register/page.tsx`

**Estrutura:**

-   Esta é uma Rota do App Router por defeito
-   O formulário TEM de ser um Componente de Cliente
-   Crie ficheiro separado `register-form.tsx` com `"use client";` no topo
-   Importe-o na `page.tsx`

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

-   `Form` - wrapper do formulário
-   `FormField` - campo individual (integra com React Hook Form)
-   `FormControl` - controlo do input
-   `FormMessage` - mensagens de erro
-   `Input` - campos de texto
-   `Button` - botão de submissão

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

## <<<<<<< HEAD

### Exemplo de Código Completo: Registo de Utilizador (Frontend)

#### Schema Zod - Validação

```typescript
// next-frontend/lib/validations/auth.ts
import { z } from "zod";

export const registerSchema = z
    .object({
        name: z
            .string()
            .min(2, "Nome deve ter pelo menos 2 caracteres")
            .max(100, "Nome muito longo"),
        email: z.string().email("Email inválido").toLowerCase(),
        password: z
            .string()
            .min(8, "Password deve ter pelo menos 8 caracteres")
            .regex(
                /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/,
                "Password deve conter maiúscula, minúscula, número e símbolo"
            ),
        confirmPassword: z.string(),
    })
    .refine((data) => data.password === data.confirmPassword, {
        message: "As passwords não coincidem",
        path: ["confirmPassword"],
    });

export type RegisterInput = z.infer<typeof registerSchema>;
```

#### API Client

```typescript
// next-frontend/lib/api/client.ts
import axios from "axios";

export const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
    withCredentials: true, // CRÍTICO para cookies httpOnly
    headers: {
        "Content-Type": "application/json",
    },
});

// Interceptor para tratamento de erros
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Redirecionar para login
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);
```

#### API Service - Auth

```typescript
// next-frontend/lib/api/auth.ts
import { apiClient } from "./client";
import { RegisterInput } from "../validations/auth";

export const authApi = {
    register: async (data: RegisterInput) => {
        const response = await apiClient.post("/auth/register", {
            name: data.name,
            email: data.email,
            password: data.password,
        });
        return response.data;
    },

    verifyEmail: async (token: string) => {
        const response = await apiClient.post(`/auth/verify-email/${token}`);
        return response.data;
    },
};
```

#### Componente - RegisterForm

```typescript
// next-frontend/components/auth/register-form.tsx
"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { registerSchema, RegisterInput } from "@/lib/validations/auth";
import { authApi } from "@/lib/api/auth";
import { useToast } from "@/hooks/use-toast";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

export function RegisterForm() {
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();
    const { toast } = useToast();

    const form = useForm<RegisterInput>({
        resolver: zodResolver(registerSchema),
        defaultValues: {
            name: "",
            email: "",
            password: "",
            confirmPassword: "",
        },
    });

    const onSubmit = async (data: RegisterInput) => {
        setIsLoading(true);

        try {
            const response = await authApi.register(data);

            toast({
                title: "Registo bem-sucedido!",
                description:
                    response.message ||
                    "Verifique o seu email para ativar a conta.",
            });

            // Redirecionar para página de confirmação
            router.push("/register/check-email");
        } catch (error: any) {
            const errorMessage =
                error.response?.data?.message ||
                "Erro ao registar. Tente novamente.";

            toast({
                title: "Erro no registo",
                description: Array.isArray(errorMessage)
                    ? errorMessage.join(", ")
                    : errorMessage,
                variant: "destructive",
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card className="w-full max-w-md mx-auto">
            <CardHeader>
                <CardTitle>Criar Conta</CardTitle>
                <CardDescription>
                    Preencha os dados para se registar
                </CardDescription>
            </CardHeader>
            <CardContent>
                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="space-y-4"
                    >
                        <FormField
                            control={form.control}
                            name="name"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Nome</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="João Silva"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="email"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Email</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="email"
                                            placeholder="joao@exemplo.com"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="password"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Password</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="password"
                                            placeholder="********"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="confirmPassword"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Confirmar Password</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="password"
                                            placeholder="********"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <Button
                            type="submit"
                            className="w-full"
                            disabled={isLoading}
                        >
                            {isLoading ? "A registar..." : "Registar"}
                        </Button>
                    </form>
                </Form>
            </CardContent>
        </Card>
    );
}
```

#### Página - Register

```typescript
// next-frontend/app/register/page.tsx
import { RegisterForm } from "@/components/auth/register-form";
import Link from "next/link";

export default function RegisterPage() {
    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="w-full max-w-md space-y-4">
                <RegisterForm />

                <p className="text-center text-sm text-muted-foreground">
                    Já tem conta?{" "}
                    <Link
                        href="/login"
                        className="text-primary hover:underline"
                    >
                        Fazer login
                    </Link>
                </p>
            </div>
        </div>
    );
}
```

---

=======

> > > > > > > origin/main

#### 3.7. Testar o Fluxo Completo

**Testes Manuais:**

1. Navegue para `http://localhost:3000/register`
2. Teste validações:

-   Submeta formulário vazio → deve mostrar erros
-   Email inválido → erro de formato
-   Password fraca → erro de requisitos

3. Registo válido:

-   Preencha todos os campos corretamente
-   Submeta → mensagem de sucesso
-   Verifique PostgreSQL: user criado com `isActive: false`
-   Console backend: token de verificação

4. Verificação:

-   Copie URL de verificação do console
-   Abra no browser
-   Verifique BD: `isActive: true`

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

<<<<<<< HEAD

### Exemplo de Código Completo: Login de Utilizador (Backend)

#### Strategies - LocalStrategy

```typescript
// nest-backend/src/auth/strategies/local.strategy.ts
import { Strategy } from "passport-local";
import { PassportStrategy } from "@nestjs/passport";
import { Injectable, UnauthorizedException, Inject } from "@nestjs/common";
import { AuthService } from "../auth.service";
import { WINSTON_MODULE_NEST_PROVIDER } from "nest-winston";
import { Logger } from "winston";

@Injectable()
export class LocalStrategy extends PassportStrategy(Strategy) {
    constructor(
        private authService: AuthService,
        @Inject(WINSTON_MODULE_NEST_PROVIDER) private readonly logger: Logger
    ) {
        super({
            usernameField: "email", // Usar email em vez de username
        });
    }

    async validate(email: string, password: string): Promise<any> {
        this.logger.info(`Tentativa de login: ${email}`, {
            context: "LocalStrategy",
        });

        const user = await this.authService.validateUser(email, password);

        if (!user) {
            this.logger.warn(`Login falhado: ${email}`, {
                context: "LocalStrategy",
            });
            throw new UnauthorizedException("Credenciais inválidas");
        }

        if (!user.isActive) {
            this.logger.warn(`Login bloqueado (conta não ativa): ${email}`, {
                context: "LocalStrategy",
            });
            throw new UnauthorizedException(
                "Conta não verificada. Verifique o seu email."
            );
        }

        this.logger.info(`Login bem-sucedido: ${email}`, {
            context: "LocalStrategy",
        });
        return user;
    }
}
```

#### Strategies - JwtStrategy

```typescript
// nest-backend/src/auth/strategies/jwt.strategy.ts
import { ExtractJwt, Strategy } from "passport-jwt";
import { PassportStrategy } from "@nestjs/passport";
import { Injectable } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { PrismaService } from "../../prisma/prisma.service";
import { Request } from "express";

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
    constructor(
        private configService: ConfigService,
        private prisma: PrismaService
    ) {
        super({
            jwtFromRequest: ExtractJwt.fromExtractors([
                (request: Request) => {
                    // Extrair JWT do cookie httpOnly
                    return request?.cookies?.access_token;
                },
            ]),
            ignoreExpiration: false,
            secretOrKey: configService.get<string>("JWT_SECRET"),
        });
    }

    async validate(payload: any) {
        // Validar que o utilizador ainda existe
        const user = await this.prisma.user.findUnique({
            where: { id: payload.sub },
            select: {
                id: true,
                email: true,
                name: true,
                role: true,
                isActive: true,
            },
        });

        if (!user || !user.isActive) {
            return null;
        }

        return user;
    }
}
```

#### Service - AuthService (Login & Validate)

```typescript
// nest-backend/src/auth/auth.service.ts (adicionar métodos)
import { JwtService } from "@nestjs/jwt";

@Injectable()
export class AuthService {
    constructor(
        private prisma: PrismaService,
        @Inject(WINSTON_MODULE_NEST_PROVIDER) private readonly logger: Logger,
        private mailerService: MailerService,
        private configService: ConfigService,
        private jwtService: JwtService // Adicionar
    ) {}

    // ... métodos de registo anteriores ...

    async validateUser(email: string, password: string): Promise<any> {
        const user = await this.prisma.user.findUnique({
            where: { email },
        });

        if (!user) {
            return null;
        }

        const isPasswordValid = await bcrypt.compare(password, user.password);

        if (!isPasswordValid) {
            return null;
        }

        // Remover password do objeto retornado
        const { password: _, ...result } = user;
        return result;
    }

    async login(user: any) {
        const payload = {
            email: user.email,
            sub: user.id,
            role: user.role,
        };

        const accessToken = this.jwtService.sign(payload, {
            expiresIn: this.configService.get("JWT_EXPIRES_IN") || "15m",
        });

        const refreshToken = this.jwtService.sign(payload, {
            expiresIn: this.configService.get("JWT_REFRESH_EXPIRES_IN") || "7d",
        });

        // Guardar refresh token na BD
        await this.prisma.session.create({
            data: {
                userId: user.id,
                refreshToken,
                expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 dias
            },
        });

        this.logger.info(`Tokens gerados para utilizador: ${user.email}`, {
            context: "AuthService",
        });

        return {
            accessToken,
            refreshToken,
            user: {
                id: user.id,
                email: user.email,
                name: user.name,
                role: user.role,
            },
        };
    }

    async logout(userId: string, refreshToken: string) {
        // Apagar sessão da BD
        await this.prisma.session.deleteMany({
            where: {
                userId,
                refreshToken,
            },
        });

        this.logger.info(`Logout realizado para utilizador: ${userId}`, {
            context: "AuthService",
        });
    }
}
```

#### DTO - LoginDto

```typescript
// nest-backend/src/auth/dto/login.dto.ts
import { ApiProperty } from "@nestjs/swagger";
import { IsEmail, IsString, MinLength } from "class-validator";

export class LoginDto {
    @ApiProperty({ example: "admin@orionone.com" })
    @IsEmail({}, { message: "Email inválido" })
    email: string;

    @ApiProperty({ example: "Admin123!" })
    @IsString()
    @MinLength(8, { message: "Password deve ter pelo menos 8 caracteres" })
    password: string;
}
```

#### Controller - AuthController (Login & Logout)

```typescript
// nest-backend/src/auth/auth.controller.ts (adicionar métodos)
import {
    Controller,
    Post,
    Body,
    Param,
    UseGuards,
    Req,
    Res,
    HttpCode,
    HttpStatus,
} from "@nestjs/common";
import { AuthGuard } from "@nestjs/passport";
import {
    ApiTags,
    ApiOperation,
    ApiResponse,
    ApiBearerAuth,
} from "@nestjs/swagger";
import { Throttle } from "@nestjs/throttler";
import { Response, Request } from "express";

@ApiTags("auth")
@Controller("auth")
export class AuthController {
    // ... métodos de registo anteriores ...

    @Post("login")
    @HttpCode(HttpStatus.OK)
    @UseGuards(AuthGuard("local"))
    @Throttle({ default: { limit: 5, ttl: 60000 } }) // 5 tentativas por minuto
    @ApiOperation({ summary: "Login de utilizador" })
    @ApiResponse({ status: 200, description: "Login bem-sucedido" })
    @ApiResponse({ status: 401, description: "Credenciais inválidas" })
    @ApiResponse({ status: 429, description: "Demasiadas tentativas" })
    async login(
        @Req() req: Request,
        @Res({ passthrough: true }) res: Response,
        @Body() _loginDto: LoginDto // Para documentação Swagger
    ) {
        const result = await this.authService.login(req.user);

        // Definir cookies httpOnly
        res.cookie("access_token", result.accessToken, {
            httpOnly: true,
            secure: process.env.NODE_ENV === "production",
            sameSite: "lax",
            maxAge: 15 * 60 * 1000, // 15 minutos
        });

        res.cookie("refresh_token", result.refreshToken, {
            httpOnly: true,
            secure: process.env.NODE_ENV === "production",
            sameSite: "lax",
            maxAge: 7 * 24 * 60 * 60 * 1000, // 7 dias
        });

        return result;
    }

    @Get("me")
    @UseGuards(AuthGuard("jwt"))
    @ApiBearerAuth()
    @ApiOperation({ summary: "Obter dados do utilizador autenticado" })
    @ApiResponse({ status: 200, description: "Dados do utilizador" })
    @ApiResponse({ status: 401, description: "Não autenticado" })
    async getMe(@Req() req: Request) {
        return req.user;
    }

    @Post("logout")
    @HttpCode(HttpStatus.OK)
    @UseGuards(AuthGuard("jwt"))
    @ApiBearerAuth()
    @ApiOperation({ summary: "Logout de utilizador" })
    @ApiResponse({ status: 200, description: "Logout bem-sucedido" })
    async logout(
        @Req() req: Request,
        @Res({ passthrough: true }) res: Response
    ) {
        const user = req.user as any;
        const refreshToken = req.cookies?.refresh_token;

        await this.authService.logout(user.id, refreshToken);

        // Limpar cookies
        res.clearCookie("access_token");
        res.clearCookie("refresh_token");

        return { message: "Logout bem-sucedido" };
    }
}
```

#### Module - AuthModule

```typescript
// nest-backend/src/auth/auth.module.ts
import { Module } from "@nestjs/common";
import { JwtModule } from "@nestjs/jwt";
import { PassportModule } from "@nestjs/passport";
import { ConfigModule, ConfigService } from "@nestjs/config";
import { AuthController } from "./auth.controller";
import { AuthService } from "./auth.service";
import { LocalStrategy } from "./strategies/local.strategy";
import { JwtStrategy } from "./strategies/jwt.strategy";
import { PrismaModule } from "../prisma/prisma.module";

@Module({
    imports: [
        PrismaModule,
        PassportModule,
        JwtModule.registerAsync({
            imports: [ConfigModule],
            useFactory: async (configService: ConfigService) => ({
                secret: configService.get<string>("JWT_SECRET"),
                signOptions: {
                    expiresIn:
                        configService.get<string>("JWT_EXPIRES_IN") || "15m",
                },
            }),
            inject: [ConfigService],
        }),
    ],
    controllers: [AuthController],
    providers: [AuthService, LocalStrategy, JwtStrategy],
    exports: [AuthService],
})
export class AuthModule {}
```

---

### Fase 3: Frontend (Next.js)

=======

### Fase 1: Base de Dados (Prisma)

> > > > > > > origin/main

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

#### 2.2. Implementar a LocalStrategy com Rate Limiting

**Ficheiro:** `nest-backend/src/auth/strategies/local.strategy.ts`

**Implementação:**

<<<<<<< HEAD

1. Injete o `AuthService`.
2. Implemente a função `validate()`.
3. Recebe `email` e `password`.
4. Procura o utilizador e usa `bcrypt.compare()` para verificar a password.
5. Se a password for válida, retorna o objeto `user`.
6. # Adicione logging com Winston para registar tentativas de login (sucesso e falha).
7. Injete o `AuthService`.
8. Implemente a função `validate()`.
9. Recebe `email` e `password`.
10. Procura o utilizador e usa `bcrypt.compare()` para verificar a password.
11. Se a password for válida, retorna o objeto `user`.
12. Adicione logging com Winston para registar tentativas de login (sucesso e falha).
    > > > > > > > origin/main

**Proteção Adicional (Rate Limiting):**
No `auth.controller.ts`, aplique o decorador `@Throttle({ default: { limit: 3, ttl: 60000 } })` ao endpoint de login para prevenir ataques de força bruta, limitando a 3 tentativas por minuto.

**Documentação:**
<<<<<<< HEAD
[Guia Oficial do Nest.js sobre Autenticação](https://docs.nestjs.com/security/authentication)
=======
[Guia Oficial do Nest.js sobre LocalStrategy](https://docs.nestjs.com/security/authentication#implementing-localstrategy)

> > > > > > > origin/main
> > > > > > > [Guia Oficial do Nest.js sobre Rate Limiting](https://docs.nestjs.com/security/rate-limiting)

#### 2.3. Implementar a JwtStrategy com Segurança

**Ficheiro:** `nest-backend/src/auth/strategies/jwt.strategy.ts`

**Responsabilidade:**
Ler e validar o JWT em TODOS os pedidos futuros, garantindo que apenas utilizadores autenticados acedem a rotas protegidas.

**Fluxo:**

<<<<<<< HEAD

1. Extrai o token do cookie `httpOnly`.
2. Usa o `JWT_SECRET` do `.env` (através do `ConfigService`) para validar a assinatura e a expiração do token.
3. # Anexa o payload do token (`userId`, `role`) ao objeto `request.user`, tornando-o disponível em todos os controllers.
4. Extrai o token do cookie `httpOnly`.
5. Usa o `JWT_SECRET` do `.env` (através do `ConfigService`) para validar a assinatura e a expiração do token.
6. Anexa o payload do token (`userId`, `role`) ao objeto `request.user`, tornando-o disponível em todos os controllers.
    > > > > > > > origin/main

**Segurança Adicional (Helmet):**
O Helmet, já configurado globalmente em `main.ts`, adiciona uma camada de segurança essencial ao proteger os cabeçalhos HTTP, prevenindo ataques comuns como XSS e clickjacking.

**Documentação:**
<<<<<<< HEAD
[Guia Oficial do Nest.js sobre JWT Strategy](https://docs.nestjs.com/security/authentication)
=======
[Guia Oficial do Nest.js sobre JwtStrategy](https://docs.nestjs.com/security/authentication#implementing-jwt)

> > > > > > > origin/main
> > > > > > > [Guia Oficial do Nest.js sobre Helmet](https://docs.nestjs.com/security/helmet)

#### 2.4. Atualizar o AuthService (Login)

**Função:** `login(user: any)`

**Quando é Chamada:**
Depois da `LocalStrategy` ser bem-sucedida.

**Responsabilidade:**

1. Recebe objeto `user`
2. Gera tokens JWT:

-   `accessToken` - 15 minutos
-   `refreshToken` - 7-30 dias

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

-   Body: `{ "email": "admin@orionone.com", "password": "Admin123!" }`
-   Verificar: cookies `access_token` e `refresh_token` definidos
-   Status: 200

2. **GET** `/auth/me`

-   Usar cookies do passo anterior
-   Verificar: dados do utilizador retornados
-   Status: 200

3. **GET** `/auth/me` (sem cookies)

-   Não enviar cookies
-   Verificar: erro de autenticação
-   Status: 401

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

-   "use client"
-   Schema Zod
-   React Hook Form
-   shadcn/ui
-   Função `onSubmit` que faz `POST` para `/api/auth/login`

#### 3.2. Configurar o Cliente Axios (CRÍTICO)

**Ficheiro:** `lib/api/client.ts`

**Configuração Obrigatória:**

```javascript
withCredentials: true;
```

**Importante:**
Sem isto, o browser NUNCA irá enviar os cookies `httpOnly` para o backend Nest.js, e a autenticação irá falhar silenciosamente.

**Documentação:**
<<<<<<< HEAD
[Guia Oficial do Axios sobre Configuração de Request](https://axios-http.com/docs/req_config)
=======
[Guia Oficial do Axios sobre withCredentials](https://axios-http.com/docs/config_defaults)

> > > > > > > origin/main

#### 3.3. Criar o AuthContext

**Ficheiro:** `context/auth-context.tsx`

**Objetivo:**
Gerir estado global da autenticação.

**Estados:**

-   `user` - objeto com dados do utilizador
-   `isAuthenticated` - boolean
-   `isLoading` - boolean

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

-   Se `isLoading` → mostra spinner
-   Se `!isAuthenticated` e `!isLoading` → redireciona para `/login`
-   Se `isAuthenticated` → renderiza `children`

**Alternativa:**
Use Middleware do Next.js para verificação no servidor.

**Documentação:**
[Guia Oficial do Next.js sobre Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware)

## <<<<<<< HEAD

### Exemplo de Código Completo: Login de Utilizador (Frontend)

#### Schema Zod - Login Validation

```typescript
// next-frontend/lib/validations/auth.ts (adicionar)
export const loginSchema = z.object({
    email: z.string().email("Email inválido").toLowerCase(),
    password: z.string().min(8, "Password deve ter pelo menos 8 caracteres"),
});

export type LoginInput = z.infer<typeof loginSchema>;
```

#### API Service - Auth (adicionar métodos)

```typescript
// next-frontend/lib/api/auth.ts (adicionar)
export const authApi = {
    // ... register e verifyEmail anteriores ...

    login: async (data: LoginInput) => {
        const response = await apiClient.post("/auth/login", data);
        return response.data;
    },

    logout: async () => {
        const response = await apiClient.post("/auth/logout");
        return response.data;
    },

    me: async () => {
        const response = await apiClient.get("/auth/me");
        return response.data;
    },
};
```

#### Context - AuthContext

```typescript
// next-frontend/contexts/auth-context.tsx
"use client";

import {
    createContext,
    useContext,
    useEffect,
    useState,
    ReactNode,
} from "react";
import { authApi } from "@/lib/api/auth";
import { useRouter } from "next/navigation";

interface User {
    id: string;
    email: string;
    name: string;
    role: "ADMIN" | "AGENT" | "USER";
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    const isAuthenticated = !!user;

    // Verificar autenticação ao carregar
    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const userData = await authApi.me();
            setUser(userData);
        } catch (error) {
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (email: string, password: string) => {
        const response = await authApi.login({ email, password });
        setUser(response.user);
        router.push("/dashboard");
    };

    const logout = async () => {
        try {
            await authApi.logout();
        } finally {
            setUser(null);
            router.push("/login");
        }
    };

    return (
        <AuthContext.Provider
            value={{ user, isAuthenticated, isLoading, login, logout }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth deve ser usado dentro de AuthProvider");
    }
    return context;
}
```

#### Componente - LoginForm

```typescript
// next-frontend/components/auth/login-form.tsx
"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, LoginInput } from "@/lib/validations/auth";
import { useAuth } from "@/contexts/auth-context";
import { useToast } from "@/hooks/use-toast";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

export function LoginForm() {
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();
    const { toast } = useToast();

    const form = useForm<LoginInput>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            email: "",
            password: "",
        },
    });

    const onSubmit = async (data: LoginInput) => {
        setIsLoading(true);

        try {
            await login(data.email, data.password);

            toast({
                title: "Login bem-sucedido!",
                description: "Bem-vindo de volta.",
            });
        } catch (error: any) {
            const errorMessage =
                error.response?.data?.message ||
                "Erro ao fazer login. Tente novamente.";

            toast({
                title: "Erro no login",
                description: errorMessage,
                variant: "destructive",
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card className="w-full max-w-md mx-auto">
            <CardHeader>
                <CardTitle>Login</CardTitle>
                <CardDescription>Entre na sua conta OrionOne</CardDescription>
            </CardHeader>
            <CardContent>
                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="space-y-4"
                    >
                        <FormField
                            control={form.control}
                            name="email"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Email</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="email"
                                            placeholder="joao@exemplo.com"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="password"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Password</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="password"
                                            placeholder="********"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <Button
                            type="submit"
                            className="w-full"
                            disabled={isLoading}
                        >
                            {isLoading ? "A entrar..." : "Entrar"}
                        </Button>
                    </form>
                </Form>
            </CardContent>
        </Card>
    );
}
```

#### Página - Login

```typescript
// next-frontend/app/login/page.tsx
import { LoginForm } from "@/components/auth/login-form";
import Link from "next/link";

export default function LoginPage() {
    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="w-full max-w-md space-y-4">
                <LoginForm />

                <div className="space-y-2 text-center text-sm">
                    <p className="text-muted-foreground">
                        Não tem conta?{" "}
                        <Link
                            href="/register"
                            className="text-primary hover:underline"
                        >
                            Registar
                        </Link>
                    </p>

                    <p className="text-muted-foreground">
                        <Link
                            href="/forgot-password"
                            className="text-primary hover:underline"
                        >
                            Esqueceu a password?
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
```

#### Layout - Root com AuthProvider

```typescript
// next-frontend/app/layout.tsx
import { AuthProvider } from "@/contexts/auth-context";
import { Toaster } from "@/components/ui/toaster";

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="pt">
            <body>
                <AuthProvider>
                    {children}
                    <Toaster />
                </AuthProvider>
            </body>
        </html>
    );
}
```

#### Componente - RequireAuth (Rotas Protegidas)

```typescript
// next-frontend/components/auth/require-auth.tsx
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";

export function RequireAuth({ children }: { children: React.ReactNode }) {
    const { isAuthenticated, isLoading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isLoading && !isAuthenticated) {
            router.push("/login");
        }
    }, [isAuthenticated, isLoading, router]);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
            </div>
        );
    }

    if (!isAuthenticated) {
        return null;
    }

    return <>{children}</>;
}
```

#### Exemplo de Página Protegida

```typescript
// next-frontend/app/dashboard/page.tsx
"use client";

import { RequireAuth } from "@/components/auth/require-auth";
import { useAuth } from "@/contexts/auth-context";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
    const { user, logout } = useAuth();

    return (
        <RequireAuth>
            <div className="container mx-auto p-8">
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold">Dashboard</h1>
                        <p className="text-muted-foreground">
                            Bem-vindo, {user?.name}! ({user?.role})
                        </p>
                    </div>

                    <Button onClick={logout} variant="outline">
                        Logout
                    </Button>
                </div>

                <div className="grid gap-4 md:grid-cols-3">
                    {/* Dashboard content aqui */}
                </div>
            </div>
        </RequireAuth>
    );
}
```

---

=======

> > > > > > > origin/main

#### 3.6. Validar Autenticação

**Fluxo de Teste Manual:**

1. **Login bem-sucedido:**

-   Aceda a `/login`
-   Use credenciais do seed (admin@orionone.com / Admin123!)
-   Verifique redirecionamento para dashboard
-   Console: cookies definidos

2. **AuthContext funcionando:**

-   Após login, verifique `user` no React DevTools
-   `isAuthenticated` deve ser `true`
-   `isLoading` deve ser `false`

3. **Rotas protegidas:**

-   Tente aceder `/dashboard` sem login
-   Deve redirecionar para `/login`
-   Após login, `/dashboard` deve ser acessível

4. **Logout:**

-   Clique botão logout
-   Cookies devem ser limpos (ver DevTools > Application > Cookies)
-   Deve redirecionar para `/login`
-   Tentar aceder `/dashboard` → redireciona novamente

5. **Token expirado:**

-   Login
-   Espere 16+ minutos (accessToken expira)
-   Tente aceder recurso protegido
-   Deve redirecionar para login (ou renovar com refresh token)

---

## Funcionalidades 1.3, 1.4, 1.5: Tarefas Restantes do Sprint 1

Siga o mesmo padrão vertical para as restantes funcionalidades do sprint.

---

### US1.3: Reset de Password

**Backend:**

Endpoints:

-   `POST /api/auth/forgot-password` - gera token
-   `POST /api/auth/reset-password/:token` - valida e altera password

Fluxo idêntico à verificação de email, mas usa tipo `PASSWORD_RESET` no `VerificationToken`.

**Frontend:**

Páginas:

-   `app/forgot-password/page.tsx` - formulário para pedir reset
-   `app/reset-password/[token]/page.tsx` - formulário para nova password

---

### US1.4: Gestão de Perfil

**Backend:**

Endpoints protegidos por JWT:

-   `PATCH /api/users/me` - atualiza nome/timezone
-   `PATCH /api/users/me/password` - altera password

Importante: Endpoint de mudança de password deve verificar `oldPassword` com `bcrypt.compare()`

**Frontend:**

Página:

-   `app/profile/page.tsx` - interface com Tabs (shadcn/ui)
-   Separar "Perfil" de "Segurança"

---

### US1.5: Controlo de Acesso Baseado em Roles (RBAC) com CASL

**Backend:**

**Implementação com CASL:**
A biblioteca CASL, já configurada no Sprint 0, oferece uma forma mais poderosa e flexível de gerir permissões do que um simples `RolesGuard`.

<<<<<<< HEAD

1. **Definir Habilidades:** No `casl-ability.factory.ts`, defina o que cada role (`ADMIN`, `AGENT`, `USER`) pode fazer (`Action`) em cada recurso (`Subject`).
2. **Criar um `PoliciesGuard`:** Este guarda irá verificar as permissões do utilizador contra a ação necessária para um determinado endpoint.
3. # **Proteger Endpoints:** Use o `PoliciesGuard` em conjunto com um decorador `@CheckPolicies` para proteger rotas específicas, verificando se o utilizador tem a permissão necessária para a ação.
4. **Definir Habilidades:** No `casl-ability.factory.ts`, defina o que cada role (`ADMIN`, `AGENT`, `USER`) pode fazer (`Action`) em cada recurso (`Subject`).
5. **Criar um `PoliciesGuard`:** Este guarda irá verificar as permissões do utilizador contra a ação necessária para um determinado endpoint.
6. **Proteger Endpoints:** Use o `PoliciesGuard` em conjunto com um decorador `@CheckPolicies` para proteger rotas específicas, verificando se o utilizador tem a permissão necessária para a ação.
    > > > > > > > origin/main

**Documentação:**
[Guia Oficial do CASL com Nest.js](https://casl.js.org/v6/en/package/casl-nestjs)

**Frontend:**

**Implementação:**

<<<<<<< HEAD

1. Exponha o `user.role` no `AuthContext`.
2. Crie um hook `usePermissions` que utilize a biblioteca `@casl/ability` no frontend para verificar permissões de forma reativa e centralizada.
3. # Renderize componentes da UI (como botões de edição ou links de administração) condicionalmente, com base nas permissões do utilizador atual.
4. Exponha o `user.role` no `AuthContext`.
5. Crie um hook `usePermissions` que utilize a biblioteca `@casl/ability` no frontend para verificar permissões de forma reativa e centralizada.
6. Renderize componentes da UI (como botões de edição ou links de administração) condicionalmente, com base nas permissões do utilizador atual.
    > > > > > > > origin/main

**Documentação:**
[Guia Oficial do CASL com React](https://casl.js.org/v6/en/package/casl-react)

---

<<<<<<< HEAD

### Exemplo de Código Completo: RBAC com CASL

#### Backend - CASL Ability Factory

```typescript
// nest-backend/src/casl/casl-ability.factory.ts
import { Injectable } from "@nestjs/common";
import {
    Ability,
    AbilityBuilder,
    AbilityClass,
    ExtractSubjectType,
    InferSubjects,
} from "@casl/ability";

export enum Action {
    Manage = "manage",
    Create = "create",
    Read = "read",
    Update = "update",
    Delete = "delete",
}

export type Subjects =
    | "Incident"
    | "User"
    | "KnowledgeBase"
    | "Comment"
    | "Attachment"
    | "all";

export type AppAbility = Ability<[Action, Subjects]>;

@Injectable()
export class CaslAbilityFactory {
    createForUser(user: any) {
        const { can, cannot, build } = new AbilityBuilder<AppAbility>(
            Ability as AbilityClass<AppAbility>
        );

        if (user.role === "ADMIN") {
            can(Action.Manage, "all");
        } else if (user.role === "AGENT") {
            can(Action.Manage, "Incident");
            can([Action.Create, Action.Read, Action.Update], "KnowledgeBase");
            can(Action.Manage, "Comment");
            can(Action.Manage, "Attachment");
            can(Action.Read, "User");
            can(Action.Update, "User", { id: user.id });
        } else if (user.role === "USER") {
            can(Action.Create, "Incident");
            can([Action.Read, Action.Update], "Incident", {
                createdById: user.id,
            });
            can(Action.Read, "KnowledgeBase", { status: "PUBLISHED" });
            can(Action.Create, "Comment", {
                incident: { createdById: user.id },
            });
            can(Action.Read, "User", { id: user.id });
            can(Action.Update, "User", { id: user.id });
        }

        return build({
            detectSubjectType: (item) =>
                item.constructor as ExtractSubjectType<Subjects>,
        });
    }
}
```

#### Frontend - CASL Hook e Componentes

```typescript
// next-frontend/lib/casl/ability.ts
import { Ability, AbilityBuilder, AbilityClass } from "@casl/ability";

export enum Action {
    Manage = "manage",
    Create = "create",
    Read = "read",
    Update = "update",
    Delete = "delete",
}

export type Subjects =
    | "Incident"
    | "User"
    | "KnowledgeBase"
    | "Comment"
    | "Attachment"
    | "all";
export type AppAbility = Ability<[Action, Subjects]>;

export function defineAbilityFor(user: any): AppAbility {
    const { can, build } = new AbilityBuilder<AppAbility>(
        Ability as AbilityClass<AppAbility>
    );

    if (user.role === "ADMIN") {
        can(Action.Manage, "all");
    } else if (user.role === "AGENT") {
        can(Action.Manage, "Incident");
        can([Action.Create, Action.Read, Action.Update], "KnowledgeBase");
    } else if (user.role === "USER") {
        can(Action.Create, "Incident");
        can(Action.Read, "Incident");
    }

    return build();
}
```

```typescript
// next-frontend/hooks/use-permissions.ts
"use client";

import { useMemo } from "react";
import { useAuth } from "@/contexts/auth-context";
import { defineAbilityFor, Action, Subjects } from "@/lib/casl/ability";

export function usePermissions() {
    const { user } = useAuth();

    const ability = useMemo(() => {
        if (!user) return null;
        return defineAbilityFor(user);
    }, [user]);

    const can = (action: Action, subject: Subjects) => {
        return ability?.can(action, subject) ?? false;
    };

    return { can, ability };
}
```

```typescript
// next-frontend/components/auth/can.tsx
"use client";

import { ReactNode } from "react";
import { usePermissions } from "@/hooks/use-permissions";
import { Action, Subjects } from "@/lib/casl/ability";

interface CanProps {
    do: Action;
    on: Subjects;
    children: ReactNode;
    fallback?: ReactNode;
}

export function Can({
    do: action,
    on: subject,
    children,
    fallback = null,
}: CanProps) {
    const { can } = usePermissions();
    return can(action, subject) ? <>{children}</> : <>{fallback}</>;
}
```

---

=======

> > > > > > > origin/main

## Referência Rápida: Testes

> **Nota:** Testes práticos estão integrados em cada fase:
>
> -   **US1.1 Backend:** Fase 2.7 (Unit tests)
> -   **US1.1 Frontend:** Fase 3.7 (Validação manual + E2E)
> -   **US1.2 Backend:** Fase 2.8 (Testes de endpoints)
> -   **US1.2 Frontend:** Fase 3.6 (Validação de autenticação)

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

-   **Backend Services:** > 80%
-   **Backend Controllers:** > 70%
-   **Frontend Components:** > 70%
-   **E2E Critical Flows:** 100% (Login, Registo)

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
MAIL_HOST="smtp.example.com"
MAIL_PORT=587
MAIL_USER="your-email@example.com"
MAIL_PASSWORD="your-app-password"
MAIL_FROM="noreply@orionone.com"

# App
NODE_ENV="development"
PORT=8000
FRONTEND_URL="http://localhost:3000"

# CORS
CORS_ORIGIN="http://localhost:3000"
```

**Importante:**

-   NUNCA commitar `.env` para Git
-   Usar `.env.example` como template
-   Em produção, usar Azure Key Vault ou similar

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
