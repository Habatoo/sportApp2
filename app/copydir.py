import os
import shutil

def copydir(source, dest):
    """Copy a directory structure overwriting existing files"""
    for root, dirs, files in os.walk(source):
        if not os.path.isdir(root):
            os.makedirs(root)

        for file in files:
            rel_path = root.replace(source, '').lstrip(os.sep)
            dest_path = os.path.join(dest, rel_path)

            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)

            shutil.copyfile(os.path.join(root, file), os.path.join(dest_path, file))

if __name__ == '__main__':
    source = r'C:\Python\web_framework\blog_flask\app\app\data\avatar'
    dest = r'C:\Python\web_framework\blog_flask\app\app\data\new'
    copydir(source, dest)
