from osrsbox import items_api
import base64
from PIL import Image
from io import BytesIO
import os
import json

#loads item data from osrsbox & saves equippable items' icons in subfolders by slot

items = items_api.load()
ids_and_names = {}

for item in items:	
	if item.equipable_by_player == True:
		if not os.path.exists("icons"):
			os.makedirs("icons")
		icon_binary = base64.b64decode(item.icon)
		img = Image.open(BytesIO(icon_binary))
		img.save(f"icons/{item.id}.png")
		ids_and_names[item.id] = item.name

		
		
with open('ids_and_names.json', 'a') as L:
	L.write(json.dumps(ids_and_names))




