---
layout: home
title: Introduction
nav_order: 1
---

# Introduction

> MAL-Remainder is an Application that allows you to update the number of episodes that you have on your `watch list` in [MAL]("https://myanimelist.net" "MyAnimeList") by regularly reminding you on the basis of events scheduled in [Google Calendar](https://www.google.com/calendar/about/)'s [ICalendar File](https://en.wikipedia.org/wiki/ICalendar ".ics file").

---

{: .note }

> Currently Tested only with Windows OS and its native Task Scheduler, Google Calendar for referring the Schedules on a day.

## Pre-Requisites

-   Familiarity with the [MAL](https://myanimelist.net)

>

---

## Reason for Existence

> Animes are kinda shows, that we would watch not just one but many, so its important/good to have exact timestamps on its completion.

### Motive

-   Normally, i would visit website once in a week or twice in a month so i have to update all the animes that i have watched up until now all at once. [I watch short ones like 12-13eps, which i will be able to finish it by a week or so], but that's a bad practice since we are providing wrong time stamps.

-   This Remainders motivates me to take a break.

### Status

> MAL's Database contains information about every registered user's interaction over anime which can be labelled as either of the following,

> > -   Completed
> > -   Watching
> > -   Dropped
> > -   On-Hold
> > -   Plan to Watch

> So when we pick an anime we initially set any of the above status, most probably we would start with **Watching** and would end up with other choices; say if we are bored of it, we drop it or maybe you enjoyed the show till the end, so we mark it as **Completed**.

{: .comfy }
Here the common / most observed pattern is that, we pick an anime watch it and then complete it. But for updating we either forget it or ur lazy to do so.

---

## Automation

{: .comfy}

So this Application tries to automatically update the episodes [_and status indirectly_] by reminding you on some custom schedule.

1.  MAL-Remainder has some Automation Scripts which makes requests with the `MAL Server` through their [API](https://myanimelist.net/apiconfig/references/api/v2) for both fetching the information and updating _(patching)_ information from/onto the server.

2.  And then it reminds you by creating a Task which is triggered based on your `ICalendar File`.

3.  And every time once you login, It tries to check if tasks were scheduled for today, if not it does step 1.
