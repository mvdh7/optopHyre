import pandas as pd
import numpy as np
import optopHyre

# data = optopHyre.read.file(
#     "data/2024-05-03_112508_64PE534-05/2024-05-03_112508_64PE534-05.txt"
# )[0]
# ship_data = pd.read_csv("data/shipsdata_NoSE2.csv", na_values="nan")
# ship_data["datetime"] = pd.to_datetime(ship_data["Date"])
# ship_data = ship_data.groupby(by="datetime").mean()

# ship_data_ = optopHyre.merge.merge(data, ship_data)

# %%
ship = pd.DataFrame({"x": [1.0, 2, 3, 4, 5]})
optode = pd.DataFrame(
    {
        "x": [1.1, 1.2, 1.9, 2.1, 4.5, 11.8],
        "y": [8.1, 8.2, 8.3, 8.4, 8.5, 8.6],
    }
)
merged = pd.merge_asof(ship, optode, on="x", tolerance=0.4, direction="nearest")

datenum_ship = ship.x.values  # datenum --- timezone
datenum_optode = optode.x.values
pH_optode = optode.y.values


def _optode_to_ship(datenum_ship, datenum_optode, pH_optode, tol=None):
    """Match pH_optode to nearest point in datenum_ship, averaging if multiple values
    of datenum_optode match the same datenum_ship.

    Parameters
    ----------
    datenum_ship : array of float
        The datenum (decimal days) of the ship/underway data points.
    datenum_optode : array of float
        The datenum (decimal days) of the optode sensor data points.
    pH_optode : array of float
        The pH values of the optode sensor.
    tol : float, optional
        The tolerance for matching between the datenums. The default is None, in which
        case it is automatically determined as half the distance between datenum_ship
        entries, which must be evenly spaced.

    Returns
    -------
    pH_ship : array of float
        The pH values matching the datenum_ship entries.
    """
    if tol is None:
        # Find gap between dt_ship entries if not provided by user
        tol = np.diff(datenum_ship)
        assert np.allclose(
            tol, np.mean(tol), rtol=0, atol=1e-8
        ), "datenum_ship is not evenly spaced!"
        tol = np.mean(tol) / 2
    # Get average pH for each ship point
    pH_ship = np.full(datenum_ship.shape, np.nan)
    for i, datenum in enumerate(datenum_ship):
        L = (datenum_optode >= datenum - tol) & (datenum_optode < datenum + tol)
        if np.any(L):
            pH_ship[i] = np.nanmean(pH_optode[L])
    return pH_ship


pH_ship = _optode_to_ship(datenum_ship, datenum_optode, pH_optode, tol=None)
