import unittest
import uuid
from ai_commons.apiModelsSearch import Chunk


class TestChunk(unittest.TestCase):

    def test_chunk_initialization_wo_id(self):
        original_document_id = str(uuid.uuid4())
        chunk = Chunk(title="apple", content="Apple are red",
                      uri="some_uri", original_document_id=original_document_id)
        self.assertEqual(chunk.title, "apple")
        self.assertEqual(chunk.content, "Apple are red")
        self.assertIsNotNone(chunk.id)
        self.assertIsInstance(
            chunk.id, str, "chunk id is not a string")
        self.assertEqual(chunk.original_document_id, original_document_id)

    def test_chunk_initialization_with_id(self):
        doc_id = str(uuid.uuid4())
        original_document_id = str(uuid.uuid4())
        chunk = Chunk(title="apple", content="Apple are red",
                      uri="some_uri", id=doc_id, original_document_id=original_document_id)
        self.assertEqual(chunk.title, "apple")
        self.assertEqual(chunk.content, "Apple are red")
        self.assertEqual(chunk.id, doc_id)
        self.assertEqual(chunk.original_document_id, original_document_id)


if __name__ == '__main__':
    unittest.main()
