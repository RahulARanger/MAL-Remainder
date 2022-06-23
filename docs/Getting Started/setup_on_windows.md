---
layout: default
title: Setup on Windows
parent: Getting Started
nav_order: 1
permalink: /docs/Getting Started/win_setup
---


[MAL-Remainder.exe](https://github.com/RahulARanger/MAL-Remainder/releases/latest/download/MAL-Remainder.exe "Executable file"){: .btn .btn-blue}
{: .px-9 }

---

# Installation Process
---

-   **Application's Setup is build using [innosetup](https://jrsoftware.org/isinfo.php)**

{: .important }
While using this setup, you will definitely see PowerShell opening up in middle. That's a way to show the progress of either installation or un-installation. Make Sure **Not to close it**.

As warned above, it is recommended not to interrupt the shell process, But if you did,

-   For installation, it will prompt for cancelling it, if yes it removes whatever it did up until now, else it reopens the shell window ~~😈~~ to continue the process.
-   For un-installation, closing the window, would proceed with a way [_less informative_] to uninstall files

{: .highlight}
Since this is a personal Project and it is made in simple way. So you may see certain warnings like the ones listed below. I would recommend you to ignore them. But It is possible to build this [`locally`](../../Local%20Setup/Windows)


{: .warning}
Since this Application is only self-signed you will definitely see this error <br><br>
<img src="../../assets/warning_installation.jpeg" alt="Warning for first time Installation" title="you may see this warning for first-time installation" width="500" height="690"/><br> If you want to install, `More Info` ➡ `Run Anyway`

## Here some of the screenshots:
---

* ![Shell Window while Installation](../../assets/shell_installation.jpg "Shell Window shows up in mid of installation for setting up python env")

----

* ![Rolling Back](../../assets/rolling_back.jpg "Rolls back if installation fails")

----

* Closing the shell window while installation and agreeing to stop the installation,<br><br>
![Closed as request](../../assets/closed_as_requested.jpg "Closed as per request")


Most of the errors that could occur while installation would raise this message box but with a different message.

## End Result
----

At the Beginning of the Installation, Application would require 45 MB but at the end it would only consume over 35.6 MB.

Creates

- [X] Shortcut in your Startup Folder.
- [X] Shortcut in groups Folder.
- [X] Shortcut in desktop if requested.
