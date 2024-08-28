import pandas as pd


def determine_sensor_type(filename):
    """
    Determine the sensor type based on the device name in the file header.
    """
    with open(filename, "r", encoding="unicode_escape") as f:
        lines = f.read().splitlines()
    sensor_type = "Unknown"  # Default sensor type is Unknown
    for line in lines:
        if line.startswith("#Device Name") or line.startswith("#Device:"):
            if "Pico" in line:
                sensor_type = "Pico"
            elif "AquapHOx" in line:
                sensor_type = "AquapHOx"
            else:
                print("Unknown sensor.")
    return sensor_type


def find_data_start_row(lines):
    """
    Determine the row where actual data starts, indicated 'Date'.
    """
    i = 0  # Initialize row index
    while not lines[i].startswith("Date"):  # Loop until 'Date' is found
        i += 1
    return i


def read_pico(filename, skiprows):
    """
    Reads and processes data specific to the Pico sensor, handling cases where optional columns might not be present.
    """
    data = pd.read_table(
        filename, skiprows=skiprows, encoding="unicode_escape", low_memory=False
    )
    # Base renaming map for columns that are always present
    rn = {
        "Date [A Ch.1 Main]": "date",
        "Time [A Ch.1 Main]": "time",
        " dt (s) [A Ch.1 Main]": "seconds",
        "pH [A Ch.1 Main]": "pH",
        "Sample Temp. (°C) [A Ch.1 CompT]": "temperature",
        "dphi (°) [A Ch.1 Main]": "phase_shift",
        "Signal Intensity (mV) [A Ch.1 Main]": "signal_intensity",
        "Ambient Light (mV) [A Ch.1 Main]": "ambient_light",
        "Status [A Ch.1 Main]": "status_pH",
        "Status [A Ch.1 CompT]": "status_temperature",
    }
    # Optional columns which might not always be present
    optional_columns = {
        "ldev (nm) [A Ch.1 Main]": "ldev",
        "Date [A T1]": "date_T",
        "Time [A T1]": "time_T",
        " dt (s) [A T1]": "seconds_T",
        "Sample Temp. (°C) [A T1]": "temperature_T",
        "Status [A T1]": "status_temperature_T",
    }
    # Add optional columns to the renaming map if present
    for original, renamed in optional_columns.items():
        if original in data.columns:
            rn[original] = renamed

    # Apply the renaming map to the data
    data.rename(columns=rn, inplace=True)

    # Create datetime columns for the base dataset
    data["datetime"] = pd.to_datetime(
        data["date"] + " " + data["time"], format="%d-%m-%Y %H:%M:%S.%f"
    )
    # Create datetime columns for optional T data if applicable
    if "date_T" in data.columns and "time_T" in data.columns:
        data["datetime_T"] = pd.to_datetime(
            data["date_T"] + " " + data["time_T"], format="%d-%m-%Y %H:%M:%S.%f"
        )
    # Splitting data into main and T datasets
    data_T_columns = [c for c in data.columns if c.endswith("_T")]
    data_T = data[data_T_columns].dropna(how="all")
    data_main = data[[c for c in data.columns if c not in data_T_columns]]
    # Drop NaN values
    data_main = data_main.dropna(how="all")
    data_T = data_T.dropna(how="all")
    # Filter columns based on additional criteria, exclude "date" and "time"
    cols = [
        k
        for k in rn.values()
        if k not in ["date", "time", "date_T", "time_T"] and not k.endswith("_T")
    ]
    # Add the 'datetime' column to the list of columns to return
    cols = ["datetime"] + cols
    data_main = data_main[cols]

    return data_main, data_T


def read_aquaphox(filename, skiprows):
    """
    Reads and processes data specific to the AquapHOx sensor.
    """
    data = pd.read_table(filename, skiprows=skiprows, encoding="unicode_escape")
    rn = {  # Renaming columns based on sensor type
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
    }
    data.rename(columns=rn, inplace=True)  # Apply column renaming
    
    # Create a datetime column
    data["datetime"] = pd.to_datetime(data["datetime"], format="%Y-%m-%d %H:%M:%S")
    
    # Identify numeric columns (excluding datetime columns)
    numeric_columns = data.select_dtypes(include=['number']).columns
    
    # Divide the numeric columns by 1000
    data[numeric_columns] = data[numeric_columns] / 1000

    # Create a column with seconds
    data["seconds"] = (data["datetime"] - data["datetime"].iloc[0]).dt.total_seconds()

    return data


def read_pyrosci(filename):
    """
    Determine sensor type and dispatch to the appropriate reading function.
    """
    sensor_type = determine_sensor_type(filename)
    assert sensor_type != "Unknown", "Unknown sensor type."

    with open(filename, "r", encoding="unicode_escape") as f:
        print(filename)
        lines = f.read().splitlines()
    data_start_row = find_data_start_row(lines)  # Find the start of data

    if sensor_type == "Pico":
        return read_pico(filename, skiprows=data_start_row)
    elif sensor_type == "AquapHOx":
        return read_aquaphox(filename, skiprows=data_start_row)
