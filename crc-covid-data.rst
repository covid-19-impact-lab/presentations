:Title: (Programming) Lessons Learned
:Authors: Hans-Martin v. Gaudecker & the `CoViD-19 Impact Lab <https://covid-19-impact-lab.readthedocs.io/en/latest/people.html>`__ team
:Organization: Universität Bonn & IZA
:Course: CoViD-19 Impact Lab
:Copyright: Creative Commons



CoViD-19 Impact Lab
====================

* Youngest child of OSE — founded 15 March or so
* 4 arms

  * LISS data analysis (NL)
  * GESIS data analysis (DE)
  * Twitter sentiment analysis
  * Infection model

* Major support from ECONtribute, CRC TR/224, IZA, NWO


Quickly grown out of infancy
============================

* 4 + 1 waves of data collection
* Informative `website <https://covid-19-impact-lab.io>`_
* A `beautiful dashboard <https://covid-19-impact-lab.iza.org/>`_
* 1 Working paper + 2 imminent
* Reports published by CPB, DNB
* Results discussed in German and Dutch cabinets

Background
=============

* LISS panel a long-running Dutch Internet Panel (since 2007)
* Probability-based sample, ~7000 respondents
* Data can be linked to administrative records at an individual-level
* Christian, Axel and me have collected lots of data on ambiguity there for the past two years (and I did some stuff previously)


CoViD-19 surveys
================

* See https://liss-covid-19-questionnaires-documentation.readthedocs.io/
* **March 20-31:** Risk perceptions, behavioural reactions and preferences re social distancing policies, changes in the work and childcare situation, intentions and expectations regarding consumption/savings decisions, mental health **(financed by ECONtribute)**.
* **April 6-28:** Risk perceptions, number of personal contacts, changes in the work situation, income and macro expectations **(financed by ECONtribute)**
* **April 21-28:** Time Use and Consumption survey, similar to November 2019 edition, adapted to current situation **(financed by CRC/TR 224)**
* **May** Mostly labour, some health, home schooling
* **June** Mostly labour, lots of job search, how do parents deal with opening of daycares / primary schools?


Data management: Background
===========================

* Data management: First idea — get out some dataset to be used quickly
* Traded off speed for consistency
* Lesson learned: There is no trade-off


Variable names
===========================================

* https://estimagic.readthedocs.io/en/latest/contributing/styleguide.html
* What is the probability that the Coronavirus crisis will lead to a situation where you have no income or where your income is lower than what you need to cover basic needs and outstanding payment obligations?
* = Financial distress if you have a million on your bank account?


Stick to Normal forms
===========================================

* Values do not have any internal structure
* Tables do not contain redundant information
* No structure in variable names

Started with wide format -- painful (lots of string parsing for variable names, little flexibility)


Technical hurdles
===========================================

* Started out with group of people who knew their tools (in particular Python, Git)
* Many of those who are eager to analyse data are on Stata or R and have no idea of either Python or Git
* Lots of double work and confusion (how to discretise probability statements?)
* Classic open source issue -- get a solution for your problem, do not take externalities into account
* Need to solve challenges


Interoperability Pandas -- R / Stata
===========================================

* Stay away from the bleeding edge of Pandas, especially the internal data types including missings -- killed feather
* Went with pickle for Pandas DataFrames, csv for R & Stata
* Lots of information lost in transition
* Silver bullet not found yet, trying Parquet / dta now


Overall conclusions
===================

* Much slower than what we had envisioned, largely my "fault"
* Frictions between "applied" people and nerds tough if under time pressure
* Information flow in unstructured / not very structured organisation
* Still, pretty much did what large research institutes do for 7 or 8-digit budgets with 10 core + 15 non-core people
* Very proud of what we have achieved so far
