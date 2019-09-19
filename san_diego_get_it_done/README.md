This example is using an awesome data set out of San Diego called [Get It Done](https://www.sandiego.gov/get-it-done) that is an open data set of non-emergency problems submitted by the community.

#### Data
For this example, we'll be using the `Get It Done Requests year-to-date` csv found [here](https://data.sandiego.gov/datasets/get-it-done-311/)

Download this data as a CSV and use the [file upload](https://www.elastic.co/blog/importing-csv-and-log-data-into-elasticsearch-with-file-data-visualizer) functionality in Kibana to import and ingest a CSV. When in the advanced settings you can use the below mappings and ingest processor to add the location `geo_point`

**Mappings**
```JSON
{
  "case_age_days": {
    "type": "long"
  },
  "case_origin": {
    "type": "keyword"
  },
  "case_record_type": {
    "type": "keyword"
  },
  "comm_plan_code": {
    "type": "long"
  },
  "comm_plan_name": {
    "type": "keyword"
  },
  "council_district": {
    "type": "long"
  },
  "lat": {
    "type": "double"
  },
  "long": {
    "type": "double"
  },
  "park_name": {
    "type": "keyword"
  },
  "public_description": {
    "type": "text"
  },
  "referred": {
    "type": "text"
  },
  "requested_datetime": {
    "type": "date",
    "format": "iso8601"
  },
  "sap_notification_number": {
    "type": "long"
  },
  "service_name": {
    "type": "keyword"
  },
  "service_request_id": {
    "type": "long"
  },
  "service_request_parent_id": {
    "type": "long"
  },
  "status": {
    "type": "keyword"
  },
  "location": {
    "type": "geo_point"
  }
}
```

**Ingest Processor**
```json
{
  "processors": [
    {
      "set": {
        "field": "location",
        "value": "{{lat}},{{long}}"
      }
    }
  ]
}
```

In order to use or create a Cases by County view, you'll need to use the [GeoJSON upload](https://www.elastic.co/guide/en/kibana/current/geojson-upload.html) functionality in the Maps app to ingest `sd.json`.

#### Map
Open up the [saved object management UI](https://www.elastic.co/guide/en/kibana/current/managing-saved-objects.html) and import `get_it_done.ndjson`

You can open the new map under the Maps application or open the dashboard that has the map embedded.

![screenshot](https://github.com/alexfrancoeur/elastic_maps_examples/blob/master/images/get_it_done.gif)
