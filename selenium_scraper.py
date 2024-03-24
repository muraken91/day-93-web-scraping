from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PropertyURLScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.current_page = 1

    def close_driver(self):
        self.driver.quit()

    def scrape_property_urls(self):
        self.driver.get(self.url)
        property_urls = []

        try:
            while True:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'prop-name')))
                property_urls.extend(self._extract_property_urls())

                next_page_link = self._get_next_page_link()
                if next_page_link:
                    next_page_link.click()
                    self.current_page += 1
                else:
                    break

            return property_urls

        except Exception as e:
            print("Error scraping property URLs:", e)
            return []

    def _extract_property_urls(self):
        property_elements = self.driver.find_elements(By.CLASS_NAME, 'prop-name')
        property_urls = []
        for element in property_elements:
            link_element = element.find_element(By.TAG_NAME, 'a')
            property_urls.append(link_element.get_attribute('href'))
        return property_urls

    def _get_next_page_link(self):
        pagination = self.driver.find_element(By.CLASS_NAME, 'pager')
        pagination_links = pagination.find_elements(By.TAG_NAME, 'a')
        for link in pagination_links:
            page_number = link.text.strip()
            if page_number.isdigit() and int(page_number) == self.current_page + 1:
                return link
        return None


class PropertyInfoScraper:
    def __init__(self, driver):
        self.driver = driver

    def scrape_property_info(self):
        try:
            # Click the "Show More" button if it exists
            show_more_button = self.driver.find_element(By.CLASS_NAME, 'olm-show-more-units')
            if show_more_button:
                show_more_button.click()

            # Wait for the size and price elements to be present
            size_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td:nth-child(3) a.Unit__header"))
            )
            price_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td:nth-child(4) a.Unit__header"))
            )

            # Extract text from size and price elements
            size = [element.text.strip() for element in size_elements]
            price = [element.text.strip() for element in price_elements]

            # Extract building name
            building_name_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title"))
            )
            building_name = building_name_element.text.strip()

            print("Scraped building name:", building_name)
            print("Scraped size:", size)
            print("Scraped price:", price)

            return [building_name] * len(size), size, price
        except Exception as e:
            print("Error scraping property info:", e)
            return [], [], []