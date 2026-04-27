"""Transfer syntax classification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict


@dataclass(frozen=True)
class TransferSyntax:
    """DICOM transfer syntax metadata."""

    uid: str
    name: str
    is_little_endian: bool
    is_explicit_vr: bool
    is_encapsulated: bool = False

    _KNOWN: ClassVar[Dict[str, "TransferSyntax"]] = {}

    @property
    def is_compressed(self) -> bool:
        return self.is_encapsulated

    @classmethod
    def register(
        cls,
        uid: str,
        name: str,
        *,
        is_little_endian: bool,
        is_explicit_vr: bool,
        is_encapsulated: bool = False,
    ) -> "TransferSyntax":
        syntax = cls(uid, name, is_little_endian, is_explicit_vr, is_encapsulated)
        cls._KNOWN[uid] = syntax
        return syntax

    @classmethod
    def from_uid(cls, uid: str) -> "TransferSyntax":
        known = cls._KNOWN.get(uid)
        if known is not None:
            return known
        return cls(
            uid=uid,
            name=f"Unknown Transfer Syntax {uid}",
            is_little_endian=True,
            is_explicit_vr=True,
            is_encapsulated=True,
        )


TransferSyntax.register(
    "1.2.840.10008.1.2",
    "Implicit VR Little Endian",
    is_little_endian=True,
    is_explicit_vr=False,
)
TransferSyntax.register(
    "1.2.840.10008.1.2.1",
    "Explicit VR Little Endian",
    is_little_endian=True,
    is_explicit_vr=True,
)
TransferSyntax.register(
    "1.2.840.10008.1.2.1.99",
    "Deflated Explicit VR Little Endian",
    is_little_endian=True,
    is_explicit_vr=True,
)
TransferSyntax.register(
    "1.2.840.10008.1.2.2",
    "Explicit VR Big Endian",
    is_little_endian=False,
    is_explicit_vr=True,
)
TransferSyntax.register(
    "1.2.840.10008.1.2.4.50",
    "JPEG Baseline Process 1",
    is_little_endian=True,
    is_explicit_vr=True,
    is_encapsulated=True,
)
TransferSyntax.register(
    "1.2.840.10008.1.2.4.70",
    "JPEG Lossless",
    is_little_endian=True,
    is_explicit_vr=True,
    is_encapsulated=True,
)
TransferSyntax.register(
    "1.2.840.10008.1.2.4.80",
    "JPEG-LS Lossless",
    is_little_endian=True,
    is_explicit_vr=True,
    is_encapsulated=True,
)
TransferSyntax.register(
    "1.2.840.10008.1.2.4.90",
    "JPEG 2000 Lossless",
    is_little_endian=True,
    is_explicit_vr=True,
    is_encapsulated=True,
)
TransferSyntax.register(
    "1.2.840.10008.1.2.5",
    "RLE Lossless",
    is_little_endian=True,
    is_explicit_vr=True,
    is_encapsulated=True,
)
