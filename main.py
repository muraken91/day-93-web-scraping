from selenium_scraper import PropertyURLScraper, PropertyInfoScraper
import csv
from datetime import datetime
import os


def main():
    # URL of the main search page
    main_search_url = os.environ["url"]

    # Instantiate PropertyURLScraper and scrape property URLs
    url_scraper = PropertyURLScraper(main_search_url)
    property_urls = url_scraper.scrape_property_urls()

    # Check if property URLs are available
    if not property_urls:
        print("No property URLs found.")
        return

    # Instantiate PropertyInfoScraper
    info_scraper = PropertyInfoScraper(url_scraper.driver)

    # Create a new CSV file with the current date added to the file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"{os.environ['filename1']}_offices_{timestamp}.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Building Name', 'Size', 'Price'])

        try:
            # Scrape property info from each property page and append to CSV
            for url in property_urls:
                # Navigate to property URL
                url_scraper.driver.get(url)

                # Scrape property info
                building_name, size, price = info_scraper.scrape_property_info()

                # Write scraped data to CSV
                for i in range(len(size)):
                    writer.writerow([building_name[i], size[i], price[i]])
                    print("Data appended for:", building_name[i])

        finally:
            # Close the Selenium driver
            url_scraper.close_driver()


if __name__ == "__main__":
    main()