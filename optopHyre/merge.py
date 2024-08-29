import numpy as np


def ship_to_optode(ship, optode, interp_vars, inplace=True):
    """Linearly interpolate some variables from the ship df into the optode df.

    Parameters
    ----------
    ship : pandas.DataFrame
        Data to interpolate.  Must contain a column called 'datenum' which is used for
        the interpolation.
    optode : pandas.DataFrame
        Dataset to interpolate into.  Must contain a column called 'datenum'.
    interp_vars : list of str
        List of columns to interpolate.
    inplace : bool, optional
        Whether to add the columns to the optode df inplace. The default is True.

    Returns
    -------
    optode : pandas.DataFrame
        The optode df with added interpolated columns, which have '_ship' appended to
        their names.

    """
    if not inplace:
        optode = optode.copy()
    if isinstance(interp_vars, str):
        interp_vars = [interp_vars]
    datenum_ship = ship.datenum.values  # datenum --- timezone
    datenum_optode = optode.datenum.values
    vars_ship = ship[interp_vars].values.T
    for i, v in enumerate(interp_vars):
        vs = v + "_ship"
        if vs in optode:
            print(
                "Warning: overwriting existing column '{}' in the optode df!".format(vs)
            )
        optode[vs] = np.interp(datenum_optode, datenum_ship, vars_ship[i])
    return optode


def optode_to_ship(datenum_ship, datenum_optode, pH_optode, tol=None):
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
