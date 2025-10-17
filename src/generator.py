import os
import shutil

from markdown import markdown_to_html_node


def copy_dir(copypath, path):

    if not os.path.exists(copypath):
        os.mkdir(copypath)

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        destfilepath = os.path.join(copypath, filename)        
        print('copying ' + filepath + ' to ' + copypath)
        if os.path.isfile(filepath):
            shutil.copy(filepath, destfilepath)
        else:
            copy_dir(destfilepath, filepath)

    return

def extract_title(markdown):
        
    lines = markdown.split('\n')

    for line in lines:

        if line.lstrip().startswith("# "):
            title = line[2:]
            return title.strip()
        
    raise Exception("No header found")

def generate_page(from_path, template_path, dest_path, basepath):

    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    dirs = dest_path.split('/')
    new_path = ''

    for dir in dirs:
        if dir != dirs[-1]:
            new_path = new_path + dir + "/"
            if not os.path.exists(new_path):
                os.mkdir(new_path)

    mdfile = open(from_path)
    templatefile = open(template_path)
    htmlfile = open(dest_path, "x")

    template = templatefile.read()
    markdown = mdfile.read()
    
    htmlstring = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    htmlfile.write(template.replace("{{ Title }}", title).replace("{{ Content }}", htmlstring).replace('href="/', f'href="{basepath}'.replace('src="/', f'src="{basepath}')))

    mdfile.close()
    templatefile.close()
    htmlfile.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    content_dirs = os.listdir(dir_path_content)

    for content_dir in content_dirs:
        if os.path.isdir(os.path.join(dir_path_content, content_dir)):
            generate_pages_recursive(os.path.join(dir_path_content, content_dir), template_path, os.path.join(dest_dir_path, content_dir), basepath)
        else:
            generate_page(os.path.join(dir_path_content, content_dir), template_path, os.path.join(dest_dir_path, "index.html"), basepath)