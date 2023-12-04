import pandas as pd
import numpy as np
from scipy.stats import truncnorm
from random import uniform

# Define the minimal costs and maximum bid
FC_MIN_COST = 400
CB_MIN_COST = 300
MAX_BID = 600
STD_DEV = 50  # Standard deviation of $50 million

# Function to calculate rewards
def calculate_rewards(FC_bid, CB_bid):
    if FC_bid < CB_bid:
        return FC_bid - FC_MIN_COST, 0
    elif CB_bid < FC_bid:
        return 0, CB_bid - CB_MIN_COST
    else:  # In case of a tie, FC wins because of higher quality
        return FC_bid - FC_MIN_COST, 0

# Function to generate bids using a truncated normal distribution
def generate_bid_normal(breakeven_cost):
    midpoint = (breakeven_cost + MAX_BID) / 2
    # Calculate the lower and upper bounds in standard deviation units
    lower_bound = (breakeven_cost - midpoint) / STD_DEV
    upper_bound = (MAX_BID - midpoint) / STD_DEV
    # Generate a bid from the truncated normal distribution
    bid = truncnorm.rvs(lower_bound, upper_bound, loc=midpoint, scale=STD_DEV)
    return int(round(bid))  # Convert the bid to an integer and round it

# Function to generate bids using a truncated normal distribution
def generate_bid_uniform(breakeven_cost):
    midpoint = (breakeven_cost + MAX_BID) / 2
    # Calculate the lower and upper bounds in standard deviation units
    lower_bound = (midpoint - STD_DEV *2)
    upper_bound = (midpoint + STD_DEV *2)
    # Generate a bid from uniform distribution
    bid = uniform(breakeven_cost, MAX_BID)
    return int(round(bid))  # Convert the bid to an integer and round it


# Run the simulation
def run_simulation(num_simulations=10000):
    results = []
    for _ in range(num_simulations):
        FC_bid = generate_bid_uniform(FC_MIN_COST)
        CB_bid = generate_bid_uniform(CB_MIN_COST)
        FC_reward, CB_reward = calculate_rewards(FC_bid, CB_bid)
        results.append([FC_bid, FC_reward, CB_bid, CB_reward])
    return results

# Convert the results to a DataFrame
def results_to_dataframe(results):
    df = pd.DataFrame(results, columns=['FC\'s Bid', 'FC\'s Reward', 'CB\'s Bid', 'CB\'s Reward'])
    return df

# Main function
def main():
    results = run_simulation()
    df = results_to_dataframe(results)
    df.to_csv("10000runs_monteCarloSimulation.csv", index=False)
    print(df)

if __name__ == "__main__":
    main()