import { TripSpec, TripPlan } from './types';

const API_BASE = 'http://localhost:8000';

export async function createPlan(spec: TripSpec): Promise<TripPlan> {
    const res = await fetch(`${API_BASE}/plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(spec),
    });

    if (!res.ok) {
        throw new Error('Failed to generate plan');
    }

    const data = await res.json();
    if (data.status === 'failed') {
        throw new Error(data.error || 'Plan generation failed');
    }
    return data.plan;
}

export async function getTrips() {
    const res = await fetch(`${API_BASE}/trips`);
    return res.json();
}
