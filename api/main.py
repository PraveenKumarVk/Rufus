from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import openai
import os
import re

app = FastAPI()
RUFUS_API_KEY = "ax-8yewdbiubc-ajdb93"
class ScrapeRequest(BaseModel):
    prompt: str
# Validate API key function
def validate_api_key(authorization: str = Header(None)):
    if authorization != RUFUS_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
class RufusAI:
    def __init__(self, api_key, google_api_key, google_cx):
        self.llm = openai.ChatCompletion.create  # Initialize OpenAI completion
        self.google_api_key = google_api_key
        self.google_cx = google_cx
        openai.api_key = api_key

    def extract_website_from_prompt(self, prompt):
        url_pattern = re.compile(r'https?://[^\s]+')
        match = url_pattern.search(prompt)
        if match:
            return match.group(0)
        else:
            return None

    def analyze_prompt_with_ai(self, prompt):
        query = f"Extract relevant search keywords from this query: '{prompt}'"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            max_tokens=50
        )
        return response.choices[0].text.strip()

    def search_websites(self, keywords):
        search_url = f"https://www.googleapis.com/customsearch/v1?key={self.google_api_key}&cx={self.google_cx}&q={keywords}"
        response = requests.get(search_url)
        if response.status_code == 200:
            search_results = response.json()
            return [item['link'] for item in search_results.get('items', [])]
        else:
            print(f"Error fetching search results: {response.status_code}")
            return []

    def fetch_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def extract_relevant_content(self, html, prompt):
        soup = BeautifulSoup(html, 'html.parser')
        sections = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
            section_text = tag.get_text(strip=True)
            if section_text:
                sections.append(section_text)

        relevant_content = self.filter_and_rank(sections, prompt)
        return relevant_content

    def filter_and_rank(self, sections, prompt):
        relevant_content = []
        for section in sections:
            query = f"Is the following content relevant to the query '{prompt}'?\n\nContent: {section}"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=query,
                max_tokens=50
            )
            relevance = response.choices[0].text.strip().lower()
            if 'yes' in relevance or 'relevant' in relevance:
                relevant_content.append(section)

        return relevant_content

    def scrape(self, prompt):
        user_provided_website = self.extract_website_from_prompt(prompt)

        if user_provided_website:
            html = self.fetch_page(user_provided_website)
            if html:
                relevant_content = self.extract_relevant_content(html, prompt)
                return relevant_content
            return []

        else:
            keywords = self.analyze_prompt_with_ai(prompt)
            websites = self.search_websites(keywords)
            all_relevant_content = []

            for website in websites:
                html = self.fetch_page(website)
                if html:
                    relevant_content = self.extract_relevant_content(html, prompt)
                    all_relevant_content.extend(relevant_content)

            return all_relevant_content

# Initialize Rufus
os.environ['OPENAI_API_KEY'] = "sk-N1nj_B13pzTctbuUxaSiEzEgMNhZUcetLSf_GQZAmtT3BlbkFJEBttXqcVHsJPSzzKCT6WDpjO4XLDFT9boN_-xkV1sA"
os.environ['GOOGLE_API_KEY'] = "AIzaSyDvuO88AVR1wRjwX0CTGLRiCSUDlpUVu-4"
os.environ['GOOGLE_CX'] = "a0694e2a9ba594e16"


openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cx = os.getenv("GOOGLE_CX")
rufus = RufusAI(openai_api_key, google_api_key, google_cx)

@app.post("/scrape/")
def scrape(request: ScrapeRequest):
    """
    API endpoint for scraping based on a user-provided prompt.
    """
    return {"content": rufus.scrape(request.prompt)}
