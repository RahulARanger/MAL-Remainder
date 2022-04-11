---
layout: default
title: Settings
parent: Know More
permalink: /docs/Know More/settings
nav_order: 3
---

As seen before, this is the settings page.

![Settings Page](../../assets/settings.jpg "Settings page")

# Features

In Settings page one can 

* [Force a Remainder](#force-a-remainder)
* [ReSchedule events from the calendar](#reschedule)
* [Reset OAuth](./api/#authentication)
* [Refresh Tokens](./api#refreshing-tokens)
* [Import Settings](#import-settings)
* [Auto Update](#auto-update)


And other it redirects to your AnimeList in [MyAnimeList](https://myanimelist.net)/animelist/your_name. Though this would work only if Application has fetched some of your details in your profile. It just uses your name and Profile Picture.

## Force a Remainder

It would just open [UpdateList](./UpdateList) page as it would with remainders set in your Scheduler.

## Import Settings

Refer this below image which was taken from Settings Page

![Import Settings](../../assets/import_settings.jpg "Importing Settings")

Just make sure to upload correct database file and then go with `Refer`.

## ReSchedule

In the Settings Page, you would see **Calendar with a button next to it**. Just fill the correct URL and then go with that button

It will first download the `ics` file and saves it locally and then reschedules it through powershell script.

### On Login

the latter part is automated that is referring your local ics file and then creating triggers based on the events in your file.


## Auto Update

MAL-Remainder auto checks for the updates just after closing the application if it was triggered by the scheduler. By default this behavior is off. You can let the application know your preference based on the switch in the footer.

Just checks with the repo if there's any latest release available based on the version hardcoded 
inside the MAL_Remainder python package. If found one, updates it but it just downloads the installer and runs it. So you would need to be there for it to update _(updating takes less time than the installation)_.

You can check for updates here [latest release](https://github.com/RahulARanger/MAL-Remainder/releases/latest "latest release")