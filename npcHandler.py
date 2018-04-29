import config as conf
from npc import NPC
from random import randrange

from tableCreationScript import MiscTables


def npcGenerator(aliveNPCDict, maxPopulation, location, race = "human"):
    # Create seed population with 18 year old couples
    for pop in range(int(maxPopulation / 2)):
        if race == "human":
            coupleRace = MiscTables["BasicRaces"].rollTable()[0].lower()
        else:
            pass #TODO
        # Create male and add him to the alive population dictionary
        maleNPC = NPC(race=coupleRace, gender="male", isAlive=True, bornIn=location,
                      age=randrange(conf.ageGroupLimits[coupleRace][1], conf.ageGroupLimits[coupleRace][2]))
        aliveNPCDict[maleNPC.firstName + " " + maleNPC.lastName] = maleNPC

        # Create female and add her to the alive population dictionary
        femaleNPC = NPC(race=coupleRace, gender="female", isAlive=True, bornIn=location,  lastName=maleNPC.lastName,
                        age = randrange(conf.ageGroupLimits[coupleRace][1], conf.ageGroupLimits[coupleRace][2]))
        aliveNPCDict[femaleNPC.firstName + " " + femaleNPC.lastName] = femaleNPC

        # Marry the NPCs
        marryNPCs(maleNPC, femaleNPC)

        # print(maleNPC)
        # print(femaleNPC)
        # input()

def simulateNPCsYear(aliveNPCDict, businesses):
    for npcName in aliveNPCDict.copy():
        npc = aliveNPCDict[npcName]
        if not npc.isAlive:
            continue

        # Simulate
        returnDict = npc.yearUpdate()

        # Handle returnDict events that happened in a year
        for key, val in returnDict.items():
            if key == "died" and val == True:
                # NPC died
                npc.isAlive = False

                # NPC dying leaves behind a widow/widower
                if npc.spouse != None:
                    npc.spouse.isWidowed = True

                # If NPC had a job, it is now vacant
                if npc.job != None:
                    businesses[npc.workplace]["jobs"][npc.job] = None
                    businesses[npc.workplace]["vacancies"] += 1

                del aliveNPCDict[npc.firstName + " " + npc.lastName]

            if key == "childBorn" and val == True:
                npc.pregnant = False
                # NPC gave birth to a baby
                baby = NPC(race=npc.race, age=0, isAlive=True, bornIn=npc.currentLocation, lastName=npc.lastName)

                # Add mother/father to baby
                baby.mother = npc
                baby.father = npc.spouse

                # Add sibling relationships
                for sibling in baby.mother.children:
                    sibling.siblings.append(baby)
                    baby.siblings.append(sibling)

                # Add to mother/father children lists
                baby.mother.children.append(baby)
                baby.father.children.append(baby)

                aliveNPCDict[baby.firstName + " " + baby.lastName] = baby

            if key == "retired" and val == True:
                businesses[npc.workplace]["jobs"][npc.job] = None
                businesses[npc.workplace]["vacancies"] += 1

                npc.isRetired = True
                npc.job = None
                npc.workplace = None

            if key == "foundJob" and val == True:
                # Loop through all businesses
                foundJob = False
                for businessName in businesses:
                    # Find business with vacancy
                    if businesses[businessName]["vacancies"] >= 1:
                        # Loop through jobs to find the available one, or one of the available jobs
                        for jobName in businesses[businessName]["jobs"]:
                            if businesses[businessName]["jobs"][jobName] == None: # Eg. "worker1" : None
                                businesses[businessName]["jobs"][jobName] = npc
                                businesses[businessName]["vacancies"] -= 1

                                npc.job = jobName
                                npc.workplace = businessName

                                foundJob = True
                                break
                    # If a job is found, then stop looking for vacancies
                    if foundJob:
                        break

            if key == "gotMarried" and val == True:
                # NPC got married to another NPC
                # Find an elligible NPC
                for otherNPCName, otherNPC in aliveNPCDict.items():
                    if otherNPC.lastName != npc.lastName:
                        if otherNPC.ageGroup == npc.ageGroup and otherNPC.gender != npc.gender and \
                                (otherNPC.spouse == None or otherNPC.isWidowed) and npc.race == otherNPC.race:
                            marryNPCs(npc, otherNPC)
                            # print("Married NPCs!")
                            # print(npc)
                            # print(otherNPC)
                            break


def marryNPCs(npc1, npc2):
    npc1.spouse = npc2
    npc2.spouse = npc1

# def createOffspring(npcMale, npcFemale,
#                     offspringProb=conf.offspringProb, maxOffspring = conf.maxOffspring, deadChance = 0.1):
#     # Give the couple children
#     createdOffspingList = []
#
#     # Assign appropriate age group to the offspring based on parent's age group
#     offspringAgeGroup = None
#     if npcMale.ageGroup == "senior":
#         offspringAgeGroup = hf.rollList(["adult", "senior"])
#     elif npcMale.ageGroup == "adult":
#         offspringAgeGroup = hf.rollList(["adult", "youth", "child"])
#     elif npcMale.ageGroup == "youth":
#         offspringAgeGroup = hf.rollList(["child"])
#
#     for offspringCount in range(maxOffspring):
#         if hf.roll(offspringProb):
#             offspringNPC = NPC(race="Human", ageGroup=offspringAgeGroup, isAlive=hf.roll(1.0 - deadChance),
#                                lastName=npcMale.lastName)
#             while npcFemale.age - offspringNPC.age < 12:
#                 if offspringNPC.age - 1 >= 0:
#                     offspringNPC.age -= 1
#                 npcMale.age += 1
#                 npcFemale.age += 1
#             while npcFemale.age - offspringNPC.age > 40:
#                 offspringNPC.age +=  1
#                 if npcFemale.age - 1 >= 0:
#                     npcFemale.age -=  1
#                 if npcMale.age - 1 >= 0:
#                     npcMale.age -=  1
#
#             npcMale.children.append(offspringNPC)
#             npcFemale.children.append(offspringNPC)
#             offspringNPC.mother = npcFemale
#             offspringNPC.father = npcMale
#             for sibling in npcMale.children:
#                 if sibling != offspringNPC:
#                     offspringNPC.siblings.append(sibling)
#                     sibling.siblings.append(offspringNPC)
#
#             createdOffspingList.append(offspringNPC)
#         else:
#             break
#
#     return createdOffspingList

# def addLoveInterest(npc, aliveNPCDict, loveInterestProb = conf.loveInterestProb,
#                     illegitimateLIProb = conf.illegitimateLoveInterestProb):
#     # Does the npc have a love interest?
#     # print("Does " + npc.firstName + " " + npc.lastName + " have a love interest?")
#     if hf.roll(loveInterestProb):
#         # If npc is NOT married then he surely has a love interest by now, first part becomes true and we go into the if
#         # OR if the npc IS married the first part becomes false so we have to roll on illegitimateLIProbability to add
#         # an illegitimate love interest. If roll fails, then we have (false or false) and add the spouse as the npc's LI
#         if not npc.isMarried or hf.roll(illegitimateLIProb):
#             # print("NPC is not married or has an illegitimate love interest.")
#             # Look for another npc that is appropriate
#             for anotherNPCName, anotherNPC in aliveNPCDict.items():
#                 # If the other npc is of the same age group and is not self or spouse
#                 if anotherNPC.ageGroup == npc.ageGroup and anotherNPC != npc.spouse and anotherNPC != npc:
#
#                     # If NPC is homosexual and the other npc is of same gender
#                     if npc.isHomosexual and anotherNPC.gender == npc.gender:
#                         # Add the other npc as love interest
#                         # print("NPC has a love interest in " + anotherNPC.firstName + " " + anotherNPC.lastName)
#                         npc.loveInterest = anotherNPC
#                         # If the other npc IS homosexual, then there is a chance that this is a mutual LI
#                         if anotherNPC.isHomosexual and hf.roll(conf.mutualLoveInterestProb):
#                             # print("Love interest with " + anotherNPC.firstName + " " + anotherNPC.lastName +
#                             #       " is mutual!")
#                             # The other npc is homosexual and the LI is mutual
#                             # Add the npc as a LI for the other npc
#                             anotherNPC.loveInterest = npc
#                             # There is a chance that the mutual LI situation ends up in a relationship, awww <3
#                             if hf.roll(conf.mutualLoveInterestHaveRelationshipProb):
#                                 # print("The mutual love interest with " + anotherNPC.firstName + " " +
#                                 #       anotherNPC.lastName + " is a relationship!")
#                                 npc.relationshipPartner = anotherNPC
#                                 anotherNPC.relationshipPartner = npc
#
#                         return True # Added a love interest
#
#                     # NPC is not homosexual and the other npc is of a different gender
#                     elif not npc.isHomosexual and anotherNPC.gender != npc.gender:
#                         # Add the other npc as love interest
#                         npc.loveInterest = anotherNPC
#                         # print("NPC has a love interest in " + anotherNPC.firstName + " " + anotherNPC.lastName)
#                         # If the other npc also not homosexual, then there is a chance that this is a mutual LI
#                         if not anotherNPC.isHomosexual and hf.roll(conf.mutualLoveInterestProb):
#                             # print("Love interest with " + anotherNPC.firstName + " " + anotherNPC.lastName +
#                             #       " is mutual!")
#                             # The other npc is homosexual and the LI is mutual
#                             # Add the npc as a LI for the other npc
#                             anotherNPC.loveInterest = npc
#                             # There is a chance that the mutual LI situation ends up in a relationship, awww <3
#                             if hf.roll(conf.mutualLoveInterestHaveRelationshipProb):
#                                 # print("The mutual love interest with " + anotherNPC.firstName + " " +
#                                 #       anotherNPC.lastName + " is a relationship!")
#                                 npc.relationshipPartner = anotherNPC
#                                 anotherNPC.relationshipPartner = npc
#
#                         return True # Added a love interest
#         # Npc is married, has a love interest and it isn't illegitimate, they are devoted to their spouse <3
#         else:
#             # print("NPC has a love interest in his spouse " + npc.spouse.firstName + " " + npc.spouse.lastName)
#             npc.loveInterest = npc.spouse
#             npc.relationshipPartner = npc.spouse
#     else:
#         # print("No npc does not have a love interest.")
#         # Easter egg, 0.2%(out of 100%) chance for npc to be in love with themselves
#         if hf.roll(0.01):
#             # print("NPC is in love with themselves")
#             npc.loveInterest = npc
#             npc.relationshipPartner = npc
#             return True
#         # No love interest
#         # Love interest stays None (as initialized) or is affected by some other npc with the above procedure
#         return False