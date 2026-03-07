import time
import numpy as np
from typing import Optional, List, Dict, Union
from dataclasses import dataclass, field
from enum import Enum
from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class SearchMode(Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"


@dataclass
class PriceStatistics:
    min_price: float
    mean_price: float
    max_price: float
    median_price: float
    offers_count: int
    prices: List[float] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"📊 Price Statistics:\n"
            f"{'─' * 40}\n"
            f"💵 Min price:  {self.min_price:.2f} BYN\n"
            f"💰 Mean price: {self.mean_price:.2f} BYN\n"
            f"💎 Max price:  {self.max_price:.2f} BYN\n"
            f"📈 Median:     {self.median_price:.2f} BYN\n"
            f"📦 Offers:     {self.offers_count}\n"
            f"{'─' * 40}"
        )


@dataclass
class ProductInfo:
    name: str
    url: str
    price_stats: Optional[PriceStatistics] = None
    ai_description: Optional[str] = None
    search_query: str = ""


class OnlinerParser:

    def __init__(self, headless: bool = False, detach: bool = True):
        self.base_url = "https://catalog.onliner.by/"
        self.driver = None
        self.wait = None
        self.headless = headless
        self.detach = detach
        self._setup_driver()

    def _setup_driver(self) -> None:

        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")

        if self.detach:
            chrome_options.add_experimental_option("detach", True)

        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            raise

    def _safe_click(self, xpath: str, max_attempts: int = 3, wait_time: int = 2) -> bool:

        for attempt in range(max_attempts):
            try:
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)

                element = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                element.click()
                return True
            except (StaleElementReferenceException, TimeoutException) as e:
                if attempt == max_attempts - 1:
                    return False
                time.sleep(1)
        return False

    def _handle_cookies(self) -> None:
        try:
            cookies = self.wait.until(
                EC.element_to_be_clickable((By.ID, "submit-button"))
            )
            cookies.click()
        except (NoSuchElementException, TimeoutException):
            return None

    def _get_ai_description(self) -> Optional[str]:
        try:
            self._safe_click(
                '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[1]/div[2]/div[4]/div[4]/a'
            )

            description_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/div"))
            )
            description = description_element.text

            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/span'))
            )
            close_button.click()

            return description

        except TimeoutException as e:
            return None

    def _get_price_statistics(self) -> Optional[PriceStatistics]:
        try:
            if not self._safe_click(
                    '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/aside/div[last()]/a'
            ):
                return None

            time.sleep(2)

            self._safe_click(
                '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[2]/div[1]/div/div[3]/div/div[3]/div[6]/span'
            )

            time.sleep(1)

            offers_block = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//*[@id="container"]/div/div/div/div/div[2]/div[1]/main/div/div/div[2]/div[1]/div/div[3]/div/div[3]'
                ))
            )

            price_elements = []

            price_elements = offers_block.find_elements(
                By.CSS_SELECTOR,
                'div[class*="offers-list__description"][class*="offers-list__description_alter-other"][class*="offers-list__description_huge-alter"]'
            )

            if not price_elements:
                price_elements = offers_block.find_elements(
                    By.CSS_SELECTOR,
                    'div.offers-list__description.offers-list__description_alter-other'
                )

            if not price_elements:
                price_elements = offers_block.find_elements(
                    By.CLASS_NAME,
                    'offers-list__description'
                )

            prices = []
            for elem in price_elements:
                if elem.text.strip():
                    try:
                        price_text = elem.text.strip().replace(',', '.').replace('р', '').replace(' ', '')
                        import re
                        price_match = re.search(r'(\d+\.?\d*)', price_text)
                        if price_match:
                            price = float(price_match.group(1))
                            prices.append(price)
                    except (ValueError, AttributeError) as e:
                        continue

            if not prices:

                try:
                    price_elements = self.driver.find_elements(
                        By.XPATH,
                        '//div[contains(@class, "offers-list__description")]//div[contains(text(), "р.")]'
                    )

                    for elem in price_elements:
                        if elem.text.strip():
                            price_text = elem.text.strip().replace(',', '.').replace('р', '').replace(' ', '')
                            import re
                            price_match = re.search(r'(\d+\.?\d*)', price_text)
                            if price_match:
                                price = float(price_match.group(1))
                                prices.append(price)
                except:
                    pass

            if not prices:
                return None

            prices_array = np.array(prices)
            stats = PriceStatistics(
                min_price=float(prices_array.min()),
                mean_price=float(prices_array.mean()),
                max_price=float(prices_array.max()),
                median_price=float(np.median(prices_array)),
                offers_count=len(prices),
                prices=prices
            )
            return stats

        except TimeoutException as e:
            return None
        except Exception as e:
            return None

    def search_product(self, query: Optional[str] = None) -> Optional[ProductInfo]:
        try:
            if not query:
                query = input("🔍 What do you want to find? ")
            self.driver.get(self.base_url)

            search_bar = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[@id="container"]/div/div/header/div[3]/div/div[2]/div[1]/div[1]/input'
                ))
            )
            search_bar.send_keys(query)

            first_result = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "/html/body/div[4]/div/div/div[1]/div[2]/ul/li/a/div/div[2]/div/a"
                ))
            )
            first_result.click()

            self._handle_cookies()

            name_element = self.driver.find_element(By.CLASS_NAME, 'catalog-masthead__title')
            product_name = name_element.text

            product = ProductInfo(
                name=product_name,
                url=self.driver.current_url,
                search_query=query
            )

            ai_description = self._get_ai_description()
            if ai_description:
                product.ai_description = ai_description

            price_stats = self._get_price_statistics()
            if price_stats:
                product.price_stats = price_stats
            else:
                product.price_stats = None
            return product

        except Exception as e:
            return None

    def close(self):
        """Закрытие браузера"""
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def main():
    with OnlinerParser(headless=False, detach=True) as parser:
        product = parser.search_product("iphone 15")

        if product:
            print(f"\n✅ Search completed for: {product.name}")


if __name__ == "__main__":
    main()