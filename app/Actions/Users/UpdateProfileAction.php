<?php

namespace App\Actions\Users;

// Importa o modelo User para manipular dados do utilizador
use App\Models\User;

// Importa a classe UploadedFile para verificar se é um ficheiro enviado via HTTP
use Illuminate\Http\UploadedFile;

// Importa a facade Storage para manipular ficheiros (guardar, apagar)
// Acede ao sistema de ficheiros configurado em config/filesystems.php
use Illuminate\Support\Facades\Storage;

// Importa a facade Image do pacote Intervention/Image versão 3 para processar imagens
// Permite redimensionar, cortar, converter formatos de imagem
use Intervention\Image\ImageManager;
use Intervention\Image\Drivers\Gd\Driver;

// Importa o trait AsAction do pacote lorisleiva/laravel-actions
// Permite usar esta classe como: Controller, Job, Listener, Command
use Lorisleiva\Actions\Concerns\AsAction;

// Define a classe Action reutilizável para atualizar perfil de utilizador
class UpdateProfileAction
{
    // Usa o trait AsAction que adiciona métodos mágicos:
    // - asController() = usar como controller
    // - asJob() = usar como queue job
    // - asListener() = usar como event listener
    use AsAction;

    /**
     * Método principal que executa a lógica de atualização do perfil
     *
     * @param User $user - O utilizador a ser atualizado (vem da autenticação)
     * @param array $data - Dados validados do formulário ['name' => ..., 'avatar' => ...]
     * @return User - Retorna o utilizador atualizado (com dados frescos da BD)
     */
    public function handle(User $user, array $data): User
    {
        // ============= PROCESSAMENTO DO AVATAR (se foi enviado) =============

        // Verifica se o campo 'avatar' existe no array $data
        // E verifica se é uma instância de UploadedFile (ficheiro real enviado via POST)
        if (isset($data['avatar']) && $data['avatar'] instanceof UploadedFile) {            // Verifica se o utilizador JÁ TEM um avatar guardado (campo não é NULL)
            if ($user->avatar) {
                // Apaga o ficheiro físico do disco 'public' (storage/app/public)
                // $user->avatar contém o caminho ex: 'avatars/1_1699999999.jpg'
                Storage::disk('public')->delete($user->avatar);
            }

            // Lê o ficheiro enviado e carrega-o na memória como objeto Image (versão 3)
            // $data['avatar'] é o UploadedFile (JPG, PNG, etc)
            $manager = new ImageManager(new Driver());
            $image = $manager->read($data['avatar']);

            // Redimensiona e corta a imagem para 200x200 pixels (quadrado)
            // cover() mantém aspeto mas corta excesso (diferente de resize que distorce)
            $image->cover(200, 200);

            // Cria nome único para o ficheiro: 'avatars/ID_TIMESTAMP.jpg'
            // Ex: 'avatars/5_1699887654.jpg'
            // $user->id = ID do utilizador (único)
            // time() = timestamp atual (evita conflitos se fizer upload várias vezes)
            $path = 'avatars/' . $user->id . '_' . time() . '.jpg';

            // Guarda a imagem processada no disco 'public'
            // toJpeg() converte a imagem para JPG (compressão) e retorna EncodedImage
            // Convertemos para string com toString() para guardar o conteúdo binário
            // Ficheiro fica em: storage/app/public/avatars/5_1699887654.jpg
            Storage::disk('public')->put($path, (string) $image->toJpeg());

            // Substitui o UploadedFile no array $data pelo caminho do ficheiro guardado
            // Agora $data['avatar'] = 'avatars/5_1699887654.jpg' (string)
            $data['avatar'] = $path;
        }

        // Atualiza os campos do utilizador na tabela 'users'
        $user->update([
            'name' => $data['name'], // Novo nome (sempre atualiza)

            // Operador ?? (null coalescing):
            // Se $data['avatar'] existe (foi feito upload), usa o novo caminho
            // Se não existe (não foi enviado ficheiro), mantém o avatar atual ($user->avatar)
            'avatar' => $data['avatar'] ?? $user->avatar,
        ]);

        // Recarrega o utilizador da base de dados para obter valores atualizados
        // fresh() faz SELECT * FROM users WHERE id = ?
        // Importante porque update() não atualiza o objeto $user em memória
        return $user->fresh();
    }

    /**
     * Método executado quando esta Action é usada como Controller
     * Define a rota em routes/web.php: Route::post('/profile', UpdateProfileAction::class)
     *
     * @return \Illuminate\Http\RedirectResponse - Resposta HTTP de redirecionamento
     */
    public function asController(): \Illuminate\Http\RedirectResponse
    {
        // Valida os dados recebidos do formulário (request HTTP)
        // request() = helper do Laravel que acede ao pedido HTTP atual
        // Se validação falhar, Laravel redireciona automaticamente com erros
        $validated = request()->validate([
            // 'name' é obrigatório, tipo string, máximo 255 caracteres
            'name' => ['required', 'string', 'max:255'],

            // 'avatar' é opcional (nullable), mas SE enviado tem de ser:
            // - image: tipo MIME de imagem
            // - mimes:jpeg,png,jpg: apenas estes formatos
            // - max:2048: máximo 2MB (2048 KB)
            'avatar' => ['nullable', 'image', 'mimes:jpeg,png,jpg', 'max:2048'],
        ]);

        // Chama o método handle() passando:
        // - auth()->user() = utilizador autenticado (logado) na sessão atual
        // - $validated = array com dados validados ['name' => ..., 'avatar' => ...]
        $this->handle(auth()->user(), $validated);

        // Redireciona para a página de edição do perfil
        // route('profile.edit') gera URL da rota nomeada 'profile.edit'
        // with('success', ...) adiciona mensagem flash à sessão (aparece 1 vez)
        return redirect()->route('profile.edit')
            ->with('success', 'Perfil atualizado com sucesso!');
    }
}
