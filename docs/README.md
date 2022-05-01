---
layout: default
title: Introduction
nav_order: 1
permalink: /
---
# Introduction
---

MAL-Remainder is an Application that allows you to update the number of episodes that you have on your `watch list` in [MyAnimeList](https://myanimelist.net "MyAnimeList") by regularly reminding you on the basis of events scheduled in [Google Calendar](https://www.google.com/calendar/about/ "Google Calendar")'s [ICalendar File](https://en.wikipedia.org/wiki/ICalendar ".ics file").


## MyAnimeList

[MyAnimeList](https://myanimelist.net "MyAnimeList") is a website known for its vast database over animes that have been released up until now and it also maintains a list of animes that you have watched or completed, etc... These are just a subset of its features. It can even do more. 


## Pre-Requisites
---

{: .note}

> Currently Runs only with Windows OS and its native Task Scheduler.

-   Must have an Account in [MAL](https://myanimelist.net "MyAnimeList")
-   Must be ok with Initial Setup as it is bit lengthy like filling a form for using API, feeding some details in this application, etc...


## Reason for its Existence
---

Animes are kinda shows, that we would watch not just one but many, so its important/good to have exact timestamps on its completion.


### Motive

-   I feel its good to have a systematic way of correctly updating your watch-list at regular intervals.

-   While using **PC**, I get stuck and spend a lot of time unnecessarily on some part. The Best way to deal with it is to take a break. And the best way to take a break is to have someone remind you to take a break.

- I wanted to track my movements and since `Watching` is one of my prime activity in my day-to-day activities, I wanted to track this. and i feel this is one way to do that.

### Watch-list

MAL's Database contains information about every registered user's interaction over anime which can be labelled as either one of the following,

-   Completed
-   Watching
-   Dropped
-   On-Hold
-   Plan to Watch

{: .comfy }
Most probably, we pick an anime watch it and then complete it.

## Automation
---
   
MAL-Remainder has some Automation Scripts which makes requests with the `MAL Server` through their [API](https://myanimelist.net/apiconfig/references/api/v2) for both fetching the information and updating information from/onto the server.

This follows things are automated by MAL-Remainder for you.

1.  Every time you login in your system, It reschedules events for today, it does that by referring from your local _.ics_ file _(if not present, tries to download from the given url in settings)_, It schedules events based on the events in calendar under the name `MAL_Remainder`.

2. Before Updating your preferences, it fetches your watchlist where animes are labelled as `watching`, which then fetches details about each of that anime.

3. After Updating your preference, values are recorded in a file named `data.csv` which can downloaded in settings.

----

[Getting Started](./docs/Getting Started){: .btn .btn-blue}