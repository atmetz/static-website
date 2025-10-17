
from generator import copy_dir, generate_pages_recursive
import os
import shutil
import sys

public_path = './docs'
static_path = './static'
content_path = './content'
template_path = "./template.html"

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = '/'

print(basepath)

def main():

    print("Deleteing public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    
    print("Copying static files to public directory...")
    copy_dir(public_path, static_path)

    print("Generating content...")
    generate_pages_recursive(content_path, template_path, public_path, basepath)



main()
