"""Generate a 1M-row CSV and a 50k-row xlsx for sandbox testing."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)
n = 1_000_000
df = pd.DataFrame({
    "order_id": np.arange(n),
    "region": rng.choice(["EMEA", "APAC", "AMER"], n),
    "amount": rng.normal(100, 25, n).round(2),
    "qty": rng.integers(1, 20, n),
    "note": np.where(rng.random(n) < 0.1, None, "ok"),
})
df.to_csv(out / "sales_1m.csv", index=False)
df.head(50_000).to_excel(out / "sales_50k.xlsx", index=False)
