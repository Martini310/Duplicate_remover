import os
from PIL import Image, ImageChops
import itertools
import shutil

given_path = input("Podaj ścieżkę do folderu, który chcesz przeskanować:\n")

# List with paths, sizes and names of found images.
photos = []
for root, dirs, files in os.walk(given_path, topdown=True):
    for name in files:
        if name.lower().endswith(".jpg") or name.lower().endswith(".png"):
            photos.append([os.path.join(root, name), os.path.getsize(os.path.join(root, name)), name])

# Create a dir for duplicated images.
if not os.path.exists(r".\duplicates"):
    os.mkdir(r".\duplicates")

# List with duplicates.
duplicates = []
for e in itertools.combinations(photos, 2):
    if e[0][1] == e[1][1]:
        duplicates.append([e[0], e[1]])

nr = 1  # An increasing amount of copy if name exists.
count = 0  # Amount of moved files.
for dup in duplicates:
    if os.path.exists(dup[0][0]) and os.path.exists(dup[1][0]):
        img1 = Image.open(dup[0][0])
        img2 = Image.open(dup[1][0])
        if not ImageChops.difference(img1, img2).getbbox():  # Compare images
            if not os.path.exists(r"duplicates\\" + dup[0][2]):
                shutil.move(dup[0][0], r"duplicates\\" + dup[0][2])
            else:
                os.rename(dup[0][0], fr".\duplicates\\{dup[0][2][:-4]}({str(nr)}){dup[0][2][-4:]}")
                nr += 1
            photos.pop(0)
            with open("duplikaty.txt", encoding="utf-8", mode="a") as spis:
                spis.write(f"Przeniesiono {dup[0][2]}, pozostawiono {dup[1][2]}\n")
            spis.close()
            count += 1

# Delete folder if empty and add info.
if not os.listdir(r".\duplicates"):
    with open("duplikaty.txt", encoding="utf-8", mode="a") as spis:
        spis.write(f"Brak zduplikowanych obrazów w podanym folderze.")
    spis.close()
    os.rmdir(r".\duplicates")
    os.startfile(r".\duplikaty.txt")
else:
    os.startfile(r".\duplicates")
    os.startfile(r".\duplikaty.txt")
