<script setup>
import {
    Alert,
    Avatar,
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
    Input,
    Label,
    Select,
    Textarea,
} from "@/components/ui";
import { Head } from "@inertiajs/vue3";

const user = {
    name: "João Santos",
    email: "joao@orionone.test",
    avatar: null,
};

const tickets = [
    {
        id: 1,
        number: "TK-20251108-0001",
        title: "Laptop não liga",
        status: "open",
        priority: "high",
    },
    {
        id: 2,
        number: "TK-20251108-0002",
        title: "Erro no sistema",
        status: "in_progress",
        priority: "urgent",
    },
    {
        id: 3,
        number: "TK-20251108-0003",
        title: "Dúvida sobre feature",
        status: "resolved",
        priority: "low",
    },
];

const statusVariants = {
    open: "default",
    in_progress: "warning",
    resolved: "success",
    closed: "secondary",
};

const priorityVariants = {
    low: "secondary",
    medium: "default",
    high: "warning",
    urgent: "destructive",
};
</script>

<template>
    <Head title="Componentes Demo" />

    <div class="min-h-screen bg-background p-8">
        <div class="max-w-6xl mx-auto space-y-8">
            <!-- Header -->
            <div class="space-y-2">
                <h1 class="text-4xl font-bold">Componentes UI Demo</h1>
                <p class="text-muted-foreground">
                    Todos os componentes Shadcn-vue criados e funcionais
                </p>
            </div>

            <!-- Alerts -->
            <section>
                <h2 class="text-2xl font-semibold mb-4">Alerts</h2>
                <div class="space-y-2">
                    <Alert variant="success"
                        >✅ Ticket criado com sucesso!</Alert
                    >
                    <Alert variant="destructive"
                        >❌ Erro ao processar pedido</Alert
                    >
                    <Alert variant="warning"
                        >⚠️ Atenção: Este ticket será atribuído
                        automaticamente</Alert
                    >
                    <Alert>ℹ️ Informação: Sistema atualizado</Alert>
                </div>
            </section>

            <!-- Buttons -->
            <section>
                <h2 class="text-2xl font-semibold mb-4">Buttons</h2>
                <div class="flex flex-wrap gap-2">
                    <Button>Default</Button>
                    <Button variant="destructive">Destructive</Button>
                    <Button variant="outline">Outline</Button>
                    <Button variant="secondary">Secondary</Button>
                    <Button variant="ghost">Ghost</Button>
                    <Button variant="link">Link</Button>
                    <Button size="sm">Small</Button>
                    <Button size="lg">Large</Button>
                    <Button :disabled="true">Disabled</Button>
                </div>
            </section>

            <!-- Badges -->
            <section>
                <h2 class="text-2xl font-semibold mb-4">Badges</h2>
                <div class="flex flex-wrap gap-2">
                    <Badge>Default</Badge>
                    <Badge variant="secondary">Secondary</Badge>
                    <Badge variant="destructive">Destructive</Badge>
                    <Badge variant="outline">Outline</Badge>
                    <Badge variant="success">Success</Badge>
                    <Badge variant="warning">Warning</Badge>
                </div>
            </section>

            <!-- Avatars -->
            <section>
                <h2 class="text-2xl font-semibold mb-4">Avatars</h2>
                <div class="flex items-center gap-4">
                    <Avatar size="sm" :alt="user.name" fallback="JS" />
                    <Avatar size="md" :alt="user.name" fallback="JS" />
                    <Avatar size="lg" :alt="user.name" fallback="JS" />
                    <Avatar size="xl" :alt="user.name" fallback="JS" />
                </div>
            </section>

            <!-- Form Components -->
            <section>
                <h2 class="text-2xl font-semibold mb-4">Form Components</h2>
                <Card>
                    <CardHeader>
                        <CardTitle>Exemplo de Formulário</CardTitle>
                        <CardDescription
                            >Todos os inputs estilizados</CardDescription
                        >
                    </CardHeader>
                    <CardContent class="space-y-4">
                        <div>
                            <Label for="name" required>Nome</Label>
                            <Input id="name" placeholder="João Santos" />
                        </div>

                        <div>
                            <Label for="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="joao@exemplo.com"
                            />
                        </div>

                        <div>
                            <Label for="description">Descrição</Label>
                            <Textarea
                                id="description"
                                placeholder="Escreva aqui..."
                                :rows="3"
                            />
                        </div>

                        <div>
                            <Label for="priority">Prioridade</Label>
                            <Select id="priority">
                                <option value="low">Baixa</option>
                                <option value="medium">Média</option>
                                <option value="high">Alta</option>
                                <option value="urgent">Urgente</option>
                            </Select>
                        </div>
                    </CardContent>
                    <CardFooter class="gap-2">
                        <Button>Submeter</Button>
                        <Button variant="outline">Cancelar</Button>
                    </CardFooter>
                </Card>
            </section>

            <!-- Ticket Cards -->
            <section>
                <h2 class="text-2xl font-semibold mb-4">Ticket Cards</h2>
                <div class="grid gap-4 md:grid-cols-3">
                    <Card
                        v-for="ticket in tickets"
                        :key="ticket.id"
                        class="cursor-pointer hover:shadow-lg transition"
                    >
                        <CardContent class="pt-6">
                            <div class="space-y-2">
                                <div class="flex items-center justify-between">
                                    <span
                                        class="text-xs text-muted-foreground font-mono"
                                    >
                                        {{ ticket.number }}
                                    </span>
                                    <Badge
                                        :variant="statusVariants[ticket.status]"
                                    >
                                        {{ ticket.status }}
                                    </Badge>
                                </div>

                                <h3 class="font-medium">{{ ticket.title }}</h3>

                                <div class="flex items-center gap-2">
                                    <Badge
                                        :variant="
                                            priorityVariants[ticket.priority]
                                        "
                                        class="text-xs"
                                    >
                                        {{ ticket.priority }}
                                    </Badge>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </section>

            <!-- Dark Mode Toggle -->
            <section>
                <h2 class="text-2xl font-semibold mb-4">Dark Mode</h2>
                <Card>
                    <CardContent class="pt-6">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="font-medium">Tema Escuro</p>
                                <p class="text-sm text-muted-foreground">
                                    Alternar entre modo claro e escuro
                                </p>
                            </div>
                            <Button
                                variant="outline"
                                @click="
                                    document.documentElement.classList.toggle(
                                        'dark'
                                    )
                                "
                            >
                                🌓 Alternar
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </section>
        </div>
    </div>
</template>
