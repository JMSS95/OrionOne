# Docker Deep Dive - OrionOne

## 📚 Índice

1. [Conceitos Fundamentais](#conceitos-fundamentais)
2. [Anatomia do docker-compose.yml](#anatomia-do-docker-composeyml)
3. [Dockerfile Explicado](#dockerfile-explicado)
4. [Networking e Comunicação](#networking-e-comunicação)
5. [Volumes e Persistência](#volumes-e-persistência)
6. [Processo de Setup Completo](#processo-de-setup-completo)
7. [Troubleshooting Comum](#troubleshooting-comum)

---

## Conceitos Fundamentais

### O que é Docker?

Docker é uma plataforma que permite empacotar aplicações e suas dependências em **containers** isolados.

**Analogia:** Pensa num container como uma "casa móvel" completa:

-   Tem tudo que precisa (SO, runtime, bibliotecas)
-   É portátil (funciona igual em qualquer PC)
-   É isolada (não interfere com outras "casas")

### Componentes Principais

```
┌─────────────────────────────────────────┐
│         DOCKER ECOSYSTEM                │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────────────┐    │
│  │  Image   │  │   Container       │    │
│  │ (Molde)  │─→│ (Instância ativa) │    │
│  └──────────┘  └──────────────────┘    │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │     docker-compose.yml           │  │
│  │  (Orquestrador multi-container)  │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │ Network  │  │  Volume  │            │
│  │ (Ponte)  │  │  (Disco) │            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
```

#### 1. **Image (Imagem)**

-   É um **template read-only**
-   Define o que vai ter no container (SO, runtime, código)
-   Criada a partir de um `Dockerfile`

**Exemplo:**

```dockerfile
FROM php:8.2-fpm-alpine  # Imagem base
RUN apk add git          # Comandos para customizar
```

#### 2. **Container**

-   É uma **instância ativa** de uma imagem
-   Pode ser iniciado, parado, removido
-   Isolado do host e de outros containers

**Exemplo:**

```bash
docker run -d nginx:alpine  # Cria e inicia container do Nginx
```

#### 3. **Volume**

-   **Armazenamento persistente** (sobrevive à remoção do container)
-   Permite compartilhar dados entre host ↔ container

**Tipos:**

```yaml
volumes:
    - ./codigo:/app # Bind mount (pasta do host)
    - orionone_pgdata:/var/lib # Named volume (gerenciado pelo Docker)
    - /app/node_modules # Anonymous volume (temporário)
```

#### 4. **Network**

-   Permite containers **comunicarem entre si**
-   Isola tráfego de rede

**Exemplo:**

```yaml
networks:
    orionone_network:
        driver: bridge # Rede privada interna
```

#### 5. **docker-compose**

-   Ferramenta para **orquestrar múltiplos containers**
-   Usa arquivo `docker-compose.yml` (YAML)
-   Facilita start/stop de toda a stack

---

## Anatomia do docker-compose.yml

Vamos **dissecar** o arquivo do OrionOne linha por linha:

### Estrutura Geral

```yaml
services:       # Lista de containers
  app:          # Nome do serviço
    image:      # Imagem pronta OU
    build:      # Dockerfile customizado
    ports:      # Mapeamento de portas
    volumes:    # Volumes (dados persistentes)
    environment:# Variáveis de ambiente
    depends_on: # Dependências (ordem de inicialização)
    networks:   # Redes para comunicação
    healthcheck:# Verificação de saúde

networks:       # Redes personalizadas
volumes:        # Volumes nomeados
```

### Service 1: Laravel + PHP-FPM

```yaml
orionone-app:
    build:
        context: . # Pasta onde está o Dockerfile
        dockerfile: Dockerfile # Nome do arquivo
    container_name: orionone_app # Nome fixo (não auto-gerado)
    restart: unless-stopped # Reinicia se crashar (exceto stop manual)
    working_dir: /var/www/html # Pasta de trabalho dentro do container
    volumes:
        - ./:/var/www/html # BIND MOUNT: Código do host → container
          # Permite editar no host, reflete no container
    environment:
        - DB_HOST=orionone-db # Variáveis de ambiente
        - DB_PORT=5432 # Sobrescrevem .env
        - DB_USERNAME=laravel
    depends_on:
        orionone-db:
            condition: service_healthy # Só inicia DEPOIS do DB estar healthy
    networks:
        - orionone_network # Conecta à rede privada
    healthcheck:
        test: ["CMD", "php", "-v"] # Comando para testar saúde
        interval: 30s # Executa a cada 30s
        timeout: 10s
        retries: 3 # Tenta 3x antes de marcar unhealthy
```

**Por que `build` em vez de `image`?**

-   `image: nginx:alpine` → Usa imagem pronta do Docker Hub
-   `build: .` → **Constrói imagem customizada** a partir do Dockerfile

### Service 2: Frontend (Vite)

```yaml
orionone-frontend:
    image: node:20-alpine # Imagem pronta (Node.js 20 em Alpine Linux)
    command: npm run dev -- --host 0.0.0.0 # Sobrescreve CMD padrão da imagem
    volumes:
        - ./:/app # Código do host
    ports:
        - "5173:5173" # HOST:CONTAINER
          # localhost:5173 → container porta 5173
```

**Por que Alpine?**

-   Distribuição Linux **ultra-leve** (~5MB)
-   Ideal para containers (menos espaço, mais rápido)

### Service 3: PostgreSQL

```yaml
orionone-db:
    image: postgres:16-alpine
    environment:
        POSTGRES_DB: orionone # Cria DB automaticamente
        POSTGRES_USER: laravel
        POSTGRES_PASSWORD: secret
    volumes:
        - orionone_pgdata:/var/lib/postgresql/data # NAMED VOLUME (persistente)
        - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
          # Script executado APENAS na 1ª inicialização
          # :ro = read-only (segurança)
    healthcheck:
        test: ["CMD-SHELL", "pg_isready -U laravel"] # Testa conexão PostgreSQL
```

**Por que Named Volume?**

```yaml
volumes:
    orionone_pgdata: # Docker gerencia onde fica fisicamente
```

-   Dados **persistem** mesmo deletando o container
-   Backup facilitado: `docker cp orionone_postgres:/var/lib/postgresql/data backup/`

### Service 4: Redis

```yaml
orionone-redis:
    image: redis:7-alpine
    command:
        ["redis-server", "--appendonly", "yes", "--requirepass", ""]
        # Sobrescreve comando padrão
        # --appendonly yes = persistência AOF (Append Only File)
        # --requirepass "" = sem senha (desenvolvimento)
```

### Service 5: Nginx

```yaml
orionone-nginx:
    image: nginx:alpine
    ports:
        - "8888:80" # localhost:8888 → Nginx porta 80
    volumes:
        - ./:/var/www/html # Código PHP
        - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
          # Configuração customizada do Nginx
    depends_on:
        - orionone-app # Nginx precisa do PHP-FPM rodando
```

### Networks

```yaml
networks:
    orionone_network:
        driver: bridge # Rede privada interna (padrão)
```

**Como funciona:**

```
┌─────────────────────────────────────────┐
│      orionone_network (172.18.0.0/16)   │
│  ┌────────────┬────────────┬──────────┐ │
│  │ orionone-  │ orionone-  │ orionone-│ │
│  │    app     │     db     │   redis  │ │
│  │ 172.18.0.2 │ 172.18.0.3 │172.18.0.4│ │
│  └────────────┴────────────┴──────────┘ │
└─────────────────────────────────────────┘
         ↓
   Host: localhost:8888
```

Containers podem comunicar usando **nome do serviço**:

```php
// Dentro do container orionone-app
DB_HOST=orionone-db  // DNS interno resolve para 172.18.0.3
```

---

## Dockerfile Explicado

O `Dockerfile` é uma **receita** para construir uma imagem.

### Estrutura do OrionOne

```dockerfile
# 1. IMAGEM BASE
FROM php:8.2-fpm-alpine
# php:8.2-fpm = PHP 8.2 com FastCGI Process Manager
# alpine = Linux Alpine (leve)

# 2. INSTALAR DEPENDÊNCIAS DO SISTEMA
RUN apk add --no-cache \
    git \
    curl \
    libpng-dev \      # Biblioteca para GD (imagens)
    postgresql-dev \  # Headers do PostgreSQL
    autoconf \        # Necessário para compilar extensões PECL
    g++ \             # Compilador C++
    make              # Build tool

# 3. INSTALAR EXTENSÕES PHP
RUN docker-php-ext-install \
    pdo_pgsql \  # Driver PostgreSQL
    zip \        # Manipular arquivos ZIP
    gd \         # Manipular imagens (GD library)
    opcache      # Cache de bytecode (performance)

# 4. INSTALAR EXTENSÕES PECL
RUN pecl install redis && docker-php-ext-enable redis
# PECL = repositório de extensões PHP em C
# redis = extensão para conectar ao Redis

# 5. INSTALAR COMPOSER
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer
# Multi-stage build: copia apenas o binário da imagem oficial

# 6. DEFINIR WORKDIR
WORKDIR /var/www/html
# Todos os comandos seguintes executam nesta pasta

# 7. COPIAR CÓDIGO
COPY . /var/www/html
# Copia todo o projeto para dentro da imagem

# 8. INSTALAR DEPENDÊNCIAS PHP
RUN composer install --no-dev --optimize-autoloader --no-interaction
# --no-dev = ignora dependências de desenvolvimento
# --optimize-autoloader = otimiza carregamento de classes

# 9. PERMISSÕES
RUN chown -R www-data:www-data /var/www/html/storage
# www-data = usuário padrão do PHP-FPM
# Garante que Laravel pode escrever em storage/

# 10. EXPOR PORTA
EXPOSE 9000
# Documenta que PHP-FPM escuta na porta 9000 (FastCGI)

# 11. COMANDO PADRÃO
CMD ["php-fpm"]
# Inicia PHP-FPM quando container iniciar
```

### Build Process

Quando você executa `docker-compose build`:

```bash
docker-compose build
```

**Processo:**

1. Lê o `Dockerfile`
2. Executa cada instrução (`FROM`, `RUN`, `COPY`...)
3. Cada instrução cria uma **layer** (camada)
4. Layers são **cacheadas** (build futuro mais rápido)
5. Gera imagem final com tag `orionone-orionone-app`

**Exemplo de Layers:**

```
┌─────────────────────────────┐
│ CMD ["php-fpm"]             │  Layer 10 (1KB)
├─────────────────────────────┤
│ COPY . /var/www/html        │  Layer 9 (50MB)
├─────────────────────────────┤
│ RUN composer install        │  Layer 8 (100MB)
├─────────────────────────────┤
│ RUN docker-php-ext-install  │  Layer 7 (20MB)
├─────────────────────────────┤
│ RUN apk add git curl...     │  Layer 6 (30MB)
├─────────────────────────────┤
│ FROM php:8.2-fpm-alpine     │  Layer base (80MB)
└─────────────────────────────┘
Total: ~280MB
```

**Cache Busting:**

-   Se alterar Layer 6, Layers 7-10 são **reconstruídas**
-   Por isso `COPY` fica no final (código muda frequentemente)

---

## Networking e Comunicação

### Como Containers se Comunicam?

#### 1. **Dentro da mesma rede Docker**

```yaml
services:
    app:
        networks:
            - orionone_network
    db:
        networks:
            - orionone_network
```

**Comunicação:**

```php
// Container 'app' pode acessar 'db' pelo nome:
$host = 'orionone-db';  // Docker DNS resolve automaticamente
$port = 5432;
```

**DNS Interno:**

```
orionone-db → 172.18.0.3
orionone-redis → 172.18.0.4
```

#### 2. **Host → Container**

```yaml
ports:
    - "8888:80" # HOST_PORT:CONTAINER_PORT
```

**Fluxo:**

```
Browser (localhost:8888)
     ↓
Docker Desktop (bind port)
     ↓
orionone-nginx (porta 80)
```

#### 3. **Container → Host**

No Windows/Mac, use `host.docker.internal`:

```php
// Acessar MySQL do Laragon (fora do Docker):
DB_HOST=host.docker.internal
DB_PORT=3306
```

### Exemplo Completo: Request HTTP

```
1. Browser → http://localhost:8888/login

2. Docker Desktop recebe na porta 8888

3. Encaminha para orionone-nginx (porta 80)

4. Nginx lê /var/www/html/public/index.php

5. Nginx encaminha para orionone-app:9000 (FastCGI)
   ↓
   location ~ \.php$ {
       fastcgi_pass orionone-app:9000;  # DNS interno!
   }

6. PHP-FPM executa Laravel

7. Laravel conecta ao PostgreSQL:
   DB_HOST=orionone-db:5432  # DNS interno!

8. Resposta: Nginx → Docker → Browser
```

---

## Volumes e Persistência

### Tipos de Volumes

#### 1. **Bind Mount** (Sincronização host ↔ container)

```yaml
volumes:
    - ./codigo:/app
```

**Uso:**

-   Desenvolvimento (editar no host, reflete no container)
-   Configurações (`./docker/nginx/default.conf`)

**Exemplo:**

```bash
# No host (Windows):
echo "<?php echo 'Hello';" > index.php

# Dentro do container:
cat /var/www/html/index.php
# Output: <?php echo 'Hello';
```

#### 2. **Named Volume** (Persistência gerenciada)

```yaml
volumes:
    orionone_pgdata:
        driver: local

services:
    db:
        volumes:
            - orionone_pgdata:/var/lib/postgresql/data
```

**Uso:**

-   Dados de banco (PostgreSQL, MySQL)
-   Cache Redis
-   Uploads de usuários

**Localização física:**

```bash
# Windows (WSL2):
\\wsl$\docker-desktop-data\data\docker\volumes\orionone_orionone_pgdata

# Linux:
/var/lib/docker/volumes/orionone_orionone_pgdata
```

**Backup:**

```bash
# Exportar volume
docker run --rm -v orionone_pgdata:/data -v $(pwd):/backup alpine tar czf /backup/pgdata.tar.gz /data

# Restaurar
docker run --rm -v orionone_pgdata:/data -v $(pwd):/backup alpine tar xzf /backup/pgdata.tar.gz -C /
```

#### 3. **Anonymous Volume** (Temporário)

```yaml
volumes:
    - /app/node_modules
```

**Uso:**

-   Prevenir que pasta do host sobrescreva pasta do container
-   Exemplo: `node_modules` compilado no Linux não funciona no Windows

---

## Processo de Setup Completo

### Fluxo de Inicialização

```
┌─────────────────────────────────────────────────┐
│ 1. docker-compose up -d                         │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 2. Lê docker-compose.yml                        │
│    - Valida sintaxe YAML                        │
│    - Verifica imagens/Dockerfiles               │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 3. Build de Imagens Customizadas                │
│    - Se não existir: docker-compose build       │
│    - Se existir: usa imagem cacheada            │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 4. Cria Network                                  │
│    - orionone_network (bridge)                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 5. Cria Volumes                                  │
│    - orionone_pgdata (se não existir)            │
│    - orionone_redisdata (se não existir)         │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 6. Inicia Containers (ordem: depends_on)         │
│    ① orionone-db (PostgreSQL)                    │
│    ② orionone-redis (Redis)                      │
│    ③ orionone-frontend (Vite)                    │
│    ④ orionone-app (Laravel) ← Aguarda DB healthy │
│    ⑤ orionone-nginx (Nginx) ← Aguarda App        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 7. Healthchecks Contínuos                        │
│    - DB: pg_isready -U laravel                   │
│    - Redis: redis-cli ping                       │
│    - App: php -v                                 │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 8. Aplicação Pronta!                             │
│    http://localhost:8888                         │
└─────────────────────────────────────────────────┘
```

### Setup Passo a Passo (PC Novo)

```bash
# 1. Clone do repositório
git clone https://github.com/JMSS95/OrionOne.git
cd OrionOne

# 2. Inicia containers
docker-compose up -d
# ✅ Cria imagens, networks, volumes, containers

# 3. Verifica status
docker-compose ps
# Todos devem estar "Up" ou "Up (healthy)"

# 4. Instala dependências PHP (dentro do container)
docker-compose exec orionone-app composer install

# 5. Instala dependências Node (Linux-compatible)
docker-compose run --rm orionone-frontend npm install --legacy-peer-deps

# 6. Gera chave da aplicação
docker-compose exec orionone-app php artisan key:generate

# 7. Executa migrations
docker-compose exec orionone-app php artisan migrate

# 8. (Opcional) Seeders
docker-compose exec orionone-app php artisan db:seed

# 9. Acessa aplicação
# http://localhost:8888
```

**Tempo estimado:** 5-10 minutos (primeira vez)

---

## Troubleshooting Comum

### 1. Container não inicia (Restarting loop)

**Sintoma:**

```bash
docker-compose ps
# STATUS: Restarting (127)
```

**Diagnóstico:**

```bash
docker-compose logs orionone-frontend
# vite: not found
```

**Solução:**

```bash
# Faltam dependências Node
docker-compose run --rm orionone-frontend npm install
docker-compose restart orionone-frontend
```

---

### 2. Erro "connection refused" entre containers

**Sintoma:**

```
SQLSTATE[08006] could not connect to server: Connection refused
```

**Causa:** Containers em redes diferentes ou DB não iniciado

**Solução:**

```yaml
# Verificar:
networks:
    - orionone_network # Deve estar em TODOS os services

depends_on:
    orionone-db:
        condition: service_healthy # Aguarda DB estar pronto
```

---

### 3. Volumes não persistem dados

**Sintoma:**

```bash
docker-compose down
docker-compose up -d
# Dados do PostgreSQL perdidos!
```

**Causa:** Usando `docker-compose down -v` (remove volumes)

**Solução:**

```bash
# Parar sem remover volumes:
docker-compose down  # ✅ Mantém orionone_pgdata

# Remover apenas containers:
docker-compose stop
```

---

### 4. Porta já em uso

**Sintoma:**

```
Error: Bind for 0.0.0.0:8888 failed: port is already allocated
```

**Solução:**

```bash
# Descobrir quem usa a porta:
netstat -ano | findstr :8888

# Opção 1: Parar processo
taskkill /PID <PID> /F

# Opção 2: Mudar porta no docker-compose.yml
ports:
  - "8889:80"  # Usa porta 8889 no host
```

---

### 5. Build lento (cache não funciona)

**Causa:** Ordem incorreta no Dockerfile

**Ruim:**

```dockerfile
COPY . /app           # Muda sempre → invalida cache
RUN composer install  # Sempre reinstala dependências
```

**Bom:**

```dockerfile
COPY composer.json composer.lock /app/  # Só muda se dependências mudarem
RUN composer install                     # Cache aproveitado!
COPY . /app                              # Código muda frequentemente
```

---

### 6. Permissões (Linux)

**Sintoma:**

```
failed to open stream: Permission denied
```

**Causa:** Container roda como `www-data`, mas arquivos pertencem a `root`

**Solução:**

```dockerfile
RUN chown -R www-data:www-data /var/www/html/storage
RUN chmod -R 775 /var/www/html/storage
```

---

## Comandos Úteis Explicados

### Gerenciamento de Containers

```bash
# Iniciar todos os serviços
docker-compose up -d
# -d = detached (background)

# Parar sem remover
docker-compose stop

# Parar e remover containers (volumes persistem)
docker-compose down

# Reconstruir imagens
docker-compose build --no-cache
# --no-cache = ignora cache (útil após mudar Dockerfile)

# Ver logs em tempo real
docker-compose logs -f orionone-app
# -f = follow (continua mostrando novos logs)

# Executar comando em container rodando
docker-compose exec orionone-app php artisan migrate
# exec = executa dentro do container existente

# Executar comando em container temporário
docker-compose run --rm orionone-app php artisan test
# run = cria novo container (útil para testes isolados)
# --rm = remove container após execução
```

### Inspeção e Debug

```bash
# Entrar no shell do container
docker-compose exec orionone-app sh
# (Alpine usa 'sh', Ubuntu usa 'bash')

# Ver processos dentro do container
docker-compose exec orionone-app ps aux

# Ver variáveis de ambiente
docker-compose exec orionone-app env

# Ver networks
docker network ls
docker network inspect orionone_orionone_network

# Ver volumes
docker volume ls
docker volume inspect orionone_orionone_pgdata

# Ver uso de recursos
docker stats
```

### Limpeza

```bash
# Remover containers parados
docker container prune

# Remover imagens não usadas
docker image prune -a

# Remover volumes não usados
docker volume prune

# Limpar TUDO (cuidado!)
docker system prune -a --volumes
```

---

## Variações de Ambiente

### Desenvolvimento (atual)

```yaml
services:
    orionone-app:
        volumes:
            - ./:/var/www/html # Código editável
        environment:
            - APP_DEBUG=true
```

### Staging/Produção

```yaml
services:
    orionone-app:
        # Sem bind mount (código baked in na imagem)
        environment:
            - APP_DEBUG=false
            - APP_ENV=production
        restart: always # Reinicia mesmo após falha crítica
```

**Deploy em Produção:**

```bash
# Build otimizado
docker-compose -f docker-compose.prod.yml build

# Push para registry
docker tag orionone-app registry.example.com/orionone:v1.0
docker push registry.example.com/orionone:v1.0

# Pull no servidor
docker pull registry.example.com/orionone:v1.0
docker-compose -f docker-compose.prod.yml up -d
```

---

## Recursos Adicionais

### Documentação Oficial

-   [Docker Docs](https://docs.docker.com/)
-   [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
-   [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Ferramentas Úteis

-   **Portainer:** Interface gráfica para gerenciar Docker
-   **Dive:** Inspecionar layers de imagens
-   **Lazydocker:** TUI (Terminal UI) para Docker

### Aprendizado

-   [Play with Docker](https://labs.play-with-docker.com/) - Playground online
-   [Docker Curriculum](https://docker-curriculum.com/) - Tutorial interativo

---

## Próximos Passos

Agora que entende Docker, pode explorar:

1. **Multi-stage builds** (imagens menores)
2. **Docker Swarm / Kubernetes** (orquestração em produção)
3. **CI/CD com Docker** (GitHub Actions, GitLab CI)
4. **Segurança** (scanning de vulnerabilidades, secrets management)
5. **Otimização** (cache layers, imagens Alpine)

---

**Autor:** Assistente GitHub Copilot
**Projeto:** OrionOne ITSM
**Data:** Novembro 2025
