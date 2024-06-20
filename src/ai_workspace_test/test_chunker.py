import unittest
import uuid
from ai_workspace.chunker import Chunker


class TestChunker(unittest.TestCase):

    def test_chunker_initialization(self):
        chunker = Chunker()
        # self.assertEqual(chunk.title, "apple")
        # self.assertEqual(chunk.content, "Apple are red")
        # self.assertIsNotNone(chunk.id)
        # self.assertIsInstance(
        #     chunk.id, uuid.UUID, "chunk id is not a UUID instance")
        # self.assertEqual(chunk.id.version, 4,
        #                  "chunk id is not a valid UUID4")
        # self.assertEqual(chunk.original_document_id, "some_id")


if __name__ == '__main__':
    unittest.main()
