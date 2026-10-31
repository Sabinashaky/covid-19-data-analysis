from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT = Path("COVID-19-Data-Analysis.csv").resolve().parent
DATA = ROOT / "COVID-19-Data-Analysis.csv"
GRAPHS = ROOT / "graphs"
GRAPHS.mkdir(exist_ok=True)
if not DATA.exists():
    raise FileNotFoundError(
        f"Missing {DATA}. Download the dataset; see data/README.md."
    )
df = pd.read_csv(DATA, low_memory=False, on_bad_lines='skip')
print("Shape:", df.shape)
unique_countries = df["country"].dropna().unique()
matches = [c for c in unique_countries if "nep" in c.lower()]
print("Found matching countries:", matches)
n_countries = sorted([c for c in unique_countries if c.strip().lower().startswith('n')])
print("Unique countries starting with 'N':", n_countries[:15])