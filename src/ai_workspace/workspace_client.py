class WorkspaceClient:

    def search(self, query: str, top: int = 5):
        """A search API to find docs based on a query."""
        searcher = searcher.Searcher()
        results = await searcher.search(query, top=top)
        return results