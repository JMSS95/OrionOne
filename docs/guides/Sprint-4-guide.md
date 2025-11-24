# Guia de Implementação Detalhado do Sprint 4: Knowledge Base & Meilisearch

## Visão Geral do Sprint

**Objetivo:**
Implementar uma Knowledge Base (KB) para artigos de autoajuda e integrar o Meilisearch para uma pesquisa unificada e instantânea que abranja tanto incidentes como artigos da KB.

**User Stories:**

-   [Em Curso] US4.1: Criar, Editar e Visualizar Artigos da Knowledge Base
-   [Em Curso] US4.2: Integrar Meilisearch para Pesquisa Unificada (Incidentes + Artigos)
-   [Em Curso] US4.3: Exibir Resultados de Pesquisa numa Interface Única

**Pré-requisitos:**

-   Sprints 1, 2 e 3 completos.
-   Container Docker do Meilisearch a correr.

---

## Aplicando as Tecnologias Fundamentais

Neste sprint, o foco é a criação da Knowledge Base e a sua integração com um motor de pesquisa avançado. Vamos aplicar as tecnologias da nossa stack para construir esta funcionalidade de forma robusta.

### 1. Pesquisa Avançada com Meilisearch

**Objetivo:** Implementar uma pesquisa full-text rápida e com tolerância a erros de digitação para os artigos da Knowledge Base.

**Ações:**

-   **Configuração:** Crie um `MeilisearchModule` e um `MeilisearchService` no `nest-backend`.
-   **Indexação:** Configure um índice `articles` no Meilisearch. O serviço deve ser responsável por adicionar, atualizar e remover artigos do índice sempre que um artigo é criado, atualizado ou apagado na base de dados.
-   **Pesquisa:** O `MeilisearchService` deve expor um método `search` que executa a pesquisa no índice `articles`, permitindo filtros por categoria, status, etc.

**Documentação:**
[Documentação Oficial do Meilisearch](https://www.meilisearch.com/docs/learn/getting_started/quick_start)
[SDK JavaScript do Meilisearch](https://github.com/meilisearch/meilisearch-js)

### 2. Gestão de Configuração com ConfigModule

**Objetivo:** Gerir as credenciais e o endereço do Meilisearch de forma segura.

**Ações:**

-   Adicione `MEILISEARCH_HOST` e `MEILISEARCH_KEY` ao seu ficheiro `.env`.
-   No `MeilisearchModule` ou `MeilisearchService`, use o `ConfigService` do Nest.js para aceder a estas variáveis de ambiente, evitando hardcoding de credenciais.

**Documentação:**
[Guia Oficial do Nest.js sobre Configuration](https://docs.nestjs.com/techniques/configuration)

### 3. Logging de Pesquisa com Winston

**Objetivo:** Registar e analisar o comportamento de pesquisa dos utilizadores.

**Ações:**

-   No `MeilisearchService`, injete o `LoggerService` (Winston).
-   Registe cada pesquisa efetuada (`query`), o número de resultados encontrados e, crucialmente, as pesquisas que não retornam resultados. Isto é valioso para identificar lacunas de conteúdo na Knowledge Base.

**Documentação:**
[Guia Oficial do `nest-winston`](https://github.com/gremo/nest-winston)

### 4. Documentação da API de Pesquisa com Swagger

**Objetivo:** Documentar claramente como utilizar o endpoint de pesquisa.

**Ações:**

-   No `articles.controller.ts` (ou num `search.controller.ts` dedicado), documente o endpoint de pesquisa.
-   Use `@ApiQuery` para detalhar todos os parâmetros de pesquisa disponíveis: `query`, `filter`, `sort`, `limit`, etc.

**Documentação:**
[Guia Oficial do Nest.js sobre OpenAPI (Swagger)](https://docs.nestjs.com/openapi/introduction)

### 5. Autorização com CASL

**Objetivo:** Definir quem pode criar, editar, publicar e ler artigos.

**Ações:**

-   No `casl-ability.factory.ts`, defina as permissões para o `subject` 'Article'.
    -   `ADMIN` pode gerir (`manage`) todos os artigos.
    -   `AGENT` pode criar e editar artigos, mas talvez não publicar.
    -   `USER` pode apenas ler (`read`) artigos com o status `PUBLISHED`.
-   Aplique estas regras nos métodos do `articles.service.ts`.

**Documentação:**
[Guia Oficial do CASL](https://casl.js.org/v6/en/guide/intro)
[Integração do CASL com Nest.js](https://docs.nestjs.com/security/authorization#casl)

### 6. Reutilização do Tiptap e Validação

-   **Tiptap:** Reutilize o componente de Rich Text do frontend para o corpo (`content`) dos artigos, garantindo uma experiência de edição consistente.
-   **Validação:** Use `class-validator` nos DTOs de pesquisa para garantir que os parâmetros (como `query`) são do tipo correto e não estão malformados.

**Documentação:**
[Guia Oficial do Nest.js sobre Validação](https://docs.nestjs.com/techniques/validation)

### 7. Compressão

-   **Compressão:** A compressão global continua a ser importante, especialmente ao retornar o conteúdo de múltiplos artigos nos resultados da pesquisa, reduzindo o tamanho do payload.

---

## Funcionalidade 4.1: CRUD de Artigos da Knowledge Base

**Objetivo:** Implementar um "vertical slice" para a gestão de artigos, utilizando o mesmo editor Rich Text (Tiptap) dos incidentes.

---

### Fase 1: Base de Dados (Prisma & PostgreSQL)

#### 1.1. Definir o Modelo `Article` e `KbCategory`

**Ficheiro:** `nest-backend/prisma/schema.prisma`

**Ação:**
Adicione os modelos `Article` e `KbCategory` para estruturar a Knowledge Base.

**Modelo `Article`:**

-   **Campos:** `id`, `title`, `slug` (único, gerado automaticamente), `content` (do tipo `Json` para rich text do Tiptap), `status` (enum `ArticleStatus`: `DRAFT`, `PUBLISHED`), `createdAt`, `updatedAt`.
-   **Relações:**
    -   `author` (relação muitos-para-um com `User`).
    -   `category` (relação muitos-para-um com `KbCategory`).

**Modelo `KbCategory`:**

-   **Campos:** `id`, `name`, `slug` (único), `description`.

**Documentação:**
[Guia Oficial do Prisma sobre Modelos de Dados e Tipos JSON](https://www.prisma.io/docs/orm/prisma-schema/data-model)

#### 1.2. Executar a Migração

**Comando:**

```bash
cd nest-backend
npm run prisma:migrate:dev -- --name add_kb_tables
```

**O que acontece:**
Guarda o schema, gera o ficheiro SQL com as alterações e aplica-o à base de dados PostgreSQL, criando fisicamente as tabelas `Article` e `KbCategory`.

**Documentação:**
[Guia Oficial do Prisma sobre Migrações](https://www.prisma.io/docs/orm/prisma-migrate/getting-started)

---

### Fase 2: Backend (Nest.js)

#### 2.1. Instalar Dependências

**Comando:**

```bash
cd nest-backend
npm install slugify
```

**Objetivo:**
A biblioteca `slugify` será usada para gerar URLs amigáveis a partir dos títulos dos artigos (ex: "Como Resetar Password" → "como-resetar-password").

#### 2.2. Gerar o Recurso `articles`

**Comando:**

```bash
cd nest-backend
nest g resource articles --no-spec
```

**Resultado:**
Cria automaticamente `articles.module.ts`, `articles.controller.ts`, `articles.service.ts` e a pasta `dto`, poupando trabalho manual.

**Documentação:**
[Guia Oficial do Nest.js sobre Geração de Recursos](https://docs.nestjs.com/cli/generators#resource-generator)

#### 2.2. Definir DTOs para Artigos

**Ficheiros:** `create-article.dto.ts`, `update-article.dto.ts`

**Objetivo:**
Definir a "forma" dos dados que os endpoints esperam. É a primeira camada de validação.

**`CreateArticleDto`:**
Define a estrutura de dados para criar um novo artigo da KB. Os validadores (`class-validator`) garantem a integridade dos dados na entrada da API.

-   `title`: Deve ser uma `string` e não pode estar vazio. Será usado para gerar o `slug` automaticamente.
-   `content`: Deve ser um objeto JSON, preparado para receber a estrutura de dados do editor Tiptap (idêntico aos incidentes).
-   `categoryId`: Deve ser o ID (`string`) de uma categoria KB existente.

**`UpdateArticleDto`:**
Define os campos que podem ser atualizados num artigo existente. Todos os campos devem ser opcionais, permitindo atualizações parciais.

-   `title`: Opcional, para renomear o artigo (regenera o `slug`).
-   `content`: Opcional, para editar o conteúdo rich text.
-   `status`: Opcional, para mudar o estado do artigo (ex: de `DRAFT` para `PUBLISHED`).

**Documentação:**
[Guia Oficial do Nest.js sobre Validação (class-validator)](https://docs.nestjs.com/techniques/validation)

---

### 💻 Exemplo de Código: CRUD de Artigos da KB

#### Backend - Prisma Schema

```prisma
// nest-backend/prisma/schema.prisma
enum ArticleStatus {
  DRAFT
  PUBLISHED
}

model KbCategory {
  id          String    @id @default(cuid())
  name        String
  slug        String    @unique
  description String?
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  articles    Article[]
}

model Article {
  id         String        @id @default(cuid())
  title      String
  slug       String        @unique
  content    Json          // Tiptap rich text
  status     ArticleStatus @default(DRAFT)
  authorId   String
  categoryId String
  createdAt  DateTime      @default(now())
  updatedAt  DateTime      @updatedAt

  author     User          @relation(fields: [authorId], references: [id])
  category   KbCategory    @relation(fields: [categoryId], references: [id])

  @@index([status, categoryId])
  @@index([slug])
}
```

#### Backend - DTOs

```typescript
// nest-backend/src/articles/dto/create-article.dto.ts
import { IsString, IsNotEmpty, IsObject, IsUUID } from "class-validator";
import { ApiProperty } from "@nestjs/swagger";

export class CreateArticleDto {
    @ApiProperty({ example: "Como Resetar Password" })
    @IsString()
    @IsNotEmpty()
    title: string;

    @ApiProperty({
        example: {
            type: "doc",
            content: [
                {
                    type: "paragraph",
                    content: [{ type: "text", text: "Conteúdo..." }],
                },
            ],
        },
        description: "Conteúdo rich text do Tiptap",
    })
    @IsObject()
    content: any;

    @ApiProperty({ example: "cat-123" })
    @IsUUID()
    categoryId: string;
}

// nest-backend/src/articles/dto/update-article.dto.ts
import { PartialType } from "@nestjs/swagger";
import { IsEnum, IsOptional } from "class-validator";
import { ArticleStatus } from "@prisma/client";

export class UpdateArticleDto extends PartialType(CreateArticleDto) {
    @IsOptional()
    @IsEnum(ArticleStatus)
    status?: ArticleStatus;
}
```

#### Backend - Service

```typescript
// nest-backend/src/articles/articles.service.ts
import { Injectable, NotFoundException, Inject } from "@nestjs/common";
import { PrismaService } from "../prisma/prisma.service";
import { WINSTON_MODULE_PROVIDER } from "nest-winston";
import { Logger } from "winston";
import slugify from "slugify";

@Injectable()
export class ArticlesService {
    constructor(
        private prisma: PrismaService,
        @Inject(WINSTON_MODULE_PROVIDER) private readonly logger: Logger
    ) {}

    async create(dto: CreateArticleDto, userId: string) {
        // Generate unique slug
        let slug = slugify(dto.title, { lower: true, strict: true });
        let counter = 2;

        while (await this.prisma.article.findUnique({ where: { slug } })) {
            slug = `${slugify(dto.title, {
                lower: true,
                strict: true,
            })}-${counter}`;
            counter++;
        }

        const article = await this.prisma.article.create({
            data: {
                title: dto.title,
                slug,
                content: dto.content,
                authorId: userId,
                categoryId: dto.categoryId,
                status: "DRAFT",
            },
            include: { author: true, category: true },
        });

        this.logger.info("KB article created", {
            articleId: article.id,
            slug,
            userId,
        });
        return article;
    }

    async findAll(filters?: { status?: string; categoryId?: string }) {
        return this.prisma.article.findMany({
            where: {
                ...(filters?.status && { status: filters.status as any }),
                ...(filters?.categoryId && { categoryId: filters.categoryId }),
            },
            include: {
                author: { select: { name: true, email: true } },
                category: true,
            },
            orderBy: { createdAt: "desc" },
        });
    }

    async findOne(slug: string) {
        const article = await this.prisma.article.findUnique({
            where: { slug },
            include: {
                author: { select: { name: true, email: true } },
                category: true,
            },
        });

        if (!article) {
            throw new NotFoundException(
                `Article with slug "${slug}" not found`
            );
        }

        return article;
    }

    async update(slug: string, dto: UpdateArticleDto) {
        const article = await this.findOne(slug);

        // Regenerate slug if title changed
        let newSlug = slug;
        if (dto.title && dto.title !== article.title) {
            newSlug = slugify(dto.title, { lower: true, strict: true });
            let counter = 2;
            while (
                await this.prisma.article.findUnique({
                    where: { slug: newSlug },
                })
            ) {
                newSlug = `${slugify(dto.title, {
                    lower: true,
                    strict: true,
                })}-${counter}`;
                counter++;
            }
        }

        const updated = await this.prisma.article.update({
            where: { slug },
            data: {
                ...(dto.title && { title: dto.title, slug: newSlug }),
                ...(dto.content && { content: dto.content }),
                ...(dto.status && { status: dto.status }),
                ...(dto.categoryId && { categoryId: dto.categoryId }),
            },
            include: { author: true, category: true },
        });

        this.logger.info("KB article updated", {
            articleId: updated.id,
            slug: newSlug,
        });
        return updated;
    }

    async remove(slug: string) {
        await this.findOne(slug); // Check exists
        await this.prisma.article.delete({ where: { slug } });
        this.logger.info("KB article deleted", { slug });
        return { message: "Article deleted successfully" };
    }
}
```

#### Backend - Controller

```typescript
// nest-backend/src/articles/articles.controller.ts
import {
    Controller,
    Get,
    Post,
    Body,
    Patch,
    Param,
    Delete,
    UseGuards,
    Request,
    Query,
} from "@nestjs/common";
import { ApiTags, ApiOperation, ApiBearerAuth } from "@nestjs/swagger";
import { ArticlesService } from "./articles.service";
import { CreateArticleDto, UpdateArticleDto } from "./dto";
import { JwtAuthGuard } from "../auth/guards/jwt-auth.guard";

@ApiTags("articles")
@Controller("articles")
export class ArticlesController {
    constructor(private readonly articlesService: ArticlesService) {}

    @Post()
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: "Create new KB article" })
    create(@Body() createArticleDto: CreateArticleDto, @Request() req) {
        return this.articlesService.create(createArticleDto, req.user.id);
    }

    @Get()
    @ApiOperation({
        summary: "List all articles (filterable by status/category)",
    })
    findAll(
        @Query("status") status?: string,
        @Query("categoryId") categoryId?: string
    ) {
        return this.articlesService.findAll({ status, categoryId });
    }

    @Get(":slug")
    @ApiOperation({ summary: "Get article by slug" })
    findOne(@Param("slug") slug: string) {
        return this.articlesService.findOne(slug);
    }

    @Patch(":slug")
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: "Update article" })
    update(
        @Param("slug") slug: string,
        @Body() updateArticleDto: UpdateArticleDto
    ) {
        return this.articlesService.update(slug, updateArticleDto);
    }

    @Delete(":slug")
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: "Delete article" })
    remove(@Param("slug") slug: string) {
        return this.articlesService.remove(slug);
    }
}
```

#### Frontend - Formulário de Criação

```typescript
// next-frontend/app/admin/kb/create/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { RichTextEditor } from "@/components/editor/rich-text-editor";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { apiClient } from "@/lib/api-client";

const articleSchema = z.object({
    title: z.string().min(3, "Título deve ter pelo menos 3 caracteres"),
    content: z.any(),
    categoryId: z.string().uuid("Selecione uma categoria válida"),
});

export default function CreateArticlePage() {
    const router = useRouter();
    const {
        register,
        control,
        handleSubmit,
        formState: { errors },
    } = useForm({
        resolver: zodResolver(articleSchema),
    });

    // Fetch categories
    const { data: categories } = useQuery({
        queryKey: ["kb-categories"],
        queryFn: () => apiClient.get("/kb-categories").then((res) => res.data),
    });

    const createMutation = useMutation({
        mutationFn: (data: z.infer<typeof articleSchema>) =>
            apiClient.post("/articles", data),
        onSuccess: (response) => {
            router.push(`/kb/${response.data.slug}`);
        },
    });

    const publishMutation = useMutation({
        mutationFn: async (data: z.infer<typeof articleSchema>) => {
            const created = await apiClient.post("/articles", data);
            return apiClient.patch(`/articles/${created.data.slug}`, {
                status: "PUBLISHED",
            });
        },
        onSuccess: (response) => {
            router.push(`/kb/${response.data.slug}`);
        },
    });

    const onSaveDraft = handleSubmit((data) => createMutation.mutate(data));
    const onPublish = handleSubmit((data) => publishMutation.mutate(data));

    return (
        <div className="max-w-4xl mx-auto p-6">
            <h1 className="text-3xl font-bold mb-6">
                Criar Artigo da Knowledge Base
            </h1>

            <form className="space-y-6">
                <div>
                    <label className="block text-sm font-medium mb-2">
                        Título
                    </label>
                    <Input
                        {...register("title")}
                        placeholder="Como configurar VPN..."
                    />
                    {errors.title && (
                        <p className="text-red-500 text-sm mt-1">
                            {errors.title.message as string}
                        </p>
                    )}
                </div>

                <div>
                    <label className="block text-sm font-medium mb-2">
                        Categoria
                    </label>
                    <select
                        {...register("categoryId")}
                        className="w-full border rounded p-2"
                    >
                        <option value="">Selecione...</option>
                        {categories?.map((cat) => (
                            <option key={cat.id} value={cat.id}>
                                {cat.name}
                            </option>
                        ))}
                    </select>
                    {errors.categoryId && (
                        <p className="text-red-500 text-sm mt-1">
                            {errors.categoryId.message as string}
                        </p>
                    )}
                </div>

                <div>
                    <label className="block text-sm font-medium mb-2">
                        Conteúdo
                    </label>
                    <Controller
                        name="content"
                        control={control}
                        render={({ field }) => (
                            <RichTextEditor
                                value={field.value}
                                onChange={field.onChange}
                                placeholder="Escreva o conteúdo do artigo..."
                            />
                        )}
                    />
                </div>

                <div className="flex gap-4">
                    <Button
                        type="button"
                        onClick={onSaveDraft}
                        disabled={createMutation.isPending}
                        variant="outline"
                    >
                        Guardar como Rascunho
                    </Button>
                    <Button
                        type="button"
                        onClick={onPublish}
                        disabled={publishMutation.isPending}
                    >
                        Publicar
                    </Button>
                </div>
            </form>
        </div>
    );
}
```

#### Frontend - Página de Visualização

```typescript
// next-frontend/app/kb/[slug]/page.tsx
import { notFound } from "next/navigation";
import { EditorContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Link from "@tiptap/extension-link";

async function getArticle(slug: string) {
    const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/articles/${slug}`,
        {
            next: { revalidate: 60 }, // ISR cache
        }
    );
    if (!res.ok) return null;
    return res.json();
}

export default async function ArticlePage({
    params,
}: {
    params: { slug: string };
}) {
    const article = await getArticle(params.slug);

    if (!article || article.status !== "PUBLISHED") {
        notFound();
    }

    return (
        <div className="max-w-4xl mx-auto p-6">
            <nav className="text-sm text-gray-600 mb-4">
                <a href="/kb" className="hover:underline">
                    Knowledge Base
                </a>{" "}
                /
                <a
                    href={`/kb?category=${article.category.slug}`}
                    className="hover:underline"
                >
                    {article.category.name}
                </a>
            </nav>

            <article className="prose prose-lg max-w-none">
                <h1>{article.title}</h1>

                <div className="text-sm text-gray-600 mb-6">
                    Escrito por {article.author.name} •{" "}
                    {new Date(article.createdAt).toLocaleDateString()}
                </div>

                <ArticleContent content={article.content} />
            </article>
        </div>
    );
}

// Client component for Tiptap
("use client");
function ArticleContent({ content }: { content: any }) {
    const editor = useEditor({
        extensions: [StarterKit, Link],
        content,
        editable: false,
    });

    return <EditorContent editor={editor} />;
}
```

#### Fluxo de Execução End-to-End

1. Um administrador navega até `/admin/kb/create`, preenche o formulário e submete. O formulário chama `POST /articles`, que gera o `slug`, guarda o artigo como `DRAFT` e regista o evento nos logs.
2. Quando o administrador clica em **Publicar**, o frontend envia um `PATCH /articles/:slug` para mudar o `status` para `PUBLISHED`. O serviço aplica CASL para validar permissões, sincroniza o artigo no Meilisearch e devolve o estado final.
3. A página `/kb/[slug]` executa `fetch` no servidor (Next.js server component) para `GET /articles/:slug`, valida se está publicado e renderiza o conteúdo com o editor Tiptap em modo read-only.
4. Qualquer edição subsequente repete o ciclo: atualiza o conteúdo, regenera o `slug` se necessário e aciona a reindexação, garantindo que o artigo e a pesquisa estão sempre alinhados.

---

#### 2.3. Implementar o `ArticlesService`

**Ficheiro:** `nest-backend/src/articles/articles.service.ts`

**Objetivo:**
Implementar a lógica de negócio para gestão de artigos da KB.

**Ações:**

1.  **`create()`**:

    -   Recebe o `CreateArticleDto` e o `userId` do utilizador autenticado.
    -   Gere um `slug` único a partir do `title` usando `slugify` (ex: "Como Resetar Password" → "como-resetar-password").
    -   Se o slug já existir, adicione um sufixo numérico (ex: "como-resetar-password-2").
    -   Cria um novo registo na tabela `Article` com status `DRAFT` por defeito.

2.  **`findAll()`**:

    -   Aceita query parameters para filtrar por `status` (ex: só `PUBLISHED`) e `categoryId`.
    -   Retorna a lista de artigos com os dados da categoria (`include: { category: true }`).

3.  **`findOne(slug)`**:

    -   Procura um artigo pelo seu `slug` único.
    -   Inclui os dados do autor e da categoria.

4.  **`update()`**:

    -   Permite atualizar `title`, `content` e `status`.
    -   Se o `title` mudar, regenera o `slug`.

5.  **`remove()`**:
    -   Soft delete ou hard delete do artigo.

**Documentação:**
[Guia Oficial do Prisma sobre Consultas CRUD](https://www.prisma.io/docs/orm/prisma-client/queries/crud)

#### 2.4. Configurar o `ArticlesController`

**Ficheiro:** `nest-backend/src/articles/articles.controller.ts`

**Objetivo:**
Definir as rotas da API para gerir artigos da KB.

**Ações:**

-   **`POST /articles`**: Rota para criar um novo artigo. Protegida com `@UseGuards(JwtAuthGuard)`.
-   **`GET /articles`**: Rota pública para listar artigos publicados (pode aceitar query params para filtrar).
-   **`GET /articles/:slug`**: Rota pública para visualizar um artigo específico pelo seu slug.
-   **`PATCH /articles/:slug`**: Rota para editar um artigo. Protegida com `@UseGuards(JwtAuthGuard)` e verificação de permissões.
-   **`DELETE /articles/:slug`**: Rota para remover um artigo. Protegida com `@UseGuards(JwtAuthGuard)` e verificação de permissões.

**Documentação:**
[Guia Oficial do Nest.js sobre Controllers](https://docs.nestjs.com/controllers)

#### 2.5. Escrever Testes (TDD)

**Ficheiro:** `nest-backend/src/articles/articles.service.spec.ts`

**Testes Essenciais:**

```typescript
describe("ArticlesService - CRUD", () => {
    it("deve criar artigo e gerar slug único", async () => {
        const dto = {
            title: "Como Resetar Password",
            content: { type: "doc", content: [] },
            categoryId: "cat-123",
        };
        const userId = "user-123";
        const result = await service.create(dto, userId);
        expect(result.slug).toBe("como-resetar-password");
        expect(result.status).toBe("DRAFT");
    });

    it("deve adicionar sufixo numérico se slug já existe", async () => {
        // Criar primeiro artigo
        await service.create(
            { title: "Test", categoryId: "cat-123" },
            "user-123"
        );
        // Criar segundo com mesmo título
        const result = await service.create(
            { title: "Test", categoryId: "cat-123" },
            "user-123"
        );
        expect(result.slug).toBe("test-2");
    });

    it("deve listar apenas artigos publicados", async () => {
        const filters = { status: "PUBLISHED" };
        const articles = await service.findAll(filters);
        articles.forEach((article) => {
            expect(article.status).toBe("PUBLISHED");
        });
    });

    it("deve encontrar artigo pelo slug", async () => {
        const slug = "como-resetar-password";
        const article = await service.findOne(slug);
        expect(article.slug).toBe(slug);
        expect(article.author).toBeDefined();
        expect(article.category).toBeDefined();
    });

    it("deve atualizar status de DRAFT para PUBLISHED", async () => {
        const slug = "test-article";
        const result = await service.update(slug, { status: "PUBLISHED" });
        expect(result.status).toBe("PUBLISHED");
    });
});
```

**Executar:**

```bash
npm run test -- articles.service.spec.ts
```

**Documentação:**
[Nest.js Testing](https://docs.nestjs.com/fundamentals/testing)

---

### Fase 3: Frontend (Next.js)

#### 3.1. Criar Páginas da Knowledge Base

**Estrutura de Ficheiros:**

-   `next-frontend/app/kb/page.tsx` (Listagem de categorias/artigos)
-   `next-frontend/app/kb/[slug]/page.tsx` (Visualização de um artigo)
-   `next-frontend/app/admin/kb/create/page.tsx` (Formulário de criação)
-   `next-frontend/app/admin/kb/[slug]/edit/page.tsx` (Formulário de edição)

**Objetivo:**
Criar a interface completa para gestão e visualização de artigos da Knowledge Base.

**Ações:**

1.  **Listagem (`/kb/page.tsx`):**

    -   Mostre as categorias e artigos publicados organizados por categoria.
    -   Use `TanStack Query` para fazer fetch de `GET /api/articles?status=PUBLISHED`.
    -   Cada artigo deve ser um card clicável que navega para `/kb/[slug]`.

2.  **Visualização (`/kb/[slug]/page.tsx`):**

    -   Renderize o conteúdo rich text do artigo usando o viewer do Tiptap (read-only).
    -   Mostre metadados: autor, categoria, data de publicação.
    -   Adicione breadcrumbs para navegação.

3.  **Criação/Edição (`/admin/kb/create` e `/admin/kb/[slug]/edit`):**
    -   **Reutilize o `RichTextEditor`** do Sprint 2 (mesmo componente usado nos incidentes).
    -   Use `React Hook Form` + `Zod` para validação do formulário.
    -   Permita selecionar a categoria através de um dropdown.
    -   Adicione botões para "Guardar como Rascunho" e "Publicar".

**Documentação:**
[Guia Oficial do TanStack Query sobre Query Keys](https://tanstack.com/query/latest/docs/react/guides/query-keys)
[Guia Oficial do Tiptap sobre Editor Read-Only](https://tiptap.dev/docs/editor/api/editor#editable)

#### 3.2. Testar o Fluxo da KB

**Testes Manuais:**

1.  **Criar Artigo como DRAFT:**

    -   Navegue para `http://localhost:3000/admin/kb/create`
    -   Preencha título (ex: "Como Configurar VPN")
    -   Selecione categoria no dropdown
    -   Use o Rich Text Editor:
        -   Adicione texto formatado (bold, italic, listas)
        -   Adicione headings (H2, H3)
        -   Adicione links
        -   Adicione code blocks
    -   Clique "Guardar como Rascunho"
    -   Verifique: slug gerado automaticamente (ex: "como-configurar-vpn")
    -   Verifique PostgreSQL: registo criado com `status: DRAFT`

2.  **Verificar Visibilidade de Rascunhos:**

    -   Navegue para `http://localhost:3000/kb`
    -   Verifique: artigo em DRAFT **não** aparece na listagem pública
    -   Tente aceder diretamente a `/kb/como-configurar-vpn`
    -   Verifique: deve retornar 404 ou mensagem "Artigo não publicado"

3.  **Publicar Artigo:**

    -   Navegue para `http://localhost:3000/admin/kb/como-configurar-vpn/edit`
    -   Clique "Publicar" (ou mude status para PUBLISHED)
    -   Verifique: redirecionamento para página de visualização
    -   Verifique PostgreSQL: `status: PUBLISHED`

4.  **Visualizar Artigo Publicado:**

    -   Navegue para `http://localhost:3000/kb`
    -   Verifique: artigo agora aparece na listagem
    -   Clique no card do artigo
    -   Verifique: conteúdo rich text renderizado corretamente
    -   Verifique: formatação preservada (bold, listas, headings, links)
    -   Verifique: metadados visíveis (autor, categoria, data)

5.  **Testar Slugs Únicos:**
    -   Crie outro artigo com o mesmo título "Como Configurar VPN"
    -   Verifique: slug gerado é "como-configurar-vpn-2"
    -   Verifique: ambos os artigos são acessíveis pelos seus slugs únicos

**Teste E2E (Opcional):**

```typescript
// next-frontend/e2e/kb/create-article.spec.ts
test("criar e publicar artigo da KB", async ({ page }) => {
    await page.goto("/admin/kb/create");

    await page.fill('[name="title"]', "Artigo de Teste E2E");
    await page.selectOption('[name="categoryId"]', { label: "Tutoriais" });

    // Rich text
    const editor = page.locator(".tiptap");
    await editor.click();
    await editor.type("Este é um artigo de teste com **formatação**.");

    // Guardar como rascunho
    await page.click('button:has-text("Guardar como Rascunho")');
    await expect(page.getByText(/artigo criado/i)).toBeVisible();

    // Verificar que não aparece na listagem pública
    await page.goto("/kb");
    await expect(page.getByText("Artigo de Teste E2E")).not.toBeVisible();

    // Publicar
    await page.goto("/admin/kb/artigo-de-teste-e2e/edit");
    await page.click('button:has-text("Publicar")');

    // Verificar que agora aparece
    await page.goto("/kb");
    await expect(page.getByText("Artigo de Teste E2E")).toBeVisible();
});
```

**Documentação:**
[Playwright Testing Guide](https://playwright.dev/)

---

## Funcionalidade 4.2 & 4.3: Pesquisa Unificada com Meilisearch

**Objetivo:** Sincronizar os artigos da KB com o Meilisearch e criar um endpoint de pesquisa que retorne tanto incidentes como artigos.

---

### Fase 1: Backend (Nest.js)

#### 1.1. Configurar o `MeilisearchService`

**Ficheiro:** `nest-backend/src/meilisearch/meilisearch.service.ts`

**Ação:**
Modifique o serviço para gerir múltiplos índices (`incidents` e `articles`).

**Objetivo:**
Extender o serviço para indexar e pesquisar múltiplos tipos de documentos (incidentes e artigos).

**Descrição:**

1.  **`onModuleInit()`**:

    -   Modifique o método para criar e configurar **dois índices**: `incidents` e `articles`.
    -   Para o índice `articles`, defina:
        -   `searchableAttributes`: `['title', 'content', 'category.name']` (campos pesquisáveis)
        -   `filterableAttributes`: `['status', 'categoryId', 'authorId']` (campos filtráveis)
        -   `sortableAttributes`: `['createdAt', 'updatedAt']` (campos ordenáveis)

2.  **Sincronização de Artigos:**

    -   Crie um método `syncArticle(article: Article)` que adiciona ou atualiza um documento no índice `articles`.
    -   **Importante:** Apenas sincronize artigos com `status: PUBLISHED`. Artigos em DRAFT não devem aparecer na pesquisa.
    -   Transforme o objeto `Article` antes de indexar (ex: converta o JSON do `content` em texto plano para pesquisa).
    -   Este método deve ser chamado nos métodos `create` e `update` do `ArticlesService` **apenas quando o status mudar para PUBLISHED**.

3.  **Remoção de Artigos:**
    -   Crie um método `deleteArticle(articleId: string)` para remover artigos do índice.
    -   Chame este método quando um artigo for apagado ou quando mudar de PUBLISHED para DRAFT.

**Documentação:**
[Guia Oficial do Meilisearch sobre Multi-Search](https://www.meilisearch.com/docs/reference/api/multi_search)
[Guia Oficial do Meilisearch sobre Configuração de Índices](https://www.meilisearch.com/docs/learn/core_concepts/indexes)

---

### 💻 Exemplo de Código: Integração Meilisearch

#### Backend - Meilisearch Service

```typescript
// nest-backend/src/meilisearch/meilisearch.service.ts
import { Injectable, OnModuleInit, Inject } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { MeiliSearch } from "meilisearch";
import { WINSTON_MODULE_PROVIDER } from "nest-winston";
import { Logger } from "winston";

@Injectable()
export class MeilisearchService implements OnModuleInit {
    private client: MeiliSearch;

    constructor(
        private config: ConfigService,
        @Inject(WINSTON_MODULE_PROVIDER) private readonly logger: Logger
    ) {
        this.client = new MeiliSearch({
            host:
                this.config.get("MEILISEARCH_HOST") || "http://localhost:7700",
            apiKey: this.config.get("MEILISEARCH_KEY"),
        });
    }

    async onModuleInit() {
        // Configure articles index
        const articlesIndex = this.client.index("articles");
        await articlesIndex.updateSettings({
            searchableAttributes: ["title", "content", "category.name"],
            filterableAttributes: ["status", "categoryId", "authorId"],
            sortableAttributes: ["createdAt", "updatedAt"],
        });

        // Configure incidents index
        const incidentsIndex = this.client.index("incidents");
        await incidentsIndex.updateSettings({
            searchableAttributes: ["title", "description", "incidentNumber"],
            filterableAttributes: ["status", "priority", "assigneeId"],
            sortableAttributes: ["createdAt", "updatedAt"],
        });

        this.logger.info("Meilisearch indexes configured");
    }

    async syncArticle(article: any) {
        if (article.status !== "PUBLISHED") return;

        const plainTextContent = this.extractTextFromTiptap(article.content);
        const document = {
            id: article.id,
            title: article.title,
            slug: article.slug,
            content: plainTextContent,
            status: article.status,
            categoryId: article.categoryId,
            category: article.category,
        };

        await this.client.index("articles").addDocuments([document]);
        this.logger.info("Article synced to Meilisearch", {
            articleId: article.id,
        });
    }

    async deleteArticle(articleId: string) {
        await this.client.index("articles").deleteDocument(articleId);
    }

    async multiSearch(query: string) {
        const results = await this.client.multiSearch({
            queries: [
                {
                    indexUid: "incidents",
                    q: query,
                    limit: 10,
                    attributesToHighlight: ["title", "description"],
                },
                {
                    indexUid: "articles",
                    q: query,
                    filter: "status = PUBLISHED",
                    limit: 10,
                    attributesToHighlight: ["title", "content"],
                },
            ],
        });

        return {
            incidents: results.results[0].hits,
            articles: results.results[1].hits,
            totalHits:
                results.results[0].estimatedTotalHits +
                results.results[1].estimatedTotalHits,
        };
    }

    private extractTextFromTiptap(content: any): string {
        if (!content?.content) return "";
        const extractText = (node: any): string => {
            if (node.type === "text") return node.text || "";
            if (node.content) return node.content.map(extractText).join(" ");
            return "";
        };
        return extractText(content);
    }
}
```

#### Backend - Search Controller

```typescript
// nest-backend/src/search/search.controller.ts
import { Controller, Get, Query, UseGuards } from "@nestjs/common";
import {
    ApiTags,
    ApiOperation,
    ApiBearerAuth,
    ApiQuery,
} from "@nestjs/swagger";
import { JwtAuthGuard } from "../auth/guards/jwt-auth.guard";
import { MeilisearchService } from "../meilisearch/meilisearch.service";

@ApiTags("search")
@Controller("search")
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class SearchController {
    constructor(private readonly meilisearchService: MeilisearchService) {}

    @Get()
    @ApiOperation({ summary: "Unified search across incidents and articles" })
    @ApiQuery({ name: "q", required: true, description: "Search query" })
    async search(@Query("q") query: string) {
        return this.meilisearchService.multiSearch(query);
    }
}
```

#### Frontend - Barra de Pesquisa Global

```typescript
// next-frontend/components/layout/global-search-bar.tsx
"use client";

import { useState, useEffect } from "react";
import { useDebounce } from "@/hooks/use-debounce";
import { useQuery } from "@tanstack/react-query";
import { Input } from "@/components/ui/input";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import { SearchResults } from "./search-results";
import { Search } from "lucide-react";
import { apiClient } from "@/lib/api-client";

export function GlobalSearchBar() {
    const [open, setOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const debouncedSearch = useDebounce(searchTerm, 300);

    const { data, isLoading } = useQuery({
        queryKey: ["search", debouncedSearch],
        queryFn: () =>
            apiClient
                .get(`/search?q=${debouncedSearch}`)
                .then((res) => res.data),
        enabled: debouncedSearch.length >= 3,
    });

    // Keyboard shortcut: Ctrl+K
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if ((e.ctrlKey || e.metaKey) && e.key === "k") {
                e.preventDefault();
                setOpen(true);
            }
        };
        document.addEventListener("keydown", handleKeyDown);
        return () => document.removeEventListener("keydown", handleKeyDown);
    }, []);

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <div className="relative w-full max-w-md">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                    <Input
                        placeholder="Pesquisar... (Ctrl+K)"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10"
                    />
                </div>
            </PopoverTrigger>
            {debouncedSearch.length >= 3 && (
                <PopoverContent className="w-[600px] p-0" align="start">
                    <SearchResults
                        data={data}
                        isLoading={isLoading}
                        onSelectResult={() => setOpen(false)}
                    />
                </PopoverContent>
            )}
        </Popover>
    );
}
```

#### Frontend - Resultados de Pesquisa

```typescript
// next-frontend/components/layout/search-results.tsx
"use client";

import { useRouter } from "next/navigation";
import { Ticket, BookOpen } from "lucide-react";

export function SearchResults({ data, isLoading, onSelectResult }: any) {
    const router = useRouter();

    if (isLoading) return <div className="p-4">Pesquisando...</div>;
    if (!data || data.totalHits === 0)
        return (
            <div className="p-4 text-gray-500">Nenhum resultado encontrado</div>
        );

    const handleClick = (type: "incident" | "article", id: string) => {
        router.push(type === "incident" ? `/incidents/${id}` : `/kb/${id}`);
        onSelectResult();
    };

    return (
        <div className="max-h-[500px] overflow-y-auto">
            {data.incidents?.length > 0 && (
                <div className="p-4 border-b">
                    <h3 className="text-sm font-semibold text-gray-600 mb-2 flex items-center gap-2">
                        <Ticket className="h-4 w-4" /> Incidentes (
                        {data.incidents.length})
                    </h3>
                    {data.incidents.map((incident: any) => (
                        <div
                            key={incident.id}
                            onClick={() => handleClick("incident", incident.id)}
                            className="p-3 hover:bg-gray-100 rounded cursor-pointer"
                        >
                            <div
                                className="font-medium text-sm"
                                dangerouslySetInnerHTML={{
                                    __html:
                                        incident._formatted?.title ||
                                        incident.title,
                                }}
                            />
                            <div
                                className="text-xs text-gray-600 mt-1 line-clamp-2"
                                dangerouslySetInnerHTML={{
                                    __html: incident._formatted?.description,
                                }}
                            />
                            <div className="text-xs text-gray-500 mt-1">
                                {incident.incidentNumber} • {incident.status}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {data.articles?.length > 0 && (
                <div className="p-4">
                    <h3 className="text-sm font-semibold text-gray-600 mb-2 flex items-center gap-2">
                        <BookOpen className="h-4 w-4" /> Artigos KB (
                        {data.articles.length})
                    </h3>
                    {data.articles.map((article: any) => (
                        <div
                            key={article.id}
                            onClick={() => handleClick("article", article.slug)}
                            className="p-3 hover:bg-gray-100 rounded cursor-pointer"
                        >
                            <div
                                className="font-medium text-sm"
                                dangerouslySetInnerHTML={{
                                    __html:
                                        article._formatted?.title ||
                                        article.title,
                                }}
                            />
                            <div
                                className="text-xs text-gray-600 mt-1 line-clamp-2"
                                dangerouslySetInnerHTML={{
                                    __html: article._formatted?.content,
                                }}
                            />
                            <div className="text-xs text-gray-500 mt-1">
                                {article.category?.name}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
```

---

#### 1.2. Criar um Endpoint de Pesquisa Unificada

**Ficheiro:** `nest-backend/src/search/search.controller.ts` (crie um novo recurso `search`)

**Objetivo:**
Criar um único endpoint `GET /search?q=termo` que pesquisa em múltiplos índices simultaneamente.

**Comando para criar o recurso:**

```bash
cd nest-backend
nest g resource search --no-spec
```

**Ação no `SearchService`:**

1.  Crie um método `search(query: string, userId?: string)`.
2.  Use o método `client.multiSearch()` do Meilisearch:

```typescript
const results = await this.client.multiSearch({
    queries: [
        {
            indexUid: "incidents",
            q: query,
            limit: 10,
            attributesToHighlight: ["title", "description"],
        },
        {
            indexUid: "articles",
            q: query,
            filter: "status = PUBLISHED",
            limit: 10,
            attributesToHighlight: ["title", "content"],
        },
    ],
});
```

3.  **Combine e formate os resultados:**

    -   Agrupe por tipo (`incidents`, `articles`).
    -   Adicione metadados úteis (ex: tipo de documento, ícone, rota).
    -   Use o campo `_formatted` do Meilisearch para obter texto com highlights.

4.  **Retorne um objeto estruturado:**

```typescript
return {
    incidents: results.results[0].hits,
    articles: results.results[1].hits,
    totalHits:
        results.results[0].estimatedTotalHits +
        results.results[1].estimatedTotalHits,
};
```

**Documentação:**
[Guia Oficial do Meilisearch sobre Multi-Search](https://www.meilisearch.com/docs/reference/api/multi_search)

#### 1.3. Escrever Testes (TDD)

**Ficheiro:** `nest-backend/src/search/search.service.spec.ts`

**Testes Essenciais:**

```typescript
describe("SearchService - Pesquisa Unificada", () => {
    it("deve pesquisar em ambos os índices simultaneamente", async () => {
        const query = "network";
        const result = await service.search(query);
        expect(result.incidents).toBeDefined();
        expect(result.articles).toBeDefined();
        expect(meilisearchClient.multiSearch).toHaveBeenCalledWith(
            expect.objectContaining({
                queries: expect.arrayContaining([
                    expect.objectContaining({
                        indexUid: "incidents",
                        q: query,
                    }),
                    expect.objectContaining({ indexUid: "articles", q: query }),
                ]),
            })
        );
    });

    it("deve filtrar apenas artigos PUBLISHED", async () => {
        await service.search("test");
        expect(meilisearchClient.multiSearch).toHaveBeenCalledWith(
            expect.objectContaining({
                queries: expect.arrayContaining([
                    expect.objectContaining({
                        indexUid: "articles",
                        filter: "status = PUBLISHED",
                    }),
                ]),
            })
        );
    });

    it("deve retornar resultados mesmo se um índice estiver vazio", async () => {
        // Mock: incidents tem resultados, articles está vazio
        meilisearchClient.multiSearch.mockResolvedValue({
            results: [
                {
                    hits: [{ id: "1", title: "Incident 1" }],
                    estimatedTotalHits: 1,
                },
                { hits: [], estimatedTotalHits: 0 },
            ],
        });

        const result = await service.search("test");
        expect(result.incidents).toHaveLength(1);
        expect(result.articles).toHaveLength(0);
        expect(result.totalHits).toBe(1);
    });

    it("deve incluir highlights nos resultados", async () => {
        const result = await service.search("network issue");
        result.incidents.forEach((incident) => {
            expect(incident._formatted).toBeDefined();
        });
    });
});
```

**Executar:**

```bash
npm run test -- search.service.spec.ts
```

**Documentação:**
[Nest.js Testing](https://docs.nestjs.com/fundamentals/testing)

---

### Fase 2: Frontend (Next.js)

#### 2.1. Criar uma Barra de Pesquisa Global

**Ficheiro:** `next-frontend/components/layout/global-search-bar.tsx`

**Objetivo:**
Implementar uma barra de pesquisa proeminente e sempre visível, idealmente no cabeçalho da aplicação.

**Descrição:**

1.  **Componente:**

    -   Marque com `"use client";` (componente de cliente).
    -   Use um `Input` (shadcn/ui) com ícone de pesquisa.
    -   Quando focado ou com texto, abra um `Popover` ou `Dialog` com os resultados.

2.  **Debounce:**

    -   Use `useDebouncedValue` ou `useDebounce` para evitar chamadas excessivas.
    -   Apenas faça a pesquisa após o utilizador parar de digitar por 300-500ms.

3.  **Fetching de Dados:**
    -   Use `TanStack Query` com `useQuery`:

```typescript
const { data, isLoading } = useQuery({
    queryKey: ["search", debouncedQuery],
    queryFn: () => searchAPI(debouncedQuery),
    enabled: debouncedQuery.length >= 3, // Apenas pesquisar com 3+ caracteres
});
```

4.  **Atalho de Teclado (Opcional):**
    -   Adicione um atalho global (ex: `Ctrl+K` ou `Cmd+K`) para focar a barra de pesquisa.
    -   Use `useHotkeys` ou evento `keydown` no `useEffect`.

**Documentação:**
[Guia Oficial do shadcn/ui sobre Popover](https://ui.shadcn.com/docs/components/popover)
[Guia Oficial do TanStack Query sobre Enabled Queries](https://tanstack.com/query/latest/docs/react/guides/dependent-queries)

#### 2.2. Criar a UI de Resultados de Pesquisa

**Ficheiro:** `next-frontend/components/search/search-results.tsx`

**Objetivo:**
Exibir os resultados da pesquisa de forma clara, organizada e visualmente apelativa.

**Descrição:**

1.  **Estrutura:**

    -   Divida em secções: "Incidentes" e "Artigos da Knowledge Base".
    -   Se uma secção não tiver resultados, mostre uma mensagem (ex: "Nenhum incidente encontrado").
    -   Limite a exibição inicial a 5 resultados por secção, com botão "Ver todos".

2.  **Card de Resultado:**

    -   **Ícone:** Mostre um ícone diferente para cada tipo (ex: ticket para incidentes, livro para artigos).
    -   **Título:** Use o campo `_formatted.title` do Meilisearch que já inclui os highlights (`<mark>termo</mark>`).
    -   **Trecho:** Mostre as primeiras 2-3 linhas do conteúdo, também com highlights.
    -   **Metadados:** Categoria, status, ou data (conforme relevante).
    -   **Link:** O card inteiro deve ser clicável, navegando para `/incidents/[id]` ou `/kb/[slug]`.

3.  **Estados:**

    -   **Loading:** Mostre skeleton loaders enquanto pesquisa.
    -   **Vazio:** Se nenhum resultado, mostre mensagem amigável (ex: "Nenhum resultado para 'termo'. Tente outras palavras.").
    -   **Erro:** Se a API falhar, mostre mensagem de erro.

4.  **Navegação por Teclado:**
    -   Permita navegar pelos resultados com setas ↑↓.
    -   Enter para abrir o resultado selecionado.
    -   Esc para fechar o popover.

**Documentação:**
[Guia Oficial do Meilisearch sobre Highlighting](https://www.meilisearch.com/docs/learn/fine_tuning_results/search_preview)

#### 2.3. Testar o Fluxo de Pesquisa Unificada

**Testes Manuais:**

1.  **Pesquisar por Termo de Incidente:**
    -   Use um termo que exista apenas num título de incidente.
    -   Verifique se o incidente aparece nos resultados sob o grupo "Incidentes".
2.  **Pesquisar por Termo de Artigo:**
    -   Use um termo que exista apenas num artigo da KB.
    -   Verifique se o artigo aparece nos resultados sob o grupo "Artigos".
3.  **Pesquisar por Termo Comum:**
    -   Use uma palavra que exista em ambos.
    -   Verifique se os resultados aparecem em ambos os grupos.
4.  **Verificar Destaques:**
    -   Confirme que os termos pesquisados estão visualmente destacados (ex: a negrito) nos resultados.
5.  **Navegação:**
    -   Clique num resultado de incidente e verifique se navega para a página correta do incidente.
    -   Clique num resultado de artigo e verifique se navega para a página correta da KB.

**Teste E2E (Opcional):**

```typescript
// next-frontend/e2e/search/unified-search.spec.ts
test("pesquisa unificada deve retornar incidentes e artigos", async ({
    page,
}) => {
    await page.goto("/dashboard");

    // Pesquisar por um termo que existe em ambos
    const searchTerm = "network issue";
    await page.fill('[placeholder*="Search..."]', searchTerm);

    // Verificar se os resultados aparecem
    await expect(page.getByText("Incidentes")).toBeVisible();
    await expect(page.getByText("Artigos da Knowledge Base")).toBeVisible();

    // Verificar se o termo está destacado
    const highlightedResult = page.locator('mark:has-text("network")').first();
    await expect(highlightedResult).toBeVisible();

    // Testar navegação
    await page.click(".search-result-item:first-child");
    await expect(page).toHaveURL(/\/(incidents|kb)\/.+/);
});

test("pesquisa deve funcionar com atalho de teclado", async ({ page }) => {
    await page.goto("/dashboard");

    // Pressionar Ctrl+K (ou Cmd+K no Mac)
    await page.keyboard.press("Control+K");

    // Verificar se barra de pesquisa está focada
    const searchInput = page.locator('[placeholder*="Search..."]');
    await expect(searchInput).toBeFocused();
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
describe("Search API (e2e)", () => {
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

    it("GET /search - deve retornar resultados de ambos os índices", () => {
        return request(app.getHttpServer())
            .get("/search?q=network")
            .set("Authorization", `Bearer ${accessToken}`)
            .expect(200)
            .expect((res) => {
                expect(res.body.incidents).toBeDefined();
                expect(res.body.articles).toBeDefined();
                expect(res.body.totalHits).toBeGreaterThan(0);
            });
    });

    it("GET /search - deve incluir highlights", () => {
        return request(app.getHttpServer())
            .get("/search?q=password")
            .set("Authorization", `Bearer ${accessToken}`)
            .expect(200)
            .expect((res) => {
                const firstResult =
                    res.body.articles[0] || res.body.incidents[0];
                expect(firstResult._formatted).toBeDefined();
            });
    });

    it("GET /search - deve filtrar artigos não publicados", () => {
        return request(app.getHttpServer())
            .get("/search?q=draft")
            .set("Authorization", `Bearer ${accessToken}`)
            .expect(200)
            .expect((res) => {
                res.body.articles.forEach((article) => {
                    expect(article.status).toBe("PUBLISHED");
                });
            });
    });

    afterAll(async () => {
        await app.close();
    });
});
```
