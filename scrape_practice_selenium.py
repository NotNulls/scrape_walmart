from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException
import time

options = Options()
options.add_argument('window-size=1600x1000')

driver = webdriver.Firefox(options=options)
driver.get('https://franchisedisclosure.gov.au/Register')

time.sleep(1)

continue_cookie_button = driver.find_element(By.ID, 'publictouaction')
checkbox = driver.find_element(By.ID, 'acceptTOU')
checkbox.click()
continue_cookie_button.click()

search_bar = driver.find_element(By.ID, 'Search_SearchTerm')

search_word = input('Please insert search criteria to look for: ')

search_bar.send_keys(search_word)

search_button = driver.find_element(By.ID, 'btnSearch')
search_button.click()

disclosure_check_box = driver.find_element(By.ID, 'Search_HasDisclosureDocument')

disclosure_check_question = input('Please select if you are looking for "Disclosure document available" (Y/N): ')
print(disclosure_check_box)

if disclosure_check_question.lower() == 'y':
    driver.execute_script("arguments[0].scrollIntoView(true);", disclosure_check_box)
    time.sleep(1)
    disclosure_check_box.click()
    time.sleep(3)
elif disclosure_check_question.lower() == 'n':
    pass
else:
    'Please type "Y" or "N"'
    print('\n')


all_names = driver.find_element(By.TAG_NAME, 'table')

time.sleep(1)

try:
    for row in driver.find_elements(By.TAG_NAME, 'tr')[1:]:
        # print (row.text)
        time.sleep(0.1)
        comp_name = [element.text.split('\n') for element in row.find_elements(By.TAG_NAME, 'td')][0][0]
        print(comp_name)
        if search_word != comp_name:
            time.sleep(1)
            next_button = driver.find_element(By.CLASS_NAME, 'svg-inline--fa fa-step-forward fa-w-14')
            next_button.click()
            print('check 1')
            link = row.find_element(By.TAG_NAME, 'td')
            driver.execute_script("arguments[0].scrollIntoView(true);", link)
            time.sleep(1)
            link.click()
            time.sleep(1)

        elif search_word == comp_name:
            print('check 2')
            link = row.find_element(By.TAG_NAME, 'td')
            driver.execute_script("arguments[0].scrollIntoView(true);", link)
            time.sleep(1)
            link.click()
            time.sleep(1)
            header = driver.find_elements(By.TAG_NAME, 'label')
            header = [element.text for element in header]
            print(len(header), header)
            print('\n\n')
            data = driver.find_elements(By.TAG_NAME, 'dd')
            data = [element.text.replace('\n', '') for element in data]
            print(len(data), data)

except StaleElementReferenceException as e:

    print(f'Error: {e}')

    # driver.close()
