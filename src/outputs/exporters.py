thonimport json
import logging

class JSONExporter:
    def export_json(self, data, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logging.info(f"Exported {len(data)} records to {path}")
        except Exception as e:
            logging.error(f"Failed to write JSON output: {e}")