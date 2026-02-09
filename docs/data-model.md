Overview
This document defines the core entities and relationships for the Agentic AI Travel Companion. The model is designed for MVP SQLite storage with an upgrade path to Postgres.

Entities (ERD-style)
1. User
   - id (uuid)
   - email
   - name
   - created_at

2. Trip
   - id (uuid)
   - user_id (nullable for MVP)
   - title
   - origin
   - destinations (json array)
   - start_date
   - end_date
   - travelers (json)
   - budget (json)
   - preferences (json)
   - constraints (json)
   - created_at
   - updated_at

3. TripRun
   - id (uuid)
   - trip_id
   - status (running/success/failure)
   - input_spec (json)
   - output_plan (json)
   - created_at

4. ItineraryDay
   - id (uuid)
   - trip_id
   - date
   - city
   - summary
   - items (json array)

5. Booking
   - id (uuid)
   - trip_id
   - kind (flight/train/hotel/activity/cab)
   - provider
   - link
   - price_estimate
   - currency
   - last_checked_at

6. Reservation (future)
   - id (uuid)
   - booking_id
   - confirmation_code
   - check_in_time
   - details (json)

7. Preferences
   - id (uuid)
   - user_id
   - travel_style
   - interests (json array)
   - constraints (json)

8. Budget
   - id (uuid)
   - trip_id
   - tier
   - total_estimate
   - breakdown (json)

9. Alerts (future)
   - id (uuid)
   - user_id
   - trip_id
   - type (weather/delay/check-in)
   - message
   - created_at

10. Conversation (future)
   - id (uuid)
   - user_id
   - trip_id
   - messages (json array)
   - created_at

Relationships
1. User 1—N Trip
2. Trip 1—N TripRun
3. Trip 1—N ItineraryDay
4. Trip 1—N Booking
5. Booking 1—N Reservation (future)
6. User 1—1 Preferences (optional)

Notes
1. MVP stores ItineraryDay and Booking denormalized in TripPlan JSON, but the schema supports later normalization.
2. TripRun is the primary observability record for agent runs and outputs.
3. User is optional in MVP; trips can be anonymous.
