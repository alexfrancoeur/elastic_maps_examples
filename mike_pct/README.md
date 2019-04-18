#### Data

Download the `snapshots.zip` file, unzip and [follow the documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-snapshots.html) to restore an index. This export was done in 7.0

If you're randomly stumbling upon this example, make sure you read the blog post series for the full story. [Part 1](https://www.elastic.co/blog/hiking-the-pacific-crest-trail-with-the-elastic-stack), [Part 2](https://www.elastic.co/blog/hiking-the-pacific-crest-trail-with-the-elastic-stack-part-2-hitting-1000) and [Part 3](https://www.elastic.co/blog/hiking-the-pacific-crest-trail-with-the-elastic-stack-part-3-mission-complete).

#### Map
Use the [Saved Object API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api-create.html) to create a saved object with the JSON from `mike_pct.json`. Be sure to also import the index pattern and additional saved objects with `lmike_saved_objects.json`

The following curl command should work:

```curl
curl -X POST 'http://localhost:5601/api/saved_objects/map/' -H 'Content-Type: application/json' -H "kbn-xsrf: true" -d "@mike_pct.json"
```
If you are not adding the map to the default space, you'll need to add the space name as part of the POST

```curl
curl -X POST 'http://localhost:5601/s/SPACENAME/api/saved_objects/map/' -H 'Content-Type: application/json' -H "kbn-xsrf: true" -d "@mike_pct.json"
```

![screenshot](https://github.com/alexfrancoeur/elastic_maps_examples/blob/master/images/mike_pct.png)
