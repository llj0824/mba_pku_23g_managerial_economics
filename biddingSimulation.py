import pandas as pd
import numpy as np

# Initialize an empty DataFrame
df = pd.DataFrame(columns=['FC\'s Bid', 'FC\'s Reward', 'CB\'s Bid', 'CB\'s Reward'])

# Define the minimal costs
FC_min_cost = 400
CB_min_cost = 300

# Run the simulation
for i in range(1000):  # Run 1000 simulations
    # Generate random bids
    FC_bid = np.random.randint(400, 600)
    CB_bid = np.random.randint(300, 600)

    # Calculate rewards
    if FC_bid > CB_bid:
        FC_reward = FC_bid - FC_min_cost
        CB_reward = 0
    elif CB_bid > FC_bid:
        CB_reward = CB_bid - CB_min_cost
        FC_reward = 0
    else:  # In case of a tie, both get 0 reward
        FC_reward = 0
        CB_reward = 0

    # Append the results to the DataFrame
    df = df.append({'FC\'s Bid': FC_bid, 'FC\'s Reward': FC_reward, 'CB\'s Bid': CB_bid, 'CB\'s Reward': CB_reward}, ignore_index=True)

# Print the DataFrame
print(df)