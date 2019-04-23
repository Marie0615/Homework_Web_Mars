# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time 


#function to initialize browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# ### NASA Mars News

def scrape():
    browser = init_browser()
  
    mars_news_url= 'https://mars.nasa.gov/news/'
    browser = init_browser()
    browser.visit(mars_news_url)
    news_title = browser.find_by_css('.content_title').first.text
    news_p = browser.find_by_css('.article_teaser_body').first.text
    
# ### JPL Mars Space Images - Featured Image

    mars_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = init_browser()
    browser.visit(mars_images)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    jpl_results = jpl_soup.find('article')
    extension = jpl_results.find('a')['data-fancybox-href']
    jpl_link = "https://www.jpl.nasa.gov"
    featured_image_url = jpl_link + extension

#Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page.
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"

    browser.visit(mars_weather_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    weather_info_list = []

    for weather_info in soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_info_list.append(weather_info.text)
    mars_weather = weather_info_list[0]
    
# ## Mars Facts

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_df =  pd.read_html (mars_facts_url, attrs = {'id': 'tablepress-mars'})[0]
    mars_facts_df.columns = ['Measurement','Value']
    mars_fact_df = mars_facts_df.set_index('Measurement')
    mars_facts_html = mars_fact_df.to_html()
    
# ## Mars Hemisperes

    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisperes_response = requests.get(mars_hemispheres_url)
    hemisperes_soup = BeautifulSoup(hemisperes_response.text, 'html.parser')

    hemisperes_list = hemisperes_soup.find_all('a', class_="itemLink product-item")
    hemisperes_list

    hemisphere_image_urls = []
    for hemi_img in hemisperes_list:
        img_title = hemi_img.find('h3').text
        link_to_img = "https://astrogeology.usgs.gov/" + hemi_img['href']
        img_request = requests.get(link_to_img)
        soup = BeautifulSoup(img_request.text, 'html.parser')
        img_tag = soup.find('div', class_='downloads')
        img_url = img_tag.find('a')['href']
        hemisphere_image_urls.append({"Title": img_title, "Image_Url": img_url})
    
    
    mars_data = {
     "News_Title": news_title,
     "Paragraph_Text": news_p,
     "Most_Recent_Mars_Image": featured_image_url,
     "Mars_Weather": mars_weather,
     "Mars_hem": hemisphere_image_urls,
     "Mars_Facts" : mars_facts_html
     
     }
    return mars_data  