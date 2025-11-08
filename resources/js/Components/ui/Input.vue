<script setup>
import { cn } from "@/lib/utils";
import { computed, useAttrs } from "vue";

const props = defineProps({
    modelValue: {
        type: [String, Number],
        default: "",
    },
    type: {
        type: String,
        default: "text",
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

const inputClasses = computed(() => {
    return cn(
        "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors",
        "file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground",
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
    <input
        :type="type"
        :value="modelValue"
        :class="inputClasses"
        :disabled="disabled"
        v-bind="attrs"
        @input="handleInput"
    />
</template>
