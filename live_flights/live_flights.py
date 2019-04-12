import json
import urllib,urllib2
import elasticsearch
import pprint
import time
import datetime
from dateutil import relativedelta
from opensky_api import OpenSkyApi
from pytz import timezone

try:
    es = elasticsearch.Elasticsearch(["localhost"],port=9200)
except:
    print "unable to load es"

mapping = {
        "mappings": {
            #"_doc": {
                "properties": {
                    "icao24": {
                     "type": "keyword"
                    },
                    "callsign": {
                     "type": "keyword"
                    },
                    "location": {
                      "type": "geo_point"
                    },
                    "time_position": {
                      "type": "date"
                    },
                    "last_contact": {
                      "type": "date"
                    },
                    "@timestamp": {
                      "type": "date"
                    },
                    "baro_altitude": {
                      "type": "float"
                    },
                    "on_ground": {
                      "type": "boolean"
                    },
                    "velocity": {
                      "type": "float"
                    },
                    "vertical_rate": {
                      "type": "float"
                    },
                    "true_track": {
                      "type": "float"
                    },
                    "geo_altitude": {
                      "type": "float"
                    },
                    "squawk": {
                      "type": "keyword"
                    },
                    "spi": {
                      "type": "boolean"
                    },
                    "position_source": {
                      "type": "integer"
                    }
            }
        #}
    }
}
try:
    es.indices.create(index="flight_tracking",body=mapping, ignore=400)
    f = open("flight_tracking.txt", "w")
except Exception as e:
    print e

while True:
    try:
        api = OpenSkyApi()
        s = api.get_states()
        for s in s.states:
            try:
                new_body = {}
                if s.icao24 is not None : new_body["icao24"] = s.icao24
                if s.callsign is not None : new_body["callsign"] = s.callsign
                if s.origin_country is not None : new_body["origin_country"] = s.origin_country
                if s.time_position is not None : new_body["time_position"] = s.time_position*1000
                if s.last_contact is not None : new_body["last_contact"] = s.last_contact*1000
                if (s.longitude is not None and s.latitude is not None) : new_body["location"] = { "lat": s.latitude, "lon": s.longitude }
                if s.geo_altitude is not None : new_body["geo_altitude"] = s.geo_altitude
                on_ground_str = "{0}".format(s.on_ground)
                new_body["on_ground"] = on_ground_str.lower()
                if s.velocity is not None : new_body["velocity"] = s.velocity
                if s.heading is not None : new_body["heading"] = s.heading
                if s.vertical_rate is not None : new_body["vertical_rate"] = s.vertical_rate
                if s.baro_altitude is not None : new_body["baro_altitude"] = s.baro_altitude
                if s.squawk is not None : new_body["squawk"] = s.squawk
                spi_str = "{0}".format(s.spi)
                new_body["spi"] = spi_str.lower()
                if s.position_source is not None : new_body["position_source"] = s.position_source
                new_body["@timestamp"] = int(round(time.time() * 1000))

                #pprint.pprint(new_body)
                res = es.index(index="flight_tracking", doc_type="_doc", id=new_body["icao24"], body=new_body)
                print "------------------------------------------"
                pprint.pprint("{0}:{1}".format(new_body["icao24"],new_body["@timestamp"]))
                pprint.pprint("flight tracking - {0}".format(res['result']))
            except:
                print "------------------------------------------"
                print "unable to index in elasticsearch"
                print "------------------------------------------"
                error = s
                print error
                print "------------------------------------------"
                f = open("flight_tracking.txt", "a")
                f.write(error)
                f.write("\n")
                f.close()
    except:
        print "all done, starting again soon"
        time.sleep(60)
