########################################################################################################################
########################################################################################################################
# Offspring
maxOffspring = 10 # Max offspring per family
offspringProb = 0.75 # Probability for a family to have at least one offspring
multipOffspringProb = [0.1, 0.3, 1, 0.01, 0] # Love interest probability multipliers for each ageGroup

########################################################################################################################
# Love interests
loveInterestProb = 0.1 # Base probability for an NPC to get a love interest
multipLIProb = [0, 2, 4, 1, 0.5] # Love interest probability multipliers for each ageGroup

loveInterestIsSpouseProb = 0.8

wantsRelationshipProb = 0.5 # Base probability for an NPC to want to have a relationship with loveInterest
multipWantsLIProb = [0, 8, 6, 3, 2] # Probability multipliers for each ageGroup to want to have a relationship

#  Marriage
getMarriedProb = 0.25 # Base probability for an npc to get married
multipGetMarriedProb = [0, 0.01, 1, 0.5, 0.1] # Probability multipliers for each ageGroup to get married
multipWidowGetMarriedProb = [0, 1, 0.2, 0.1, 0.01] # Probability multipliers for each ageGroup to get married after
                                                   # spouse died
########################################################################################################################
# Professions
# Retire
retireProb = 0.1 # Base probability for an npc to retire from their job
multipRetireProb = [0, 0.01, 0.5, 1, 5] # Probability multipliers for each ageGroup to retire from job
# Find job
findJobProb = 0.1 # Base probability for an npc to find a job if they don't already have and are not retired
multipFindJobProb = [0, 2, 5, 3, 1]

########################################################################################################################
# Death
yearlyDeathProb = 0.015 # Base probability that an NPC dies each year
multipYearlyDeathProb = [3, 2, 1, 3, 10] # Death probability multipliers for each ageGroup

########################################################################################################################
ageGroups = ["child", "youth", "youngAdult", "adult", "senior"]
# Age group limits:
# - first number is the upper limit of child
# - second number is upper limit of youth
# - third number is upper limit of youngAdult
# - fourth number is upper limit of adult, after this we have a senior
ageGroupLimits = {
    "human": [10, 18, 35, 65],
    "dwarf": [18, 50, 125, 200],
    "elf": [18, 100, 450, 650],
    "dragonborn": [10, 20, 30, 50],
    "gnome": [6, 20, 40, 200],
    "half-elf": [6, 20, 50, 150],
    "half-orc": [10, 14, 45, 60],
    "tiefling": [6, 18, 40, 70],
    "halfling": [6, 20, 40, 150]
}

########################################################################################################################
# Services
# Support Value (SV): To find the number of, say, inns in a city, divide the population of the city by the SV value for
# inns (2,000). For a village of 400 people, this reveals only 20% of an inn! This means that there is a 20% chance of
# there being one at all. And even if there is one, it will be smaller and less impressive than an urban inn. The SV
# for taverns is 400, so there will be a single tavern.
SVDict = {"Government": 1000, "Shoemakers": 150, "Tailors": 250, "Barbers": 350, "Jewelers": 400, "Tavern": 400,
          "Old Clothes": 400, "Masons": 500, "Carpenters": 550, "Weavers": 600, "Coopers": 700, "Bakers": 800,
          "Winesellers": 900, "Hatmakers": 950, "Saddlers": 1000, "Pursemakers": 1100, "Woodsellers": 2400,
          "Magic Shop": 2800, "Bookbinders": 3000, "Butchers": 1200, "Fishmongers": 1200, "Beersellers": 1400,
          "Bucklemakers": 1400, "Spiceseller": 1400, "Blacksmiths": 1500, "Painters": 1500, "Doctors": 1700,
          "Roofers": 1800, "Locksmiths": 1900, "Ropemakers": 1900, "Inns": 2000, "Tanners": 2000, "Sculptors": 2000,
          "Rugmakers": 2000, "Booksellers": 6300}