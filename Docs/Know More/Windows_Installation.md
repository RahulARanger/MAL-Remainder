---
layout: default
title: Windows Installation
parent: Know More
---

{: .important }
![Checking]()<br><br>You might be seeing this while installing the Application, because i didn't have signed license.

# Why Shell Scripts?

---

This Application depends on the Shell Scripts for the following reasons:

-   FileDialog: for selecting the path of the local file.
-   **Adding a Task on your system's scheduler**
-   Supporting script for setup [_Unzipping folder, deleting a directory, etc..._]

This can't be achieved efficiently in python. even if it exists, it takes a lot of space in your disk which is what i want to avoid the most of small application.

You can view the source code, if you want more trust.

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

-   Helper script for the setup
-   Executes Python Scripts whenever required
-   Registers Tasks
-   Edits Tasks
