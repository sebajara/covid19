## Approach

As the number of infected people should follow some king of exponential
function, I used the
[fitderiv](http://swainlab.bio.ed.ac.uk/software/fitderiv/) package for
inferring the derivative of the log of the data (growth-rate). I also
present infer the growth-rate for the total number of test and deaths,
although I have no reason to expect them to follow an exponential
function (perhaps deaths?). NOTE: errors on the log-rates are likely to
be underestimated.

## Preliminary analysis

* Overall we can appreciate a reduction in the posive cases growth-rate,
most likely as a result of the measures taken. 
* Are the total tests gr-rates and the positives gr-rates correlated? It
  appears so in some cases. But how is testing decided and how they is
  reported/collected? Also should account for likely delays in reporting
  or collection.
* Death rates seem to decrease or remain relatively flat. Hard to say if
  "sharp" transitions observed are due to low numbers (just random), or
  details on how the data was reported/collected. We should wait for a
  few more weeks.

It is easy to see how overall rates begin to decrease from the second
half of March. Animation:
![Animation. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates.gif)
Each point represents a state, and the colors are by the total number of
reported deaths (from white to dark red). For plotting NaN values were
set to 0 just for visualization. 

For more details we plot the trajectory of the variables and the
estimated growth-rates. States are clustered within similar total
population range.

**California, Texas, Florida, New York, & Pennsylvania**
![Set 0. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_0.png)
**Illinois, Ohio, Georgia, North Carolina, & Michigan**
![Set 1. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_1.png)
**New Jersey, Virginia, Washington, Arizona, & Massachusetts**
![Set 2. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_2.png)
**Tennessee, Indiana, Missouri, Maryland, Wisconsin**
![Set 3. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_3.png)
**Colorado, Minnesota, South Carolina, Alabama, & Louisiana**
![Set 4. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_4.png)
**Kentucky, Oregon, Oklahoma, Connecticut, & Utah**
![Set 5. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_5.png)
**Iowa, Nevada, Arkansas, Mississippi, & Kansas**
![Set 6. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_6.png)
**New Mexico, Nebraska, West Virginia, Idaho, & Hawaii**
![Set 7. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_7.png)
**New Hampshire, Maine, Montana, Rhode Island, & Delaware**
![Set 8. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_8.png)
**South Dakota, North Dakota, Alaska, District of Columbia, Vermont, & Wyoming**
![Set 9. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_9.png)
**American Samoa, Guam, Northern Mariana Islands, Puerto Rico, & Virgin Islands**
![Set 10. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates_byset_10.png)

## Directions and TODOs

TODO:
* Improve estimation of the errors in the rates.

Directions:
* Obtain data regarding date and degree of isolation measures and
  overlay this with the rates.
* Obtain data regarding state metrics such as health index, population
  density, age distributions, etc and correlate with these estimation. I
  think would be most meaningful with the data after a few more months.
