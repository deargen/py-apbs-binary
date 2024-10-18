import os
from pathlib import Path

BIN_DIR = Path(__file__).parent / "bin"
# NOTE: lib/ only exists for macos arm64, because we built using homebrew
# and it didn't build entirely statically.
# Thus we have to pass DYLD_LIBRARY_PATH to the subprocess.run call.
LIB_DIR = Path(__file__).parent / "lib"


def bin_path(bin_name: str) -> Path:
    if os.name == "nt":
        return BIN_DIR / f"{bin_name}.exe"
    return BIN_DIR / bin_name


# bin/
APBS_BIN_PATH = bin_path("apbs")

# originally share/apbs/tools/bin/, but moved to bin/
ANALYSIS_BIN_PATH = bin_path("analysis")
BENCHMARK_BIN_PATH = bin_path("benchmark")
BORN_BIN_PATH = bin_path("born")
COULOMB_BIN_PATH = bin_path("coulomb")
DEL2DX_BIN_PATH = bin_path("del2dx")
DX2MOL_BIN_PATH = bin_path("dx2mol")
DX2UHBD_BIN_PATH = bin_path("dx2uhbd")
DXMATH_BIN_PATH = bin_path("dxmath")
MERGEDX_BIN_PATH = bin_path("mergedx")
MERGEDX2_BIN_PATH = bin_path("mergedx2")
MGMESH_BIN_PATH = bin_path("mgmesh")
MULTIVALUE_BIN_PATH = bin_path("multivalue")
SIMILARITY_BIN_PATH = bin_path("similarity")
SMOOTH_BIN_PATH = bin_path("smooth")
TENSOR2DX_BIN_PATH = bin_path("tensor2dx")
UHBD_ASC2BIN_BIN_PATH = bin_path("uhbd_asc2bin")
VALUE_BIN_PATH = bin_path("value")


from .executable import (
    popen_analysis,
    popen_apbs,
    popen_benchmark,
    popen_born,
    popen_coulomb,
    popen_del2dx,
    popen_dx2mol,
    popen_dx2uhbd,
    popen_dxmath,
    popen_mergedx,
    popen_mergedx2,
    popen_mgmesh,
    popen_multivalue,
    popen_similarity,
    popen_smooth,
    popen_tensor2dx,
    popen_uhbd_asc2bin,
    popen_value,
    run_analysis,
    run_apbs,
    run_benchmark,
    run_born,
    run_coulomb,
    run_del2dx,
    run_dx2mol,
    run_dx2uhbd,
    run_dxmath,
    run_mergedx,
    run_mergedx2,
    run_mgmesh,
    run_multivalue,
    run_similarity,
    run_smooth,
    run_tensor2dx,
    run_uhbd_asc2bin,
    run_value,
)

__version__ = "0.0.0"
