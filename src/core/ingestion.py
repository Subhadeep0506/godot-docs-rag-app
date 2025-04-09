from typing import List

from langchain.document_loaders.readthedocs import ReadTheDocsLoader
from langchain.schema import Document
from langchain.vectorstores.base import VectorStore


class Ingestion:
    def __init__(self, data_path: str, vectorstore: VectorStore):
        self.loader = ReadTheDocsLoader(
            path=data_path,
            exclude_links_ratio=0.5,
        )
        self.vectorstore = vectorstore

    def _inject_metadata(self, pages: List[Document]) -> List[Document]:
        def get_category(source: str) -> str:
            category = source.split("latest/")[-1].split("/")[0]
            return category

        for page in pages:
            page.metadata = {
                "category": get_category(page.metadata["source"]),
                "source": page.metadata["source"].split("latest/")[-1],
            }
        return pages

    def ingest(self):
        pages = self.loader.load()
        pages = self._inject_metadata(pages)

        self.vectorstore.add_documents(
            documents=pages,
        )
