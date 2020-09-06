import sys
import os
from os import path
from github import Github
import json

with open("settings.json") as r:
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
path = settings["path"]
token = settings["token"]

_dir = os.path.join(path, foldername)

if not flag: # Not local -> remote
    g = Github(token)
    user = g.get_user()
    login = user.login
    repo = user.create_repo(foldername, private=True)

    commands = [
        f"copy template.md " + os.path.join(_dir, "README.md"),
        f"copy template.gitignore" + os.path.join(_dir, ".gitignore"),
        f"copy LICENSE " + os.path.join(_dir, "LICENSE"),
        "git init",
        f"git remote add origin https://github.com/{login}/{foldername}.git",
        "git add .",
        'git commit -m "Initial commit"',
        "git push -u origin master",
    ]

else: # local
    commands = [
        "git init",
        "git add README.md",
        "git commit -m \"First commit\"",
    ]

try:
    os.mkdir(_dir)
    os.chdir(_dir)

    for c in commands:
        os.system(c)

    print(f"{foldername} created")

except Exception as e:
    print("create <foldername> {py}")
    print(e)
