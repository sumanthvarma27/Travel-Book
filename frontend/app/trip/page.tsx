"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import TripResults from '@/components/TripResults';
import { TripPlan } from '@/lib/types';

export default function ResultsPage() {
    const router = useRouter();
    const [plan, setPlan] = useState<TripPlan | null>(null);

    useEffect(() => {
        const stored = localStorage.getItem('currentPlan');
        if (!stored) {
            router.push('/');
            return;
        }
        setPlan(JSON.parse(stored));
    }, [router]);

    if (!plan) {
        return (
            <div className="min-h-screen bg-[#0b1121] flex items-center justify-center">
                <div className="text-white text-xl">Loading your trip...</div>
            </div>
        );
    }

    return <TripResults plan={plan} />;
}
