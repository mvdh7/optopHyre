import optopHyre

# Read all data files in data folder (could be changed to any folder)
combined_pico_main, combined_pico_T, combined_aquaphox_main, combined_aquaphox_T = (
    optopHyre.read.folder("data")
)

# Same but returning tuple
all_data = optopHyre.read.folder("data")
