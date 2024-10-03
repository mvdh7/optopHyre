import optopHyre
import pandas as pd


def test_read_folder():
    # Read all data files in data folder (could be changed to any folder)
    combined_pico_main, combined_pico_T, combined_aquaphox_main, combined_aquaphox_T = (
        optopHyre.read.folder("data")
    )
    assert isinstance(combined_pico_main, pd.DataFrame)
    assert isinstance(combined_pico_T, pd.DataFrame)
    assert isinstance(combined_aquaphox_main, pd.DataFrame)
    assert isinstance(combined_aquaphox_T, pd.DataFrame)


# test_read_folder()
