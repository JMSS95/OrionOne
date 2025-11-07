# Arquitetura do OrionOne

## Padrão Arquitetural

OrionOne segue uma arquitetura MVC (Model-View-Controller) com camada de serviços.

## Camadas

### Presentation Layer

-   Inertia.js pages (Vue 3 components)
-   Controllers (request handling)

### Business Logic Layer

-   Services (business rules)
-   Policies (authorization)

### Data Layer

-   Eloquent Models
-   Repositories (future)

## Diagrama

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP
┌──────▼──────┐
│   Inertia   │
└──────┬──────┘
       │
┌──────▼──────┐      ┌──────────┐
│ Controllers │─────>│ Services │
└──────┬──────┘      └─────┬────┘
       │                   │
       │              ┌────▼────┐
       └─────────────>│ Models  │
                      └────┬────┘
                           │
                      ┌────▼─────┐
                      │PostgreSQL│
                      └──────────┘
```
