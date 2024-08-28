import pandas as pd

def merge(data, ship_data, tolerance=pd.Timedelta(minutes=1)):
    
    # Copy datetime from pH data so it appears in new dataframe
    data = data.copy()
    data["datetime_pH"] = data["datetime"].copy()
    
    # Import pH data into ship data
    ship_data = pd.merge_asof(
        ship_data,
        data,
        on="datetime",
        direction="nearest",
        tolerance=tolerance,
    )
    
    # Sanity check for tolerance argument
    
    
    return ship_data
