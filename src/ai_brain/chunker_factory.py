from typing import Any, Dict
from ai_brain.chunker import Chunker
from ai_brain.chunker_char_text_splitter import ChunkerCharacterTextSplitter


class ChunkerFactory:

    def create_chunker(self, parameters: Dict[str, Any]) -> Chunker:
        chunker_type = parameters.get("chunker_type", "character_text_splitter")
        if chunker_type == "character_text_splitter":
            new_chunker = ChunkerCharacterTextSplitter(parameters)
            return new_chunker
        else:
            raise ValueError(f"Unknown chunker type: {chunker_type}")
