Vision
Build a production-minded Agentic AI Travel Companion that plans multi-city trips with realistic budgets and actionable booking links, while keeping estimates transparent and data sources attributable. The MVP emphasizes reliable, structured outputs (JSON + Markdown), real-time-ish context (weather + search), and an architecture that can scale to real provider integrations without rewrites.

Target users
1. Solo traveler: wants efficient planning, budget clarity, and easy booking links.
2. Family planner: needs constraints (kid-friendly, walking limits), safety tips, and predictable costs.
3. Business traveler: prioritizes time windows, transit reliability, and lodging near venues.
4. Backpacker: prefers budget tiers, local transport tips, and flexible itineraries.

Core flows (plan → book → travel → replan)
1. Plan: user enters TripSpec (origin, destinations, dates, travelers, budget, style, interests, constraints) and receives a structured TripPlan with daily itinerary, budget, packing list, and shortlists.
2. Book: user reviews flight/train/hotel/activity options with deep links and a booking checklist; estimates labeled as such with “last checked” timestamps where applicable.
3. Travel: day-of view shows that day’s itinerary, local transport tips, weather snapshot, and reservations.
4. Replan: user changes constraints or disruptions occur (weather changes, delays); system regenerates only impacted days/legs with a diffs-friendly update.

Feature list (P0/P1/P2)
P0 (MVP)
1. TripSpec input with validation (multi-city, constraints, budget tier/amount, travel style).
2. TripPlan output with day-by-day itinerary, budget breakdown, packing list, hotel shortlist, and transport tips.
3. Real-time-ish data: Open-Meteo weather + search-based activities/hotels; booking adapters are mockable.
4. Export: Downloadable Markdown and JSON.
5. Agentic orchestration with retries and structured JSON outputs per agent.
6. Observability: run_id, logs of prompts/tool calls/outputs in SQLite.
7. Safety: guardrails against “exact prices,” explicit estimation language, citations for sources/links.

P1 (V1)
1. Accounts, saved trips, and re-planning during travel.
2. Notifications for schedule, weather, and booking reminders.
3. Map view with route visualization and daily walking estimates.
4. Provider adapters for at least flights + hotels + activities (real APIs when keys present).
5. Price snapshots and “last checked” display with refresh.

P2 (Later)
1. Offline mode with cached itineraries and reservations.
2. Team travel and shared editing.
3. Advanced personalization (loyalty programs, visa checks, accessibility).
4. Multi-language support and currency conversions.

Non-functional requirements
1. Latency: initial planning response under 30 seconds for typical 3–7 day trips; partial replans under 15 seconds.
2. Reliability: tool retries with backoff; planner can re-run specific agents up to N times; graceful degradation to mock adapters.
3. Data integrity: strict schema validation (Pydantic) for all agent outputs and final plan.
4. Privacy/security: store minimal PII; redact logs; secrets in environment variables only; audit logging for run_id.
5. Observability: per-run traces in SQLite with prompt/tool/output snapshots; searchable by run_id.

Out of scope (for now)
1. Mobile app and push notifications.
2. Full live booking and payments.
3. Real-time disruption feeds beyond weather (airline live ops).
4. Complex loyalty point optimization.
