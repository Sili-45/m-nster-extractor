thonimport logging
import requests
from bs4 import BeautifulSoup
from extractors.utils_formatting import clean_text

class MonsterParser:
    BASE_URL = "https://www.monster.com/jobs/search/"

    def _fetch(self, query, region=None):
        params = {"q": query}
        if region:
            params["where"] = region

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.error(f"Failed to fetch job listings: {e}")
            return ""

    def search_jobs(self, query, region=None):
        html = self._fetch(query, region)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        listings = soup.select("section.card-content")

        results = []

        for item in listings:
            try:
                title_el = item.select_one("h2.title")
                company_el = item.select_one("div.company")
                location_el = item.select_one("div.location")
                link_el = item.select_one("a")

                job = {
                    "job_title": clean_text(title_el.text if title_el else ""),
                    "company_name": clean_text(company_el.text if company_el else ""),
                    "location": clean_text(location_el.text if location_el else ""),
                    "job_description": "",
                    "job_url": link_el["href"] if link_el and link_el.get("href") else "",
                    "date_posted": "",
                    "employment_type": "",
                    "salary": "",
                    "category": "",
                    "id": clean_text(link_el["href"].split("-")[-1]) if link_el and link_el.get("href") else "",
                }
                results.append(job)
            except Exception as e:
                logging.warning(f"Error parsing job entry: {e}")

        return results