"""
Market basket analysis: frequent itemsets (Apriori) and association rules.

Usage:
  python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
  pip install -r requirements.txt
  python analyze.py
  python analyze.py --csv data/sample_transactions.csv --min-support 0.15 --min-confidence 0.5
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


def load_transactions_long(csv_path: Path) -> list[list[str]]:
    df = pd.read_csv(csv_path)
    if "transaction_id" not in df.columns or "item" not in df.columns:
        raise ValueError("CSV must have columns: transaction_id, item")
    grouped = df.groupby("transaction_id", sort=True)["item"].apply(
        lambda s: sorted(s.astype(str).unique().tolist())
    )
    return grouped.tolist()


def main() -> None:
    parser = argparse.ArgumentParser(description="Market basket analysis (Apriori + association rules)")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().parent / "data" / "sample_transactions.csv",
        help="Path to CSV with transaction_id, item columns",
    )
    parser.add_argument("--min-support", type=float, default=0.2, help="Minimum support for itemsets")
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.5,
        help="Minimum confidence for association rules",
    )
    parser.add_argument("--min-lift", type=float, default=1.0, help="Minimum lift for association rules")
    args = parser.parse_args()

    transactions = load_transactions_long(args.csv)
    te = TransactionEncoder()
    ohe = te.fit(transactions).transform(transactions)
    basket_df = pd.DataFrame(ohe, columns=te.columns_)

    frequent = apriori(basket_df, min_support=args.min_support, use_colnames=True)
    if frequent.empty:
        print("No frequent itemsets at this support threshold. Try lowering --min-support.")
        return

    rules = association_rules(
        frequent,
        metric="confidence",
        min_threshold=args.min_confidence,
    )
    rules = rules[rules["lift"] >= args.min_lift].sort_values("lift", ascending=False)

    print(f"Transactions: {len(transactions)} | Items: {basket_df.shape[1]}")
    print("\n--- Frequent itemsets ---")
    print(frequent.sort_values("support", ascending=False).to_string(index=False))

    if rules.empty:
        print("\nNo rules at confidence/lift thresholds. Try lowering --min-confidence or --min-lift.")
        return

    print("\n--- Association rules (sorted by lift) ---")
    display_cols = [
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "lift",
        "leverage",
        "conviction",
    ]
    out = rules[display_cols].copy()
    out["antecedents"] = out["antecedents"].apply(lambda x: ", ".join(sorted(x)))
    out["consequents"] = out["consequents"].apply(lambda x: ", ".join(sorted(x)))
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
