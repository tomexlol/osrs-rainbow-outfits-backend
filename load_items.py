from osrsbox import items_api
import base64
from PIL import Image
from io import BytesIO
import os

#loads item data from osrsbox & saves equippable items' icons in subfolders by slot

items = items_api.load()


for item in items:	
	if item.equipable_by_player == True:
		if not os.path.exists(f"{item.equipment.slot}"):
			os.makedirs(f"{item.equipment.slot}")
		icon_binary = base64.b64decode(item.icon)
		img = Image.open(BytesIO(icon_binary))
		img.save(f"{item.equipment.slot}/{item.id}.png")
		
		
		
		





