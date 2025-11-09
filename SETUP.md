# Setup Rápido - OrionOne

## Docker (Recomendado)

```bash
# Iniciar containers
docker-compose up -d

### Frontend não compila / Vite não inicia

```bash
# Reinstalar dependências
docker-compose exec orionone-frontend rm -rf node_modules package-lock.json
docker-compose exec orionone-frontend npm install --legacy-peer-deps

# Verificar portas (5173 deve estar livre)
docker-compose ps
```

### Base de Dados

-   **Host:** localhost (ou orionone-db dentro do Docker)
-   **Porta:** 5433 (externa) / 5432 (interna)
-   **Database:** orionone
-   **User:** laravel
-   **Password:** laravel

---

## 📚 Documentação Completa

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

**Status:** Ambiente 100% configurado, pronto para desenvolvimento!
