# Shadcn-vue Components - Guia Completo

**Última Atualização:** 08 Novembro 2025, 01:05
**Status:** COMPLETO - 14 Componentes---

## Status da Implementação

### Componentes Criados (14 + 1 Index)

1. **Button.vue** - 6 variantes (default, destructive, outline, secondary, ghost, link), 4 tamanhos
2. **Input.vue** - Text input com suporte para erros e disabled
3. **Textarea.vue** - Textarea com rows configurável
4. **Select.vue** - Dropdown select com variantes
5. **Card.vue** - Container principal
6. **CardHeader.vue** - Cabeçalho do card
7. **CardTitle.vue** - Título do card
8. **CardDescription.vue** - Descrição do card
9. **CardContent.vue** - Conteúdo principal
10. **CardFooter.vue** - Rodapé (botões, ações)
11. **Badge.vue** - 6 variantes (default, secondary, destructive, outline, success, warning)
12. **Label.vue** - Labels com asterisco para campos obrigatórios
13. **Avatar.vue** - 4 tamanhos (sm, md, lg, xl) com fallback
14. **Alert.vue** - 4 variantes (default, destructive, success, warning)
15. **index.js** - Barrel export para imports convenientes

### Estrutura de Ficheiros

```
resources/js/
├── components/
│   └── ui/
│       ├── Alert.vue
│       ├── Avatar.vue
│       ├── Badge.vue
│       ├── Button.vue
│       ├── Card.vue
│       ├── CardContent.vue
│       ├── CardDescription.vue
│       ├── CardFooter.vue
│       ├── CardHeader.vue
│       ├── CardTitle.vue
│       ├── Input.vue
│       ├── Label.vue
│       ├── Select.vue
│       ├── Textarea.vue
│       └── index.js
├── lib/
│   └── utils.js (cn() helper)
└── Pages/
    └── ComponentsDemo.vue (página de teste)
```

### Página de Demo

Criada página de teste em `/components-demo` com:

-   Todos os componentes visíveis
-   Todas as variantes
-   Exemplos de uso
-   Dark mode toggle

**Aceder:** http://localhost:8888/components-demo

---

## Como Importar

### Opção 1: Import individual

```vue
<script setup>
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";
import Card from "@/components/ui/Card.vue";
</script>
```

### Opção 2: Import do index (recomendado)

```vue
<script setup>
import {
    Button,
    Input,
    Card,
    CardHeader,
    CardTitle,
    CardContent,
} from "@/components/ui";
</script>
```

---

## Button

### Variantes

-   `default` (azul/primary)
-   `destructive` (vermelho)
-   `outline` (borda)
-   `secondary` (cinza)
-   `ghost` (transparente)
-   `link` (texto com underline)

### Tamanhos

-   `sm` (pequeno)
-   `default` (médio)
-   `lg` (grande)
-   `icon` (quadrado para ícones)

### Exemplos

```vue
<template>
    <!-- Primary button -->
    <Button>Criar Ticket</Button>

    <!-- Destructive -->
    <Button variant="destructive">Apagar</Button>

    <!-- Outline -->
    <Button variant="outline">Cancelar</Button>

    <!-- Loading state -->
    <Button :disabled="form.processing"> Guardar... </Button>

    <!-- Com ícone -->
    <Button>
        <Icon icon="mdi:plus" class="w-4 h-4 mr-2" />
        Novo Ticket
    </Button>

    <!-- Link button -->
    <Button variant="link" @click="router.visit(route('tickets.index'))">
        Ver todos os tickets
    </Button>
</template>
```

---

## Input

### Props

-   `modelValue` - v-model value
-   `type` - input type (text, email, password, etc)
-   `disabled` - desabilitar input
-   `error` - mostrar estado de erro (borda vermelha)

### Exemplos

```vue
<template>
    <!-- Input simples -->
    <Input v-model="form.title" placeholder="Título do ticket" />

    <!-- Email -->
    <Input v-model="form.email" type="email" placeholder="email@exemplo.com" />

    <!-- Password -->
    <Input v-model="form.password" type="password" />

    <!-- Com erro -->
    <Input
        v-model="form.title"
        :error="!!form.errors.title"
        placeholder="Título"
    />
    <p v-if="form.errors.title" class="text-sm text-destructive mt-1">
        {{ form.errors.title }}
    </p>

    <!-- Disabled -->
    <Input v-model="ticketNumber" disabled />
</template>
```

---

## Textarea

### Props

-   `modelValue` - v-model value
-   `rows` - número de linhas (default: 3)
-   `disabled` - desabilitar
-   `error` - estado de erro

### Exemplos

```vue
<template>
    <!-- Textarea simples -->
    <Textarea v-model="form.description" placeholder="Descreva o problema..." />

    <!-- Com mais linhas -->
    <Textarea v-model="form.description" :rows="6" />

    <!-- Com erro -->
    <Textarea v-model="form.description" :error="!!form.errors.description" />
</template>
```

---

## Select

### Props

-   `modelValue` - v-model value
-   `disabled` - desabilitar
-   `error` - estado de erro

### Exemplos

```vue
<template>
    <!-- Select simples -->
    <Select v-model="form.priority">
        <option value="">Selecione a prioridade</option>
        <option value="low">Baixa</option>
        <option value="medium">Média</option>
        <option value="high">Alta</option>
        <option value="urgent">Urgente</option>
    </Select>

    <!-- Com equipas dinâmicas -->
    <Select v-model="form.team_id">
        <option :value="null">Atribuir automaticamente</option>
        <option v-for="team in teams" :key="team.id" :value="team.id">
            {{ team.name }}
        </option>
    </Select>

    <!-- Com erro -->
    <Select v-model="form.status" :error="!!form.errors.status">
        <option value="open">Aberto</option>
        <option value="closed">Fechado</option>
    </Select>
</template>
```

---

## Card

Card é composto por múltiplos sub-componentes:

-   `Card` - Container principal
-   `CardHeader` - Cabeçalho
-   `CardTitle` - Título
-   `CardDescription` - Descrição
-   `CardContent` - Conteúdo principal
-   `CardFooter` - Rodapé (botões, ações)

### Exemplos

```vue
<template>
    <!-- Card básico -->
    <Card>
        <CardHeader>
            <CardTitle>Criar Ticket</CardTitle>
            <CardDescription>Preencha os dados abaixo</CardDescription>
        </CardHeader>

        <CardContent>
            <div class="space-y-4">
                <div>
                    <Label for="title">Título</Label>
                    <Input id="title" v-model="form.title" />
                </div>

                <div>
                    <Label for="description">Descrição</Label>
                    <Textarea id="description" v-model="form.description" />
                </div>
            </div>
        </CardContent>

        <CardFooter class="gap-2">
            <Button @click="submit">Criar</Button>
            <Button variant="outline" @click="cancel">Cancelar</Button>
        </CardFooter>
    </Card>

    <!-- Card de ticket (clicável) -->
    <Card
        class="cursor-pointer hover:shadow-lg transition"
        @click="router.visit(route('tickets.show', ticket.id))"
    >
        <CardContent class="pt-6">
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-foreground">{{
                        ticket.ticket_number
                    }}</span>
                    <Badge :variant="statusVariant(ticket.status)">
                        {{ ticket.status }}
                    </Badge>
                </div>

                <h3 class="font-medium">{{ ticket.title }}</h3>
                <p class="text-sm text-muted-foreground line-clamp-2">
                    {{ ticket.description }}
                </p>
            </div>
        </CardContent>
    </Card>
</template>
```

---

## Badge

### Variantes

-   `default` (azul)
-   `secondary` (cinza)
-   `destructive` (vermelho)
-   `outline` (borda)
-   `success` (verde)
-   `warning` (amarelo)

### Exemplos

```vue
<template>
    <!-- Status badges -->
    <Badge>Open</Badge>
    <Badge variant="warning">In Progress</Badge>
    <Badge variant="success">Resolved</Badge>
    <Badge variant="secondary">Closed</Badge>

    <!-- Prioridade -->
    <Badge variant="destructive">Urgent</Badge>
    <Badge variant="warning">High</Badge>
    <Badge>Medium</Badge>
    <Badge variant="secondary">Low</Badge>

    <!-- Custom -->
    <Badge variant="outline">Draft</Badge>
</template>
```

---

## Label

### Props

-   `for` - ID do input associado
-   `required` - mostrar asterisco vermelho

### Exemplos

```vue
<template>
    <!-- Label simples -->
    <Label for="email">Email</Label>
    <Input id="email" type="email" />

    <!-- Obrigatório -->
    <Label for="title" required>Título</Label>
    <Input id="title" />

    <!-- Custom styling -->
    <Label for="description" class="text-lg">Descrição Completa</Label>
</template>
```

---

## Avatar

### Props

-   `src` - URL da imagem
-   `alt` - Texto alternativo
-   `fallback` - Letra/texto a mostrar se sem imagem
-   `size` - sm, md (default), lg, xl

### Exemplos

```vue
<template>
    <!-- Com imagem -->
    <Avatar src="/storage/avatars/user.jpg" alt="João Santos" />

    <!-- Fallback (primeira letra do nome) -->
    <Avatar alt="João Santos" fallback="JS" />

    <!-- Tamanhos -->
    <Avatar size="sm" :src="user.avatar" />
    <Avatar size="md" :src="user.avatar" />
    <Avatar size="lg" :src="user.avatar" />
    <Avatar size="xl" :src="user.avatar" />

    <!-- Lista de utilizadores -->
    <div class="flex -space-x-2">
        <Avatar
            v-for="user in team.members"
            :key="user.id"
            :src="user.avatar"
            :alt="user.name"
            class="ring-2 ring-background"
        />
    </div>
</template>
```

---

## Alert

### Variantes

-   `default` (neutro)
-   `destructive` (erro)
-   `success` (sucesso)
-   `warning` (aviso)

### Exemplos

```vue
<template>
    <!-- Mensagem de sucesso -->
    <Alert variant="success">
        <div class="flex items-center gap-2">
            <Icon icon="mdi:check-circle" class="w-5 h-5" />
            <span>Ticket criado com sucesso!</span>
        </div>
    </Alert>

    <!-- Erro -->
    <Alert variant="destructive">
        <div class="flex items-center gap-2">
            <Icon icon="mdi:alert-circle" class="w-5 h-5" />
            <span>Erro ao criar ticket. Tente novamente.</span>
        </div>
    </Alert>

    <!-- Info -->
    <Alert>
        <p class="font-medium">Atenção</p>
        <p class="text-sm">
            Este ticket será atribuído automaticamente à equipa de suporte.
        </p>
    </Alert>
</template>
```

---

## Form Completo (Exemplo Real)

```vue
<script setup>
import { useForm } from "@inertiajs/vue3";
import {
    Button,
    Input,
    Textarea,
    Select,
    Label,
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    CardFooter,
    Alert,
} from "@/components/ui";

const props = defineProps({
    teams: Array,
    success: String,
    error: String,
});

const form = useForm({
    title: "",
    description: "",
    priority: "medium",
    team_id: null,
});

const submit = () => {
    form.post(route("tickets.store"), {
        onSuccess: () => form.reset(),
    });
};
</script>

<template>
    <div class="max-w-2xl mx-auto p-6">
        <!-- Mensagens de feedback -->
        <Alert v-if="success" variant="success" class="mb-4">
            {{ success }}
        </Alert>

        <Alert v-if="error" variant="destructive" class="mb-4">
            {{ error }}
        </Alert>

        <!-- Formulário -->
        <Card>
            <CardHeader>
                <CardTitle>Criar Novo Ticket</CardTitle>
            </CardHeader>

            <form @submit.prevent="submit">
                <CardContent class="space-y-4">
                    <!-- Título -->
                    <div>
                        <Label for="title" required>Título</Label>
                        <Input
                            id="title"
                            v-model="form.title"
                            :error="!!form.errors.title"
                            placeholder="Descreva brevemente o problema"
                        />
                        <p
                            v-if="form.errors.title"
                            class="text-sm text-destructive mt-1"
                        >
                            {{ form.errors.title }}
                        </p>
                    </div>

                    <!-- Descrição -->
                    <div>
                        <Label for="description" required>Descrição</Label>
                        <Textarea
                            id="description"
                            v-model="form.description"
                            :rows="6"
                            :error="!!form.errors.description"
                            placeholder="Explique o problema em detalhe"
                        />
                        <p
                            v-if="form.errors.description"
                            class="text-sm text-destructive mt-1"
                        >
                            {{ form.errors.description }}
                        </p>
                    </div>

                    <!-- Prioridade -->
                    <div>
                        <Label for="priority">Prioridade</Label>
                        <Select id="priority" v-model="form.priority">
                            <option value="low">Baixa</option>
                            <option value="medium">Média</option>
                            <option value="high">Alta</option>
                            <option value="urgent">Urgente</option>
                        </Select>
                    </div>

                    <!-- Equipa -->
                    <div v-if="teams?.length">
                        <Label for="team">Equipa</Label>
                        <Select id="team" v-model="form.team_id">
                            <option :value="null">
                                Atribuir automaticamente
                            </option>
                            <option
                                v-for="team in teams"
                                :key="team.id"
                                :value="team.id"
                            >
                                {{ team.name }}
                            </option>
                        </Select>
                    </div>
                </CardContent>

                <CardFooter class="gap-2">
                    <Button type="submit" :disabled="form.processing">
                        {{ form.processing ? "A criar..." : "Criar Ticket" }}
                    </Button>
                    <Button
                        type="button"
                        variant="outline"
                        @click="$inertia.visit(route('tickets.index'))"
                    >
                        Cancelar
                    </Button>
                </CardFooter>
            </form>
        </Card>
    </div>
</template>
```

---

## Dark Mode

Todos os componentes suportam dark mode automaticamente via CSS variables. Para alternar:

```vue
<script setup>
import { ref, onMounted } from "vue";

const isDark = ref(false);

const toggleTheme = () => {
    isDark.value = !isDark.value;
    document.documentElement.classList.toggle("dark");
};

onMounted(() => {
    // Verificar preferência do sistema
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        isDark.value = true;
        document.documentElement.classList.add("dark");
    }
});
</script>

<template>
    <Button @click="toggleTheme"> {{ isDark ? "☀" : "🌙" }} Tema </Button>
</template>
```

---

## Customização

### Alterar Cores do Tema

Editar `resources/css/app.css`:

```css
@layer base {
    :root {
        --primary: 220 90% 56%; /* Azul mais vibrante */
        --destructive: 0 84% 60%; /* Vermelho */
    }
}
```

### Criar Variantes Personalizadas

Exemplo: Button com variante "info":

```vue
<script setup>
// Em Button.vue, adicionar ao objeto variants:
const variants = {
    // ... variantes existentes
    info: "bg-blue-500 text-white shadow hover:bg-blue-600",
};
</script>
```

---

## Próximos Componentes (Roadmap)

### Sprint 2 (Tickets)

-   **Dialog.vue** - Modals
-   **DropdownMenu.vue** - Menus contextuais
-   **Table.vue** - Data tables
-   **Pagination.vue** - Navegação de páginas
-   **Toast.vue** - Notificações temporárias

### Sprint 3 (Colaboração)

-   **Tabs.vue** - Navegação em tabs
-   **Accordion.vue** - FAQ colapsáveis
-   **Command.vue** - Search palette (Cmd+K)
-   **Popover.vue** - Tooltips avançados

### Sprint 4 (Knowledge Base)

-   **Breadcrumb.vue** - Navegação hierárquica
-   **Separator.vue** - Divisores visuais
-   **ScrollArea.vue** - Scroll customizado

---

## Features Implementadas

### Design System

-   CSS Variables para cores (light + dark mode)
-   Tailwind CSS com `cn()` helper (merge classes sem conflitos)
-   Class Variance Authority (CVA) para variantes type-safe
-   Responsive design (mobile-first)

### Acessibilidade

-   ARIA attributes
-   Focus states (ring)
-   Disabled states
-   Error states (borda vermelha)

### Developer Experience

-   Props tipados e validados
-   v-model support
-   Eventos customizados
-   Slots para flexibilidade
-   JSConfig aliases (`@/components/ui`)

---

## Checklist de Implementação

-   14 componentes base criados
-   Utils helper (`cn()`)
-   Index.js para barrel exports
-   Página de demo funcional
-   Rota `/components-demo` criada
-   Dark mode suportado
-   Mobile responsive
-   Acessibilidade básica
-   Documentação completa

---

**Última Atualização:** 08 Novembro 2025, 01:05
