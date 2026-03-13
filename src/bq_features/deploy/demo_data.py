"""Bundled finance demo data generation and discovery."""

from __future__ import annotations

import csv
from pathlib import Path

# Trading days (weekdays) 2024-01-02 through 2024-02-29 so joins on date are filled
TRADING_DAYS_JAN_FEB_2024 = [
    "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08", "2024-01-09",
    "2024-01-10", "2024-01-11", "2024-01-12", "2024-01-15", "2024-01-16", "2024-01-17",
    "2024-01-18", "2024-01-19", "2024-01-22", "2024-01-23", "2024-01-24", "2024-01-25",
    "2024-01-26", "2024-01-29", "2024-01-30", "2024-01-31",
    "2024-02-01", "2024-02-02", "2024-02-05", "2024-02-06", "2024-02-07", "2024-02-08",
    "2024-02-09", "2024-02-12", "2024-02-13", "2024-02-14", "2024-02-15", "2024-02-16",
    "2024-02-19", "2024-02-20", "2024-02-21", "2024-02-22", "2024-02-23",
    "2024-02-26", "2024-02-27", "2024-02-28", "2024-02-29",
]

SYMBOLS = ["AAPL", "GOOGL", "MSFT", "AMZN", "NVDA"]
# Base close price per symbol (approx) for first day; we drift by day index
BASE_CLOSE = {"AAPL": 185.0, "GOOGL": 142.0, "MSFT": 398.0, "AMZN": 155.0, "NVDA": 520.0}


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


def _daily_prices_rows() -> list[list[str]]:
    """Generate daily_prices rows: every (symbol, date) so joins on date are filled."""
    sym_idx = {s: i for i, s in enumerate(SYMBOLS)}
    rows = []
    for sym in SYMBOLS:
        base = BASE_CLOSE[sym]
        prev_close = base
        idx = sym_idx[sym]
        for i, dt in enumerate(TRADING_DAYS_JAN_FEB_2024):
            step = 0.3 * (1 + (i % 5) - 2) + (idx % 10) / 100.0
            close = round(prev_close + step, 2)
            open_ = prev_close
            high = round(max(open_, close) + 0.5, 2)
            low = round(min(open_, close) - 0.3, 2)
            volume = 20_000_000 + (i * 500_000) + (idx % 5) * 1_000_000
            rows.append([sym, dt, open_, high, low, close, volume])
            prev_close = close
    return rows


def _portfolio_holdings_rows() -> list[list[str]]:
    """Generate portfolio_holdings: as_of_date only from TRADING_DAYS so join to daily_prices works."""
    snapshot_dates = ["2024-01-15", "2024-01-31", "2024-02-15", "2024-02-29"]
    rows = []
    hid = 1
    for as_of in snapshot_dates:
        for qty, sym in [(100, "AAPL"), (50, "GOOGL"), (75, "MSFT"), (40, "AMZN"), (30, "NVDA")]:
            # Slight quantity changes over time (add 0–5 per period)
            extra = (hid % 3) * 2
            rows.append([str(hid), sym, str(qty + extra), as_of])
            hid += 1
    return rows


def _transactions_rows() -> list[list[str]]:
    """Generate transactions: tx_date only from TRADING_DAYS so joins to daily_prices work."""
    # More transactions spread across the date range
    txs = [
        ("T1", "AAPL", "BUY", 100, 185.50, "2024-01-10"),
        ("T2", "GOOGL", "BUY", 50, 142.30, "2024-01-12"),
        ("T3", "MSFT", "BUY", 75, 398.20, "2024-01-14"),
        ("T4", "AMZN", "BUY", 40, 155.00, "2024-01-16"),
        ("T5", "NVDA", "BUY", 30, 520.00, "2024-01-18"),
        ("T6", "GOOGL", "BUY", 5, 145.00, "2024-02-01"),
        ("T7", "MSFT", "BUY", 5, 405.00, "2024-02-05"),
        ("T8", "AAPL", "BUY", 10, 192.00, "2024-01-22"),
        ("T9", "AMZN", "SELL", 5, 158.00, "2024-01-24"),
        ("T10", "NVDA", "BUY", 15, 535.00, "2024-01-26"),
        ("T11", "GOOGL", "BUY", 10, 148.00, "2024-01-29"),
        ("T12", "MSFT", "BUY", 10, 408.00, "2024-01-30"),
        ("T13", "AAPL", "SELL", 20, 195.00, "2024-02-06"),
        ("T14", "AMZN", "BUY", 25, 162.00, "2024-02-08"),
        ("T15", "NVDA", "BUY", 10, 545.00, "2024-02-12"),
        ("T16", "GOOGL", "SELL", 5, 152.00, "2024-02-14"),
        ("T17", "MSFT", "BUY", 15, 415.00, "2024-02-16"),
        ("T18", "AAPL", "BUY", 25, 188.00, "2024-02-19"),
        ("T19", "AMZN", "BUY", 10, 168.00, "2024-02-21"),
        ("T20", "NVDA", "SELL", 5, 560.00, "2024-02-23"),
        ("T21", "GOOGL", "BUY", 8, 150.00, "2024-02-26"),
        ("T22", "MSFT", "SELL", 10, 420.00, "2024-02-27"),
        ("T23", "AAPL", "BUY", 15, 182.00, "2024-02-28"),
        ("T24", "AMZN", "BUY", 20, 170.00, "2024-02-29"),
        ("T25", "NVDA", "BUY", 12, 550.00, "2024-02-29"),
    ]
    return [[t[0], t[1], t[2], str(t[3]), str(t[4]), t[5]] for t in txs]


def _pnl_daily_rows() -> list[list[str]]:
    """Generate pnl_daily: one row per trading day (and optional second strategy) so date joins are filled."""
    rows = []
    for i, dt in enumerate(TRADING_DAYS_JAN_FEB_2024):
        pnl_eq = round(500.0 + (i * 12.5) - ((i % 7) * 80), 2)
        rows.append([dt, "equity", str(pnl_eq)])
    for i, dt in enumerate(TRADING_DAYS_JAN_FEB_2024):
        pnl_fi = round(200.0 + (i * 3.0) + ((i % 5) * 15), 2)
        rows.append([dt, "fixed_income", str(pnl_fi)])
    return rows


def write_bundled_demo_data(out_dir: Path) -> None:
    """Write sample finance CSV files into out_dir. Dates align across tables so joins on date are filled."""
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "daily_prices.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["symbol", "date", "open", "high", "low", "close", "volume"])
        w.writerows(_daily_prices_rows())

    with open(out_dir / "portfolio_holdings.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["holding_id", "symbol", "quantity", "as_of_date"])
        w.writerows(_portfolio_holdings_rows())

    with open(out_dir / "transactions.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tx_id", "symbol", "side", "quantity", "price", "tx_date"])
        w.writerows(_transactions_rows())

    with open(out_dir / "pnl_daily.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "strategy", "pnl"])
        w.writerows(_pnl_daily_rows())
