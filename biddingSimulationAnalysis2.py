import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the CSV file
file_path = '10000runs_monteCarloSimulation.csv'
monte_carlo_data = pd.read_csv(file_path)
max_bid = 600
fc_color = "blue"
cb_color = "black"

# Define a function to calculate the specified percentiles for a series
def calculate_percentiles(series):
    return {
        '25% Percentile Reward': series.quantile(0.25),
        '50% Percentile Reward': series.quantile(0.50),  # median
        '75% Percentile Reward': series.quantile(0.75),
        '90% Percentile Reward': series.quantile(0.90),
    }

# Calculating the likelihood of winning the bid for each bid amount
fc_win_likelihood = monte_carlo_data[monte_carlo_data["FC's Reward"] > 0].groupby("FC's Bid").size() / monte_carlo_data.groupby("FC's Bid").size()
cb_win_likelihood = monte_carlo_data[monte_carlo_data["CB's Reward"] > 0].groupby("CB's Bid").size() / monte_carlo_data.groupby("CB's Bid").size()

# Calculating percentiles for FC
fc_percentiles = monte_carlo_data.groupby("FC's Bid")["FC's Reward"].apply(calculate_percentiles).unstack()
# Adding the likelihood of winning to the FC percentiles dataframe
fc_percentiles['Likelihood of Winning'] = fc_win_likelihood

# Calculating percentiles for CB
cb_percentiles = monte_carlo_data.groupby("CB's Bid")["CB's Reward"].apply(calculate_percentiles).unstack()
# Adding the likelihood of winning to the CB percentiles dataframe
cb_percentiles['Likelihood of Winning'] = cb_win_likelihood

# Handling NaN values by replacing them with zero
fc_percentiles['Likelihood of Winning'].fillna(0, inplace=True)
cb_percentiles['Likelihood of Winning'].fillna(0, inplace=True)

# Formatting 'Likelihood of Winning' as percentage with one decimal place
fc_percentiles['Likelihood of Winning'] = fc_percentiles['Likelihood of Winning'].apply(lambda x: '{:.1%}'.format(x))
cb_percentiles['Likelihood of Winning'] = cb_percentiles['Likelihood of Winning'].apply(lambda x: '{:.1%}'.format(x))

# Resetting index to make 'Bid' a column and not an index, for clarity in the final table display
fc_percentiles_reset = fc_percentiles.reset_index()
cb_percentiles_reset = cb_percentiles.reset_index()

fc_percentiles_reset.to_csv("fb_bid_reward_percentiles.csv",index=False)
cb_percentiles_reset.to_csv("cb_bid_reward_percentiles.csv",index=False)

####################################
######### Optimal Bid ###############
####################################
# Adding 'Profit' columns to the dataframe
monte_carlo_data["FC's Profit"] = monte_carlo_data["FC's Reward"]
monte_carlo_data["CB's Profit"] = monte_carlo_data["CB's Reward"]

# Group the data by bid amount for each company and calculate the median reward and profit
fc_stats_by_bid = monte_carlo_data.groupby("FC's Bid").agg({
    "FC's Reward": ['median', 'count'], 
    "FC's Profit": 'median'
}).reset_index()

cb_stats_by_bid = monte_carlo_data.groupby("CB's Bid").agg({
    "CB's Reward": ['median', 'count'], 
    "CB's Profit": 'median'
}).reset_index()

# Rename the multi-level columns for ease of access
fc_stats_by_bid.columns = ['_'.join(col) if col[1] else col[0] for col in fc_stats_by_bid.columns.values]
cb_stats_by_bid.columns = ['_'.join(col) if col[1] else col[0] for col in cb_stats_by_bid.columns.values]

# Find the bid amount for FC that maximizes the average reward
fc_max_avg_reward_bid = fc_stats_by_bid.loc[fc_stats_by_bid["FC's Reward_median"].idxmax(), "FC's Bid"]

# Find the bid amount for CB that maximizes the average reward
cb_max_avg_reward_bid = cb_stats_by_bid.loc[cb_stats_by_bid["CB's Reward_median"].idxmax(), "CB's Bid"]

# Find the bid amount for FC that maximizes the average profit
fc_max_avg_profit_bid = fc_stats_by_bid.loc[fc_stats_by_bid["FC's Profit_median"].idxmax(), "FC's Bid"]

# Find the bid amount for CB that maximizes the average profit
cb_max_avg_profit_bid = cb_stats_by_bid.loc[cb_stats_by_bid["CB's Profit_median"].idxmax(), "CB's Bid"]

# Set the index back to "FC's Bid"
fc_stats_by_bid.set_index("FC's Bid", inplace=True)
cb_stats_by_bid.set_index("CB's Bid", inplace=True)

# Determine the likelihood of winning at each bid level for both companies
# We consider a win to have occurred when the reward is greater than zero
fc_stats_by_bid['FC Likelihood of Winning'] = monte_carlo_data[monte_carlo_data["FC's Reward"] > 0].groupby("FC's Bid").size() / monte_carlo_data.groupby("FC's Bid").size()
cb_stats_by_bid['CB Likelihood of Winning'] = monte_carlo_data[monte_carlo_data["CB's Reward"] > 0].groupby("CB's Bid").size() / monte_carlo_data.groupby("CB's Bid").size()

# Replace NaN values with zero (where there were no wins)
fc_stats_by_bid['FC Likelihood of Winning'].fillna(0, inplace=True)
cb_stats_by_bid['CB Likelihood of Winning'].fillna(0, inplace=True)


# Calculate the expected profit for each bid level, which is the likelihood of winning multiplied by the average profit
fc_stats_by_bid['FC Expected Profit'] = fc_stats_by_bid['FC Likelihood of Winning'] * fc_stats_by_bid["FC's Profit_median"]
cb_stats_by_bid['CB Expected Profit'] = cb_stats_by_bid['CB Likelihood of Winning'] * cb_stats_by_bid["CB's Profit_median"]

# Find the bid amount that maximizes the expected profit for each company
fc_optimal_bid_ev = fc_stats_by_bid.loc[fc_stats_by_bid['FC Expected Profit'].idxmax()]
cb_optimal_bid_ev = cb_stats_by_bid.loc[cb_stats_by_bid['CB Expected Profit'].idxmax()]
print("Fair Construction's optimal bid is: " + str(fc_optimal_bid_ev))
print("Cutthroat Builder's optimal bid is: " + str(cb_optimal_bid_ev))

##### Plot the rewards curve

# Create a new figure
plt.figure(figsize=(10, 6))

# Plot FC's expected reward
sns.lineplot(x="FC's Bid", y='FC Expected Profit', data=fc_stats_by_bid, label="Fair Construction Inc.", color=fc_color)

# Label each data point for FC
for line in fc_stats_by_bid.itertuples():
    plt.text(line[0], line[-1], f'{round(line[-1])}')

# Plot CB's expected reward
sns.lineplot(x="CB's Bid", y='CB Expected Profit', data=cb_stats_by_bid, label="Cutthroat Builders Inc.", color=cb_color)

# Label each data point for CB
for line in cb_stats_by_bid.itertuples():
    plt.text(line[0], line[-1], f'{round(line[-1])}')

# Add title and labels
plt.title('Expected Reward for Each Bid per Company')
plt.xlabel('Bid Amount (Million Yuan)')
plt.ylabel('Expected Reward (Million Yuan)')

# Show the plot
plt.show()
breakpoint()


