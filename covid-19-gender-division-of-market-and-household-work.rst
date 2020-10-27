:Title: The CoViD-19 crisis and the gender division of market and household work
:Authors: Hans-Martin von Gaudecker, Radost Holler, Lena Janys, Bettina Siflinger, Christian Zimpelmann
:Organization: Universität Bonn & IZA
:Copyright: Creative Commons


Introduction
============

* Data from the Netherlands
  * Hours of work: February – September 2020
  * Time use: November 2019, April 2020
* On average, women reduce one hour extra during lockdown, effect vanishes by June
* No additional effect of children being present in the household on either parent!
* Allocation of additional childcare depends on hours of work pre-CoViD:
  * If both parents work full-time before pandemic: roughly equal shares
  * Combinations FT / PT or FT / no work: Gender care gap increases

.. * Typically 37 + 32 hours than 45 + 45

.. raw:: latex
    
    \clearpage


Data: Background
================

* LISS: Online Panel in the Netherlands, running since 2007
* Sibling of UAS
  * Descendant of CentERpanel
  * Joint usage via `Open Probability-Based Panel Alliance <https://openpanelalliance.org/>`_
* Roughly 5,000 households / 7,500 individuals
* Each month, respondents get ≅30 minutes of questionnaires
* Around 85% of respondents can be linked to administrative microdata (not today)

.. * Based on probability sample
.. * Background data on Work, Health, Income, ...
.. * Questionnaires designed by researchers (~85c / minute / respondent)

Data: CoViD-19 surveys, Time Use
================================

* CoViD-19 questionnaires
  * March 20-31 (mild lockdown), April 6-28 (mild lockdown), May (daycare / primary schools started reopening), June, September
  * See https://liss-covid-19-questionnaires-documentation.readthedocs.io/
  * Will mostly use hours of work
* Time use & consumption questionnaires
  * November 2019: Baseline
  * April 2020: Similar to November 2019 edition, adapted to lockdown situation
  * November 2020: Similar to November 2019, adapted to current situation

.. raw:: latex
    
    \clearpage


Hours worked / worked from home
===============================

|pic1|  |pic2|

.. |pic1| image:: work-childcare/abs-change-hours-over-time-by-gender-full-unconditional.png
   :width: 35%

.. |pic2| image:: work-childcare/abs-change-hours-home-over-time-by-gender-full-unconditional.png
   :width: 35%


Fixed effects regressions
=========================

* Hours of work on gender × month, controls
* Large heterogeneity
  * Non-essential FT women reduce 3 **more** hours during lockdown than non-essential men
  * Essential FT women reduce 1.5 hours **less** than non-essential men
* Rich controls on RHS, exact set does not matter: 
  * month × gender × (1, part time, essential worker, age)
  * month × (age, percentage of work doable from home, self-employment, profession, sector)
* Add gender × month × children under 12 at home
  * No change (precise zero or hours slightly **better** preserved among parents)
  * Coefficients very similar when restricting sample to 2-parent families


Full-time / Non-working couples
===============================

.. image:: work-childcare/stacked-bar-plot-market-nonmarket-details-split-50-fulltime-olf.png


Full-time / Part-time couples
=============================

.. image:: work-childcare/stacked-bar-plot-market-nonmarket-details-split-50-fulltime-parttime.png


Full-time x2 couples
====================

.. image:: work-childcare/stacked-bar-plot-market-nonmarket-details-split-50-both-fulltime.png


Takeaways
=========

- Gender division of tasks during CoViD-19: Very heterogeneous
  - Not back to the 1950s
  - Not the great equalizer
  - Pre-existing patterns re-inforced
- Western Europe: Work hours of women (relatively) well preserved
  - Consequence of highly subsidised daycare with comparably short hours?
  - Short school closures (≅2-3 months) very likely key
- Glimpse of hope in the long run via changed norms?
  - Home office acceptance rises for men, less hindrance on career path
  - No long commute on 2-3 days → available for childcare / emergencies
