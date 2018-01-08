# velib-stations-streaming

[JCDecaux](https://developer.jcdecaux.com/#/home)'s self-service bicycles activity across various cities is open and available [here](http://velib.behmo.com/). The data looks like the following:

```json
{"number":9087,
"name":"9087-MAZARGUES",
"address":"MAZARGUES - ROND POINT DE MAZARGUES (OBELISQUE)",
"position":{"lat":43.250903869637334,"lng":5.403244616491982},
"banking":true,
"bonus":false,
"status":"OPEN",
"contract_name":"Marseille",
"bike_stands":21,
"available_bike_stands":14,
"available_bikes":7,
"last_update":1515237277000}
```
 Using Spark Streaming, we have computed a few live metrics:
 
 1.  In ```velib_empty_stations.py```, the empty velib stations (displayed every 5s).
 The *contract_name* and *name* are shown in the output along with *available_bikes*:
 ```
 -------------------------------------------
Time: 2018-01-06 06:39:50
-------------------------------------------
('Toulouse 00055 - ST SERNIN G. ARNOULT', 0)
('Nantes 00010- PICASSO', 0)
('Bruxelles-Capitale 021 - DE BROUCKERE (FERMÉE - TRAVAUX DE VOIRIE)', 0)
("Lyon 6041 - CITÉ INTERNATIONALE / TÊTE D'OR NORD", 0)
('Lyon 10005 - BOULEVARD DU 11 NOVEMBRE', 0)
('Dublin MOUNT STREET LOWER', 0)
('Seville 082_CALLE LUIS MONTOTO', 0)
('Marseille 1343 - FLAMMARION GROBET', 0)
('Seville 016_CALLE DE MANUEL VILLALOBOS', 0)
('Valence 268_PZA_LUIS_CANO_5', 0)
...
```
 
 2. In ```velib_new_empty_stations.py```, the velib stations that have became empty (displayed every 5s):
  ```
 -------------------------------------------                                	 
Time: 2018-01-06 06:48:00
-------------------------------------------
('Toulouse 00144 - SUISSE - LAUSANE', [1, 0])
('Lyon 1021 - TERREAUX / BEAUX ARTS', [1, 0])
```
 
 3. In ```velib_most_active_stations.py```, the stations that were most active (activity = number of bikes borrowed and returned) during the last 5 minutes (displayed every 1min). In the output, the first element of the couple indicates the activity:
```
-------------------------------------------                                	 
Time: 2018-01-06 06:52:00
-------------------------------------------
('Goteborg L��PPSTIFTET', (10, 0))
('Toyama ���籠町 HATAGO-MACHI', (8, 0))
('Lyon 5008 - SAINTE IR��NÉE', (8, 0))
('Lyon 7009 - JEAN JAUR��S', (2, 0))
('Toulouse 00010 - PLACE ESQUIROL', (2, 13))
('Brisbane 122 - LOWER RIVER TCE / ELLIS ST', (2, 5))
('Valence 017_ESTACION RENFE I', (2, 25))
('Seville 012_PLAZA DUQUESA DE ALBA', (2, 3))
('Lyon 7003 - GAMBETTA / GARIBALDI (FAR)', (2, 18))
('Nantes 00031-BOURSE', (1, 15))

```
 
 
