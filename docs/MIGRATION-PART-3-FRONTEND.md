# 🚀 Migração Next.js + Nest.js - PARTE 3: Frontend Migration

**Deadline:** Fim de Janeiro 2025 (10 semanas)
**Foco:** Conversão Vue 3 + Inertia → Next.js 15 App Router com máxima velocidade

---

## 📊 NEXT.JS 15 STACK COMPLETO

### Strategy: App Router + React Server Components

**Vue 3 + Inertia (atual):** Client-side rendering com SSR bridge
**Next.js 15 (novo):** Server Components + Client Islands = Performance máxima

---

### Frontend Dependencies

```bash
# Core Next.js
npm install next@latest react@latest react-dom@latest

# TypeScript
npm install -D typescript @types/react @types/node

# Styling (REUTILIZAR)
npm install tailwindcss@latest postcss autoprefixer
npm install tailwindcss-animate
npm install class-variance-authority clsx tailwind-merge

# UI Components (Shadcn-ui React)
npx shadcn@latest init
npx shadcn@latest add button input label select textarea dialog toast dropdown-menu avatar badge card

# Forms & Validation
npm install react-hook-form @hookform/resolvers zod

# State Management
npm install zustand @tanstack/react-query axios

# Rich Text (REUTILIZAR Tiptap!)
npm install @tiptap/react @tiptap/starter-kit @tiptap/extension-placeholder

# Charts (MELHOR que Chart.js para React)
npm install recharts

# Utilities (REUTILIZAR)
npm install date-fns lucide-react

# Development
npm install -D @types/node @types/react @types/react-dom
```

---

## 🏗️ NEXT.JS PROJECT STRUCTURE

```
next-frontend/
├── app/
│   ├── (auth)/                    # Auth layout group
│   │   ├── layout.tsx             # Auth-specific layout
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   │
│   ├── (dashboard)/               # Dashboard layout group
│   │   ├── layout.tsx             # Dashboard layout (sidebar, header)
│   │   │
│   │   ├── page.tsx               # /dashboard (home)
│   │   │
│   │   ├── tickets/
│   │   │   ├── page.tsx           # /tickets (list)
│   │   │   ├── [id]/
│   │   │   │   ├── page.tsx       # /tickets/[id] (detail)
│   │   │   │   └── edit/
│   │   │   │       └── page.tsx   # /tickets/[id]/edit
│   │   │   └── create/
│   │   │       └── page.tsx       # /tickets/create
│   │   │
│   │   ├── knowledge-base/
│   │   │   ├── page.tsx           # /knowledge-base (articles list)
│   │   │   ├── [slug]/
│   │   │   │   └── page.tsx       # /knowledge-base/[slug]
│   │   │   └── create/
│   │   │       └── page.tsx
│   │   │
│   │   ├── teams/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── assets/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── reports/
│   │   │   └── page.tsx
│   │   │
│   │   └── profile/
│   │       └── page.tsx
│   │
│   ├── api/                       # API Routes (optional, proxy to Nest.js)
│   │   └── [...proxy]/
│   │       └── route.ts
│   │
│   ├── layout.tsx                 # Root layout
│   ├── page.tsx                   # / (landing page)
│   ├── globals.css                # Global styles
│   └── error.tsx                  # Error boundary
│
├── components/
│   ├── ui/                        # Shadcn-ui components (auto-generated)
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   ├── select.tsx
│   │   ├── textarea.tsx
│   │   ├── toast.tsx
│   │   ├── avatar.tsx
│   │   ├── badge.tsx
│   │   └── ...
│   │
│   ├── layout/
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   ├── footer.tsx
│   │   └── theme-provider.tsx
│   │
│   ├── tickets/
│   │   ├── ticket-card.tsx
│   │   ├── ticket-list.tsx
│   │   ├── ticket-form.tsx
│   │   ├── ticket-filters.tsx
│   │   ├── ticket-status-badge.tsx
│   │   └── ticket-priority-badge.tsx
│   │
│   ├── comments/
│   │   ├── comment-list.tsx
│   │   ├── comment-form.tsx
│   │   └── comment-item.tsx
│   │
│   ├── kb/
│   │   ├── article-card.tsx
│   │   ├── article-editor.tsx    # Tiptap integration
│   │   └── category-tree.tsx
│   │
│   └── charts/
│       ├── tickets-by-status.tsx
│       ├── sla-compliance.tsx
│       └── agent-performance.tsx
│
├── lib/
│   ├── api-client.ts              # Axios instance
│   ├── auth.ts                    # JWT handling
│   ├── utils.ts                   # cn() helper
│   ├── validations.ts             # Zod schemas
│   └── constants.ts
│
├── hooks/
│   ├── use-tickets.ts             # React Query hooks
│   ├── use-auth.ts
│   ├── use-toast.ts
│   └── use-debounce.ts
│
├── store/
│   ├── auth-store.ts              # Zustand stores
│   └── ui-store.ts
│
├── types/
│   ├── api.ts                     # API response types
│   ├── ticket.ts
│   ├── user.ts
│   └── index.ts
│
├── public/
│   ├── images/
│   └── favicon.ico
│
├── .env.local
├── .env.example
├── next.config.mjs
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## 🚀 CÓDIGO-BASE ESSENCIAL

### 1. API Client (Axios + Interceptors)

```typescript
// lib/api-client.ts
import axios from "axios";

const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001",
    headers: {
        "Content-Type": "application/json",
    },
});

// Request interceptor (add JWT token)
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response interceptor (handle 401)
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

export default apiClient;
```

---

### 2. Auth Store (Zustand)

```typescript
// store/auth-store.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";
import apiClient from "@/lib/api-client";

interface User {
    id: string;
    name: string;
    email: string;
    avatar?: string;
    role: "ADMIN" | "AGENT" | "USER";
}

interface AuthState {
    user: User | null;
    accessToken: string | null;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    updateProfile: (data: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            accessToken: null,
            isAuthenticated: false,

            login: async (email, password) => {
                const response = await apiClient.post("/auth/login", {
                    email,
                    password,
                });
                const { access_token, user } = response.data;

                localStorage.setItem("access_token", access_token);
                set({ user, accessToken: access_token, isAuthenticated: true });
            },

            logout: () => {
                localStorage.removeItem("access_token");
                set({ user: null, accessToken: null, isAuthenticated: false });
            },

            updateProfile: (data) => {
                set((state) => ({
                    user: state.user ? { ...state.user, ...data } : null,
                }));
            },
        }),
        {
            name: "auth-storage",
        }
    )
);
```

---

### 3. React Query Hooks (Tickets)

```typescript
// hooks/use-tickets.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import {
    Ticket,
    CreateTicketDto,
    UpdateTicketDto,
    FilterTicketDto,
} from "@/types";
import { toast } from "@/hooks/use-toast";

export function useTickets(filters?: FilterTicketDto) {
    return useQuery({
        queryKey: ["tickets", filters],
        queryFn: async () => {
            const response = await apiClient.get("/tickets", {
                params: filters,
            });
            return response.data;
        },
    });
}

export function useTicket(id: string) {
    return useQuery({
        queryKey: ["tickets", id],
        queryFn: async () => {
            const response = await apiClient.get(`/tickets/${id}`);
            return response.data;
        },
        enabled: !!id,
    });
}

export function useCreateTicket() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (data: CreateTicketDto) => {
            const response = await apiClient.post("/tickets", data);
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["tickets"] });
            toast({
                title: "Success",
                description: "Ticket created successfully",
            });
        },
        onError: (error: any) => {
            toast({
                title: "Error",
                description:
                    error.response?.data?.message || "Failed to create ticket",
                variant: "destructive",
            });
        },
    });
}

export function useUpdateTicket(id: string) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (data: UpdateTicketDto) => {
            const response = await apiClient.patch(`/tickets/${id}`, data);
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["tickets", id] });
            queryClient.invalidateQueries({ queryKey: ["tickets"] });
            toast({
                title: "Success",
                description: "Ticket updated successfully",
            });
        },
    });
}

export function useAssignTicket(id: string) {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (assigneeId: string) => {
            const response = await apiClient.post(`/tickets/${id}/assign`, {
                assigneeId,
            });
            return response.data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["tickets", id] });
            toast({
                title: "Success",
                description: "Ticket assigned successfully",
            });
        },
    });
}
```

---

### 4. Ticket Form (React Hook Form + Zod)

```typescript
// app/(dashboard)/tickets/create/page.tsx
"use client";

import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useCreateTicket } from "@/hooks/use-tickets";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { TiptapEditor } from "@/components/tiptap-editor";

const createTicketSchema = z.object({
    title: z.string().min(5, "Title must be at least 5 characters").max(200),
    description: z
        .string()
        .min(10, "Description must be at least 10 characters"),
    priority: z.enum(["LOW", "MEDIUM", "HIGH", "URGENT"]),
    categoryId: z.string().uuid().optional(),
});

type CreateTicketForm = z.infer<typeof createTicketSchema>;

export default function CreateTicketPage() {
    const router = useRouter();
    const createTicket = useCreateTicket();

    const form = useForm<CreateTicketForm>({
        resolver: zodResolver(createTicketSchema),
        defaultValues: {
            title: "",
            description: "",
            priority: "MEDIUM",
        },
    });

    const onSubmit = async (data: CreateTicketForm) => {
        await createTicket.mutateAsync(data);
        router.push("/tickets");
    };

    return (
        <div className="container max-w-4xl py-8">
            <h1 className="text-3xl font-bold mb-8">Create New Ticket</h1>

            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                {/* Title */}
                <div>
                    <label className="block text-sm font-medium mb-2">
                        Title
                    </label>
                    <Input
                        {...form.register("title")}
                        placeholder="Brief description of the issue"
                    />
                    {form.formState.errors.title && (
                        <p className="text-sm text-red-500 mt-1">
                            {form.formState.errors.title.message}
                        </p>
                    )}
                </div>

                {/* Priority */}
                <div>
                    <label className="block text-sm font-medium mb-2">
                        Priority
                    </label>
                    <Select {...form.register("priority")}>
                        <option value="LOW">Low</option>
                        <option value="MEDIUM">Medium</option>
                        <option value="HIGH">High</option>
                        <option value="URGENT">Urgent</option>
                    </Select>
                </div>

                {/* Description (Tiptap) */}
                <div>
                    <label className="block text-sm font-medium mb-2">
                        Description
                    </label>
                    <TiptapEditor
                        content={form.watch("description")}
                        onChange={(content) =>
                            form.setValue("description", content)
                        }
                    />
                    {form.formState.errors.description && (
                        <p className="text-sm text-red-500 mt-1">
                            {form.formState.errors.description.message}
                        </p>
                    )}
                </div>

                {/* Submit */}
                <div className="flex gap-4">
                    <Button type="submit" disabled={createTicket.isPending}>
                        {createTicket.isPending
                            ? "Creating..."
                            : "Create Ticket"}
                    </Button>
                    <Button
                        type="button"
                        variant="outline"
                        onClick={() => router.back()}
                    >
                        Cancel
                    </Button>
                </div>
            </form>
        </div>
    );
}
```

---

### 5. Tickets List (Server Component + Filters)

```typescript
// app/(dashboard)/tickets/page.tsx
import { Suspense } from "react";
import { TicketsList } from "@/components/tickets/tickets-list";
import { TicketsFilters } from "@/components/tickets/tickets-filters";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function TicketsPage({
    searchParams,
}: {
    searchParams: { status?: string; priority?: string; search?: string };
}) {
    return (
        <div className="container py-8">
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold">Tickets</h1>
                <Link href="/tickets/create">
                    <Button>Create Ticket</Button>
                </Link>
            </div>

            <TicketsFilters />

            <Suspense fallback={<div>Loading tickets...</div>}>
                <TicketsList filters={searchParams} />
            </Suspense>
        </div>
    );
}

// components/tickets/tickets-list.tsx
("use client");

import { useTickets } from "@/hooks/use-tickets";
import { TicketCard } from "./ticket-card";
import { Loader2 } from "lucide-react";

export function TicketsList({ filters }: { filters: any }) {
    const { data, isLoading } = useTickets(filters);

    if (isLoading) {
        return (
            <div className="flex justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin" />
            </div>
        );
    }

    if (!data?.data?.length) {
        return (
            <div className="text-center py-12 text-muted-foreground">
                No tickets found
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {data.data.map((ticket: any) => (
                <TicketCard key={ticket.id} ticket={ticket} />
            ))}
        </div>
    );
}

// components/tickets/ticket-card.tsx
import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar } from "@/components/ui/avatar";
import { formatDistanceToNow } from "date-fns";

export function TicketCard({ ticket }: { ticket: any }) {
    return (
        <Link href={`/tickets/${ticket.id}`}>
            <Card className="p-6 hover:shadow-lg transition-shadow cursor-pointer">
                <div className="flex items-start justify-between">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                            <span className="text-sm text-muted-foreground font-mono">
                                {ticket.ticketNumber}
                            </span>
                            <Badge variant={getStatusVariant(ticket.status)}>
                                {ticket.status}
                            </Badge>
                            <Badge
                                variant={getPriorityVariant(ticket.priority)}
                            >
                                {ticket.priority}
                            </Badge>
                        </div>

                        <h3 className="text-lg font-semibold mb-2">
                            {ticket.title}
                        </h3>

                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <div className="flex items-center gap-2">
                                <Avatar className="h-6 w-6">
                                    <img
                                        src={
                                            ticket.requester.avatar ||
                                            "/default-avatar.png"
                                        }
                                    />
                                </Avatar>
                                <span>{ticket.requester.name}</span>
                            </div>

                            {ticket.assignee && (
                                <div className="flex items-center gap-2">
                                    <span>→</span>
                                    <Avatar className="h-6 w-6">
                                        <img
                                            src={
                                                ticket.assignee.avatar ||
                                                "/default-avatar.png"
                                            }
                                        />
                                    </Avatar>
                                    <span>{ticket.assignee.name}</span>
                                </div>
                            )}

                            <span>·</span>
                            <span>
                                {formatDistanceToNow(
                                    new Date(ticket.createdAt)
                                )}{" "}
                                ago
                            </span>

                            {ticket._count?.comments > 0 && (
                                <>
                                    <span>·</span>
                                    <span>
                                        {ticket._count.comments} comments
                                    </span>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </Card>
        </Link>
    );
}

function getStatusVariant(status: string) {
    const variants: Record<string, any> = {
        OPEN: "default",
        IN_PROGRESS: "secondary",
        RESOLVED: "success",
        CLOSED: "outline",
    };
    return variants[status] || "default";
}

function getPriorityVariant(priority: string) {
    const variants: Record<string, any> = {
        LOW: "outline",
        MEDIUM: "secondary",
        HIGH: "warning",
        URGENT: "destructive",
    };
    return variants[priority] || "default";
}
```

---

### 6. Tiptap Editor Component (REUTILIZAR Vue config)

```typescript
// components/tiptap-editor.tsx
"use client";

import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import { Button } from "./ui/button";
import { Bold, Italic, List, ListOrdered, Heading2 } from "lucide-react";

interface TiptapEditorProps {
    content: string;
    onChange: (content: string) => void;
    placeholder?: string;
}

export function TiptapEditor({
    content,
    onChange,
    placeholder,
}: TiptapEditorProps) {
    const editor = useEditor({
        extensions: [
            StarterKit,
            Placeholder.configure({
                placeholder: placeholder || "Write your description here...",
            }),
        ],
        content,
        onUpdate: ({ editor }) => {
            onChange(editor.getHTML());
        },
    });

    if (!editor) return null;

    return (
        <div className="border rounded-lg">
            {/* Toolbar */}
            <div className="border-b p-2 flex gap-1">
                <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => editor.chain().focus().toggleBold().run()}
                    className={editor.isActive("bold") ? "bg-muted" : ""}
                >
                    <Bold className="h-4 w-4" />
                </Button>
                <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() => editor.chain().focus().toggleItalic().run()}
                    className={editor.isActive("italic") ? "bg-muted" : ""}
                >
                    <Italic className="h-4 w-4" />
                </Button>
                <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() =>
                        editor.chain().focus().toggleHeading({ level: 2 }).run()
                    }
                    className={
                        editor.isActive("heading", { level: 2 })
                            ? "bg-muted"
                            : ""
                    }
                >
                    <Heading2 className="h-4 w-4" />
                </Button>
                <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() =>
                        editor.chain().focus().toggleBulletList().run()
                    }
                    className={editor.isActive("bulletList") ? "bg-muted" : ""}
                >
                    <List className="h-4 w-4" />
                </Button>
                <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    onClick={() =>
                        editor.chain().focus().toggleOrderedList().run()
                    }
                    className={editor.isActive("orderedList") ? "bg-muted" : ""}
                >
                    <ListOrdered className="h-4 w-4" />
                </Button>
            </div>

            {/* Editor */}
            <EditorContent
                editor={editor}
                className="prose prose-sm max-w-none p-4"
            />
        </div>
    );
}
```

---

### 7. Dashboard Layout (Sidebar + Header)

```typescript
// app/(dashboard)/layout.tsx
import { Sidebar } from "@/components/layout/sidebar";
import { Header } from "@/components/layout/header";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col overflow-hidden">
                <Header />
                <main className="flex-1 overflow-y-auto bg-muted/10">
                    {children}
                </main>
            </div>
        </div>
    );
}

// components/layout/sidebar.tsx
("use client");

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Home, Ticket, Book, Users, Package, BarChart3 } from "lucide-react";

const routes = [
    { href: "/dashboard", label: "Dashboard", icon: Home },
    { href: "/tickets", label: "Tickets", icon: Ticket },
    { href: "/knowledge-base", label: "Knowledge Base", icon: Book },
    { href: "/teams", label: "Teams", icon: Users },
    { href: "/assets", label: "Assets", icon: Package },
    { href: "/reports", label: "Reports", icon: BarChart3 },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="w-64 bg-card border-r">
            <div className="p-6">
                <h2 className="text-2xl font-bold">OrionOne</h2>
            </div>

            <nav className="px-3 space-y-1">
                {routes.map((route) => {
                    const Icon = route.icon;
                    const isActive = pathname.startsWith(route.href);

                    return (
                        <Link
                            key={route.href}
                            href={route.href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                                isActive
                                    ? "bg-primary text-primary-foreground"
                                    : "text-muted-foreground hover:bg-muted"
                            )}
                        >
                            <Icon className="h-5 w-5" />
                            {route.label}
                        </Link>
                    );
                })}
            </nav>
        </aside>
    );
}
```

---

## 📦 RESUMO FRONTEND

**Conversão Vue → React:**

-   **Inertia.js** → **React Server Components** (melhor SSR)
-   **VeeValidate** → **React Hook Form + Zod** (type-safe)
-   **Shadcn-vue** → **Shadcn-ui** (mesma API, mesma aparência)
-   **Chart.js** → **Recharts** (melhor integração React)
-   **Tiptap Vue** → **Tiptap React** (mesma configuração!)

**Arquivos a criar:** ~60 componentes React
**Linhas de código:** ~6000
**Ganhos:**

-   ✅ Type-safety total (TypeScript)
-   ✅ React Query caching automático
-   ✅ Server Components (performance)
-   ✅ File-based routing (zero config)

---

**Continua em:** `MIGRATION-PART-4-TIMELINE.md`
