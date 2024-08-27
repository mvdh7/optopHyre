import optode

filenames = [
    # "data/underway_pH_1.txt",
    # "data/2023-05-26_145716_64PE517_NoSE_part3/2023-05-26_145716_64PE517_NoSE_part3.txt",
    # "data/2020-12-11_163148_NAPTRAM2020/2020-12-11_163148_NAPTRAM2020.txt",
    # "data/2022-02-24_221145_SO289/2022-02-24_221145_SO289.txt",
    "data/St16_VIDEO1_23430014.txt",
]

for filename in filenames:
    data = optode.read_split.read_pyrosci(filename)
