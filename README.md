# CbXManager
Easily create/extract cbz or cbr files with a python script, can split and adapt to manga read order

# Purpose
I need to manage book or images and sometimes I need to deal with the folder and another with the cbz file.
CbXManager can guess the input and:

  If the input is a folder -> it will create a cbz
  If the input is a cbz it will extract it
  
I added some options: like splitting the wide images in two and reverse the read order to adapt to manga.

# Example

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

# Options
* -c option to cut the image in two parts
* -r reverse the lecture order
* -v verbose mode activated
