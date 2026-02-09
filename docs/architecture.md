Vision
Define a production-minded system architecture for an Agentic AI Travel Companion that can evolve from MVP to V1 without rewrites. The architecture separates the web app, API, orchestration, and data services with clear boundaries and upgrade paths.

Architecture style
Platform + Agents
The platform provides API, storage, auth, and integrations. The agentic orchestrator performs planning and synthesis using structured schemas and tool adapters.

Components
1. Web app (Next.js)
   - Trip Builder Wizard
   - Results view (Itinerary/Budget/Bookings/Weather/Packing)
   - Saved trips

2. Mobile app (future)
   - Offline itinerary and notifications
   - Travel-day quick actions

3. Backend API (FastAPI)
   - Trip CRUD
   - Plan generation and export
   - Saved runs and plan retrieval
   - User accounts in V1

4. Orchestrator (LangGraph)
   - Multi-agent graph with retries and validation
   - Structured output via Pydantic schemas

5. Data stores
   - MVP: SQLite (trips, runs, outputs, logs)
   - V1: Postgres

6. Cache and rate limits
   - MVP: in-memory + SQLite cache
   - V1: Redis

7. Queue and background workers
   - MVP: synchronous execution
   - V1: task queue for re-planning, refresh, and notifications

8. Observability
   - Run logs and tool traces in DB
   - V1: OpenTelemetry + dashboards

High-level flow
1. User submits TripSpec from web app.
2. API validates and calls orchestrator.
3. Orchestrator runs agents and tools.
4. Planner validates TripPlan, retries as needed.
5. API stores outputs and returns TripPlan.
6. Web app renders results and allows export.

Data boundaries
1. Web app
   - Only handles public plan data for display and export.

2. API
   - Owns persistence and access control.
   - Exposes only validated schemas.

3. Orchestrator
   - Isolated from web concerns.
   - Uses tool adapters with strict interfaces.

Upgrade path
1. Replace SQLite with Postgres.
2. Add Redis cache + rate limiting.
3. Add background workers for re-planning.
4. Add real provider adapters with secrets.
5. Introduce mobile client.
