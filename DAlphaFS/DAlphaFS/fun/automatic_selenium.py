from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def trywithPasswords(pwd):
    driver = webdriver.Chrome('chromedriver')
    #driver.get("http://10.0.0.148:8000/login/?next=/home")
    driver.get("http://127.0.0.1:8000/login/?next=/home")
    print(driver.title)
    search_bar = driver.find_element_by_name("username")
    search_bar.clear()
    search_bar.send_keys("testing")
    password_bar = driver.find_element_by_name("password")
    password_bar.send_keys(pwd)
    #submit_button = driver.find_element_by_class_name("login_container")
    submit_button = driver.find_element_by_xpath("//input[@value='Login']")
    submit_button.click()
    try:
        home_btn = driver.find_element_by_name("Homebtn")
        if(home_btn):
            print("Success")
        else:
            print("Failure")
        #search_bar.send_keys(Keys.RETURN)
        print(driver.current_url)
    except(Exception) as error:
        driver.close()
        return None
    
    driver.close()
    return pwd

password_ls = ['abc','nononono','ghi','kbc','Nov@2021;;']
for pwd in password_ls:
    pwd_var = trywithPasswords(pwd)
    if(pwd_var is None):
        continue
    else:
        print("Hey, the password is"+pwd_var)

