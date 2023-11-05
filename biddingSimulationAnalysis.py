import pandas as pd

# Load the data from the CSV file
file_path = '10000runs_monteCarloSimulation.csv'
data = pd.read_csv(file_path)

# Grouping data by 'FC's Bid' and 'CB's Bid' and calculating the percentiles for rewards
# Define a function to calculate the specified percentiles for a series
def calculate_percentiles(series):
    return {
        '25% Percentile Reward': series.quantile(0.25),
        '50% Percentile Reward': series.quantile(0.50),  # median
        '75% Percentile Reward': series.quantile(0.75),
        '90% Percentile Reward': series.quantile(0.90),
    }

# Calculating percentiles for FC
fc_percentiles = data.groupby("FC's Bid")["FC's Reward"].apply(calculate_percentiles).unstack()

# Calculating percentiles for CB
cb_percentiles = data.groupby("CB's Bid")["CB's Reward"].apply(calculate_percentiles).unstack()

# Resetting index to make 'Bid' a column and not an index, for clarity in the final table display
fc_percentiles_reset = fc_percentiles.reset_index()
cb_percentiles_reset = cb_percentiles.reset_index()

breakpoint()
fc_percentiles_reset, cb_percentiles_reset