# consumption:耗電 generation:產電 holdings:當前持有量
import pandas as pd
import numpy as np


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


def strategy(generation, consumption):
    generation = pd.read_csv(generation, header=None)
    consumption = pd.read_csv(consumption, header=None)

    get_date = generation.iloc[-1, 0]
    month = int(get_date.split('-')[1])
    day = int(get_date.split('-')[2].split(' ')[0])

    next_day = day
    next_month = month
    if (month == 4 or month == 6 or month == 9 or month == 11):
        if (day == 30):
            next_month = month + 1
            next_day = 1
        else:
            next_day = day + 1
    else:
        if (day == 31):
            next_month = month + 1
            next_day = 1
        else:
            next_day = day + 1

    generation = generation.drop([0])
    generation = generation.drop([0], axis=1)
    consumption = consumption.drop([0])
    consumption = consumption.drop([0], axis=1)

    generation = generation.iloc[-24:]
    generation = generation.values.astype(float)
    consumption = consumption.iloc[-24:]
    consumption = consumption.values.astype(float)

    ans = []
    action = []
    for i in range(generation.shape[0]):
        holdings = generation[i]
        
        # sell generation - consumption
        if generation[i] - consumption[i] > 0:
            if (i < 10):
                action.append("2018-" + str(next_month) + "-" + str(next_day) + " 0" + str(i) + ":00:00")
            elif (i >= 10):
                action.append("2018-" + str(next_month) + "-" + str(next_day) + " " + str(i) + ":00:00")
                
            volume = generation[i] - consumption[i]
            holdings = holdings - volume
            volume = round(volume.tolist()[0], 2)
            
            action.append("sell")
            action.append(0.01)
            action.append(volume)
            ans.append(action)
            action = []
            
        # buy consumption - generation
        if generation[i] - consumption[i] < 0:
            if (i < 10):
                action.append("2018-" + str(next_month) + "-" + str(next_day) + " 0" + str(i) + ":00:00")
            elif (i >= 10):
                action.append("2018-" + str(next_month) + "-" + str(next_day) + " " + str(i) + ":00:00")

            volume = consumption[i] - generation[i]
            volume = round(volume.tolist()[0], 2)
            
            action.append("buy")
            action.append(2.52)
            action.append(volume)
            ans.append(action)
            action = []
        
        # sell holdings
        if (i < 10):
            action.append("2018-" + str(next_month) + "-" + str(next_day) + " 0" + str(i) + ":00:00")
        elif (i >= 10):
            action.append("2018-" + str(next_month) + "-" + str(next_day) + " " + str(i) + ":00:00")
        
        volume = round(holdings.tolist()[0], 2)
        
        action.append("sell")
        action.append(2.53)
        action.append(volume)
        ans.append(action)
        action = []

    return ans


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv",
                        help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    args = parser.parse_args()

    ans = strategy(args.generation, args.consumption)
    output(args.output, ans)
