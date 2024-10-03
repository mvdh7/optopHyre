import optopHyre
import pandas as pd

filenames = [
    "data/underway_pH_1.txt",
    "data/2023-05-26_145716_64PE517_NoSE_part3/2023-05-26_145716_64PE517_NoSE_part3.txt",
    "data/2020-12-11_163148_NAPTRAM2020/2020-12-11_163148_NAPTRAM2020.txt",
    "data/2022-02-24_221145_SO289/2022-02-24_221145_SO289.txt",
    "data/St16_VIDEO1_23430014.txt",
]


def test_read_file():
    for filename in filenames:
        data = optopHyre.read.file(filename)
        assert len(data) == 2
        assert isinstance(data[0], pd.DataFrame)


# test_read_file()
