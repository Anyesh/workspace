<p align="center">
  <a href=#">
    <img width="100" src="./assets/workspace.png">
  </a>
</p>

<h1 align="center">Workspace</h1>
<p align="center">Easy way to change back-and-forth between different git branches that you are working on.</p>

# Installation

You can install `workspace` directly from github

```bash
pip install git+https://github.com/Anyesh/workspace@develop#egg=workspace
```

OR

You can download this repo and run

```bash
pip install -e .
```

from the root directory.

# Usage

## Working on a new branch?

```bash
ws create
```

If you are a first time user, you will be asked to provide the path to your root directory.

Output:

```bash
❯ ws create
[14:48:24] 😃 Hello there <user>!                                                                                                                                                                                                     cli.py:109
Looks like this is your first time here
🦝 Let's get you set up
[?] Full path of your Alaya directory (something like '/home/user/path/') : /home/user/test/path/
[14:49:42] 👍 All set! using /home/user/test/path as your root dir
```

```bash
❯ ws create
[15:00:45] 😃 Hello there <user>!                                                                                                                                                                                                     cli.py:109
[?] Which Jira ticket are you working on?: tset-01
[?] Which apps are you working on?:
   X submodule_1
 > X submodule_2

[?] Short Description: testing this script
[?] Ticket Type: story
 > story
   subtask
   bugfix
   hotfix
   release

[15:00:55] ⚙ creating branch on submodule_1 ..                                                                                                                                                                                         cli.py:75
[?] Which branch you want to base submodule_1 on?: master
 > master

[15:00:57] ⚙ saving any unsaved changes                                                                                                                                                                                                cli.py:96
           ⚙ checking out master ..                                                                                                                                                                                                    cli.py:98
           ⚙ pulling latest changes
[15:00:55] ⚙ creating branch on submodule_2 ..                                                                                                                                                                                         cli.py:75
[?] Which branch you want to base submodule_2 on?: master
 > master

[15:00:57] ⚙ saving any unsaved changes                                                                                                                                                                                                cli.py:96
           ⚙ checking out master ..                                                                                                                                                                                                    cli.py:98
           ⚙ pulling latest changes
[15:00:59] ✓ All done! 🍀
```

## Switching between branches?

```bash
ws change
```

Output:

```bash
❯ ws change
[15:02:50] 😃 Hello there <user>!                                                                                                                                                                                                     cli.py:109
[?] Which Jira ticket are you working on?: aus-05
[?] Which apps are you working on?:
   X submodule_1
 > X submodule_2

[15:02:54] ⚙ changing branch of submodule_1 ..
[15:02:54] ⚙ changing branch of submodule_2 ..
[15:02:54] ✓ All done! 🍀
```

## Want to get current info?

```bash
ws info
```

Output:

```bash
[13:44:18] 😃 Hello there <user>!                                                                                                                                                                                                     cli.py:109
Your current project path: '/home/<user>/path'
Your current root branch is 'develop'
Your submodules status are:
+28b45b0a121cd324392c42c1ee09d4b23fb23bf3 submodule1 (release-0.275.0-2321-g28ba5b0011)

[13:44:20] ✓ All done! 🍀
```

## Want to quickly change branch?

```bash
ws change <ticket-id>

Quickly changing branch to <ticket-id> on recently used apps (if available) assista
[23:14:30] ⚙ changing branch submodule_2 ..
           ⚙ checking out story/<ticket-id>-this-is-<ticket-id> ..
           ⚙ changing branch of submodule_1 ..
           Branch not found for submodule_1
           ✓ All done! 🍀
```

---

If anything goes wrong, delete the `.workspace` folder in your home directory and try again.
