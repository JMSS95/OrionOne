<script setup>
import { ref } from "vue";
import { useForm } from "@inertiajs/vue3";
import AuthenticatedLayout from "@/Layouts/AuthenticatedLayout.vue";
import Button from "@/components/ui/Button.vue";
import Input from "@/components/ui/Input.vue";

const props = defineProps({
    user: Object,
});

const avatarPreview = ref(
    props.user.avatar ? `/storage/${props.user.avatar}` : null
);

const form = useForm({
    name: props.user.name,
    avatar: null,
});

const handleAvatarChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        form.avatar = file;
        avatarPreview.value = URL.createObjectURL(file);
    }
};

const submit = () => {
    form.post(route("profile.update"));
};
</script>

<template>
    <AuthenticatedLayout>
        <div class="max-w-2xl mx-auto p-6">
            <h1 class="text-2xl font-bold mb-6">Editar Perfil</h1>

            <form @submit.prevent="submit" class="space-y-6">
                <!-- Avatar -->
                <div>
                    <label class="block text-sm font-medium mb-2">
                        Foto de Perfil
                    </label>

                    <div class="flex items-center space-x-4">
                        <img
                            v-if="avatarPreview"
                            :src="avatarPreview"
                            alt="Avatar"
                            class="w-24 h-24 rounded-full object-cover"
                        />
                        <div
                            v-else
                            class="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center"
                        >
                            <span class="text-gray-500 text-2xl">
                                {{ user.name.charAt(0).toUpperCase() }}
                            </span>
                        </div>

                        <Input
                            type="file"
                            @change="handleAvatarChange"
                            accept="image/jpeg,image/png,image/jpg"
                        />
                    </div>

                    <p
                        v-if="form.errors.avatar"
                        class="mt-2 text-sm text-red-600"
                    >
                        {{ form.errors.avatar }}
                    </p>
                </div>

                <!-- Name -->
                <div>
                    <label class="block text-sm font-medium mb-2">Nome</label>
                    <Input v-model="form.name" required />
                    <p
                        v-if="form.errors.name"
                        class="mt-2 text-sm text-red-600"
                    >
                        {{ form.errors.name }}
                    </p>
                </div>

                <!-- Submit -->
                <Button type="submit" :disabled="form.processing">
                    Guardar Alterações
                </Button>
            </form>
        </div>
    </AuthenticatedLayout>
</template>
