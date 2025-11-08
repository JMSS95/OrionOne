<script setup>
import { cn } from "@/lib/utils";
import { computed } from "vue";

const props = defineProps({
    src: {
        type: String,
        default: "",
    },
    alt: {
        type: String,
        default: "Avatar",
    },
    fallback: {
        type: String,
        default: "",
    },
    size: {
        type: String,
        default: "md",
        validator: (value) => ["sm", "md", "lg", "xl"].includes(value),
    },
});

const sizeClasses = {
    sm: "h-8 w-8 text-xs",
    md: "h-10 w-10 text-sm",
    lg: "h-16 w-16 text-lg",
    xl: "h-24 w-24 text-2xl",
};

const avatarClasses = computed(() => {
    return cn(
        "relative flex shrink-0 overflow-hidden rounded-full",
        sizeClasses[props.size]
    );
});

const fallbackText = computed(() => {
    if (props.fallback) return props.fallback;
    if (props.alt) return props.alt.charAt(0).toUpperCase();
    return "?";
});
</script>

<template>
    <div :class="avatarClasses">
        <img
            v-if="src"
            :src="src"
            :alt="alt"
            class="aspect-square h-full w-full object-cover"
        />
        <div
            v-else
            class="flex h-full w-full items-center justify-center rounded-full bg-muted text-muted-foreground font-medium"
        >
            {{ fallbackText }}
        </div>
    </div>
</template>
