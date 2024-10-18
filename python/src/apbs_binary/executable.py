"""
Wrapper that does subprocess.run or Popen with given binaries, with the correct environment variables set.

To perfect the type hinting, we have executable.pyi that copies the signatures
from subprocess.run and subprocess.Popen.
Normally, functions with *args, **kwargs are hard to type hint.
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Callable
from copy import deepcopy
from os import PathLike

from . import LIB_DIR, bin_path


def _subprocess_with_env(run_or_popen_func: Callable, *args, **kwargs):
    """
    In macOS, we need to set DYLD_LIBRARY_PATH to the lib/ directory.
    """
    if sys.platform == "darwin":
        my_env: dict[str, str]
        if kwargs.get("env") is not None:
            my_env = deepcopy(kwargs["env"])
            my_env["DYLD_LIBRARY_PATH"] = str(LIB_DIR)
            kwargs.pop("env")
        else:
            my_env = os.environ.copy()
            my_env["DYLD_LIBRARY_PATH"] = str(LIB_DIR)
        return run_or_popen_func(*args, env=my_env, **kwargs)

    return run_or_popen_func(*args, **kwargs)


def _subprocess_with_env_and_bin(run_or_popen_func, bin_name: str, *args, **kwargs):
    if len(args) > 0:
        cmd_args = args[0]
        args = args[1:]
    else:
        cmd_args = None

    if cmd_args is None or (isinstance(cmd_args, str) and cmd_args == ""):
        return _subprocess_with_env(
            run_or_popen_func, bin_path(bin_name), *args, **kwargs
        )
    elif isinstance(cmd_args, (str, bytes, PathLike)):
        return _subprocess_with_env(
            run_or_popen_func, [bin_path(bin_name), cmd_args], *args, **kwargs
        )
    return _subprocess_with_env(
        run_or_popen_func, [bin_path(bin_name), *cmd_args], *args, **kwargs
    )


def run_apbs(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "apbs", *args, **kwargs)


def popen_apbs(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "apbs", *args, **kwargs)


def run_multivalue(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "multivalue", *args, **kwargs)


def popen_multivalue(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "multivalue", *args, **kwargs)


def run_analysis(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "analysis", *args, **kwargs)


def popen_analysis(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "analysis", *args, **kwargs)


def run_benchmark(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "benchmark", *args, **kwargs)


def popen_benchmark(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "benchmark", *args, **kwargs)


def run_born(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "born", *args, **kwargs)


def popen_born(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "born", *args, **kwargs)


def run_coulomb(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "coulomb", *args, **kwargs)


def popen_coulomb(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "coulomb", *args, **kwargs)


def run_del2dx(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "del2dx", *args, **kwargs)


def popen_del2dx(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "del2dx", *args, **kwargs)


def run_dx2mol(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "dx2mol", *args, **kwargs)


def popen_dx2mol(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "dx2mol", *args, **kwargs)


def run_dx2uhbd(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "dx2uhbd", *args, **kwargs)


def popen_dx2uhbd(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "dx2uhbd", *args, **kwargs)


def run_dxmath(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "dxmath", *args, **kwargs)


def popen_dxmath(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "dxmath", *args, **kwargs)


def run_mergedx(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "mergedx", *args, **kwargs)


def popen_mergedx(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "mergedx", *args, **kwargs)


def run_mergedx2(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "mergedx2", *args, **kwargs)


def popen_mergedx2(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "mergedx2", *args, **kwargs)


def run_mgmesh(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "mgmesh", *args, **kwargs)


def popen_mgmesh(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "mgmesh", *args, **kwargs)


def run_similarity(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "similarity", *args, **kwargs)


def popen_similarity(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "similarity", *args, **kwargs)


def run_smooth(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "smooth", *args, **kwargs)


def popen_smooth(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "smooth", *args, **kwargs)


def run_tensor2dx(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "tensor2dx", *args, **kwargs)


def popen_tensor2dx(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "tensor2dx", *args, **kwargs)


def run_uhbd_asc2bin(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "uhbd_asc2bin", *args, **kwargs)


def popen_uhbd_asc2bin(*args, **kwargs):
    return _subprocess_with_env_and_bin(
        subprocess.Popen, "uhbd_asc2bin", *args, **kwargs
    )


def run_value(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.run, "value", *args, **kwargs)


def popen_value(*args, **kwargs):
    return _subprocess_with_env_and_bin(subprocess.Popen, "value", *args, **kwargs)
