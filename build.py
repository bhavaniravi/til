#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import itertools
import subprocess as sp
import pathlib
import asyncio

HEADER = """---
description: Not all those who wander are lost
---

# Start Here

> Hi I'm Bhavani & Welcome to my digital garden 🪴

_A digital garden is **an online space at the intersection of a notebook and a blog, where digital gardeners share seeds of thoughts to be cultivated in public**._
To know more about me [Click here](start-here/about-me.md)

---"""

BASE_URL = ""

SKIP_CATEGORY = ["about-me"]

async def get_category_list():
    """
    Walk the current directory and get a list of all subdirectories at that
    level.  These are the "categories" of TILs.
    """
    avoid_dirs = [
        "images",
        "stylesheets",
        "javascripts",
        "_layouts",
        ".sass-cache",
        "_site",
    ] + SKIP_CATEGORY
    dirs = [
        x
        for x in os.listdir(".")
        if os.path.isdir(x) and ".git" not in x and x not in avoid_dirs
    ]
    return dirs


def get_title(til_file):
    """
    Read the file until we hit the first line that starts with a #
    indicating a title in markdown.
    """
    with open(til_file) as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                # print(line[1:])
                return line[1:].lstrip()  # text after # and whitespace


def get_tils(category):
    """
    For a given category, get the list of TIL titles
    """
    til_files = [x for x in os.listdir(category)]
    titles = []
    for filename in til_files:
        fullname = os.path.join(category, filename)
        if (os.path.isfile(fullname)) and fullname.endswith(".md"):
            title = get_title(fullname)
            # changing path separator for Windows paths
            # https://mail.python.org/pipermail/tutor/2011-July/084788.html
            titles.append((title, fullname.replace(os.path.sep, "/")))
    return titles


def get_category_dict(category_names):
    categories = {}
    count = 0
    for category in category_names:
        if category not in SKIP_CATEGORY:
            titles = get_tils(category)
            categories[category] = titles
            count += len(titles)
    return (count, categories)


def read_file(filename):
    with open(filename) as file:
        return file.read()


# async def create_gitbooks_summary(category_names, categories):
#     """
#     Create SUMMARY.md for GitBooks site
#     """
#     print("Generating SUMMARY.md")
#     with open("SUMMARY.md", "w") as summary:
#         for category in sorted(category_names):
#             summary.write("\n\n## {0}\n\n".format(category))
#             tils = categories[category]
#             summary.write("<ul>")
#             for (title, filename) in sorted(tils):
#                 summary.write("\n<li>")
#                 summary.write(f"""<a href="{filename}">{title}</a>""")
#             summary.write("\n")
#             summary.write("</ul>")


async def create_til_count_file(count):
    """
    Used by shields.io for generating the TILs count badge on GitHub
    """
    print("Generating count.json")
    with open("count.json", "w") as json_file:
        data = {"count": count}
        json.dump(data, json_file, indent=" ")


async def create_readme(category_names, categories):
    """
    Generate the README.md for github repo
    """
    print("Generating README.md")

    with open("README.md", "w") as file:
        file.write(HEADER)
        file.write("""\n\n## Categories\n""")
        # print the list of categories with links
        for category in sorted(category_names):
            tils = categories[category]
            file.write(
                f"""* [{category.replace("-", " ").title()}](#{category.replace(' ', '-').lower()}) [**`{len(tils)}`**]\n"""
            )

        if len(category_names) > 0:
            file.write("""\n---\n\n""")
            # print the section for each category
        for category in sorted(category_names):
            
            tils = categories[category]
            if len(tils) > 0:
                file.write("\n\n\n### {0}\n\n".format(category.replace("-", " ").title()))
                # file.write("<ul>")
                for (title, filename) in sorted(tils):
                    # file.write("\n<li>")
                    file.write(
                        f"""- [{title}](/{filename})"""
                    )
                    file.write("\n")


async def create_recent_tils_file(categories):
    """
    Generate recent_tils.json to be used by my website & github profile readme
    """

    print("Generating recent_tils.json")
    cmd = "git log --no-color --date=format:'%d %b, %Y' --diff-filter=A --name-status --pretty=''"
    recent_tils = []

    result = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = result.communicate()
    clean_output = out.decode("utf-8").strip("\n").replace("A\t", "").split("\n")
    # filter filepaths that don't exist
    flattened_list = list(itertools.chain(*list(categories.values())))
    flattened_list = [item[1] for item in flattened_list]
    valid_files = list(
        filter(
            lambda path: pathlib.Path(path).exists() and path in flattened_list,
            clean_output,
        )
    )

    for til in valid_files[:10]:
        til_dict = {}
        til_dict["title"] = get_title(til)
        til_dict["url"] = f"{BASE_URL}/{til[:til.rfind('.')].lower()}"
        recent_tils.append(til_dict)

    with open("recent_tils.json", "w") as json_file:
        json.dump(recent_tils, json_file, ensure_ascii=False, indent=" ")


async def main():
    """
    TIL Build Script Algorithm:

    1. Get list of directories
    2. For each valid TIL category, find markdown files inside it
    3. Generate recent_tils using git
    4. Generate SUMMARY.md for gitbook
    5. Generate README.md for GitHub
    """

    get_categories = asyncio.create_task(get_category_list())
    category_names = await get_categories
    count, categories = get_category_dict(category_names)

    task1 = asyncio.create_task(create_recent_tils_file(categories))
    task2 = asyncio.create_task(create_readme(category_names, categories))
    # task3 = asyncio.create_task(create_gitbooks_summary(category_names, categories))
    task4 = asyncio.create_task(create_til_count_file(count))

    await task1
    await task2
    # await task3
    await task4

    print(count, "TILs read")


asyncio.run(main())