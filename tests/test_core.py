import unittest

from dicomforge import AnonymizationPlan, DicomDataset, Tag, TransferSyntax
from dicomforge.codecs import default_registry
from dicomforge.errors import UnsupportedTransferSyntaxError


class TagTests(unittest.TestCase):
    def test_parse_keyword_and_hex(self):
        self.assertEqual(Tag.parse("PatientName"), Tag.PatientName)
        self.assertEqual(Tag.parse("(0010,0010)"), Tag.PatientName)
        self.assertEqual(Tag.parse("00100010"), Tag.PatientName)

    def test_private_tag_detection(self):
        self.assertTrue(Tag(0x0011, 0x1001).is_private)
        self.assertFalse(Tag.PatientName.is_private)


class DatasetTests(unittest.TestCase):
    def test_dataset_normalizes_tags(self):
        dataset = DicomDataset({"PatientName": "Ada"})
        self.assertEqual(dataset.get(Tag.PatientName), "Ada")
        dataset[(0x0008, 0x0060)] = "MR"
        self.assertEqual(dataset.get("Modality"), "MR")

    def test_anonymization_plan(self):
        dataset = DicomDataset({"PatientName": "Ada", "PatientID": "123", (0x0011, 0x1001): "secret"})
        AnonymizationPlan.basic_profile().apply(dataset)
        self.assertEqual(dataset.get("PatientName"), "Anonymous")
        self.assertEqual(dataset.get("PatientID"), "ANON")
        self.assertIsNone(dataset.get((0x0011, 0x1001)))


class TransferSyntaxTests(unittest.TestCase):
    def test_known_transfer_syntax(self):
        syntax = TransferSyntax.from_uid("1.2.840.10008.1.2.1")
        self.assertTrue(syntax.is_little_endian)
        self.assertTrue(syntax.is_explicit_vr)
        self.assertFalse(syntax.is_compressed)

    def test_unknown_transfer_syntax_is_safe_default(self):
        syntax = TransferSyntax.from_uid("1.2.3")
        self.assertTrue(syntax.is_encapsulated)
        self.assertIn("Unknown", syntax.name)


class CodecRegistryTests(unittest.TestCase):
    def test_default_registry_supports_uncompressed(self):
        registry = default_registry()
        syntax = TransferSyntax.from_uid("1.2.840.10008.1.2.1")
        self.assertTrue(registry.supports(syntax))

    def test_default_registry_rejects_jpeg2000(self):
        registry = default_registry()
        syntax = TransferSyntax.from_uid("1.2.840.10008.1.2.4.90")
        with self.assertRaises(UnsupportedTransferSyntaxError):
            registry.find(syntax)


if __name__ == "__main__":
    unittest.main()
