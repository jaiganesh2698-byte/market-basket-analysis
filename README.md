# Market basket analysis

Small Python project for **frequent itemsets** (Apriori) and **association rules** on retail-style transaction data, using [pandas](https://pandas.pydata.org/) and [mlxtend](https://rasbt.github.io/mlxtend/).

## Setup

```bash
cd market-basket-analysis
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python analyze.py
```

With your own CSV and thresholds:

```bash
python analyze.py --csv path/to/transactions.csv --min-support 0.15 --min-confidence 0.5 --min-lift 1.0
```

## Data format

CSV with two columns:

| Column           | Description                          |
|------------------|--------------------------------------|
| `transaction_id` | Basket / order identifier            |
| `item`           | One product per row (repeat id for multiple lines in the same basket) |

Example: `data/sample_transactions.csv`.

## Git

Initialize a repository in this folder when you are ready:

```bash
git init
git add .
git commit -m "Initial commit: market basket analysis"
```

`.gitignore` already excludes `.venv/` and common Python artifacts.
