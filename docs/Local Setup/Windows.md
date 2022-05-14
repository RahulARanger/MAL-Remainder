---
layout: default
title: Windows
parent: Local Setup
permalink: /docs/Local Setup/Windows
nav_order: 3
---

# Using Installer 

* Download [innosetup](https://jrsoftware.org/isdl.php) and follow the steps.

* Download [this](https://github.com/RahulARanger/MAL-Remainder/archive/refs/heads/master.zip) zip which is clone of this [repo](https://github.com/RahulARanger/MAL-Remainder).

* And open this file [InnoSetup-Installer-Scripts -> setup.iss](https://github.com/RahulARanger/MAL-Remainder/blob/master/InnoSetup-Installer-Scripts/setup.iss) from the root of the project in innosetup compiler.

* Comment [this](https://github.com/RahulARanger/MAL-Remainder/blob/99e2eb1a78112024cb5eaef97d1f9019e783cd34/InnoSetup-Installer-Scripts/setup.iss#L84) line from the above file

* Compile and run it and enjoy 😃

You can edit the unzipped project and then recompile to install modified ones.
