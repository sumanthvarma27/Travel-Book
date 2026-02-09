"use client";
import { useState, useRef } from 'react';
import { TripPlan } from '@/lib/types';
import { motion, AnimatePresence } from 'framer-motion';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

type TabType = 'places' | 'flights' | 'hotels' | 'itinerary' | 'packing';

export default function TripResults({ plan }: { plan: TripPlan }) {
    const [activeTab, setActiveTab] = useState<TabType>('places');
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

    // Get origin and destination from plan
    const origin = plan.itinerary?.[0]?.city || 'Your City';
    const destination = plan.itinerary?.[plan.itinerary.length - 1]?.city || 'Destination';

    const icons = [
        { id: 'places' as TabType, label: 'Places to Visit', icon: '/assets/icons/attractions.png', color: 'from-purple-500 to-indigo-500' },
        { id: 'flights' as TabType, label: 'Flight Tickets', icon: '/assets/icons/flight.png', color: 'from-blue-500 to-cyan-500' },
        { id: 'hotels' as TabType, label: 'Accommodation', icon: '/assets/icons/hotel.png', color: 'from-orange-500 to-amber-500' },
    ];

    return (
        <div className="min-h-screen text-white p-4 md:p-8" ref={contentRef}>
            {/* Header / Title */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-7xl mx-auto mb-10 flex flex-col md:flex-row justify-between items-center gap-4"
            >
                <div>
                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-teal-200 via-white to-blue-200 bg-clip-text text-transparent">
                        {origin} → {destination}
                    </h1>
                    <p className="text-gray-400 mt-2 text-lg max-w-2xl">{plan.summary}</p>
                </div>
                <div className="flex gap-3">
                    <button onClick={handlePrint} className="px-5 py-2 bg-white/5 border border-white/10 rounded-full hover:bg-white/10 transition flex items-center gap-2">
                        <span>🖨️</span> Print Itinerary
                    </button>
                    <button onClick={downloadJSON} className="px-5 py-2 bg-teal-500/10 border border-teal-500/20 text-teal-300 rounded-full hover:bg-teal-500/20 transition flex items-center gap-2">
                        <span>💾</span> Export JSON
                    </button>
                </div>
            </motion.div>

            {/* 3D Icon Menu - Only 3 icons */}
            <div className="max-w-7xl mx-auto mb-12">
                <div className="grid grid-cols-3 gap-6 max-w-4xl mx-auto">
                    {icons.map((item, index) => (
                        <motion.div
                            key={item.id}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ y: -10, scale: 1.05 }}
                            onClick={() => setActiveTab(item.id)}
                            className={`
                                relative cursor-pointer group rounded-3xl p-6 flex flex-col items-center justify-center gap-4
                                bg-gradient-to-br bg-white/5 border border-white/5 backdrop-blur-sm
                                hover:bg-white/10 hover:border-white/20 transition-all duration-300
                                ${activeTab === item.id ? 'ring-2 ring-teal-500/50 bg-white/10' : ''}
                            `}
                        >
                            {/* Floating 3D Icon */}
                            <motion.div
                                animate={{ y: [0, -8, 0] }}
                                transition={{ repeat: Infinity, duration: 3 + index, ease: "easeInOut" }}
                                className="relative w-28 h-28 md:w-32 md:h-32 filter drop-shadow-[0_10px_10px_rgba(0,0,0,0.5)]"
                            >
                                <img
                                    src={item.icon}
                                    alt={item.label}
                                    className="w-full h-full object-contain"
                                />
                            </motion.div>

                            {/* Label */}
                            <div className="text-center z-10 relative">
                                <h3 className="text-base font-bold text-gray-200 group-hover:text-white tracking-wide">{item.label}</h3>
                                <div className="h-0.5 w-0 group-hover:w-full bg-teal-400 transition-all duration-300 mt-1 mx-auto"></div>
                            </div>

                            {/* Glow Effect */}
                            <div className={`absolute inset-0 rounded-3xl bg-gradient-to-br ${item.color} opacity-0 group-hover:opacity-10 blur-2xl transition-opacity duration-500`}></div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Tab Content Display */}
            <div className="max-w-7xl mx-auto bg-slate-900/40 backdrop-blur-xl border border-white/10 rounded-3xl p-8 min-h-[500px]">
                <AnimatePresence mode="wait">
                    {/* PLACES TO VISIT TAB */}
                    {activeTab === 'places' && (
                        <motion.div
                            key="places"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-8"
                        >
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-2xl font-bold text-white">📍 Places to Visit</h2>
                                <div className="text-sm text-gray-400">Detailed daily itinerary</div>
                            </div>

                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                {(plan.itinerary || []).map((day) => (
                                    <div key={day.day_number} className="bg-white/5 border border-white/5 rounded-2xl p-6 hover:border-teal-500/30 transition-colors">
                                        <div className="flex justify-between items-center mb-4 pb-4 border-b border-white/5">
                                            <h3 className="text-xl font-bold text-teal-300">Day {day.day_number}</h3>
                                            <span className="text-sm bg-white/10 px-3 py-1 rounded-full text-gray-300">{day.date}</span>
                                        </div>

                                        {/* Weather Widget Mini */}
                                        {day.weather ? (
                                            <div className="flex items-center gap-3 mb-6 bg-blue-500/10 p-3 rounded-xl border border-blue-500/10">
                                                <span className="text-2xl">⛅</span>
                                                <div>
                                                    <div className="text-sm font-semibold text-blue-200">{day.weather.temperature_c}°C</div>
                                                    <div className="text-xs text-blue-300/70">{day.weather.condition}</div>
                                                </div>
                                            </div>
                                        ) : null}

                                        <div className="space-y-6">
                                            {[...(day.morning_activities || []), ...(day.afternoon_activities || []), ...(day.evening_activities || [])].map((activity, i) => (
                                                <div key={i} className="relative pl-6 border-l-2 border-white/10 hover:border-teal-500/50 transition-colors">
                                                    <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-slate-900 border-2 border-teal-500"></div>
                                                    <div className="mb-1 text-xs font-mono text-teal-400 uppercase tracking-widest">{activity.time_slot}</div>
                                                    <h4 className="font-semibold text-lg text-white">{activity.name}</h4>
                                                    <p className="text-sm text-gray-400 mb-2">{activity.description}</p>
                                                    <div className="flex items-center gap-4 text-xs text-gray-500">
                                                        <span>📍 {activity.location}</span>
                                                        <span>💰 ${activity.estimated_cost}</span>
                                                    </div>
                                                    {activity.booking_link && (
                                                        <a
                                                            href={activity.booking_link}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="mt-3 inline-block px-3 py-1 bg-teal-500/20 text-teal-300 text-xs rounded-lg hover:bg-teal-500/30 transition-colors"
                                                        >
                                                            Book Now ↗
                                                        </a>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Activity Booking Platforms */}
                            {plan.activity_platforms && Object.keys(plan.activity_platforms).length > 0 && (
                                <div className="mt-12 bg-white/5 border border-white/5 rounded-2xl p-6">
                                    <h3 className="text-xl font-bold text-white mb-4">🎫 Book Experiences & Tours</h3>
                                    <div className="flex flex-wrap gap-4">
                                        {Object.entries(plan.activity_platforms).map(([name, url]) => (
                                            <a
                                                key={name}
                                                href={url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="px-5 py-3 bg-teal-500/10 border border-teal-500/20 hover:bg-teal-500/20 text-teal-300 rounded-xl transition-all flex items-center gap-2 font-medium"
                                            >
                                                {name} ↗
                                            </a>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    )}

                    {/* FLIGHT TICKETS TAB */}
                    {activeTab === 'flights' && (
                        <motion.div
                            key="flights"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                        >
                            <h2 className="text-2xl font-bold text-white mb-6">✈️ Flight Tickets & Transportation</h2>

                            {/* Budget Summary for Flights */}
                            <div className="bg-gradient-to-br from-blue-900/50 to-blue-800/20 border border-blue-500/20 p-6 rounded-2xl mb-8">
                                <div className="text-blue-400 text-sm font-semibold uppercase tracking-wider mb-2">Estimated Flight Cost</div>
                                <div className="text-4xl font-bold text-white">${plan.budget?.flights || 0}</div>
                                <div className="text-blue-400/60 text-xs mt-1">Round trip for {plan.itinerary?.length || 1} days</div>
                            </div>

                            {/* Flight Options */}
                            {plan.intercity_travel && plan.intercity_travel.length > 0 ? (
                                <div className="space-y-6">
                                    <h3 className="text-xl font-bold text-white mb-4">🎫 Available Flights</h3>
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
                                                    <a
                                                        href={flight.booking_link}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="mt-4 w-full block text-center px-4 py-2 bg-blue-500/20 text-blue-300 rounded-lg hover:bg-blue-500/30 transition-colors"
                                                    >
                                                        Book Flight ↗
                                                    </a>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                <div className="bg-white/5 border border-white/10 rounded-2xl p-8 text-center">
                                    <div className="text-6xl mb-4">✈️</div>
                                    <h3 className="text-xl font-bold text-white mb-2">Search for Flights</h3>
                                    <p className="text-gray-400 mb-6">Use these platforms to find the best flight deals</p>
                                </div>
                            )}

                            {/* Flight Booking Platforms */}
                            <div className="mt-8 bg-white/5 border border-white/5 rounded-2xl p-6">
                                <h3 className="text-xl font-bold text-white mb-4">🔍 Find Best Flight Deals</h3>
                                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                    {[
                                        { name: 'Google Flights', url: `https://www.google.com/travel/flights?q=flights+from+${origin.replace(' ', '+')}+to+${destination.replace(' ', '+')}` },
                                        { name: 'Skyscanner', url: `https://www.skyscanner.com/transport/flights/${origin}/${destination}` },
                                        { name: 'Kayak', url: `https://www.kayak.com/flights/${origin}-${destination}` },
                                        { name: 'Expedia', url: `https://www.expedia.com/Flights-Search?trip=roundtrip&leg1=from:${origin},to:${destination}` },
                                        { name: 'Momondo', url: `https://www.momondo.com/flight-search/${origin}-${destination}` },
                                        { name: 'CheapOair', url: `https://www.cheapoair.com/` }
                                    ].map((platform) => (
                                        <a
                                            key={platform.name}
                                            href={platform.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="px-5 py-3 bg-blue-500/10 border border-blue-500/20 hover:bg-blue-500/20 text-blue-300 rounded-xl transition-all flex items-center justify-center gap-2 font-medium"
                                        >
                                            {platform.name} ↗
                                        </a>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* HOTELS TAB */}
                    {activeTab === 'hotels' && (
                        <motion.div
                            key="hotels"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                        >
                            <h2 className="text-2xl font-bold text-white mb-6">🏨 Accommodation Options</h2>

                            {/* Budget Summary for Hotels */}
                            <div className="bg-gradient-to-br from-orange-900/50 to-orange-800/20 border border-orange-500/20 p-6 rounded-2xl mb-8">
                                <div className="text-orange-400 text-sm font-semibold uppercase tracking-wider mb-2">Estimated Accommodation Cost</div>
                                <div className="text-4xl font-bold text-white">${plan.budget?.accommodation || 0}</div>
                                <div className="text-orange-400/60 text-xs mt-1">For {plan.itinerary?.length || 1} nights</div>
                            </div>

                            <h3 className="text-xl font-bold text-white mb-4">Recommended Hotels</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                                {(plan.hotels_shortlist || []).map((hotel, i) => (
                                    <div key={i} className="group bg-slate-800/50 p-4 rounded-xl border border-white/5 hover:border-orange-500/30 transition-all">
                                        <div className="h-32 bg-slate-700 rounded-lg mb-4 overflow-hidden relative">
                                            <div className="absolute inset-0 bg-gradient-to-t from-slate-900 to-transparent"></div>
                                            <div className="absolute bottom-2 left-2 text-white font-bold">{hotel.name}</div>
                                        </div>
                                        <div className="space-y-2">
                                            <div className="flex items-center justify-between">
                                                <span className="text-sm text-gray-400">📍 {hotel.area}</span>
                                                <span className="text-yellow-400 text-sm">⭐ {hotel.rating}/5</span>
                                            </div>
                                            <p className="text-xs text-gray-500 line-clamp-2">{hotel.description}</p>
                                            <div className="flex items-center justify-between pt-2 border-t border-white/5">
                                                <span className="text-lg font-bold text-teal-400">${hotel.price_per_night}/night</span>
                                                {hotel.booking_link && (
                                                    <a
                                                        href={hotel.booking_link}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="px-3 py-1 bg-orange-500/20 text-orange-300 text-xs rounded-lg hover:bg-orange-500/30 transition-colors"
                                                    >
                                                        View ↗
                                                    </a>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Hotel Booking Platforms */}
                            {plan.booking_platforms && Object.keys(plan.booking_platforms).length > 0 && (
                                <div className="bg-white/5 border border-white/5 rounded-2xl p-6">
                                    <h3 className="text-xl font-bold text-white mb-4">🔍 Compare Prices on Major Platforms</h3>
                                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                                        {Object.entries(plan.booking_platforms).map(([name, url]) => (
                                            <a
                                                key={name}
                                                href={url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="px-5 py-3 bg-orange-500/10 border border-orange-500/20 hover:bg-orange-500/20 text-orange-300 rounded-xl transition-all flex items-center justify-center gap-2 font-medium text-sm"
                                            >
                                                {name} ↗
                                            </a>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
