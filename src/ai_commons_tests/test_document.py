import unittest
import uuid
from ai_commons.api_models import Document



class TestDocument(unittest.TestCase):

    def test_document_initialization_wo_id(self):
        doc = Document(title="apple", content="Apple are red", uri="some_uri")
        self.assertEqual(doc.title, "apple")
        self.assertEqual(doc.content, "Apple are red")
        self.assertIsNotNone(doc.id)
        self.assertIsInstance(
        doc.id, uuid.UUID, "Document id is not a UUID instance")
        self.assertEqual(doc.id.version, 4, "Document id is not a valid UUID4")

    def test_document_initialization_with_id(self):
        doc_id = uuid.uuid4()
        doc = Document(title="apple", content="Apple are red", uri="some_uri", id=doc_id)
        self.assertEqual(doc.title, "apple")
        self.assertEqual(doc.content, "Apple are red")
        self.assertEqual(doc.id, doc_id)

    def test_document_from_lc_document(self):
        from langchain.docstore.document import Document as lc_Document
        lc_doc = lc_Document(page_content="Apple are red", metadata={"title": "apple", "source": "some_uri"})
        doc = Document.from_lc_document(lc_doc)
        self.assertEqual(doc.title, "apple")
        self.assertEqual(doc.content, "Apple are red")
        self.assertEqual(doc.uri, "some_uri")

    def test_document_to_lc_document(self):
        doc = Document(title="apple", content="Apple are red", uri="some_uri")
        lc_doc = doc.to_lc_document()
        self.assertEqual(lc_doc.page_content, "Apple are red")
        self.assertEqual(lc_doc.metadata, {"source": "some_uri", "title": "apple", "id": doc.id})
        
if __name__ == '__main__':
    unittest.main()
