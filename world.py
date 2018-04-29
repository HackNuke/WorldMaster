import random

import nameGenerator as nameGen
import helperFunctions as hf
from location import *

class World:
    def __init__(self, numberOfLocations = 2, verbose = False):
        self.name = nameGen.generateName('locationName')
        self.numberOfLocations = numberOfLocations
        self.worldPopulation = 0
        self.locations = {}
        self.createLocations()
        self.year = 0
        if verbose:
            print("Created the world of", self.name)
            print("This world consists of", self.numberOfLocations, "locations:")
            counter = 1
            for locationKey, location in self.locations.items():
                print(str(counter) + ")", location)
                counter += 1
            print("World population is", str(self.worldPopulation) + ".")

    def __str__(self):
        print("The world of", self.name)
        print("World age:", self.year)
        print("This world consists of", self.numberOfLocations, "locations:")
        counter = 1
        pop = 0
        for locationKey, location in self.locations.items():
            print(str(counter) + ")", location)
            pop += location.population
            counter += 1
        self.worldPopulation = pop
        print("Total population is", self.worldPopulation)
        return ""

    def createLocations(self):
        newDungeonIndex = 2
        newSettlementIndex = 2
        while len(self.locations) < self.numberOfLocations:
            if "dungeon1" not in self.locations:
                # Starting dungeon
                self.locations["dungeon1"] = Dungeon()
                self.worldPopulation += self.locations["dungeon1"].population
            elif "settlement1" not in self.locations:
                # Starting settlement
                self.locations["settlement1"] = Settlement()
                self.worldPopulation += self.locations["settlement1"].population
            else:
                # Additional locations
                if hf.roll():
                    self.locations["dungeon" + str(newDungeonIndex)] = Dungeon()
                    self.worldPopulation += self.locations["dungeon" + str(newDungeonIndex)].population
                    newDungeonIndex += 1
                else:
                    self.locations["settlement" + str(newSettlementIndex)] = Settlement()
                    self.worldPopulation += self.locations["settlement" + str(newSettlementIndex)].population
                    newSettlementIndex += 1

    def simulateWorld(self, simYears = 1, verbose = False):
        for year in range(simYears):
            for locName, location in self.locations.items():
                if verbose:
                    print("Simulate a year for", locName)
                location.simulate(verbose=verbose)
        self.year += simYears