# Poker script generator for Pokernow ledger format

import pandas as pd

# Upload ledger as ledger.csv
df = pd.read_csv("ledger.csv")

id_to_player = {}
id_to_money = {}
winners = []
losers = []

for index, row in df.iterrows():
    id = row["player_id"]
    # Construct id_to_player
    if id not in id_to_player:
        id_to_player[id] = row["player_nickname"]

    # Correspond player id's to money
    if id not in id_to_money:
        id_to_money[id] = row["net"]
    else:
        id_to_money[id] += row["net"]
    
# Construct winners and losers
for i in id_to_money:
    if id_to_money[i] > 0:
        winners.append([i, id_to_money[i]])
    elif id_to_money[i] < 0:
        losers.append([i, id_to_money[i]])

winners = sorted(winners, key=lambda x: x[1], reverse=True)
losers = sorted(losers, key=lambda x: x[1])

# Function to make Pokernow numbers look pretty
def decimalfy(n):
    str_n = str(n)
    if len(str_n) < 3:
        return str_n
    else:
        return (str_n[:-2] + "." + str_n[-2:])

# Recursive function to print out the script
def print_script(winners, losers):
    if len(winners) == 0:
        return
    else:
        current_winner = winners[0]
        current_loser = losers[0]
        current_net = current_winner[1] + current_loser[1]

        if current_net > 0:
            print(f"{id_to_player[current_loser[0]]} pays {id_to_player[current_winner[0]]} {decimalfy(current_loser[1] * -1)}")
            winners[0][1] = current_net
            del losers[0]

        elif current_net < 0:
            print(f"{id_to_player[current_loser[0]]} pays {id_to_player[current_winner[0]]} {decimalfy(current_winner[1])}")
            losers[0][1] = current_net
            del winners[0]
        
        else:
            print(f"{id_to_player[current_loser[0]]} pays {id_to_player[current_winner[0]]} {decimalfy(current_winner[1])}")
            del winners[0]
            del losers[0]
        
        print_script(winners, losers)

print_script(winners, losers)