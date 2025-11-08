<script setup>
import { cn } from "@/lib/utils";
import { computed, useAttrs } from "vue";

const props = defineProps({
    modelValue: {
        type: [String, Number, Boolean],
        default: "",
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

const emit = defineEmits(["update:modelValue", "change"]);

const attrs = useAttrs();

const selectClasses = computed(() => {
    return cn(
        "flex h-9 w-full items-center justify-between rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm",
        "focus:outline-none focus:ring-1 focus:ring-ring",
        "disabled:cursor-not-allowed disabled:opacity-50",
        props.error && "border-destructive focus:ring-destructive"
    );
});

const handleChange = (event) => {
    const value = event.target.value;
    emit("update:modelValue", value);
    emit("change", value);
};
</script>

<template>
    <select
        :value="modelValue"
        :class="selectClasses"
        :disabled="disabled"
        v-bind="attrs"
        @change="handleChange"
    >
        <slot />
    </select>
</template>
