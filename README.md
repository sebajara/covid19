# Overview

This is a collection of resources, visualizations, and analysis
regarding the Covid-19 pandemic. For now it includes some graphical
representations, and an example on how to use Gaussian Process to infer
the rates of positive cases and deaths with time and with respect to
each other. Once the epidemic passes the goal will be to correlate the
dynamics of individual countries and US' states with their respective
responses, as well as some socio-economic metrics.

## Countries

## USA States

Here is an animation showing the evolution of covid19 in the USA (by state).
![Animation of US data by state from covidtracking](figures/covidtracking_states_eda1_zoom.gif)
Each point represents a state, the circle sizes are by the [estimated
population in
2019](https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail/),
and the colors are by the total number of reported deaths (from white to
dark red). Notice we are using log-scales and total positives scale
begins from 100. A few states were not included because I lacked the
population data. Data taken from
[covidtracking](https://covidtracking.com/), mostly because it included
the number of tests performed on each state. Quality varies, see website
for details.

In the document [USA_STATE_RATES.md](USA_STATE_RATES.md) I describe the
(ongoing) resuls related to inferring rates using Gaussian Process.

## Data sources on Covid19
* Covid19 data by country compiled by the European Centre for Disease Prevention and Control [ecdc-covid-19-cases-worldwide](https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases)
* Testing data sources compiled by OurWorldInData [github/owid/covid-19-data](https://github.com/owid/covid-19-data/tree/master/public/data/testing)
* Johns Hopkins CSSE repo [github/Johns-Hopkins/COVID-19](https://github.com/CSSEGISandData/COVID-19)
* Covid19 data from the US by state. It includes number of tests. [covidtracking](https://covidtracking.com/)
* Covid19 data from the US by state and county. Does not include number of tests. [github/nytimes/covid-19-data](https://github.com/nytimes/covid-19-data)
* Covid data from France [github/opencovid19-fr](https://github.com/opencovid19-fr/data)
* Hospital covid data from France [donnees-hospitalieres-relatives-a-lepidemie-de-covid-19](https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/)
* Covid19 data from Germany [github/covid-19-germany-gae](https://github.com/jgehrcke/covid-19-germany-gae)
* Covid19 data from Spain [github/datadista/COVID 2019](https://github.com/datadista/datasets/tree/master/COVID%2019)
* "COVID-19 Economic Stimulus Index" [paper](http://web.boun.edu.tr/elgin/COVID_19.pdf), [website](http://web.boun.edu.tr/elgin/COVID.htm), [data](COVID-19 Economic Stimulus Index)

## Interesting analysis and commentaries on Covid19
* Genomic epidemiology of covid19 [nextstrain/ncov](https://nextstrain.org/ncov)
* Analysis by OurWorldInData. Good charts and discussions. [ourworldindata/coronavirus](https://ourworldindata.org/coronavirus)
* Collection of tableau graphics [tableau-data-resources](https://www.tableau.com/covid-19-coronavirus-data-resources)
* Collection of different statistical analysis and visualizations on
  covid19 data by people interested. [covid19dashboards](https://covid19dashboards.com/)
* Oxford is tracking goverment responses and the number of covid cases. [oxford-covid-19-government-response-tracker](https://www.bsg.ox.ac.uk/research/research-projects/oxford-covid-19-government-response-tracker)
* The paper that changed the mind of the UK goverment on how to handle the virus. Historically relevant
  [Imperial-College-COVID19-NPI-modelling](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-NPI-modelling-16-03-2020.pdf)
* Article on what is the "good" attitude one should have when doing data science on covid19 [How_To_Be_Curious_Instead_of_Contrarian_About_Covid19](https://rexdouglass.github.io/TIGR/Douglass_2020_How_To_Be_Curious_Instead_of_Contrarian_About_Covid19.nb.html)
* Article on potential danger of making all models equally relative. Lessons learned from the public opinion on climate change. [all-models-are-wrong-but-some-are-completely-wrong](https://rssdss.design.blog/2020/03/31/all-models-are-wrong-but-some-are-completely-wrong/)
* Article discussing some of the difficulties in modeling the infection, mostly on how data is constructed and hidden variables [why-its-so-freaking-hard-to-make-a-good-covid-19-model](https://fivethirtyeight.com/features/why-its-so-freaking-hard-to-make-a-good-covid-19-model/)
* Article on the meaning of positive cases, and some other ways to estimate the actual number of cases [coronavirus-case-counts-are-meaningless](https://fivethirtyeight.com/features/coronavirus-case-counts-are-meaningless/)
* Interesting preliminary analysis from concerned citizens [the-hammer-and-the-dance](https://medium.com/@tomaspueyo/coronavirus-the-hammer-and-the-dance-be9337092b56)

## More general resources on infection disease modelling
* Modeling of SEIRS epidemic dynamics with extensions, including
  network-structured populations, testing, contact tracing, and social
  distancing. [seirsplus](https://github.com/ryansmcgee/seirsplus)
* Paper on how to incorporate behavioural change in forecasting
  models. "Systematic biases in disease forecasting – The role of
  behavior
  change". [link](https://www.sciencedirect.com/science/article/pii/S1755436518301063?via%3Dihub)
* Paper on the Importance on accounting individual variability v/s average population
  models. They describe how individual-specific control measures can
  outperform population-wide measures". "Superspreading and the effect
  of individual variation on disease
  emergence". [link](https://www.nature.com/articles/nature04153)
