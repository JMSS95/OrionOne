<script setup>
import { cn } from "@/lib/utils";
import { computed, useAttrs } from "vue";

const props = defineProps({
    modelValue: {
        type: [String, Number],
        default: "",
    },
    rows: {
        type: Number,
        default: 3,
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    error: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);

const attrs = useAttrs();

const textareaClasses = computed(() => {
    return cn(
        "flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm",
        "placeholder:text-muted-foreground",
        "focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring",
        "disabled:cursor-not-allowed disabled:opacity-50",
        props.error && "border-destructive focus-visible:ring-destructive"
    );
});

const handleInput = (event) => {
    emit("update:modelValue", event.target.value);
};
</script>

<template>
    <textarea
        :value="modelValue"
        :rows="rows"
        :class="textareaClasses"
        :disabled="disabled"
        v-bind="attrs"
        @input="handleInput"
    />
</template>
