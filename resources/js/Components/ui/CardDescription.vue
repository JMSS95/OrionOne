<script setup>
import { cn } from "@/lib/utils";

defineProps({
    class: {
        type: String,
        default: "",
    },
});
</script>

<template>
    <div :class="cn('text-sm text-muted-foreground', $props.class)">
        <slot />
    </div>
</template>
