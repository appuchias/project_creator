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

parser.add_argument(
    "-l", "--local", help="Set the project as local", action="store_true"
)
parser.add_argument(
    "-py", "--python", help="Auto add python main file", action="store_true"
)
parser.add_argument(
    "-s", "--script", help="Set the project as a script", action="store_true"
)
parser.add_argument(
    "project_name",
    help="Your local and remote project's name",
    type=str,
)  # nargs="?",)

args = parser.parse_args()

is_local, PROJECTNAME = args.local, args.project_name
DEST = getenv("DEST")
TOKEN = getenv("TOKEN")  # GitHub token
LOCAL = pathlib.Path(__file__).parent.resolve()
SCRIPTS = getenv("SCRIPTS_FOLDER_NAME")

if args.script and not args.python:  # Set the new root destination to
    DEST = path.join(DEST, "SCRIPTS")
elif args.script and args.python:
    DEST = path.join(DEST, SCRIPTS)

NEWFOLDER = path.join(DEST, PROJECTNAME)  # New folder on destination


# Make sure all settings are correct
c.print(
    f"""[cyan]Current settings:
    [·] - Project name: `{PROJECTNAME}`
    [·] - Project folder: `{NEWFOLDER}`
    [·] - {'Local' if is_local else 'Remote'} project
{'    [·] -' if args.python or args.script else ''} \
{'Python script file' if args.python and args.script else ('Python file' if args.python else ('Script' if args.script else ''))}""",
    end="" if not (args.python or args.script) else "\n",
)
c.print("[blue]If you want to proceed, press ENTER. Otherwise, press CTRL+C", end="")
input()


# Create destination folder if it doesn't exist, else warn the user
if not path.exists(NEWFOLDER):
    os.makedirs(NEWFOLDER)
else:
    c.print(
        f"[red bold]Path `{NEWFOLDER}` already exists, proceed anyways?\n\
[blue](ENTER to proceed, CTRL+C to exit)"
    )
    input("")

# Generic commands
commands = [
    "git init",
    "git add README.md",
    'git commit -m "Initial commit"',
]

# Add remote commands
if not is_local:
    user = Github(TOKEN).get_user()  # Login to GitHub
    login = user.login
    user.create_repo(PROJECTNAME, private=True)

    commands.append(
        f"git remote add origin https://github.com/{login}/{PROJECTNAME}.git"
    )
    commands.append("git push -u origin master")


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
    for command in commands:
        os.system(command)

    print(f"{PROJECTNAME} created")
except:
    c.print_exception()

finally:
    c.print("Done!")
    os.system("code .")  # Open edtor
    c.print(f"cd {NEWFOLDER}")
