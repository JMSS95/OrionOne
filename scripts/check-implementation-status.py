#!/usr/bin/env python3
"""
Script para verificar automaticamente o estado de implementação do OrionOne
e atualizar a secção de status no implementation-checklist.md

Uso:
    python scripts/check-implementation-status.py
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Diretório raiz do projeto
PROJECT_ROOT = Path(__file__).parent.parent

# Definição de features e seus artefactos esperados
FEATURES = {
    "Sprint 1": {
        "Feature 1: Roles & Permissions": {
            "files": [
                "database/seeders/RolePermissionSeeder.php",
                "database/seeders/UserSeeder.php",
                "tests/Feature/RolePermissionTest.php",
            ],
            "migrations": ["create_permission_tables", "create_activity_log_table"],
        },
        "Feature 2: Avatar Upload": {
            "files": [
                "app/Actions/Users/UpdateProfileAction.php",
                "tests/Feature/UpdateProfileTest.php",
            ],
            "migrations": ["add_avatar_to_users_table"],
        },
    },
    "Sprint 2": {
        "Feature 3: Create Ticket": {
            "files": [
                "app/Models/Ticket.php",
                "app/Data/TicketData.php",
                "app/Actions/Tickets/CreateTicketAction.php",
                "tests/Feature/CreateTicketTest.php",
                "database/factories/TicketFactory.php",
            ],
            "migrations": ["create_tickets_table"],
        },
        "Feature 4: List Tickets": {
            "files": [
                "app/Http/Controllers/TicketController.php",
                "resources/js/Pages/Tickets/Index.vue",
                "resources/js/Pages/Tickets/Create.vue",
                "tests/Feature/ListTicketsTest.php",
            ],
        },
        "Feature 5: Swagger Setup": {
            "files": [
                "config/l5-swagger.php",
            ],
            "composer_packages": ["darkaonline/l5-swagger"],
        },
    },
    "Sprint 3": {
        "Feature 6: Comments System": {
            "files": [
                "app/Models/Comment.php",
                "app/Data/CommentData.php",
                "app/Actions/Comments/CreateCommentAction.php",
                "tests/Feature/CommentTest.php",
            ],
            "migrations": ["create_comments_table"],
        },
        "Feature 7: Teams Management": {
            "files": [
                "app/Models/Team.php",
                "app/Http/Controllers/TeamController.php",
                "tests/Feature/TeamTest.php",
            ],
            "migrations": ["create_teams_table", "create_team_user_table"],
        },
        "Feature 8: Email Notifications": {
            "files": [
                "app/Notifications/TicketAssignedNotification.php",
                "app/Notifications/CommentAddedNotification.php",
                "app/Notifications/TicketStatusChangedNotification.php",
            ],
        },
    },
}


def check_file_exists(filepath):
    """Verifica se um ficheiro existe"""
    return (PROJECT_ROOT / filepath).exists()


def check_migration_exists(migration_name):
    """Verifica se uma migration existe"""
    migrations_dir = PROJECT_ROOT / "database" / "migrations"
    if not migrations_dir.exists():
        return False

    for migration_file in migrations_dir.glob("*.php"):
        if migration_name in migration_file.name:
            return True
    return False


def check_composer_package(package_name):
    """Verifica se um pacote está instalado via Composer"""
    composer_lock = PROJECT_ROOT / "composer.lock"
    if not composer_lock.exists():
        return False

    with open(composer_lock, "r", encoding="utf-8") as f:
        content = f.read()
        return package_name in content


def check_feature_status(feature_data):
    """Verifica o status de uma feature"""
    total_items = 0
    completed_items = 0

    # Verificar ficheiros
    if "files" in feature_data:
        for file in feature_data["files"]:
            total_items += 1
            if check_file_exists(file):
                completed_items += 1

    # Verificar migrations
    if "migrations" in feature_data:
        for migration in feature_data["migrations"]:
            total_items += 1
            if check_migration_exists(migration):
                completed_items += 1

    # Verificar pacotes Composer
    if "composer_packages" in feature_data:
        for package in feature_data["composer_packages"]:
            total_items += 1
            if check_composer_package(package):
                completed_items += 1

    if total_items == 0:
        return 0.0

    return (completed_items / total_items) * 100


def generate_status_report():
    """Gera relatório de status"""
    report = []
    report.append("## 📊 Estado Atual da Implementação\n")
    report.append(f"**Última Verificação:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")

    total_features = 0
    completed_features = 0

    for sprint_name, features in FEATURES.items():
        report.append(f"### {sprint_name}\n")

        sprint_progress = []
        for feature_name, feature_data in features.items():
            total_features += 1
            progress = check_feature_status(feature_data)

            if progress == 100:
                status = "✅"
                completed_features += 1
            elif progress > 0:
                status = "🟡"
            else:
                status = "🔴"

            sprint_progress.append(progress)
            report.append(f"- {status} **{feature_name}**: {progress:.0f}% completo\n")

        avg_progress = sum(sprint_progress) / len(sprint_progress) if sprint_progress else 0
        sprint_status = "✅" if avg_progress == 100 else "🟡" if avg_progress > 0 else "🔴"
        report.append(f"\n**Status do Sprint:** {sprint_status} {avg_progress:.0f}% completo\n\n")

    # Resumo geral
    overall_progress = (completed_features / total_features) * 100 if total_features > 0 else 0
    report.append("---\n\n")
    report.append("### 📈 Resumo Geral\n\n")
    report.append(f"- **Features Totais:** {total_features}\n")
    report.append(f"- **Features Completas:** {completed_features}\n")
    report.append(f"- **Progresso Global:** {overall_progress:.1f}%\n")

    return "".join(report)


def main():
    """Função principal"""
    print("🔍 Verificando estado de implementação do OrionOne...\n")

    report = generate_status_report()
    print(report)

    print("\n✅ Verificação completa!")
    print("\n💡 Para atualizar o implementation-checklist.md, copie o output acima")
    print("   para a secção 'Estado Atual da Implementação'")


if __name__ == "__main__":
    main()
