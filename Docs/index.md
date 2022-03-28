---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
title: Introduction
---

# Introduction

> MAL-Remainder is an Application that allows you to update the number of episodes that you have on your `watch list` in [MAL](https://myanimelist.net) by regularly reminding you on the basis of events scheduled in [Google Calendar](https://www.google.com/calendar/about/) or more precisely [ICalendar File](https://en.wikipedia.org/wiki/ICalendar)<sub>`.ics`</sub>.

---

{: .note }
Do not blah blah blah...

**Currently tested with only Windows OS and it's Task Scheduler and Google Calendar to schedule events**

## Pre-Requisites

-   Familiarity with the [MAL](https://myanimelist.net)

---

## Reason for Existence

> Animes are kinda shows, that we would watch not just one but many, so its important/good to have exact timestamps on its completion.

### Motive

> Normally, i would visit website once in a week or twice in a month so i have to update all the animes [I watch short ones like 12-13eps, which i will be able to finish it by a week or so] at once, but that's a bad practice since we are providing wrong time stamps.

### Status

> MAL maintains an animelist for every user, so each and every anime that we have (/_shown_) interest on, can have various status:

> > -   Completed
> > -   Watching
> > -   Dropped
> > -   On-Hold
> > -   Plan to Watch

> So when we pick an anime we initially set any of the above status, most probably we would start with **Watching** and would end up with other choices; say if we are bored of it, we drop it or maybe you enjoyed the show till the end, so we mark it completed.

Here the common/ most observed pattern is that we pick an anime watch it and then complete it. But for updating we either forget it or

---

## Automation

1.  MAL-Remainder has some Automation Scripts which makes requests with the `MAL Server` through their [API](https://myanimelist.net/apiconfig/references/api/v2) for both fetching the information and updating _(patching)_ information from/onto the server.

2.  But before, fetching Application needs to parse the `ICalendar File` and fetch the events from it. for that, [ICalEvents](https://github.com/jazzband/icalevents) made it possible.

3.  This step is OS-Specific, where we interact with the system's scheduler, by registering events for every time we Reschedule we request, it also deletes out-dated tasks [tasks made from the old calendar] to replace with the new ones.
