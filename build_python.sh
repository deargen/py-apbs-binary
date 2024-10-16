if [ "$#" -ne 2 ]; then
    echo "Build python wheels in a temp directory."
    echo "Usage: $0 <apbs_version> <py_package_version>"
    echo "Example: $0 3.4.1 3.4.1.post4"
    exit 1
fi

APBS_VERSION="$1"
PY_PACKAGE_VERSION="$2"

# use gsed on mac
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED="gsed"
else
    SED="sed"
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
mkdir -p "$SCRIPT_DIR/dist"

prepare_python_in_temp_dir() {
    TEMP_DIR=$(mktemp -d)
    PYTHON_BUILD_DIR="$TEMP_DIR/python"
    PYTHON_PACKAGE_DIR="$PYTHON_BUILD_DIR/src/apbs_binary"
    echo "Temp directory: $TEMP_DIR"
    echo "Python build directory: $PYTHON_BUILD_DIR"

    # copy the python project to the temp directory
    cp -r "$SCRIPT_DIR/python" "$TEMP_DIR"
    cp "$SCRIPT_DIR/README.md" "$PYTHON_BUILD_DIR"
    mkdir "$PYTHON_BUILD_DIR/src/apbs_binary/bin"

    # Replace version = "0.0.0" with the desired version
    $SED -i "s/version = \"0.0.0\"/version = \"$PY_PACKAGE_VERSION\"/g" "$PYTHON_BUILD_DIR/pyproject.toml" || { echo "Failure"; exit 1; }
    # Replace __version__ = "0.0.0" with the desired version
    $SED -i "s/__version__ = \"0.0.0\"/__version__ = \"$PY_PACKAGE_VERSION\"/g" "$PYTHON_PACKAGE_DIR/__init__.py" || { echo "Failure"; exit 1; }
}

build_wheel() {
    cd "$PYTHON_BUILD_DIR" || { echo "Failure"; exit 1; }
    pyproject-build --installer=uv --wheel
    wheel tags --python-tag py3 --abi-tag none --platform "$PLATFORM_NAME" dist/*.whl --remove
    mv "$PYTHON_BUILD_DIR/dist/"*.whl "$SCRIPT_DIR/dist"
}

# extract each binary in the temp directory
# 1. macosx_12_0_arm64
prepare_python_in_temp_dir

PLATFORM_NAME="macosx_12_0_arm64"
tar xvzf "$SCRIPT_DIR/data/apbs-$APBS_VERSION/macosx_12_0_arm64/apbs.tar.gz" -C "$TEMP_DIR"
tar xvzf "$SCRIPT_DIR/data/apbs-$APBS_VERSION/macosx_12_0_arm64/metis.tar.gz" -C "$TEMP_DIR"
mv "$TEMP_DIR/apbs/${APBS_VERSION}_2/bin/apbs" "$PYTHON_PACKAGE_DIR/bin"
mv "$TEMP_DIR/apbs/${APBS_VERSION}_2/share/apbs/tools/bin/"* "$PYTHON_PACKAGE_DIR/bin"
mkdir -p "$PYTHON_PACKAGE_DIR/lib"
mv "$TEMP_DIR/metis/5.1.0/lib/libmetis.dylib" "$PYTHON_PACKAGE_DIR/lib"

build_wheel

# 2. macosx_10_15_x86_64
prepare_python_in_temp_dir

PLATFORM_NAME="macosx_10_15_x86_64"
# unzip "$SCRIPT_DIR/data/apbs-${APBS_VERSION}/APBS-${APBS_VERSION}.Darwin.zip" -d "$TEMP_DIR"
# mv "$TEMP_DIR/APBS-${APBS_VERSION}.Darwin/bin/apbs" "$PYTHON_PACKAGE_DIR/bin"
# mv "$TEMP_DIR/APBS-${APBS_VERSION}.Darwin/share/apbs/tools/bin/"* "$PYTHON_PACKAGE_DIR/bin"
tar xvzf "$SCRIPT_DIR/data/apbs-$APBS_VERSION/macosx_10_15_x86_64/apbs.tar.gz" -C "$TEMP_DIR"
tar xvzf "$SCRIPT_DIR/data/apbs-$APBS_VERSION/macosx_10_15_x86_64/metis.tar.gz" -C "$TEMP_DIR"
mv "$TEMP_DIR/apbs/${APBS_VERSION}_2/bin/apbs" "$PYTHON_PACKAGE_DIR/bin"
mv "$TEMP_DIR/apbs/${APBS_VERSION}_2/share/apbs/tools/bin/"* "$PYTHON_PACKAGE_DIR/bin"
mkdir -p "$PYTHON_PACKAGE_DIR/lib"
mv "$TEMP_DIR/metis/5.1.0/lib/libmetis.dylib" "$PYTHON_PACKAGE_DIR/lib"

build_wheel

# 3. Linux
prepare_python_in_temp_dir

# NOTE: the actual platform is manylinux_2_30_x86_64, but it won't be compatible with uv pip compile.
# Thus we use manylinux_2_28_x86_64, for now.
# It will crash when running in Ubuntu 18.04 but still succeed to install.
PLATFORM_NAME="manylinux_2_28_x86_64"
# rm -rf "${PYTHON_PACKAGE_DIR:?}/bin"  # ${var:?} to ensure it doesn't expand to /bin !
# mkdir "$PYTHON_PACKAGE_DIR/bin"
unzip "$SCRIPT_DIR/data/apbs-${APBS_VERSION}/APBS-${APBS_VERSION}.Linux.zip" -d "$TEMP_DIR"
mv "$TEMP_DIR/APBS-${APBS_VERSION}.Linux/bin/apbs" "$PYTHON_PACKAGE_DIR/bin"
mv "$TEMP_DIR/APBS-${APBS_VERSION}.Linux/share/apbs/tools/bin/"* "$PYTHON_PACKAGE_DIR/bin"

build_wheel

# 4. Windows
# NOTE: failed to execute the binary because of lack of python39.dll
# and adding it to PATH didn't work.
# Thus, we disable windows, for now.
#
# prepare_python_in_temp_dir
#
# PLATFORM_NAME="win_amd64"
# # rm -rf "${PYTHON_PACKAGE_DIR:?}/bin"  # ${var:?} to ensure it doesn't expand to /bin !
# # mkdir "$PYTHON_PACKAGE_DIR/bin"
# unzip "$SCRIPT_DIR/data/apbs-${APBS_VERSION}/APBS-${APBS_VERSION}.Windows.zip" -d "$TEMP_DIR"
# mv "$TEMP_DIR/APBS-${APBS_VERSION}.Windows/bin/apbs.exe" "$PYTHON_PACKAGE_DIR/bin"
# mv "$TEMP_DIR/APBS-${APBS_VERSION}.Windows/bin/*.dll" "$PYTHON_PACKAGE_DIR/bin"
# mv "$TEMP_DIR/APBS-${APBS_VERSION}.Windows/share/apbs/tools/bin/Release/"*.exe "$PYTHON_PACKAGE_DIR/bin"
# cp "$SCRIPT_DIR/python39.dll" "$PYTHON_PACKAGE_DIR/bin"

build_wheel
