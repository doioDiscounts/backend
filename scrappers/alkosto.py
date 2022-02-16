from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from categoryConverter import categoryConverter
from dotenv import load_dotenv
import os

load_dotenv()

elasticsearchClient = Elasticsearch(
    [os.environ.get("ELASTICSEARCH_HOST")], 
    scheme="http", 
    port=os.environ.get("ELASTICSEARCH_PORT")
)

# Delete all documents with provider dafiti 
try: elasticsearchClient.delete_by_query(index="products", body={"query": {"match": {"provider": "Alkosto"}}})
except: pass

driver = webdriver.Firefox()

driver.get('https://www.alkosto.com/')

products = []

action = ActionChains(driver)
# Loop over categories
for categoryIndex in range(15):
    # Loop over subcategories
    for subCategoryIndex in range(15):
        # Hover over category
        action.move_to_element(driver.find_element_by_css_selector('.main-navigation').find_elements_by_tag_name('span')[categoryIndex]).perform()
        category = driver.find_element_by_css_selector('.main-navigation').find_elements_by_tag_name('span')[categoryIndex].text
        # Go to subcategory link with size 100 products
        driver.get(f'{driver.find_elements_by_css_selector(".subcategories--item--label")[subCategoryIndex].find_element_by_tag_name("a").get_attribute("href")}?page=1&pageSize=100&sort=relevance')
        # Lazy load images
        y = 500
        for timer in range(20):
            driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 500  
            time.sleep(1.5)
        # Get get products with more than 40% discount
        for product in driver.find_elements_by_css_selector(".product__list--item.product__list--alkosto"):
            try: 
                if (float(product.find_element_by_css_selector(".price").text.replace('$', '').replace('.', '')) * 100)/float(product.find_element_by_css_selector(".product__price--discounts__old").text.replace('$', '').replace('.', '')) < 60:
                    item = {}
                    item["discount"] = 100 - int((float(product.find_element_by_css_selector(".price").text.replace('$', '').replace('.', '')) * 100)/float(product.find_element_by_css_selector(".product__price--discounts__old").text.replace('$', '').replace('.', '')))
                    item["title"] = product.find_elements_by_css_selector(".js-product-click-datalayer")[4].text 
                    item["imageLink"] = product.find_element_by_tag_name("img").get_attribute("src")
                    item["link"] = product.find_element_by_css_selector(".js-product-click-datalayer").get_attribute("href")
                    item["provider"] = "Alkosto"
                    item["category"] = categoryConverter(category)
                    if item not in products: products.append(item)
            except: pass

# Close session
driver.close()

#Index every product to elasticsearch 
for product in products: elasticsearchClient.index(index="products", document=product)