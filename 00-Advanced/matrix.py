# marix.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, Optional
import concurrent.futures as cf
import threading
import time
import math
import os

# ---------- Errors (sentinel-like) ----------
class DimensionMismatch(ValueError):
    pass

# ---------- Errors (sentinel-like) ----------
class EmptyMatrix(ValueError):
    pass

# ---------- Matrix type (value semantics + methods) ----------
class Matrix:
    """
    Row-major dense matrix, dependency-free (no NumPy).
    data[*cols + j] stores element at (i, j)
    """

    __slots__ = ("_r", "_c", "_data")
    
    def __init__(self, rows: int, cols: int):
        if rows <= 0 or cols <= 0:
            raise EmptyMatrix("matrix cannot be empty")
        self._r = rows
        self._c = cols
        self._data = [0.0] * (rows * cols)
        
    @staticmethod
    def from_slice(rows: int, cols: int, row_major: Iterable[float]) -> "Matrix":
        if rows <= 0 or cols <= 0:
            raise EmptyMatrix("matrix cannot be empty")
        data = list(row_major)
        if len(data) != rows * cols:
            raise ValueError(f"invalid data length: got {len(data)}, want {rows * cols}")
        m = Matrix(rows, cols)
        m._data[:] = data
        return m
    
    @property
    def rows(self) -> int:
        return self._r
    
    @property
    def cols(self) -> int:
        return self._c
    
    def at(self, i: int, j: int) -> float:
        # like Go´s At the may panic, we intentionally do not boudnd check here
        return self._data[i * self._c + j]

    def set(self, i: int, j: int, v: float) -> None:
        self._data[i * self._c + j] = v
        
    def clone(self) -> "Matrix":
        out = Matrix(self._r, self._c)
        out._data[:] = self._data
        return out
    
    def transpose(self) -> "Matrix":
        out = Matrix(self._c, self._r)
        # cache local vars for speed in python loops
        oc = out._c
        c = self._c
        data = self._data
        odata = out._data
        r = self._r
        for i in range(r):
            base = i * c
            for j in range(c):
                # out[i, j] = self[i, j]
                odata[j * oc + i] = data[base + j]
        return out
    
    # convenience for iteration; not required but handy in tests
    def row(self, i: int) -> list[float]:
        start = i * self._c
        return self._data[start: start + self._c]
    
# ---------- Option pattern (Pythonic: dataclass config + kw overrides) ----------
@dataclass(frozen=True)
class MulConfig:
    workers: int = max(1, os.cpu_count() or 1)
    block_rows: int = 16; # true granularity
    

# ---------- Cancellation token (Python analog to Go context) ----------
class CancelToken:
    def __init__(self) -> None:
        self._ev = threading.Event()
    
    def cancel(self) -> None:
        self._ev.set()
    
    def cancelled(self) -> bool:
        return self._ev.is_set()
    
    def wait(self, timeout: Optional[float] = None) -> bool:
        return self._ev.wait(timeout)
    
 # ---------- Row-block job ----------
class _RowBlock: 
    __slots__ = ("start", "end")
    
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end # exclusive


# ---------- Concurrent multiplication (worker pool + cancellation) ----------
def mul_concurrent(
    a: Matrix,
    b: Matrix,
    *,
    config: MulConfig | None = None,
    cancel: CancelToken | None = None,
    timeout: Optional[float] = None
    ) -> Matrix:
    """ 
    C = A * B using a row-block worker pool.
    
    - Validates dims
    - Transposes B for locality
    - Partitions by block rows
    - Honors cancellation and optional timeout
    """
    if a.rows <= 0 or a.cols <= 0 or b.rows <= 0 or b.cols <= 0:
        raise EmptyMatrix("matrix cannot be empty")
    if a.cols != b.rows:
        raise DimensionMismatch("matrix dimension mismatch")
    
    cfg = config or MulConfig()
    cancel = cancel or CancelToken()
    
    out = Matrix(a.row, b.cols)
    bt = b.transpose()
    
    # Pre.bind locals for speed
    a_data = a._data
    bt_data = bt._data
    out_data = out._data
    a_c = a.cols
    out_c = out.cols
    bt_c = bt.cols # equals a.cols
    a_r = a.rows
    
    # Partition jobs by block_rows
    jobs: list[_RowBlock] = []
    br = max(1, cfg.block_rows)
    s = 0
    while s < a_r:
        e = min(a_r, s + br)
        jobs.append(_RowBlock(s, e))
        s = e
        
    # Worker task: compute assigned row block
    def _do_block(block: _RowBlock) -> None:
        # quick cancellation check
        if cancel.cancelled():
            return 
        start, end = block.start, block.end
        for i in range(start, end):
            arow = i * a_c
            orow = i * out_c
            # (i, j) dor product
            for j in range(out_c):
                s = 0.0
                btrow = j * bt_c
                # tight inner loop
                for k in range(a_c):
                    s += a_data[arow + k] * bt_data[btrow + k]
                out_data[orow + j] = s
        if cancel.cancelled():
            return
    # Execute with ThreadPool (dependency-free).
    # NOTE: For true CPU scaling in Python, consider ProcessPoolExecutor
    # but it has higher overhead due to data shipping no shared memory here).
    start_t = time.perf_counter()
    with cf.ThreadPoolExecutor(max_workers=cfg.workers) as ex:
        futs = [ex.submit(_do_block, jb) for jb in jobs]
        # Manage completion, timeout, cancellation
        for fut in cf.as_completed(futs, timeout=timeout):
            if cancel.cancelled():
                break
            # propagate exceptions early
            _ = fut.result()
            
    # Best-effort timeout handling—if we timed out, surface it as cancellation
    if timeout is not None and (time.perf_counter() -start_t) > timeout:
        cancel.cancel()
    if cancel.cancelled():
        raise TimeoutError("multiplication cancelled/timeout")
    return out


# ---------- Deterministic filler (like the Go helper) ----------
def fill_deterministic(m: Matrix, seed: float) -> Matrix:
    out = m.clone()
    v = float(seed)
    data = out._data
    for i in range(len(data)):
        v = v * 1.0001 + 0.0003
        data[i] = v
    return out
 
 
 # ---------- Demo main ----------
if __name__ == "__main__":
    # Context like cancellation by timeout
    tok = CancelToken()
    cfg = MulConfig(workers=max(1, os.cpu_count() or 1), block_rows=32)
    
    a = Matrix(256, 256)
    b = Matrix(256, 256)
    a = fill_deterministic(a, 1.0)
    b = fill_deterministic(b, 2.0)
    
    t0 = time.perf_counter()
    try:
        c = mul_concurrent(a, b, config=cfg, cancel=tok, timeout=5.0)
    except TimeoutError as e:
        print("mul error:", e)
        raise
    dt = time.perf_counter() - t0
    
    print(f"C[0,0]={c.at(0,0):.6f} C[10,10]={c.at(10,10):.6f} elapsed={dt:.3f}s workers={cfg.workers}")
