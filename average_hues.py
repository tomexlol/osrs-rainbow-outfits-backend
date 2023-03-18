#import base64
from PIL import Image
from io import BytesIO
import numpy as np
import glob
import json

#for every slot's subfolder, checks the average hue of every item and generates a json with items per slot by hue ranges
#output["weapon"]["under_{30-360}"]



hues_by_slot = {}
ids_and_hues = {}
slots = ["2h", "ammo", "body", "cape", "feet", "hands", "head", "legs", "neck", "ring", "shield", "weapon"]

for slot in slots:
	for i in glob.glob(f"{slot}/*.png"):
		img = Image.open(i)
		img_hsv = img.convert("HSV")
		hue_results = []
		for x in range(36):
			for y in range(32):
				pixel = img_hsv.getpixel((x, y))		
				if pixel[2] > 90 and pixel[0]:
					hue_results.append(pixel[0])
		average_hue = np.mean(hue_results)

		itemid = i.split(".")[0].split("/")[1]

		ids_and_hues[f"{itemid}"] = average_hue

	hue_ranges = {
	"under_30": [],
	"under_60": [],
	"under_90": [],
	"under_120": [],
	"under_150": [],
	"under_180": [],
	"under_210": [],
	"under_240": [],
	"under_270": [],
	"under_300": [],
	"under_330": [],
	"under_360": []
	}



	for item_id, hue in ids_and_hues.items():
		for range_name, item_list in hue_ranges.items():
			range_start = int(range_name.split("_")[1])
			range_end = range_start + 30
			if range_start <= hue <= range_end:
				item_list.append(item_id)
				break
	hues_by_slot[slot] = hue_ranges
	
	


json_data = json.dumps(hues_by_slot)
with open('output.json', 'w') as f:
    f.write(json_data)






