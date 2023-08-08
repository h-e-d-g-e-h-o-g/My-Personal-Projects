from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_driver_path = "C:\Development\chromedriver.exe"
servie = Service(executable_path=chrome_driver_path)

class Bot:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(service=servie)
        self.driver.get(url="https://www.imdb.com/chart/toptv/")
        close_button = self.driver.find_element(By.CSS_SELECTOR, ".ipc-snackbar .ipc-icon-button--baseAlt")
        close_button.click()
        option_detailed = self.driver.find_element(By.ID, "list-view-option-detailed")
        option_detailed.click()

    def obtain_show_details(self):
        self.show_titles = [show.text for show in self.driver.find_elements(By.CSS_SELECTOR, ".ipc-title-link-no-icon h3")[:100]]
        self.show_ratings = [show.text for show in self.driver.find_elements(By.CLASS_NAME, "ratingGroup--imdb-rating")[:100]]
        self.show_synopis = [show.text for show in self.driver.find_elements(By.CLASS_NAME, "ipc-html-content-inner-div")[:100]]
        self.show_posters = [show.get_attribute('src') for show in self.driver.find_elements(By.CSS_SELECTOR, ".ipc-media--poster-m .ipc-image")[:100]]
        #print(len(show_posters))
        self.driver.quit()
        return self.show_titles
    
    def prepare_details(self):
        library = []
        for num in range(100):
                dictionary = {
                     'name': self.show_titles[num],
                     'ratings': self.show_ratings[num],
                     'synopsis': self.show_synopis[num],
                     'src_poster': self.show_posters[num]
                }
                library.append(dictionary)

        return library
