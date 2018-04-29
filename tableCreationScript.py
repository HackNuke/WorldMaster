import os

from fileManagement import loadFile
from table import Table

loadMiscTables = True
MiscJsons = {}
MiscTables = {}

loadBTTTables = True
BTTJsons = {}
BTTTables = {}

loadDMGTables = True
DMGJsons = {}
DMGTables = {}

loadXGTETables = True
XGTEJsons = {}
XGTETables = {}


def main():
    if loadMiscTables:
        # Load BehindTheTables tables
        directoryString = "Tables/MiscTables/"
        directory = os.fsencode(directoryString)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                name = filename.replace(".txt", "")
                MiscJsons[name] = loadFile(directoryString + name)

        # Create objects of class Table
        id = 0
        for key, val in MiscJsons.items():
            # print(key, val)
            MiscTables[key] = Table(id=id, name=key,
                                    table={val["entries"][e]["entry"]: val["entries"][e]["description"]
                                           for e in range(val["size"])},
                                    probabilities=[float(val["entries"][p]["probability"])
                                                   for p in range(val["size"])])
            id += 1

    if loadBTTTables:
        # Load BehindTheTables tables
        directoryString = "Tables/BehindTheTables/"
        directory = os.fsencode(directoryString)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                name = filename.replace(".txt", "")
                BTTJsons[name] = loadFile(directoryString + name)

        # Create objects of class Table
        id = 0
        for key, val in BTTJsons.items():
            BTTTables[key] = Table(id=id, name=key,
                                   table={val["entries"][e]["entry"]: val["entries"][e]["description"]
                                          for e in range(val["size"])},
                                   probabilities=[float(val["entries"][p]["probability"])
                                                  for p in range(val["size"])])
            id += 1

    if loadDMGTables:
        # Load BehindTheTables tables
        directoryString = "Tables/DMGTables/"
        directory = os.fsencode(directoryString)

        id = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                name = filename.replace(".txt", "")
                DMGJsons[name] = loadFile(directoryString + name)

        # Create objects of class Table
        id = 0
        for key, val in DMGJsons.items():
            # print(key, val)
            DMGTables[key] = Table(id=id, name=key,
                                   table={val["entries"][e]["entry"]: val["entries"][e]["description"]
                                          for e in range(val["size"])},
                                   probabilities=[float(val["entries"][p]["probability"])
                                                  for p in range(val["size"])])
            id += 1

    if loadXGTETables:
        # Load Xanathar's Guide to Everything tables
        directoryString = "Tables/XGTETables"
        directory = os.fsencode(directoryString)

        id = 0
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                name = filename.replace(".txt", "")
                XGTEJsons[name] = loadFile(directoryString + name)

        # Create objects of class Table
        id = 0
        for key, val in XGTEJsons.items():
            # print(key, val)
            XGTETables[key] = Table(id=id, name=key,
                                    table={val["entries"][e]["entry"]: val["entries"][e]["description"]
                                           for e in range(val["size"])},
                                    probabilities=[float(val["entries"][p]["probability"])
                                                   for p in range(val["size"])])
            id += 1


if __name__ == "__main__":
    main()
