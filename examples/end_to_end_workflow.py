"""End-to-end DICOMForge workflow with a fake pydicom backend.

The example mirrors a common commercial pipeline:

1. read a DICOM object through the pydicom adapter
2. verify pixel metadata before touching pixel bytes
3. apply a starter de-identification plan
4. write the output object
5. keep an audit report for downstream review

The fake backend keeps the example runnable without external files or optional
dependencies. In production, install `dicomforge[pydicom]` and call
`dicomforge.io.read` / `write` against real paths.
"""

from __future__ import annotations

import sys
import types

from dicomforge import AnonymizationPlan, PrivateTagAction, Tag
from dicomforge.io import read, write
from dicomforge.pixels import check_pixel_capability
from dicomforge.uids import SopClassUID, TransferSyntaxUID


class FakeTag:
    def __init__(self, group: int, element: int) -> None:
        self.group = group
        self.element = element


class FakeElement:
    def __init__(self, tag: Tag, value: object) -> None:
        self.tag = FakeTag(tag.group, tag.element)
        self.value = value


class FakeReadableDataset:
    def __init__(self) -> None:
        self.file_meta = [
            FakeElement(Tag.TransferSyntaxUID, TransferSyntaxUID.ExplicitVRLittleEndian),
        ]
        self._elements = [
            FakeElement(Tag.SOPClassUID, SopClassUID.SecondaryCaptureImageStorage),
            FakeElement(Tag.SOPInstanceUID, "1.2.826.0.1.3680043.10.100"),
            FakeElement(Tag.StudyInstanceUID, "1.2.826.0.1.3680043.10.1"),
            FakeElement(Tag.SeriesInstanceUID, "1.2.826.0.1.3680043.10.2"),
            FakeElement(Tag.PatientName, "Ada Lovelace"),
            FakeElement(Tag.PatientID, "MRN-123"),
            FakeElement(Tag.Rows, 2),
            FakeElement(Tag.Columns, 2),
            FakeElement(Tag.SamplesPerPixel, 1),
            FakeElement(Tag.PhotometricInterpretation, "MONOCHROME2"),
            FakeElement(Tag.BitsAllocated, 16),
            FakeElement(Tag.BitsStored, 12),
            FakeElement(Tag.HighBit, 11),
            FakeElement(Tag.PixelRepresentation, 0),
            FakeElement(Tag.PixelData, b"\x00\x00\x01\x00\x02\x00\x03\x00"),
            FakeElement(Tag(0x0011, 0x1001), "vendor private value"),
        ]

    def __iter__(self):
        return iter(self._elements)


class FakeWritableDataset:
    def __init__(self) -> None:
        self.file_meta = None
        self.elements = []
        self.saved_path = ""

    def add_new(self, tag, vr, value):
        self.elements.append((tag, vr, value))

    def save_as(self, path):
        self.saved_path = path


def install_fake_pydicom_backend() -> FakeWritableDataset:
    writable = FakeWritableDataset()
    fake_pydicom = types.SimpleNamespace(
        Dataset=lambda: writable,
        FileMetaDataset=FakeWritableDataset,
        dcmread=lambda *args, **kwargs: FakeReadableDataset(),
    )
    sys.modules["pydicom"] = fake_pydicom
    return writable


def main() -> None:
    written = install_fake_pydicom_backend()

    dataset = read("input.dcm")
    capability = check_pixel_capability(dataset)

    plan = AnonymizationPlan.starter_profile(
        uid_salt="customer-project-secret",
        private_tag_action=PrivateTagAction.REMOVE,
    )
    report = plan.apply_with_report(dataset)

    write("output.dcm", dataset)

    print(f"pixel codec: {capability.codec_name}")
    print(f"output path: {written.saved_path}")
    print(f"patient name: {dataset.get(Tag.PatientName)}")
    print(f"private tags removed: {report.private_tags_removed}")
    print(f"audit events: {len(report.events)}")


if __name__ == "__main__":
    main()
