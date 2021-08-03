#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

#################################################
# Mac
#################################################
# Set Executable Path & Initialize Chrome Browser
#executable_path = {"executable_path": "chromedriver"}
#browser = Browser("chrome", **executable_path, headless=False)

#################################################
# Windows
#################################################
# Set Executable Path & Initialize Chrome Browser
# executable_path = {"executable_path": "chromedriver.exe"}
# browser = Browser("chrome", **executable_path)


#################################################
# NASA Mars News
#################################################
# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    # Parse Results HTML with BeautifulSoup
    try:
        # Scrape the Latest News Title
        news_title = news_soup.find("div", class_="content_title").text
        news_paragraph = news_soup.find("div", class_="article_teaser_body").text

    except AttributeError:
        return None, None
    return news_title, news_paragraph


#################################################
# JPL Mars Space Images - Featured Image
#################################################
# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    images = soup.findAll('img')
    try:    
        for image in images:
            if 'featured' in image.attrs['src']:
                featured = image.attrs['src']
    except AttributeError:
        return None 
    # Concatenate website url with scrapped route
    featured_image_url = url + featured

    return featured_image_url


#################################################
# Mars Facts
#################################################
# Mars Facts Web Scraper
def mars_facts():
    # Visit Mars facts url 
    facts_url = 'https://galaxyfacts-mars.com/'
    try:
        # Use Panda's `read_html` to parse the url
        mars_facts = pd.read_html(facts_url)
    except BaseException:
        return None
    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value','Drop']
    mars_df = mars_df.drop(columns=['Drop'])

    # Set the index to the `Description` column without row indexing
    # mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html(classes="table table-striped",index=False)

    return data#df.to_html(classes="table table-striped")


#################################################
# Mars Hemispheres
#################################################
# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    imageList = []

    # Store the main_ul 
    hemispheres_main_url = 'https://marshemispheres.com/' 

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
           
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
            
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
            
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
            
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
        # Append the retreived information into a list of dictionaries 
        imageList.append({"title" : title, "img_url" : img_url})

    #mars_info['hiu'] = hiu
    return imageList


#################################################
# Main Web Scraping Bot
#################################################
def scrape_all():
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)

    print (news_title)
    print(news_paragraph)
    img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title
        ,"news_paragraph": news_paragraph
        , "featured_image": img_url
        , "facts": facts
        , "hemispheres": hemisphere_image_urls
       , "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())