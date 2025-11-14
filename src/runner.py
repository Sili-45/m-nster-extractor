thonimport json
import os
import logging
from extractors.monster_parser import MonsterParser
from outputs.exporters import JSONExporter

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_settings():
    config_path = os.path.join(os.path.dirname(__file__), "config", "settings.example.json")
    with open(config_path, "r") as f:
        return json.load(f)

def main():
    settings = load_settings()

    keywords_file = os.path.join(os.path.dirname(__file__), "..", "data", "inputs.sample.txt")
    with open(keywords_file, "r") as f:
        keywords = [line.strip() for line in f.readlines() if line.strip()]

    parser = MonsterParser()
    exporter = JSONExporter()

    all_results = []

    for kw in keywords:
        logging.info(f"Extracting job listings for keyword: {kw}")
        results = parser.search_jobs(kw, region=settings.get("region"))
        all_results.extend(results)

    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample.json")
    exporter.export_json(all_results, output_path)

    logging.info(f"Extraction complete. {len(all_results)} jobs saved to {output_path}")

if __name__ == "__main__":
    main()