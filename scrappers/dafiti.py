from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from categoryConverter import categoryConverter
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

elasticsearchClient = Elasticsearch(
    [os.environ.get("ELASTICSEARCH_HOST")], 
    scheme="http", 
    port=os.environ.get("ELASTICSEARCH_PORT")
)

# Delete all documents with provider dafiti 
try: elasticsearchClient.delete_by_query(index="products", body={"query": {"match": {"provider": "Dafiti"}}})
except: pass

# Create driver
driver = webdriver.Firefox()

# Set empty products list to fill with scrapped data 
products = []

# Loop over number of pages to scrape data from 
for page in range(2):

  # Go to dafiti website 
  driver.get(f'https://www.dafiti.com.co/precio-especial/?dir=desc&sort=discount&special_price={page + 1}')

  # Wait for page to load
  time.sleep(3)

  # For each product card, get values 
  for n in range(100):
    product = {}
    try: 
      if int(driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-saleFlagPercent').text[1:-1]) >= 50:
        product['title'] = driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-title').text 
        product['discount'] = int(driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-saleFlagPercent').text[1:-1])
        product['imageLink'] = driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-img').get_attribute('src')        
        product['link'] = driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-link').get_attribute('href')
        product["provider"] = "Dafiti"
        # Click on product to get its category
        driver.find_elements_by_class_name('itm-product-main-info')[n].click()
        product['category'] = categoryConverter(driver.find_elements_by_css_selector('li.prs')[2].text.split()[0])
        if product not in products: products.append(product)
      driver.execute_script("window.history.go(-1)")
      y = 500
      for timer in range(20):
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 500  
        time.sleep(1.5)
    except: break

# Close session
driver.close()

#Index every product to elasticsearch 
for product in products: elasticsearchClient.index(index="products", document=product)

