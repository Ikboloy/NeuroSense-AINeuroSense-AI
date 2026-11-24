# Near-side depth boundaries in ten TUM frame pairs

Run `python edges.py PATH_TO_freiburg1_xyz > edges.csv` with NumPy, SciPy and Pillow. The [parent comparison](comparison.md) defines the matcher and gaps. Its pooled baseline and filtered counts reproduce exactly. See [per-pair results](edges.csv).

At 160 × 120, a near-side edge is a baseline-eligible sensor sample at 0.45–1.00 m with at least one of its four immediate neighbors at least 0.15 m farther away and within the valid 0.45–3 m range. The near interior comparator requires all four neighbors valid and differing by less than 0.15 m in either direction. Other near pixels are unclassified. These fixed thresholds define geometric depth jumps, not annotated object outlines. Sensor data label scoring regions only. Counts pool repeated observations, not independent objects.

| Gap | Edge kept / 798 | Interior kept / 60,837 | Median retained edge error |
|---|---:|---:|---:|
| Baseline | 798 | 60,837 | 5.16 cm |
| >0 | 798 | 59,944 | 5.16 cm |
| >1 | 193 | 2,047 | 3.72 cm |
| >3 | 26 | 225 | 3.40 cm |

At gap >1 the near edges survived more frequently (24.19%) than near interiors (3.36%), yet 605 of 798 eligible edge observations were rejected. At gap >3 only 26 remain. Rates condition on the baseline mask: missing sensor depth and rejected baseline pixels do not enter the denominator. Sensor alignment and downsampling can shift a one-pixel edge. This desk sequence does not measure obstacle-level recall or navigation safety.