import unittest
import uuid
from ai_commons.api_models import Chunk


class TestChunk(unittest.TestCase):

    def test_chunk_initialization_wo_id(self):
        chunk = Chunk(title="apple", content="Apple are red",
                      uri="some_uri", original_document_id="some_id")
        self.assertEqual(chunk.title, "apple")
        self.assertEqual(chunk.content, "Apple are red")
        self.assertIsNotNone(chunk.id)
        self.assertIsInstance(
            chunk.id, uuid.UUID, "chunk id is not a UUID instance")
        self.assertEqual(chunk.id.version, 4,
                         "chunk id is not a valid UUID4")
        self.assertEqual(chunk.original_document_id, "some_id")

    def test_chunk_initialization_with_id(self):
        doc_id = uuid.uuid4()
        chunk = Chunk(title="apple", content="Apple are red",
                      uri="some_uri", id=doc_id, original_document_id="some_id")
        self.assertEqual(chunk.title, "apple")
        self.assertEqual(chunk.content, "Apple are red")
        self.assertEqual(chunk.id, doc_id)
        self.assertEqual(chunk.original_document_id, "some_id")


if __name__ == '__main__':
    unittest.main()
