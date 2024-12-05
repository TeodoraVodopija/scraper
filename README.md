# Sports News Scraper

## Overview
This project is a Python-based web scraping tool designed to extract and process sports news from the website **Index.hr**. The tool fetches HTML content from the website, parses it to identify sports categories, retrieves news articles, and saves the data into individual `.xlsx` files for each category.

## Features
- **Dynamic Scraping**: Automatically detects sports categories and their links.
- **Content Extraction**: Extracts headlines, summaries, publish dates, and URLs for news articles.
- **Data Storage**: Saves latest 5 news articles for each category into separate `.xlsx` files.
- **Error Handling**: Logs errors and handles missing files gracefully.

## Prerequisites
Ensure the following are installed on your system:
- Python 3.7+
- Required Python libraries:
  - `requests`
  - `pandas`
  - `beautifulsoup4`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/teodoraa2019/scraper.git
   cd scraper
   ```

## Usage
1. Run the script:
   ```bash
   python Scraper.py
   ```
2. The script will:
   - Fetch the main page of **Index.hr**.
   - Extract sports categories and their corresponding news links.
   - Save the raw HTML content of each category to the `data/` directory.
   - Process the HTML files to extract news and save them as `.xlsx` files in the `data/` directory.

## Directory Structure
```
.
├── data/                # Directory for storing downloaded HTML and .xlsx files
├── Scraper.py           # Main script
├── README.md            # Project documentation
```

## Output
For each sports category, the script generates an `.xlsx` file in the `data/` directory with the following columns:
- **Title**: The headline of the news article.
- **Summary**: A brief summary of the article.
- **Publish Date**: The date the article was published.
- **URL**: The link to the full article.

## Logging
The script creates a `process_log.txt` file in the `data/` directory to log information, warnings, and errors.

## Notes
- The `data/` directory is created automatically if it doesn't exist.
- Make sure the `Index.hr` website structure remains unchanged, as any updates might require script adjustments.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed explanation of your changes.
