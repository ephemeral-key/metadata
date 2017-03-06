#!/usr/bin/env python
# Purpose: EXIF & IPTC Metadata Analysis & Removal
# Author: Ryan Fetterman -- https://github.com/ephemeral-key
# =================================================================================
# metEraser is a python privacy tool build to view all EXIF and IPTC metadata for a
# designated image or directory images. metErase offers the option to strip all
# metadata from the associated images to allow posting online without disclosing
# personal information, such as geolocation.
# =================================================================================

import Image
import os
import time
import exifread

def print_welcome():
    print"##############################################################################"
    print"                                  __                                         "
    print"                       __  _ _|_ |_  __ _  _  _  __                          "
    print"                       |||(/_ |_ |__ | (_|_> (/_ |                           "
    print"                               version 1.0                                   "
    print""
    print"##############################################################################"

def main():
    img_file = raw_input("[*] Enter Image Path or drag file to analyze: ")
    directory, filename = os.path.split(img_file)

    if os.path.isfile(img_file):
        image = Image.open(img_file)
        print "[*] Checking attributes of '" + str(filename) + "'"
        print "----------------------------------------------------------------"
        print "[+] image format: " + str(image.format)
        print "[+] image size: " + str(image.size)
        print "[+] image mode: " + str(image.mode)
        print "----------------------------------------------------------------"
        print "[*] Checking associated metadata of '" + str(filename) + "'"
        print "----------------------------------------------------------------"
        time.sleep(2)
        img_file = open(str(img_file), 'rb')

        tags = exifread.process_file(img_file)

        for tag in sorted(tags.keys()):
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote', 'EXIF UserComment'):
                print "[+] %s: %s" % (tag, tags[tag])


        if tags.values()!=[]:
            print "----------------------------------------------------------------"
            decision = raw_input("[*] Would you like to erase all metadata? (y/n): ")
            try:
                if decision == 'y':
                    data = list(image.getdata())
                    clean_img = Image.new(image.mode, image.size)
                    clean_img.putdata(data)
                    clean_img.save(directory + 'meta_stripped_' + filename)
                    print "New image files have been created in '" + str(directory) + "' with no metadata."
                elif decision == 'n':
                    print ""
                    quit()
                else:
                    print "[!] 'y' or 'n' inputs only. "
                    quit()
            except:
                quit()
        else:
            print "no EXIF Metadata present."

    elif os.path.isdir(img_file):
        directory = img_file
        for file in os.listdir(directory):
            print "[*] Checking attributes of '" + file + "':"
            print "----------------------------------------------------------------"
            image = Image.open(directory + '\\' + file)
            print "[+] image format: " + str(image.format)
            print "[+] image size: " + str(image.size)
            print "[+] image mode: " + str(image.mode)
            print "----------------------------------------------------------------"
            print "[*] Checking associated metadata of '" + file + "':"
            print "----------------------------------------------------------------"

            opened = open(str(img_file+ '\\' + file), 'rb')

            tags = exifread.process_file(opened)

            for tag in sorted(tags.keys()):
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote', 'EXIF UserComment'):
                    print "[+] %s: %s" % (tag, tags[tag])

            if tags.values() != []:
                print "----------------------------------------------------------------"
                decision = raw_input("[*] Would you like to erase all metadata? (y/n): ")
                try:
                    if decision == 'y':
                        data = list(image.getdata())
                        clean_img = Image.new(image.mode, image.size)
                        clean_img.putdata(data)
                        clean_img.save(directory + 'meta_stripped_' + file)
                        print "New image files have been created in '" + str(directory) + "' with no metadata."
                        continue
                    elif decision == 'n':
                        print "no received"
                        print ""
                        continue
                    else:
                        print "[!] 'y' or 'n' inputs only. "
                        quit()
                except:
                    continue
            else:
                print "no EXIF Metadata present."
                continue

print_welcome()
main()

