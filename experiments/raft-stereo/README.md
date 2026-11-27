# RAFT-Stereo vs SGBM
Question: does learned matching preserve the boundaries of chess pieces and skate laces better? No model results yet.

Use the official [RAFT-Stereo](https://github.com/princeton-vl/RAFT-Stereo) CUDA environment and its pretrained Middlebury checkpoint. Record the upstream commit, checkpoint hash, GPU and image resolution. For each rectified scene set SCENE to its absolute directory, CKPT to the checkpoint, OUT to an absolute results directory, and NEUROSENSE to this repository's absolute path. From the upstream repository:

```bash
python demo.py --restore_ckpt "$CKPT" --valid_iters 32 --save_numpy -l "$SCENE/im0.png" -r "$SCENE/im1.png" --output_directory "$OUT/flow"
python "$NEUROSENSE/experiments/raft-stereo/compare.py" "$SCENE" "$OUT/flow/$(basename "$SCENE").npy" "$OUT"
```

The comparison script requires NumPy and OpenCV. Inspect the left image, SGBM and RAFT panels at the same zoom; both maps use the same disparity scale. Black denotes invalid predictions. With disp0.pfm, JSON includes common-valid MAE and fraction above 2 px. Read coverage alongside accuracy. Inspect chess-piece boundaries, laces and mat separately; global errors alone cannot establish better boundaries. Only SGBM compute time is recorded; do not compare it with end-to-end demo time. Two scenes are exploratory, and the Middlebury checkpoint is not evidence of generalization to unseen datasets.