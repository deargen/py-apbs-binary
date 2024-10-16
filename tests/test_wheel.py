import os
from collections.abc import Callable
from pathlib import Path

import pytest
from apbs_binary import (
    APBS_BIN_PATH,
    MULTIVALUE_BIN_PATH,
    apbs,
    multivalue,
    process_run,
)

RETURN_CODE_NO_ARGS = [
    ("apbs", 13),
    ("multivalue", 1),
    ("analysis", 2),
    ("benchmark", 12),
    ("born", 154),
    ("coulomb", 154),
    ("del2dx", 1),
    ("dx2mol", 1),
    ("dx2uhbd", 1),
    ("dxmath", 13),
    ("mergedx", 255),
    ("mergedx2", 1),
    ("mgmesh", 0),
    ("similarity", 2),
    ("smooth", 2),
    ("tensor2dx", 255),
    ("uhbd_asc2bin", -11),
    ("value", 2),
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


def test_execute_help():
    """
    Note:
        multivalue does not have a --help option.
    """
    return_code = apbs("--help")
    assert return_code == 13


@pytest.mark.parametrize(
    ("func", "expected_return_code"),
    [
        (apbs, 13),
        (multivalue, 1),
    ],
)
def test_execute_noarg(func: Callable, expected_return_code: int):
    return_code = func()
    assert return_code == expected_return_code


@pytest.mark.parametrize(
    ("bin_name", "expected_return_code"),
    RETURN_CODE_NO_ARGS,
)
def test_process_run_noarg(bin_name: str, expected_return_code: int):
    return_code = process_run(bin_name)
    assert return_code == expected_return_code


@pytest.mark.parametrize(
    ("bin_name", "expected_return_code"),
    RETURN_CODE_NO_ARGS,
)
def test_process_run_noarg_with_env(bin_name: str, expected_return_code: int):
    """
    In macOS, the env variable `DYLD_LIBRARY_PATH` is required to run the binaries. Thus, we check if custom env settings still respect this.
    """
    my_env = os.environ.copy()
    my_env["PATH"] = "/usr/local/bin"  # dummy change. Not important
    return_code = process_run(bin_name, env=my_env)
    assert return_code == expected_return_code


@pytest.mark.parametrize(
    ("func", "line_number", "line_match"),
    [
        (apbs, 3, r"APBS -- Adaptive Poisson-Boltzmann Solver"),
        (
            multivalue,
            2,
            r"Usage: multivalue <csvCoordinatesFile> <dxFormattedFile> <outputFile> [outputformat]",
        ),
    ],
)
def test_execute_noarg_message_stdout(
    func: Callable, line_number: int, line_match: str
):
    proc = func(return_completed_process=True, capture_output=True, text=True)
    print(proc)
    if isinstance(proc.stdout, bytes):
        lines = proc.stdout.decode("utf-8")
    else:
        lines = proc.stdout
    line = lines.splitlines()[line_number]
    assert line.strip() == line_match
