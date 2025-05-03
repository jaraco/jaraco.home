.. image:: https://img.shields.io/pypi/v/jaraco.home.svg
   :target: https://pypi.org/project/jaraco.home

.. image:: https://img.shields.io/pypi/pyversions/jaraco.home.svg

.. image:: https://github.com/jaraco/jaraco.home/actions/workflows/main.yml/badge.svg
   :target: https://github.com/jaraco/jaraco.home/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. .. image:: https://readthedocs.org/projects/PROJECT_RTD/badge/?version=latest
..    :target: https://PROJECT_RTD.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2025-informational
   :target: https://blog.jaraco.com/skeleton


Report spam calls
=================

Jason uses this routine to report spam calls to the FTC:

```
py -m jaraco.develop.report-spam-call 202-555-1212
```

It uses `Splinter <https://splinter.readthedocs.io/en/stable/index.html>`_ to automate the process of reporting a spam call through the donotcall.gov website.

It might be overly tuned to a specific class of calls, so feel free to propose extensions to the process to suit more needs.
