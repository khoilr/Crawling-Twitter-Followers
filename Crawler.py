# setup selenium
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class Crawler:
    # =========================================================================
    # region INITIALIZE

    def __init__(self) -> None:
        # browser
        self.browser = self._init_browser()

    def _init_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-device-discovery-notifications')
        options.add_argument('--disable-breakpad')
        options.add_argument('--disable-client-side-phishing-detection')
        options.add_argument('--disable-cast-streaming-hw-encoding')
        options.add_argument('--disable-cast-streaming-hw-decoding')
        options.add_argument('--disable-cast-streaming-dma-buf-video')
        options.add_argument('--disable-cast-streaming-vp9-video')
        options.add_argument('--disable-cast-streaming-h264-video')
        options.add_argument('--disable-cast-streaming-vp8-video')
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-accelerated-2d-canvas')
        options.add_argument('--disable-accelerated-jpeg-decoding')
        options.add_argument('--disable-accelerated-mjpeg-decode')
        options.add_argument('--disable-accelerated-video-decode')

        options.add_experimental_option("detach", True)

        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                   options=options)

        # browser.set_window_size(5000 , 5000)
        # browser.set_window_position(0, 0)

        return browser

    # endregion
    # =========================================================================

    # =========================================================================
    # region WAIT

    def _wait_driver(self, timeout):
        return WebDriverWait(self.browser, timeout)

    def wait_element(self, xpath="/html/body", timeout=10):
        try:
            wait = self._wait_driver(timeout)
            wait.until(EC.visibility_of_element_located((By.XPATH,
                                                         xpath)))
            return True
        except TimeoutException:
            print("Timed out waiting for page to load element " + xpath)
            return False

    def wait_element_and_select(self, xpath, timeout=10) -> WebElement:
        try:
            wait = self._wait_driver(timeout)
            div = wait.until(EC.presence_of_element_located((By.XPATH,
                                                             xpath)))
            return div
        except TimeoutException:
            print("Timed out waiting for page to load and select element" + xpath)
            return False

    def wait_url(self, url, timeout=10):
        try:
            wait = self._wait_driver(timeout)
            wait.until(EC.url_to_be(url))
            return True
        except TimeoutException as e:
            print("Timed out waiting for url " + url)
            return False

    # endregion
    # =========================================================================

    # ==========================================================================
    # region METHODS

    def to_number(self, str: str) -> int:
        remove_comma = str.replace(".", "").replace(',', '')
        remove_letter = remove_comma.replace('k', '')
        remove_letter = remove_letter.replace('m', '')
        remove_letter = remove_letter.replace('b', '')
        remove_letter = remove_letter.replace('t', '')
        remove_letter = remove_letter.replace('K', '')
        remove_letter = remove_letter.replace('M', '')
        remove_letter = remove_letter.replace('B', '')
        remove_letter = remove_letter.replace('T', '')
        return int(remove_letter)

    def generate_xpath(self, child_element: WebElement, current: str = '') -> str:
        child_tag = child_element.tag_name

        if child_tag == "html":
            return "/html[1]"+current

        parent_element = child_element.find_element(By.XPATH, "..")
        children_elements = parent_element.find_elements(By.XPATH, "*")

        count = 0

        for children_element in children_elements:
            children_tag = children_element.tag_name

            if child_tag == children_tag:
                count += 1

            if child_element == children_element:
                return self.generate_xpath(parent_element, "/" + child_tag + "[" + str(count) + "]"+current)

        return None

    # endregion
    # ==========================================================================

    # ==========================================================================
    # region ACTIONS

    def hover(self, element: WebElement) -> None:
        # hover on link to reveal time
        hover = ActionChains(self.browser).move_to_element(element)
        hover.perform()

    def scroll_to_end(self) -> None:
        # * variables
        last_height = self.browser.execute_script(         # get height of page
            "return document.body.scrollHeight")
        patience = 0  # n times tried

        # * scroll to end of page
        while True:
            # execute scroll command and wait for 1 seconds
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # get height after scroll
            new_height = self.browser.execute_script(
                "return document.body.scrollHeight")

            # if height is the same, it means page is at the end
            if new_height == last_height:
                patience += 1
                # after tried patience times, break
                if(patience == 5):
                    break
            else:
                last_height = new_height
                # reset patience
                patience = 0

    def scroll_to_element(self, element: WebElement) -> None:
        # variables
        element_location = element.location

        # scroll to element
        self.browser.execute_script(
            "window.scrollTo({}, {})".format(element_location["x"], element_location["y"]))

    def scroll_element_to_center(self, element: WebElement) -> None:
        # variables
        element_location = element.location
        element_height = element.size["height"]
        element_width = element.size["width"]

        print(element_location, element_height, element_width)

        # scroll to element
        self.browser.execute_script(
            "window.scrollTo({}, {})".format(element_location["x"] + element_width/2, element_location["y"] + element_height/2))

    # endregion
    # ==========================================================================


class TwitterCrawler(Crawler):

    # ==========================================================================
    # region CONSTRUCTOR and LOGIN

    def __init__(self, account) -> None:
        super().__init__()
        self.account = account
        self._login()

    def _login(self):
        self.browser.get('https://twitter.com/i/flow/login')

        # input email
        username_field = self.wait_element_and_select("//input[contains(@name, 'text')]",
                                                      timeout=60)
        username_field.send_keys(self.account['username'])
        self.browser.find_element(By.XPATH,  # click next button to fill password
                                  "//div[contains(@role, 'button')]//span[text()='Next']").click()
        time.sleep(1)

        # Fill the email if requires
        email_field = self.wait_element_and_select("//input[contains(@name, 'text') and \
                                                            contains(@data-testid, 'ocfEnterTextTextInput')]",
                                                   timeout=1)
        if email_field:
            email_field.send_keys(self.account['email'])
            self.browser.find_element(By.XPATH,
                                      "//div[contains(@role, 'button')]//span[text()='Next']").click()
            time.sleep(1)

        # check login error
        if self._login_error():
            return

        # input password
        password_field = self.wait_element_and_select(
            "//input[contains(@name, 'password')]"
        )
        password_field.send_keys(self.account['password'])
        self.browser.find_element(By.XPATH,  # click login button
                                  "//div[contains(@data-testid, 'LoginForm_Login_Button')]").click()

        # wait for login
        self.wait_url('https://twitter.com/home')
        self.wait_element('//h2')

    def _login_error(self):
        confirm_box = self.browser.find_elements(By.XPATH,
                                                 "//div[contains(@data-testid, 'confirmationSheetDialog')]")
        if len(confirm_box) > 0:
            print("Login error, retrying...")
            self._login()
            return True
        else:
            return False

    # endregion
    # ==========================================================================

    # ==========================================================================
    # region ACCOUNT CHECKING

    def check_account_followings(self, user) -> bool:
        self.browser.get(f'https://twitter.com/{user}')
        self.wait_element('//h2')

        return self.is_exist(page_loaded=True) and self.have_followings(user, page_loaded=True)

    def is_exist(self, user: str = None, page_loaded: bool = False) -> bool:
        if page_loaded:
            # account doesn't exist will have div that has data-testid = emptyState
            return len(self.browser.find_elements(By.XPATH,
                                                  '//div[contains(@data-testid, "emptyState")]')) == 0

        elif user is None:
            raise ValueError("User is required when page hasn't been loaded")

        else:
            self.browser.get(f'https://twitter.com/{user}')
            self.wait_element('//h2')

            return self.is_exist(user, page_loaded=True)

    def have_followings(self, user: str = None, page_loaded: bool = False) -> bool:
        if page_loaded:
            # check number of followings at the account intro
            followings = self.browser.find_element(By.XPATH,
                                                   f"//a[substring(@href, string-length(@href) - string-length('{user}/following') +1) = '{user}/following']")
            followings = followings.get_attribute('innerText').split(' ')[0]
            n_followings = self.to_number(followings)

            return n_followings > 0

        elif user is None:
            raise ValueError("User is required when page hasn't been loaded")

        else:
            self.browser.get(f'https://twitter.com/{user}')
            self.wait_element('//h2')

            return self.have_followings(user, page_loaded=True)

    def check_account_followers(self, user) -> bool:
        self.browser.get(f'https://twitter.com/{user}')
        self.wait_element('//h2')

        return self.is_exist(page_loaded=True) and self.have_followers(user, page_loaded=True)

    def have_followers(self, user=None, page_loaded=False) -> bool:
        if page_loaded:
            # check number of followers at the account intro
            followers = self.browser.find_element(By.XPATH,
                                                  f"//a[substring(@href, string-length(@href) - string-length('{user}/followers') +1) = '{user}/followers']")
            followers = followers.get_attribute('innerText').split(' ')[0]
            n_followers = self.to_number(followers)

            return n_followers > 0

        elif user is None:
            raise ValueError("User is required when page hasn't been loaded")

        else:
            self.browser.get(f'https://twitter.com/{user}')
            self.wait_element('//h2')

            return self.have_followers(user, page_loaded=True)

    # endregion
    # ==========================================================================

    # ==========================================================================
    # region GET INFO

    def _get_info_from_user_cell(self, user_cell):
        # get link
        link = user_cell.find_element(By.XPATH,
                                      ".//a").get_attribute('href')
        # get name
        name = user_cell.find_element(By.CSS_SELECTOR,
                                      "span.css-901oao.css-16my406.css-bfa6kz.r-poiln3.r-bcqeeo.r-qvutc0").get_attribute("innerText").strip()

        # get id
        try:
            id = user_cell.find_element(By.CSS_SELECTOR,
                                        "div.css-1dbjc4n.r-18u37iz.r-1wbh5a2").get_attribute("innerText").strip()
        except NoSuchElementException:
            id = None

        info = {'link': link,
                'name': name,
                'id': id}

        return info

    # endregion
    # ==========================================================================

    # ==========================================================================
    # region GET FOLLOWINGS

    def get_followings(self, user, verbose=1) -> pd.DataFrame or None:
        # check account
        if not self.check_account_followings(user):
            return

        # define followings set
        followings_user = []

        # get and wait for element
        self.browser.get(f'https://twitter.com/{user}/following')
        user_cell = self.wait_element_and_select(
            '//div[contains(@data-testid, "primaryColumn")]//div[contains(@data-testid, "UserCell")]'
        )

        # * really start crawling
        while True:
            # scroll to div
            self.scroll_to_element(user_cell)

            # get info
            info = self._get_info_from_user_cell(user_cell)

            # print if verbose
            if verbose == 1:
                print(info)

            # append to list
            followings_user.append(info)

            # next usercell
            grandparent = user_cell.find_elements(By.XPATH,
                                                  './/../..')
            next_sibling = grandparent[0].find_elements(By.XPATH,
                                                        './following-sibling::div//div[contains(@data-testid, "UserCell")]')
            if len(next_sibling) == 0:
                break
            else:
                user_cell = next_sibling[0]

        # convert to DataFrame and return
        df = pd.DataFrame(followings_user)
        return df

    # endregion
    # ==========================================================================

    # ==========================================================================
    # region GET FOLLOWERS

    def get_followers(self, user, verbose=1) -> pd.DataFrame or None:
        # check account
        if not self.check_account_followers(user):
            return

        # define followers set
        followers_user = []

        # get and wait for element
        self.browser.get(f'https://twitter.com/{user}/followers')
        user_cell = self.wait_element_and_select(
            '//div[contains(@data-testid, "primaryColumn")]//div[contains(@data-testid, "UserCell")]'
        )

        # * really start crawling
        while True:
            # scroll to div
            self.scroll_to_element(user_cell)

            # get info
            info = self._get_info_from_user_cell(user_cell)

            # print if verbose
            if verbose == 1:
                print(info)

            # append to list
            followers_user.append(info)

            # next usercell
            grandparent = user_cell.find_elements(By.XPATH,
                                                  './/../..')
            next_sibling = grandparent[0].find_elements(By.XPATH,
                                                        './following-sibling::div//div[contains(@data-testid, "UserCell")]')
            if len(next_sibling) == 0:
                break
            else:
                user_cell = next_sibling[0]

        # convert to DataFrame and return
        df = pd.DataFrame(followers_user)
        return df

    # endregion
    # ==========================================================================
