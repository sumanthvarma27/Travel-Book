"use client";
import { useEffect, useState } from 'react';
import { getTrips } from '@/lib/api';
import Link from 'next/link';

export default function SavedTrips() {
    const [trips, setTrips] = useState<any[]>([]);

    useEffect(() => {
        getTrips().then(setTrips).catch(console.error);
    }, []);

    return (
        <div className="min-h-screen bg-slate-900 text-white p-10">
            <h1 className="text-3xl font-bold mb-8">Saved Trips</h1>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {trips.map(trip => (
                    <div key={trip.id} className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                        <h2 className="text-xl font-bold mb-2">{trip.destination}</h2>
                        <span className="text-sm bg-slate-700 px-2 py-1 rounded text-gray-300">{trip.id}</span>
                    </div>
                ))}
                {trips.length === 0 && (
                    <div className="text-gray-500">No trips saved yet. Go back home to plan one!</div>
                )}
            </div>
            <Link href="/" className="mt-8 inline-block text-teal-400 hover:underline">← Back to Generator</Link>
        </div>
    );
}
