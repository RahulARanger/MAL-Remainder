---
layout: default
title: MAL API
parent: Getting Started
---

# Creating API

---

We need MyAnimeList API in order to communicate with MAL Server. for that follow the steps from this [blog](https://myanimelist.net/blog.php?eid=835707) but make sure to read the below points side by side.

## Fixed parameters in the form

There are certain things to note while creating API

-   make sure to select App Type as `web`
-   App Redirect URL as http://**{host}**:**{port}**

{: .warning}
Don't share the Client ID and Client Secret
