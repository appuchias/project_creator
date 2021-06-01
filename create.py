import shutil, os, argparse
from os import path
from rich.console import Console
from rich.traceback import install
from github import Github
from dotenv import load_dotenv
from os import getenv

load_dotenv()
install()
c = Console()


# Argparser stuff
parser = argparse.ArgumentParser()

parser.add_argument("-l", "--local", help="Set the project as local", action="store_true")
parser.add_argument(
    "-p", "--python", help="Automatically add python main file", action="store_true"
)
parser.add_argument("-s", "--script", help="Set the project as a script", action="store_true")
parser.add_argument("project_name", help="Your project's name for your files and GitHub", nargs="?")

args = parser.parse_args()
name, local = args.project_name, args.local

if not name:
    name = input("Please specify project name: ").strip()


DEST = getenv("DEST")  # Projects root folder
TOKEN = getenv("TOKEN")  # GitHub token
LOCAL = getenv("LOCAL")  # This file's folder

PROJECTNAME = name
NEWFOLDER = path.join(DEST, PROJECTNAME)  # New folder on destination

if not path.exists(NEWFOLDER):  # Create destination folder
    os.mkdir(NEWFOLDER)


# Commands setting
if local:
    commands = [
        "git init",
        "git add README.md",
        'git commit -m "Initial commit"',
    ]

else:  # Not local -> remote
    user = Github(TOKEN).get_user()  # Login to GitHub
    login = user.login
    user.create_repo(PROJECTNAME, private=True)

    commands = [
        "git init",
        f"git remote add origin https://github.com/{login}/{PROJECTNAME}.git",
        "git add .",
        'git commit -m "Initial commit"',
        "git push -u origin master",
    ]


# Global actions
try:
    # Move files to destination
    for fileobj in os.scandir(path.join(LOCAL, "toClone")):
        shutil.copy2(
            path.join(fileobj.path),
            path.join(NEWFOLDER, fileobj.name.replace("template", "")),
        )

    # Change to destination folder
    os.chdir(NEWFOLDER)

    # Create project
    for c in commands:
        os.system(c)

    os.system("python -m virtualenv venv")
    os.system(".\\venv\\Scripts\\activate.bat")
    os.system("code .")

    print(f"{PROJECTNAME} created")
except:
    c.print_exception()

finally:
    print("Done!")
    os.system(f"cd {NEWFOLDER}")
