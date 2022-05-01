---
layout: default
title: Data
nav_order: 6
permalink: /docs/data/
---


This section is about the `data.csv` that we can get from [settings](). It contains the recorded data from the previous polls.

{: .note}
Data that was recorded, is never stored in cloud or sent to any server. so you must try to save this data like before un-installation. Setup tries its best to warn you in dire situations.


## Sample Structure
---

| id   | name       | up_until | watched | total | genres                           | rating | score | rank | popularity | duration | updated          |
|------|------------|----------|---------|-------|----------------------------------|--------|-------|------|------------|----------|------------------|
| 6702 | Fairy Tail | 113      | 1       | 175   | Action,Adventure,Fantasy,Shounen | pg_13  | 7.59  | 1367 | 44         | 1484     | 2022-04-30 09:30 |
| 6702 | Fairy Tail | 114      | 1       | 175   | Action,Adventure,Fantasy,Shounen | pg_13  | 7.59  | 1367 | 45         | 1484     |2022-04-30 09:45 |
| 6702 | Fairy Tail | 115      | 3       | 175   | Action,Adventure,Fantasy,Shounen | pg_13  | 7.59  | 1367 | 45         | 1484     | 2022-05-01 01:45 | 


## Variables
---

* #### id `<str>`

    ID given to the anime by [MyAnimeList](https://myanimelist.net)

* #### name  `<str>`

    Name of the Anime

* #### up_until `<int>`  

    Number of Episodes that you have watched before

* #### watched `<int>`

    Asked to update this number of episodes.

* #### total `<int>`

    Total Number of Episodes of that anime.

* #### genres `<str>`

    Comma separated genres that anime belongs to.

* #### rating `<str>`

    age rate (e.g. pg_13)

* #### score `<float>`

    average score given to this anime by the users on the scale 1-10.

* #### rank `<int>`

    position based in the score. 

* #### popularity `<int>`

    position based in the the number of users who have added the anime to their list. (e.g 39)

* #### duration `<int>`

    Average Duration of the anime in seconds.

* #### updated `<datetime>`

    Timestamp for this request.


## Tidying
---

This structure is untidy and has many repetitions. Try to tidy this data.

you can refer some script like this.


```python
import pandas
import pathlib
raw_file = pathlib.Path(...)
...

raw_data = pandas.read_csv(raw_file, index_col=False)
user_data = raw_data[["id", "up_until", "watched", "updated"]]
animes_data = raw_data.groupby("id").last()[
    ["name", "total", "genres", "rating", "score", "rank", "popularity", "duration"]
]
user_data.to_csv(..., index=False)
animes_data.to_csv(..., index=False)

# make sure to fill ... with necessary paths
# if you find any other simple way to tidy this data, please let me know.
```