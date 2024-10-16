# https://stackoverflow.com/questions/59717828/copy-type-signature-from-another-function
# Needed to make subprocess.Popen or subprocess.run wrappers without modifying the signature
import subprocess
from collections.abc import Callable
from typing import Any, Generic, TypeVar

_F = TypeVar("_F", bound=Callable[..., Any])

# NOTE: it will return None and make the resulting function uncallable.
# Only use in TYPE_CHECKING block
class CopySignature(Generic[_F]):
    def __init__(self, target: _F) -> None: ...
    def __call__(self, wrapped: Callable[..., Any]) -> _F: ...

@CopySignature(subprocess.run)
def run_apbs(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_apbs(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_multivalue(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_multivalue(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_analysis(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_analysis(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_benchmark(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_benchmark(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_born(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_born(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_coulomb(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_coulomb(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_del2dx(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_del2dx(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_dx2mol(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_dx2mol(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_dx2uhbd(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_dx2uhbd(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_dxmath(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_dxmath(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_mergedx(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_mergedx(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_mergedx2(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_mergedx2(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_mgmesh(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_mgmesh(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_similarity(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_similarity(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_smooth(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_smooth(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_tensor2dx(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_tensor2dx(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_uhbd_asc2bin(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_uhbd_asc2bin(*args, **kwargs): ...
@CopySignature(subprocess.run)
def run_value(*args, **kwargs): ...
@CopySignature(subprocess.Popen)
def popen_value(*args, **kwargs): ...
