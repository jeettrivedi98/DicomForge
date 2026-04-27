"""File IO adapters."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Union

from dicomforge.dataset import DicomDataset
from dicomforge.errors import MissingBackendError

PathLike = Union[str, Path]


def read(path: PathLike, *, stop_before_pixels: bool = False, force: bool = False) -> DicomDataset:
    """Read a DICOM file through the optional pydicom backend."""

    try:
        import pydicom  # type: ignore[import-not-found]
    except ImportError as exc:
        raise MissingBackendError(
            "Reading DICOM files requires the optional pydicom backend. "
            "Install with `pip install dicomforge[pydicom]`."
        ) from exc

    raw = pydicom.dcmread(str(path), stop_before_pixels=stop_before_pixels, force=force)
    dataset = DicomDataset()
    for element in raw:
        dataset.set((element.tag.group, element.tag.element), element.value)
    return dataset


def write(path: PathLike, dataset: DicomDataset, *, template: Any = None) -> None:
    """Write through pydicom using an optional template dataset."""

    try:
        import pydicom  # type: ignore[import-not-found]
    except ImportError as exc:
        raise MissingBackendError(
            "Writing DICOM files requires the optional pydicom backend. "
            "Install with `pip install dicomforge[pydicom]`."
        ) from exc

    raw = template if template is not None else pydicom.Dataset()
    for tag, value in dataset.items():
        raw.add_new((tag.group, tag.element), "UN", value)
    raw.save_as(str(path))
