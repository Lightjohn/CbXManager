#!/usr/bin/python3
# coding=utf-8
import argparse
import os
import shutil
from PIL import Image  # python-imaging
from zipfile import ZipFile

images = ["png", "jpg", "jpeg"]
suffix_sliced = "_sliced"


class CbxManager:
    def __init__(self):
        self.verbose = False
        self.cut = False
        self.reverse = False
        self.sep = os.sep

    def parse_dir(self, input_path):
        """
        This function should be called with path to folder as argument. It will
        extract images from the folder with NO recursivity and will add the images
        inside a cbz archive that will be named:
            :param input_path: path/to/folder
        """
        # if the input is a folder we will try to cbz it
        path_deconstruct = [
            x for x in input_path.split(self.sep) if x != ""
        ]  # Note: sep
        folder = path_deconstruct[-1]
        if self.verbose:
            print("Parsing folder: " + folder)
        # opening cbz and parsing folder to find images
        path_deconstruct[-1] += ".cbz"
        out_cbz = os.path.join(*path_deconstruct)  # Note: list to args=*
        # If the path was from the root
        if input_path[0] == self.sep:
            out_cbz = self.sep + out_cbz
        # Adding all images in the output cbz
        with ZipFile(out_cbz, "w") as myzip:
            for files in sorted(os.listdir(input_path)):
                ext = files[-3:].lower()
                if ext in images:
                    file_to_add = os.path.join(input_path, files)
                    if self.verbose:  # Note: If verbose
                        print("        Adding " + file_to_add)
                    myzip.write(file_to_add, arcname=files)
            if self.verbose:
                print("    CBZ created: " + out_cbz)

    def parse_cbz(self, input_path):
        """
        This function should be called with path to cbz as argument. It will
        extract images from the cbz and will write them in a folder near the cbz
            :param input_path: path/to/file.cbz
            output = path/to/file

        """
        path_deconstruct = [
            x for x in input_path.split(self.sep) if x != ""
        ]  # Note: os.sep
        cbr_file = path_deconstruct[-1]
        path_out = input_path.replace(".cbz", "")
        if self.verbose:
            print("Parsing cbr files: " + cbr_file)
        with ZipFile(input_path, "r") as myzip:
            files_to_extract = myzip.namelist()
            try:
                os.mkdir(path_out)
            except OSError:
                pass
            for tmp_file in files_to_extract:
                name = tmp_file.split(self.sep)[-1]
                if self.verbose:
                    print("        Extracting " + path_out + self.sep + name)
                with open(path_out + self.sep + name, "wb") as tmp_img:
                    tmp_img.write(myzip.read(tmp_file))
            if self.verbose:
                print("    CBZ extracted to " + path_out)

    def image_slice(self, image_path):
        original = Image.open(image_path)
        width, height = original.size
        wid = int(width / 2)
        return original.crop((0, 0, wid, height)), original.crop(
            (wid, 0, width, height)
        )

    def slice_folder(self, input_path):
        """
        This function should be called with a path to a folder as argument. It will
        extract images from the folder with NO recursivity and will slice them if the
        weight is > to the height.
            :param input_path: path/to/folder/bigImage.jpg
            output = path/to/folder_sliced/bigImage-0_01_01.jpg
                     path/to/folder_sliced/bigImage-0_01_02.jpg

        """
        print("Parsing folder: " + input_path)
        if input_path[-1] == self.sep:
            path_out = input_path[:-1] + suffix_sliced
        else:
            path_out = input_path + suffix_sliced
        try:
            os.mkdir(path_out)
        except OSError:
            pass
        for files in sorted(os.listdir(input_path)):
            ext = files[-3:].lower()
            if ext in images:
                file_to_add = os.path.join(input_path, files)
                im = Image.open(file_to_add)
                (w, h) = im.size
                if w > h:
                    if self.verbose:  # Note: If verbose
                        print("        Slicing ", file_to_add, str(w) + "x" + str(h))
                    img_a, img_b = self.image_slice(file_to_add)
                    if (
                        self.reverse
                    ):  # If it's a manga, then the first page is the right page
                        img_a, img_b = img_b, img_a
                    for c, im in enumerate([img_a, img_b]):
                        im.save(f"{path_out}{self.sep}{files[:-4]}_{c}.jpg")
                else:
                    shutil.copy(file_to_add, path_out)
        return path_out

    def launch(self, path_to_data, verbose=True, cut=False, reverse=False):
        """
        Front function that receive the arguments and choose what to do:
        Path -> Convert to cbz
        CbX -> Try to open it
        :param reverse: To switch from manga to comic or comic to manga
        :param cut: Split the images in two
        :param verbose: You talk to me ?
        :param path_to_data: The folder or cbz file
        """
        self.verbose = verbose
        self.cut = cut
        self.reverse = reverse
        # We need a list to be able to iter on
        if not isinstance(path_to_data, list):
            path_to_data = [path_to_data]
        for i in path_to_data:
            if i[-4:] == ".cbz":
                self.parse_cbz(i)
            elif os.path.isdir(i):
                if cut:
                    path_tmp = self.slice_folder(i)
                    self.parse_dir(path_tmp)
                    shutil.rmtree(path_tmp)
                else:
                    self.parse_dir(i)
            else:
                print("Do not know what it is: " + i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process folders to cbX, cbX to folders and maybe more\n \
        if the input is a folder, we will compress it to a cbz\n \
        if the input is a cbX we will do according to the options\n \
            no option: extract the cbz to a folder\n\
            -c extract and split the images\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("pathToData", nargs="+", help="Path to the folder or cbX")
    parser.add_argument(
        "-c",
        action="store_true",
        help="will try to extract the images from cbX and cut the image in 2",
    )
    parser.add_argument(
        "-r",
        action="store_true",
        help="If splitting is activated then we will reverse the order if the pages (for manga)",
    )
    parser.add_argument("-v", action="store_true", help="verbose")
    args = parser.parse_args()

    cbx = CbxManager()
    cbx.launch(args.pathToData, verbose=args.v, cut=args.c, reverse=args.r)
