import json
import random

with open('output.json', 'r') as f:
    data = json.load(f)

visible_slots_2h = ["2h", "body", "cape", "feet", "hands", "head", "legs", "neck",]
visible_slots_1h = ["body", "cape", "feet", "hands", "head", "legs", "neck", "shield", "weapon"]


def generateSet(hue_range, two_hands):
        gear_set = {}
        print(two_hands)
        if int(two_hands) == 1:
            for slot in visible_slots_2h:
                gear_set[slot] = random.choice(data[slot][f"under_{hue_range}"])
        if int(two_hands) == 0:
            for slot in visible_slots_1h:
                gear_set[slot] = random.choice(data[slot][f"under_{hue_range}"])
        print(gear_set)


number = input("pone el numero")
twohanding = input("two hand? 1/0")



generateSet(number, twohanding)   