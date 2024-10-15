import unittest
import uuid
from ai_commons.apiModelsSearch import Chunk, SearchResultChunksAndDocuments


class TestChunk(unittest.TestCase):

    def test_chunk_initialization_wo_id(self):
        original_document_id = str(uuid.uuid4())
        chunk = Chunk(
            title="apple",
            content="Apple are red",
            uri="some_uri",
            original_document_id=original_document_id,
        )
        self.assertEqual(chunk.title, "apple")
        self.assertEqual(chunk.content, "Apple are red")
        self.assertIsNotNone(chunk.id)
        self.assertIsInstance(chunk.id, str, "chunk id is not a string")
        self.assertEqual(chunk.original_document_id, original_document_id)

    def test_chunk_initialization_with_id(self):
        doc_id = str(uuid.uuid4())
        original_document_id = str(uuid.uuid4())
        chunk = Chunk(
            title="apple",
            content="Apple are red",
            uri="some_uri",
            id=doc_id,
            original_document_id=original_document_id,
        )
        self.assertEqual(chunk.title, "apple")
        self.assertEqual(chunk.content, "Apple are red")
        self.assertEqual(chunk.id, doc_id)
        self.assertEqual(chunk.original_document_id, original_document_id)

    def test_chunk_as_str(self):
        doc_id = str(uuid.uuid4())
        original_document_id = str(uuid.uuid4())
        chunk1 = Chunk(
            title="apple",
            content="Apple are red",
            uri="some_uri",
            id=doc_id,
            original_document_id=original_document_id,
        )
        chunk2 = Chunk(
            title="banana",
            content="Bananas are krumm",
            uri="some_uri",
            id=doc_id,
            original_document_id=original_document_id,
        )
        chunk3 = Chunk(
            title="orange",
            content="Oranges are round",
            uri="some_uri",
            id=doc_id,
            original_document_id=original_document_id,
        )
        search_res_chunks = SearchResultChunksAndDocuments(
            chunks=[chunk1, chunk2, chunk3], documents=[]
        )
        context = search_res_chunks.chunks_as_str("--")
        self.assertEqual(context, "Apple are red--Bananas are krumm--Oranges are round")


if __name__ == "__main__":
    unittest.main()
