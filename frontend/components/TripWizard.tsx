"use client";
import { useState } from 'react';
import { TripSpec } from '@/lib/types';
import { createPlan } from '@/lib/api';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function TripWizard() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState<TripSpec>({
        origin: '',
        destination: '',
        dates: '',
        travelers: 1,
        budget_tier: 'medium',
        travel_style: 'pleasure',
        interests: [],
        constraints: []
    });

    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [groupType, setGroupType] = useState<'solo' | 'couple' | 'family' | 'friends'>('solo');
    const [selectedInterests, setSelectedInterests] = useState<string[]>([]);

    const handleChange = (e: any) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const toggleInterest = (interest: string) => {
        setSelectedInterests(prev =>
            prev.includes(interest)
                ? prev.filter(i => i !== interest)
                : [...prev, interest]
        );
    };

    const getTravelersCount = (type: string) => {
        switch (type) {
            case 'solo': return 1;
            case 'couple': return 2;
            case 'family': return 4;
            case 'friends': return 3;
            default: return 1;
        }
    };

    const handleSubmit = async (e: any) => {
        e.preventDefault();
        setLoading(true);
        try {
            const dateRange = startDate && endDate ? `${startDate} to ${endDate}` : formData.dates;
            const submissionData = {
                ...formData,
                dates: dateRange,
                travelers: getTravelersCount(groupType),
                interests: selectedInterests
            };
            const plan = await createPlan(submissionData);
            localStorage.setItem('currentPlan', JSON.stringify(plan));
            router.push('/trip');
        } catch (error) {
            console.error(error);
            alert("Failed to generate plan. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const containerVariants = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0 }
    };

    const glassClass = "bg-black/60 backdrop-blur-xl border border-white/10 rounded-xl p-3 shadow-lg transition-all hover:border-white/20";
    const labelClass = "block text-[10px] font-bold text-gray-300 uppercase tracking-wider mb-1";
    const inputClass = "w-full bg-white/5 border border-white/10 rounded-lg py-2 px-3 text-sm text-white placeholder-gray-500 focus:ring-1 focus:ring-teal-500/50 focus:border-teal-500/50 outline-none transition-all";

    return (
        <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="show"
            className="w-full max-w-[420px] flex flex-col gap-2"
        >
            {loading ? (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className={`${glassClass} flex flex-col items-center justify-center py-12 space-y-4`}
                >
                    <div className="relative">
                        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-500"></div>
                        <div className="absolute inset-0 animate-ping rounded-full h-12 w-12 border border-teal-500/30"></div>
                    </div>
                    <p className="text-sm text-teal-200 animate-pulse">Crafting your itinerary...</p>
                </motion.div>
            ) : (
                <form onSubmit={handleSubmit} className="flex flex-col gap-2">

                    {/* From & To - Split Floating Blocks */}
                    <div className="grid grid-cols-2 gap-2">
                        <motion.div variants={itemVariants} className={glassClass}>
                            <label className={labelClass}>From</label>
                            <input
                                name="origin"
                                value={formData.origin}
                                onChange={handleChange}
                                placeholder="City..."
                                className={inputClass}
                                required
                            />
                        </motion.div>
                        <motion.div variants={itemVariants} className={glassClass}>
                            <label className={labelClass}>To</label>
                            <input
                                name="destination"
                                value={formData.destination}
                                onChange={handleChange}
                                placeholder="City..."
                                className={inputClass}
                                required
                            />
                        </motion.div>
                    </div>

                    {/* Dates - Split Floating Blocks */}
                    <div className="grid grid-cols-2 gap-2">
                        <motion.div variants={itemVariants} className={glassClass}>
                            <label className={labelClass}>Start</label>
                            <input
                                type="date"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                className={inputClass}
                                required
                            />
                        </motion.div>
                        <motion.div variants={itemVariants} className={glassClass}>
                            <label className={labelClass}>End</label>
                            <input
                                type="date"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className={inputClass}
                                required
                            />
                        </motion.div>
                    </div>

                    {/* Peeps - Floating Block (Kept as one for cohesion) */}
                    <motion.div variants={itemVariants} className={glassClass}>
                        <label className={labelClass}>Travelers</label>
                        <div className="grid grid-cols-4 gap-2">
                            {[
                                { value: 'solo', label: 'Solo' },
                                { value: 'couple', label: 'Couple' },
                                { value: 'family', label: 'Family' },
                                { value: 'friends', label: 'Friends' }
                            ].map((type) => (
                                <button
                                    key={type.value}
                                    type="button"
                                    onClick={() => setGroupType(type.value as any)}
                                    className={`py-2 px-1 flex flex-col items-center justify-center rounded-lg transition-all border ${groupType === type.value
                                        ? 'bg-teal-500 border-teal-500 text-black shadow-lg shadow-teal-500/20'
                                        : 'bg-white/5 border-transparent text-gray-400 hover:bg-white/10 hover:text-white'
                                        }`}
                                >
                                    <span className="text-[10px] font-bold uppercase">{type.label}</span>
                                </button>
                            ))}
                        </div>
                    </motion.div>

                    {/* Purpose & Budget - Split Floating Blocks */}
                    <div className="grid grid-cols-2 gap-2">
                        <motion.div variants={itemVariants} className={glassClass}>
                            <label className={labelClass}>Vibe</label>
                            <div className="relative group">
                                <select
                                    name="travel_style"
                                    value={formData.travel_style}
                                    onChange={handleChange}
                                    className={`${inputClass} appearance-none cursor-pointer hover:bg-white/10 transition-colors pr-8`}
                                >
                                    <option value="pleasure" className="bg-neutral-900">Pleasure</option>
                                    <option value="work" className="bg-neutral-900">Work</option>
                                    <option value="business" className="bg-neutral-900">Business</option>
                                </select>
                                <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400 group-hover:text-white transition-colors">
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                                </div>
                            </div>
                        </motion.div>
                        <motion.div variants={itemVariants} className={glassClass}>
                            <label className={labelClass}>Budget</label>
                            <div className="relative group">
                                <select
                                    name="budget_tier"
                                    value={formData.budget_tier}
                                    onChange={handleChange}
                                    className={`${inputClass} appearance-none cursor-pointer hover:bg-white/10 transition-colors pr-8`}
                                >
                                    <option value="low" className="bg-neutral-900">$ Low</option>
                                    <option value="medium" className="bg-neutral-900">$$ Medium</option>
                                    <option value="high" className="bg-neutral-900">$$$ High</option>
                                </select>
                                <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400 group-hover:text-white transition-colors">
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                                </div>
                            </div>
                        </motion.div>
                    </div>

                    {/* Interests - Floating Block (Optional) */}
                    <motion.div variants={itemVariants} className={glassClass}>
                        <label className={labelClass}>Interests</label>
                        <div className="flex flex-wrap gap-2">
                            {['Food', 'Shopping', 'Explore', 'Heritage', 'Relax'].map((interest) => (
                                <button
                                    key={interest}
                                    type="button"
                                    onClick={() => toggleInterest(interest.toLowerCase())}
                                    className={`py-1.5 px-4 rounded-full text-xs font-bold uppercase tracking-wide transition-all border ${selectedInterests.includes(interest.toLowerCase())
                                        ? 'bg-teal-500 border-teal-500 text-black'
                                        : 'bg-transparent border-white/20 text-gray-400 hover:border-white/50 hover:text-white'
                                        }`}
                                >
                                    {interest}
                                </button>
                            ))}
                        </div>
                    </motion.div>

                    {/* Submit Button - Floating */}
                    <motion.button
                        variants={itemVariants}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        type="submit"
                        className="w-full bg-teal-500 hover:bg-teal-400 text-black font-bold text-lg py-3 rounded-xl shadow-xl shadow-teal-500/20 transition-all flex justify-center items-center gap-2 mt-1"
                    >
                        <span>Let's Go</span>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                        </svg>
                    </motion.button>

                </form>
            )}
        </motion.div>
    );
}
