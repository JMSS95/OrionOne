<?php

namespace Tests\Feature;

use Tests\TestCase;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Database\Seeders\RolePermissionSeeder;

class RolePermissionTest extends TestCase
{
    use RefreshDatabase;

    public function test_system_has_required_roles(): void
    {
        $this->seed(RolePermissionSeeder::class);

        $this->assertDatabaseHas('roles', ['name' => 'admin']);
        $this->assertDatabaseHas('roles', ['name' => 'agent']);
        $this->assertDatabaseHas('roles', ['name' => 'user']);
    }

    public function test_admin_has_all_permissions(): void
    {
        $this->seed(RolePermissionSeeder::class);

        $admin = Role::findByName('admin');

        $this->assertTrue($admin->hasPermissionTo('tickets.create'));
        $this->assertTrue($admin->hasPermissionTo('tickets.delete'));
        $this->assertTrue($admin->hasPermissionTo('users.manage'));
    }

    public function test_agent_can_manage_tickets_only(): void
    {
        $this->seed(RolePermissionSeeder::class);

        $agent = Role::findByName('agent');

        $this->assertTrue($agent->hasPermissionTo('tickets.create'));
        $this->assertTrue($agent->hasPermissionTo('comments.create'));
        $this->assertFalse($agent->hasPermissionTo('users.manage'));
    }

    public function test_user_can_only_create_tickets(): void
    {
        $this->seed(RolePermissionSeeder::class);

        $user = Role::findByName('user');

        $this->assertTrue($user->hasPermissionTo('tickets.create'));
        $this->assertFalse($user->hasPermissionTo('tickets.delete'));
        $this->assertFalse($user->hasPermissionTo('users.view'));
    }
}
