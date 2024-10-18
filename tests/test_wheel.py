from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

import pytest
from apbs_binary import (
    APBS_BIN_PATH,
    MULTIVALUE_BIN_PATH,
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

RETURN_CODE_NO_ARGS = [
    (run_apbs, popen_apbs, 13),
    (run_multivalue, popen_multivalue, 1),
    (run_analysis, popen_analysis, 2),
    (run_benchmark, popen_benchmark, 12),
    (run_born, popen_born, 154),
    (run_coulomb, popen_coulomb, 154),
    (run_del2dx, popen_del2dx, 1),
    (run_dx2mol, popen_dx2mol, 1),
    (run_dx2uhbd, popen_dx2uhbd, 1),
    (run_dxmath, popen_dxmath, 13),
    (run_mergedx, popen_mergedx, 255),
    (run_mergedx2, popen_mergedx2, 1),
    (run_mgmesh, popen_mgmesh, 0),
    (run_similarity, popen_similarity, 2),
    (run_smooth, popen_smooth, 2),
    (run_tensor2dx, popen_tensor2dx, 255),
    (run_uhbd_asc2bin, popen_uhbd_asc2bin, -11),
    (run_value, popen_value, 2),
]


@pytest.mark.parametrize(
    "bin_path",
    [
        APBS_BIN_PATH,
        MULTIVALUE_BIN_PATH,
    ],
)
def test_exists(bin_path: Path):
    assert bin_path.is_file()


@pytest.mark.parametrize(
    ("bin_path", "expected_name"),
    [
        (APBS_BIN_PATH, "apbs"),
        (MULTIVALUE_BIN_PATH, "multivalue"),
    ],
)
def test_name(bin_path: Path, expected_name: str):
    assert bin_path.name == expected_name or bin_path.name == expected_name + ".exe"


@pytest.mark.parametrize(
    ("run_func", "popen_func", "arg", "expected_return_code"),
    [
        (run_apbs, popen_apbs, "--help", 13),
        (run_apbs, popen_apbs, ["--help"], 13),
    ],
)
def test_execute_onearg(
    run_func: Callable,
    popen_func: Callable,
    arg: str | list[str],
    expected_return_code: int,
):
    """
    Test run_apbs and popen_apbs with --help option, str and list arguments.

    Note:
        multivalue does not have a --help option.
    """
    proc = run_func(arg)
    assert proc.returncode == expected_return_code

    proc = popen_func(arg)
    proc.wait()
    assert proc.returncode == expected_return_code


@pytest.mark.parametrize(
    ("run_func", "popen_func", "expected_return_code"),
    RETURN_CODE_NO_ARGS,
)
def test_execute_noarg(
    run_func: Callable, popen_func: Callable, expected_return_code: int
):
    proc = run_func("")
    assert proc.returncode == expected_return_code

    proc = popen_func("")
    proc.wait()
    assert proc.returncode == expected_return_code

    # below will fail the type checking but it should still run as expected.
    proc = run_func()
    assert proc.returncode == expected_return_code

    proc = popen_func()
    proc.wait()
    assert proc.returncode == expected_return_code


@pytest.mark.parametrize(
    ("run_func", "popen_func", "expected_return_code"),
    RETURN_CODE_NO_ARGS,
)
def test_process_run_noarg_with_env(
    run_func: Callable, popen_func: Callable, expected_return_code: int
):
    """
    In macOS, the env variable `DYLD_LIBRARY_PATH` is required to run the binaries. Thus, we check if custom env settings still respect this.
    """
    my_env = os.environ.copy()
    my_env["PATH"] = "/usr/local/bin"  # dummy change. Not important
    proc = run_func("", env=my_env)
    assert proc.returncode == expected_return_code

    proc = popen_func("", env=my_env)
    proc.wait()
    assert proc.returncode == expected_return_code


@pytest.mark.parametrize(
    ("run_func", "line_number", "line_match"),
    [
        (run_apbs, 3, r"APBS -- Adaptive Poisson-Boltzmann Solver"),
        (
            run_multivalue,
            2,
            r"Usage: multivalue <csvCoordinatesFile> <dxFormattedFile> <outputFile> [outputformat]",
        ),
    ],
)
def test_execute_noarg_message_stdout(
    run_func: Callable, line_number: int, line_match: str
):
    proc = run_func("", capture_output=True, text=True, encoding="utf-8")
    line = proc.stdout.splitlines()[line_number]
    assert line.strip() == line_match
