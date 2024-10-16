from __future__ import annotations

import os
import platform
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Literal, overload

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


@overload
def process_run(
    bin_name, *args: str, return_completed_process: Literal[True], **kwargs: Any
) -> subprocess.CompletedProcess[str | bytes]: ...


@overload
def process_run(
    bin_name, *args: str, return_completed_process: Literal[False] = ..., **kwargs: Any
) -> int: ...


@overload
def process_run(
    bin_name, *args: str, return_completed_process: bool = False, **kwargs: Any
) -> int | subprocess.CompletedProcess[str | bytes]: ...


def process_run(
    bin_name, *args: str, return_completed_process: bool = False, **kwargs: Any
) -> int | subprocess.CompletedProcess[str | bytes]:
    # if mac arm64, set DYLD_LIBRARY_PATH
    if sys.platform == "darwin":
        my_env: dict[str, str]
        if kwargs.get("env") is not None:
            my_env = deepcopy(kwargs["env"])
            my_env["DYLD_LIBRARY_PATH"] = str(LIB_DIR)
            kwargs.pop("env")
        else:
            my_env = os.environ.copy()
            my_env["DYLD_LIBRARY_PATH"] = str(LIB_DIR)
        complete_process = subprocess.run(
            [bin_path(bin_name), *args], env=my_env, **kwargs
        )
    # elif os.name == "nt":
    #     # dll files are together with the binaries.
    #     # so we need to add the directory to PATH
    #     my_env = os.environ.copy()
    #     my_env["PATH"] = f"{BIN_DIR!s};{my_env['PATH']}"
    #     complete_process = subprocess.run(
    #         [bin_path(bin_name), *args], env=my_env, shell=True, **kwargs
    #     )
    else:
        complete_process = subprocess.run([bin_path(bin_name), *args], **kwargs)

    if return_completed_process:
        return complete_process
    return complete_process.returncode


@overload
def apbs(
    *args: str, return_completed_process: Literal[True], **kwargs: Any
) -> subprocess.CompletedProcess[str | bytes]: ...


@overload
def apbs(
    *args: str, return_completed_process: Literal[False] = ..., **kwargs: Any
) -> int: ...


def apbs(
    *args: str, return_completed_process: bool = False, **kwargs: Any
) -> int | subprocess.CompletedProcess[str | bytes]:
    return process_run(
        "apbs", *args, return_completed_process=return_completed_process, **kwargs
    )


@overload
def multivalue(
    *args: str, return_completed_process: Literal[True], **kwargs: Any
) -> subprocess.CompletedProcess[str | bytes]: ...


@overload
def multivalue(
    *args: str, return_completed_process: Literal[False] = ..., **kwargs: Any
) -> int: ...


def multivalue(
    *args: str, return_completed_process: bool = False, **kwargs: Any
) -> int | subprocess.CompletedProcess[str | bytes]:
    return process_run(
        "multivalue", *args, return_completed_process=return_completed_process, **kwargs
    )
