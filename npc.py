import random

import config as conf
import helperFunctions as hf
from nameGenerator import nameGen

from tableCreationScript import DMGTables
from tableCreationScript import XGTETables
from tableCreationScript import BTTTables
from tableCreationScript import MiscTables

class NPC:
    def __init__(self, isAlive = True, race = "human", raceProb = None, gender = "random",
                 age = "random", lastName = "random", bornIn = None):

        self.isAlive = isAlive
        self.bornIn = bornIn
        self.currentLocation = bornIn
        ################################################################################################################
        # Race
        if race == "random":
            self.race = MiscTables["PlayableRaces"].rollTable(customProbabilities=raceProb)[0].lower()
        else:
            self.race = race.lower()

        ################################################################################################################
        # Gender
        if gender == "random":
            self.gender = MiscTables["Gender"].rollTable()[0].lower()
        else:
            self.gender = gender.lower()

        if self.gender == "female":
            self.offspringProb = conf.offspringProb
            self.pregnant = False

        ################################################################################################################
        # Age
        if age == "random":
            self.age = self.rollAge()
        else:
            self.age = age
        self.ageGroup = ""
        self.ageGroupInd = 0
        self.assignAgeGroup()

        ################################################################################################################
        # Name
        if self.gender == "male":
            self.firstName = nameGen.generateName('male')
        elif self.gender == "female":
            self.firstName = nameGen.generateName('female')
        # else:
        #     self.firstName = nameGen.generateName('asexual')

        if lastName== "random":
            self.lastName = nameGen.generateName('surname')
        else:
            self.lastName = lastName

        ################################################################################################################
        # Job
        self.job = None
        self.workplace = None
        self.isRetired = False
        # if self.ageGroup == "child":
        #     self.job = None
        #     self.isRetired = False
        #
        # elif self.ageGroup == "senior":
        #     self.job = BTTTables["Professions"].rollTable()[0]
        #     self.isRetired = hf.roll(conf.seniorIsRetiredChance)
        #
        # elif self.ageGroup == "youth":
        #     if hf.roll():
        #         self.job = BTTTables["Professions"].rollTable()[0]
        #         self.isRetired = False
        #     else:
        #         self.job = None
        #         self.isRetired = False
        #
        # else: # adult
        #     self.job = BTTTables["Professions"].rollTable()[0]
        #     self.isRetired = hf.roll(conf.adultIsRetiredChance)

        ################################################################################################################
        # Relationships
        self.isHomosexual = False # Gender preference
        self.loveInterest = None # Who they are reallly interested for, might be spouse or someone else
        self.relationshipPartner = None # # If the NPC is in a relationship this is their partner
        self.spouse = None  # wife, husband, etc.
        self.isWidowed = False # wife, husband, etc.

        self.children = []

        self.mother = None # This npc's mother
        self.father = None # This npc's father

        self.siblings = []

        ################################################################################################################
        # Description

        # Facial characteristics
        self.facialCharacteristics = {}
        self.facialCharacteristics["eyes"] = BTTTables["NPCTraitsEyes"].rollTable()[0]
        self.facialCharacteristics["ears"] = BTTTables["NPCTraitsEars"].rollTable()[0]
        self.facialCharacteristics["mouth"] = BTTTables["NPCTraitsMouth"].rollTable()[0]
        self.facialCharacteristics["nose"] = BTTTables["NPCTraitsNose"].rollTable()[0]
        self.facialCharacteristics["chinJaw"] = BTTTables["NPCTraitsChinJaw"].rollTable()[0]
        self.facialCharacteristics["hair"] = BTTTables["NPCTraitsHair"].rollTable()[0]
        self.facialCharacteristics["face"] = BTTTables["NPCTraitsFace"].rollTable()[0]

        # Physical characteristics
        self.physicalCharacteristics = {}
        self.physicalCharacteristics["height"] = BTTTables["NPCTraitsHeight"].rollTable()[0]
        self.physicalCharacteristics["body"] = BTTTables["NPCTraitsBody"].rollTable()[0]
        self.physicalCharacteristics["hands"] = BTTTables["NPCTraitsHands"].rollTable()[0]
        self.physicalCharacteristics["scar"] = BTTTables["NPCTraitsScar"].rollTable()[0]

        # Accessories
        self.accessories = {}
        self.accessories["tattoo"] = "Tattoo: " + BTTTables["NPCTraitsTattoo"].rollTable()[0].lower()
        self.accessories["jewelry"]= "Wears " + BTTTables["NPCTraitsJewelry"].rollTable()[0].lower() + " made of " + \
                                     BTTTables["NPCTraitsJewelryMaterial"].rollTable()[0].lower()
        self.accessories["clothes"]= "Clothes are " + BTTTables["NPCTraitsClothes"].rollTable()[0].lower()

        # Emotions and attitude
        self.emotionsAndAttitude = {}
        self.emotionsAndAttitude["calmTrait"] = "When calm he/she is " + \
                                                BTTTables["NPCTraitsCalmTrait"].rollTable()[0].lower()
        self.emotionsAndAttitude["stressTrait"]= "When stressed he/she is " + \
                                                 BTTTables["NPCTraitsStressTrait"].rollTable()[0].lower()
        self.emotionsAndAttitude["mood"]= "Current mood is " + BTTTables["NPCTraitsMood"].rollTable()[0].lower()

        # Other, faiths - beliefs - flaws
        self.other= {}
        self.other["faith"] = BTTTables["NPCTraitsFaith"].rollTable()[0].lower()
        self.other["prejudice"] = BTTTables["NPCTraitsPrejudice"].rollTable()[0].lower()

        # Flaw
        self.other["flaw"] = BTTTables["NPCTraitsFlaw"].rollTable()[0].lower()

    def __str__(self):
        print("Name: " + self.firstName, self.lastName)
        print("Alive: " + str(self.isAlive))
        print("Race: " + self.race)
        print("Gender: " + self.gender)
        print("Born in: " + self.bornIn.name)
        print("Age group: " + self.ageGroup)
        print("Age: " + str(self.age))
        if self.father != None:
            print("Father name: " + self.father.firstName + " " + self.father.lastName)
        if self.mother != None:
            print("Mother name: " + self.mother.firstName + " " + self.mother.lastName)

        print("Is homosexual: " + str(self.isHomosexual))

        if self.loveInterest != None:
            print("Love interest: " + self.loveInterest.firstName + " " + self.loveInterest.lastName)

        if self.relationshipPartner != None:
            print("Relationship partner: ", self.relationshipPartner.firstName, self.relationshipPartner.lastName)

        elif self.isWidowed:
            print("Widow/widower")
        if self.spouse != None:
            print("Spouse: " + self.spouse.firstName, self.spouse.lastName)

        if len(self.children) != 0:
            for child in self.children:
                print("Child: " + child.firstName, child.lastName)
        if len(self.siblings) != 0:
            for sibling in self.siblings:
                print("Sibling: " + sibling.firstName, sibling.lastName)

        if self.job != None:
            print("Job: " + self.job + " of " + self.workplace)
        elif self.isRetired:
            print("Job: NPC is retired")
        print("Facial characteristics:", [val for key, val in self.facialCharacteristics.items()])
        print("Physical characteristics:", [val for key, val in self.physicalCharacteristics.items()])
        print("Accessories:", [val for key, val in self.accessories.items()])
        print("Emotions and Attitude:", [val for key, val in self.emotionsAndAttitude.items()])
        print("Other:", [val for key, val in self.other.items()])
        return ""

    def rollAge(self):
        age = 0
        # TODO add more races
        if self.race == "human":
            age = random.randrange(0, 120) # [0, 120)
        elif self.race == "dwarf":
            age = random.randrange(0, 400)
        return age

    def assignAgeGroup(self):
        ageGroupLimits = conf.ageGroupLimits
        if self.age < ageGroupLimits[self.race][0]:
            self.ageGroup = conf.ageGroups[0] # Child
            self.ageGroupInd = 0
            return True # ageGroup changed
        elif self.age >= ageGroupLimits[self.race][0] and self.age < ageGroupLimits[self.race][1]:
            self.ageGroup = conf.ageGroups[1] # Youth
            self.ageGroupInd = 1
            return True # ageGroup changed
        elif self.age >= ageGroupLimits[self.race][1] and self.age < ageGroupLimits[self.race][2]:
            self.ageGroup = conf.ageGroups[2] # youngAdult
            self.ageGroupInd = 2
            return True # ageGroup changed
        elif self.age >= ageGroupLimits[self.race][2] and self.age < ageGroupLimits[self.race][3]:
            self.ageGroup = conf.ageGroups[3] # Adult
            self.ageGroupInd = 3
            return True # ageGroup changed
        elif self.age >= ageGroupLimits[self.race][3]:
            self.ageGroup = conf.ageGroups[4] # Senior
            self.ageGroupInd = 4
            return True # ageGroup changed

    def yearUpdate(self):
        # Return arguments dictionary
        returnDict = {}
        # Update age and ageGroup
        self.age += 1
        changedAgeGroup = self.assignAgeGroup()

        ################################################################################################################
        # Marriage
        # General probability of NPC becoming married for the first time
        if self.spouse == None and hf.roll(conf.getMarriedProb*conf.multipGetMarriedProb[self.ageGroupInd]):
            returnDict["gotMarried"] = True
        # NPC gets married after the old spouse died
        if self.isWidowed and hf.roll(conf.getMarriedProb*conf.multipWidowGetMarriedProb[self.ageGroupInd]):
            returnDict["gotMarried"] = True

        ################################################################################################################
        # Birth
        # Is the NPC pregnant or has she given birth to a child?
        # If NPC is female and is already pregnant the child is born!
        if self.gender == "female" and self.pregnant:
            returnDict["childBorn"] = True

        # If NPC is female of appropriate age and is married or in a relationship there is a chance she becomes pregnant
        if self.gender == "female" and self.age > conf.ageGroupLimits[self.race][0] and not self.pregnant and \
                ((self.spouse != None and not self.isWidowed) or self.relationshipPartner != None) and \
                hf.roll(self.offspringProb*conf.multipOffspringProb[self.ageGroupInd]):
            # NPC is pregnant!
            self.pregnant = True
            # Reduce probability for next child
            self.offspringProb = self.offspringProb * conf.offspringProb

        ################################################################################################################
        # Death
        # Did the npc die?
        if hf.roll(conf.yearlyDeathProb * conf.multipYearlyDeathProb[self.ageGroupInd]):
            self.isAlive = False
            returnDict["died"] = True

        ################################################################################################################
        # Job
        # Did the npc retire? NPC must have a job and not be retired. Owners don't retire.
        if self.job != "owner" and self.job != None and not self.isRetired and\
                hf.roll(conf.retireProb*conf.multipRetireProb[self.ageGroupInd]):
            returnDict["retired"] = True

        # Did the npc find a job?
        if self.job == None and not self.isRetired and \
                hf.roll(conf.findJobProb * conf.multipFindJobProb[self.ageGroupInd]):
            returnDict["foundJob"] = True

        ################################################################################################################

        # TODO add other stuff that can happen in a year, eg get a job when of appropriate age

        return returnDict