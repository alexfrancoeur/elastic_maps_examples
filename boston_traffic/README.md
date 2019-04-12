#### Traffic Data
Load up the python script `boston_traffic.py` to with `python boston_traffic.py` to start ingesting fake and real time boston traffic data

#### Map
Use the [Saved Object API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api-create.html) to create a saved object with the JSON from `boston_traffic.json`. Be sure to also import the index pattern saved object `mass_traffic_index_pattern.json`

The following curl command should work:

```curl
curl -X POST 'http://localhost:5601/api/saved_objects/map/' -H 'Content-Type: application/json' -H "kbn-xsrf: true" -d "@boston_traffic.json"
```
If you are not adding the map to the default space, you'll need to add the space name as part of the POST

```curl
curl -X POST 'http://localhost:5601/s/SPACENAME/api/saved_objects/map/' -H 'Content-Type: application/json' -H "kbn-xsrf: true" -d "@boston_traffic.json"
```

![screenshot](https://github.com/alexfrancoeur/elastic_maps_examples/blob/master/images/boston_traffic.png)
