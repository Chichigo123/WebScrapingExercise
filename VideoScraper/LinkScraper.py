# http://www.mangago.me/read-manga/pendulum_kemonohito_omegaverse/
# https://horriblesubs.info/shows/ballroom-e-youkoso/
# http://jpmanga.space/?p=4830
# http://www.lovelyanime.com/Cardfight-Vanguard-G-Next/41/
# http://animepill.com/fireball-humorous-episode-1

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import pprint
from selenium.webdriver.chrome.options import Options
from lxml import etree
import pprint as pp
from io import StringIO


def printSourceToTextFile(textFileName, page_source):
    """

    :param textFileName:
           page_source:
    :return:
    """

    strPointer = StringIO()
    pp.pprint(page_source, strPointer)

    File = open(textFileName, "w+", encoding="utf-8")
    File.write(strPointer.getvalue())

    File.close()


class BaseLinkScraper():

    def getPageSource(self, website, waitForAnElement=None):
        """

        :return:
        """
        self.driver.implicitly_wait(5)
        self.driver.get(website)
        self.driver.maximize_window()

        wait = WebDriverWait(self.driver, 30)

        print("Web Driver is waiting for iframes to load ... ")


        video = wait.until(ec.presence_of_all_elements_located((By.XPATH, "//" + waitForAnElement)))

        page_source = self.driver.page_source

        return page_source

    def getIFramesFromTree(self, tree):
        """

        :param tree:
        :return:
        """

        iFrames = tree.xpath('//iframe')
        iFrameSources = []
        for iFrame in iFrames:
            iFrameSources.append(iFrame.get('src'))

        return iFrameSources

    def getElementsFromDriverByTagName(self, tag_name):
        """

        :param tree:
        :return:
        """

        elements = self.driver.find_elements_by_tag_name(tag_name)

        return elements

    def switchToIFramesAndReturnSource(self, iFramesList, counter = 0):
        """

        :param tree:
        :return:
        """


        for idx, iFrame in enumerate(iFramesList):
            print(idx)
            self.driver.switch_to.frame(iFrame)
            self.driver.implicitly_wait(30)

            self.iFrame_page_sources.append(self.driver.page_source)
            self.driver.get_screenshot_as_file('iFrame' + str(idx) + '_' + str(counter) +'.png')

            # TO DO Go to nested Frames and Navigate Back
            # nestedIFrameElements = self.getElementsFromDriverByTagName("iframe")
            # #
            # if len(nestedIFrameElements) > 0:
            #     self.iFrameCounter += 1
            #     self.switchToIFramesAndReturnSource(nestedIFrameElements, self.iFrameCounter)
            self.driver.switch_to.default_content()


    def configureChromeDriver(self, ):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # Download latest version of chrome driver and specify absolute path in params
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome('C:/Users/Acer-Laptop/PythonDrivers/chromedriver_win32/chromedriver.exe',
                                       options=chrome_options)

    def __init__(self):
        self.iFrameCounter = 0
        self.iFrame_page_sources = []



class DerivedLinkScraper(BaseLinkScraper):
    """

    """

    def __init__(self):
        self.pp = pp.PrettyPrinter(indent=4)

        self.configureChromeDriver()
        self.iFrameCounter = 0
        self.iFrame_page_sources = []
        pass


if __name__ == "__main__":

    # try:
    website = "https://animepill.com/fireball-humorous-episode-1"
    scraper = DerivedLinkScraper()
    page_source = scraper.getPageSource(website, "iframe")

    websiteName = website.replace("/", "")
    websiteName = websiteName.replace("https:", "")

    printSourceToTextFile(websiteName + "_source.txt", page_source)

    iFramesList = scraper.getElementsFromDriverByTagName("iframe")
    scraper.switchToIFramesAndReturnSource(iFramesList)


    # tree = etree.HTML(page_source)
    #
    # src = tree.xpath("//*[@src]")

    for idx, page_source in enumerate(scraper.iFrame_page_sources):
        printSourceToTextFile(websiteName + "_src" + str(idx) + str(scraper.iFrameCounter) + ".txt", page_source)

    # except:
    #     scraper.driver.quit()
    # finally:
    scraper.driver.close()












