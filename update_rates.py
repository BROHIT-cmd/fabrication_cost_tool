import pandas as pd
from datetime import datetime

# Load existing
df = pd.read_csv("material_rates.csv")

# Add last updated column
df["LastUpdated"] = datetime.now().strftime("%Y-%m-%d")

# Save
df.to_csv("material_rates.csv", index=False)

print("✅ Rates updated")
