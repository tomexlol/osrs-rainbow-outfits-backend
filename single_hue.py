from PIL import Image
import numpy as np
import glob
import json

#esto es para analizar 1 solo icono te pide el id se lo das te tira que pixeles son de cada categoria. nada mas. no tocar nada (?)

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




hues_by_slot = {}

slots = ["2h", "ammo", "body", "cape", "feet", "hands", "head", "legs", "neck", "ring", "shield", "weapon"]
visible_slots = ["2h", "body", "cape", "feet", "hands", "head", "legs", "neck", "shield", "weapon"]



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
imp = input("poner id:\n")
i = f"{imp}.png"
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
#itemid = i.split(".")[0].split("/")[1]
	
#ids_and_hues[f"{itemid}"] = average_hue
print(f"item {i}")
print(f"gray pixels: {gray_pixels}")
print(f"black pixels: {black_pixels}")
print(f"white pixels: {white_pixels}")
print(f"transparent pixels: {transparent_pixels}")
print(f"color pixels: {len(hue_results)}")
print(f"my avg hue is: {average_hue}")


#with open('jajajjjjjjjjjjj.txt', 'a') as L:
	#	L.write(json.dumps(ids_and_hues))


#	print(f"TERMINANDO DE ITERAR EL SLOT: {slot}")
	#print(f"LOS RANGOS SON: {hue_ranges}")
	#hues_by_slot[slot] = hue_ranges



json_data = json.dumps(hues_by_slot)
with open('output.json', 'a') as f:
    f.write(json_data)