import shutil, os
from os import path
from sys import argv
from rich.console import Console
from rich.traceback import install
from github import Github
from dotenv import load_dotenv
from os import getenv

load_dotenv()
install()


def create(name: str, flag: str):
    c = Console()

    DEST = getenv("DEST")  # Destination folder
    TOKEN = getenv("TOKEN")  # GitHub token
    LOCAL = getenv("LOCAL")  # Local folder

    FOLDERNAME = name
    NEWDIR = path.join(DEST, FOLDERNAME)  # New folder on destination

    if not path.exists(NEWDIR):  # Add destination folder
        os.mkdir(NEWDIR)

    # Commands setting
    if not flag:  # Not local -> remote
        user = Github(TOKEN).get_user()  # Login to GitHub
        login = user.login
        user.create_repo(FOLDERNAME, private=True)

        commands = [
            "git init",
            f"git remote add origin https://github.com/{login}/{FOLDERNAME}.git",
            "git add .",
            'git commit -m "Initial commit"',
            "git push -u origin master",
        ]

    else:  # local
        commands = [
            "git init",
            "git add README.md",
            'git commit -m "Initial commit"',
        ]

    # Global actions
    try:
        for fileobj in os.scandir(path.join(LOCAL, "toClone")):  # Move files to destination
            shutil.copy2(
                path.join(fileobj.path),
                path.join(NEWDIR, fileobj.name.replace("template", "")),
            )

        os.chdir(NEWDIR)  # Change to destination folder

        for c in commands:  # Create project
            os.system(c)

        os.system("virtualenv venv")
        os.system(".\\venv\\Scripts\\activate.bat")
        os.system("code .")

        print(f"{FOLDERNAME} created")
    except:
        c.print_exception()

    finally:
        print("Done!")
        os.system(f"cd {NEWDIR}")

    return NEWDIR


if __name__ == "__main__":
    assert argv[1], "Project name could not be found"

    # Set local or remote
    try:
        flag = argv[2]
    except IndexError:
        flag = None

    create(str(argv[1]), flag)
