# JOSS readiness checklist

**Current status: not yet ready to submit.** This repository includes an installable research library, a Chess1 command-line pipeline, synthetic tests, and an optional full-dataset regression test. Independent Chess1 image-to-metric recalculation matches archived CSVs, but direct package-level full-data regression is still pending.

- [x] Public source repository with a permissive license.
- [x] Preliminary installable Python package.
- [x] Preliminary unit tests and GitHub Actions configuration.
- [x] Draft paper.md and bibliography.
- [x] Independently recalculate Chess1 image-to-metric values and compare with archived Experiment 14 and 16 CSVs.\n- [ ] Run the **installed package** against the full Chess1 dataset using the opt-in regression test; public CI skips this without the dataset.
- [ ] Provide data acquisition, version, checksums, and executable experiment configuration.
- [x] Provide a Chess1 image-to-metric command-line pipeline and Motorcycle metric-evaluation CLI.\n- [x] Extract calibrated 3D point-cloud geometry and PLY writer into tested functions.\n- [x] Independently verify Motorcycle 3D geometry against archived PLY: 301,197 points, identical RGB and maximum XYZ difference 5.2e-6 metres.\n- [ ] Execute the **installed package's** opt-in PLY regression with original data and integrate remaining original experiment scripts.\n- [ ] Package the original full multi-scene disparity workflows.
- [ ] Add reliable tests covering actual research paths and numerical edge cases.
- [x] Provide initial API/user guide, examples, citation metadata, and research-evidence register.\n- [ ] Add more examples and third-party validation.
- [ ] Establish sustained public development history and evidence of research use.
- [ ] Evaluate JOSS scope, significance, and pre-submission policies against latest published criteria.
- [ ] Verify any copied third-party code/data can be distributed.

This project provides offline research results and **does not** establish pedestrian safety.
