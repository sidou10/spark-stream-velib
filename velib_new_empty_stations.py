#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyspark.streaming import StreamingContext
from pyspark import SparkContext
import json

sc = SparkContext()

t = 5
ssc = StreamingContext(sc, t)

stream = ssc.socketTextStream("velib.behmo.com", 9999)

def updateFunc(new_values, old_state):
    """ old_state is a couple. The first element indicates if the 
    station became empty (meaning that the last recorded value for the 
    number of available bike is null and it was not null in the previous
    states). The second element indicates if there was at least one available 
    bike in the previous state (cf. is_last_nonempty).
    """
    # No new record
    if len(new_values) == 0:
        return None

    # Initialization of old_state
    elif old_state == None:
        return [0, is_last_nonempty(new_values)]

    else: 

        # In the new values of the stream, there was at least one non null 
        # value for the available bikes and the last value is null. In this
        # case, we can say that the station became empty
        if (new_values[-1] == 0) and sum(new_values) > 0:
            return [1, is_last_nonempty(new_values)]

        # All the new values of the stream are null, but there was at least 
        # one available bike in the previous state
        elif sum(new_values) == 0 and old_state[1] == 1:
            return [1, is_last_nonempty(new_values)]

        # The station did not become empty
        else:
            return [0, is_last_nonempty(new_values)]

def is_last_nonempty(new_values):
    """ Return 1 if the last value in the new values (from the current
    DStream) has at least one bike.
    """
    return int(new_values[-1] > 0)


# Print the velib stations that have became empty (every 5 secondss)
stations = stream.map(lambda station: json.loads(station))\
    .map(lambda station: (
        station["contract_name"] + " " + station["name"],
        station["available_bikes"]
    ))\
    .updateStateByKey(updateFunc)\
    .filter(lambda station: station[1][0] == 1)\
    .pprint()
    
ssc.checkpoint("./checkpoint")
ssc.start()
ssc.awaitTermination()