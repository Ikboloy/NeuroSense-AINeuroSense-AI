---
title: "NeuroSense AI: Offline Stereo Depth and Confidence Analysis Utilities"
tags:
  - Python
  - stereo vision
  - depth estimation
  - computer vision
authors:
  - name: Sobirova Ikboloy Ikrom Kizi
    affiliation: 1
affiliations:
  - name: Independent Researcher, Daegu, Republic of Korea
    index: 1
date: 17 November 2026
bibliography: paper.bib
---

# Summary

NeuroSense AI is early-stage research software for analysing classical stereo-derived depth estimates, left-right consistency and pixel-level error in offline assistive-perception research. Current utilities implement depth conversion and selected validation metrics; a full reproducible pipeline remains future work.

# Statement of need

Explicit measurement of uncertainty and unassessed image regions is relevant to offline depth-estimation benchmarking. The software aims to support reproducible experiments without treating missing depth as safe navigable space.

# Research context

The project's preliminary research preprint is available on Zenodo [@sobirova2026]. It evaluates Middlebury images, including a recall-precision tradeoff when rejecting disparities. These reported results are not new validation of this software package; reproducing them from this package remains to be completed.

# Limitations

This package is not a pedestrian navigation system, has not been tested with visually impaired participants, and does not establish navigation safety. This document is an initial *draft*, not an accepted or submitted JOSS paper.
