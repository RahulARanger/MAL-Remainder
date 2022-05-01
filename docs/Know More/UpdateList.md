---
layout: default
title: UpdateList
parent: Know More
permalink: /docs/Know More/UpdateList
nav_order: 4
---

This is how UpdateList could look like 
<br>

![UpdateList](../../../assets/update_list.jpg "UpdateList Page")


## Options
---

Before reaching this page, Application fetches all the animes in your watch-list and sets them as options in select box _(dark orange box)_.

{: .note}
These options are sorted by the anime which was updated at latest.(`list_updated_at`)

## Numbers
---

You can see those numbers in the box,  it is of following order:
1. No of Episodes you have completed before.
2. No. of Episodes you have watched for today _connected with slider_.
3. Total Number of Episodes.

## Updating List
---

You can go with `update` button.

{: .note}
Negative values are allowed. It just decreases the number of episodes you have watched before.


{: .highlight} 
If total episodes watched == Total Number of episodes, then it will change the status from `watching` to `Completed`.


## Ensure
---

Normally one would use route `/` that is `http:{host}:{port}/` but there's a Optional route which is `/ensure` which ensures and then opens this page like it checks for the expiration date of the `access tokens`.

## Possible Errors
---

* You wouldn't be able to reach this route `/` or `/ensure` if your credentials were wrong which even includes `access token`.

If you have reached this page, most probably you wouldn't face any issue other than connection error due to network issue if happens.


