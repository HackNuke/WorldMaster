import random
import numpy as np

def roll(chance=0.5):
    if random.random() < chance:
        return True
    else:
        return False

def rollList(list=[True, False], probList=[]):
    if len(probList) == 0:
        probList = [1.0 for i in range(len(list))]
        probList = normalizeToSum(probList)
    return random.choices(list, weights=probList)[0]


def normalizeToSum(array):
    # Helper method
    # Normalize an array by dividing each element by the array's sum,
    # after normalization sum(array) == 1.
    sum = np.sum(array)
    for i in range(len(array)):
        if sum != 0.0:
            array[i] = array[i] / sum
        else:
            print("Normalization of array failed. sum(array) == 0.0")
            return None
    return array