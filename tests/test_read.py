import optode

filenames = ["data/underway_pH_1.txt"]

for filename in filenames:
    data = optode.read.read_pyrosci(filename)
