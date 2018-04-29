import random
import numpy as np

import helperFunctions as hf

class Table:
    def __init__(self, id=None, name="Unnamed", table=None, descriptions=None, probabilities=None, verbose=False):

        self.id = id
        self.name = name
        self.descriptions = descriptions
        self.setTable(table, descriptions, probabilities)
        if verbose:
            print("Created new table with id:", self.id, ", name:", self.name, ", table:", self.table,
                  ", descriptions:", self.descriptions, ", probabilities:", self.probabilities)
        self.secondaryTable = None
        self.secondaryProbabilities = None

    def __str__(self):
        print("Table:", self.table)
        print("Probabilities:", self.probabilities)
        if self.secondaryTable != None:
            print("Secondary Table:", self.secondaryTable)
        if self.secondaryTable != None:
            print("Secondary Probabilities:", self.secondaryProbabilities)
        return ""

    def getTable(self):
        return self.table

    def getProbabilities(self):
        return self.probabilities

    def getSecondaryTable(self):
        return self.secondaryTable

    def getSecondaryProbabilities(self):
        return self.secondaryProbabilities

    def setTable(self, table=None, descriptions=None, probabilities=None):

        if table == None and probabilities == None:
            # Empty table and empty probabilities
            # Empty object initialized
            self.table = {}
            self.probabilities = []

        elif table != None and probabilities == None:
            # Non empty table, empty probabilities
            # Initialize with default probabilities, uniform distribution
            self.table = table
            self.probabilities = hf.normalizeToSum([1.0 for i in range(len(table))])

        elif table == None and probabilities != None:
            # Empty table, non empty probabilities
            # Initialize table with empty strings with length equal to probabilities length
            self.table = {"": "" for i in range(len(probabilities))}
            self.probabilities = hf.normalizeToSum(probabilities)

        else:
            # Both table and probabilities are supplied
            # Check for wrong size
            if len(table) != len(probabilities):
                print("Table and probabilities must be of equal size.")
                print("Reverting to default probabilities/uniform distribution.")
                self.probabilities = hf.normalizeToSum([1.0 for i in range(len(table))])
            else:
                self.probabilities = hf.normalizeToSum(probabilities)

            self.table = table

    def setSecondaryTable(self, table, probabilities=None):

        if table == None and probabilities == None:
            # Empty table and empty probabilities
            # Empty object initialized
            self.secondaryTable = {}
            self.secondaryProbabilities = []

        elif table != None and probabilities == None:
            # Non empty table, empty probabilities
            # Initialize with default probabilities, uniform distribution
            self.secondaryTable = table
            self.secondaryProbabilities = hf.normalizeToSum([1.0 for i in range(len(table))])

        elif table == None and probabilities != None:
            # Empty table, non empty probabilities
            # Initialize table with empty strings with length equal to probabilities length
            self.secondaryTable = {"": "" for i in range(len(probabilities))}
            self.secondaryProbabilities = hf.normalizeToSum(probabilities)

        else:
            # Both table and probabilities are supplied
            # Check for wrong size
            if len(table) != len(probabilities):
                print("Table and probabilities must be of equal size.")
                print("Reverting to default probabilities/uniform distribution.")
                self.secondaryProbabilities = hf.normalizeToSum([1.0 for i in range(len(table))])
            else:
                self.secondaryProbabilities = hf.normalizeToSum(probabilities)

            self.secondaryTable = table

    def rollTable(self, customProbabilities = None):

        if self.table != None and self.probabilities != None and \
                len(self.table) != 0 and len(self.probabilities) != 0:

            if customProbabilities == None:
                # Roll with table default probabilities
                randomKey = random.choices([key for key, val in self.table.items()], self.probabilities, k=1)[0]
            else:
                # Check if custom probabilities are of correct size
                if len(self.table) != len(customProbabilities):
                    print("Table and custom probabilities must be of equal size.")
                    print("Reverting to table default probabilities.")
                    print("Table ", self.name,"is of size:", len(self.table))
                    randomKey = random.choices([key for key, val in self.table.items()], self.probabilities, k=1)[0]
                else:
                    # Roll with custom supplied probabilities
                    randomKey = random.choices([key for key, val in self.table.items()], customProbabilities, k=1)[0]

            # Return the rolled item (randomKey) and its description
            return randomKey, self.table[randomKey]

        else:
            print("Table is empty.")
            return None

    def rollSecondaryTable(self, customProbabilities = None):

        if self.secondaryTable != None and self.secondaryProbabilities != None and \
                len(self.secondaryTable) != 0 and len(self.secondaryProbabilities) != 0:

            if customProbabilities == None:
                # Roll with table default probabilities
                randomKey = random.choices(
                    [key for key, val in self.secondaryTable.items()], self.secondaryProbabilities, k=1)[0]
            else:
                # Check if custom probabilities are of correct size
                if len(self.secondaryTable) != len(customProbabilities):
                    print("Table and custom probabilities must be of equal size.")
                    print("Reverting to table default probabilities.")
                    print("Table is of size: ", len(table))
                    randomKey = random.choices([key for key, val in self.secondaryTable.items()],
                                               self.secondaryProbabilities, k=1)[0]
                else:
                    # Roll with custom supplied probabilities
                    randomKey = random.choices([key for key, val in self.secondaryTable.items()],
                                               customProbabilities, k=1)[0]

            # Return the rolled item (randomKey) and its description
            return randomKey, self.secondaryTable[randomKey]

        else:
            print("Secondary table is empty.")
            return None
