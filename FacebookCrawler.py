

# class FacebookCrawler(Crawler):
#     # ===========================================================================
#     # region CONSTRUCTOR AND LOGIN

#     def __init__(self, account) -> None:
#         super().__init__()
#         self._login(account)

#     def _login(self, account) -> None:
#         # get link
#         self.browser.get('https://www.facebook.com/login')

#         # wait for page load
#         self.wait_element("//input[@name='email']")

#         # input with name is email
#         email = self.browser.find_element(By.NAME, 'email')
#         email.send_keys(account['username'])

#         # input with name is pass
#         password = self.browser.find_element(By.NAME, 'pass')
#         password.send_keys(account['password'])

#         # button with name is login
#         login = self.browser.find_element(By.NAME, 'login')
#         login.click()

#         # wait for login complete
#         self.wait_element()

#     # endregion
#     # ===========================================================================

#     # ===========================================================================
#     # region CRAWL POST BY HASHTAG

#     def get_posts_info_by_hashtag(self,
#                                   hashtag: str,
#                                   n_posts: integer = 10,
#                                   verbose: integer = 1) -> pd.DataFrame:

#         # ! Raise error when n_posts is lower than 0
#         if n_posts < 0:
#             raise ValueError("n_posts must be greater than 0")

#         # * get page and wait for page load
#         self.browser.get(f'https://www.facebook.com/hashtag/{hashtag}')
#         self.wait_element("//div[contains(@class, 'du4w35lb') and\
#                                    contains(@class, 'k4urcfbm') and\
#                                    contains(@class, 'l9j0dhe7') and\
#                                    contains(@class, 'sjgh65i0')]")

#         # * scroll
#         self.scroll_to_end() if n_posts == 0 else self._scroll_posts(n_posts)

#         # * get posts
#         divs = self._get_posts_div_by_hashtag()

#         # * crawl data from each post
#         data = []
#         for div in divs:
#             if len(data) >= n_posts and n_posts != 0:
#                 break

#             post_info = self._crawling(div)

#             if verbose == 1:
#                 print(post_info)

#             if post_info is not None:
#                 data.append(post_info)

#         # * convert to dataframe and return
#         df = pd.DataFrame(data)
#         return df

#     def _crawling(self, div):
#         # skip shared post
#         if self._is_shared_post(div):
#             return

#         # scroll to div
#         self.scroll_element_to_center(div)
#         time.sleep(0.5)

#         # get data
#         meta = self._get_meta_data(div)     # meta data
#         content = self._get_content(div)    # content

#         return {**meta, **{'Content': content}}

#     def _is_shared_post(self, div) -> bool:
#         if len(div.find_elements(By.XPATH, ".//div[contains(@class, 'cwj9ozl2') and\
#                                                     contains(@class, 'l6v480f0') and\
#                                                     contains(@class, 'maa8sdkg') and\
#                                                     contains(@class, 's1tcr66n') and\
#                                                     contains(@class, 'aypy0576') and\
#                                                     contains(@class, 'ue3kfks5') and\
#                                                     contains(@class, 'pw54ja7n') and\
#                                                     contains(@class, 'uo3d90p7') and\
#                                                     contains(@class, 'l82x9zwi') and\
#                                                     contains(@class, 'tvfksri0') and\
#                                                     contains(@class, 'ozuftl9m')]")) > 0:
#             return True
#         else:
#             return False

#     def _get_posts_div_by_hashtag(self) -> list:
#         return self.browser.find_elements(By.XPATH,
#                                           "//div[contains(@class, 'du4w35lb') and\
#                                                  contains(@class, 'k4urcfbm') and\
#                                                  contains(@class, 'l9j0dhe7') and\
#                                                  contains(@class, 'sjgh65i0')]")

#     # endregion
#     # ==========================================================================

#     # ===========================================================================
#     # region SCROLL

#     def _scroll_posts(self, n_posts) -> None:
#         # * variables
#         patience = 0  # n times tried
#         n_last_posts = len(self._get_posts_div_by_hashtag())  # number of posts

#         # * if number of posts is not satisfied, then scroll
#         while n_last_posts < n_posts:
#             # scroll and wait for 1 seconds
#             self.browser.execute_script(
#                 "window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(1)

#             # n posts after scroll
#             n_new_posts = len(self._get_posts_div_by_hashtag())

#             # there is no new posts
#             if n_new_posts == n_last_posts:
#                 # if after 'patience' times, no new posts are found, break
#                 patience += 1
#                 if(patience == 5):
#                     break

#             # new posts are found
#             else:
#                 n_last_posts = n_new_posts
#                 # reset patience
#                 patience = 0

#     # endregion
#     # ===========================================================================

#     # ==========================================================================
#     # region GET DATA

#     # =================================
#     # region META DATA

#     def _get_meta_data(self, div) -> dict:
#         # * post heading
#         div_head = div.find_element(By.XPATH,
#                                     ".//div[contains(@class, 'j83agx80') and\
#                                             contains(@class, 'cbu4d94t') and\
#                                             contains(@class, 'ew0dbk1b') and\
#                                             contains(@class, 'irj2b8pg')]")

#         # * person info and group info (if exists)
#         # find profile and group
#         h2 = div_head.find_element(By.XPATH, ".//h2")

#         # check if h2 have div -> group post, else -> person post
#         if len(h2.find_elements(By.XPATH, ".//div/div")) > 0:
#             person_info = self._get_meta_data_group_post(h2)
#         else:
#             person_info = self._get_meta_data_person_post(h2)

#         # * post time and link
#         time_data = self._get_time_and_link(div_head)

#         # * merge meta and time_data and return
#         return {**person_info, **time_data}

#     def _get_meta_data_person_post(self, element) -> dict:
#         profile = element.find_elements(By.XPATH, ".//a")

#         # account is normal
#         if len(profile) > 0:
#             profile_link = profile[0].get_attribute('href')
#             profile_name = profile[0].get_attribute('innerText')
#         # account is disabled
#         else:
#             profile_link = ''
#             profile_name = element.find_element(By.XPATH,
#                                                 ".//strong").get_attribute('innerText')

#         # empty group info
#         group_link = ''
#         group_name = ''

#         # remove GET method attributes from link
#         profile_link = profile_link.split('?')[0]

#         return {'Profile link': profile_link,
#                 'Profile name': profile_name,
#                 'Group link': group_link,
#                 'Group name': group_name}

#     def _get_meta_data_group_post(self, h2) -> dict:
#         links = h2.find_elements(By.XPATH, ".//a")

#         # len(links) == 1 -> account is disabled
#         if len(links) == 1:
#             # group info
#             group_link = links[0].get_attribute('href')
#             group_name = links[0].get_attribute('innerText')

#             # name profile
#             span = h2.find_element(By.XPATH, ".//span")
#             profile_name = span.get_attribute('innerText')
#             profile_link = ''

#         # normal account
#         else:
#             for link in links:
#                 # if link contain 'group' -> that's group, else -> that's profile
#                 if 'user' in link.get_attribute('href'):
#                     profile_link = link.get_attribute('href')
#                     profile_name = link.get_attribute('innerText')
#                 else:
#                     group_link = link.get_attribute('href')
#                     group_name = link.get_attribute('innerText')

#         # remove GET method attribute from link
#         group_link = group_link.split('?')[0]
#         profile_link = profile_link.split('?')[0]

#         return {'Profile link': profile_link,
#                 'Profile name': profile_name,
#                 'Group link': group_link,
#                 'Group name': group_name}

#     def _get_time_and_link(self, div_head) -> dict:
#         result = {}

#         # a contains time info
#         time_a = div_head.find_element(By.XPATH, ".//a[contains(@class, 'oajrlxb2') and \
#                                                         contains(@class, 'g5ia77u1') and \
#                                                         contains(@class, 'qu0x051f') and \
#                                                         contains(@class, 'esr5mh6w') and \
#                                                         contains(@class, 'e9989ue4') and \
#                                                         contains(@class, 'r7d6kgcz') and \
#                                                         contains(@class, 'rq0escxv') and \
#                                                         contains(@class, 'nhd2j8a9') and \
#                                                         contains(@class, 'nc684nl6') and \
#                                                         contains(@class, 'p7hjln8o') and \
#                                                         contains(@class, 'kvgmc6g5') and \
#                                                         contains(@class, 'cxmmr5t8') and \
#                                                         contains(@class, 'oygrvhab') and \
#                                                         contains(@class, 'hcukyx3x') and \
#                                                         contains(@class, 'jb3vyjys') and \
#                                                         contains(@class, 'rz4wbd8a') and \
#                                                         contains(@class, 'qt6c0cv9') and \
#                                                         contains(@class, 'a8nywdso') and \
#                                                         contains(@class, 'i1ao9s8h') and \
#                                                         contains(@class, 'esuyzwwr') and \
#                                                         contains(@class, 'f1sip0of') and \
#                                                         contains(@class, 'lzcic4wl') and \
#                                                         contains(@class, 'gmql0nx0') and \
#                                                         contains(@class, 'gpro0wi8') and \
#                                                         contains(@class, 'b1v8xokw')]")
#         parent = time_a.find_element(By.XPATH, ".//..")

#         if time_a.is_displayed():
#             # hover on link to reveal time
#             self.hover(time_a)

#             # wait for time to be revealed
#             span_parent_path = self.generate_xpath(
#                 parent
#             )+"[@aria-describedby]"
#             span_parent = self.wait_element_and_select(span_parent_path)

#             if span_parent:
#                 id_time = span_parent.get_attribute('aria-describedby')

#                 # get time
#                 time_relative = self.browser.find_element(By.ID,
#                                                           id_time).get_attribute('innerText')
#                 time_absolute = self._convert_relative_to_absolute_time(
#                     time_relative
#                 )
#                 result['Time'] = time_absolute

#             else:
#                 self.browser.save_screenshot('error.png')

#             # assign link and time
#             link = time_a.get_attribute('href')
#             result['Post link'] = link

#         return result

#     def _convert_relative_to_absolute_time(self, relative_time) -> str:
#         # Time format: Wednesday, August 2, 2018 at 8:02 PM
#         pieces = relative_time.split(', ')

#         month, day = pieces[1].split(' ')
#         year = pieces[2].split(' ')[0]
#         hour = pieces[2].split(' ')[2].split(':')[0]
#         minute = pieces[2].split(' ')[2].split(':')[1]
#         locale = pieces[2].split(' ')[3]

#         # add 0 to day and hour if less than 10
#         if int(day) < 10:
#             day = '0' + day
#         if int(hour) < 10:
#             hour = '0' + hour

#         # merge time
#         facebook_time = year + '-' + month + '-' + \
#             day + ' ' + hour + ':' + minute + ':00' + ' ' + locale

#         # convert to YYYY-MM-DD HH:MM:SS
#         absolute_time = datetime.strptime(facebook_time,
#                                           '%Y-%B-%d %I:%M:%S %p')
#         absolute_time = absolute_time.strftime('%Y-%m-%d %H:%M:%S')

#         return absolute_time

#     # endregion
#     # =================================

#     # =================================
#     # region CONTENT

#     def _get_content(self, div) -> str:
#         # get content text
#         try:
#             content = self._get_content_post(div)

#             # click 'See more' to reveal full content
#             try:
#                 # click on "See more"
#                 see_more = content.find_element(By.XPATH, ".//div[@role='button' and\
#                                                                 text()='See more']")
#                 self.browser.execute_script("arguments[0].click();", see_more)

#                 # re select content
#                 content = self._get_content_post(div)

#             # content is fully loaded
#             except NoSuchElementException:
#                 pass

#         # post without content
#         except NoSuchElementException:
#             return ''

#         return content.get_attribute('innerText')

#     def _get_content_post(self, div) -> WebElement:
#         return div.find_element(By.XPATH,  # normal post, sell post
#                                 ".//div[contains(@class, 'ecm0bbzt') and\
#                                         contains(@class, 'ihqw7lf3') and\
#                                         contains(@class, 'hv4rvrfc') and\
#                                         contains(@class, 'dati1w0a')]\
#                                     |\
#                                     .//div[contains(@class, 'rq0escxv') and\
#                                         contains(@class, 'a8c37x1j') and\
#                                         contains(@class, 'rz4wbd8a') and\
#                                         contains(@class, 'a8nywdso')]\
#                                     |\
#                                     .//div[contains(@class, 'bp9cbjyn') and\
#                                             contains(@class, 'j83agx80') and\
#                                             contains(@class, 'cbu4d94t') and\
#                                             contains(@class, 'datstx6m') and\
#                                             contains(@class, 'taijpn5t') and\
#                                             contains(@class, 'pmk7jnqg') and\
#                                             contains(@class, 'j9ispegn') and\
#                                             contains(@class, 'kr520xx4') and\
#                                             contains(@class, 'k4urcfbm')] \
#                                     |\
#                                     .//div [contains(@class, 'ecm0bbzt') and\
#                                             contains(@class, 'hv4rvrfc') and\
#                                             contains(@class, 'dati1w0a') and\
#                                             contains(@class, 'e5nlhep0')]")

#     # endregion
#     # =================================

#     # endregion
#     # ==========================================================================
