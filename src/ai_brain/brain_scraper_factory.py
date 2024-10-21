from typing import Any, Dict
from ai_brain.brain_scraper_wikipedia import BrainScraperWikipedia
from ai_brain.brain_scraper import BrainScraper


class BrainScraperFactory:

    def create_brain_scraper(self, parameters: Dict[str, Any]) -> BrainScraper:
        scraper_type = parameters.get("scraper_type", "wikipedia")
        if scraper_type == "wikipedia":
            new_scraper = BrainScraperWikipedia(parameters)
            return new_scraper
        # if scraper_type=="confluence":
        #     new_scraper = AiBrainImporterConfluence(brain, parameters)
        #     return new_scraper
        else:
            raise ValueError(f"Unknown scraper type: {scraper_type}")
