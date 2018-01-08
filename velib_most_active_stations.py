#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyspark.streaming import StreamingContext
from pyspark import SparkContext
import json

sc = SparkContext()

window_length = 300
sliding_interval = 60

# Batch interval chosen equal to the sliding interval
t = 60

ssc = StreamingContext(sc, t)

stream = ssc.socketTextStream("velib.behmo.com", 9999)

def reducer(x, y):
    """ Returns a couple (a,b)
    a is the cumulated absolute difference
    b is the number of available bikes in the latest record in the reducer (y)
    """
    # x[1] == 0 corresponds to the first record for a given station
    if x[1] == 0:
        return (abs(y[0]-x[0]), y[0])
    else:
        return (abs(y[0]-x[1]) + x[0], y[0])

stations = stream.map(lambda station: json.loads(station))\
    .map(lambda station: (
        station["contract_name"] + " " + station["name"],
        (station["available_bikes"], 0) # 0 arbitrary value for the initialization
        # Value of (key, value) is a couple
    ))\
    .reduceByKeyAndWindow(lambda x, y: reducer(x, y), window_length, sliding_interval)\
    .transform(lambda rdd: rdd.sortBy(lambda station: station[1][0], ascending=False))\
    .pprint()

ssc.checkpoint("./checkpoint")
ssc.start()
ssc.awaitTermination()