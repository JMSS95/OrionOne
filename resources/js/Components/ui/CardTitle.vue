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
    <div
        :class="
            cn(
                'text-2xl font-semibold leading-none tracking-tight',
                $props.class
            )
        "
    >
        <slot />
    </div>
</template>
