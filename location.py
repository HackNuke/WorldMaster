# Location classes
# Parent class "Location" and children classes like "Dungeon", "Settlement", etc.

import random

import config as conf
import helperFunctions as hf
from npcHandler import *
from nameGenerator import nameGen

from tableCreationScript import DMGTables
from tableCreationScript import XGTETables
from tableCreationScript import BTTTables
from tableCreationScript import MiscTables


class Location:
    def __init__(self):
        pass

class Dungeon(Location):
    def __init__(self):
        super().__init__()

        self.name = nameGen.generateName('locationName')
        self.population = 0

    def __str__(self):
        print("Dungeon:", self.name)
        return ""

    def simulate(self, simYears=1, verbose = False):
        pass

class Settlement(Location):
    def __init__(self, race = "human", size = "random"):
        super().__init__()

        self.name = nameGen.generateName('locationName')
        self.race = race # Default race for a settlement is human, 64% of population is human
        if size == "random":
            self.settlementSize = MiscTables["SimpleSettlements"].rollTable()[0]
        else:
            self.settlementSize = size

        # Set up population
        populationRange = MiscTables["SimpleSettlements"].table[self.settlementSize]
        populationRange = [int(populationRange.split("-")[0]), int(populationRange.split("-")[1])]
        self.population = int(int(random.randrange(populationRange[0], populationRange[1])/2) * 2) # Make it even

        self.aliveNPCDict = {}

        npcGenerator(self.aliveNPCDict, self.population, self, self.race)

        self.businesses = {}
        # Example business
        # "Name": {type: "tavern",
        #          jobs: {"owner": npcObj1, "cook": npcObj2, "waiter": npcObj3},
        #          etc.
        #         }
        self.addBusinesses()

    def __str__(self):
        print("Settlement:", self.name)
        print("Population size:", self.population)
        return ""


    def addBusinesses(self):
        # addBusinesses runs only at the initialization, so there is no need to check for NPC
        # age, etc. All NPCs of seed population are eligible.
        for businessType, SV in conf.SVDict.items():
            SVRatio = self.population / SV
            businessesCount = SVRatio//1 # The village has *businessesCount* of this business
            if hf.roll(SVRatio - SVRatio//1): # Chance to add one more (or just one if SVRatio < 1.0)
                businessesCount += 1


            # print(businessesCount)
            # print("The settlement has", SVRatio//1, businessType, "and", SVRatio - SVRatio//1, "chance for one more.")

            # If current businessType is governement, there can't be more than one government
            if businessType == "Government" and businessesCount > 1.0:
                businessName = "government"
                self.businesses[businessName] = \
                    {
                        "type": businessType,
                        "jobs":
                            {
                                "chancellor": None,  # Head of state
                                "steward": None,     # Second in command, governor
                                "chamberlain": None, # Head of economy
                                "chaplain": None,    # Head of religion, cleric
                                "secretary": None    # Head of communication, advisor
                            },
                        "vacancies": 5
                    }

                for job in self.businesses[businessName]["jobs"]:
                    for npcName, npc in self.aliveNPCDict.items():
                        if npc.job == None and self.businesses[businessName]["jobs"][job] == None:
                            self.businesses[businessName]["jobs"][job]
                            npc.job = job
                            npc.workplace = businessName
                            self.businesses[businessName]["jobs"][job] = npc
                            self.businesses[businessName]["vacancies"] -= 1
                            break

            elif businessType != "Government":
                for b in range(int(businessesCount)):
                    businessName = businessType + str(b + 1)
                    self.businesses[businessName] = \
                        {
                            "type": businessType,
                            "jobs":
                            {
                                "owner": None,
                                "worker1": None,
                                "worker2": None
                            },
                            "vacancies": 3
                        }
                    for job in self.businesses[businessName]["jobs"]:
                        for npcName, npc in self.aliveNPCDict.items():
                            if npc.job == None and self.businesses[businessName]["jobs"][job] == None:
                                self.businesses[businessName]["jobs"][job]
                                npc.job = job
                                npc.workplace = businessName
                                self.businesses[businessName]["jobs"][job] = npc
                                self.businesses[businessName]["vacancies"] -= 1
                                break
            # input()

    def simulate(self, simYears=1, verbose = False):
        inp = 'y'
        pop = []

        yearCounter = 0
        while yearCounter < simYears:
            simulateNPCsYear(self.aliveNPCDict, self.businesses)

            for npcName, npc in self.aliveNPCDict.items():
                pass

            pop.append(len(self.aliveNPCDict))

            yearCounter += 1

            if verbose:
                print("Current population of", self.name + ":", pop[-1])

            if pop[-1] == 0:
                break

        self.population = pop[-1]