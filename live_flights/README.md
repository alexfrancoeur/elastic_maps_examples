#### Airport Data
Load up the python script `airport_ingest.py` and update line 68 `df = pandas.read_csv('PATH_TO_CSV/airports.csv', na_values=[''])` to have the correct path to the CSV. Then run `python airport_ingest.py` to start ingesting fake and static airport data. This is a one time ingest.

#### Historic Routes Data
Load up the python script `routes.py` and update line 59 `with open('PATH_TO_ROUTES/routes.geojson') as f:` to have the correct path to the `routes.geojson` file. Then run `python routes.py` to start ingesting fake and static historical routes. This is a one time ingest.

#### Live Flights Data
Load up the python script `live_flights.py` and run `python live_flights.py` to start ingesting live flights in the air

#### Map
Use the [Saved Object API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api-create.html) to create a saved object with the JSON from `flight_demo.json`. Be sure to also import the index pattern saved object `live_flights_index_pattern.json`

The following curl command should work:

```curl
curl -X POST 'http://localhost:5601/api/saved_objects/map/' -H 'Content-Type: application/json' -H "kbn-xsrf: true" -d "@flight_demo.json"
```
If you are not adding the map to the default space, you'll need to add the space name as part of the POST

```curl
curl -X POST 'http://localhost:5601/s/SPACENAME/api/saved_objects/map/' -H 'Content-Type: application/json' -H "kbn-xsrf: true" -d "@bflight_demo.json"
```

![screenshot](https://github.com/alexfrancoeur/elastic_maps_examples/blob/master/images/live_flights.png)
