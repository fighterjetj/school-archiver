from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from downloader import get_videos
from videoMaker import concatenate_files
from constants import *
import os, time, re


SITE = "https://bruinlearn.ucla.edu"


# INPUTS: user = username, passw = password, driver = Selenium webdriver object, site = Site that redirects to the DUO Mobile sign in screen, trust = Trust the browser
# Navigates through the login screen, however the user must do two factor authentication with the app/other method
# Assumes the webdriver has a long implicit wait time, if not this may not work, as DUO Mobile needs time to redirect
def duoMobileLogin(user, passw, driver, site, trust=False):
    driver.get(site)
    # Signing in
    username = driver.find_element(By.XPATH, '//*[@id="logon"]')
    password = driver.find_element(By.XPATH, '//*[@id="pass"]')
    signinButton = driver.find_element(
        By.XPATH,
        "/html/body/section/table/tbody/tr/td/div/form/div/table/tbody/tr/td[1]/button",
    )
    username.send_keys(user)
    password.send_keys(passw)
    signinButton.click()
    # Clicking trust or do not trust depending on what values were passed
    if trust:
        doTrustButton = driver.find_element(By.XPATH, '//*[@id="trust-browser-button"]')
        doTrustButton.click()
    else:
        noTrustButton = driver.find_element(
            By.XPATH, '//*[@id="dont-trust-browser-button"]'
        )
        noTrustButton.click()


# INPUTS: user = username, passw = password, driver = Selenium webdriver object
# Returns a list of links to each course currently enrolled in
def getCourseLinks(user, passw, driver):
    duoMobileLogin(user, passw, driver, SITE)
    showCourses = driver.find_element(By.XPATH, '//*[@id="global_nav_courses_link"]')
    # Wait a few seconds because if the button is clicked before everything loads it will cause an issue
    time.sleep(3)
    showCourses.click()
    listHeader = driver.find_element(By.XPATH, '//h2[text()="Courses"]')
    # Wait a few seconds for the course menu to load
    time.sleep(3)
    unorderedList = driver.find_element(
        locate_with(By.TAG_NAME, "ul").below(listHeader)
    )
    links = unorderedList.find_elements(By.TAG_NAME, "a")
    return [link.get_attribute("href") for link in links]


# INPUTS: button = Selenium element object referring to a play button on the UCLA Media Reserves page
# RETURNS: The lecture date
def getButtonDate(button):
    parentSpan = button.find_element(By.XPATH, "..")
    parentTd = parentSpan.find_element(By.XPATH, "..")
    parentTr = parentTd.find_element(By.XPATH, "..")
    # Getting the first element of the TD, which comes before the button
    dateTd = parentTr.find_element(By.CLASS_NAME, "css-1fxcqnu-view-cell")
    return dateTd.text


# INPUT: Selenium webdriver at the video page
# RETURNS: The name of the video file
def getVideoFilename(driver):
    """
    iframe = driver.find_element(By.ID, "tool_content")
    driver.switch_to.frame(iframe)
    """
    videoPlayer = driver.find_element(By.CLASS_NAME, "jwplayer")
    vidID = videoPlayer.get_attribute("id")
    # ID is formatted like https://bclive.oid.ucla.edu/2022f-v/mp4:cs35l-1-20220926-25128.mp4/playlist.m3u8?wowzatokenendtime=1668850874&wowzatokenhash=IM8dvW7jL4TC41oDsh3fDTUwjQguz0WWsNca2r_sBdY=
    # Assume that all files are stored as mp4s, so we search for the format "mp4:.*\.mp4"
    fileMatch = re.search(r"mp4:(.*)\.mp4", vidID)
    filename = fileMatch.group(1) + FINISHED_VIDEO_TYPE
    return filename


def getCourseVideoLinks(url, driver):
    # Going to the course UCLA media reserve
    driver.get(url + "/external_tools/871")
    iframe = driver.find_element(By.ID, "tool_content")
    # Switching to the iframe that contains the play buttons
    driver.switch_to.frame(iframe)
    buttons = driver.find_elements(
        By.CLASS_NAME, "css-16frnar-view--inlineBlock-baseButton"
    )
    videos = {}
    # Iterating over the buttons
    for i in range(len(buttons)):
        date = getButtonDate(buttons[i])
        date = date.replace("/", "-")
        buttons[i].click()
        time.sleep(3)
        filename = getVideoFilename(driver)
        videos[date] = filename
        # Going back a page and then 'refinding' the buttons
        backButton = driver.find_element(
            By.CLASS_NAME, "css-16t9593-view--inlineBlock-baseButton"
        )
        backButton.click()
        time.sleep(3)
        buttons = driver.find_elements(
            By.CLASS_NAME, "css-16frnar-view--inlineBlock-baseButton"
        )
    return videos


# Video source
# https://bclive.oid.ucla.edu/2022f-v/mp4:cs35l-1-20221114-27441.mp4/media_w1256890193_tkd293emF0b2tlbmVuZHRpbWU9MTY2ODgwMjkxMCZ3b3d6YXRva2VuaGFzaD1rd3RJUUlPUjdOU0Q1WXJXdHhVV2N4dFh1SGFMRDVkZVB2Slg1QlFEb1djPQ==_0.ts
# Class id
# https://bclive.oid.ucla.edu/2022f-v/mp4:cs35l-1-20221114-27441.mp4/playlist.m3u8?wowzatokenendtime=1668802910&wowzatokenhash=kwtIQIOR7NSD5YrWtxUWcxtXuHaLD5dePvJX5BQDoWc=


# INPUT: UCLA username and password
# RETURNS: A dictionary of dictionaries for each class.  The dictionary for a class links a given date to a tuple - (name of file, download link)
def getAllCourseVideoLinks(user, passw):
    os.environ["PATH"] += r"C:/Selenium Drivers"
    # Set for storing all the video download links
    vid_download_links = set()
    # Function for intercepting requests
    def interceptor(request):
        if "https://bclive.oid.ucla.edu/" in request.url:
            if request.url[-len(CLIP_VIDEO_TYPE) :] == CLIP_VIDEO_TYPE:
                url = request.url[: -len(CLIP_VIDEO_TYPE)]
                while url[-1].isnumeric():
                    url = url[:-1]
                vid_download_links.add(url)
                # print(url)

    driver = webdriver.Chrome()
    driver.request_interceptor = interceptor
    # Allows the page to wait up to 15 seconds for an element to load
    # Helps with allowing users to get their duo mobile to go through
    driver.implicitly_wait(15)
    courseLinks = getCourseLinks(user, passw, driver)
    videoLinkDicts = []
    for link in courseLinks:
        videoLinkDicts.append(getCourseVideoLinks(link, driver))
    driver.quit()
    vid_download_links = list(vid_download_links)
    # Function for taking the filename as input and returning the corresponding download link
    def getVidDownloadLink(filename):
        for link in vid_download_links:
            if filename in link:
                return link
        return ""

    final_dict = {}
    numClasses = 0
    for dict in videoLinkDicts:
        numClasses += 1
        dictKeys = dict.keys()
        # If there's no videos, don't make a dictionary
        if len(dictKeys) > 0:
            className = ""
            for key in dictKeys:
                filename = dict[key]
                className = filename
                dict[key] = (filename, getVidDownloadLink(filename))
            # Calculating the class name - the video files are usually formatted as classname-somenumbers
            i = 0
            while className[i] != "-" and i < len(className):
                i += 1
            # If no class name can be determined, gives it a generic class name
            if i == len(className):
                className = "class" + str(numClasses)
            else:
                className = className[:i]
            final_dict[className] = dict

    return final_dict
