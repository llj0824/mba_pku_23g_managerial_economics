import pandas as pd
import numpy as np

# Define the minimal costs
FC_MIN_COST = 400
CB_MIN_COST = 300

# Function to calculate rewards
def calculate_rewards(FC_bid, CB_bid):
    if FC_bid < CB_bid:
        return FC_bid - FC_MIN_COST, 0
    elif CB_bid < FC_bid:
        return 0, CB_bid - CB_MIN_COST
    else:  # In case of a tie, FC wins because of higher quality
        return FC_bid - FC_MIN_COST, 0

# Run the simulation
def run_simulation(num_simulations=10000):
    results = []
    for _ in range(num_simulations):
        # Randomly picking in increments of 10M
        FC_bid = np.random.randint(41, 60) * 10
        CB_bid = np.random.randint(31, 60) * 10
        FC_reward, CB_reward = calculate_rewards(FC_bid, CB_bid)
        results.append([FC_bid, FC_reward, CB_bid, CB_reward])
    return results

# Convert the results to a DataFrame
def results_to_dataframe(results):
    return pd.DataFrame(results, columns=['FC\'s Bid', 'FC\'s Reward', 'CB\'s Bid', 'CB\'s Reward'])

# Main function
def main():
    results = run_simulation()
    df = results_to_dataframe(results)
    df.to_csv("10000runs_monteCarloSimulation.csv",index=True)
    print(df)

if __name__ == "__main__":
    main()