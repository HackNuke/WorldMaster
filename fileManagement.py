import json
import os


def createNewFile(filePath):
    try:
        with open(filePath + ".txt", 'w') as file:
            # Table name
            tableName = input("Enter table name (enter to return): ")
            if tableName == "":
                return True
            # Source
            source = input("Enter table source: ")

            # Table size
            tableSize = -1
            while tableSize < 0:
                try:
                    tableSize = int(input("Enter table size (0 for custom): "))
                except Exception as err:
                    print("Please enter a positive integer. ", err)

            if tableSize == 0:
                customSize = True
                loopCount = 0
            else:
                customSize = False
                loopCount = tableSize
            # Write table entries
            entries = []
            i = 0
            while i < loopCount or customSize:
                if customSize:
                    newEntry = input("Enter table entry " + str(i + 1) + " (enter to end): ")
                else:
                    newEntry = input("Enter table entry" + str(i + 1) + "/" + str(tableSize) + ": ")
                if newEntry == "" and customSize:
                    break
                elif newEntry != "" and customSize:
                    entries.append(newEntry)
                    tableSize += 1
                elif not customSize:
                    entries.append(newEntry)
                i += 1

            choice = ""
            while choice.lower() != 'y' and choice.lower() != 'n':
                try:
                    choice = input("Add probabilities for entries? y/n")
                except Exception as err:
                    print("Please enter y/n. ", err)

            probabilities = []
            if choice.lower() == 'y':
                # Write entries' probabilities
                for i in range(tableSize):
                    probabilities.append(input("Enter probability for table entry " + str(i + 1) + "/" +
                                               str(tableSize) + ": "))
            else:
                for i in range(tableSize):
                    probabilities.append(1.0)

            choice = ""
            while choice.lower() != 'y' and choice.lower() != 'n':
                try:
                    choice = input("Add descriptions for entries? y/n")
                except Exception as err:
                    print("Please enter y/n. ", err)

            descriptions = []
            if choice.lower() == 'y':
                # Write entries' descriptions
                for i in range(tableSize):
                    descriptions.append(input("Enter description for table entry " + str(i + 1) + "/" +
                                              str(tableSize) + ": "))
            else:
                for i in range(tableSize):
                    descriptions.append("")

            dictionary = {'source': source, 'tableName': tableName, 'size': tableSize,
                          'entries': [
                              {"entry": entries[i],
                               "probability": probabilities[i],
                               "description": descriptions[i]} for i in range(tableSize)
                          ]}
            file.write(json.dumps(dictionary))

        return True

    except Exception as err:
        print("Error while creating new file: " + str(err))
        return False

def loadFile(filePath):
    try:
        with open(filePath + ".txt", 'r') as file:
            dictionary = json.loads(file.read())
            return dictionary
    except Exception as err:
        print("Error while loading file: " + str(err))
        return False


def deleteFile(filePath):
    try:
        os.remove(filePath + ".txt")
        return True
    except Exception as err:
        print("Error while deleting file: " + str(err))
        return False

def main():
    # Menu
    while True:
        print("1. Create new file.")
        print("2. Load file.")
        print("3. Delete file.")
        print("0. Exit.")
        try:
            choice = int(input())
        except:
            print("Please enter an integer.")
            continue

        if choice == 0:
            exit()

        elif choice == 1:
            print()
            print("Create new file")
            complete = False
            while not complete:
                inp = input("Enter file path (or enter to return): ")
                if inp == "":
                    complete = True
                    break
                complete = createNewFile(inp)

        elif choice == 2:
            print()
            print("Load file")
            complete = False
            while not complete:
                inp = input("Enter file path to load (or enter to return): ")
                if inp == "":
                    complete = True
                    break
                complete = loadFile(inp)
                if complete != False and type(complete) == dict:
                    # Print loaded table
                    print()
                    print("Source: ", complete["source"])
                    print("Name:   ", complete["tableName"])
                    print("Size:   ", complete["size"])
                    for i in range(complete["size"]):
                        print(complete["entries"][i])
                    print()
                    complete = True

        elif choice == 3:
            print()
            print("Delete file")
            complete = False
            while not complete:
                inp = input("Enter file path to delete (or enter to return): ")
                if inp == "":
                    complete = True
                    break
                complete = deleteFile(inp)


if __name__ == "__main__":
    main()
