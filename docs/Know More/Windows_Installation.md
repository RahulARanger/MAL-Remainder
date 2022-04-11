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

-   **Adding a Task on your system's scheduler** 
-   Supporting script for setup [_Unzipping folder, deleting a directory, etc..._]


Those reasons are why that this application is OS-Specific. For now i was able to implement this in Windows. If you want in other os then if you are able to replicate the above steps, You can easily have this application in your System.

# Roles

## Cmd Script

---

🌉 between powershell and python script. cmd scripts are recognized which means they can run without explicitly specifying the extension. In linux i guess we can do that with .sh files.

So using this cmd script, I was trying to execute powershell script without specifying its extension.

```python
import subprocess
import sys
subprocess.run([
'setup', *sys.argv
], cwd=...)
```

## Powershell Script

---

#### 💖 Powershell, made this application light and also look kinda evil but it isn't evil.

-   Helper script for the setup q
-   Executes Python Scripts whenever required
-   Registers Tasks
-   Edits Tasks

You can refer [gate.ps1](https://github.com/RahulARanger/MAL-Remainder/blob/master/gate.ps1) and [setup.cmd](https://github.com/RahulARanger/MAL-Remainder/blob/master/setup.cmd)