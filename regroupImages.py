import argparse
import os
from os import walk
from os.path import join
from shutil import copyfile
from zipfile import ZipFile

images_type = ["jpg", "jpeg", "png", "webp"]

HARD_LIMIT = 170
USE_CBZ = True


def regroup_all_images(folder):
    out_folder = folder
    count_images = 0
    count_folder = 1
    volume = "Vol 01"
    os.makedirs(out_folder, exist_ok=True)
    os.makedirs(join(out_folder, volume))
    current_dir = ""
    for (root, dirs, files) in walk(folder):
        for i in files:
            ext_file = i.split(".")[-1].lower()
            if ext_file in images_type:
                print("FOUND:", root, i)
                if count_images == HARD_LIMIT:
                    current_dir = root
                if count_images > HARD_LIMIT and current_dir != root:
                    current_dir = root
                    count_folder += 1
                    count_images = 0
                    volume = "Vol " + str(count_folder).zfill(2)
                    os.makedirs(join(out_folder, volume), exist_ok=True)

                input_path = join(root, i)
                output_path = join(out_folder, volume, str(count_images).zfill(3) + "." + ext_file)
                copyfile(input_path, output_path)
                count_images += 1


def regroup_all_images_cbz(folder, delete=False):
    out_folder = folder
    count_images = 0
    count_folder = 1
    volume = "Vol 01.cbz"
    os.makedirs(out_folder, exist_ok=True)
    current_dir = ""
    cbz_file = None
    for (root, dirs, files) in walk(folder):
        dirs.sort()
        files.sort()
        if root == folder:
            continue
        for i in files:
            ext_file = i.split(".")[-1].lower()
            if ext_file in images_type:
                print("FOUND:", root, i)
                if count_images == HARD_LIMIT:
                    current_dir = root
                if count_images > HARD_LIMIT and current_dir != root:
                    current_dir = root
                    count_folder += 1
                    count_images = 0
                    cbz_file.close()
                    volume = "Vol " + str(count_folder).zfill(2) + ".cbz"
                    cbz_file = ZipFile(join(out_folder, volume), 'w')

                input_path = join(root, i)
                output_path = str(count_images).zfill(3) + "." + ext_file
                if not cbz_file:
                    # Lazy initialisation for empty folders
                    cbz_file = ZipFile(join(out_folder, volume), 'w')
                cbz_file.write(input_path, output_path)
                if delete:
                    os.remove(input_path)
                count_images += 1
        if delete:
            print("DELETE", root)
            os.removedirs(root)
    if cbz_file:
        cbz_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename all files inside a folder.')
    parser.add_argument("path", help="folder to rename", nargs='+')
    parser.add_argument("--delete", help="move and not copy", action="store_true")
    parser.add_argument("--limit", help="number of images per tome", default=170)
    args = parser.parse_args()
    HARD_LIMIT = args.limit
    for path in args.path:
        regroup_all_images_cbz(path, args.delete)
