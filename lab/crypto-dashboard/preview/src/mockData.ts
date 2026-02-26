/**
 * Mock data for the Crypto Dashboard.
 * Decouples the UI from the data layer for cleaner components.
 */

export interface Asset {
    id: string;
    name: string;
    symbol: string;
    price: number;
    change24h: number;
    holdings: number;
    value: number;
    sparkline: number[];
}

export const PORTFOLIO_DATA = {
    totalBalance: 128450.62,
    volume24h: 12450.00,
    diversity: 42,
    nextMilestone: 150000,
    assets: [
        {
            id: "1",
            name: "Bitcoin",
            symbol: "BTC",
            price: 64230.15,
            change24h: 2.45,
            holdings: 1.25,
            value: 80287.69,
            sparkline: [62000, 63000, 62500, 64000, 64500, 64230],
        },
        {
            id: "2",
            name: "Ethereum",
            symbol: "ETH",
            price: 3450.22,
            change24h: -1.2,
            holdings: 10.5,
            value: 36227.31,
            sparkline: [3550, 3500, 3400, 3420, 3480, 3450],
        },
        {
            id: "3",
            name: "Solana",
            symbol: "SOL",
            price: 145.67,
            change24h: 5.67,
            holdings: 85.0,
            value: 12381.95,
            sparkline: [130, 135, 138, 142, 148, 145],
        },
    ] as Asset[],
};

export const MENU_ITEMS = [
    { label: "Dashboard", icon: "LayoutDashboard" },
    { label: "Wallet", icon: "Wallet" },
    { label: "Market", icon: "TrendingUp" },
    { label: "Settings", icon: "Settings" },
];
