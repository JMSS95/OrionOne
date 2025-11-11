<?php

namespace Tests\Feature;

// Importa a classe base TestCase que fornece métodos auxiliares para testes
use Tests\TestCase;

// Importa o modelo User para poder criar e manipular utilizadores nos testes
use App\Models\User;

// Importa a classe UploadedFile que simula o upload de ficheiros em testes
use Illuminate\Http\UploadedFile;

// Importa a facade Storage para manipular o sistema de ficheiros
use Illuminate\Support\Facades\Storage;

// Importa o trait RefreshDatabase que limpa a base de dados entre testes
use Illuminate\Foundation\Testing\RefreshDatabase;

// Importa o trait WithoutMiddleware para desativar middleware CSRF nos testes
use Illuminate\Foundation\Testing\WithoutMiddleware;

class UpdateProfileTest extends TestCase
{
    // Usa o trait RefreshDatabase para garantir que cada teste tem uma BD limpa
    // Executa migrations antes de cada teste e faz rollback depois
    use RefreshDatabase;

    // Usa WithoutMiddleware para desativar CSRF protection durante os testes
    // Isto evita o erro 419 (CSRF token mismatch)
    use WithoutMiddleware;

     //Verifica se um utilizador consegue atualizar o perfil com avatar
     //Testa o fluxo completo de upload de imagem e atualização de dados
    public function test_user_can_update_profile_with_avatar(): void
    {
        // Cria um sistema de ficheiros falso (em memória) para o disco 'public'
        // Isto evita criar ficheiros reais durante os testes
        Storage::fake('public');

        // Cria um utilizador de teste usando a factory (database/factories/UserFactory.php)
        // A factory gera dados aleatórios (nome, email, password) automaticamente
        $user = User::factory()->create();

        // Simula um pedido HTTP POST autenticado (actingAs = fazer login como este user)
        // Envia para a rota 'profile.update' (definida em routes/web.php)
        // Os dados enviados são: nome atualizado + ficheiro de imagem simulado
        $response = $this->actingAs($user)->post(route('profile.update'), [
            'name' => 'Updated Name', // Novo nome para o utilizador
            'avatar' => UploadedFile::fake()->image('avatar.jpg'), // Simula upload de imagem JPG
        ]);

        // Debug: mostrar status e conteúdo da resposta se falhar
        if ($response->status() !== 302) {
            dump($response->status(), $response->getContent());
        }

        // Verifica se a resposta HTTP redireciona para a página de edição do perfil
        // assertRedirect confirma que o controller fez redirect() após sucesso
        $response->assertRedirect(route('profile.edit'));

        // $user->fresh() recarrega o utilizador da base de dados (obtém dados atualizados)
        // assertEquals verifica se o nome foi realmente atualizado na BD
        $this->assertEquals('Updated Name', $user->fresh()->name);

        // assertNotNull verifica que o campo 'avatar' já não é NULL (ficheiro foi guardado)
        $this->assertNotNull($user->fresh()->avatar);

        // Verifica que o ficheiro do avatar existe fisicamente no disco 'public'
        // O caminho vem de $user->avatar (ex: 'avatars/abc123.jpg')
        Storage::disk('public')->assertExists($user->fresh()->avatar);
    }

     // Verifica validação - avatar tem de ser uma imagem
     // Testa que ficheiros não-imagem (PDF, TXT, etc) são rejeitados
    public function test_avatar_must_be_image(): void
    {
        // Cria um utilizador de teste
        $user = User::factory()->create();

        // Tenta enviar um PDF em vez de uma imagem
        // UploadedFile::fake()->create() cria ficheiro genérico (não-imagem)
        $response = $this->actingAs($user)->post(route('profile.update'), [
            'name' => 'Test',
            'avatar' => UploadedFile::fake()->create('document.pdf'), // PDF não é imagem
        ]);

        // assertSessionHasErrors verifica que existe erro de validação para 'avatar'
        // O controller/FormRequest deve ter regra: 'avatar' => 'image'
        $response->assertSessionHasErrors(['avatar']);
    }

     //Verifica que o avatar antigo é apagado quando se faz upload de novo
     //Testa a limpeza de ficheiros órfãos (importante para não encher o disco)
    public function test_old_avatar_is_deleted_on_new_upload(): void
    {
        // Cria sistema de ficheiros falso
        Storage::fake('public');

        // Cria utilizador JÁ COM avatar antigo no campo 'avatar'
        // factory()->create(['campo' => 'valor']) sobrescreve valores gerados
        $user = User::factory()->create([
            'avatar' => 'avatars/old-avatar.jpg', // Simula que já tinha avatar
        ]);

        // Cria fisicamente o ficheiro antigo no storage falso
        // put(caminho, conteúdo) - 'old content' é texto qualquer para simular ficheiro
        Storage::disk('public')->put('avatars/old-avatar.jpg', 'old content');

        // Faz upload de NOVO avatar (mantém o mesmo nome do utilizador)
        $this->actingAs($user)->post(route('profile.update'), [
            'name' => $user->name, // Mantém nome original
            'avatar' => UploadedFile::fake()->image('new-avatar.jpg'), // Novo avatar
        ]);

        // assertMissing verifica que o ficheiro ANTIGO foi APAGADO do storage
        // O controller deve ter lógica: if($user->avatar) Storage::delete($user->avatar);
        Storage::disk('public')->assertMissing('avatars/old-avatar.jpg');

        // assertExists verifica que o ficheiro NOVO existe
        // $user->fresh()->avatar agora tem o caminho do novo ficheiro
        Storage::disk('public')->assertExists($user->fresh()->avatar);
    }
}
