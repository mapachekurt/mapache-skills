import React from 'react';

interface StatCardProps {
    label: string;
    value: string | number;
    subtext?: string;
    trend?: 'up' | 'down' | 'neutral';
}

export const StatCard: React.FC<StatCardProps> = ({ label, value, subtext, trend }) => {
    return (
        <div className="bg-[#161A1E] border border-[#2B2F36] rounded-2xl p-6 glass-effect">
            <p className="text-slate-500 text-sm font-medium mb-2 uppercase tracking-wider">{label}</p>
            <div className="flex items-baseline space-x-2">
                <h3 className="text-2xl font-bold text-[#EAECEF]">{value}</h3>
                {trend && (
                    <span className={`text-xs font-bold ${trend === 'up' ? 'text-[#00FFA3]' : trend === 'down' ? 'text-[#FF4D4D]' : 'text-slate-400'}`}>
                        {trend === 'up' ? '↑' : trend === 'down' ? '↓' : ''} {subtext}
                    </span>
                )}
            </div>
            {!trend && subtext && <p className="text-xs text-slate-400 mt-1">{subtext}</p>}
        </div>
    );
};
