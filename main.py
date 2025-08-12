import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# --- 1. Synthetic Data Generation ---
np.random.seed(42)  # for reproducibility
num_customers = 500
data = {
    'Recency': np.random.randint(1, 365, num_customers),  # Days since last purchase
    'Frequency': np.random.poisson(lam=5, size=num_customers),  # Number of purchases
    'MonetaryValue': np.random.exponential(scale=100, size=num_customers)  # Average purchase value
}
df = pd.DataFrame(data)
# --- 2. Data Preparation ---
# Calculate RFM scores (Recency, Frequency, MonetaryValue)
df['R'] = df['Recency'].apply(lambda x: 5 - pd.qcut(df['Recency'], 5, labels=False, duplicates='drop'))
df['F'] = pd.qcut(df['Frequency'], 5, labels=False, duplicates='drop') + 1
df['M'] = pd.qcut(df['MonetaryValue'], 5, labels=False, duplicates='drop') + 1
df['RFM_Score'] = df['R'] * 100 + df['F'] * 10 + df['M']
# --- 3. Customer Segmentation using K-Means ---
# Scale the RFM data for KMeans
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(df[['R', 'F', 'M']])
# Determine optimal number of clusters (elbow method - simplified for brevity)
kmeans = KMeans(n_clusters=3, random_state=42) # Choosing 3 clusters as an example.  More sophisticated methods could be used.
kmeans.fit(rfm_scaled)
df['Cluster'] = kmeans.labels_
# --- 4. Visualization ---
# Visualize clusters (example using first two RFM components)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='R', y='F', hue='Cluster', data=df, palette='viridis')
plt.title('Customer Segmentation based on Recency and Frequency')
plt.xlabel('Recency Score')
plt.ylabel('Frequency Score')
plt.savefig('customer_segments.png')
print("Plot saved to customer_segments.png")
# --- 5. Analysis and Interpretation (example) ---
# Analyze average RFM scores per cluster
print("\nAverage RFM scores per cluster:")
print(df.groupby('Cluster')[['R', 'F', 'M']].mean())
#Further analysis could involve predicting CLTV using regression models and assigning marketing strategies to each segment.  This is omitted for brevity.