import urllib2
import xmltodict
import pprint
import json
import xml.etree.ElementTree as ET
import elasticsearch
from datetime import datetime
import time

# define pretty printer
def my_safe_repr(object, context, maxlevels, level):
    typ = pprint._type(object)
    if typ is unicode:
        object = str(object)
    return pprint._safe_repr(object, context, maxlevels, level)

printer = pprint.PrettyPrinter()
printer.format = my_safe_repr

# define mapping
mapping = {
        "mappings": {
            "_doc": {
                "properties": {
                    "LastUpdated": {
                     "type": "date"
                    },
                    "Destination": {
                     "type": "keyword"
                    },
                    "Direction": {
                      "type": "keyword"
                    },
                    "FreeFlow": {
                      "type": "float"
                    },
                    "Highway": {
                      "type": "keyword"
                    },
                    "Origin": {
                      "type": "keyword"
                    },
                    "PairID": {
                      "type": "keyword"
                    },
                    "Route": {
                      "type": "geo_shape"
                    },
                    "Speed": {
                      "type": "float"
                    },
                    "Stale": {
                      "type": "keyword"
                    },
                    "Status": {
                      "type": "keyword"
                    },
                    "Title": {
                      "type": "keyword"
                    },
                    "TravelTime": {
                      "type": "float"
                    },
                    "dnid": {
                      "type": "keyword"
                    },
                    "onid": {
                      "type": "keyword"
                    }
                }
            }
        }
}

# load Elasticsearch
try:
    es = elasticsearch.Elasticsearch(["localhost"],port=9200)
except:
    print "unable to es"

f = open("mass_traffic.txt", "w")

# create index mass_traffic
try:
    response = es.indices.create(index="mass_traffic",body=mapping, ignore=400)
except Exception as e:
    print(e)



#loop through data, build JSON and ingest
while True:
    try:
        # load massdot xml
        massdot_req = urllib2.Request('https://dotfeeds.state.ma.us/api/RTTMDeveloperFeed/Index', headers={'Accept':'application/xml'})
        massdot_file = urllib2.urlopen(massdot_req)
        massdot_data = massdot_file.read()
        massdot_data = massdot_data.encode('utf16')
        massdot_file.close()

        #convert to JSON
        massdot_json = json.loads(json.dumps(xmltodict.parse(massdot_data)))

        for pairdata in massdot_json["btdata"]["TRAVELDATA"]["PAIRDATA"]:
            try:
                #printer.pprint(pairdata)
                new_body = {}
                if massdot_json["btdata"]["TRAVELDATA"]["LastUpdated"] is not None:
                    datetime_object = datetime.strptime(massdot_json["btdata"]["TRAVELDATA"]["LastUpdated"].replace(' GMT',''), '%b-%d-%Y %H:%M:%S')
                    new_body["LastUpdated"] = datetime_object.strftime('%Y-%m-%dT%H:%M:%S')
                if pairdata['PairID'] is not None: new_body["PairID"] = pairdata['PairID']
                if pairdata['Destination'] is not None: new_body["Destination"] = pairdata['Destination']
                if pairdata['FreeFlow'] is not None: new_body["FreeFlow"] = float(pairdata['FreeFlow'])
                if pairdata['Highway'] is not None: new_body["Highway"] = pairdata['Highway']
                if pairdata['Origin'] is not None: new_body["Origin"] = pairdata['Origin']
                if pairdata['Speed'] is not None: new_body["Speed"] = float(pairdata['Speed'])
                if pairdata['Stale'] is not None: new_body["Stale"] = pairdata['Stale']
                if pairdata['Status'] is not None: new_body["Status"] = pairdata['Status']
                if pairdata['Title'] is not None: new_body["Title"] = pairdata['Title']
                if pairdata['TravelTime'] is not None: new_body["TravelTime"] = float(pairdata['TravelTime'])
                if pairdata['dnid'] is not None: new_body["dnid"] = pairdata['dnid']
                if pairdata['onid'] is not None: new_body["onid"] = pairdata['onid']
                if (pairdata['Routes'] is not None and pairdata['Routes']['Route'] is not None):
                    type = 'LineString'
                    coordinates = []
                    for routes in pairdata['Routes']['Route']:
                        coordinates.append([float(routes['lon']),float(routes['lat'])])
                    new_body["Route"] = {"type": type, "coordinates": coordinates}

                #index and keep history
                #id = "{0}-{1}".format(new_body["PairID"],new_body["LastUpdated"])
                #index for most recent status
                id = new_body["PairID"]
                #printer.pprint(id)
                #printer.pprint(new_body)
                res = es.index(index="mass_traffic", doc_type="_doc", id=id, body=new_body)
                print "------------------------------------------"
                printer.pprint(res['result'])
            except Exception as e:
                print "------------------------------------------"
                print "unable to index in elasticsearch"
                print "------------------------------------------"
                error = "{0}: {1}".format(id,e)
                print error
                print "------------------------------------------"
                f = open("mass_traffic.txt", "a")
                f.write(error)
                f.write("\n")
                f.close()
        print "all done, starting again soon"
        time.sleep(15)
    except:
        print "weird, error; starting again soon"
        time.sleep(60)
