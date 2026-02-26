import React from 'react';
import './dashboard.css';
import { Sidebar } from './components/Sidebar';
import { StatCard } from './components/StatCard';
import { AssetList } from './components/AssetList';
import { PORTFOLIO_DATA } from './mockData';

const CryptoDashboard: React.FC = () => {
    return (
        <div className="flex h-screen bg-[#0B0E11] text-[#EAECEF] overflow-hidden">
            {/* 1. Sidebar */}
            <Sidebar />

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col overflow-y-auto">
                {/* 2. Header */}
                <header className="px-8 py-6 border-b border-[#2B2F36] flex justify-between items-center bg-[#0B0E11]/50 backdrop-blur-md sticky top-0 z-10">
                    <div>
                        <h2 className="text-slate-500 text-sm font-medium uppercase tracking-widest">Total Balance</h2>
                        <h1 className="text-4xl font-bold text-[#EAECEF] mt-1">
                            ${PORTFOLIO_DATA.totalBalance.toLocaleString()}
                        </h1>
                    </div>

                    <div className="flex items-center space-x-4">
                        <div className="relative">
                            <input
                                type="text"
                                placeholder="Search assets..."
                                className="bg-[#161A1E] border border-[#2B2F36] rounded-full px-10 py-2 text-sm focus:outline-none focus:border-[#00FFA3] transition-all w-64"
                            />
                            <span className="absolute left-4 top-2.5 text-slate-500 text-xs">🔍</span>
                        </div>
                        <button className="p-2 bg-[#161A1E] border border-[#2B2F36] rounded-full hover:bg-[#2B2F36] transition-colors">
                            🔔
                        </button>
                        <div className="w-10 h-10 rounded-full bg-slate-800 border-2 border-[#00FFA3]"></div>
                    </div>
                </header>

                {/* 3. Dashboard Grid */}
                <section className="p-8 space-y-8">
                    {/* Stats Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <StatCard
                            label="24h Volume"
                            value={`$${PORTFOLIO_DATA.volume24h.toLocaleString()}`}
                            subtext="+2.4%"
                            trend="up"
                        />
                        <StatCard
                            label="Diversity"
                            value={`${PORTFOLIO_DATA.diversity}%`}
                            subtext="Healthy"
                        />
                        <StatCard
                            label="Next Milestone"
                            value={`$${PORTFOLIO_DATA.nextMilestone.toLocaleString()}`}
                            subtext="85.6% achieved"
                        />
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* 4. Chart Area */}
                        <div className="lg:col-span-2 bg-[#161A1E] border border-[#2B2F36] rounded-2xl p-6 glass-effect min-h-[400px] flex flex-col">
                            <div className="flex justify-between items-center mb-6">
                                <h3 className="text-lg font-bold text-[#EAECEF]">Performance Over Time</h3>
                                <div className="flex space-x-2">
                                    {['1H', '24H', '1W', '1M', 'ALL'].map(t => (
                                        <button key={t} className={`px-3 py-1 rounded-md text-xs font-bold ${t === '24H' ? 'bg-[#00FFA3] text-[#0B0E11]' : 'text-slate-500 hover:text-white'}`}>
                                            {t}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="flex-1 flex items-center justify-center border-t border-[#2B2F36]/30">
                                <p className="text-slate-600 italic">Advanced Candlestick Chart (Cyber Blue) Rendering...</p>
                            </div>
                        </div>

                        {/* 5. Quick Actions */}
                        <div className="space-y-6">
                            <div className="bg-[#161A1E] border border-[#2B2F36] rounded-2xl p-6 glass-effect">
                                <h3 className="text-lg font-bold text-[#EAECEF] mb-4">Quick Trade</h3>
                                <div className="space-y-4">
                                    <div className="bg-[#0B0E11] p-4 rounded-xl border border-[#2B2F36]">
                                        <label className="text-xs text-slate-500 uppercase">You Pay</label>
                                        <div className="flex justify-between mt-1">
                                            <input type="number" defaultValue="250.00" className="bg-transparent text-xl font-bold focus:outline-none w-1/2" />
                                            <span className="font-bold">USD</span>
                                        </div>
                                    </div>
                                    <div className="bg-[#0B0E11] p-4 rounded-xl border border-[#2B2F36]">
                                        <label className="text-xs text-slate-500 uppercase">You Get</label>
                                        <div className="flex justify-between mt-1">
                                            <input type="number" defaultValue="0.0038" className="bg-transparent text-xl font-bold focus:outline-none w-1/2" />
                                            <span className="font-bold">BTC</span>
                                        </div>
                                    </div>
                                    <button className="w-full py-4 bg-[#00FFA3] text-[#0B0E11] font-black rounded-xl hover:shadow-[0_0_20px_rgba(0,255,163,0.4)] transition-all uppercase tracking-widest">
                                        Buy BTC
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* 6. Asset List */}
                    <AssetList assets={PORTFOLIO_DATA.assets} />
                </section>
            </main>
        </div>
    );
};

export default CryptoDashboard;
