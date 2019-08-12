This example is from the webinar [Elastic Maps for Geospatial Analysis](https://www.elastic.co/webinars/elastic-maps-for-geospatial-analysis)

**Note, this has been updated with additional saved objects and instructions for Kibana 7.3 on August 12, 2019**

#### Mock Data
Add the [index template](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates.html) found in `mappings_filebeat.json` in this directory

Load up the python script `filebeat-ecs.py` with `python filebeat-ecs.py` to start ingesting fake and randomized suricata logs

#### Map
Open up the [saved object management UI](https://www.elastic.co/guide/en/kibana/current/managing-saved-objects.html) and import `suricata_events.ndjson`

You can open the new map under the Maps application or open the dashboard that has the map embedded.

![screenshot](https://github.com/alexfrancoeur/elastic_maps_examples/blob/master/images/suricata_maps.gif)
