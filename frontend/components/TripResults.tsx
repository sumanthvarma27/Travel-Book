"use client";
import { useState, useRef } from 'react';
import { TripPlan } from '@/lib/types';
import { motion, AnimatePresence } from 'framer-motion';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

type TabType = 'places' | 'flights' | 'hotels' | 'itinerary' | 'packing';

export default function TripResults({ plan }: { plan: TripPlan }) {
    const [activeTab, setActiveTab] = useState<TabType>('itinerary');
    const contentRef = useRef<HTMLDivElement>(null);

    const handlePrint = async () => {
        if (!contentRef.current) return;
        const canvas = await html2canvas(contentRef.current);
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save('trip-plan.pdf');
    };

    const downloadJSON = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(plan, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "trip-plan.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    const origin = plan.origin || plan.itinerary?.[0]?.city || 'Your City';
    const destination = plan.destination || plan.itinerary?.[plan.itinerary.length - 1]?.city || 'Destination';

    const icons = [
        { id: 'itinerary' as TabType, label: 'Itinerary', emoji: '🗓️', color: 'from-teal-500 to-emerald-500' },
        { id: 'places' as TabType, label: 'Places to Visit', emoji: '📍', color: 'from-purple-500 to-indigo-500' },
        { id: 'flights' as TabType, label: 'Flight Tickets', emoji: '✈️', color: 'from-blue-500 to-cyan-500' },
        { id: 'hotels' as TabType, label: 'Accommodation', emoji: '🏨', color: 'from-orange-500 to-amber-500' },
        { id: 'packing' as TabType, label: 'Packing List', emoji: '🎒', color: 'from-pink-500 to-rose-500' },
    ];

    // Group packing list by category
    const packingByCategory: Record<string, string[]> = {};
    (plan.packing_list || []).forEach((item) => {
        const cat = item.category || 'General';
        if (!packingByCategory[cat]) packingByCategory[cat] = [];
        packingByCategory[cat].push(item.item);
    });

    return (
        <div className="min-h-screen text-white p-4 md:p-8" ref={contentRef}>
            {/* Header */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-7xl mx-auto mb-10 flex flex-col md:flex-row justify-between items-center gap-4"
            >
                <div>
                    <h1 className="text-4xl md:text-5xl font-bold bg-linear-to-r from-teal-200 via-white to-blue-200 bg-clip-text text-transparent">
                        {origin} → {destination}
                    </h1>
                    <p className="text-gray-400 mt-2 text-lg max-w-2xl">{plan.summary}</p>
                </div>
                <div className="flex gap-3">
                    <button onClick={handlePrint} className="px-5 py-2 bg-white/5 border border-white/10 rounded-full hover:bg-white/10 transition flex items-center gap-2">
                        <span>🖨️</span> Print
                    </button>
                    <button onClick={downloadJSON} className="px-5 py-2 bg-teal-500/10 border border-teal-500/20 text-teal-300 rounded-full hover:bg-teal-500/20 transition flex items-center gap-2">
                        <span>💾</span> Export
                    </button>
                </div>
            </motion.div>

            {/* Budget Overview Bar */}
            {plan.budget && (
                <div className="max-w-7xl mx-auto mb-8">
                    <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-lg font-bold text-white">💰 Budget Overview</h3>
                            <span className="text-2xl font-bold text-teal-400">
                                ${plan.budget.total_estimated?.toLocaleString()} {plan.budget.currency || 'USD'}
                            </span>
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                            {[
                                { label: 'Flights', value: plan.budget.flights, color: 'text-blue-400' },
                                { label: 'Hotels', value: plan.budget.accommodation, color: 'text-orange-400' },
                                { label: 'Activities', value: plan.budget.activities, color: 'text-purple-400' },
                                { label: 'Food', value: plan.budget.food, color: 'text-green-400' },
                                { label: 'Transport', value: plan.budget.transport_local, color: 'text-cyan-400' },
                            ].map((item) => (
                                <div key={item.label} className="text-center">
                                    <div className={`text-lg font-bold ${item.color}`}>${item.value?.toLocaleString() || 0}</div>
                                    <div className="text-xs text-gray-500">{item.label}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Tab Navigation - 5 tabs */}
            <div className="max-w-7xl mx-auto mb-8">
                <div className="flex flex-wrap justify-center gap-3">
                    {icons.map((item, index) => (
                        <motion.button
                            key={item.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                            onClick={() => setActiveTab(item.id)}
                            className={`
                                px-5 py-3 rounded-xl flex items-center gap-2 font-medium transition-all duration-300
                                ${activeTab === item.id
                                    ? 'bg-teal-500/20 border-2 border-teal-500/50 text-teal-300 shadow-lg shadow-teal-500/10'
                                    : 'bg-white/5 border border-white/10 text-gray-400 hover:bg-white/10 hover:text-white'
                                }
                            `}
                        >
                            <span className="text-xl">{item.emoji}</span>
                            <span className="hidden md:inline">{item.label}</span>
                        </motion.button>
                    ))}
                </div>
            </div>

            {/* Tab Content */}
            <div className="max-w-7xl mx-auto bg-slate-900/40 backdrop-blur-xl border border-white/10 rounded-3xl p-8 min-h-125">
                <AnimatePresence mode="wait">

                    {/* ===== ITINERARY TAB ===== */}
                    {activeTab === 'itinerary' && (
                        <motion.div
                            key="itinerary"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-6"
                        >
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-2xl font-bold text-white">🗓️ Day-by-Day Itinerary</h2>
                                <div className="text-sm text-gray-400">{plan.itinerary?.length || 0} days planned</div>
                            </div>

                            {(plan.itinerary || []).map((day) => (
                                <div key={day.day_number} className="bg-white/5 border border-white/5 rounded-2xl p-6 hover:border-teal-500/30 transition-colors">
                                    <div className="flex justify-between items-center mb-4 pb-4 border-b border-white/5">
                                        <div className="flex items-center gap-4">
                                            <div className="w-12 h-12 rounded-xl bg-teal-500/20 flex items-center justify-center text-teal-300 font-bold text-lg">
                                                {day.day_number}
                                            </div>
                                            <div>
                                                <h3 className="text-lg font-bold text-white">Day {day.day_number} — {day.city}</h3>
                                                <span className="text-sm text-gray-400">{day.date}</span>
                                            </div>
                                        </div>
                                        {day.weather && (
                                            <div className="flex items-center gap-2 bg-blue-500/10 px-4 py-2 rounded-xl border border-blue-500/10">
                                                <span className="text-xl">
                                                    {day.weather.condition?.toLowerCase().includes('rain') ? '🌧️' :
                                                     day.weather.condition?.toLowerCase().includes('cloud') ? '☁️' :
                                                     day.weather.condition?.toLowerCase().includes('snow') ? '❄️' : '☀️'}
                                                </span>
                                                <div>
                                                    <div className="text-sm font-semibold text-blue-200">{day.weather.temperature_c}°C</div>
                                                    <div className="text-xs text-blue-300/70">{day.weather.condition}</div>
                                                </div>
                                            </div>
                                        )}
                                    </div>

                                    {/* Timeline */}
                                    <div className="space-y-4">
                                        {/* Morning */}
                                        {(day.morning_activities || []).length > 0 && (
                                            <div>
                                                <div className="text-xs font-bold text-yellow-400/80 uppercase tracking-widest mb-2">🌅 Morning</div>
                                                {day.morning_activities.map((act, i) => (
                                                    <ActivityCard key={`m-${i}`} activity={act} />
                                                ))}
                                            </div>
                                        )}
                                        {/* Afternoon */}
                                        {(day.afternoon_activities || []).length > 0 && (
                                            <div>
                                                <div className="text-xs font-bold text-orange-400/80 uppercase tracking-widest mb-2">☀️ Afternoon</div>
                                                {day.afternoon_activities.map((act, i) => (
                                                    <ActivityCard key={`a-${i}`} activity={act} />
                                                ))}
                                            </div>
                                        )}
                                        {/* Evening */}
                                        {(day.evening_activities || []).length > 0 && (
                                            <div>
                                                <div className="text-xs font-bold text-purple-400/80 uppercase tracking-widest mb-2">🌙 Evening</div>
                                                {day.evening_activities.map((act, i) => (
                                                    <ActivityCard key={`e-${i}`} activity={act} />
                                                ))}
                                            </div>
                                        )}
                                        {/* Meals */}
                                        {(day.meal_suggestions || []).length > 0 && (
                                            <div className="mt-4 p-3 bg-green-500/5 border border-green-500/10 rounded-xl">
                                                <div className="text-xs font-bold text-green-400/80 uppercase tracking-widest mb-2">🍽️ Meal Suggestions</div>
                                                <div className="flex flex-wrap gap-2">
                                                    {day.meal_suggestions.map((meal, i) => (
                                                        <span key={i} className="text-sm text-green-300/80 bg-green-500/10 px-3 py-1 rounded-lg">{meal}</span>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </motion.div>
                    )}

                    {/* ===== PLACES TO VISIT TAB ===== */}
                    {activeTab === 'places' && (
                        <motion.div
                            key="places"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-8"
                        >
                            <h2 className="text-2xl font-bold text-white mb-6">📍 Places to Visit</h2>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {(plan.itinerary || []).flatMap((day) =>
                                    [...(day.morning_activities || []), ...(day.afternoon_activities || []), ...(day.evening_activities || [])]
                                ).filter((act, i, arr) =>
                                    arr.findIndex(a => a.name === act.name) === i
                                ).map((activity, i) => (
                                    <div key={i} className="bg-white/5 border border-white/5 rounded-2xl p-5 hover:border-purple-500/30 transition-colors group">
                                        <h4 className="font-bold text-lg text-white mb-2 group-hover:text-purple-300 transition-colors">{activity.name}</h4>
                                        <p className="text-sm text-gray-400 mb-3">{activity.description}</p>
                                        <div className="flex items-center justify-between text-xs text-gray-500">
                                            <span>📍 {activity.location}</span>
                                            <span className="text-teal-400 font-semibold">${activity.estimated_cost}</span>
                                        </div>
                                        {activity.booking_link && (
                                            <a href={activity.booking_link} target="_blank" rel="noopener noreferrer"
                                                className="mt-3 inline-block px-3 py-1 bg-purple-500/20 text-purple-300 text-xs rounded-lg hover:bg-purple-500/30 transition-colors">
                                                Book Now ↗
                                            </a>
                                        )}
                                    </div>
                                ))}
                            </div>

                            {plan.activity_platforms && Object.keys(plan.activity_platforms).length > 0 && (
                                <div className="mt-8 bg-white/5 border border-white/5 rounded-2xl p-6">
                                    <h3 className="text-xl font-bold text-white mb-4">🎫 Book Experiences & Tours</h3>
                                    <div className="flex flex-wrap gap-4">
                                        {Object.entries(plan.activity_platforms).map(([name, url]) => (
                                            <a key={name} href={url} target="_blank" rel="noopener noreferrer"
                                                className="px-5 py-3 bg-teal-500/10 border border-teal-500/20 hover:bg-teal-500/20 text-teal-300 rounded-xl transition-all flex items-center gap-2 font-medium">
                                                {name} ↗
                                            </a>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    )}

                    {/* ===== FLIGHT TICKETS TAB ===== */}
                    {activeTab === 'flights' && (
                        <motion.div
                            key="flights"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                        >
                            <h2 className="text-2xl font-bold text-white mb-6">✈️ Flight Tickets & Transportation</h2>

                            <div className="bg-linear-to-br from-blue-900/50 to-blue-800/20 border border-blue-500/20 p-6 rounded-2xl mb-8">
                                <div className="text-blue-400 text-sm font-semibold uppercase tracking-wider mb-2">Estimated Flight Cost</div>
                                <div className="text-4xl font-bold text-white">${plan.budget?.flights || 0}</div>
                                <div className="text-blue-400/60 text-xs mt-1">Round trip for {plan.itinerary?.length || 1} days</div>
                            </div>

                            {plan.intercity_travel && plan.intercity_travel.length > 0 && (
                                <div className="space-y-6 mb-8">
                                    <h3 className="text-xl font-bold text-white mb-4">🎫 Available Routes</h3>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        {plan.intercity_travel.map((flight, i) => (
                                            <div key={i} className="bg-white/5 border border-white/10 rounded-2xl p-6 hover:border-blue-500/30 transition-colors">
                                                <div className="flex justify-between items-start mb-4">
                                                    <div>
                                                        <h4 className="font-bold text-lg text-white">{flight.from} → {flight.to}</h4>
                                                        <p className="text-sm text-gray-400">{flight.mode || 'Flight'}</p>
                                                    </div>
                                                    <div className="text-right">
                                                        <div className="text-2xl font-bold text-blue-400">${flight.estimated_cost}</div>
                                                        <div className="text-xs text-gray-500">per person</div>
                                                    </div>
                                                </div>
                                                {flight.booking_link && (
                                                    <a href={flight.booking_link} target="_blank" rel="noopener noreferrer"
                                                        className="mt-4 w-full block text-center px-4 py-2 bg-blue-500/20 text-blue-300 rounded-lg hover:bg-blue-500/30 transition-colors">
                                                        Book ↗
                                                    </a>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            <div className="bg-white/5 border border-white/5 rounded-2xl p-6">
                                <h3 className="text-xl font-bold text-white mb-4">🔍 Find Best Flight Deals</h3>
                                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                    {[
                                        { name: 'Google Flights', url: `https://www.google.com/travel/flights?q=flights+from+${encodeURIComponent(origin)}+to+${encodeURIComponent(destination)}` },
                                        { name: 'Skyscanner', url: `https://www.skyscanner.com/transport/flights/${encodeURIComponent(origin)}/${encodeURIComponent(destination)}` },
                                        { name: 'Kayak', url: `https://www.kayak.com/flights/${encodeURIComponent(origin)}-${encodeURIComponent(destination)}` },
                                        { name: 'Expedia', url: `https://www.expedia.com/Flights` },
                                        { name: 'Momondo', url: `https://www.momondo.com/flight-search/${encodeURIComponent(origin)}-${encodeURIComponent(destination)}` },
                                        { name: 'CheapOair', url: `https://www.cheapoair.com/` }
                                    ].map((platform) => (
                                        <a key={platform.name} href={platform.url} target="_blank" rel="noopener noreferrer"
                                            className="px-5 py-3 bg-blue-500/10 border border-blue-500/20 hover:bg-blue-500/20 text-blue-300 rounded-xl transition-all flex items-center justify-center gap-2 font-medium">
                                            {platform.name} ↗
                                        </a>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* ===== HOTELS TAB ===== */}
                    {activeTab === 'hotels' && (
                        <motion.div
                            key="hotels"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                        >
                            <h2 className="text-2xl font-bold text-white mb-6">🏨 Accommodation Options</h2>

                            <div className="bg-linear-to-br from-orange-900/50 to-orange-800/20 border border-orange-500/20 p-6 rounded-2xl mb-8">
                                <div className="text-orange-400 text-sm font-semibold uppercase tracking-wider mb-2">Estimated Accommodation Cost</div>
                                <div className="text-4xl font-bold text-white">${plan.budget?.accommodation || 0}</div>
                                <div className="text-orange-400/60 text-xs mt-1">For {plan.itinerary?.length || 1} nights</div>
                            </div>

                            <h3 className="text-xl font-bold text-white mb-4">Recommended Hotels</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                                {(plan.hotels_shortlist || []).map((hotel, i) => (
                                    <div key={i} className="group bg-slate-800/50 p-5 rounded-xl border border-white/5 hover:border-orange-500/30 transition-all">
                                        <h4 className="font-bold text-lg text-white mb-2">{hotel.name}</h4>
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="text-sm text-gray-400">📍 {hotel.area}</span>
                                            {hotel.rating && <span className="text-yellow-400 text-sm">⭐ {hotel.rating}/5</span>}
                                        </div>
                                        <p className="text-xs text-gray-500 mb-3 line-clamp-2">{hotel.description}</p>
                                        <div className="flex items-center justify-between pt-3 border-t border-white/5">
                                            <span className="text-lg font-bold text-teal-400">${hotel.price_per_night}/night</span>
                                            {hotel.booking_link && (
                                                <a href={hotel.booking_link} target="_blank" rel="noopener noreferrer"
                                                    className="px-3 py-1 bg-orange-500/20 text-orange-300 text-xs rounded-lg hover:bg-orange-500/30 transition-colors">
                                                    View ↗
                                                </a>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {plan.booking_platforms && Object.keys(plan.booking_platforms).length > 0 && (
                                <div className="bg-white/5 border border-white/5 rounded-2xl p-6">
                                    <h3 className="text-xl font-bold text-white mb-4">🔍 Compare Prices</h3>
                                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                                        {Object.entries(plan.booking_platforms).map(([name, url]) => (
                                            <a key={name} href={url} target="_blank" rel="noopener noreferrer"
                                                className="px-5 py-3 bg-orange-500/10 border border-orange-500/20 hover:bg-orange-500/20 text-orange-300 rounded-xl transition-all flex items-center justify-center gap-2 font-medium text-sm">
                                                {name} ↗
                                            </a>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    )}

                    {/* ===== PACKING LIST TAB ===== */}
                    {activeTab === 'packing' && (
                        <motion.div
                            key="packing"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                        >
                            <h2 className="text-2xl font-bold text-white mb-6">🎒 Packing List</h2>

                            {Object.keys(packingByCategory).length > 0 ? (
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {Object.entries(packingByCategory).map(([category, items]) => {
                                        const categoryEmojis: Record<string, string> = {
                                            'Clothing': '👕', 'Clothes': '👕', 'Essentials': '🎒', 'Documents': '📄',
                                            'Toiletries': '🧴', 'Electronics': '📱', 'Health': '💊', 'Medicine': '💊',
                                            'Accessories': '🕶️', 'Footwear': '👟', 'Shoes': '👟', 'Weather': '☂️',
                                            'Miscellaneous': '📦', 'General': '📦', 'Tech': '💻', 'Travel': '✈️',
                                        };
                                        const emoji = categoryEmojis[category] || '📦';

                                        return (
                                            <div key={category} className="bg-white/5 border border-white/5 rounded-2xl p-5">
                                                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                                                    <span>{emoji}</span> {category}
                                                </h3>
                                                <div className="space-y-2">
                                                    {items.map((item, i) => (
                                                        <label key={i} className="flex items-center gap-3 text-sm text-gray-300 hover:text-white cursor-pointer group">
                                                            <input type="checkbox" className="w-4 h-4 rounded border-gray-600 bg-transparent text-teal-500 focus:ring-teal-500/30" />
                                                            <span className="group-hover:text-teal-300 transition-colors">{item}</span>
                                                        </label>
                                                    ))}
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            ) : (
                                <div className="text-center py-16 text-gray-500">
                                    <div className="text-6xl mb-4">🎒</div>
                                    <p>No packing list available for this trip.</p>
                                </div>
                            )}
                        </motion.div>
                    )}

                </AnimatePresence>
            </div>
        </div>
    );
}

/* Reusable Activity Card */
function ActivityCard({ activity }: { activity: { name: string; description: string; location: string; estimated_cost: number; booking_link?: string; time_slot: string } }) {
    return (
        <div className="relative pl-6 border-l-2 border-white/10 hover:border-teal-500/50 transition-colors mb-4">
            <div className="absolute -left-2.25 top-1 w-4 h-4 rounded-full bg-slate-900 border-2 border-teal-500"></div>
            <div className="mb-1 text-xs font-mono text-teal-400 uppercase tracking-widest">{activity.time_slot}</div>
            <h4 className="font-semibold text-base text-white">{activity.name}</h4>
            <p className="text-sm text-gray-400 mb-2">{activity.description}</p>
            <div className="flex items-center gap-4 text-xs text-gray-500">
                <span>📍 {activity.location}</span>
                <span>💰 ${activity.estimated_cost}</span>
            </div>
            {activity.booking_link && (
                <a href={activity.booking_link} target="_blank" rel="noopener noreferrer"
                    className="mt-2 inline-block px-3 py-1 bg-teal-500/20 text-teal-300 text-xs rounded-lg hover:bg-teal-500/30 transition-colors">
                    Book Now ↗
                </a>
            )}
        </div>
    );
}