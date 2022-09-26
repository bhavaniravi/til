# # read all the files from blog directory

# import os
# import frontmatter
# import shutil

# mapping = {}
# tag_mapping = {}
# for filename in os.listdir("blogs/"):
#     # for each file, we are going to read the metadata
#     post = frontmatter.load(f"blogs/{filename}")

#     # extract the slug and tag, title from there
#     slug = post["slug"]
#     title = post["title"]
#     tag = post["tags"][0]

#     if len(tag) < 3:
#         print(title)
#     # create a dict mapping of `blog/<slug>` to `<tag>/<title.md>`
#     mapping[f"blog/{slug}"] = f"{tag}/{slug}.md"
#     if tag in tag_mapping:
#         tag_mapping[tag].append(f"* [{title}]({tag}/{slug}.md)")
#     else:
#         tag_mapping[tag] = [f"* [{title}]({tag}/{slug}.md)"]

# for key, value in tag_mapping.items():
#     print(key)
#     for item in value:
#         print(item)

#     print("\n\n")


# print the redirect mapping in the yaml format
# with open("data.yaml", "w") as outfile:
#     for key, value in mapping.items():
#         outfile.write(f"{key}: {value} \n")

# copy the file from `blogs/file.md` into `tag/<title.md>`
# if not os.path.exists(tag):
#     os.makedirs(tag)
# shutil.copyfile(f"blogs/{filename}", f"{tag}/{slug}.md")
# print(f"* [{title}]({tag}/{slug}.md)")


import os
import frontmatter
import shutil

mapping = {}
# for filename in os.listdir("talks/"):
#     post = frontmatter.load(f"talks/{filename}")
#     slug = filename
#     title = post.get("title")
#     print(f"* [{title}](talks/{slug})")


# for filename in os.listdir("projects/"):
#     post = frontmatter.load(f"projects/{filename}")
#     slug = filename
#     title = post.get("title")
#     description = post.get("description")
#     tech_stack = ""
#     for tag in post.get("tech"):
#         tech_stack += f"- {tag}\n"

#     client = post.get("client")
#     client_url = post.get("client_url")

#     with open(f"projects/{filename}", "a+") as f:
#         f.write(
#             f"# {title}\n{description}\n\n## Tech Stack\n{tech_stack}\n## Client\n[{client}]({client_url})"
#         )

# for filename in os.listdir("open-source/contributions"):
#     post = frontmatter.load(f"open-source/contributions/{filename}")
#     slug = filename
#     title = post.get("title")
#     print(f"* [{title}](open-source/contributions/{slug})")
