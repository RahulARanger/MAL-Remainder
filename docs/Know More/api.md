---
layout: default
title: API
parent: Know More
nav_order: 1
permalink: /docs/Know More/api
---

Application tries to modify or access the data in your account using the [MAL API<sup>v2</sup>](https://myanimelist.net/apiconfig/references/api/v2).

MyAnimeList API uses OAuth 2.0 for authentication and authorization of the users. So one of our first steps is to get authorized by the MAL server.

## Process
- [Authentication](#authentication)
- [Authorization](#authorization)
- [Refreshing Tokens](#refreshing-tokens)


## Keywords
____

{: .important}
MAL uses [OAuth 2.0](https://oauth.net/2/) in order to authenticate and then authorize the user. So it's important to know certain keywords.

### `Client ID` and `Client Secret`

> These two are unique and are very important, make sure to specify them without any mistake. Wrong Values will led failed authentication.

### `Access` Tokens

> These Tokens are given to authorized users. Using this tokens one can communicate with the Server.

### `Expiry Date` and `Refresh Token`

> `Expiry Date` is the date when the `Access` Token will expire. and `Refresh Token` is used for refreshing the `Access token`. 



## Authentication
----


After feeding the `Client ID` and `Client Secret` on [Settings Page](./settings). Proceed with Reset Oauth on that page. You will see this. <br><br>

![success oauth](../../assets/success.jpg "Success Oauth")


{: .note}
Whenever we open Oauth Session, You have maximum of [6 minutes](https://github.com/RahulARanger/MAL-Remainder/blob/c03bdfdb86e2a4b1b9b10138f62e30c64a2ceecd/MAL_Remainder/oauth_responder.py#L111) to respond else MAL-Remainder cuts off the Session and makes it expired.


{: .attention}
You can either call `Reset-Oauth` Again to get new Oauth Session and cut off the old ones or go with `./close-oauth-session` on settings page to close any session if available.


{: .tip}
If sometimes, Oauth Session is stuck for some reason, You can always click on `./close-oauth-session` on the settings.



### Possible Errors
----


{: .error}
Would happen if either `Client ID` or `Client Secret` is invalid or if your port doesn't match with the value of your registered API  <br><br> ![Invalid Client ID or Client Secret](../../assets/error_oauth.jpg "Invalid Client ID or Client Secret")


{: .error}
Time out error for Oauth Session <br><br> ![Time out Error](../../assets/time-out.jpg "time out error")

### Alerts

{: .highlight}
Happens if you decline the OAuth or if used invalid host value. <br><br> ![Wrong Host Error](../../../assets/bad_errors.jpg "Wrong Host Error")


## Authorization
----

Authenticated User with their Client ID and Client Secret can get `Tokens` for getting an access in database. It is one os the process done while `Resetting Oauth`. 


You would receive `Access Tokens` and `Refresh Tokens`. `Access Tokens` could expire in [31 days](https://myanimelist.net/blog.php?eid=835707#:~:text=a1b2c3d4e5...%22%2C%0A%20%20%20%20%22refresh_token%22%3A%20%22z9y8x7w6u5...%22%0A%7D-,IMPORTANT,-%3A%20currently%2C%20the%20lifetime).


### Invalid Access Tokens or Refresh Tokens
---
In-Case if you face any Error regarding `Invalid Token` you can manually `Reset Tokens`. The alert is similar to ones seen in [here](#alerts). MAL-Remainder alerts you with either `Failed to update your profile` in settings page or `Invalid Token` in Update Page.


### Refreshing Tokens
---

If your Access Tokens is about to get expired, You would not be able to communicate with the server so if your **Refresh Token is valid**.

Application tries to refresh the tokens without Oauth verification which is a _Human Task_, You can also manually `Refresh Tokens` from settings page.

It updates the `Expiry Time` _see in the footer of your settings page_. 

