# Tech Deep Dive - Frontend (Vue.js/Inertia/Tailwind)

Guia Completo: Como funciona o frontend do OrionOne - Vue 3, Inertia.js, Tailwind CSS, Shadcn-vue

---

## 1. VUE.JS 3 (Framework JavaScript Reativo)

### O que é Vue.js?

**Vue.js** é um framework JavaScript progressivo para construir interfaces de utilizador (UI). A palavra-chave aqui é "reativo" - significa que quando os dados mudam, a interface atualiza-se automaticamente sem precisares de escrever código manual de manipulação do DOM.

**Analogia:** Pensa em Vue como uma "folha de cálculo do Excel" para web:

-   Quando mudas um valor numa célula (dados)
-   Todas as fórmulas que dependem dessa célula atualizam automaticamente (UI)
-   Não precisas de recalcular manualmente

### Porque Vue 3 (não React ou Angular)?

**Decisão Técnica para o OrionOne:**

1. **Curva de Aprendizagem Suave**

    - Sintaxe próxima de HTML/CSS/JavaScript puro
    - Menos conceitos abstratos que React (JSX, Hooks complexos)
    - Documentação em português disponível

2. **Performance Nativa**

    - Virtual DOM otimizado (renderização seletiva)
    - Compiler hints para otimização automática
    - Bundle size menor que Angular (~30KB vs ~150KB)

3. **Composition API**

    - Organização lógica de código (não por tipo de função)
    - Reutilização fácil via composables
    - TypeScript opcional (não obrigatório como Angular)

4. **Ecossistema Maduro**

    - Inertia.js para integração com Laravel
    - Pinia para state management
    - VueUse para utilities
    - Shadcn-vue para componentes

5. **Integração com Inertia.js**
    - Vue é a escolha primária do Inertia
    - Documentação e exemplos focados em Vue
    - Comunidade maior Vue+Laravel

### Como Funciona a Reatividade?

**O Problema da Manipulação Manual do DOM:**

#### Sem Vue - JavaScript Vanilla (Manual e Trabalhoso)

```html
<div id="counter">
    <p>Contagem: <span id="count">0</span></p>
    <button onclick="increment()">+1</button>
</div>

<script>
    // Estado da aplicação (apenas uma variável JavaScript)
    let count = 0;

    function increment() {
        // 1. Atualizar o estado (JavaScript)
        count++;

        // 2. MANUALMENTE atualizar o DOM (HTML)
        // Problema: Tens que LEMBRAR de fazer isto SEMPRE que count muda!
        document.getElementById("count").textContent = count;

        // 3. Se esqueceres este passo, o HTML fica desatualizado
        // Aplicação fica "fora de sincronização"
    }

    // Imagina ter 50 lugares onde count é mostrado...
    // Terias que atualizar TODOS manualmente!
    // Código fica cheio de: document.getElementById(), querySelector(), etc
</script>
```

**Problemas desta Abordagem:**

1. **Verboso:** Muito código repetitivo para atualizar UI
2. **Propenso a Erros:** Fácil esquecer de atualizar algum elemento
3. **Difícil de Manter:** Lógica misturada com manipulação DOM
4. **Performance:** Atualizar DOM é lento, não há otimização

#### Com Vue 3 - Reatividade Automática

```vue
<template>
    <!-- Template: HTML com sintaxe Vue -->
    <div>
        <!-- {{ }} = Interpolação - mostra valor de count -->
        <!-- Vue observa count automaticamente -->
        <p>Contagem: {{ count }}</p>

        <!-- @click = Event listener do Vue (equivale a onclick) -->
        <!-- increment é chamado quando botão é clicado -->
        <button @click="increment">+1</button>
    </div>
</template>

<script setup>
// setup = Composition API (Vue 3)
// Código executa quando componente é criado
import { ref } from "vue";

// ref() = Cria variável REATIVA
// Vue "observa" esta variável e detecta mudanças
const count = ref(0); // count.value = 0

function increment() {
    // Quando count.value muda...
    count.value++;

    // Vue AUTOMATICAMENTE:
    // 1. Detecta que count mudou
    // 2. Re-renderiza APENAS o <p> que usa count
    // 3. Atualiza o DOM de forma otimizada

    // TU não precisas de fazer NADA!
    // Sem document.getElementById, sem querySelector, sem nada!
}

// Se count fosse usado em 50 lugares no template,
// TODOS seriam atualizados automaticamente!
</script>

<style scoped>
/* scoped = CSS só afeta este componente */
/* Não vaza para outros componentes */
button {
    padding: 0.5rem 1rem;
    background: blue;
    color: white;
}
</style>
```

**Como Vue Detecta Mudanças? (Proxy ES6)**

```javascript
// Por trás dos panos, Vue usa Proxy do JavaScript ES6
const count = ref(0);

// Vue transforma ref() em algo assim:
const count = new Proxy(
    { value: 0 },
    {
        get(target, property) {
            // Quando LERES count.value
            // Vue regista: "Este componente depende de count"
            console.log("Alguém leu count.value");
            return target[property];
        },
        set(target, property, newValue) {
            // Quando ESCREVERES count.value = X
            // Vue sabe: "count mudou! Re-renderizar componentes que usam count"
            console.log("count.value mudou para:", newValue);
            target[property] = newValue;

            // Vue dispara re-render
            updateComponent();
            return true;
        },
    }
);

// Por isso precisas de .value:
count.value++; // Proxy intercepta e dispara re-render
count++; // ERRO! count é um Proxy, não um número
```

**Vantagens da Reatividade Vue:**

1. **Menos Código:** Não precisas de manipular DOM manualmente
2. **Mais Confiável:** Impossível esquecer de atualizar UI
3. **Performance:** Vue atualiza apenas o necessário (diff algorithm)
4. **Debugging:** Vue DevTools mostra estado reativo em tempo real
5. **Composição:** Lógica reativa pode ser reutilizada (composables)

---

### Composition API (Vue 3)

#### O que é?

Forma moderna de organizar código Vue. Substitui Options API (Vue 2).

#### Exemplo Real no OrionOne:

```vue
<!-- resources/js/Pages/Tickets/Index.vue -->
<template>
    <div>
        <!-- Filtros -->
        <div class="filters">
            <select v-model="filters.status">
                <option value="">Todos</option>
                <option value="open">Abertos</option>
                <option value="closed">Fechados</option>
            </select>
        </div>

        <!-- Lista de tickets -->
        <div v-for="ticket in tickets.data" :key="ticket.id">
            <h3>{{ ticket.title }}</h3>
            <p>{{ ticket.description }}</p>
            <span :class="priorityClass(ticket.priority)">
                {{ ticket.priority }}
            </span>
        </div>

        <!-- Paginação -->
        <Pagination :links="tickets.links" />
    </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { router } from "@inertiajs/vue3";

// Props vindas do Laravel (Inertia.js)
const props = defineProps({
    tickets: Object,
    filters: Object,
});

// Estado local (reativo)
const filters = ref({
    status: props.filters.status || "",
    priority: props.filters.priority || "",
});

// Computed (calculado automaticamente)
const hasFilters = computed(() => {
    return filters.value.status || filters.value.priority;
});

// Watch (observa mudanças)
watch(
    filters,
    (newFilters) => {
        // Quando filtros mudam, recarrega dados via Inertia
        router.get("/tickets", newFilters, {
            preserveState: true,
            preserveScroll: true,
        });
    },
    { deep: true }
);

// Funções
function priorityClass(priority) {
    const classes = {
        low: "bg-gray-200 text-gray-800",
        medium: "bg-yellow-200 text-yellow-800",
        high: "bg-orange-200 text-orange-800",
        urgent: "bg-red-200 text-red-800",
    };
    return classes[priority];
}
</script>
```

### Conceitos Vue 3 Usados no OrionOne:

#### 1. **Reatividade (ref, reactive)**

```js
import { ref, reactive } from "vue";

// ref: para valores primitivos
const count = ref(0);
count.value++; // Acesso via .value

// reactive: para objetos
const form = reactive({
    title: "",
    description: "",
    priority: "medium",
});
form.title = "Novo título"; // Sem .value
```

#### 2. **Computed Properties** (valores calculados)

```js
const fullName = computed(() => {
    return `${user.firstName} ${user.lastName}`;
});

// Atualiza automaticamente quando user.firstName ou user.lastName mudam!
```

#### 3. **Watchers** (observadores)

```js
watch(searchQuery, (newValue, oldValue) => {
    console.log(`Pesquisa mudou de "${oldValue}" para "${newValue}"`);

    // Debounce (espera 300ms antes de pesquisar)
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        fetchResults(newValue);
    }, 300);
});
```

#### 4. **Lifecycle Hooks** (ciclo de vida)

```js
import { onMounted, onUnmounted } from "vue";

onMounted(() => {
    // Executado quando componente é criado
    console.log("Componente montado!");
    fetchData();
});

onUnmounted(() => {
    // Executado quando componente é destruído
    console.log("Componente desmontado!");
    cleanupEventListeners();
});
```

---

## 2. INERTIA.JS (Monolith SPA)

### O que é?

**Inertia.js** liga Laravel (backend) com Vue.js (frontend) SEM precisar de API REST.

### Problema que Resolve:

#### Arquitetura Tradicional (Separada)

```
Backend (Laravel)                Frontend (Vue SPA)
   ↓                                    ↓
API REST (/api/tickets)           fetch('/api/tickets')
   ↓                                    ↓
JSON response                      Render Vue
```

**Problemas:**

-   Duplicação de validação (backend + frontend)
-   CORS headaches
-   Autenticação complexa (tokens)
-   SEO difícil

#### Inertia.js (Híbrido - Best of Both Worlds)

```
Laravel Controller                Vue Component
   ↓                                    ↓
Inertia::render('Tickets/Index')  <template>...
   ↓                                    ↓
JSON (via X-Inertia header)       Render Vue
```

**Vantagens:**

-   **Sem API**: Laravel chama Vue diretamente
-   **Routing Laravel**: `route('tickets.index')`
-   **Validação Laravel**: Form Requests
    ✅ **Autenticação Laravel**: `auth()` funciona
    ✅ **SEO**: Server-side rendering possível

### Como Funciona?

#### Backend (Laravel Controller)

```php
// app/Http/Controllers/TicketController.php
use Inertia\Inertia;

class TicketController extends Controller
{
    public function index()
    {
        $tickets = Ticket::with('user', 'team')
            ->latest()
            ->paginate(20);

        return Inertia::render('Tickets/Index', [
            'tickets' => $tickets,
            'filters' => request()->only(['status', 'priority']),
        ]);
    }
}
```

#### Frontend (Vue Component)

```vue
<!-- resources/js/Pages/Tickets/Index.vue -->
<template>
    <div>
        <h1>Tickets</h1>
        <!-- tickets e filters estão disponíveis automaticamente! -->
        <div v-for="ticket in tickets.data" :key="ticket.id">
            {{ ticket.title }}
        </div>
    </div>
</template>

<script setup>
// Props vindas do Laravel (Inertia injeta automaticamente)
defineProps({
    tickets: Object,
    filters: Object,
});
</script>
```

### Features Principais do Inertia:

#### 1. **Navigation (SPA-style)**

```vue
<template>
    <!-- Link SPA (não recarrega página!) -->
    <Link href="/tickets/create">Novo Ticket</Link>

    <!-- Formulário Inertia -->
    <form @submit.prevent="submit">
        <input v-model="form.title" />
        <button type="submit">Criar</button>
    </form>
</template>

<script setup>
import { useForm } from "@inertiajs/vue3";

const form = useForm({
    title: "",
    description: "",
});

function submit() {
    form.post("/tickets", {
        onSuccess: () => {
            // Sucesso!
            form.reset();
        },
        onError: (errors) => {
            // Laravel retornou erros de validação
            console.log(errors); // { title: ['O título é obrigatório'] }
        },
    });
}
</script>
```

#### 2. **Partial Reloads** (Performance)

```js
// Recarrega APENAS a prop 'tickets', não a página inteira
router.reload({ only: ["tickets"] });

// Preserva scroll durante navegação
router.get(
    "/tickets?page=2",
    {},
    {
        preserveScroll: true,
    }
);
```

#### 3. **Shared Data** (Props Globais)

```php
// app/Http/Middleware/HandleInertiaRequests.php
public function share(Request $request): array
{
    return [
        ...parent::share($request),

        // Disponível em TODOS os componentes Vue
        'auth' => [
            'user' => $request->user(),
        ],
        'flash' => [
            'success' => $request->session()->get('success'),
            'error' => $request->session()->get('error'),
        ],
    ];
}
```

```vue
<!-- Qualquer componente pode acessar -->
<template>
    <div v-if="$page.props.auth.user">
        Olá, {{ $page.props.auth.user.name }}!
    </div>

    <div v-if="$page.props.flash.success" class="alert">
        {{ $page.props.flash.success }}
    </div>
</template>
```

#### 4. **File Uploads**

```vue
<template>
    <form @submit.prevent="submit">
        <input type="file" @input="form.avatar = $event.target.files[0]" />
        <button type="submit">Upload</button>
    </form>
</template>

<script setup>
import { useForm } from "@inertiajs/vue3";

const form = useForm({
    avatar: null,
});

function submit() {
    form.post("/profile/avatar", {
        forceFormData: true, // Envia como multipart/form-data
    });
}
</script>
```

---

## 3. TAILWIND CSS (Utility-First CSS)

### O que é?

Framework CSS com **classes utilitárias**. Em vez de escrever CSS custom, usas classes predefinidas.

### Filosofia:

#### CSS Tradicional (Escrever classes custom)

```css
/* styles.css */
.button {
    padding: 0.5rem 1rem;
    background-color: #3b82f6;
    color: white;
    border-radius: 0.375rem;
    font-weight: 600;
}

.button:hover {
    background-color: #2563eb;
}
```

```html
<button class="button">Clica aqui</button>
```

#### Tailwind CSS (Utility classes)

```html
<button
    class="px-4 py-2 bg-blue-500 text-white rounded-md font-semibold hover:bg-blue-600"
>
    Clica aqui
</button>
```

**Vantagens:**
✅ **Sem naming debates**: "Como chamar esta classe?"
✅ **Sem CSS não usado**: Purge automático
✅ **Responsive**: `md:text-lg lg:text-xl`
✅ **Dark mode**: `dark:bg-gray-800`
✅ **Consistência**: Design system integrado

### Tailwind no OrionOne:

#### **Spacing (Espaçamento)**

```html
<!-- Padding -->
<div class="p-4">
    <!-- padding: 1rem (all) -->
    <div class="px-6 py-3">
        <!-- padding-x: 1.5rem, padding-y: 0.75rem -->
        <div class="pt-2">
            <!-- padding-top: 0.5rem -->

            <!-- Margin -->
            <div class="m-4">
                <!-- margin: 1rem (all) -->
                <div class="mt-8">
                    <!-- margin-top: 2rem -->
                    <div class="-ml-2">
                        <!-- margin-left: -0.5rem (negativo) -->

                        <!-- Gap (Flexbox/Grid) -->
                        <div class="flex gap-4">
                            <!-- gap entre items: 1rem -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

#### **Cores**

```html
<!-- Background -->
<div class="bg-blue-500">
    <!-- Azul médio -->
    <div class="bg-gray-100">
        <!-- Cinza claro -->
        <div class="bg-red-600">
            <!-- Vermelho escuro -->

            <!-- Text -->
            <p class="text-gray-700"><!-- Texto cinza escuro --></p>
            <p class="text-green-500">
                <!-- Texto verde -->

                <!-- Border -->
            </p>

            <div class="border border-gray-300"><!-- Borda cinza --></div>
        </div>
    </div>
</div>
```

#### **Layout**

```html
<!-- Flexbox -->
<div class="flex items-center justify-between">
    <!-- Flex com items centrados verticalmente e espaçados -->
</div>

<!-- Grid -->
<div class="grid grid-cols-3 gap-4">
    <!-- Grid com 3 colunas e gap de 1rem -->
</div>

<!-- Width/Height -->
<div class="w-full h-64">
    <!-- width: 100%, height: 16rem -->
    <div class="max-w-4xl mx-auto"><!-- max-width + centered --></div>
</div>
```

#### **Responsive Design**

```html
<!-- Mobile-first: sm, md, lg, xl, 2xl -->
<div class="text-sm md:text-base lg:text-lg">
    <!-- text-sm no mobile -->
    <!-- text-base em tablets (768px+) -->
    <!-- text-lg em desktops (1024px+) -->
</div>

<div class="hidden md:block">
    <!-- Escondido no mobile, visível em tablets+ -->
</div>
```

#### **States (hover, focus, active)**

```html
<button
    class="bg-blue-500 hover:bg-blue-600 focus:ring-2 focus:ring-blue-300 active:bg-blue-700"
>
    Hover me!
</button>
```

#### **Dark Mode**

```html
<div class="bg-white dark:bg-gray-900 text-black dark:text-white">
    <!-- Branco em light mode, cinza escuro em dark mode -->
</div>
```

### Tailwind Config no OrionOne:

```js
// tailwind.config.js
export default {
    content: [
        "./resources/**/*.blade.php",
        "./resources/**/*.js",
        "./resources/**/*.vue",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: "#f0f9ff",
                    500: "#0ea5e9",
                    900: "#0c4a6e",
                },
            },
            fontFamily: {
                sans: ["Inter", "sans-serif"],
            },
        },
    },
    plugins: [],
};
```

---

## 4. SHADCN-VUE (Componentes UI)

### O que é?

**Coleção de componentes UI** baseados em Radix Vue + Tailwind CSS. **NÃO é uma biblioteca instalada**, são ficheiros copiados para o teu projeto.

### Filosofia: "Copy & Paste"

```bash
# Instalar CLI
npx shadcn-vue@latest init

# Adicionar componente Button
npx shadcn-vue@latest add button

# Ficheiro criado em:
# resources/js/Components/ui/button/Button.vue
```

### Vantagens:

✅ **Ownership**: Tu és dono do código (não dependência)
✅ **Customizável**: Edita livremente
✅ **Type-safe**: TypeScript completo
✅ **Accessible**: ARIA completo (a11y)
✅ **Tailwind-first**: Estilização fácil

### Componentes Usados no OrionOne:

#### 1. **Button**

```vue
<template>
    <Button>Click me</Button>
    <Button variant="destructive">Delete</Button>
    <Button variant="outline">Cancel</Button>
    <Button size="sm">Small</Button>
    <Button size="lg">Large</Button>
</template>

<script setup>
import { Button } from "@/Components/ui/button";
</script>
```

#### 2. **Input**

```vue
<template>
    <Input v-model="form.email" type="email" placeholder="email@example.com" />
</template>

<script setup>
import { Input } from "@/Components/ui/input";
</script>
```

#### 3. **Select**

```vue
<template>
    <Select v-model="form.priority">
        <SelectTrigger>
            <SelectValue placeholder="Seleciona prioridade" />
        </SelectTrigger>
        <SelectContent>
            <SelectItem value="low">Baixa</SelectItem>
            <SelectItem value="medium">Média</SelectItem>
            <SelectItem value="high">Alta</SelectItem>
            <SelectItem value="urgent">Urgente</SelectItem>
        </SelectContent>
    </Select>
</template>

<script setup>
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/Components/ui/select";
</script>
```

#### 4. **Dialog (Modal)**

```vue
<template>
    <Dialog v-model:open="isOpen">
        <DialogTrigger as-child>
            <Button>Abrir Modal</Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Confirmar Ação</DialogTitle>
                <DialogDescription>
                    Tens a certeza que queres apagar este ticket?
                </DialogDescription>
            </DialogHeader>
            <DialogFooter>
                <Button variant="outline" @click="isOpen = false"
                    >Cancelar</Button
                >
                <Button variant="destructive" @click="deleteTicket"
                    >Apagar</Button
                >
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { ref } from "vue";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/Components/ui/dialog";
import { Button } from "@/Components/ui/button";

const isOpen = ref(false);

function deleteTicket() {
    // Lógica de apagar
    isOpen.value = false;
}
</script>
```

#### 5. **Table**

```vue
<template>
    <Table>
        <TableHeader>
            <TableRow>
                <TableHead>#</TableHead>
                <TableHead>Título</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Ações</TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            <TableRow v-for="ticket in tickets" :key="ticket.id">
                <TableCell>{{ ticket.ticket_number }}</TableCell>
                <TableCell>{{ ticket.title }}</TableCell>
                <TableCell>
                    <Badge :variant="statusVariant(ticket.status)">
                        {{ ticket.status }}
                    </Badge>
                </TableCell>
                <TableCell>
                    <Button size="sm">Ver</Button>
                </TableCell>
            </TableRow>
        </TableBody>
    </Table>
</template>

<script setup>
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/Components/ui/table";
import { Badge } from "@/Components/ui/badge";
import { Button } from "@/Components/ui/button";

defineProps({
    tickets: Array,
});

function statusVariant(status) {
    const variants = {
        open: "default",
        in_progress: "secondary",
        resolved: "success",
        closed: "outline",
    };
    return variants[status];
}
</script>
```

#### 6. **Toast (Notificações)**

```vue
<template>
    <Button @click="showToast">Show Toast</Button>
</template>

<script setup>
import { useToast } from "@/Components/ui/toast";
import { Button } from "@/Components/ui/button";

const { toast } = useToast();

function showToast() {
    toast({
        title: "Ticket criado!",
        description: "O ticket #TKT-000123 foi criado com sucesso.",
        variant: "success",
    });
}
</script>
```

---

## 5. VITE (Build Tool)

### O que é?

**Vite** é o build tool moderno que compila o frontend. Substitui Webpack (mais lento).

### Porque Vite?

✅ **Dev Server instantâneo**: < 1 segundo para iniciar
✅ **Hot Module Replacement (HMR)**: Mudanças aparecem sem refresh
✅ **Build otimizado**: Code splitting automático
✅ **ES Modules**: Usa import/export nativos

### Como Funciona?

#### Desenvolvimento:

```bash
npm run dev
# Inicia server em http://localhost:5173
# Mudanças em .vue aparecem INSTANTANEAMENTE (HMR)
```

#### Produção:

```bash
npm run build
# Compila, minifica, code split
# Output em public/build/
```

### Vite Config no OrionOne:

```js
// vite.config.js
import { defineConfig } from "vite";
import laravel from "laravel-vite-plugin";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
    plugins: [
        laravel({
            input: ["resources/css/app.css", "resources/js/app.js"],
            refresh: true,
        }),
        vue({
            template: {
                transformAssetUrls: {
                    base: null,
                    includeAbsolute: false,
                },
            },
        }),
    ],
    resolve: {
        alias: {
            "@": "/resources/js", // Alias: import { Button } from '@/Components/ui/button'
        },
    },
});
```

---

## 6. COMPOSABLES (Lógica Reutilizável)

### O que são?

Funções Vue que encapsulam lógica reutilizável. Pensa neles como "hooks personalizados".

### Exemplo no OrionOne:

#### **useFilters.js** (Filtros URL)

```js
// resources/js/Composables/useFilters.js
import { ref, watch } from "vue";
import { router } from "@inertiajs/vue3";

export function useFilters(initialFilters = {}) {
    const filters = ref(initialFilters);

    watch(
        filters,
        (newFilters) => {
            router.get(route(route().current()), newFilters, {
                preserveState: true,
                preserveScroll: true,
                only: ["tickets"], // Partial reload
            });
        },
        { deep: true }
    );

    function clearFilters() {
        Object.keys(filters.value).forEach((key) => {
            filters.value[key] = "";
        });
    }

    return {
        filters,
        clearFilters,
    };
}
```

**Uso:**

```vue
<script setup>
import { useFilters } from "@/Composables/useFilters";

const props = defineProps({ tickets: Object, filters: Object });

const { filters, clearFilters } = useFilters(props.filters);
</script>
```

#### **useConfirm.js** (Confirmações)

```js
// resources/js/Composables/useConfirm.js
import { ref } from "vue";

export function useConfirm() {
    const isOpen = ref(false);
    const message = ref("");
    const callback = ref(null);

    function confirm(msg, onConfirm) {
        message.value = msg;
        callback.value = onConfirm;
        isOpen.value = true;
    }

    function handleConfirm() {
        if (callback.value) {
            callback.value();
        }
        isOpen.value = false;
    }

    function handleCancel() {
        isOpen.value = false;
    }

    return {
        isOpen,
        message,
        confirm,
        handleConfirm,
        handleCancel,
    };
}
```

**Uso:**

```vue
<template>
    <Button @click="deleteTicket">Apagar</Button>

    <ConfirmDialog
        v-model:open="isOpen"
        :message="message"
        @confirm="handleConfirm"
        @cancel="handleCancel"
    />
</template>

<script setup>
import { useConfirm } from "@/Composables/useConfirm";

const { isOpen, message, confirm, handleConfirm, handleCancel } = useConfirm();

function deleteTicket() {
    confirm("Tens a certeza que queres apagar este ticket?", () => {
        router.delete(`/tickets/${ticket.id}`);
    });
}
</script>
```

---

## RESUMO: Stack Frontend

| Tecnologia       | Propósito                            |
| ---------------- | ------------------------------------ |
| **Vue 3**        | Framework reativo (UI)               |
| **Inertia.js**   | Liga Laravel ↔ Vue (sem API)         |
| **Tailwind CSS** | Utility-first CSS framework          |
| **Shadcn-vue**   | Componentes UI (Button, Dialog, etc) |
| **Vite**         | Build tool (dev server + produção)   |
| **Composables**  | Lógica reutilizável                  |

---

## Fluxo Completo: Request → Response

```
1. Utilizador clica em "Criar Ticket"
   ↓
2. Vue emite event @click
   ↓
3. Inertia.js envia POST /tickets (AJAX)
   ↓
4. Laravel recebe request
   ↓
5. Validation (Form Request)
   ↓
6. CreateTicketAction cria ticket
   ↓
7. Inertia::render('Tickets/Show', ['ticket' => $ticket])
   ↓
8. Inertia envia JSON para Vue
   ↓
9. Vue renderiza Tickets/Show.vue
   ↓
10. Vite HMR atualiza página (se em dev)
```

---

## Próximos Guias

-   **[TECH-DEEP-DIVE-DATABASE.md](./TECH-DEEP-DIVE-DATABASE.md)** - PostgreSQL, Redis
-   **[TECH-DEEP-DIVE-DEVOPS.md](./TECH-DEEP-DIVE-DEVOPS.md)** - Docker, Nginx

---

**Dúvidas?** Lê a documentação oficial:

-   [Vue 3 Docs](https://vuejs.org)
-   [Inertia.js Docs](https://inertiajs.com)
-   [Tailwind CSS Docs](https://tailwindcss.com)
-   [Shadcn-vue Docs](https://www.shadcn-vue.com)
