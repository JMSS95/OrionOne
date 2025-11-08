<script setup>
import { cn } from "@/lib/utils";

defineProps({
    for: {
        type: String,
        default: "",
    },
    required: {
        type: Boolean,
        default: false,
    },
    class: {
        type: String,
        default: "",
    },
});
</script>

<template>
    <label
        :for="for"
        :class="
            cn(
                'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
                $props.class
            )
        "
    >
        <slot />
        <span v-if="required" class="text-destructive ml-1">*</span>
    </label>
</template>
