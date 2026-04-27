"""A small typed dataset wrapper."""

from __future__ import annotations

from collections.abc import Iterator, MutableMapping
from typing import Any, Dict, Optional

from dicomforge.tags import Tag, TagInput


class DicomDataset(MutableMapping[Tag, Any]):
    """Dictionary-like DICOM dataset with typed tag normalization."""

    def __init__(self, values: Optional[Dict[TagInput, Any]] = None) -> None:
        self._values: Dict[Tag, Any] = {}
        if values:
            for tag, value in values.items():
                self.set(tag, value)

    def set(self, tag: TagInput, value: Any) -> None:
        self._values[Tag.parse(tag)] = value

    def get(self, tag: TagInput, default: Any = None) -> Any:
        return self._values.get(Tag.parse(tag), default)

    def require(self, tag: TagInput) -> Any:
        parsed = Tag.parse(tag)
        if parsed not in self._values:
            raise KeyError(f"Required DICOM tag {parsed} is missing")
        return self._values[parsed]

    def remove_private_tags(self) -> int:
        private_tags = [tag for tag in self._values if tag.is_private]
        for tag in private_tags:
            del self._values[tag]
        return len(private_tags)

    def __getitem__(self, key: TagInput) -> Any:
        return self._values[Tag.parse(key)]

    def __setitem__(self, key: TagInput, value: Any) -> None:
        self.set(key, value)

    def __delitem__(self, key: TagInput) -> None:
        del self._values[Tag.parse(key)]

    def __iter__(self) -> Iterator[Tag]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def to_plain_dict(self) -> Dict[str, Any]:
        """Return a serializable dictionary keyed by canonical tag strings."""

        return {str(tag): value for tag, value in sorted(self._values.items())}
