import pandas as pd
import optopHyre

data = optopHyre.read_split.read_pyrosci("data/2024-05-03_112508_64PE534-05/2024-05-03_112508_64PE534-05.txt")[0]
ship_data = pd.read_csv("data/shipsdata_NoSE2.csv", na_values="nan")
ship_data["datetime"] = pd.to_datetime(ship_data["Date"])
ship_data = ship_data.groupby(by="datetime").mean()

ship_data_ = optopHyre.merge.merge(data, ship_data)
