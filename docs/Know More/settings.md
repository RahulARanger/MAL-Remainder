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
---

* Redirect to [Update-Progress](./UpdateList)
* ### [ReSchedule events from the calendar](#reschedule-🔄)
* ### [Reset OAuth](./api/#authentication)
* [Refresh Tokens](./api#refreshing-tokens)
* [Download Settings](# "look at button named 'Settings' at the top right corner")
* ### [Import Settings](#import-settings)
* [Auto Update](#auto-update)
* Redirects to your in [MyAnimeList](https://myanimelist.net)/animelist/your_name
* ## [Download the Data Collected](# "Look at the color-changing Button named 'data' at the top right corner")


### ReSchedule 🔄

This is same as the one which was automated [here](../../#:~:text=Every%20time%20you%20log%20in%20your%20system). But before scheduling in Task Scheduler, It tries to download calendar from the given URL. and then saves it locally.

### Import Settings

Refer this below image which was taken from Settings Page

![Import Settings](../../assets/import_settings.jpg "Importing Settings")

Just make sure to upload correct database file and then go with `Refer`. It just imports the settings from the given file so you wouldn't need to manually type them again.

## Auto Update
---

MAL-Remainder auto checks for the updates just after closing the application if it was triggered by the scheduler. By default this behavior is off. You can let the application know your preference based on the switch in the footer.

You can check for updates here [latest release](https://github.com/RahulARanger/MAL-Remainder/releases/latest "latest release")