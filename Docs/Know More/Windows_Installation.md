---
layout: default
title: Windows Installation
parent: Know More
nav_order: 1
permalink: /docs/Know More/Win_Installation
---
# Why Shell Scripts?

---

This Application depends on the Shell Scripts for the following reasons:

-   used local FileDialog for importing Settings.
-   **Adding a Task on your system's scheduler**
-   Supporting script for setup [_Unzipping folder, deleting a directory, etc..._]

I believe this makes our application consume less space than before.


# Roles

## Cmd Script

---

🌉 between powershell and python script. In Windows, running the command `setup` would trigger the batch script

```python
import subprocess
import sys
subprocess.run([
'setup', *sys.argv
], cwd=...)
```

> So by this way, i can access setup file irrespective of extension of the setup file. In linux, i guess we can do this with `setup.bat`.

## Powershell Script

---

#### 💖 Powershell, made this application light and also look kinda evil but it isn't evil.

-   Helper script for the setup q
-   Executes Python Scripts whenever required
-   Registers Tasks
-   Edits Tasks
