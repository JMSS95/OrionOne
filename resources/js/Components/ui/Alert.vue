<script setup>
import { cn } from "@/lib/utils";
import { computed } from "vue";

const props = defineProps({
    variant: {
        type: String,
        default: "default",
        validator: (value) =>
            ["default", "destructive", "success", "warning"].includes(value),
    },
});

const alertClasses = computed(() => {
    const baseClasses = "relative w-full rounded-lg border px-4 py-3 text-sm";

    const variants = {
        default: "bg-background text-foreground",
        destructive:
            "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
        success:
            "border-green-500/50 text-green-700 bg-green-50 dark:bg-green-950 [&>svg]:text-green-700",
        warning:
            "border-yellow-500/50 text-yellow-700 bg-yellow-50 dark:bg-yellow-950 [&>svg]:text-yellow-700",
    };

    return cn(baseClasses, variants[props.variant]);
});
</script>

<template>
    <div :class="alertClasses" role="alert">
        <slot />
    </div>
</template>
