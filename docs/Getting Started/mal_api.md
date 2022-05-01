---
layout: default
title: MAL API
parent: Getting Started
permalink: /docs/Getting Started/mal_api
nav_order: 2
---

# Creating ID in MAL API
____

We will need to create an **ID** in MyAnimeList API in order to communicate with MAL Server. This process is similar to and referred from this [blog](https://myanimelist.net/blog.php?eid=835707#:~:text=Step%200%20%2D%20Register%20your%20application).

### Fixed parameters in the form

There are certain things to note while creating API

-   Make sure to select `App Type` as `web`
-   `App Redirect URL` as http://**{host}**:**{port}**//save.

 _I would recommend to use http://localhost:6969. You can use any port but try to use localhost._

{: .note}
"//save" shouldn't be written as "/save" and the protocol `http` is used and not `https`


Other than `App type` and `App Redirect URL`, you can fill the rest with your own values.


## Steps
----

1. Profile -> Account Settings
2. you will see the below page, then go to _API_ tab.
3. Then do notice this 
> ![Creating API ID](../../assets/create.jpg "Creating API ID")

4. Then just look at the rest of the details _for reference._
> ![Rest of the details](../../assets/rest_details.jpg "Rest of the details")
5. Read & Accept the License Agreement


### Editing an app
---

In case if you already have any `web` type app, just make sure to just **append** App Redirect url in the format mentioned above.


{: .note}

Make sure to note `Client ID` and `Client Secret` Values. <br><br> ![Note](../../assets/note.jpg "Note those values")
