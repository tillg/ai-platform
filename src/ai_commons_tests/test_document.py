import unittest
import uuid
from ai_commons.apiModelsSearch import Document
from ai_commons.constants import TMP_DATA_DIR, TEST_DATA_DIR
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestDocument(unittest.TestCase):

    def test_document_initialization_wo_id(self):
        doc = Document(title="apple", content="Apple are red", uri="some_uri")
        self.assertEqual(doc.title, "apple")
        self.assertEqual(doc.content, "Apple are red")
        self.assertIsNotNone(doc.id)
        self.assertIsInstance(
            doc.id, str, "Document id is not a string")

    def test_document_initialization_with_id(self):
        doc_id = str(uuid.uuid4())
        doc = Document(title="apple", content="Apple are red",
                       uri="some_uri", id=doc_id)
        self.assertEqual(doc.title, "apple")
        self.assertEqual(doc.content, "Apple are red")
        self.assertEqual(doc.id, doc_id)

    def test_document_from_lc_document(self):
        from langchain.docstore.document import Document as lc_Document
        lc_doc = lc_Document(page_content="Apple are red", metadata={
                             "title": "apple", "source": "some_uri"})
        doc = Document.from_lc_document(lc_doc)
        self.assertEqual(doc.title, "apple")
        self.assertEqual(doc.content, "Apple are red")
        self.assertEqual(doc.uri, "some_uri")

    def test_document_to_lc_document(self):
        doc = Document(title="apple", content="Apple are red", uri="some_uri")
        lc_doc = doc.to_lc_document()
        self.assertEqual(lc_doc.page_content, "Apple are red")
        self.assertEqual(lc_doc.metadata, {
                         "uri": "some_uri", "title": "apple", "id": doc.id})

    def test_document_from_file(self):
        file_path = os.path.join(TEST_DATA_DIR, "wikipedia_peru.txt")
        with open(file_path, 'r', encoding='utf-8') as file:
            wikipedia_peru_content = file.read()

        doc = Document.from_text_file(file_path)
        self.assertEqual(doc.title, "wikipedia_peru")
        self.assertIsNotNone(doc.content)
        self.assertEqual(doc.uri, file_path)
        self.assertEqual(doc.content, wikipedia_peru_content)

    def test_document_from_json_file(self):
        file_path_for_sample_doc = os.path.join(TEST_DATA_DIR, "wikipedia_peru.txt")

        doc = Document.from_text_file(file_path_for_sample_doc)
        file_path_for_json_doc = os.path.join(TMP_DATA_DIR, "wikipedia_peru")
        logger.info(f"Writing doc to json file: {file_path_for_json_doc}")
        doc.write_2_json(file_path_for_json_doc)

        filename_for_json = Document.get_filename_by_id(file_path_for_json_doc, doc.id)

        doc_from_json = Document.from_json_file(filename_for_json)
        self.assertEqual(doc_from_json, doc)



if __name__ == '__main__':
    unittest.main()
