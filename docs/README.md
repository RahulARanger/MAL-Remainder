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

[MyAnimeList](https://myanimelist.net "MyAnimeList") is a website known for its vast database over animes that have been released up until now and it also maintains a list of your animes that you have watched or completed, etc... This is just a subset of its features. It can even do more. 


## Pre-Requisites
---
{: .note }

> Currently Runs only with Windows OS and its native Task Scheduler, Google Calendar for referring the Schedules on a day.

-   Account in [MAL](https://myanimelist.net "MyAnimeList")
-   Must be ok with Initial Setup as it is bit lengthy like creating an API, filling settings, etc...


## Reason for Existence
---

Animes are kinda shows, that we would watch not just one but many, so its important/good to have exact timestamps on its completion.


### Motive

-   I feel its good to have a systematic way of correctly updating your watchlist at regular intervals.

-   While using **PC**, I get stuck and spend a lot of time unnecessarily on some part. The Best way to deal with it is to take a break. And the best way to take a break is to have someone remind you to take a break.

### Watchlist

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
   
This follows things are automated by MAL-Remainder for you.

1.  MAL-Remainder has some Automation Scripts which makes requests with the `MAL Server` through their [API](https://myanimelist.net/apiconfig/references/api/v2) for both fetching the information and updating _(patching)_ information from/onto the server.

2.  Every time you login, It tries to check if tasks were scheduled for today. If not scheduled it schedules based on the events in your `ICalendar File` and then creates the required number of triggers for a Task.


----

[Getting Started](./docs/Getting Started){: .btn .btn-blue}