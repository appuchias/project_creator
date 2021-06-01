# Project creator

[![MIT license](https://img.shields.io/github/license/appuchias/project_creator?style=flat-square)](https://github.com/appuchias/project_creator/blob/master/LICENSE)
[![Author](https://img.shields.io/badge/Project%20by-Appu-9cf?style=flat-square)](https://github.com/appuchias)
![Size](https://img.shields.io/github/repo-size/appuchias/project_creator?color=orange&style=flat-square)

## **How it works**

This project automates the repetitive taskk of creating a folder with the same files every time you decide to start a new project of your own. With this script you will be able to place all the files you want to be cloned into your new folder inside the `toClone` folder and after you run the file, they will be placed in their correspondent folder. Make sure you set up the necessary environmental variables _before_ you run the file so it can find them.

## **Setup**

1. Navigate to the desired folder: `cd <path>`
1. Clone the repo: `git clone https://github.com/appuchias/project_creator.git`
1. Navigate into the repo folder: `cd project_creator`
1. Setup environmental variables (Inside `.env` file)

    - TOKEN

        Your (upload allowed) GitHub token

    - LOCAL

        The folder the repo is in

    - DEST

        The folder new project folders will be created in

1. Install the project dependencies: `pip install -r requirements.txt`
1. Run the file: `python create.py [-h] [-l] [-p] [-s] project_name`

- **[Tip!]** Add `create` to PATH or create a runner file to ease the use. (Help [here](PathAddition.md))

## **License**

This project is licensed under the [MIT license](https://github.com/appuchias/project_creator/blob/master/LICENSE).

Coded with 🖤 by Appu
