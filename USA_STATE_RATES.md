## Methods

As the number of infected people should follow some king of exponential
function, I used the
[fitderiv](http://swainlab.bio.ed.ac.uk/software/fitderiv/) package for
inferring the derivative of the log of the data (growth-rate). I also
present the result from inferring the growth-rate for the total number
of test and deaths. It is less clear a priory whether these should
follow an exponential function. NOTE: errors apear to be highly
underestimated given the default parameters used.

Animation:
![Animation. Infering rates from US covidtracking data. Last update: 2020-04-07](figures/covidtracking_states_rates.gif)
Each point represents a state, the circle sizes are by the [estimated
population in
2019](https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail/),
and the colors are by the total number of reported deaths (from white to
dark red). Some island states were not included because I lacked the
population data. Also NaN values were set to 0 just for visualization.

Preliminary analysis:
* Overall we can appreciate a reduction in the posive cases growth-rate,
most likely as a result of the measures taken. 
* Some states appear to vary on the quality of their reporting or data
  gathering efforts. How to correct for it?
* The dynamics on the number of tests seems highly arbitrary (other than
  a loose correlation with number of cases). 



Potential directions:
* Obtain data regarding date and degree of isolation measures and
  overlay this with the rates.
* Obtain data regarding state metrics such as health index, population
  density, age distributions, etc and correlate with these estimation. I
  think would be most meaningful with the data after a few more months.
