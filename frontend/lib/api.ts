import { TripSpec, TripPlan } from './types';

const API_BASE = 'http://localhost:8000';

export async function createPlan(spec: TripSpec): Promise<TripPlan> {
    const res = await fetch(`${API_BASE}/plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(spec),
    });

    const data = await res.json();

    if (!res.ok) {
        const errorMsg = typeof data.detail === 'string'
            ? data.detail
            : (data.detail?.error || data.error || 'Failed to generate plan');
        throw new Error(errorMsg);
    }

    if (data.status === 'failed') {
        throw new Error(data.error || 'Plan generation failed');
    }

    // Ensure origin and destination are set on the plan
    const plan = data.plan as TripPlan;
    if (!plan.origin) plan.origin = spec.origin;
    if (!plan.destination) plan.destination = spec.destination;

    return plan;
}

export async function getTrips() {
    const res = await fetch(`${API_BASE}/trips`);
    return res.json();
}