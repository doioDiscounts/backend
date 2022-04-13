from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from utils.categoryConverter import categoryConverter
from dotenv import load_dotenv
from utils.localOrElasticsearch import localOrElasticsearch

load_dotenv()

driver = webdriver.Firefox()

driver.get('https://www.alkosto.com/')

products = []

action = ActionChains(driver)
# Loop over categories
for categoryIndex in range(15):
    # Loop over subcategories
    for subCategoryIndex in range(15):

        # Hover over category
        action.move_to_element(driver.find_elements_by_css_selector('.option-link')[categoryIndex].find_element_by_tag_name('span')).perform()
        category = driver.find_elements_by_css_selector('.option-link')[categoryIndex].find_element_by_tag_name('span').text
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

localOrElasticsearch("local", products, "Alkosto")