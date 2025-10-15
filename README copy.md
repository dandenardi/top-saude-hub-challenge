# Full‑Stack — Catálogo e Pedidos (FastAPI + Next.js + PostgreSQL + Docker)

Stack:
- Backend: FastAPI, SQLAlchemy 2 (async), Alembic, structlog, Pytest
- Frontend: Next.js 14 (App Router) + React 18 + TypeScript + Tailwind
- DB: PostgreSQL 16
- Infra: Docker/Docker Compose
- Envelope: `{ cod_retorno, mensagem, data }`

## Como rodar
```bash
cp .env.example .env
docker compose up --build -d
docker compose exec api alembic upgrade head
docker compose exec api python -m src.infrastructure.seed
```
- API: http://localhost:8000/docs
- Web: http://localhost:3000

## Testes
```bash
docker compose exec api pytest -q
```

## Uso de IA
Protótipo inicialmente gerado com auxílio de IA para scaffolding e documentação. Código revisado e ajustado manualmente.
