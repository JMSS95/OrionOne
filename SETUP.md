# Setup Rápido - OrionOne

## Docker (Recomendado)

```bash
# Iniciar containers
docker-compose up -d

# Instalar dependências
docker-compose exec orionone-app composer install
docker-compose exec orionone-frontend npm install --legacy-peer-deps

# Configurar ambiente
docker-compose exec orionone-app cp .env.example .env
docker-compose exec orionone-app php artisan key:generate

# Base de dados
docker-compose exec orionone-app php artisan migrate --seed
```

**Aceder:**

-   Laravel: http://localhost:8888
-   Vite HMR: http://localhost:5173

---

## Documentação Completa

Para informação detalhada sobre o setup, consultar:

-   **[Setup Changelog](docs/setup-changelog.md)** - Histórico completo de instalação, pacotes, configurações
-   **[Commands Reference](docs/commands-reference.md)** - Todos os comandos (Git, Docker, Laravel, NPM)
-   **[Docker Guide](docs/docker-guide.md)** - Guia Docker para iniciantes
-   **[Tech Stack](docs/tech-stack.md)** - Stack tecnológica completa

---

## Próximos Passos

Seguir **[Implementation Checklist](docs/implementation-checklist.md)** para começar o desenvolvimento:

1. **Sprint 1:** Auth & Users (Roles, Permissions, Seeders)
2. **Sprint 2:** Tickets Core (CRUD, Status, Priority)
3. **Sprint 3:** Colaboração (Comments, Teams, Notifications)
4. **Sprint 4:** Knowledge Base
5. **Sprint 5:** Dashboard & Reports
6. **Sprint 6:** Polish & Deploy

---

**Status:** ✅ Ambiente 100% configurado, pronto para desenvolvimento!
