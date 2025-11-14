# shadcn/ui Components - Complete Guide

**Stack:** Next.js 15.5.6 + React 19.2.0 + shadcn/ui + Tailwind CSS v4
**Last Updated:** 13 November 2025
**Status:** SETUP READY - Components to be added

---

## Official Documentation

- **shadcn/ui Docs**: https://ui.shadcn.com/docs
- **Next.js Installation**: https://ui.shadcn.com/docs/installation/next
- **Components Reference**: https://ui.shadcn.com/docs/components
- **Themes**: https://ui.shadcn.com/themes
- **Examples**: https://ui.shadcn.com/examples

---

## Introduction

shadcn/ui is **NOT a component library**. It's a collection of re-usable components that you can copy and paste into your apps.

### Key Principles

1. **Copy & Paste** - Components live in your codebase
2. **Customizable** - You own the code, modify as needed
3. **Accessible** - Built on Radix UI primitives
4. **Styled with Tailwind** - Utility-first CSS framework
5. **Type-safe** - Written in TypeScript

### Why shadcn/ui?

 **Full Control** - Components are in your project, not node_modules
 **No Lock-in** - Modify components without library constraints
 **Tree-shakeable** - Only bundle what you use
 **Accessible** - Radix UI provides keyboard navigation, ARIA
 **Modern** - React Server Components compatible

---

## Project Configuration

### Current Setup

The project is already configured with shadcn/ui foundations:

**`components.json`** (Configuration File)

```json
{
 "$schema": "https://ui.shadcn.com/schema.json",
 "style": "new-york", // Design style (new-york or default)
 "rsc": true, // React Server Components
 "tsx": true, // TypeScript + JSX
 "tailwind": {
 "config": "",
 "css": "app/globals.css",
 "baseColor": "neutral", // Base color theme
 "cssVariables": true, // Use CSS variables
 "prefix": "" // No prefix for Tailwind classes
 },
 "iconLibrary": "lucide", // lucide-react icons
 "aliases": {
 "components": "@/components",
 "utils": "@/lib/utils",
 "ui": "@/components/ui",
 "lib": "@/lib",
 "hooks": "@/hooks"
 }
}
```

**Project Structure**

```
next-frontend/
 app/
 globals.css Tailwind + CSS Variables configured
 layout.tsx Root layout with font setup
 page.tsx Home page
 components/ TO CREATE - UI components folder
 ui/ TO CREATE - shadcn components
 lib/
 utils.ts cn() utility function
 hooks/ TO CREATE (optional) - Custom hooks
 components.json shadcn/ui configuration
```

### Dependencies Installed

**UI Dependencies** (Already in package.json)

```json
{
 "class-variance-authority": "^0.7.1", // CVA for variant styling
 "clsx": "^2.1.1", // Conditional classnames
 "tailwind-merge": "^3.4.0", // Merge Tailwind classes
 "lucide-react": "^0.553.0" // Icon library (14.1M downloads/week)
}
```

**Missing Dependencies** (To Install)

```bash
npm install @radix-ui/react-slot @radix-ui/react-avatar @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-label @radix-ui/react-popover @radix-ui/react-select @radix-ui/react-separator @radix-ui/react-switch @radix-ui/react-tabs @radix-ui/react-tooltip
```

---

## Installation & Setup

### Step 1: Initialize shadcn/ui (Already Done)

The project already has `components.json` configured. If starting fresh:

```bash
npx shadcn@latest init
```

### Step 2: Add Components

Add components one by one as needed:

```bash
# Essential components for ITSM
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add card
npx shadcn@latest add badge
npx shadcn@latest add avatar
npx shadcn@latest add alert
npx shadcn@latest add select
npx shadcn@latest add textarea
npx shadcn@latest add form
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add table
npx shadcn@latest add tabs
npx shadcn@latest add tooltip
npx shadcn@latest add separator
npx shadcn@latest add skeleton
npx shadcn@latest add switch
npx shadcn@latest add checkbox
npx shadcn@latest add radio-group
```

### Step 3: Create Folders (If Not Auto-Created)

```bash
mkdir -p components/ui
mkdir -p hooks
```

---

## Core Components for OrionOne ITSM

### Priority 1: Forms & Inputs (Authentication, Ticket Creation)

| Component | Purpose | Install Command |
| --------------- | -------------------------------------- | ----------------------------------- |
| **Button** | Actions, form submissions | `npx shadcn@latest add button` |
| **Input** | Text fields (email, title, etc) | `npx shadcn@latest add input` |
| **Label** | Form labels with accessibility | `npx shadcn@latest add label` |
| **Textarea** | Multi-line text (descriptions) | `npx shadcn@latest add textarea` |
| **Select** | Dropdowns (status, priority, category) | `npx shadcn@latest add select` |
| **Checkbox** | Multi-select, agreements | `npx shadcn@latest add checkbox` |
| **Radio Group** | Single choice options | `npx shadcn@latest add radio-group` |
| **Switch** | Toggle options (active/inactive) | `npx shadcn@latest add switch` |
| **Form** | React Hook Form integration | `npx shadcn@latest add form` |

### Priority 2: Layout & Display (Tickets, Dashboard)

| Component | Purpose | Install Command |
| ------------- | ---------------------------- | --------------------------------- |
| **Card** | Ticket cards, info panels | `npx shadcn@latest add card` |
| **Badge** | Status badges (OPEN, CLOSED) | `npx shadcn@latest add badge` |
| **Avatar** | User avatars | `npx shadcn@latest add avatar` |
| **Alert** | Success/error messages | `npx shadcn@latest add alert` |
| **Table** | Ticket list, reports | `npx shadcn@latest add table` |
| **Tabs** | Dashboard sections | `npx shadcn@latest add tabs` |
| **Separator** | Visual dividers | `npx shadcn@latest add separator` |
| **Skeleton** | Loading placeholders | `npx shadcn@latest add skeleton` |

### Priority 3: Interactions (Modals, Menus)

| Component | Purpose | Install Command |
| ----------------- | -------------------------------------- | ------------------------------------- |
| **Dialog** | Modals (create ticket, confirm delete) | `npx shadcn@latest add dialog` |
| **Dropdown Menu** | User menu, actions menu | `npx shadcn@latest add dropdown-menu` |
| **Popover** | Context info, filters | `npx shadcn@latest add popover` |
| **Tooltip** | Help text on hover | `npx shadcn@latest add tooltip` |
| **Command** | Command palette (search) | `npx shadcn@latest add command` |
| **Sheet** | Side panels (filters, settings) | `npx shadcn@latest add sheet` |

### Priority 4: Advanced (Dashboard, Analytics)

| Component | Purpose | Install Command |
| -------------- | ------------------------- | ---------------------------------- |
| **Chart** | Analytics charts | `npx shadcn@latest add chart` |
| **Calendar** | Date picker (deadlines) | `npx shadcn@latest add calendar` |
| **Carousel** | Image galleries | `npx shadcn@latest add carousel` |
| **Accordion** | FAQ, collapsible sections | `npx shadcn@latest add accordion` |
| **Breadcrumb** | Navigation trail | `npx shadcn@latest add breadcrumb` |
| **Pagination** | Table pagination | `npx shadcn@latest add pagination` |

---

## Usage Examples

### Button Component

**Basic Usage**

```tsx
import { Button } from "@/components/ui/button";

export default function LoginPage() {
 return <Button>Sign In</Button>;
}
```

**All Variants**

```tsx
<Button variant="default">Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Cancel</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link Button</Button>
```

**All Sizes**

```tsx
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon">
 <TrashIcon />
</Button>
```

**With Icons (Lucide React)**

```tsx
import { Button } from "@/components/ui/button"
import { PlusCircle, Trash2, Download } from "lucide-react"

<Button>
 <PlusCircle className="mr-2 h-4 w-4" />
 Create Ticket
</Button>

<Button variant="destructive" size="sm">
 <Trash2 className="mr-2 h-4 w-4" />
 Delete
</Button>

<Button variant="outline">
 <Download className="mr-2 h-4 w-4" />
 Export
</Button>
```

---

### Input Component

**Basic Input**

```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

<div className="space-y-2">
 <Label htmlFor="email">Email</Label>
 <Input id="email" type="email" placeholder="you@example.com" />
</div>;
```

**With React Hook Form + Zod**

```tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

const loginSchema = z.object({
 email: z.string().email("Invalid email address"),
 password: z.string().min(8, "Password must be at least 8 characters"),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function LoginForm() {
 const {
 register,
 handleSubmit,
 formState: { errors },
 } = useForm<LoginForm>({
 resolver: zodResolver(loginSchema),
 });

 const onSubmit = (data: LoginForm) => {
 console.log(data);
 };

 return (
 <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
 <div className="space-y-2">
 <Label htmlFor="email">Email</Label>
 <Input id="email" type="email" {...register("email")} />
 {errors.email && (
 <p className="text-sm text-destructive">
 {errors.email.message}
 </p>
 )}
 </div>

 <div className="space-y-2">
 <Label htmlFor="password">Password</Label>
 <Input
 id="password"
 type="password"
 {...register("password")}
 />
 {errors.password && (
 <p className="text-sm text-destructive">
 {errors.password.message}
 </p>
 )}
 </div>

 <Button type="submit" className="w-full">
 Sign In
 </Button>
 </form>
 );
}
```

---

### Card Component

**Ticket Card Example**

```tsx
import {
 Card,
 CardContent,
 CardDescription,
 CardFooter,
 CardHeader,
 CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function TicketCard({ ticket }) {
 return (
 <Card>
 <CardHeader>
 <div className="flex items-center justify-between">
 <CardTitle className="text-lg">#{ticket.number}</CardTitle>
 <Badge
 variant={
 ticket.status === "OPEN" ? "default" : "secondary"
 }
 >
 {ticket.status}
 </Badge>
 </div>
 <CardDescription>{ticket.title}</CardDescription>
 </CardHeader>

 <CardContent>
 <p className="text-sm text-muted-foreground line-clamp-2">
 {ticket.description}
 </p>

 <div className="mt-4 flex items-center gap-2">
 <Avatar className="h-6 w-6">
 <AvatarImage src={ticket.assignee?.avatar} />
 <AvatarFallback>
 {ticket.assignee?.initials}
 </AvatarFallback>
 </Avatar>
 <span className="text-sm">{ticket.assignee?.name}</span>
 </div>
 </CardContent>

 <CardFooter className="gap-2">
 <Button variant="outline" size="sm">
 View
 </Button>
 <Button size="sm">Assign</Button>
 </CardFooter>
 </Card>
 );
}
```

---

### Form Component (with shadcn Form)

**Complete Form with Validation**

```tsx
"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";

import { Button } from "@/components/ui/button";
import {
 Form,
 FormControl,
 FormDescription,
 FormField,
 FormItem,
 FormLabel,
 FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
 Select,
 SelectContent,
 SelectItem,
 SelectTrigger,
 SelectValue,
} from "@/components/ui/select";

const ticketSchema = z.object({
 title: z.string().min(5, "Title must be at least 5 characters"),
 description: z
 .string()
 .min(20, "Description must be at least 20 characters"),
 priority: z.enum(["LOW", "MEDIUM", "HIGH", "URGENT"]),
 category: z.string().min(1, "Please select a category"),
});

export function CreateTicketForm() {
 const form = useForm<z.infer<typeof ticketSchema>>({
 resolver: zodResolver(ticketSchema),
 defaultValues: {
 title: "",
 description: "",
 priority: "MEDIUM",
 category: "",
 },
 });

 function onSubmit(values: z.infer<typeof ticketSchema>) {
 console.log(values);
 // Submit to API
 }

 return (
 <Form {...form}>
 <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
 <FormField
 control={form.control}
 name="title"
 render={({ field }) => (
 <FormItem>
 <FormLabel>Title</FormLabel>
 <FormControl>
 <Input
 placeholder="Brief description of the issue"
 {...field}
 />
 </FormControl>
 <FormDescription>
 A clear, concise title for your ticket.
 </FormDescription>
 <FormMessage />
 </FormItem>
 )}
 />

 <FormField
 control={form.control}
 name="description"
 render={({ field }) => (
 <FormItem>
 <FormLabel>Description</FormLabel>
 <FormControl>
 <Textarea
 placeholder="Detailed description of the issue"
 className="min-h-[120px]"
 {...field}
 />
 </FormControl>
 <FormMessage />
 </FormItem>
 )}
 />

 <FormField
 control={form.control}
 name="priority"
 render={({ field }) => (
 <FormItem>
 <FormLabel>Priority</FormLabel>
 <Select
 onValueChange={field.onChange}
 defaultValue={field.value}
 >
 <FormControl>
 <SelectTrigger>
 <SelectValue placeholder="Select priority" />
 </SelectTrigger>
 </FormControl>
 <SelectContent>
 <SelectItem value="LOW">Low</SelectItem>
 <SelectItem value="MEDIUM">
 Medium
 </SelectItem>
 <SelectItem value="HIGH">High</SelectItem>
 <SelectItem value="URGENT">
 Urgent
 </SelectItem>
 </SelectContent>
 </Select>
 <FormMessage />
 </FormItem>
 )}
 />

 <FormField
 control={form.control}
 name="category"
 render={({ field }) => (
 <FormItem>
 <FormLabel>Category</FormLabel>
 <Select
 onValueChange={field.onChange}
 defaultValue={field.value}
 >
 <FormControl>
 <SelectTrigger>
 <SelectValue placeholder="Select category" />
 </SelectTrigger>
 </FormControl>
 <SelectContent>
 <SelectItem value="hardware">
 Hardware
 </SelectItem>
 <SelectItem value="software">
 Software
 </SelectItem>
 <SelectItem value="network">
 Network
 </SelectItem>
 <SelectItem value="access">
 Access
 </SelectItem>
 <SelectItem value="other">Other</SelectItem>
 </SelectContent>
 </Select>
 <FormMessage />
 </FormItem>
 )}
 />

 <Button type="submit">Create Ticket</Button>
 </form>
 </Form>
 );
}
```

---

### Dialog Component (Modal)

**Confirmation Dialog**

```tsx
import {
 Dialog,
 DialogContent,
 DialogDescription,
 DialogFooter,
 DialogHeader,
 DialogTitle,
 DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";

export function DeleteTicketDialog({ ticketId }) {
 const handleDelete = async () => {
 // Delete ticket logic
 console.log("Deleting ticket:", ticketId);
 };

 return (
 <Dialog>
 <DialogTrigger asChild>
 <Button variant="destructive" size="sm">
 <Trash2 className="mr-2 h-4 w-4" />
 Delete
 </Button>
 </DialogTrigger>
 <DialogContent>
 <DialogHeader>
 <DialogTitle>Are you absolutely sure?</DialogTitle>
 <DialogDescription>
 This action cannot be undone. This will permanently
 delete the ticket and remove all associated data.
 </DialogDescription>
 </DialogHeader>
 <DialogFooter>
 <Button variant="outline">Cancel</Button>
 <Button variant="destructive" onClick={handleDelete}>
 Delete Ticket
 </Button>
 </DialogFooter>
 </DialogContent>
 </Dialog>
 );
}
```

---

### Badge Component

**Status Badges for Tickets**

```tsx
import { Badge } from "@/components/ui/badge";

export function TicketStatusBadge({ status }) {
 const variants = {
 OPEN: "default",
 IN_PROGRESS: "secondary",
 PENDING: "outline",
 RESOLVED: "default",
 CLOSED: "secondary",
 CANCELLED: "destructive",
 };

 return (
 <Badge variant={variants[status] || "default"}>
 {status.replace("_", " ")}
 </Badge>
 );
}

// Priority Badges
export function PriorityBadge({ priority }) {
 const styles = {
 LOW: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
 MEDIUM: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
 HIGH: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200",
 URGENT: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
 };

 return <Badge className={styles[priority]}>{priority}</Badge>;
}
```

---

### Table Component

**Tickets Table**

```tsx
import {
 Table,
 TableBody,
 TableCaption,
 TableCell,
 TableHead,
 TableHeader,
 TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function TicketsTable({ tickets }) {
 return (
 <Table>
 <TableCaption>A list of recent tickets.</TableCaption>
 <TableHeader>
 <TableRow>
 <TableHead>Ticket</TableHead>
 <TableHead>Title</TableHead>
 <TableHead>Status</TableHead>
 <TableHead>Priority</TableHead>
 <TableHead>Assignee</TableHead>
 <TableHead>Created</TableHead>
 </TableRow>
 </TableHeader>
 <TableBody>
 {tickets.map((ticket) => (
 <TableRow key={ticket.id}>
 <TableCell className="font-medium">
 #{ticket.number}
 </TableCell>
 <TableCell>{ticket.title}</TableCell>
 <TableCell>
 <Badge variant="outline">{ticket.status}</Badge>
 </TableCell>
 <TableCell>
 <Badge>{ticket.priority}</Badge>
 </TableCell>
 <TableCell>
 <div className="flex items-center gap-2">
 <Avatar className="h-6 w-6">
 <AvatarImage
 src={ticket.assignee?.avatar}
 />
 <AvatarFallback>
 {ticket.assignee?.initials}
 </AvatarFallback>
 </Avatar>
 <span className="text-sm">
 {ticket.assignee?.name}
 </span>
 </div>
 </TableCell>
 <TableCell>
 {new Date(ticket.createdAt).toLocaleDateString()}
 </TableCell>
 </TableRow>
 ))}
 </TableBody>
 </Table>
 );
}
```

---

## Theming & Customization

### CSS Variables (Already Configured)

The project uses CSS variables for theming. All colors are defined in `app/globals.css`:

```css
:root {
 --radius: 0.625rem;
 --background: oklch(1 0 0);
 --foreground: oklch(0.145 0 0);
 --card: oklch(1 0 0);
 --card-foreground: oklch(0.145 0 0);
 --popover: oklch(1 0 0);
 --popover-foreground: oklch(0.145 0 0);
 --primary: oklch(0.266 0 0);
 --primary-foreground: oklch(0.984 0 0);
 --secondary: oklch(0.961 0 0);
 --secondary-foreground: oklch(0.145 0 0);
 /* ... more colors */
}

.dark {
 --background: oklch(0.117 0 0);
 --foreground: oklch(0.984 0 0);
 /* ... dark mode colors */
}
```

### Customize Colors

Edit `app/globals.css` to change theme colors. Use the **shadcn/ui Themes** tool:

- https://ui.shadcn.com/themes

### Customize Components

Since components are in your codebase, you can modify them directly:

```bash
# Edit button component
code components/ui/button.tsx

# Add custom variant
# Edit the buttonVariants object
```

---

## Utility Functions

### `cn()` Helper (Already Available)

Located in `lib/utils.ts`:

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
 return twMerge(clsx(inputs));
}
```

**Usage:**

```tsx
import { cn } from "@/lib/utils";

// Merge classes conditionally
<div
 className={cn(
 "base-classes",
 isActive && "active-classes",
 isPending && "pending-classes"
 )}
/>;
```

---

## Responsive Design

All shadcn/ui components are responsive by default. Use Tailwind breakpoints:

```tsx
<Button className="w-full md:w-auto">
 Responsive Button
</Button>

<Card className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
 {/* Responsive grid */}
</Card>
```

**Tailwind Breakpoints:**

- `sm` - 640px
- `md` - 768px
- `lg` - 1024px
- `xl` - 1280px
- `2xl` - 1536px

---

## Accessibility

shadcn/ui components are built on **Radix UI** primitives which provide:

 **Keyboard Navigation** - Full keyboard support
 **ARIA Attributes** - Proper ARIA labels and roles
 **Focus Management** - Focus trap in modals, focus visible states
 **Screen Reader Support** - Semantic HTML and ARIA live regions

### Best Practices

```tsx
// Always use Label with Input
<Label htmlFor="email">Email</Label>
<Input id="email" type="email" />

// Use aria-label for icon-only buttons
<Button size="icon" aria-label="Delete ticket">
 <Trash2 />
</Button>

// Provide descriptions for complex forms
<FormDescription>
 This will permanently delete your account.
</FormDescription>
```

---

## Testing Components

### Unit Testing (Jest + React Testing Library)

```tsx
import { render, screen } from "@testing-library/react";
import { Button } from "@/components/ui/button";

describe("Button", () => {
 it("renders with text", () => {
 render(<Button>Click me</Button>);
 expect(screen.getByText("Click me")).toBeInTheDocument();
 });

 it("handles click events", () => {
 const handleClick = jest.fn();
 render(<Button onClick={handleClick}>Click me</Button>);
 screen.getByText("Click me").click();
 expect(handleClick).toHaveBeenCalledTimes(1);
 });
});
```

---

## Implementation Checklist for OrionOne ITSM

### Phase 1: Authentication & Basic UI

- [ ] Install core components: `button`, `input`, `label`, `card`, `alert`
- [ ] Create login form with Zod validation
- [ ] Create register form
- [ ] Add loading skeletons
- [ ] Test authentication flow

### Phase 2: Ticket Management

- [ ] Install: `textarea`, `select`, `badge`, `avatar`, `form`
- [ ] Create ticket form
- [ ] Create ticket card component
- [ ] Create ticket list/table
- [ ] Add status badges
- [ ] Add priority badges

### Phase 3: Advanced Features

- [ ] Install: `dialog`, `dropdown-menu`, `tabs`, `tooltip`
- [ ] Create ticket detail modal
- [ ] Add user dropdown menu
- [ ] Create dashboard with tabs
- [ ] Add tooltips for help text

### Phase 4: Data Display

- [ ] Install: `table`, `pagination`, `chart`
- [ ] Create tickets table
- [ ] Add pagination
- [ ] Create analytics charts
- [ ] Add export functionality

### Phase 5: Polish

- [ ] Install: `skeleton`, `separator`, `breadcrumb`
- [ ] Add loading states everywhere
- [ ] Add visual separators
- [ ] Create navigation breadcrumbs
- [ ] Add dark mode toggle

---

## Additional Resources

### Official Links

- **Documentation**: https://ui.shadcn.com/docs
- **GitHub**: https://github.com/shadcn-ui/ui
- **Discord**: https://discord.com/invite/W3nubBd7qy
- **Twitter**: https://twitter.com/shadcn

### Community Resources

- **Component Directory**: https://ui.shadcn.com/docs/directory
- **Examples**: https://ui.shadcn.com/examples
- **Blocks**: https://ui.shadcn.com/blocks

### Related Documentation

- **Radix UI**: https://www.radix-ui.com/primitives/docs/overview/introduction
- **Tailwind CSS**: https://tailwindcss.com/docs
- **React Hook Form**: https://react-hook-form.com/
- **Zod**: https://zod.dev/

---

## Next Steps

1. **Install Priority 1 Components** (Forms)

 ```bash
 npx shadcn@latest add button input label textarea select form
 ```

2. **Create First Form** (Login)

 - Use React Hook Form + Zod
 - Test validation
 - Test submission

3. **Install Priority 2 Components** (Layout)

 ```bash
 npx shadcn@latest add card badge avatar alert table
 ```

4. **Build Ticket Components**

 - TicketCard
 - TicketList
 - CreateTicketForm
 - TicketTable

5. **Add Interactions**
 ```bash
 npx shadcn@latest add dialog dropdown-menu tabs tooltip
 ```

---

**Last Updated:** 13 November 2025
**Maintained by:** OrionOne Development Team
**Framework:** Next.js 15.5.6 + React 19.2.0 + shadcn/ui + Tailwind CSS v4
