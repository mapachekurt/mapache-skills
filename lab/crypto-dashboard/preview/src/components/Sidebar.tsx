import React from 'react';
import { MENU_ITEMS } from '../mockData';

export const Sidebar: React.FC = () => {
    return (
        <aside className="w-20 lg:w-64 bg-[#161A1E] border-r border-[#2B2F36] flex flex-col items-center lg:items-start py-8 transition-all">
            <div className="px-6 mb-12">
                <div className="w-10 h-10 bg-[#00FFA3] rounded-xl flex items-center justify-center">
                    <span className="text-[#0B0E11] font-bold text-xl">S</span>
                </div>
            </div>

            <nav className="flex-1 w-full space-y-2">
                {MENU_ITEMS.map((item) => (
                    <button
                        key={item.label}
                        className="w-full flex items-center px-6 py-4 text-slate-400 hover:text-[#00FFA3] hover:bg-[#2B2F36]/50 transition-colors group"
                    >
                        <div className="w-6 h-6 rounded bg-slate-800 group-hover:bg-[#00FFA3]/20 flex items-center justify-center mr-4">
                            {/* Icon Placeholder */}
                        </div>
                        <span className="hidden lg:block font-medium">{item.label}</span>
                    </button>
                ))}
            </nav>

            <div className="mt-auto px-6 w-full">
                <div className="p-4 bg-[#2B2F36]/30 rounded-2xl hidden lg:block">
                    <p className="text-xs text-slate-500 mb-1">Pro Status</p>
                    <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full bg-[#00FFA3] w-3/4"></div>
                    </div>
                </div>
            </div>
        </aside>
    );
};
