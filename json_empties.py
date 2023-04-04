import json

# Load JSON data from file
with open('output.json') as f:
    data = json.load(f)

empty_keys = []

def loop_subkeys(data, parent_key = None):
    if isinstance(data, dict):
        # If the data is a dictionary, loop through its keys
        for key, value in data.items():
            print(f"soy la key: {key}")
            print(f"soy el value: {value}")
            if not value:
                print(f"I am {key} of {parent_key} and i am empty D:")
                empty_keys.append((parent_key, key))
            if isinstance(value, dict):
                print("If the value of the key is a dictionary, recurse into it")
                loop_subkeys(value, parent_key = key)
            elif isinstance(value, list):
                print("If the value of the key is a list, loop through its items")
                for item in value:
                    if item:
                        print(f"i am {item} :D")
                        print(f"and my parent is {parent_key} :D")
                    if isinstance(item, dict):
                        print("If an item in the list is a dictionary, recurse into it")
                        loop_subkeys(item, parent_key = key)
            else:
                # If the value is not a dictionary or list, it is a subkey
                print(f"Subkey: {key}, Value: {value}")
    elif isinstance(data, list):
        # If the data is a list, loop through its items
        for item in data:
            if isinstance(item, dict):
                print("If an item in the list is a dictionary, recurse into it")
                loop_subkeys(item, parent_key = None)
    print("these are the empties:")
    print(empty_keys)

print("i am looping subkeys")
loop_subkeys(data)
