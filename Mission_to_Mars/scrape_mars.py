# import dependencies
from bs4 import BeautifulSoup

from splinter import Browser

import time
import re
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #scrape latest news
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    #delay to make sure the browser runs before the soup
    time.sleep(3)
    html = browser.html
    soup_news = BeautifulSoup(html, 'html.parser')

    #retrieve latest news title
    title_results = soup_news.find_all('div', class_='content_title')
    news_title = title_results[0].text.strip()

    #retieve latest news paragraph text
    paragraph_results = soup_news.find_all('div', class_='article_teaser_body')
    news_p = paragraph_results[0].text.strip()

    print(f"""Latest News
    ---
    {news_title}
    ---
    {news_p}""")


    #scrape featured image
    base_url = 'https://www.jpl.nasa.gov'
    search_url = '/spaceimages/?search=&category=Mars'
    url_image = base_url+search_url
    browser.visit(url_image)

    #delay to make sure the browser runs before the soup
    time.sleep(3)
    html = browser.html
    soup_image = BeautifulSoup(html, 'html.parser')

    #retrieve url
    url_search = soup_image.find_all('div', class_='carousel_container')[0].find('article')['style']

    #store url
    # Helpful source: https://stackoverflow.com/questions/19449709/how-to-extract-string-inside-single-quotes-using-python-script
    feature_url = re.findall(r"'(.*?)'", url_search)[0]
    featured_image_url = base_url+feature_url
    print(featured_image_url)


    #scrape weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    #delay to make sure the browser runs before the soup
    time.sleep(3)
    html = browser.html
    soup_twitter = BeautifulSoup(html, 'html.parser')

    #store weather
    weather_results = soup_twitter.find_all('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_weather = weather_results[0].text.replace('\n',' ')

    print (f"""Mars Weather
    ---
    {mars_weather}""")


    #scrape facts
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)

    #extract table and clean
    df = facts_table[0]
    df.columns = ['Description', 'Value']
    # df.set_index('Description', inplace=True)

    #table to html in html_table variable
    html_table = df.to_html(classes='', border=False, index=False)
    html_table = html_table.replace('\n', '')

    print ("df complete")



    #scrape hemispheres
    base_url = 'https://astrogeology.usgs.gov'
    search_url = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_url = base_url+search_url
    browser.visit(hemisphere_url)

    # delay to make sure the browser runs before the soup
    time.sleep(3)
    html = browser.html
    soup_hemisphere = BeautifulSoup(html, 'html.parser')

    #obtain list of hemisphere related html
    hem_items = soup_hemisphere.find_all('div', class_='item')

    #set up list for saving hemisphere dictionaries
    hemisphere_image_urls = []

    #iterating through each hemisphere
    for item in hem_items:
        
    #set up dictionary for title and img_url
        hem_dict = {}
        
        #find hemisphere name
        hem_name = item.find('h3').text
        
        #clean and store title
        h_img_title = hem_name.split(' Enhanced')[0]
        hem_dict['title']= h_img_title 
        
        #navigate to specific site to retrieve image
        browser.click_link_by_partial_text(hem_name)

        # delay to make sure the browser runs before the soup for hemisphere page
        time.sleep(3)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        # retrieve image
        hem_img = soup.find_all('img', class_='wide-image')
        h_img_url = hem_img[0]['src']
        h_img_url_full = base_url + h_img_url
        hem_dict['img_url']= h_img_url_full
        
        #add to list
        hemisphere_image_urls.append(hem_dict)
        
        #get back to main page
        browser.back()
    print(hemisphere_image_urls)

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img": featured_image_url,
        "weather": mars_weather,
        "facts": html_table,
        "hemispheres": hemisphere_image_urls
    }

    browser.quit()

    return mars_data