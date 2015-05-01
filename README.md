MediaCloud GeoTag Labeller
==========================

This script go trought the MediaCloud geographic tag set and labels all the tags with 
readable labels and descriptions.  We need to do this because tags are instantiated as needed, 
without labels nor descriptions.

Installation
------------

First install the [MediaCloud API client library](https://github.com/c4fcm/MediaCloud-API-Client).
Then install these python dependencies:

```
pip install -r requirements.pip
```

Now copy `settings.config.sample` to `settings.config` and be sure to fill in these properties: 
* mediacloud.key
* medialcoud.geo_tag_sets_id

Use
---

Simply run `label-geo-tags.py` to label another N tags from the tag set.  It keeps track of the last 
labelled tag for you, so can run this on cron to label new tags as they are added to the set.
