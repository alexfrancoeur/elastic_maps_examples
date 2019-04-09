This example is from the webinar [Elastic Maps for Geospatial Analysis](https://www.elastic.co/webinars/elastic-maps-for-geospatial-analysis)

#### Mock Data
Add the [index template](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates.html) found in `mappings_filebeat.json` in this directory

Load up the python script `filebeat-ecs.py` to with `python filebeat-ecs.py` to start ingesting fake and randomized suricata logs

#### Map
Use the [Saved Object API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api-create.html) to create a saved object with the JSON from `Suricata_Events_Dark.json`. You will need a `filebeat-*` index pattern.

The following curl command should work:

```curl
curl -X POST 'http://localhost:5601/api/saved_objects/map/' -H 'Content-Type: application/json' -H "kbn-xsrf: true" -d "@Suricata_Events_Dark.json"
```
If you are not adding the map to the default space, you'll need to add the space name as part of the POST

```curl
curl -X POST 'http://localhost:5601/s/SPACENAME/api/saved_objects/map/' -H 'Content-Type: application/json' -H "kbn-xsrf: true" -d "@Suricata_Events_Dark.json"
```

![screenshot](https://github.com/alexfrancoeur/elastic_maps_examples/blob/master/images/elastic_maps_webinar.png)
