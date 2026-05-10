# Changelog

All notable changes to DicomForge are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

## [0.6.0] — 2026-05-05

### Added
- `dicomforge.adapt` — adoption-layer integration adapters:
  - `from_pydicom` / `to_pydicom` — bidirectional pydicom Dataset conversion
  - `pixel_array` — numpy array from uncompressed PixelData with correct dtype
  - `to_pil_image` — PIL Image with automatic VOI windowing and MONOCHROME1 inversion
  - `to_json` / `from_json` — DICOM JSON Model round-trip
  - `from_pynetdicom_event` — extract DicomDataset from a pynetdicom event
- `dicomforge.api` — high-level convenience API:
  - `DicomFile` — lazy-loading file wrapper with named property access for 30+ tags
  - `quick_anonymize` — read → de-identify → write in one call
  - `validate_dataset` — structural validation with human-readable issue list
  - `batch_anonymize` — anonymize a file list; partial failures are isolated
- 55 additional `Tag` keywords (SeriesNumber, BodyPartExamined, PixelSpacing,
  ImagePositionPatient, Manufacturer, AttendingPhysicianName, and more)
- 20+ additional `SopClassUID` constants (PET, NM, US, RT, SR, WSI, enhanced CT/MR)
- 6 additional `TransferSyntaxUID` constants (JPEG 2000 lossy, JPEG-LS near-lossless,
  HT-JPEG 2000 lossless and lossy)
- 6 additional registered `TransferSyntax` entries
- `network` and `all` optional dependency extras in `pyproject.toml`
- `DicomDataset.copy()` and `DicomDataset.__repr__`
- `Tag.__repr__` returns keyword name when available (e.g. `Tag.PatientName`)

### Changed
- `AnonymizationPlan.starter_profile` expanded from 27 to 48 de-identification rules,
  adding patient weight/size/comments, ethnic group, smoking/pregnancy status,
  attending/requesting physician, device serial number, and department name
- `UidRemapper` is now thread-safe (internal cache protected by `threading.Lock`)
- `UidRemapper` now also remaps `MediaStorageSOPInstanceUID` and `ReferencedSOPInstanceUID`
- `default_registry()` now returns a cached singleton instead of a new instance per call
- `io.write` prefers `pydicom.dcmwrite()` on pydicom ≥ 3.0 (avoids deprecation warning)
- Network `_read_message` and `_write_message` now enforce a 30-second timeout and a
  64 MiB maximum message size
- All public pixel helper functions (`rescale_values`, `is_monochrome`, `voi_window_bounds`,
  `apply_voi_window_from_dataset`, etc.) are now exported from `dicomforge` top level
- `pyproject.toml` version bumped to 0.6.0; development status promoted to Beta

### Fixed
- `assert_pixel_data_length` incorrectly validated the last byte of even-length
  pixel data as a padding byte, causing `PixelMetadataError` for any dataset
  whose last pixel value was non-zero

---

## [0.5.0] — 2025-01-01

### Added
- `dicomforge.dicomweb` — dependency-free DICOMweb client:
  - QIDO-RS query builder (`QidoQuery`)
  - WADO-RS study/series/instance retrieval
  - STOW-RS multipart upload
  - DICOM JSON Model conversion (`dataset_from_dicom_json`, `dataset_to_dicom_json`)
  - `parse_multipart_related` / `build_multipart_related`
  - Injectable `DicomwebTransport` protocol with stdlib `UrllibDicomwebTransport`
- `dicomforge.network` — async DIMSE-style services:
  - `Association` client with C-ECHO, C-FIND, C-MOVE, C-STORE
  - `DimseServer` SCP with backpressure-aware C-STORE queue
  - `open_association` / `start_dimse_server` convenience helpers
  - `AssociationRejectedError`, `AssociationClosedError`
- DICOMweb integration: `dataset_to_message` / `dataset_from_message` with
  base64-encoded binary and nested dataset support

---

## [0.4.0] — 2024-10-01

### Added
- `dicomforge.network` initial implementation (async association lifecycle,
  C-ECHO, JSON framing)
- `DimseStatus` with class-level constants (SUCCESS, PENDING, CANCEL, UNABLE_TO_PROCESS)
- `AssociationRequest` frozen dataclass

---

## [0.3.0] — 2024-07-01

### Added
- `dicomforge.anonymize` — de-identification engine:
  - `AnonymizationPlan` with `starter_profile()` and `basic_profile()` factory methods
  - `UidRemapper` with SHA-256 deterministic remapping
  - `AnonymizationReport` / `AnonymizationEvent` audit trail
  - `PrivateTagAction` (REMOVE / KEEP)
  - Recursive sequence processing

---

## [0.2.0] — 2024-04-01

### Added
- `dicomforge.pixels` — pixel metadata and safety layer:
  - `FrameMetadata` with `from_dataset` and eager validation
  - `check_pixel_capability` — metadata + codec pre-flight check
  - `PixelCapability`, `VoiLut`
  - `rescale_value`, `apply_voi_window`, photometric interpretation helpers
- `dicomforge.io` — optional pydicom read/write backend

---

## [0.1.0] — 2024-01-01

### Added
- `dicomforge.tags` — `Tag` frozen dataclass with keyword registry and multi-format parser
- `dicomforge.dataset` — `DicomDataset` (MutableMapping with tag normalization)
- `dicomforge.transfer_syntax` — `TransferSyntax` registry with safe unknown defaults
- `dicomforge.codecs` — `CodecRegistry` and `Codec` capability model
- `dicomforge.errors` — `DicomForgeError` hierarchy
- `dicomforge.uids` — `SopClassUID`, `TransferSyntaxUID`, `ImplementationUID`, `DimseStatusCode`
- CI matrix: Python 3.9–3.13 on GitHub Actions
- MIT license, CONTRIBUTING.md, SECURITY.md, architecture and conformance docs
