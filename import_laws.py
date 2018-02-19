# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
import urllib.request
import os
import zipfile
import codecs
import time


def extract_download_links():
    """take a xml File and extract the download links of legislative texts"""
    tree = etree.parse('gii-toc.xml')
    root = tree.getroot()
    linkList = []
    for child in root:
        for step_child in child:
            if step_child.tag == "link":
                linkList.append(step_child.text)
    return linkList


def download_zip_files(linkList):
    """take a list of links and download the files to the dedicated folder"""
    """TODO: improve rate limiter"""
    counter = 0
    for element in linkList:
        file_name = "Text" + str(counter) + ".zip"
        if not os.path.exists("Downloads"):
            os.makedirs("Downloads")
        try:
            urllib.request.urlretrieve(element, "Downloads/"+file_name)
        except:
            time.sleep(2)
            try:
                urllib.request.urlretrieve(element, "Downloads/"+file_name)
            except:
                print("Datei konnte immer noch nicht herunter geladen werden")

        print("Datei "+ str(counter) +" gedownloaded")
        counter += 1


def unzip_downloads():
    """unzip the files in the download folder and move them to the Source folder"""
    download_folder_path = os.getcwd()+"/Downloads"
    if not os.path.exists("Source"):
        os.makedirs("Source")
    for filename in os.listdir(download_folder_path):
        zip_path = "Downloads/"+filename
        zip_ref = zipfile.ZipFile(zip_path, 'r')
        zip_ref.extractall("Source")
        zip_ref.close()
        print(filename)

def create_law_list():
    """list the names of the laws in the Source folder"""
    name_list = []
    for filename in os.listdir("Source"):
        if ".xml" in filename:
            tree = etree.parse("Source/"+filename)
            root = tree.getroot()
            law_name = root.find("norm").find("metadaten").find("langue").text
            law_name = " ".join(law_name.split("\n")) #remove linebreaks from extracted name
            name_list.append(law_name)
            print(law_name)
    return name_list


def save_law_list(law_list):
    """save the law list to file"""
    law_list_file = codecs.open("law_list.txt", "w", "utf-8")
    for item in law_list:
        law_list_file.write("%s\n" % item)
    law_list_file.close()


#link_list = extract_download_links()
#print(str(len(link_list)) + " Gesetzestexte geladen")
#download_zip_files(link_list)
#print("Fuenf Dateien heruntergeladen")
#unzip_downloads()
law_list = create_law_list()
save_law_list(law_list)

"""TODO: Create Objects from XMLs"""
