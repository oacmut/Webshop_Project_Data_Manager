import pandas as pd
import os
import shutil
from PIL import Image


df = pd.read_excel('c:/Projektjeim/bvins.xlsx')


base_dir = 'c:/Projektjeim/termekek'
if not os.path.exists(base_dir):
    os.makedirs(base_dir)


source_dir = 'c:/Projektjeim/fressnapf_images'


for index, row in df.iterrows():

    folder_name = str(row[0]) 

    image_name = str(row[1])
    

    new_folder_path = os.path.join(base_dir, folder_name)
    

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    

    medium_path = os.path.join(new_folder_path, 'medium')
    small_path = os.path.join(new_folder_path, 'small')
    
    os.makedirs(medium_path, exist_ok=True)
    os.makedirs(small_path, exist_ok=True)
    

    source_image_path = os.path.join(source_dir, image_name)
    

    if os.path.exists(source_image_path):

        destination_image_path = os.path.join(new_folder_path, image_name)
        shutil.copy2(source_image_path, destination_image_path)
        

        with Image.open(destination_image_path) as img:

            img_small = img.copy()
            img_small.thumbnail((220, 220), Image.Resampling.LANCZOS)
            small_save_path = os.path.join(small_path, image_name)
            img_small.save(small_save_path)
            
            img_medium = img.copy()
            img_medium.thumbnail((248, 248), Image.Resampling.LANCZOS)
            medium_save_path = os.path.join(medium_path, image_name)
            img_medium.save(medium_save_path)
            
        print(f"Feldolgozva: {folder_name} - {image_name}")
    else:
        print(f"Nem található kép: {source_image_path}")

print("A program befejezte a feldolgozást!")