# MAL Remainder
[![say_thanks](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg "letting me know you are happy with this application 😄")](https://saythanks.io/to/RahulARanger)

With this application, you can update the number of episodes that you have watched at anytime in [MyAnimeList]("https://myanimelist.net" "MyAnimeList").
But it can also schedule events that can remind to update the episodes So you won't be able to forget to do that.


It uses System's own scheduler to schedule events so when triggered it starts a flask session whereby you can fill the details in the form to reflect in your MyAnimeList Account.

For Scheduling events, It requires `Icalendar file` that could be generated from [Google Calendar](https://www.google.com/calendar/about/ "One of the Web Services that could generate ics file")

For more Information, Please take look over [Documentation](https://rahularanger.github.io/MAL-Remainder).

> **Note:**  Since this application automates things that would require authentication, setup process is a bit lengthy.

## Supported OS
For now,
-   Windows

## APIs Used
-   [MAL API](https://myanimelist.net/apiconfig/references/api/v2)

## Schedulers Used
- Windows's [ScheduledTasks](https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/?view=windowsserver2022-ps) 
