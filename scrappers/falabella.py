from selenium import webdriver
import time
from utils.categoryConverter import categoryConverter
from utils.localOrElasticsearch import localOrElasticsearch

driver = webdriver.Firefox()

products = []

for categoryIndex in range(20):
    # Try to loop over all categories until out of range
    try:

        #Go to homescreen
        driver.get('https://www.falabella.com.co/falabella-co')

        driver.find_element_by_css_selector(".BackgroundImageOnly-module_half-width-only-desktop__OXKgG").click()

        #Open sidebar
        driver.find_element_by_css_selector(".HamburgerBtn-module_line__382dh").click()

        #Open category
        category = driver.find_element_by_xpath('//*[@id="cross-header"]/div[3]/div/div[2]/div/ul').find_elements_by_tag_name('p')[categoryIndex].text
        driver.find_element_by_xpath('//*[@id="cross-header"]/div[3]/div/div[2]/div/ul').find_elements_by_tag_name('p')[categoryIndex].click()

        for subCategoryIndex in range(20):
            
            # Try to loop over every subcategory until finished and get out of range 
            try:

                #Open ver todo
                driver.find_elements_by_tag_name('b')[subCategoryIndex].click()
                
                #Append data for vertically alligned products
                for product in driver.find_elements_by_css_selector('div.jsx-4221770651.pod'): 
                    try: 
                        if int(product.find_element_by_css_selector(".jsx-3167696911.jsx-2117988457.copy8.primary.jsx-3548557188.bold.pod-badges-item-LIST.pod-badges-item").text[:2]) > 10:  
                            products.append({
                                "category": categoryConverter(driver.find_element_by_css_selector('.jsx-2883309125.l2category').text), 
                                "title": product.find_element_by_css_selector(".jsx-4221770651.title2.primary.jsx-3548557188.bold.pod-subTitle").text, 
                                "discount": int(product.find_element_by_css_selector(".jsx-3167696911.jsx-2117988457.copy8.primary.jsx-3548557188.bold.pod-badges-item-LIST.pod-badges-item").text[:2]),
                                "link": product.find_element_by_css_selector('.jsx-3128226947.list-view').get_attribute('href'),
                                "provider": "Falabella"
                            })
                    except: pass

                #Append data for horizontally alligned products
                for product in driver.find_elements_by_css_selector('div.jsx-4001457643.search-results-4-grid.grid-pod'): 
                    try:
                        if int(product.find_element_by_css_selector('.jsx-3167696911.jsx-2117988457.copy8.primary.jsx-3548557188.bold.pod-badges-item-4_GRID.pod-badges-item').text[:2]) > 10:        
                            products.append({
                                "category": categoryConverter(driver.find_element_by_css_selector('.jsx-2883309125.l2category').text), 
                                "title": product.find_element_by_css_selector('.jsx-1327784995.copy2.primary.jsx-3548557188.normal.pod-subTitle').text, 
                                "discount": int(product.find_element_by_css_selector('.jsx-3167696911.jsx-2117988457.copy8.primary.jsx-3548557188.bold.pod-badges-item-4_GRID.pod-badges-item').text[:2]),
                                "link": product.find_element_by_css_selector('.jsx-1327784995.jsx-97019337.pod-summary.pod-link.pod-summary-4_GRID').get_attribute('href'),
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

localOrElasticsearch("local", products, "Falabella")