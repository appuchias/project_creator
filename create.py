import shutil, os, argparse, pathlib
from os import path
from rich.console import Console
from rich.traceback import install
from github import Github
from dotenv import load_dotenv
from os import getenv

load_dotenv()
install()
c = Console()

# ############################################################################ #
# DEST         - The folder where new projects' folders will be created into.  #
# LOCAL        - The folder where `create.py` is located.                      #
# SCRIPTS      - The folder name of script type files.                         #
# PROJECTNAME  - The name of the project created (And so the folder).          #
# NEWFOLDER    - The path to the folder to be created (DEST + PROJECTNAME).    #
# ############################################################################ #


# Argparser
parser = argparse.ArgumentParser()

parser.add_argument("-l", "--local", help="Set the project as local", action="store_true")
parser.add_argument("-py", "--python", help="Auto add python main file", action="store_true")
parser.add_argument("-s", "--script", help="Set the project as a script", action="store_true")
parser.add_argument(
    "project_name",
    help="Your local and remote project's name",
    type=str,
)  # nargs="?",)

args = parser.parse_args()
name, local = args.project_name, args.local

is_local, PROJECTNAME = args.local, args.project_name
DEST = getenv("DEST")
TOKEN = getenv("TOKEN")  # GitHub token
LOCAL = pathlib.Path(__file__).parent.resolve()
SCRIPTS = getenv("SCRIPTS_FOLDER_NAME")

if args.script and not args.python:  # Set the new root destination to
    DEST = path.join(DEST, SCRIPTS)

if args.script:  # Set the new root destination to
    DEST = path.exists(path.join(DEST, SCRIPTS_FOLDER_NAME))

NEWFOLDER = path.join(DEST, PROJECTNAME)  # New folder on destination

if not path.exists(NEWFOLDER):  # Create destination folder
    os.makedirs(NEWFOLDER)


# Commands setting
if is_local:
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

    if args.python:
        open(path.join(NEWFOLDER, "main.py"), "a").close()

    # Create project
    for c in commands:
        os.system(c)

    os.system("python -m virtualenv venv")
    os.system("code .")

    print(f"{PROJECTNAME} created")
except:
    c.print_exception()

finally:
    print("Done!")
    os.system(f"cd {NEWFOLDER}")
