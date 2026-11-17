import numpy as np
import pytest
from neurosense_ai.pointcloud import disparity_to_points, write_ply


def test_reconstruction_coordinates():
    disp = np.full((2,2), 10.0)
    rgb = np.zeros((2,2,3), dtype=np.uint8)
    rgb[0,1] = [10,20,30]
    points, colors = disparity_to_points(disp,rgb,100,100,0,0,0.1,step=1)
    assert points.shape == (4,3)
    assert np.allclose(points[1], [0.01,0,1])
    assert colors[1].tolist() == [10,20,30]


def test_invalid_disparity_filtered():
    d=np.array([[0.,np.nan],[-1.,10.]])
    p,_=disparity_to_points(d,np.zeros((2,2,3),dtype=np.uint8),100,100,0,0,0.1,step=1)
    assert p.shape == (1,3)


def test_ply_output(tmp_path):
    p=tmp_path/"points.ply"
    write_ply(p,np.array([[0.,0.,1.]]),np.array([[255,2,3]],dtype=np.uint8))
    content=p.read_text()
    assert "element vertex 1" in content
    assert "0.00000 0.00000 1.00000 255 2 3" in content


def test_bad_shapes():
    with pytest.raises(ValueError):
        disparity_to_points(np.ones((2,2)),np.ones((2,2)),100,100,0,0,0.1)
