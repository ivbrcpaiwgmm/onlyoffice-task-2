import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

import locators


def get_firefox_driver():
    driver_service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=driver_service)
    driver.maximize_window()
    return driver


def element_is_clickable(driver, locator, timeout=5):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def elements_are_visible(driver, locator, timeout=5):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located(locator))


def parse_contacts() -> list[list]:
    try:
        driver = get_firefox_driver()
        driver.get(locators.WEBSITE_URL)
        element_is_clickable(driver, locators.RESOURCES).click()
        element_is_clickable(driver, locators.CONTACTS).click()
        contact_divs = elements_are_visible(driver, locators.CONTACT_DIVS)
        contact_data = []
        # В последнем контейнере div указаны данные, не связанные с офисами, поэтому использую [:-1].
        for div in contact_divs[:-1]:
            child_elements = div.find_elements(By.XPATH, '*')
            data = []
            for element in child_elements:
                text = element.text
                if text:
                    data.append(text)
            # Форматирую данные под требования к CSV: "Country;CompanyName;FullAddress".
            data = data[:2] + [' '.join(data[2:])]
            contact_data.append(data)
        return contact_data
    finally:
        driver.quit()


def write_to_csv(path: str, data: list[list], delimiter: str = ';') -> None:
    with open(path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=delimiter)
        csv_writer.writerows(data)


def make_contacts_csv(path: str = "office_contacts.csv") -> None:
    contact_data = parse_contacts()
    write_to_csv(path, contact_data)


if __name__ == "__main__":
    make_contacts_csv()
