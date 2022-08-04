# Git Rebase

Rebasing is when you move the base of your branch as if it was created from a different commit than the original one

Let's assume two branches&#x20;

* main with 123456 current commit ID
* feature-1 is created from main at commit 123456

Now the base of feature-1 is 123456

As developers starts to push more code to each branches the commits will grow

* Main (123456) -> (99999) -> (566788) -> (123390)
* feature-1 (123456) -> (445666) -> (222344)

Now when you do rebase of main from feature-1, the base commit will be moved to main's latest commit, 123390

feature-1 (123390) -> (445666) -> (222344)

### Keeping Current Changes When Rebasing

```
git rebase -X ours upstream
```
