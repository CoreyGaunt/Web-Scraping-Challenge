# Bring in my dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
    

mars_data = {}

def scrape_new():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    article_title = soup.find('div',class_='list_text').find('div', class_='content_title').find('a').text
    article_paragraph = soup.find('div',class_='list_text').find('div', class_='article_teaser_body').text
    article = [article_title,article_paragraph]
    return article
    browser.quit()

def scrape_featured():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    base_url = 'https://www.jpl.nasa.gov/'
    image_path_url = soup.find('div', class_='carousel_container').find('article')['style'].replace(');','')[23:-1]
    featured_img_url = base_url + image_path_url
    return featured_img_url
    browser.quit()

def scrape_facts():
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    facts = pd.read_html(url)
    mars_facts = facts[0]
    mars_facts.columns = ['Description','Value']
    mars_Facts = mars_facts.to_html(index=False)
    return mars_Facts
    browser.quit()

def scrape_hemi():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    results = soup.find_all('div',class_='item')
    hemisphere_urls = []

    for result in results:
        title = result.find('div',class_='description').find('h3').text
        base = 'https://astrogeology.usgs.gov/'
        img_1 = result.find('div',class_='description').find('a')['href']
        browser.visit(base + img_1)
        img_html = browser.html
        soup = bs(img_html,'html.parser')
        img_url = base + soup.find('div',class_='wide-image-wrapper').find('img',class_='wide-image')['src']
        hemisphere_urls.append({'title':title,'img_url':img_url})
    return hemisphere_urls
    browser.quit()

def scrape():
    article1 = scrape_new()
    title = article1[0]
    paragraph = article1[1]
    featured_image = scrape_featured()
    facts = scrape_facts()
    hemispheres = scrape_hemi()

    compressed_scrape = {'news_title':title,
                        'news_paragraph':paragraph,
                        'featured_img':featured_image,
                        'facts':facts,
                        'hemispheres':hemispheres}
    return compressed_scrape