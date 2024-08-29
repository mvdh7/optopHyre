import pandas as pd
import numpy as np
from scipy import interpolate
import optopHyre

# data = optopHyre.read.file(
#     "data/2024-05-03_112508_64PE534-05/2024-05-03_112508_64PE534-05.txt"
# )[0]
# ship_data = pd.read_csv("data/shipsdata_NoSE2.csv", na_values="nan")
# ship_data["datetime"] = pd.to_datetime(ship_data["Date"])
# ship_data = ship_data.groupby(by="datetime").mean()

# ship_data_ = optopHyre.merge.merge(data, ship_data)

# %%
ship = pd.DataFrame(
    {
        "datenum": [1.0, 2, 3, 4, 5],
        "temperature": [25, 24.5, 26, 28, 29],
        "salinity": [35.0, 34, 36, 35, 34],
    }
)
optode = pd.DataFrame(
    {
        "datenum": [1.1, 1.2, 1.9, 2.1, 4.5, 11.8],
        "pH": [8.1, 8.2, 8.3, 8.4, 8.5, 8.6],
        "temperature_ship": 5,
    }
)

pH_optode = optode.pH.values

interp_vars = ["temperature", "salinity"]
interp_vars = "temperature"


# pH_ship = _optode_to_ship(datenum_ship, datenum_optode, pH_optode, tol=None)
