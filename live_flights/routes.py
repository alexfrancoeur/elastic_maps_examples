#!/usr/bin/python
import json
import urllib,urllib2
import elasticsearch
import pprint
import time
import geocoder
import googlemaps
import datetime
from dateutil import relativedelta
import pandas

try:
    es = elasticsearch.Elasticsearch(["localhost"],port=9200)
except:
    print "unable to es"

mapping = {
        "mappings": {
            "doc": {
                "properties": {
                    "airline": {
                     "type": "keyword"
                    },
                    "airline_id": {
                     "type": "long"
                    },
                    "location": {
                      "type": "geo_shape"
                    },
                    "dst": {
                      "type": "keyword"
                    },
                    "dst_id": {
                      "type": "long"
                    },
                    "equipment": {
                      "type": "keyword"
                    },
                    "codeshre": {
                      "type": "keyword"
                    },
                    "src": {
                      "type": "keyword"
                    },
                    "src_id": {
                      "type": "long"
                    },
                    "stops": {
                      "type": "integer"
                    }
                }
            }
        }
}
es.indices.create(index="routes",body=mapping, ignore=400)
f = open("routes.txt", "w")

with open('PATH_TO_ROUTES/routes.geojson') as f:
    data = json.load(f)

for feature in data['features']:
    try:
        new_body = {}
        new_body["airline"] = feature['properties']['airline'] if feature['properties']['airline'] is not None else ''
        new_body["airline_id"] = feature['properties']['airline_id'] if feature['properties']['airline_id'] is not None else ''
        new_body["codeshare"] = feature['properties']['codeshare'] if feature['properties']['codeshare'] is not None else ''
        new_body["dst"] = feature['properties']['dst'] if feature['properties']['dst'] is not None else ''
        new_body["dst_id"] = feature['properties']['dst_id'] if feature['properties']['dst_id'] is not None else ''
        new_body["equipment"] = feature['properties']['equipment'] if feature['properties']['equipment'] is not None else ''
        new_body["src"] = feature['properties']['src'] if feature['properties']['src'] is not None else ''
        new_body["src_id"] = feature['properties']['src_id'] if feature['properties']['src_id'] is not None else ''
        new_body["stops"] = feature['properties']['stops'] if feature['properties']['stops'] is not None else ''
        if (feature['geometry']['type'] is not None or feature['geometry']['coordinates'] is not None):
            type = feature['geometry']['type']
            coordinates = feature['geometry']['coordinates']
            new_body["location"] = {"type": type, "coordinates": coordinates}

        pprint.pprint(new_body)
        res = es.index(index="routes", doc_type="doc", id=new_body["airline_id"]+new_body["src_id"]+new_body["dst_id"], body=new_body)
        print "------------------------------------------"
        pprint.pprint(res['result'])
    except:
        print "------------------------------------------"
        print "unable to index in elasticsearch"
        print "------------------------------------------"
        error = "{0} : {1}".format(new_body["airline_id"],new_body["src_id"])
        print error
        print "------------------------------------------"
        f = open("routes.txt", "a")
        f.write(error)
        f.write("\n")
        f.close()
