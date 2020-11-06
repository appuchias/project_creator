import sys
import os
import shutil
from os import path
from time import sleep
from github import Github
import json

def create():
    ROOT_FOLDER = r"C:\V\Programming"

    with open(r"C:\V\Programming\project_creator\settings.json") as r:
        settings = json.load(r)

    try:
        flag = sys.argv[1]
    except IndexError:
        raise RuntimeError("Could not find a project name in the run sentence. Please enter a project name. (python3 create.py <name>)")

    try:
        flag = sys.argv[2]
    except IndexError:
        flag = None

    foldername = str(sys.argv[1])
    token = settings["token"]
    local_path = settings["local"]

    _dir = path.join(ROOT_FOLDER, foldername)

    if not flag: # Not local -> remote
        g = Github(token)
        user = g.get_user()
        login = user.login
        user.create_repo(foldername, private=True)

        if not path.exists(_dir):
            os.mkdir(_dir)

        shutil.copy2(path.join(local_path, "template.md"), os.path.join(_dir, "README.md"))
        shutil.copy2(path.join(local_path, "template.gitignore"), os.path.join(_dir, ".gitignore"))
        shutil.copy2(path.join(local_path, "LICENSE"), os.path.join(_dir, "LICENSE"))

        commands = [
            "git init",
            f"git remote add origin https://github.com/{login}/{foldername}.git",
            "git add .",
            "git commit -m \"Initial commit\"",
            "git push -u origin master",
        ]

    else: # local
        commands = [
            "git init",
            "git add README.md",
            "git commit -m \"Initial commit\"",
        ]

    try:
        os.chdir(_dir)

        for c in commands:
            os.system(c)
        
        os.system("code .")

        print(f"{foldername} created")
    finally:
        pass
        
if __name__ == "__main__":
    create()
    sleep(2)
    os.system("exit")
