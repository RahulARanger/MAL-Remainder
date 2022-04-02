---
layout: default
title: Installation in Windows
parent: Getting Started
---

## Pre-requisites

-   Make sure you have Powershell installed on your machine and accessible with the cmdlet `powershell`. [i guess you don't need to worry about this, as it is provided by default.]

---

## Installing Executable

> Head over to the repository's release page for download link.

---

## Installation Process

-   **Application's Setup is build using [innosetup](https://jrsoftware.org/isinfo.php)**

{: .warning }
While using this setup, you will definitely see Shell opening up in middle. That's a way to show the progress of either installation or un-installation. Make Sure **Not to close it**.

As warned above, it is recommended not to interrupt the shell process, But if you did,

-   For installation, it asks either you need to cancel the installation, if yes it removes whatever it did up until now, else it reopens the shell window ~~😈~~ to continue the process.
-   For un-installation, closing the window, would proceed with a way [_less informative_] to uninstall files

## End Result

-   Creates a Icon for MAL-Remainder [same as batch script tho] in Startup folder which when opened would redirect you to setting page of application.
-   Creates a Icon in your startup folder which fetches
