<?php

namespace App\Actions\Users;

use App\Models\User;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Intervention\Image\Laravel\Facades\Image;
use Lorisleiva\Actions\Concerns\AsAction;

class UpdateProfileAction
{
    use AsAction;

    public function handle(User $user, array $data): User
    {
        // Avatar upload
        if (isset($data['avatar']) && $data['avatar'] instanceof UploadedFile) {
            // Apagar avatar antigo
            if ($user->avatar) {
                Storage::disk('public')->delete($user->avatar);
            }

            // Processar nova imagem
            $image = Image::read($data['avatar']);
            $image->cover(200, 200);

            $path = 'avatars/' . $user->id . '_' . time() . '.jpg';
            Storage::disk('public')->put($path, $image->encode());

            $data['avatar'] = $path;
        }

        // Atualizar dados
        $user->update([
            'name' => $data['name'],
            'avatar' => $data['avatar'] ?? $user->avatar,
        ]);

        return $user->fresh();
    }

    public function asController(): \Illuminate\Http\RedirectResponse
    {
        $validated = request()->validate([
            'name' => ['required', 'string', 'max:255'],
            'avatar' => ['nullable', 'image', 'mimes:jpeg,png,jpg', 'max:2048'],
        ]);

        $this->handle(auth()->user(), $validated);

        return redirect()->route('profile.edit')
            ->with('success', 'Perfil atualizado com sucesso!');
    }
}
