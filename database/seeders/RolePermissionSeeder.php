<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Spatie\Permission\Models\Role;
use Spatie\Permission\Models\Permission;

class RolePermissionSeeder extends Seeder
{
    public function run(): void
    {
        // Reset cached roles and permissions
        app()[\Spatie\Permission\PermissionRegistrar::class]->forgetCachedPermissions();

        // Criar permissões
        $permissions = [
            'tickets.create',
            'tickets.view',
            'tickets.update',
            'tickets.delete',
            'tickets.assign',
            'tickets.close',
            'comments.create',
            'comments.delete',
            'users.view',
            'users.manage',
        ];

        foreach ($permissions as $permission) {
            Permission::create(['name' => $permission]);
        }

        // Admin - todas as permissões
        $admin = Role::create(['name' => 'admin']);
        $admin->givePermissionTo(Permission::all());

        // Agent - gestão de tickets
        $agent = Role::create(['name' => 'agent']);
        $agent->givePermissionTo([
            'tickets.create',
            'tickets.view',
            'tickets.update',
            'tickets.assign',
            'tickets.close',
            'comments.create',
            'comments.delete',
        ]);

        // User - apenas criar tickets
        $user = Role::create(['name' => 'user']);
        $user->givePermissionTo([
            'tickets.create',
            'tickets.view',
            'comments.create',
        ]);
    }
}
