from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
	data = {}
	
	executable_path = {'executable_path': 'chromedriver'}
	browser = Browser('chrome', **executable_path, headless=True)
	
	# Retrieve news title and description
	url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
	browser.visit(url)
    
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
    
	news_article = soup.find('li', class_='slide')

	news_title = news_article.find('div', class_="content_title").get_text()
	news_p = news_article.find('div', class_="article_teaser_body").get_text()
	
	############
	
	# Retrieve featured image
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url)
    
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	featured_image = soup.find('a', class_='button fancybox')['data-fancybox-href']
	featured_image_url = 'https://www.jpl.nasa.gov' + featured_image
	
	############
	
	# Retrieve tweet
	url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(url)
    
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	first_tweet = soup.find('li', class_='js-stream-item stream-item stream-item')
	tweet_p = first_tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
	tweet_p.a.extract()

	mars_weather = tweet_p.get_text()
	
	############
	
	# Scrape info table
	url = 'https://space-facts.com/mars/'
	tables = pd.read_html(url)
	df = tables[0]
	html_table = df.to_html()

	############
	
	# Scrape hemispheres and images
	hemisphere_image_urls =[]

	for i in range(4):
		
		img_dict ={}
		
		url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
		browser.visit(url)
		
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')

		items = soup.find_all('div', class_='item')
		
		img_dict['title'] = items[i].find('h3').get_text()
		
		results = browser.find_by_tag('h3')
		results[i].click()
		
		img_dict['img_url'] = browser.find_by_text('Sample')['href']
		
		hemisphere_image_urls.append(img_dict)

	############
	
	data['news_title'] = news_title
	data['news_p'] = news_p
	data['featured_image_url'] = featured_image_url
	data['mars_weather'] = mars_weather
	data['html_table'] = html_table
	data['hemisphere_image_urls'] = hemisphere_image_urls
	
	return data