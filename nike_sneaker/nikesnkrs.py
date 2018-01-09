# -*- coding: utf-8 -*-
import logging
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from nike_sneaker.config import NIKE_SNEAKER_URL
from nike_sneaker.sneaker import NikeNewSneaker

formatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


class NikeSNKRSException(Exception):
    pass


class NikeSNKRS(object):
    def __init__(self, web_driver='headless-chrome'):
        self._web_driver_type = web_driver
        self.soup = None
        self.sneakers = []

    def __get_raw_html(self, wait_time=5):
        _logger.info("get raw html from {}".format(NIKE_SNEAKER_URL))
        start_time = time.time()
        try:
            if self._web_driver_type == 'phantomjs':
                driver = webdriver.PhantomJS()
            elif self._web_driver_type == 'headless-chrome':
                # headless mode
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                driver = webdriver.Chrome(chrome_options=options)
            else:
                raise NikeSNKRSException("bad web driver type")
            driver.get(NIKE_SNEAKER_URL)
            # wait for JS to finish the pages
            time.sleep(wait_time)
            # TODO check load more unit it not exists
            try:
                load_more_btn = driver.find_element_by_xpath(
                # "//a[@'js-load-more ncss-brand bg-white border-top-light-grey u-sm-b u-uppercase u-align-center pt6-sm pb6-sm pt12-lg pb11-lg']")
                    "//a[starts-with(@class,'js-load-more ')]")
                load_more_btn.click()
                time.sleep(wait_time)
            except Exception:
                _logger.info("No load more button found")

            end_time = time.time()
            self.soup = BeautifulSoup(driver.page_source, "lxml")
            _logger.debug(self.soup.prettify())
        except Exception as e:
            _logger.error(e)
            raise NikeSNKRSException("Oops")
        finally:
            driver.close()

        _logger.info("get raw html finished, time: {:5.5f} seconds".format(end_time - start_time))

    def __parse_item_div(self, item_div):
        # item id / name and hyper link
        js_card_link = item_div.find_all('a', class_='js-card-link card-link d-sm-b', href=True, limit=1)[0]
        href = js_card_link['href']
        name = href.split('/')[-1]
        s = NikeNewSneaker(name)
        s.href = 'https://www.nike.com' + href
        # release date
        launch_time_div = item_div.find_all('div', class_=re.compile('launch-time.*'), limit=1)[0]
        release_date_p = launch_time_div.find('p')
        if release_date_p:
            s.release_date = release_date_p.text
        # release time
        test_time_heading = item_div.find_all('h6', class_=re.compile('.*test-time.*'), limit=1)[0]
        if test_time_heading:
            s.release_time = test_time_heading.text
        return s

    def check_new_release(self):
        try:
            self.__get_raw_html()
        except NikeSNKRSException:
            _logger.error("something bad happens when loading page")
            return

        items = self.soup.find_all('div', class_='upcoming-section')
        _logger.info("{} new sneakers are going to be released".format(len(items)))

        for item_div in items:
            s = self.__parse_item_div(item_div)
            print(s)
            print('---' * 3)
