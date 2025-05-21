import pandas as pd

# Load your CSV
df = pd.read_csv('Year-Make-Model-Trim-Full-Specs-by-Teoalida-SAMPLE.csv')

# Filter for BMW, Ford, Toyota
filtered = df[df['Make'].isin(['BMW', 'Ford', 'Toyota'])]

# Take first 15 of each
result = (
    filtered.groupby('Make', group_keys=False)
    .apply(lambda x: x.head(15))
)

# Save to new CSV
result.to_csv('filtered_15_each.csv', index=False)