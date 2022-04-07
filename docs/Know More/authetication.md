---
layout: default
title: Authentication
parent: API
grand_parent: Know More
nav_order: 1
permalink: /docs/Know More/api/authentication
---

# Authentication
----


After feeding the `Client ID` and `Client Secret` on [Settings Page](../settings). Proceed with Reset Oauth on that page. You will see this. <br><br>

![success oauth](../../../assets/success.jpg "Success Oauth")


{: .note}
Whenever we open Oauth Session, You have maximum of [6 minutes](https://github.com/RahulARanger/MAL-Remainder/blob/c03bdfdb86e2a4b1b9b10138f62e30c64a2ceecd/MAL_Remainder/oauth_responder.py#L111) to respond Else MAL-Remainder cuts off the Session and makes it expired.


{: .attention}
You can either call Reset-Oauth Again to get new Oauth Session and cut off the old ones.


{: .tip}
If sometimes, Oauth Session is stuck for some reason, You can always click on `./close-oauth-session` on the settings.



## Possible Errors
----


{: .error}
Would happen if either `Client ID` or `Client Secret` is invalid <br><br> ![Invalid Client ID or Client Secret](../../assets/error_oauth.jpg "Invalid Client ID or Client Secret")


{: .error}
Time out error for Oauth Session <br><br> ![Time out Error](../../assets/time-out.jpg "time out error")