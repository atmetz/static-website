import os
import shutil


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