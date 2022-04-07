---
layout: default
title: API
parent: Know More
has_children: true
nav_order: 2
permalink: /docs/Know More/api
---

Application tries to modify or access the data in your account using the [MAL API<sup>v2</sup>](https://myanimelist.net/apiconfig/references/api/v2).

MyAnimeList API uses OAuth 2.0 for authentication and authorization of the users. So one of our first steps is to get authorized by the MAL server.

## Process
- Authetication
- Authorization
- Refreshing Tokens


## Keywords
____

{: .important}
MAL uses OAuth 2.0 in order to authenticate and then authorize the user. So it's important to know certain keywords.

### `Client ID` and `Client Secret`

> These two are unique and very important, make sure to specify them without any mistake. Wrong Values will led failed authentication.

### `Access` Tokens

> These Tokens are given to authorized users. Using this tokens one can communicate with the Server.

### `Expiry Date` and `Refresh Token`

> `Expiry Date` is the date when the `Access` Token will expire. and `Refresh Token` is used for refreshing the `Access token`. 