from typing import Any, Dict
from ai_brain.chunker import Chunker
from ai_brain.chunker_char_text_splitter import ChunkerCharacterTextSplitter


class ChunkerFactory:

    def create_chunker(self,  params: Dict[str, Any]) -> Chunker:
        chunker_type = params.get(
            'chunker_type', 'ChunkerCharacterTextSplitter')
        if chunker_type == 'ChunkerCharacterTextSplitter':
            new_chunker = ChunkerCharacterTextSplitter(params)
            return new_chunker
        else:
            raise ValueError(f"Unknown chunker type: {chunker_type}")
