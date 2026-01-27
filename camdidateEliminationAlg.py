import numpy as np
import pandas as pd

# Load data
data = pd.read_csv("enjoySports.csv")

# Separate features and target
concepts = np.array(data.iloc[:, 0:-1])
target = np.array(data.iloc[:, -1])

# Match the output format of the image
print("Instances are:\n", concepts)
print("Target Values are: ", target)

def learn(concepts, target):
    specific_h = concepts[0].copy()
    
    print("\nInitialization of specific_h and general_h")
    print("Specific Boundary: ", specific_h)
    
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    print("Generic Boundary: ", general_h)

    for i, h in enumerate(concepts):
        # Logic for Positive Instance
        if target[i] == "yes":
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x][x] = '?'

        # Logic for Negative Instance
        if target[i] == "no":
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                else:
                    general_h[x][x] = '?'
        
        # INTERMEDIATE PRINTS REMOVED TO MATCH SCREENSHOT

    # Cleanup empty hypotheses in General Boundary
    indices = [i for i, val in enumerate(general_h) if val == ['?'] * len(specific_h)]
    for i in indices:
        general_h.remove(['?'] * len(specific_h))
        
    return specific_h, general_h

s_final, g_final = learn(concepts, target)

print("\nFinal Specific_h:", s_final, sep="\n")
print("Final General_h:", g_final, sep="\n")