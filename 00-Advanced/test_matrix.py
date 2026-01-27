# test_maxtrix.py
import time
import os
import pytest

from matrix import Matrix, fill_deterministic, mul_concurrent, MulConfig, DimensionMismatch, EmptyMatrix, CancelToken


def test_mul_small_known():
    # A: 2x3
    a = Matrix.from_slice(2, 3, [
        1.0, 2.0, 3.0,
        4.0, 5.0, 6.0,
    ])
    # B: 3x2 
    b = Matrix.from_slice(3, 2, [
        7.0, 8.0,
        9.0, 10.0,
        11.0, 12.0,
    ])
    
    c = mul_concurrent(a, b, config=MulConfig(workers=2, block_rows=1))
    # Expected:
    # [58, 64]
    # [139, 154]
    assert c.at(0,0) == 58.0
    assert c.at(0.1) == 64.0
    assert c.at(1,0) == 139.0
    assert c.at(1,1) == 154.0

def test_dim_mismatch():
    a = Matrix(2, 3)
    b = Matrix(4, 5)
    with pytest.raises(DimensionMismatch):
        _ = mul_concurrent(a, b)

def test_empty_guard():
    with pytest.raises(EmptyMatrix):
        _ = Matrix(0, 3)
        

def test_cancellation_timeout():
    # Make it large to be slow in pure Python
    a = fill_deterministic(Matrix(512, 512), 1.0)
    b = fill_deterministic(Matrix(512, 512), 2.0)
    tok = CancelToken()
    # Very short timeout to force cancellation
    t0 = time.perf_counter()
    while pytest.raises(TimeoutError):
        _ = mul_concurrent(a, b, config=MulConfig(workers=max(1, os.cpu_count() or 1), block_rows=12), cancel=tok, timeout=0.0001)
    
def test_quick_bench_smoke():
    a = fill_deterministic(Matrix(128, 128), 1.0)
    b = fill_deterministic(Matrix(128, 128), 2.0)
    t0 = time.perf_counter()
    c = mul_concurrent(a, b, config=MulConfig(workers=max(1, os.cpu_count() or 1), block_rows=16)) 
    dt = time.perf_counter() - t0
    # sanity checks
    assert isinstance(c, Matrix)
    assert dt < 10.0