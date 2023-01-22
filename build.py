#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import itertools
import subprocess as sp
import pathlib
import asyncio
import datetime

MAILCHIMP_TEXT = """{% embed url="https://bhavaniravi.substack.com/embed" %}
Newsletter embed
{% endembed %}"""

HEADER = f"""---
description: Not all those who wander are lost
---

# Start Here

> Hi I'm Bhavani & Welcome to my digital garden 🪴

_A digital garden is **an online space at the intersection of a notebook and a blog, where digital gardeners share seeds of thoughts to be cultivated in public**._
To know more about me [Click here](start-here/about-me.md)

{MAILCHIMP_TEXT}

---"""

BASE_URL = ""

SKIP_CATEGORY = ["about-me", "blogs", "start-here"]


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
            elif line.startswith("title:"):
                return line.split("title:")[-1]


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
        if os.path.isdir(fullname):
            # print(fullname)
            titles.extend(get_tils(fullname))
    return titles


async def write_mailchimp(category):
    til_files = [x for x in os.listdir(category)]
    for filename in til_files:
        fullname = os.path.join(category, filename)
        if (os.path.isfile(fullname)) and fullname.endswith(".md"):
            with open(fullname, "a") as f:
                f.write(f"\n\n--- \n\n {MAILCHIMP_TEXT}")


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
        file.write("""\n\n## Categories\n\n""")
        # print the list of categories with links
        for category, tils in sorted(
            categories.items(), key=lambda c: len(c[1]), reverse=True
        ):
            file.write(
                f"""* [{category.replace("-", " ").title()}](./#{category.replace(' ', '-').lower()}) [**`{len(tils)}`**]\n"""
            )

        if len(category_names) > 0:
            file.write("""\n---\n""")
            # print the section for each category
        for category, tils in sorted(
            categories.items(), key=lambda c: len(c[1]), reverse=True
        ):
            if len(tils) > 0:
                file.write(
                    "\n\n\n### {0}\n\n".format(category.replace("-", " ").title())
                )
                # file.write("<ul>")
                # print(tils)
                for (title, filename) in sorted(tils):
                    # file.write("\n<li>")
                    file.write(f"""* [{title.strip()}]({filename})""")
                    file.write("\n")


async def create_recent_tils_file(categories):
    """
    Generate recent_tils.json to be used by my website & github profile readme
    """

    print("Generating recent_tils.json")
    cmd = """git ls-tree -r --name-only HEAD | while read filename; do
  echo "$(git log -1 --format="%aD" -- $filename) $filename"
done"""
    recent_tils = []

    result = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = result.communicate()
    clean_output = [
        (" ".join(line.split(" ")[:-1]), line.split(" ")[-1])
        for line in out.decode("utf-8").strip("\n").split("\n")
    ]
    print(clean_output)
    # filter filepaths that don't exist
    flattened_list = list(itertools.chain(*list(categories.values())))
    flattened_list = [item[1] for item in flattened_list]
    valid_files = list(
        filter(
            lambda path: pathlib.Path(path[1]).exists() and path[1] in flattened_list,
            clean_output,
        )
    )

    for til in valid_files:
        date = til[0]
        til = til[1]
        til_dict = {}
        til_dict["title"] = get_title(til)
        til_dict["url"] = f"{BASE_URL}/{til[:til.rfind('.')].lower()}"
        til_dict["date"] = date
        recent_tils.append(til_dict)

    with open("recent_tils.json", "w") as json_file:
        json.dump(recent_tils, json_file, ensure_ascii=False, indent=" ")


def write_xml_file():
    from xml.sax.saxutils import escape

    HEAD = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <atom:link href="https://raw.githubusercontent.com/bhavaniravi/til/main/feed.xml" rel="self" type="application/rss+xml" />
"""

    FOOTER = """</channel>
</rss>
"""
    current_date = datetime.datetime.now()
    ctime = current_date.ctime()
    repo_name = os.path.basename(os.getcwd())

    files = json.loads(open("recent_tils.json").read())
    with open("feed.xml", "w") as feed:
        feed.write(HEAD)
        feed.write(
            f"""<title>Bhavani Ravi's Blogs</title>\n<link>https://www.bhavaniravi.com</link>\n"""
        )
        feed.write(
            f"""<description>Recently committed files in Bhavani's blog</description>\n"""
        )
        feed.write(
            f"""<lastBuildDate>f'{ctime[0:3]}, {current_date.day:02d} {ctime[4:7]} {current_date.strftime(' %Y %H:%M:%S %z')} GMT'</lastBuildDate>"""
        )
        feed.write
        for item in files:
            data = f"""<item>
    <guid>{"https://www.bhavaniravi.com"+item["url"]}</guid>
    <title>{escape(item["title"])}</title>
    <pubDate>{item["date"]}</pubDate>
    <link>{"https://www.bhavaniravi.com"+item["url"]}</link>
</item>\n"""

            feed.write(data)
        feed.write(FOOTER)


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
    # task2 = asyncio.create_task(create_readme(category_names, categories))
    # task3 = asyncio.create_task(create_gitbooks_summary(category_names, categories))
    task4 = asyncio.create_task(create_til_count_file(count))
    # for category in categories:
    #     if category != "products":
    #         asyncio.create_task(write_mailchimp(category))

    await task1
    # await task2
    # await task3
    await task4
    write_xml_file()

    # print(count, "TILs read")


asyncio.run(main())
