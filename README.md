# NeuroSense AI — research software preparation

**Status: early research software, not yet JOSS-ready.**

NeuroSense AI explores classical stereo matching, left–right consistency, confidence-aware depth estimation and offline 3D candidate analysis for assistive perception research. It is **not** a deployed navigation or haptic system; no pedestrian safety evaluation has been conducted.

**Research preprint:** Sobirova Ikboloy Ikrom Kizi (2026), *NeuroSense AI: Confidence-Aware Stereo Depth Estimation — An Offline Error Characterization for Assistive Perception*. Zenodo: https://doi.org/10.5281/zenodo.24299509

## Installation

Requires Python 3.10 or newer.

```bash
python -m pip install -e '.[experiments,test]'
python -m pytest -q
```

The reusable Python library contains preliminary utilities for disparity-to-depth conversion, signed left–right disparity consistency, common-valid disparity error and near-surface metrics. The library now includes reusable Chess1 confidence and near-surface evaluation and Motorcycle disparity-to-depth metrics. The original Chess1 image-to-metric calculations have been independently recomputed and match the archived CSV results; direct full-dataset regression of the installed package remains an opt-in local test. See [Chess1 reproduction instructions](docs/CHESS1_PACKAGE_REPRODUCTION.md).

## Reproduce Chess1

```bash
python -m neurosense_ai.chess1_cli --scene dataset/middlebury/chess1 --output results/chess1
```

To compare the installed package against the archived metrics, set `NEUROSENSE_CHESS1_DIR` to the Chess1 dataset directory and run `python -m pytest -q tests/test_chess1_regression.py`. Without the dataset this regression test is skipped. See [detailed instructions](docs/CHESS1_PACKAGE_REPRODUCTION.md).

## Data and safety

Obtain Middlebury stereo datasets from https://vision.middlebury.edu/stereo/ and comply with the original licensing terms. Datasets are not redistributed. Rejected estimates represent unknown regions, not confirmed free space. No safety claims are made.

## JOSS status

This repository is **not currently eligible for immediate JOSS submission**. Additional scientific software development, an auditable public development history, reliable installation, fuller tests, reproduction documentation and evidence of research use are still required.

## License

Original source code: MIT — see [LICENSE](LICENSE). Third-party material is not covered by this license.

Copyright (c) 2026 Sobirova Ikboloy Ikrom Kizi.
