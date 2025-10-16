from textnode import TextNode, TextType

from htmlnode import HTMLNode, LeafNode, ParentNode

from generator import copy_dir
import os
import shutil

destpath = './public'
path = './static'

def main():

    print("Deleteing public directory...")
    if os.path.exists(destpath):
        shutil.rmtree(destpath)
    
    print("Copying static files to public directory...")
    copy_dir(destpath, path)



main()
