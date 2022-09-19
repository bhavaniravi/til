---
slug: the-git-problem
published_date: 2020-02-06T00:00:00.000Z
created_date: 2020-02-06T00:00:00.000Z
title: How I Got Out of a Knee Deep Git Problem
template: post
draft: false
description: >-
  Git is easy to learn but hard to master. No matter how much you learn good
  chance you might screw something someday.
subtitle: ''
tags: ["software-engineering/git-and-github"]
featuredImgPath: >-
  https://camo.githubusercontent.com/b75d955466c5f5602998b752dd97ff1bdbe16168/68747470733a2f2f6769742d73636d2e636f6d2f696d616765732f6c6f676f732f646f776e6c6f6164732f4769742d4c6f676f2d32436f6c6f722e706e67
isexternal: true
---

# How I Got Out of a Knee Deep Git Problem

### Problem
- I am not used to rebasing or squashing commits, my new project strictly follows this hence I was pushed to do this.
- I started with 4 commits which I had to squash
- `git rebase -i HEAD~4` and squashed all the commits all were good
- But, as I pushed the code there was a conflict with the master
- If you remember you cannot `merge` hence I did a `git rebase -i master`
- Now I ended up having 10 more commits from god knows where
- I cannot push all of them, hence I squashed them all again, in spite of the commits not being mine
- I pushed my code, but the conflict was still there, at the brink of frustration I fixed the conflict in Github and left it there
- As expected, I was asked not to merge from master and revert it
- Now I am knee stuck with a merge, 9 commits squashed within which another 4 commits squashed

### Solution - Git Reflog to the rescue
- `git reflog` has a history of all the commands you ever executed 
- On running it I found the first squash I made
- `git reset --hard <commit_id>` took me to that commit
- One mistake I did last time when I rebased master was I didn't rebase from upstream so this time I ran `git pull upstream master --rebase`
- Now I did a `git add .` to add my changes to rebase
- `git rebase --continue` finishes the rebase successfully
- Finally `git push origin --force <branch-name>` to push the final version with no-conflicts and just my commits squashed into one.