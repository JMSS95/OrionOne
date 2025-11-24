# Guia de Implementação Detalhado do Sprint 3: Comentários & Anexos

## Visão Geral do Sprint

**Objetivo:**
Permitir a colaboração em incidentes através de um sistema de comentários e a capacidade de anexar ficheiros para fornecer contexto adicional.

**User Stories:**

-   [Em Curso] US3.1: Adicionar e Visualizar Comentários num Incidente
-   [Em Curso] US3.2: Anexar e Listar Ficheiros num Incidente

**Pré-requisitos:**

-   Sprint 1 completo (Autenticação)
-   Sprint 2 completo (CRUD de Incidentes)

---

## Aplicando as Tecnologias Fundamentais (Sprints 0, 1, 2)

Neste sprint, introduzimos a gestão de comentários e anexos. Vamos aplicar as tecnologias já estabelecidas para garantir consistência, segurança e manutenibilidade.

### 1. Upload de Ficheiros com Multer

**Objetivo:** Gerir o upload de ficheiros (`multipart/form-data`).

**Ações:**

-   **Instalação:** Adicione os type definitions para o Multer: `npm install -D @types/multer` no `nest-backend`.
-   **Configuração:** No `attachments.module.ts`, configure o `MulterModule` com as opções de armazenamento (local ou S3), limites de tamanho de ficheiro (`fileSize`) e número de ficheiros.
-   **Validação:** Crie um `FileValidator` customizado ou use os validadores integrados (`MaxFileSizeValidator`, `FileTypeValidator`) para garantir que apenas ficheiros permitidos (ex: jpg, png, pdf, zip) com tamanho máximo de 10MB são aceites.

**Documentação:**
[Guia Oficial do Nest.js sobre File Upload](https://docs.nestjs.com/techniques/file-upload)

### 2. Documentação de API com Swagger

**Objetivo:** Documentar os novos endpoints de comentários e, crucialmente, o endpoint de upload de anexos.

**Ações:**

-   **Comentários:** Use `@ApiTags('comments')` e documente o CRUD como nos sprints anteriores.
-   **Anexos:** Para o endpoint de upload, é essencial usar `@ApiConsumes('multipart/form-data')` e `@ApiBody` para descrever corretamente no Swagger que o endpoint espera ficheiros.

**Documentação:**
[Documentando File Upload no Swagger (Nest.js)](https://docs.nestjs.com/openapi/types-and-parameters#file-upload)

### 3. Logging com Winston

**Objetivo:** Registar todas as operações de ficheiros e comentários.

**Ações:**

-   **Comentários:** No `comments.service.ts`, registe a criação de cada comentário, incluindo o ID do incidente e o autor.
-   **Anexos:** No `attachments.service.ts`, registe cada upload e delete de ficheiros, incluindo o nome do ficheiro, tamanho, e o utilizador que realizou a ação. Isto é vital para auditoria.

**Documentação:**
[Guia Oficial do `nest-winston`](https://github.com/gremo/nest-winston)

### 4. Autorização com CASL

**Objetivo:** Controlar quem pode comentar e gerir anexos.

**Ações:**

-   **Definir Habilidades:** No `casl-ability.factory.ts`, adicione os `subjects` 'Comment' e 'Attachment'.
-   `AGENT` e `USER` podem criar comentários e anexos nos incidentes a que têm acesso.
-   `ADMIN` pode gerir (`manage`) todos os comentários e anexos.
-   Defina quem pode apagar anexos (ex: o autor do anexo ou um admin).
-   **Verificar Permissões:** Antes de qualquer operação de criação ou eliminação, verifique as permissões com a `CaslAbilityFactory`.

**Documentação:**
[Guia Oficial do CASL](https://casl.js.org/v6/en/guide/intro)
[Integração do CASL com Nest.js](https://casl.js.org/v6/en/package/casl-nestjs)

### 5. Reutilização do Tiptap

**Objetivo:** Usar o mesmo editor de Rich Text dos incidentes para os comentários.

**Ações:**

-   **Frontend:** Reutilize o componente Tiptap criado no Sprint 2 no formulário de criação de comentários.
-   **Backend:** O `content` do comentário no `CreateCommentDto` deve ser do tipo `object` para receber a estrutura JSON do Tiptap, tal como foi feito para a descrição do incidente.

### 6. Validação e Compressão

-   **Validação:** Além da validação de ficheiros, continue a usar `class-validator` nos DTOs de comentários para garantir que o conteúdo não está vazio.
-   **Compressão:** A compressão global continua a ser benéfica, especialmente ao carregar listas de comentários que podem conter texto extenso.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação](https://docs.nestjs.com/techniques/validation)

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

-   **Campos Essenciais:**
-   `id`: Identificador único.
-   `content`: Do tipo `String`, para armazenar o texto do comentário.
-   `createdAt`, `updatedAt`: Timestamps automáticos.
-   **Relações:**
-   Crie uma relação `author` com o modelo `User` (muitos-para-um).
-   Crie uma relação `incident` com o modelo `Incident` (muitos-para-um).

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

-   `@IsString()` e `@IsNotEmpty()` para o campo `content`.
-   `@IsString()` e `@IsNotEmpty()` para o campo `incidentId`, que será usado para associar o comentário.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação](https://docs.nestjs.com/techniques/validation)

#### 2.3. Implementar o `CommentsService`

**Ficheiro:** `nest-backend/src/comments/comments.service.ts`

**Ações:**

1. **`create()`**:

-   Recebe o `CreateCommentDto` e o `userId` do utilizador autenticado.
-   Cria um novo registo na tabela `Comment`, associando o `authorId` e o `incidentId`.

2. **`findAllForIncident()`**:

-   Recebe um `incidentId`.
-   Retorna todos os comentários para esse incidente, incluindo os dados do autor (`include: { author: true }`).
-   Ordene os resultados por `createdAt` em ordem ascendente para mostrar os mais antigos primeiro.

**Documentação:**
[Guia Oficial do Prisma sobre Criação de Registos](https://www.prisma.io/docs/orm/prisma-client/queries/crud#create)

#### 2.4. Configurar o `CommentsController`

**Ficheiro:** `nest-backend/src/comments/comments.controller.ts`

**Objetivo:**
Definir as rotas da API para gerir comentários.

**Ações:**

-   **`POST /`**: Rota para criar um novo comentário. Protegida com `@UseGuards(JwtAuthGuard)`.
-   **`GET /incident/:incidentId`**: Rota para listar todos os comentários de um incidente específico. Protegida com `@UseGuards(JwtAuthGuard)`.

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

### Exemplo de Código Completo: Sistema de Comentários (Backend)

#### Schema Prisma - Comment Model

```prisma
// nest-backend/prisma/schema.prisma (adicionar)
model Comment {
 id String @id @default(cuid())
 content Json // Rich text em Tiptap JSON format
 incidentId String
 authorId String
 createdAt DateTime @default(now())
 updatedAt DateTime @updatedAt

 incident Incident @relation(fields: [incidentId], references: [id], onDelete: Cascade)
 author User @relation("AuthoredComments", fields: [authorId], references: [id])

 @@index([incidentId])
 @@index([authorId])
 @@index([createdAt])
}

// Atualizar Incident model
model Incident {
 // ... campos existentes ...
 comments Comment[]
 // ... resto do modelo ...
}

// Atualizar User model
model User {
 // ... campos existentes ...
 comments Comment[] @relation("AuthoredComments")
 // ... resto do modelo ...
}
```

#### DTO - CreateCommentDto

```typescript
// nest-backend/src/comments/dto/create-comment.dto.ts
import { ApiProperty } from "@nestjs/swagger";
import { IsObject, IsString, IsNotEmpty, IsUUID } from "class-validator";

export class CreateCommentDto {
    @ApiProperty({
        description: "Rich text content in Tiptap JSON format",
        example: {
            type: "doc",
            content: [
                {
                    type: "paragraph",
                    content: [{ type: "text", text: "Este é um comentário" }],
                },
            ],
        },
    })
    @IsObject()
    @IsNotEmpty({ message: "Conteúdo não pode estar vazio" })
    content: any; // Tiptap JSON

    @ApiProperty({ example: "cuid-of-incident" })
    @IsUUID()
    @IsNotEmpty()
    incidentId: string;
}
```

#### Service - CommentsService

```typescript
// nest-backend/src/comments/comments.service.ts
import {
    Injectable,
    Inject,
    Logger,
    NotFoundException,
    ForbiddenException,
} from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { WINSTON_MODULE_NEST_PROVIDER } from "nest-winston";
import { CreateCommentDto } from "./dto/create-comment.dto";
import { CaslAbilityFactory, Action } from "../casl/casl-ability.factory";

@Injectable()
export class CommentsService {
    constructor(
        private prisma: PrismaService,
        @Inject(WINSTON_MODULE_NEST_PROVIDER) private readonly logger: Logger,
        private caslAbilityFactory: CaslAbilityFactory
    ) {}

    async create(dto: CreateCommentDto, userId: string) {
        this.logger.info(`Criando comentário no incidente: ${dto.incidentId}`, {
            context: "CommentsService",
            userId,
        });

        // Verificar se o incidente existe
        const incident = await this.prisma.incident.findUnique({
            where: { id: dto.incidentId },
        });

        if (!incident) {
            throw new NotFoundException("Incidente não encontrado");
        }

        const comment = await this.prisma.comment.create({
            data: {
                content: dto.content,
                incidentId: dto.incidentId,
                authorId: userId,
            },
            include: {
                author: {
                    select: {
                        id: true,
                        name: true,
                        email: true,
                        avatar: true,
                    },
                },
            },
        });

        this.logger.info(`Comentário criado: ${comment.id}`, {
            context: "CommentsService",
            commentId: comment.id,
            incidentId: dto.incidentId,
        });

        return comment;
    }

    async findAllForIncident(incidentId: string) {
        this.logger.info(`Listando comentários do incidente: ${incidentId}`, {
            context: "CommentsService",
        });

        return this.prisma.comment.findMany({
            where: { incidentId },
            include: {
                author: {
                    select: {
                        id: true,
                        name: true,
                        email: true,
                        avatar: true,
                    },
                },
            },
            orderBy: {
                createdAt: "asc", // Mais antigos primeiro
            },
        });
    }

    async delete(id: string, user: any) {
        const comment = await this.prisma.comment.findUnique({
            where: { id },
        });

        if (!comment) {
            throw new NotFoundException("Comentário não encontrado");
        }

        // Verificar permissões: apenas autor ou admin pode apagar
        const ability = this.caslAbilityFactory.createForUser(user);

        if (user.role !== "ADMIN" && comment.authorId !== user.id) {
            throw new ForbiddenException(
                "Não tem permissão para apagar este comentário"
            );
        }

        await this.prisma.comment.delete({
            where: { id },
        });

        this.logger.info(`Comentário apagado: ${id}`, {
            context: "CommentsService",
            userId: user.id,
        });

        return { message: "Comentário apagado com sucesso" };
    }
}
```

#### Controller - CommentsController

```typescript
// nest-backend/src/comments/comments.controller.ts
import {
    Controller,
    Get,
    Post,
    Delete,
    Body,
    Param,
    UseGuards,
    Req,
} from "@nestjs/common";
import { AuthGuard } from "@nestjs/passport";
import {
    ApiTags,
    ApiOperation,
    ApiResponse,
    ApiBearerAuth,
} from "@nestjs/swagger";
import { CommentsService } from "./comments.service";
import { CreateCommentDto } from "./dto/create-comment.dto";

@ApiTags("comments")
@Controller("comments")
@UseGuards(AuthGuard("jwt"))
@ApiBearerAuth()
export class CommentsController {
    constructor(private commentsService: CommentsService) {}

    @Post()
    @ApiOperation({ summary: "Criar novo comentário" })
    @ApiResponse({ status: 201, description: "Comentário criado com sucesso" })
    @ApiResponse({ status: 404, description: "Incidente não encontrado" })
    async create(@Body() dto: CreateCommentDto, @Req() req: any) {
        return this.commentsService.create(dto, req.user.id);
    }

    @Get("incident/:incidentId")
    @ApiOperation({ summary: "Listar comentários de um incidente" })
    @ApiResponse({ status: 200, description: "Lista de comentários" })
    async findAllForIncident(@Param("incidentId") incidentId: string) {
        return this.commentsService.findAllForIncident(incidentId);
    }

    @Delete(":id")
    @ApiOperation({ summary: "Apagar comentário" })
    @ApiResponse({ status: 200, description: "Comentário apagado" })
    @ApiResponse({ status: 403, description: "Sem permissão" })
    @ApiResponse({ status: 404, description: "Comentário não encontrado" })
    async delete(@Param("id") id: string, @Req() req: any) {
        return this.commentsService.delete(id, req.user);
    }
}
```

---

### Exemplo de Código Completo: Sistema de Comentários (Frontend)

#### API Service - Comments

```typescript
// next-frontend/lib/api/comments.ts
import { apiClient } from "./client";

export const commentsApi = {
    create: async (data: { content: any; incidentId: string }) => {
        const response = await apiClient.post("/comments", data);
        return response.data;
    },

    findAllForIncident: async (incidentId: string) => {
        const response = await apiClient.get(
            `/comments/incident/${incidentId}`
        );
        return response.data;
    },

    delete: async (id: string) => {
        const response = await apiClient.delete(`/comments/${id}`);
        return response.data;
    },
};
```

#### Componente - CommentForm

```typescript
// next-frontend/components/comments/comment-form.tsx
"use client";

import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { commentsApi } from "@/lib/api/comments";
import { useToast } from "@/hooks/use-toast";
import { RichTextEditor } from "@/components/ui/rich-text-editor";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface CommentFormProps {
    incidentId: string;
    onCommentAdded?: () => void;
}

export function CommentForm({ incidentId, onCommentAdded }: CommentFormProps) {
    const [isLoading, setIsLoading] = useState(false);
    const { toast } = useToast();

    const { control, handleSubmit, reset } = useForm({
        defaultValues: {
            content: {
                type: "doc",
                content: [],
            },
        },
    });

    const onSubmit = async (data: any) => {
        setIsLoading(true);

        try {
            await commentsApi.create({
                content: data.content,
                incidentId,
            });

            toast({
                title: "Comentário adicionado",
                description: "O seu comentário foi publicado com sucesso.",
            });

            reset();
            onCommentAdded?.();
        } catch (error: any) {
            toast({
                title: "Erro",
                description:
                    error.response?.data?.message ||
                    "Erro ao adicionar comentário.",
                variant: "destructive",
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Adicionar Comentário</CardTitle>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <Controller
                        name="content"
                        control={control}
                        render={({ field }) => (
                            <RichTextEditor
                                content={field.value}
                                onChange={field.onChange}
                                placeholder="Escreva o seu comentário..."
                            />
                        )}
                    />

                    <Button type="submit" disabled={isLoading}>
                        {isLoading ? "A publicar..." : "Publicar Comentário"}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
}
```

#### Componente - CommentList

```typescript
// next-frontend/components/comments/comment-list.tsx
"use client";

import { useQuery } from "@tanstack/react-query";
import { commentsApi } from "@/lib/api/comments";
import { CommentItem } from "./comment-item";
import { Skeleton } from "@/components/ui/skeleton";

interface CommentListProps {
    incidentId: string;
}

export function CommentList({ incidentId }: CommentListProps) {
    const { data: comments, isLoading } = useQuery({
        queryKey: ["comments", incidentId],
        queryFn: () => commentsApi.findAllForIncident(incidentId),
    });

    if (isLoading) {
        return (
            <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                    <Skeleton key={i} className="h-24 w-full" />
                ))}
            </div>
        );
    }

    if (!comments || comments.length === 0) {
        return (
            <div className="text-center py-8 text-muted-foreground">
                Ainda não há comentários neste incidente.
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {comments.map((comment: any) => (
                <CommentItem key={comment.id} comment={comment} />
            ))}
        </div>
    );
}
```

#### Componente - CommentItem

```typescript
// next-frontend/components/comments/comment-item.tsx
"use client";

import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";
import { EditorContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Link from "@tiptap/extension-link";

interface CommentItemProps {
    comment: {
        id: string;
        content: any;
        createdAt: string;
        author: {
            id: string;
            name: string;
            email: string;
            avatar?: string;
        };
    };
}

export function CommentItem({ comment }: CommentItemProps) {
    const editor = useEditor({
        extensions: [StarterKit, Link],
        content: comment.content,
        editable: false,
        editorProps: {
            attributes: {
                class: "prose prose-sm max-w-none",
            },
        },
    });

    const initials = comment.author.name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2);

    const timeAgo = formatDistanceToNow(new Date(comment.createdAt), {
        addSuffix: true,
        locale: ptBR,
    });

    return (
        <Card>
            <CardContent className="pt-6">
                <div className="flex gap-4">
                    <Avatar>
                        <AvatarImage src={comment.author.avatar} />
                        <AvatarFallback>{initials}</AvatarFallback>
                    </Avatar>

                    <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="font-semibold">
                                {comment.author.name}
                            </span>
                            <span className="text-sm text-muted-foreground">
                                {timeAgo}
                            </span>
                        </div>

                        <div className="text-sm">
                            {editor && <EditorContent editor={editor} />}
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
```

---

### Fase 3: Frontend (Next.js)

#### 3.1. Criar Componentes de Comentários

**Ficheiros:**

-   `next-frontend/components/comments/comment-list.tsx`
-   `next-frontend/components/comments/comment-item.tsx`
-   `next-frontend/components/comments/comment-form.tsx`

**Objetivo:**
Criar os componentes de UI para exibir e adicionar comentários.

**Descrição:**

-   **`CommentList`**: Faz o fetch dos dados de `GET /api/comments/incident/:id` e mapeia os resultados, renderizando um `CommentItem` para cada um.
-   **`CommentItem`**: Exibe o avatar do autor, nome, data e o conteúdo do comentário.
-   **`CommentForm`**: Um formulário simples com uma `Textarea` (shadcn/ui) e um botão de submissão.

**Documentação:**
[Guia Oficial do React sobre Composição de Componentes](https://react.dev/learn/passing-props-to-a-component)

#### 3.2. Integrar na Página de Detalhes do Incidente

**Ficheiro:** `next-frontend/app/incidents/[id]/page.tsx`

**Objetivo:**
Adicionar a secção de comentários à página de detalhes de um incidente.

**Ações:**

-   Abaixo dos detalhes principais do incidente, renderize o componente `CommentList`.
-   Abaixo da lista de comentários, renderize o componente `CommentForm`.
-   Use `TanStack Query` para gerir o estado dos comentários, incluindo o re-fetching da lista após a submissão de um novo comentário.

**Documentação:**
[Guia do TanStack Query sobre Invalidação de Queries](https://tanstack.com/query/latest/docs/react/guides/query-invalidation)

#### 3.3. Testar o Fluxo de Comentários

**Testes Manuais:**

1. **Adicionar Comentário:**

-   Navegue para `http://localhost:3000/incidents/[id]` (um incidente existente)
-   Localize a secção de comentários na parte inferior da página
-   Digite um comentário no formulário
-   Submeta → comentário deve aparecer instantaneamente na lista
-   Verifique: nome do autor, avatar e timestamp estão corretos
-   Atualize a página → comentário persiste
-   Verifique PostgreSQL: registo criado na tabela `comments`

2. **Listar Comentários:**

-   Abra um incidente que já tenha vários comentários
-   Verifique: comentários aparecem ordenados cronologicamente (mais antigos primeiro)
-   Verifique: cada comentário mostra o avatar e nome do autor
-   Verifique: timestamps formatados corretamente

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

-   **Campos:** `id`, `filename`, `filepath`, `mimetype`, `size`.
-   **Relações:** Crie uma relação `incident` com o modelo `Incident` e `uploadedBy` com o modelo `User`.

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

-   Importe o `MulterModule` e registe-o de forma global.
-   Configure o destino (`dest`) para uma pasta no servidor (ex: `./uploads`). Crie esta pasta na raiz do projeto Nest.js e adicione-a ao `.gitignore`.

**Documentação:**
[Guia Oficial do Nest.js sobre Upload de Ficheiros](https://docs.nestjs.com/techniques/file-upload)

#### 2.2. Criar o Endpoint de Upload

**Ficheiro:** `nest-backend/src/incidents/incidents.controller.ts`

**Objetivo:**
Criar uma rota para receber o ficheiro e associá-lo a um incidente.

**Ação:**

-   Crie um endpoint `POST /:id/attachments`.
-   Use os decoradores `@UseInterceptors(FileInterceptor('file'))` e `@UploadedFile()`.
-   No service, crie um registo na tabela `Attachment` com os metadados do ficheiro (`file.originalname`, `file.path`, etc.) e o `incidentId`.

#### 2.3. Criar Endpoint para Servir Ficheiros

**Ficheiro:** `nest-backend/src/main.ts`

**Objetivo:**
Permitir que o frontend aceda aos ficheiros que foram guardados localmente.

**Ação:**

-   Use o `app.useStaticAssets()` para expor a pasta `./uploads` publicamente.
-   Isto cria uma rota virtual (ex: `http://localhost:8000/uploads/filename.txt`) que serve os ficheiros.

**Documentação:**
[Guia Oficial do Nest.js sobre Servir Ativos Estáticos](https://docs.nestjs.com/recipes/serve-static-files)

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

-   Use um `<input type="file">` estilizado como um botão ou uma área de "arrastar e soltar" (drag-and-drop).
-   Ao selecionar um ficheiro, use `FormData` para o enviar para o endpoint `POST /api/incidents/:id/attachments`.
-   Mostre uma barra de progresso durante o upload.

**Documentação:**
[MDN - Usando FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects)

#### 3.2. Integrar na Página de Detalhes do Incidente

**Ficheiro:** `next-frontend/app/incidents/[id]/page.tsx`

**Ação:**

-   Adicione uma secção "Anexos".
-   Liste os anexos existentes, com links para download que apontam para a rota estática do backend.
-   Renderize o componente `AttachmentUploader` para permitir novos uploads.

#### 3.3. Testar o Fluxo de Anexos

**Testes Manuais:**

1. **Fazer Upload de Ficheiro:**

-   Navegue para `http://localhost:3000/incidents/[id]`
-   Localize a secção "Anexos"
-   Clique no botão de upload ou arraste um ficheiro para a área de drop
-   Selecione um ficheiro (ex: `.txt`, `.pdf`, `.png`, `.log`)
-   Verifique: barra de progresso durante o upload
-   Verifique: ficheiro aparece na lista de anexos com nome e tamanho corretos
-   Verifique: ícone apropriado para o tipo de ficheiro

2. **Download de Ficheiro:**

-   Clique no link de um anexo existente
-   Verifique: download inicia corretamente ou ficheiro abre em nova aba (para PDFs/imagens)
-   Verifique: ficheiro baixado é idêntico ao original

3. **Verificar Armazenamento:**

-   Navegue para a pasta `nest-backend/uploads/`
-   Verifique: ficheiro foi guardado fisicamente no servidor
-   Verifique: nome do ficheiro no sistema (pode ser diferente do nome original)

4. **Validações:**

-   Tente fazer upload de um ficheiro muito grande (> 10MB)
-   Verifique: mensagem de erro apropriada
-   Tente fazer upload sem selecionar ficheiro
-   Verifique: botão de submissão desabilitado ou mensagem de erro

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

### Exemplo de Código Completo: Sistema de Anexos (Backend)

#### Schema Prisma - Attachment Model

```prisma
// nest-backend/prisma/schema.prisma (adicionar)
model Attachment {
 id String @id @default(cuid())
 filename String
 originalName String
 filepath String
 mimetype String
 size Int
 incidentId String
 uploadedById String
 createdAt DateTime @default(now())

 incident Incident @relation(fields: [incidentId], references: [id], onDelete: Cascade)
 uploadedBy User @relation("UploadedAttachments", fields: [uploadedById], references: [id])

 @@index([incidentId])
 @@index([uploadedById])
}

// Atualizar Incident model
model Incident {
 // ... campos existentes ...
 attachments Attachment[]
 // ... resto do modelo ...
}

// Atualizar User model
model User {
 // ... campos existentes ...
 attachments Attachment[] @relation("UploadedAttachments")
 // ... resto do modelo ...
}
```

#### Module - MulterModule Configuration

```typescript
// nest-backend/src/attachments/attachments.module.ts
import { Module } from "@nestjs/common";
import { MulterModule } from "@nestjs/platform-express";
import { diskStorage } from "multer";
import { extname } from "path";
import { AttachmentsController } from "./attachments.controller";
import { AttachmentsService } from "./attachments.service";
import { PrismaModule } from "../prisma/prisma.module";
import { CaslModule } from "../casl/casl.module";

@Module({
    imports: [
        PrismaModule,
        CaslModule,
        MulterModule.register({
            storage: diskStorage({
                destination: "./uploads",
                filename: (req, file, callback) => {
                    const uniqueSuffix =
                        Date.now() + "-" + Math.round(Math.random() * 1e9);
                    const ext = extname(file.originalname);
                    const filename = `${file.fieldname}-${uniqueSuffix}${ext}`;
                    callback(null, filename);
                },
            }),
            limits: {
                fileSize: 10 * 1024 * 1024, // 10MB
            },
            fileFilter: (req, file, callback) => {
                // Tipos de ficheiro permitidos
                const allowedMimes = [
                    "image/jpeg",
                    "image/png",
                    "image/gif",
                    "application/pdf",
                    "application/zip",
                    "text/plain",
                    "application/json",
                ];

                if (allowedMimes.includes(file.mimetype)) {
                    callback(null, true);
                } else {
                    callback(
                        new Error("Tipo de ficheiro não permitido"),
                        false
                    );
                }
            },
        }),
    ],
    controllers: [AttachmentsController],
    providers: [AttachmentsService],
})
export class AttachmentsModule {}
```

#### Service - AttachmentsService

```typescript
// nest-backend/src/attachments/attachments.service.ts
import {
    Injectable,
    Inject,
    Logger,
    NotFoundException,
    ForbiddenException,
} from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { WINSTON_MODULE_NEST_PROVIDER } from "nest-winston";
import { CaslAbilityFactory, Action } from "../casl/casl-ability.factory";
import * as fs from "fs/promises";

@Injectable()
export class AttachmentsService {
    constructor(
        private prisma: PrismaService,
        @Inject(WINSTON_MODULE_NEST_PROVIDER) private readonly logger: Logger,
        private caslAbilityFactory: CaslAbilityFactory
    ) {}

    async create(
        file: Express.Multer.File,
        incidentId: string,
        userId: string
    ) {
        this.logger.info(`Upload de ficheiro: ${file.originalname}`, {
            context: "AttachmentsService",
            incidentId,
            userId,
            size: file.size,
            mimetype: file.mimetype,
        });

        // Verificar se o incidente existe
        const incident = await this.prisma.incident.findUnique({
            where: { id: incidentId },
        });

        if (!incident) {
            // Apagar ficheiro se incidente não existir
            await fs.unlink(file.path);
            throw new NotFoundException("Incidente não encontrado");
        }

        const attachment = await this.prisma.attachment.create({
            data: {
                filename: file.filename,
                originalName: file.originalname,
                filepath: file.path,
                mimetype: file.mimetype,
                size: file.size,
                incidentId,
                uploadedById: userId,
            },
            include: {
                uploadedBy: {
                    select: {
                        id: true,
                        name: true,
                        email: true,
                    },
                },
            },
        });

        this.logger.info(`Anexo criado: ${attachment.id}`, {
            context: "AttachmentsService",
            attachmentId: attachment.id,
            filename: file.originalname,
        });

        return attachment;
    }

    async findAllForIncident(incidentId: string) {
        return this.prisma.attachment.findMany({
            where: { incidentId },
            include: {
                uploadedBy: {
                    select: {
                        id: true,
                        name: true,
                        email: true,
                    },
                },
            },
            orderBy: {
                createdAt: "desc",
            },
        });
    }

    async delete(id: string, user: any) {
        const attachment = await this.prisma.attachment.findUnique({
            where: { id },
        });

        if (!attachment) {
            throw new NotFoundException("Anexo não encontrado");
        }

        // Verificar permissões: apenas autor ou admin pode apagar
        if (user.role !== "ADMIN" && attachment.uploadedById !== user.id) {
            throw new ForbiddenException(
                "Não tem permissão para apagar este anexo"
            );
        }

        // Apagar ficheiro físico
        try {
            await fs.unlink(attachment.filepath);
            this.logger.info(
                `Ficheiro físico apagado: ${attachment.filepath}`,
                {
                    context: "AttachmentsService",
                }
            );
        } catch (error) {
            this.logger.error(
                `Erro ao apagar ficheiro físico: ${attachment.filepath}`,
                {
                    context: "AttachmentsService",
                    error: error.message,
                }
            );
        }

        // Apagar registo da BD
        await this.prisma.attachment.delete({
            where: { id },
        });

        this.logger.info(`Anexo apagado: ${id}`, {
            context: "AttachmentsService",
            userId: user.id,
        });

        return { message: "Anexo apagado com sucesso" };
    }
}
```

#### Controller - AttachmentsController

```typescript
// nest-backend/src/attachments/attachments.controller.ts
import {
    Controller,
    Get,
    Post,
    Delete,
    Param,
    UseGuards,
    UseInterceptors,
    UploadedFile,
    Req,
    BadRequestException,
} from "@nestjs/common";
import { AuthGuard } from "@nestjs/passport";
import { FileInterceptor } from "@nestjs/platform-express";
import {
    ApiTags,
    ApiOperation,
    ApiResponse,
    ApiBearerAuth,
    ApiConsumes,
    ApiBody,
} from "@nestjs/swagger";
import { AttachmentsService } from "./attachments.service";

@ApiTags("attachments")
@Controller("attachments")
@UseGuards(AuthGuard("jwt"))
@ApiBearerAuth()
export class AttachmentsController {
    constructor(private attachmentsService: AttachmentsService) {}

    @Post("incident/:incidentId")
    @UseInterceptors(FileInterceptor("file"))
    @ApiConsumes("multipart/form-data")
    @ApiOperation({ summary: "Upload de ficheiro para um incidente" })
    @ApiBody({
        schema: {
            type: "object",
            properties: {
                file: {
                    type: "string",
                    format: "binary",
                },
            },
        },
    })
    @ApiResponse({ status: 201, description: "Ficheiro carregado com sucesso" })
    @ApiResponse({ status: 400, description: "Ficheiro inválido" })
    @ApiResponse({ status: 404, description: "Incidente não encontrado" })
    async uploadFile(
        @UploadedFile() file: Express.Multer.File,
        @Param("incidentId") incidentId: string,
        @Req() req: any
    ) {
        if (!file) {
            throw new BadRequestException("Nenhum ficheiro fornecido");
        }

        return this.attachmentsService.create(file, incidentId, req.user.id);
    }

    @Get("incident/:incidentId")
    @ApiOperation({ summary: "Listar anexos de um incidente" })
    @ApiResponse({ status: 200, description: "Lista de anexos" })
    async findAllForIncident(@Param("incidentId") incidentId: string) {
        return this.attachmentsService.findAllForIncident(incidentId);
    }

    @Delete(":id")
    @ApiOperation({ summary: "Apagar anexo" })
    @ApiResponse({ status: 200, description: "Anexo apagado" })
    @ApiResponse({ status: 403, description: "Sem permissão" })
    @ApiResponse({ status: 404, description: "Anexo não encontrado" })
    async delete(@Param("id") id: string, @Req() req: any) {
        return this.attachmentsService.delete(id, req.user);
    }
}
```

#### Main.ts - Servir Ficheiros Estáticos

```typescript
// nest-backend/src/main.ts (adicionar)
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";
import { NestExpressApplication } from "@nestjs/platform-express";
import { join } from "path";

async function bootstrap() {
    const app = await NestFactory.create<NestExpressApplication>(AppModule);

    // Servir ficheiros estáticos da pasta uploads
    app.useStaticAssets(join(__dirname, "..", "uploads"), {
        prefix: "/uploads/",
    });

    // ... resto da configuração ...

    await app.listen(process.env.PORT || 8000);
}
bootstrap();
```

---

### Exemplo de Código Completo: Sistema de Anexos (Frontend)

#### API Service - Attachments

```typescript
// next-frontend/lib/api/attachments.ts
import { apiClient } from "./client";

export const attachmentsApi = {
    upload: async (
        incidentId: string,
        file: File,
        onUploadProgress?: (progress: number) => void
    ) => {
        const formData = new FormData();
        formData.append("file", file);

        const response = await apiClient.post(
            `/attachments/incident/${incidentId}`,
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
                onUploadProgress: (progressEvent) => {
                    if (progressEvent.total) {
                        const progress = Math.round(
                            (progressEvent.loaded * 100) / progressEvent.total
                        );
                        onUploadProgress?.(progress);
                    }
                },
            }
        );

        return response.data;
    },

    findAllForIncident: async (incidentId: string) => {
        const response = await apiClient.get(
            `/attachments/incident/${incidentId}`
        );
        return response.data;
    },

    delete: async (id: string) => {
        const response = await apiClient.delete(`/attachments/${id}`);
        return response.data;
    },

    getDownloadUrl: (filepath: string) => {
        return `${process.env.NEXT_PUBLIC_API_URL}/uploads/${filepath
            .split("/")
            .pop()}`;
    },
};
```

#### Componente - AttachmentUploader

```typescript
// next-frontend/components/attachments/attachment-uploader.tsx
"use client";

import { useState, useRef } from "react";
import { attachmentsApi } from "@/lib/api/attachments";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Upload, X } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

interface AttachmentUploaderProps {
    incidentId: string;
    onUploadComplete?: () => void;
}

export function AttachmentUploader({
    incidentId,
    onUploadComplete,
}: AttachmentUploaderProps) {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const { toast } = useToast();

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            // Validar tamanho (10MB)
            if (file.size > 10 * 1024 * 1024) {
                toast({
                    title: "Ficheiro muito grande",
                    description: "O ficheiro não pode exceder 10MB.",
                    variant: "destructive",
                });
                return;
            }

            setSelectedFile(file);
            setUploadProgress(0);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsUploading(true);

        try {
            await attachmentsApi.upload(
                incidentId,
                selectedFile,
                (progress) => {
                    setUploadProgress(progress);
                }
            );

            toast({
                title: "Ficheiro carregado",
                description: `${selectedFile.name} foi carregado com sucesso.`,
            });

            setSelectedFile(null);
            setUploadProgress(0);
            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
            onUploadComplete?.();
        } catch (error: any) {
            toast({
                title: "Erro no upload",
                description:
                    error.response?.data?.message ||
                    "Erro ao carregar ficheiro.",
                variant: "destructive",
            });
        } finally {
            setIsUploading(false);
        }
    };

    const handleCancel = () => {
        setSelectedFile(null);
        setUploadProgress(0);
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    return (
        <Card>
            <CardContent className="pt-6">
                <div className="space-y-4">
                    <div className="flex items-center gap-4">
                        <input
                            ref={fileInputRef}
                            type="file"
                            onChange={handleFileSelect}
                            disabled={isUploading}
                            className="hidden"
                            id="file-upload"
                        />

                        <label htmlFor="file-upload">
                            <Button
                                type="button"
                                variant="outline"
                                disabled={isUploading}
                                asChild
                            >
                                <span>
                                    <Upload className="mr-2 h-4 w-4" />
                                    Selecionar Ficheiro
                                </span>
                            </Button>
                        </label>

                        {selectedFile && (
                            <div className="flex items-center gap-2 flex-1">
                                <span className="text-sm truncate">
                                    {selectedFile.name}
                                </span>
                                <span className="text-xs text-muted-foreground">
                                    ({(selectedFile.size / 1024).toFixed(2)} KB)
                                </span>

                                {!isUploading && (
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        size="sm"
                                        onClick={handleCancel}
                                    >
                                        <X className="h-4 w-4" />
                                    </Button>
                                )}
                            </div>
                        )}
                    </div>

                    {selectedFile && (
                        <>
                            {isUploading && (
                                <div className="space-y-2">
                                    <Progress value={uploadProgress} />
                                    <p className="text-sm text-muted-foreground text-center">
                                        A carregar... {uploadProgress}%
                                    </p>
                                </div>
                            )}

                            <Button
                                onClick={handleUpload}
                                disabled={isUploading}
                                className="w-full"
                            >
                                {isUploading
                                    ? "A carregar..."
                                    : "Carregar Ficheiro"}
                            </Button>
                        </>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}
```

#### Componente - AttachmentList

```typescript
// next-frontend/components/attachments/attachment-list.tsx
"use client";

import { useQuery } from "@tanstack/react-query";
import { attachmentsApi } from "@/lib/api/attachments";
import { AttachmentItem } from "./attachment-item";
import { Skeleton } from "@/components/ui/skeleton";

interface AttachmentListProps {
    incidentId: string;
}

export function AttachmentList({ incidentId }: AttachmentListProps) {
    const { data: attachments, isLoading } = useQuery({
        queryKey: ["attachments", incidentId],
        queryFn: () => attachmentsApi.findAllForIncident(incidentId),
    });

    if (isLoading) {
        return (
            <div className="space-y-2">
                {[1, 2].map((i) => (
                    <Skeleton key={i} className="h-16 w-full" />
                ))}
            </div>
        );
    }

    if (!attachments || attachments.length === 0) {
        return (
            <div className="text-center py-8 text-muted-foreground">
                Ainda não há anexos neste incidente.
            </div>
        );
    }

    return (
        <div className="space-y-2">
            {attachments.map((attachment: any) => (
                <AttachmentItem key={attachment.id} attachment={attachment} />
            ))}
        </div>
    );
}
```

#### Componente - AttachmentItem

```typescript
// next-frontend/components/attachments/attachment-item.tsx
"use client";

import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";
import { attachmentsApi } from "@/lib/api/attachments";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Download, FileText, Image, FileArchive, Trash2 } from "lucide-react";

interface AttachmentItemProps {
    attachment: {
        id: string;
        originalName: string;
        filepath: string;
        mimetype: string;
        size: number;
        createdAt: string;
        uploadedBy: {
            name: string;
        };
    };
    onDelete?: () => void;
}

export function AttachmentItem({ attachment, onDelete }: AttachmentItemProps) {
    const downloadUrl = attachmentsApi.getDownloadUrl(attachment.filepath);

    const getFileIcon = () => {
        if (attachment.mimetype.startsWith("image/")) {
            return <Image className="h-5 w-5" />;
        } else if (attachment.mimetype === "application/pdf") {
            return <FileText className="h-5 w-5" />;
        } else if (attachment.mimetype === "application/zip") {
            return <FileArchive className="h-5 w-5" />;
        }
        return <FileText className="h-5 w-5" />;
    };

    const formatSize = (bytes: number) => {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    };

    const timeAgo = formatDistanceToNow(new Date(attachment.createdAt), {
        addSuffix: true,
        locale: ptBR,
    });

    return (
        <Card>
            <CardContent className="p-4">
                <div className="flex items-center gap-4">
                    <div className="text-muted-foreground">{getFileIcon()}</div>

                    <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">
                            {attachment.originalName}
                        </p>
                        <p className="text-sm text-muted-foreground">
                            {formatSize(attachment.size)} •{" "}
                            {attachment.uploadedBy.name} • {timeAgo}
                        </p>
                    </div>

                    <div className="flex gap-2">
                        <Button size="sm" variant="outline" asChild>
                            <a
                                href={downloadUrl}
                                download
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <Download className="h-4 w-4" />
                            </a>
                        </Button>

                        {onDelete && (
                            <Button
                                size="sm"
                                variant="destructive"
                                onClick={onDelete}
                            >
                                <Trash2 className="h-4 w-4" />
                            </Button>
                        )}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
```

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
