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
            "_doc": {
                "properties": {
                    "airport_id": {
                     "type": "keyword"
                    },
                    "name": {
                     "type": "keyword"
                    },
                    "location": {
                      "type": "geo_point"
                    },
                    "city": {
                      "type": "keyword"
                    },
                    "country": {
                      "type": "keyword"
                    },
                    "IATA": {
                      "type": "keyword"
                    },
                    "ICAO": {
                      "type": "keyword"
                    },
                    "altitude": {
                      "type": "long"
                    },
                    "timezone": {
                      "type": "integer"
                    },
                    "dst": {
                      "type": "keyword"
                    },
                    "tz_database": {
                      "type": "keyword"
                    },
                    "type": {
                      "type": "keyword"
                    },
                    "source": {
                      "type": "keyword"
                    }
                }
            }
        }
}
es.indices.create(index="airports",body=mapping, ignore=400)
f = open("airports.txt", "w")

df = pandas.read_csv('PATH_TO_CSV/airports.csv', na_values=[''])
total_rows = df.count
current_row = 0
while current_row <= total_rows:
    try:
        new_body = {}
        new_body["airport_id"] = df["airport_id"][current_row] if pandas.isnull(df["airport_id"][current_row]) == False else ''
        new_body["name"] = df["name"][current_row] if pandas.isnull(df["name"][current_row]) == False else ''
        new_body["city"] = df["city"][current_row] if pandas.isnull(df["city"][current_row]) == False else ''
        new_body["country"] = df["country"][current_row] if pandas.isnull(df["country"][current_row]) == False else ''
        new_body["IATA"] = df["IATA"][current_row] if pandas.isnull(df["IATA"][current_row]) == False else ''
        new_body["ICAO"] = df["ICAO"][current_row] if pandas.isnull(df["ICAO"][current_row]) == False else ''
        lat = df["latitude"][current_row]
        lon = df["longitude"][current_row]
        new_body["location"] = { "lat": lat, "lon": lon }
        new_body["dst"] = df["dst"][current_row] if pandas.isnull(df["dst"][current_row]) == False else ''
        new_body["tz_database"] = df["tz_database"][current_row] if pandas.isnull(df["tz_database"][current_row]) == False else ''
        new_body["type"] = df["type"][current_row] if pandas.isnull(df["type"][current_row]) == False else ''
        new_body["source"] = df["source"][current_row] if pandas.isnull(df["source"][current_row]) == False else ''
        new_body["altitude"] = df["altitude"][current_row] if pandas.isnull(df["altitude"][current_row]) == False else 0
        new_body["timezone"] = df["timezone"][current_row] if pandas.isnull(df["timezone"][current_row]) == False else 0

        pprint.pprint(new_body)
        res = es.index(index="airports", doc_type="_doc", id=new_body["airport_id"], body=new_body)
        print "------------------------------------------"
        pprint.pprint(res['result'])
        print "------------------------------------------"
        print current_row
        print "------------------------------------------"
        current_row += 1
        #time.sleep(0.1)
    except:
        print "------------------------------------------"
        print "unable to index in elasticsearch"
        print "------------------------------------------"
        error = "{0} : {1}".format(current_row,new_body["airport_id"])
        print error
        print "------------------------------------------"
        f = open("airports.txt", "a")
        f.write(error)
        f.write("\n")
        f.close()
        current_row += 1
