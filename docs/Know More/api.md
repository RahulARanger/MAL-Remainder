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

## Authorization
----

Authenticated User with their Client ID and Client Secret can get `Tokens` which can be used for fetching or updating details on MyAnimeList Server. _It is one of the process done while `Resetting Oauth`_. 

You would receive `Access Tokens` and `Refresh Tokens`. `Access Tokens` could expire in [31 days](https://myanimelist.net/blog.php?eid=835707#:~:text=a1b2c3d4e5...%22%2C%0A%20%20%20%20%22refresh_token%22%3A%20%22z9y8x7w6u5...%22%0A%7D-,IMPORTANT,-%3A%20currently%2C%20the%20lifetime).

## Possible Errors
----


{: .error}
Would happen if either `Client ID` or `Client Secret` is invalid or if your port doesn't match with the value of your registered API  <br><br> ![Invalid Client ID or Client Secret](../../assets/error_oauth.jpg "Invalid Client ID or Client Secret")


{: .error}
Time out error for Oauth Session <br><br> ![Time out Error](../../assets/time-out.jpg "time out error")

### Alerts

{: .highlight}
Happens if you decline the OAuth or if used invalid host value. <br><br> ![Wrong Host Error](../../assets/bad_errors.jpg "Wrong Host Error")



### Invalid Access Tokens or Refresh Tokens

In-Case if you face any Error regarding `Invalid Tokens` you can manually `Reset Tokens`. 
 The alert is similar to ones seen in [here](#alerts). MAL-Remainder alerts you with either `Failed to update your profile` in [Settings](./settings) or `Invalid Token` in [Update - Page](./UpdateList).

Application tries to refresh tokens by auto if they are near to expiration but You can also `Refresh Tokens` in [Settings](./Settings) if refresh token is valid else you would need to fetch them using `Reset Tokens`

