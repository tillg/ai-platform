from typing import Any, Dict
from ai_brain_importer.ai_brain_importer import AiBrainImporter
from ai_brain_importer.ai_brain_importer_wikipedia import AiBrainImporterWikipedia
from ai_brain.brain import Brain

class BrainImporterFactory:

    def create_brain_importer(self, brain: Brain, params: Dict[str, Any]) -> AiBrainImporter:
        importer_type = params.get("importer_type", "wikipedia")
        if importer_type == "wikipedia":
            new_importer = AiBrainImporterWikipedia(brain, params)
            return new_importer
        else:
            raise ValueError(f"Unknown importer type: {importer_type}")
