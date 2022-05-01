---
layout: default
title: Google Calendar
parent: Getting Started
permalink: /docs/Getting Started/google_calendar
nav_order: 3
---

{: .note}
This is the optional section. But it would make this [scheduling feature](../../#automation) possible.

MAL-Remainder requires a URL for `.ics` file. For now I have tested only with [Google Calendar](https://www.google.com/calendar/about/). 


## Why Calendar ?
---

It is easy for us to schedule events in clean UI. and some services like [Google Calendar](https://www.google.com/calendar/about/) also provides notifications for the events.

## Info Used
---

* Refers only the events
* May refer the Event's Description or Summary in future
* Refers only the End time of the event.


Thanks to **[icalevents](https://github.com/jazzband/icalevents)** for providing an easy way to parse events. 

## Connecting Calendar from Google Calendar
---

MAL-Remainder just requires you provide the link for your `ics` calendar.
You may refer the below links for reference.

* [Creating a Calendar](https://support.google.com/calendar/answer/37095?hl=en "Creating a calendar")
* [Making it Public](https://support.google.com/calendar/answer/37083 "Making your calendar public")
* [Refer this website for referring shared link](https://simplify-everything.com/en/blog/2019/09/30/how-to-get-your-secret-address-in-ical-format-on-google-calendar/ "How to get your Secret address in iCal format on Google Calendar")
* ![Public .ics Address](https://storage.googleapis.com/gcs.ireloca.com/simplify-everything/2019/09/561afde5-copy-secret-address-ical.jpg "address of ur public ics file")

----

Now that we have everything required, you can <br>
[Let application know your required details](./feeding_values){: .btn .btn-green .mr-4}

