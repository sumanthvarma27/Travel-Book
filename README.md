# Agentic AI Travel Companion

Monorepo for a production-minded Agentic AI Travel Companion. This repo is organized into apps, services, shared packages, and docs. It is intentionally minimal at this phase.

## Structure
1. `apps/web` - Next.js web app (Trip Builder, Results, Saved Trips).
2. `apps/mobile` - Mobile app (future).
3. `services/api` - FastAPI backend (trips, planning, exports).
4. `services/orchestrator` - LangGraph orchestration service.
5. `services/worker` - Background worker for async tasks (future).
6. `packages/shared-schemas` - Shared Pydantic/TypeScript schemas.
7. `packages/ui` - Shared UI components (future).
8. `docs` - Product and architecture docs.
9. `infra` - Deployment and infrastructure (future).
