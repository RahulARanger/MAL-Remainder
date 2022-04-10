---
layout: home
title: Introduction
nav_order: 1
permalink: /docs/
---

# Introduction

> MAL-Remainder is an Application that allows you to update the number of episodes that you have on your `watch list` in [MyAnimeList](https://myanimelist.net "MyAnimeList") by regularly reminding you on the basis of events scheduled in [Google Calendar](https://www.google.com/calendar/about/ "Google Calendar")'s [ICalendar File](https://en.wikipedia.org/wiki/ICalendar ".ics file").

---

{: .note }

> Currently Runs only with Windows OS and its native Task Scheduler, Google Calendar for referring the Schedules on a day.

## Pre-Requisites

-   Familiarity with the [MAL](https://myanimelist.net "MyAnimeList")
-   Must be ok with Initial Setup as it is bit lengthy like creating an API, filling settings, etc...

---

## Reason for Existence

> Animes are kinda shows, that we would watch not just one but many, so its important/good to have exact timestamps on its completion.


### Motive

-   Normally, i would visit website once in a week or twice in a month so i will have to update all the animes that i have watched up until now all at once. [I watch short ones like 12-13eps, which i will be able to finish it by a week or so], but that's a bad practice since we are providing **wrong** time stamps.

-   This Remainders motivates me to take a break.

### Status

> MAL's Database contains information about every registered user's interaction over anime which can be labelled as either of the following,

> > -   Completed
> > -   Watching
> > -   Dropped
> > -   On-Hold
> > -   Plan to Watch

{: .comfy }
Most probably, we pick an anime watch it and then complete it.


---

## Automation

This follows things are automated by MAL-Remainder for you.

1.  MAL-Remainder has some Automation Scripts which makes requests with the `MAL Server` through their [API](https://myanimelist.net/apiconfig/references/api/v2) for both fetching the information and updating _(patching)_ information from/onto the server.

2.  Every time you login, It tries to check if tasks were scheduled for today. If not scheduled it finds the events for today from the given `ICalendar File` and then creates the required number of triggers for a Task.


----

[Getting Started](./Getting Started){: .btn .btn-blue}