from selenium import webdriver
import time
from utils import categoryConverter, localOrElasticsearch

driver = webdriver.Chrome(executable_path='/Users/eduardoblandon/Desktop/doioBackend/scrappers/chromedriver')
products = []

for page in range(2):

  driver.get(f'https://www.dafiti.com.co/precio-especial/?dir=desc&sort=discount&special_price={page + 1}')
  time.sleep(3)
  
  for n in range(100):
    product = {}
    try: 

      if int(driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-saleFlagPercent').text[1:-1]) >= 50:
        product['title'] = driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-title').text 
        product['discount'] = int(driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-saleFlagPercent').text[1:-1])
        product['imageLink'] = driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-img').get_attribute('src')        
        product['link'] = driver.find_elements_by_class_name('itm-product-main-info')[n].find_element_by_class_name('itm-link').get_attribute('href')
        product["provider"] = "Dafiti"
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

driver.close()
localOrElasticsearch("local", products, "Dafiti")
