"""Module for scraping and processing sports news from Index.hr."""
import os
from datetime import datetime
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Base link for the website
link = 'https://www.index.hr/'
output_dir = "data"

# Set up logging
log_file_path = os.path.join(output_dir, "process_log.txt")

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_file_path, mode='w', encoding='utf-8'),
                              logging.StreamHandler()])
logger = logging.getLogger()

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Fetch and save the main page content
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
file_name = f"Index_{timestamp}.txt"
file_path = os.path.join(output_dir, file_name)

try:
    logger.info("Fetching content from: %s", link)
    response = requests.get(link, timeout=60)
    response.raise_for_status()

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response.text)

    logger.info("Content fetched and saved to: %s", file_path)

except requests.RequestException as e:
    logger.error("Error fetching content: %s", e)


def extract_sports_categories(file_paths):
    """Extract sports categories and their links from the saved HTML file."""
    try: 
        with open(file_paths, "r", encoding="utf-8") as files:
            content = files.read()

        soup = BeautifulSoup(content, "html.parser")

        sport_categories = {}
        menu_items = soup.select("ul.scroll-menu li.scroll-menu-item a.sport-text-hover")

        for item in menu_items:
            sport_name = item.text.strip()
            sport_link = item.get("href")
            if sport_link:
                sport_categories[sport_name] = link.rstrip('/') + sport_link

        return sport_categories
    
    except FileNotFoundError:
        logger.error("File %s not found.", file_paths)
        return {}


def fetch_and_save_category_data(sport_categories):
    """Fetch and save the HTML content for each sports category."""
    for category, category_link in sport_categories.items():
        try:
            logger.info("Fetching data for category: %s from %s", category, category_link)
            response = requests.get(category_link, timeout=60)
            response.raise_for_status()

            safe_category_name = category.replace(" ", "_").replace("/", "_")
            file_name_category = f"{safe_category_name}.txt"
            file_path_category = os.path.join(output_dir, file_name_category)

            with open(file_path_category, "w", encoding="utf-8") as files:
                files.write(response.text)

            logger.info("Data for category '%s' saved to %s", category, file_path_category)

        except requests.RequestException as e:
            logger.error("Error fetching data for category '%s': %s", category, e)


sports_categories = extract_sports_categories(file_path)

if sports_categories:
    logger.info("Sports Categories Found:")
    for category, category_url in sports_categories.items():
        logger.info(" - %s: %s", category, category_url)
    fetch_and_save_category_data(sports_categories)
else:
    logger.info("No sports categories found.")


def extract_news_from_file(file_path_category):
    """Extract news items for a specific sports category from its saved HTML file."""
    news_data = []

    try:
        with open(file_path_category, "r", encoding="utf-8") as files:
            content = files.read()

        soup = BeautifulSoup(content, "html.parser")

        # Extract the main news item
        first_news = soup.select_one("div.first-news-holder.vertical a")
        if first_news:
            title = first_news.select_one("div.content-holder h2.title").get_text(strip=True) if first_news.select_one("div.content-holder h2.title") else "No Title"
            summary = first_news.select_one("div.content-holder p.summary").get_text(strip=True) if first_news.select_one("div.content-holder p.summary") else "No Summary"
            publish_date = first_news.select_one("div.content-holder div.publish-date").get_text(strip=True) if first_news.select_one("div.content-holder div.publish-date") else "No Date"
            links = first_news["href"]
            news_data.append({
                "Title": title,
                "Summary": summary,
                "Publish Date": publish_date,
                "URL": f"https://www.index.hr{links}" if links.startswith("/") else links
            })

        # Extract additional news items
        other_news = soup.select("div.grid-item a")
        for news_item in other_news[:4]: 
            title = news_item.select_one("div.content h3.title").get_text(strip=True) if news_item.select_one("div.content h3.title") else "No Title"
            summary = news_item.select_one("div.content span.summary").get_text(strip=True) if news_item.select_one("div.content span.summary") else "No Summary"
            publish_date = news_item.select_one("div.content div.publish-date").get_text(strip=True) if news_item.select_one("div.content div.publish-date") else "No Date"
            links = news_item["href"]
            news_data.append({
                "Title": title,
                "Summary": summary,
                "Publish Date": publish_date,
                "URL": f"https://www.index.hr{links}" if links.startswith("/") else links
            })

    except FileNotFoundError:
        logger.error("File not found: %s", file_path_category)

    return news_data


def process_all_files(data_dir):
    """Process all category files and save their news into separate .xlsx files."""
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".txt") and not file_name.startswith("Index_"):
            file_path = os.path.join(data_dir, file_name)
            logger.info("Processing file: %s", file_path)

            news = extract_news_from_file(file_path)

            if news:
                category_name = os.path.splitext(file_name)[0]
                output_excel = os.path.join(data_dir, f"{category_name}.xlsx")

                df = pd.DataFrame(news)
                df.to_excel(output_excel, index=False, sheet_name="News")
                logger.info("News for '%s' saved to %s.", category_name, output_excel)
            else:
                logger.info("No news found in file: %s.", file_name)


process_all_files(output_dir)
