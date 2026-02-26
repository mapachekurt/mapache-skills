import React from 'react';
import { Asset } from '../mockData';

interface AssetListProps {
    assets: Asset[];
}

export const AssetList: React.FC<AssetListProps> = ({ assets }) => {
    return (
        <div className="bg-[#161A1E] border border-[#2B2F36] rounded-2zl overflow-hidden glass-effect">
            <div className="px-6 py-4 border-b border-[#2B2F36] flex justify-between items-center">
                <h3 className="text-lg font-bold text-[#EAECEF]">Your Assets</h3>
                <button className="text-[#00FFA3] text-sm font-medium hover:underline">View All</button>
            </div>

            <div className="divide-y divide-[#2B2F36]">
                {assets.map((asset) => (
                    <div key={asset.id} className="px-6 py-4 flex items-center hover:bg-[#2B2F36]/20 transition-colors cursor-pointer group">
                        <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center mr-4 group-hover:bg-[#00FFA3]/10 transition-colors">
                            <span className="text-[#EAECEF] font-bold text-xs">{asset.symbol}</span>
                        </div>

                        <div className="flex-1">
                            <p className="text-[#EAECEF] font-medium">{asset.name}</p>
                            <p className="text-slate-500 text-xs">{asset.holdings} {asset.symbol}</p>
                        </div>

                        <div className="hidden md:block w-32 px-4">
                            {/* Sparkline Placeholder */}
                            <div className="h-8 flex items-end space-x-1">
                                {asset.sparkline.map((val, i) => (
                                    <div
                                        key={i}
                                        className={`flex-1 rounded-t-sm ${asset.change24h > 0 ? 'bg-[#00FFA3]/30' : 'bg-[#FF4D4D]/30'}`}
                                        style={{ height: `${(val / Math.max(...asset.sparkline)) * 100}%` }}
                                    ></div>
                                ))}
                            </div>
                        </div>

                        <div className="text-right">
                            <p className="text-[#EAECEF] font-medium">${asset.value.toLocaleString()}</p>
                            <p className={`text-xs font-bold ${asset.change24h > 0 ? 'text-[#00FFA3]' : 'text-[#FF4D4D]'}`}>
                                {asset.change24h > 0 ? '+' : ''}{asset.change24h}%
                            </p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};
