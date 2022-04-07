---
layout: default
title: Installation in Windows
parent: Getting Started
nav_order: 1
permalink: /docs/Getting Started/win_installation
---

## Pre-requisites

-   Make sure you have Powershell installed on your machine and accessible with the cmdlet `powershell`. [i guess you don't need to worry about this, as it is provided by default.]


---

## Installing Executable

> Head over to the repository's release page for download link.

---

## Installation Process

-   **Application's Setup is build using [innosetup](https://jrsoftware.org/isinfo.php)**

{: .important }
While using this setup, you will definitely see Shell opening up in middle. That's a way to show the progress of either installation or un-installation. Make Sure **Not to close it**.

As warned above, it is recommended not to interrupt the shell process, But if you did,

-   For installation, it asks either you need to cancel the installation, if yes it removes whatever it did up until now, else it reopens the shell window ~~😈~~ to continue the process.
-   For un-installation, closing the window, would proceed with a way [_less informative_] to uninstall files


{: .warning }
It is sometimes possible for your anti-virus software to warn you about this application and may sometimes cancel the installation for the first time it does because of this [setup.cmd](https://github.com/RahulARanger/MAL-Remainder/blob/master/setup.cmd). Make sure to add it to excludes.


{: .warning}
Since this Application is not signed you will definitely see this error <br><br> ![warning before installation](../../../assets/warning_installation.jpeg "you may see this warning before installation")<br> If you want to install, `More Info` -> `Run Anyway`


## Here some of the screenshots:
---

* ![Shell Window while Installation](../../../assets/shell_installation.jpg "Shell Window shows up in mid of installation for setting up python env")

----

* ![Rolling Back](../../../assets/rolling_back.jpg "Rolls back if installation fails")

----

* Here we close the shell Window which shows while installation so it asks for confirmation and we agree to stop the installation which would result in,<br><br>
![Closed as request](../../../assets/closed_as_requested.jpg "Closed as per request")


Most of the errors that could occur while installation would raise this message box but with different message.

----

## End Result

- [X] Shortcut in your Startup Folder
- [X] Shortcut in groups Folder.
