#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyspark.streaming import StreamingContext
from pyspark import SparkContext
import json

sc = SparkContext()

t = 5
ssc = StreamingContext(sc, t)

stream = ssc.socketTextStream("velib.behmo.com", 9999)

# Print the empty velib stations (every 5 seconds)
stations = stream.map(lambda station: json.loads(station))\
    .map(lambda station: (
        station["contract_name"] + " " + station["name"],
        station["available_bikes"]
    ))\
    .filter(lambda station: station[1] == 0)\
    .pprint()

ssc.checkpoint("./checkpoint")
ssc.start()
ssc.awaitTermination()