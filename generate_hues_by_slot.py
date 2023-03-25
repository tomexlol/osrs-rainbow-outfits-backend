from PIL import Image
import numpy as np
import glob
import json


#todo:
#[x]refactorear segun el comment en line 51
#[]Flaskearlo! hacer el html de la view "generar" (un slider/color picker/whatever y un boton de generate
    #el boton llama a generate_set con los parametros que saque del form o loquesea
    #al final el unico python que tiene que correr en tu server es esto - lo demás lo corrés client side y lo usás para popular la data nomás
        #sera que podés portear generate_set a javascript y correrlo en gh pages????? RE SI EH
#[]hacer el html de la view "resultados" (el set ordenado con sus respectivos íconos)
	##html: visualizer of the items (grabbeador de los icons+item names off the db maybe)
        #sólo dumpear una lista de id:name en el server y referenciarla - mismo para los iconos, dumpear una carpeta y referenciarla
	#export to Fashionscape plugin para exportar un .txt formateado para el Fashionscape
	#reroll button para rollear 1 slot sólo
        #hacelo todo en js, es lo mismo que generate set pero un solo slot. en vez de tomar two_hands toma el slot y lesto
        
#[]mas granularidad (separar de a 10-15 en vez de de a 30) - hace falta? chequearlo con ejemplos con el visualizer, es trivial hacerlo mas tarde



#checks if a pixel is black, white, gray, transparent, or color according to hsv values
#returns transparent gray white black color (str)
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


#for every slot's subfolder of icons, checks the average hue of every item and generates a json with item ids by hue ranges for each slot
#output["weapon"]["under_{30-360}"]
def generate_hues_by_slot(visible):
    slots = ["2h", "ammo", "body", "cape", "feet", "hands", "head", "legs", "neck", "ring", "shield", "weapon"]
    visible_slots = ["2h", "body", "cape", "feet", "hands", "head", "legs", "neck", "shield", "weapon"]
    hues_by_slot = {}
    for slot in (visible_slots if visible else slots):
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

            #agrega id: average_hue a ids_and_hues
            itemid = i.split(".")[0].split("/")[1]
            ids_and_hues[f"{itemid}"] = average_hue

        #esto es debugging - para tener la data en un .txt
        with open('ids_and_hues.txt', 'a') as L:
            L.write(json.dumps(ids_and_hues))
    #itera through tu ids_and_hues que venis generando arriba con el analisis de cada icono
        #sub: itera through los hue_ranges definidos arriba y sus values
        #mete cada id, hue en su respectivo [slot][hue_range] o en [slot][black|white|gray]

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


    #fuera de los loops: escribe la data de hues_by_slot a un output.json
    json_data = json.dumps(hues_by_slot)
    with open('output.json', 'a') as f:
        f.write(json_data)



generate_hues_by_slot(True)
