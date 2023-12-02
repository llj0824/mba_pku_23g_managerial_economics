import matplotlib.pyplot as plt
import pandas as pd

# Load the data from the CSV file
file_path = '10000runs_monteCarloSimulation.csv'
data = pd.read_csv(file_path)

# Set up the figure size and subplots
plt.figure(figsize=(14, 6))

# Histogram for FC's Bid
plt.subplot(1, 2, 1)  # 1 row, 2 columns, first plot
plt.hist(data["FC's Bid"], bins=100, color='blue', alpha=0.7)
plt.title("Frequency of FC's Bid Amounts")
plt.xlabel("Bid Amount")
plt.ylabel("Frequency")

# Histogram for CB's Bid
plt.subplot(1, 2, 2)  # 1 row, 2 columns, second plot
plt.hist(data["CB's Bid"], bins=100, color='green', alpha=0.7)
plt.title("Frequency of CB's Bid Amounts")
plt.xlabel("Bid Amount")
plt.ylabel("Frequency")

# Display the plots
plt.tight_layout()
plt.show()

