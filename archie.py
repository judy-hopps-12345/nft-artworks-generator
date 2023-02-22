from PIL import Image, ImageOps
import random
import json
from dotenv import load_dotenv
from enum import Enum
import os
import sys

try:
    from_num = int(sys.argv[1])
    to_num = int(sys.argv[2])
except:
    exit('Arguments incorrect')

load_dotenv()

metadataRoot = os.environ['METADATA_PATH']
f = open(metadataRoot, 'r')
rawMeta = f.read()
f.close()
meta = json.loads(rawMeta)
attributes = {}
for nft in meta:
    for attribute in nft['attributes']:
        trait_type = attribute['trait_type']
        trait_value = attribute['value']
        if trait_type in attributes and trait_value not in attributes[trait_type]:
            attributes[trait_type].append(trait_value)
        else:
            attributes[trait_type] = [trait_value]

#### IMAGE GENERATION

def attributeValue(meta, type):
    for attribute in meta['attributes']:
        if attribute['trait_type'] == type:
            return attribute['value']

ASSET_ROOT = os.environ['ASSET_ROOT']
IMAGE_OUTPUT = os.environ['IMAGE_OUTPUT']
width = 3000
for item in meta[from_num:to_num]:
    background = Image.open(f"{ASSET_ROOT}Background/{attributeValue(item, 'Background')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    skin = Image.open(f"{ASSET_ROOT}skin/{attributeValue(item, 'skin')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    footwear = Image.open(f"{ASSET_ROOT}footwear/{attributeValue(item, 'footwear')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    clothes = Image.open(f"{ASSET_ROOT}clothes/{attributeValue(item, 'clothes')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    neck = Image.open(f"{ASSET_ROOT}neck/{attributeValue(item, 'neck')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    eye = Image.open(f"{ASSET_ROOT}eye/{attributeValue(item, 'eye')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    mouth = Image.open(f"{ASSET_ROOT}mouth/{attributeValue(item, 'mouth')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    facewear = Image.open(f"{ASSET_ROOT}facewear/{attributeValue(item, 'facewear')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    accessories = Image.open(f"{ASSET_ROOT}accessories/{attributeValue(item, 'accessories')}.png").resize((width, width), Image.NEAREST).convert('RGBA')
    headwear = Image.open(f"{ASSET_ROOT}headwear/{attributeValue(item, 'headwear')}.png").resize((width, width), Image.NEAREST).convert('RGBA')

    #Create each composite
    com1 = Image.alpha_composite(background, skin)
    com2 = Image.alpha_composite(com1, footwear)
    com3 = Image.alpha_composite(com2, clothes)
    com4 = Image.alpha_composite(com3, neck)
    com5 = Image.alpha_composite(com4, eye)
    com6 = Image.alpha_composite(com5, mouth)
    com7 = Image.alpha_composite(com6, facewear)
    com8 = Image.alpha_composite(com7, accessories)
    com9 = Image.alpha_composite(com8, headwear)

    #Convert to RGB
    rgb_im = com9.convert('RGB')
#     display(rgb_im.resize((400,400), Image.NEAREST))

    file_name = str(item["edition"]) + ".jpg"
    rgb_im.save(f"{IMAGE_OUTPUT}{file_name}")
    print(f'generated {file_name}')
    
