import { Ability, AbilityBuilder, AbilityClass } from '@casl/ability';
import { Injectable } from '@nestjs/common';

// Define your entities/subjects
type Subjects = 'Incident' | 'User' | 'KnowledgeBase' | 'Comment' | 'all';

export enum Action {
    Manage = 'manage', // All actions
    Create = 'create',
    Read = 'read',
    Update = 'update',
    Delete = 'delete',
}

export type AppAbility = Ability<[Action, Subjects]>;

interface UserWithRole {
    id: string;
    role: string;
}

@Injectable()
export class CaslAbilityFactory {
    createForUser(user: UserWithRole) {
        const { can, build } = new AbilityBuilder<AppAbility>(
            Ability as AbilityClass<AppAbility>,
        );

        // Admin has full access
        if (user.role === 'ADMIN') {
            can(Action.Manage, 'all');
        }

        // Agent permissions
        if (user.role === 'AGENT') {
            can(Action.Read, 'all');
            can(Action.Create, 'Incident');
            can(Action.Update, 'Incident');
            can(Action.Create, 'Comment');
            can(Action.Create, 'KnowledgeBase');
            can(Action.Update, 'KnowledgeBase');
        }

        // User permissions (basic)
        if (user.role === 'USER') {
            can(Action.Read, 'Incident');
            can(Action.Create, 'Incident');
            can(Action.Update, 'Incident');
            can(Action.Read, 'KnowledgeBase');
            can(Action.Create, 'Comment');
        }

        return build();
    }
}
