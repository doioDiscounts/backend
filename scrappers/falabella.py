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

# Delete all documents with provider falabella 
try: elasticsearchClient.delete_by_query(index="products", body={"query": {"match": {"provider": "Falabella"}}})
except: pass

driver = webdriver.Firefox()

products = []

for categoryIndex in range(20):
    # Try to loop over all categories until out of range
    try:

        #Go to homescreen
        driver.get('https://www.falabella.com.co/falabella-co')

        #Close popup
        try: driver.find_element_by_xpath('//*[@id="acc-alert-deny"]').click()
        except: pass

        #Open sidebar
        driver.find_element_by_xpath('//*[@id="testId-HamburgerBtn-toggle"]/div[1]/div').click()

        #Open category
        category = driver.find_element_by_xpath('//*[@id="cross-header"]/div[3]/div/div[2]/div/ul').find_elements_by_tag_name('p')[categoryIndex].text
        driver.find_element_by_xpath('//*[@id="cross-header"]/div[3]/div/div[2]/div/ul').find_elements_by_tag_name('p')[categoryIndex].click()

        for subCategoryIndex in range(20):
            
            # Try to loop over every subcategory until finished and get out of range 
            try:

                #Open ver todo
                driver.find_elements_by_tag_name('b')[subCategoryIndex].click()
                time.sleep(3)
                

                #Append data for vertically alligned products
                for product in driver.find_elements_by_css_selector('div.jsx-4221770651.pod'): 
                    try: 
                        if int(product.find_element_by_css_selector('span.jsx-148017451.copy8.primary.jsx-1524574875.bold.pod-badges-item-LIST.pod-badges-item').text[:2]) > 49:
                            products.append({
                                "category": categoryConverter(driver.find_element_by_css_selector('h1.jsx-3139645404.l2category').text), 
                                "title": product.find_element_by_css_selector('b.jsx-4221770651.title2.primary.jsx-1524574875.bold.pod-subTitle').text, 
                                "discount": int(product.find_element_by_css_selector('span.jsx-148017451.copy8.primary.jsx-1524574875.bold.pod-badges-item-LIST.pod-badges-item').text[:2]),
                                "link": product.find_element_by_css_selector('a.jsx-4221770651.section-body.pod-link').get_attribute('href'),
                                "provider": "Falabella"
                            })
                    except: pass

                #Append data for horizontally alligned products
                for product in driver.find_elements_by_css_selector('div.jsx-4001457643.search-results-4-grid.grid-pod'): 
                    try:
                        if int(product.find_element_by_css_selector('span.jsx-148017451.copy8.primary.jsx-1524574875.bold.pod-badges-item-4_GRID.pod-badges-item').text[:2]) > 49:        
                            products.append({
                                "category": categoryConverter(driver.find_element_by_css_selector('h1.jsx-3139645404.l2category').text), 
                                "title": product.find_element_by_css_selector('b.jsx-3153667981.copy2.primary.jsx-1524574875.normal.pod-subTitle').text, 
                                "discount": int(product.find_element_by_css_selector('span.jsx-148017451.copy8.primary.jsx-1524574875.bold.pod-badges-item-4_GRID.pod-badges-item').text[:2]),
                                "link": product.find_element_by_css_selector('a.jsx-3153667981.jsx-3886284353.pod-summary.pod-link.pod-summary-4_GRID').get_attribute('href'),
                                "provider": "Falabella"
                            })
                    except: pass

                #Go to homescreen 
                driver.get('https://www.falabella.com.co/falabella-co')

                #Open sidebar
                driver.find_element_by_xpath('//*[@id="testId-HamburgerBtn-toggle"]/div[1]/div').click()

                #Open category
                driver.find_element_by_xpath('//*[@id="cross-header"]/div[3]/div/div[2]/div/ul').find_elements_by_tag_name('p')[categoryIndex].click()

            except: break
    
    except: 
        break

# For every product, get image
for item in range(len(products)):
    driver.get(products[item]["link"])
    time.sleep(1)
    products[item]["imageLink"] = driver.find_element_by_css_selector('img.jsx-2487856160').get_attribute('src')

driver.close()

#Index every product to elasticsearch 
for product in products: elasticsearchClient.index(index="products", document=product)