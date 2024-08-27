import pandas as pd


def read_pyrosci(filename):
    """Import the text files generated by PyroScience Workbench as a
    pandas DataFrame."""
    # Figure out how many rows to skip
    with open(filename, "r", encoding="unicode_escape") as f:
        lines = f.read().splitlines()
    i = 0
    sensor_type = "Unknown"
    while not lines[i].startswith("Date"):
        if lines[i].startswith("#Device Name") or lines[i].startswith("#Device:"):
            if "Pico" in lines[i]:
                sensor_type = "Pico"
            elif "AquapHOx" in lines[i]:
                sensor_type = "AquapHOx"
            else:
                sensor_type = "Unknown"
                print("Unknown sensor.")
        i += 1
    assert sensor_type != "Unknown"
    # Import data file
    data = pd.read_table(filename, skiprows=i, encoding="unicode_escape")
    # Rename columns
    rn = {
        "Pico": {
            "Date [A Ch.1 Main]": "date",
            "Time [A Ch.1 Main]": "time",
            " dt (s) [A Ch.1 Main]": "seconds",
            "pH [A Ch.1 Main]": "pH",
            "Sample Temp. (°C) [A Ch.1 CompT]": "temperature",
            "dphi (°) [A Ch.1 Main]": "phase_shift",
            "Signal Intensity (mV) [A Ch.1 Main]": "signal_intensity",
            "Ambient Light (mV) [A Ch.1 Main]": "ambient_light",
            "ldev (nm) [A Ch.1 Main]": "ldev",
            "Status [A Ch.1 Main]": "status_pH",
            "Status [A Ch.1 CompT]": "status_temperature",
        },
        "AquapHOx": {
            "DateTime (YYYY-MM-DD hh:mm:ss)": "datetime",
            "dphi (0.001 °)": "phase_shift",
            "dphi (0.001 ¡)": "phase_shift",
            # "umolar (0.001 umol/L)": "dissolved_oxygen",
            # "mbar (0.001 mbar)": "partial_pressure_oxygen",
            # "airSat (0.001 %air sat)": "dissolved_oxygen_air_saturation",
            "tempSample (0.001 °C)": "temperature",
            "tempSample (0.001 ¡C)": "temperature",
            "tempCase (0.001 °C)": "temperature_device",
            "tempCase (0.001 ¡C)": "temperature_device",
            "signalIntensity (0.001 mV)": "signal_intensity",
            "ambientLight (0.001 mV)": "ambient_light",
            "pressure (0.001 mbar)": "air_pressure",
            "humidity (0.001 %RH)": "humidity_device",
            "resistorTemp (0.001 Ohm or 0.001 mV)": "resistance",
            # "percentO2 (0.001 %O2)": "oxygen_volume_fraction",
            # "tempOptical (0.001 °C)": "temperature_opt_sensor",
            # "tempOptical (0.001 ¡C)": "temperature_opt_sensor",
            "pH (0.001 pH)": "pH",
        },
    }
    data = data.rename(columns=rn[sensor_type])
    # Wrangle datetime
    if sensor_type == "Pico":
        data["datetime"] = data.date + " " + data.time
        data["datetime"] = pd.to_datetime(data.datetime, format="%d-%m-%Y %H:%M:%S.%f")
    elif sensor_type == "AquapHOx":
        data["datetime"] = pd.to_datetime(data.datetime, format="%Y-%m-%d %H:%M:%S")
    # Drop NaNs and unnecessary columns
    data.dropna()
    cols = list({k for k in rn[sensor_type].values() if k not in ["date", "time"]})
    if sensor_type == "Pico":
        cols = ["datetime", *cols]
    data = data[cols]
    return data
