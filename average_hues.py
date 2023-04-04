from PIL import Image
import numpy as np
import glob
import json

#for every slot's subfolder, checks the average hue of every item and generates a json with items per slot by hue ranges
#output["weapon"]["under_{30-360}"]

#todo:
	#en grises hay outliers con mucho color. si va a ser gris checkear? a ver cuanto % de color hay similarly to blacks?
	#y si hay mucho % de color en vez de mandarlo a grays mandarlo a la categoria del color que seria si not grays
	#	infernal cape

def black_white_gray_or_color(pix):
	h = pix[0]
	s = pix[1]
	v = pix[2]
	if h == 0 and s == 0 and v == 0:
		return "transparent"
	if h <= 15 and s <= 30 and v <= 175:
		return "gray"
	elif h <= 15 and s <= 25 and v >= 175:
		return "white"
	elif h >= 15 and s >= 250 and v <= 5:
		return "black"
	else:
		return "color"

#black is: hue can exist (usually 240 for 001 in rgb), very high saturation (100%), incredible low value (1 de 255)

#white is: hue 0-10, saturation under 10%, value over 80%



#de aca sale el json final
hues_by_slot = {}

slots = ["2h", "ammo", "body", "cape", "feet", "hands", "head", "legs", "neck", "ring", "shield", "weapon"]
visible_slots = ["2h", "body", "cape", "feet", "hands", "head", "legs", "neck", "shield", "weapon"]

#esto es para iterar los iconos. ahora esta usando visible slot pq ammo y ring dan igual


#Todo esto podria ser un metodo aparte que termine escribiendo ids_and_hues a un json y despues en tu main solo lo iteras (line 110 for item_id, hue...)
# asi quedarian 3 metodos diferentes: load_items itera los items de la DB y guarda sus iconos en subcarpetas por slot
# ids_and_hues te guardaría un json con item ids y sus respectivas hues para cada slot onda 2h_hues.json body_hues.json
# de ahi es mucho mas facil combinarlos en 1 si hace falta

for slot in visible_slots:
	ids_and_hues = {}
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
	"under_360": [],
	"gray": [],
	"white": [],
	"black": []
	}
	for i in glob.glob(f"{slot}/*.png"):
		img = Image.open(i)
		img_hsv = img.convert("HSV")
		hue_results = []
		gray_pixels = 0
		black_pixels = 0
		white_pixels = 0
		transparent_pixels = 0
		for x in range(36):
			for y in range(32):
				pixel = img_hsv.getpixel((x, y))
				if pixel[2] > 90 and pixel[0] and black_white_gray_or_color(pixel) == "color":
					hue_results.append(pixel[0])
				elif black_white_gray_or_color(pixel) == "gray":
					gray_pixels += 1
				elif black_white_gray_or_color(pixel) == "white":
					white_pixels += 1
				elif black_white_gray_or_color(pixel) == "black":
					black_pixels += 1
				elif black_white_gray_or_color(pixel) == "transparent":
					transparent_pixels += 1
		if black_pixels > (gray_pixels + white_pixels + len(hue_results)):
			average_hue = "black"
		elif len(hue_results) > max([(gray_pixels, "gray"), (white_pixels, "white")])[0]:
			average_hue = np.mean(hue_results)
		else:
			average_hue = max([(gray_pixels, "gray"), (white_pixels, "white")])[1]

		itemid = i.split(".")[0].split("/")[1]

		
		ids_and_hues[f"{itemid}"] = average_hue

	#esto es debugging - para tener la data en un .txt
	with open('ids_and_hues.txt', 'a') as L:
		L.write(json.dumps(ids_and_hues))


#itera through tu ids_and_hues que venis generando arriba con el analisis de cada icono
	#sub: itera through los hue_ranges definidos arriba y sus values
	#mete cada id, hue en su respectivo [slot][hue_range]

	for item_id, hue in ids_and_hues.items():
		for range_name, item_list in hue_ranges.items():
			if range_name == hue:
				item_list.append(item_id)
				break
			if hue == "gray" or hue == "black" or hue == "white":
				continue
			if range_name.split("_")[0] == "under":
				range_start = int(range_name.split("_")[1])
				range_end = range_start + 30
				if range_start <= int(hue) <= range_end:
					item_list.append(item_id)
					break

	hues_by_slot[slot] = hue_ranges



json_data = json.dumps(hues_by_slot)
with open('output.json', 'a') as f:
    f.write(json_data)