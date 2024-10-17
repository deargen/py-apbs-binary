# pip install apbs-binary (Unofficial binary distribution of APBS)

[![image](https://img.shields.io/pypi/v/apbs-binary.svg)](https://pypi.python.org/pypi/apbs-binary)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/apbs-binary)](https://pypistats.org/packages/apbs-binary)
[![image](https://img.shields.io/pypi/l/apbs-binary.svg)](https://pypi.python.org/pypi/apbs-binary)
[![image](https://img.shields.io/pypi/pyversions/apbs-binary.svg)](https://pypi.python.org/pypi/apbs-binary)


Install and use [APBS](https://github.com/Electrostatics/apbs) with ease in Python.

```bash
pip install apbs-binary
```

```python
from apbs_binary import APBS_BIN_PATH, MULTIVALUE_BIN_PATH, apbs, multivalue, process_run

# Run apbs
print(APBS_BIN_PATH)
apbs("--help")

# Run multivalue
print(MULTIVALUE_BIN_PATH)
multivalue()
```

The other tools are also available, but not all of them have the function wrappers. Use as `apbs_binary.process_run("analysis", "--help")` for example.

Supported platforms:

- Linux x86_64 (Ubuntu 20.04 +)
- MacOS x86_64 (11.6+), arm64 (12.0+)

> [!NOTE]
> Installing the package does NOT put the binary in $PATH.  
> Instead, the API will tell you where it is located.

## 👨‍💻️ Maintenance Notes

### Releasing a new version with CI (recommended)

Go to Github Actions and run the `Build and Release` workflow.

Version rule:

3.4.1.2:

- 3.4.1 is the APBS version
- the last digit (.2) is the patch/build number. It increases as we rebuild the wheels with different configurations or update the python API.


### Running locally

This section describes how it works.

To run it locally, first install the dependencies:

```bash
pip install uv --user --break-system-packages
uv tool install wheel
uv tool install build
uv tool install huggingface_hub

# Mac
brew install gnu-sed
```

Download the built binaries into `data/`:

```bash
huggingface-cli download --repo-type dataset --local-dir data Deargen/py-apbs-binary
```

Build four wheels on all platforms. Basically it will put the binaries in the `src/apbs_binary/bin/` folder and then build the wheels in a temp directory, outputting the wheels to `dist/`.

```bash
# first arg: APBS version to find in `data/` (i.e. data/apbs-3.4.1/APBS-3.4.1.Linux)
# second arg: wheel version
bash build_python.sh 3.4.1 3.4.1.2
```

Test the wheel

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements_test.txt
uv pip install build_python/dist/*.whl    # choose the wheel for your platform only.
pytest
```

### Notes

- The official 3.4.1 binary is not static and depends on python39.dll, libpython3.9.so.1.0, etc. on Windows and Mac (Linux seems fine)
- `brew install brewsci/bio/apbs` is not static either and depends on libmetis.dylib.
- In this repository, we use the brew-created binary for macOS and the official binary for Linux. We don't support Windows yet.
