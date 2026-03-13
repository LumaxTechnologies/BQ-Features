"""Bundled finance demo data generation and discovery."""

from __future__ import annotations

import csv
from pathlib import Path


def get_bundled_demo_data_dir() -> Path | None:
    """Return path to bundled demo_data directory (package or repo)."""
    # .../src/bq_features/deploy/demo_data.py -> bq_features = parent.parent
    bq_features = Path(__file__).resolve().parent.parent
    for candidate in [
        bq_features.parent.parent / "demo_data",  # repo root demo_data
        bq_features.parent / "demo_data",         # src/demo_data
        bq_features / "demo_data",                # src/bq_features/demo_data
    ]:
        if candidate.is_dir():
            return candidate
    return None


def write_bundled_demo_data(out_dir: Path) -> None:
    """Write sample finance CSV files into out_dir for demo loading."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # Portfolio holdings: id, symbol, quantity, as_of_date
    with open(out_dir / "portfolio_holdings.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["holding_id", "symbol", "quantity", "as_of_date"])
        w.writerows([
            ["1", "AAPL", "100", "2024-01-15"],
            ["2", "GOOGL", "50", "2024-01-15"],
            ["3", "MSFT", "75", "2024-01-15"],
            ["4", "AMZN", "40", "2024-01-15"],
            ["5", "NVDA", "30", "2024-01-15"],
            ["6", "AAPL", "100", "2024-02-15"],
            ["7", "GOOGL", "55", "2024-02-15"],
            ["8", "MSFT", "80", "2024-02-15"],
        ])

    # Daily prices: symbol, date, open, high, low, close, volume
    with open(out_dir / "daily_prices.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["symbol", "date", "open", "high", "low", "close", "volume"])
        rows = []
        for sym, mult in [("AAPL", 1.0), ("GOOGL", 1.2), ("MSFT", 1.1), ("AMZN", 0.9), ("NVDA", 2.0)]:
            for i in range(30):
                d = f"2024-01-{i+1:02d}" if i < 31 else f"2024-02-{i-30:02d}"
                base = 100 * mult + i * 0.5
                rows.append([sym, d, base, base + 2, base - 1, base + 1, 1_000_000 + i * 10000])
        w.writerows(rows[:80])  # keep a small set

    # Transactions: id, symbol, side, quantity, price, tx_date
    with open(out_dir / "transactions.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tx_id", "symbol", "side", "quantity", "price", "tx_date"])
        w.writerows([
            ["T1", "AAPL", "BUY", "100", "185.50", "2024-01-10"],
            ["T2", "GOOGL", "BUY", "50", "142.30", "2024-01-12"],
            ["T3", "MSFT", "BUY", "75", "398.20", "2024-01-14"],
            ["T4", "AMZN", "BUY", "40", "155.00", "2024-01-16"],
            ["T5", "NVDA", "BUY", "30", "520.00", "2024-01-18"],
            ["T6", "GOOGL", "BUY", "5", "145.00", "2024-02-01"],
            ["T7", "MSFT", "BUY", "5", "405.00", "2024-02-05"],
        ])

    # PnL summary placeholder: date, strategy, pnl
    with open(out_dir / "pnl_daily.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "strategy", "pnl"])
        w.writerows([
            ["2024-01-15", "equity", "1250.50"],
            ["2024-01-16", "equity", "-320.25"],
            ["2024-01-17", "equity", "890.00"],
            ["2024-02-01", "equity", "2100.75"],
            ["2024-02-15", "equity", "450.00"],
        ])
