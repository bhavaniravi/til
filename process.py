# read all the files from blog directory

import os
import frontmatter
import shutil

mapping = {}
tag_mapping = {}
for filename in os.listdir("blogs/"):
    # for each file, we are going to read the metadata
    post = frontmatter.load(f"blogs/{filename}")

    # extract the slug and tag, title from there
    slug = post["slug"]
    title = post["title"]
    tag = post["tags"][0]

    if len(tag) < 3:
        print(title)
    # create a dict mapping of `blog/<slug>` to `<tag>/<title.md>`
    mapping[f"blog/{slug}"] = f"{tag}/{slug}.md"
    if tag in tag_mapping:
        tag_mapping[tag].append(f"* [{title}]({tag}/{slug}.md)")
    else:
        tag_mapping[tag] = [f"* [{title}]({tag}/{slug}.md)"]

for key, value in tag_mapping.items():
    print(key)
    for item in value:
        print(item)

    print("\n\n")


# print the redirect mapping in the yaml format
# with open("data.yaml", "w") as outfile:
#     for key, value in mapping.items():
#         outfile.write(f"{key}: {value} \n")

# copy the file from `blogs/file.md` into `tag/<title.md>`
# if not os.path.exists(tag):
#     os.makedirs(tag)
# shutil.copyfile(f"blogs/{filename}", f"{tag}/{slug}.md")
# print(f"* [{title}]({tag}/{slug}.md)")
