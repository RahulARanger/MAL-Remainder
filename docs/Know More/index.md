---
layout: default
title: Know More
has_children: true
nav_order: 3
permalink: /docs/Know More/
---

# Know More
---

This section is optional to read but good to know.

## General Instructions
---

* Hovering over an element will provide you more information.
* Read the errors from error pages and also from the console that is running in background.


## Shell Scripts
---

* #### Powershell 

> MAL-Remainder uses Powershell to automate certain tasks for instance to communicate with the [Task Scheduler](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page) to schedule a task "MAL-Remainder" or remove that, ...



* #### Command Prompt

> as a general script to access powershell script or itself without any os-specific issue.

```python
import subprocess
import sys
subprocess.run([
'setup', *sys.argv
], cwd=...)
```

For Instance for a given directory inside the `cwd` and in Windows it tries to run the `.cmd` file and in Linux it tries to run the `.sh` file,  etc...

<small><em>I Might be wrong above. Please correct me if i was wrong.</em></small>

## Task Scheduler in Windows
---

[![Task Scheduler in Windows](https://gigperformer.com/docs/ultimate-guide-to-optimize-windows-for-stage/images/hmfile_hash_bc24a763.png)](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)