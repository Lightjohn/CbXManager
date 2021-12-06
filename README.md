# CbXManager
Easily create/extract cbz or cbr files with a python script, can split and adapt to manga read order

# Notes

There are two tools here:
* [cbxManager](#cbxmanager-purpose)
* [regroupImages](#regroupimages-purpose)

`image_slicer` is pinning **pillow** in last pypi release so I advise to install deps with: `pip install --no-deps -r requirements.txt`

# CbXManager Purpose
I need to manage book or images and sometimes I need to deal with the folder and another with the cbz file.
CbXManager can guess the input and:

  If the input is a folder -> it will create a cbz
  If the input is a cbz it will extract it
  
I added some options: like splitting the wide images in two and reverse the read order to adapt to manga.

## Example

```
myFolder/image1.jpg
         image2.jpg
         image3.jpg
         image4.jpg
```

When running the foolowing command:

`
python cbxmanager.py myfolder/
`

We will have:

```
myFolder/image1.jpg
         image2.jpg
         image3.jpg
         image4.jpg
myFolder.cbz
```

And inside myFolder.cbz are all the images.

And if I run:

`
python cbxmanager.py myfolder.cbz
`

It will extract the cbz to the original folder.

## Options
* `-c` option to cut the image in two parts
* `-r` reverse the lecture order
* `-v` verbose mode activated

# regroupImages Purpose

`regroupImages` will parse a folder and it's direct subfolders to create volumes of around 170 images (by default).

It will first finish the current folder before finishing the Volume:

Example:
```
myFolder/chapter01/image1.jpg
                   ...
                   image100.jpg
myFolder/chapter02/image1.jpg
                   ...
                   image100.jpg
myFolder/chapter03/image1.jpg
                   ...
                   image100.jpg
```

Command:

`python3 regroupImages.py --delete /path/to/myFolder/`

Will result in:

```
Vol 01.cbz (200 images inside: chapter 01 & 02)
Vol 02.cbz (100 images inside: chapter 03
```

## Options
* `--delete` delete the folders/images as they are put in the `.cbz`
* `--limit` change the 170 that is an empirical value that is working well for me.

## Notes

It can only generate cbz and does not do the complicated things that `cbxManger` do.
