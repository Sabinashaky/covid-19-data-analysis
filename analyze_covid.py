"""Starter script for COVID-19 data analysis.

Place the dataset at data/covid_data.csv, then run:
    python analyze_covid.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "covid_data.csv"
GRAPHS = ROOT / "graphs"
GRAPHS.mkdir(exist_ok=True)

if not DATA.exists():
    raise FileNotFoundError(
        f"Missing {DATA}. Download the dataset; see data/README.md."
    )

df = pd.read_csv(DATA, low_memory=False)
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

if "location" not in df.columns or "date" not in df.columns:
    raise KeyError("Expected 'location' and 'date' columns. Check the dataset schema.")

nepal = df[df["location"].astype(str).str.strip().str.casefold() == "nepal"].copy()
if nepal.empty:
    print("Nepal was not found in the dataset.")
elif "total_cases" in nepal.columns:
    nepal["date"] = pd.to_datetime(nepal["date"], errors="coerce")
    nepal["total_cases"] = pd.to_numeric(nepal["total_cases"], errors="coerce")
    nepal = nepal.dropna(subset=["date", "total_cases"]).sort_values("date")
    if not nepal.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(nepal["date"], nepal["total_cases"])
        plt.title("COVID-19: Cumulative Reported Cases in Nepal")
        plt.xlabel("Date")
        plt.ylabel("Reported cases")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        output = GRAPHS / "nepal_covid_cases.png"
        plt.savefig(output, dpi=200, bbox_inches="tight")
        plt.show()
        print("Saved:", output)
