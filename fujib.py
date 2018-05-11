__author__ = "Brenden"
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import tweepy
from random import *
import lxml

errorPos = []
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_pos():
    pos1 = randint(1, 6)
    pos2 = randint(1, 26)
    pos = "qpos_"+str(pos1)+"_"+str(pos2)
    print(pos)
    return pos


def get_motivate_quote(quoteNum):
    browser = webdriver.Chrome("/Users/Brenden/Desktop/chromedriver.exe")

    browser.get("https://www.brainyquote.com/topics/motivational")
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    no_of_pagedowns = 50

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns -= 1

    quote = browser.find_element_by_xpath('//*[@id=\"'+quoteNum+'\"]/div[1]/div/a[1]').text
    author = browser.find_element_by_xpath('//*[@id=\"'+quoteNum+'\"]/div[1]/div/a[2]').text
    print(quote+"\n"+"-"+author)
    return quote+"\n"+"-"+author


def get_daily_quote():
    browser = webdriver.Chrome("/Users/Brenden/Desktop/chromedriver.exe")

    browser.get("https://www.brainyquote.com/quote_of_the_day")
    time.sleep(1)

    browser.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[1]/div[1]/div/a/img').click()
    imageQuote = browser.find_element_by_xpath('//*[@id="quotePageTopHolder"]/div/div/div[1]/div/div/div/div[2]/div[1]/div[3]/p[1]').text
    author = browser.find_element_by_xpath('//*[@id="quotePageTopHolder"]/div/div/div[1]/div/div/div/div[2]/div[1]/div[3]/p[2]/a').text
    return imageQuote+"\n"+"-"+author


def get_love_quote():
    browser = webdriver.Chrome("/Users/Brenden/Desktop/chromedriver.exe")

    browser.get("https://www.brainyquote.com/quote_of_the_day")
    time.sleep(1)

    loveQuote = browser.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[2]/div[2]/div/div/div[1]/div/a[1]').text
    author = browser.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[2]/div[2]/div/div/div[1]/div/a[2]').text
    return loveQuote+"\n"+"-"+author


while 1:
    tweets = api.user_timeline('jibbyjibstar', 20)
    daily = get_daily_quote()
    love = get_love_quote()
    position = get_pos()
    motivate = get_motivate_quote(position)

    if len(motivate) > 280:
        errorPos.append(position)
        position = get_pos()
        if position in errorPos:
            position = get_pos()
        motivate = get_motivate_quote(position)

    while motivate in tweets:
        position = get_pos()
        if position in errorPos:
            position = get_pos()
        motivate = get_motivate_quote(position)

    api.update_status(daily)
    time.sleep(60)
    api.update_status(love)
    time.sleep(60)
    api.update_status(motivate)
