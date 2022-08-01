from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import selenium.webdriver.support.ui as ui
import time
import datetime as datetime
time.start = time.time()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#Create a dataframe 
data = {
    "CE Ref" : [],
    "Name" : [],
    "Chinese Name" : [],
    "Main business address" : [],
    "Y/N" : []
}
 
df = pd.DataFrame(data)

#Required sfc website
url = "https://apps.sfc.hk/publicregWeb/searchByRa?locale=en"

#Get user input for which type: 1,2,...,9
type_number = input("Please input the type number: ")
converted_type_number = int(type_number) + 1018

driver = webdriver.Chrome(executable_path=r'C:\Users\micmic\Desktop\python\sfc\chromedriver.exe', options=options) #<--Change the appropriate dir of the excel file
driver.get(url)
driver.find_element_by_id("roleTypeCorporation-inputEl").click() #Click Corporation
time.sleep(0.5)
driver.find_element_by_id("radiofield-"+str(converted_type_number)+"-inputEl").click() #Type2:1020; Type9:1027
time.sleep(0.5)

#Extract data from the a page of website
def extract_data (dataframe):
    time.sleep(5)
    WebDriverWait(driver,100).until(lambda driver: driver.find_element_by_xpath("//*[@id='gridview-1046']/table/tbody/tr/td/div"))
    ce_ref = driver.find_elements_by_xpath("//*[@id='gridview-1046']/table/tbody/tr/td[1]/div")
    name = driver.find_elements_by_xpath("//*[@id='gridview-1046']/table/tbody/tr/td[2]/div")
    chinname = driver.find_elements_by_xpath("//*[@id='gridview-1046']/table/tbody/tr/td[3]/div")
    address = driver.find_elements_by_xpath("//*[@id='gridview-1046']/table/tbody/tr/td[6]/div")
    yesno = driver.find_elements_by_xpath("//*[@id='gridview-1046']/table/tbody/tr/td[7]/div")
    for (x,y,z,u,v) in zip(ce_ref,name,chinname,address,yesno):
        print(x.text,' ', y.text,' ', z.text,' ', u.text,' ',v.text)
        dataframe = dataframe.append({'CE Ref': x.text, 'Name': y.text, "Chinese Name": z.text, "Main business address" : u.text, "Y/N" : v.text}, ignore_index= True)
    return dataframe

#Get page number: return -99 if there is no data displayed
def get_page_number():
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.ID, "tbtext-1053")))
    page_number_rawtext = driver.find_element_by_id("tbtext-1053").text
    if (page_number_rawtext != ''):
        page_number = int(page_number_rawtext[3:])
        print("Page Number = " + str(page_number))
    else:
        page_number = -99
    return page_number

#Main program for looping
for i in range(1,37): #A-Z + 0-9 in total of 36 loops
    time.sleep(1)
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.ID, "ext-gen1069")))
    driver.find_element_by_id("ext-gen1069").click() #Clicking the dropdown button
    xpath = "//div[@id='boundlist-1064-listEl']/ul/li["+str(i)+"]"
    time.sleep(1)
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    driver.find_element_by_xpath(xpath).click() #Clicking A-Z, 0-9
    time.sleep(1)
    WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.ID, "button-1011-btnInnerEl")))
    driver.find_element_by_id("button-1011-btnInnerEl").click() #Clicking "Search" button
    time.sleep(5)
    page_number = get_page_number()
    if page_number != -99:
        for counter in range(page_number):  #Loop through each page
            df = extract_data(df)
            print("Page " + str(counter + 1) + " completed! ")
            WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.ID, "button-1055-btnIconEl")))
            driver.find_element_by_id("button-1055-btnIconEl").click() #Clicking the "next page" button
    else:
        print("Blank Page!")

print(df)

#Display the amount of time needed to run the report
time.end = time.time()
print(time.end - time.start)

#Display the current day, month and year
currentDay = str(datetime.datetime.now().day)
currentMonth = str(datetime.datetime.now().month)
currentYear = str(datetime.datetime.now().year)

#Amend the excel sheet
sheetname = currentYear + currentMonth + ' Type ' + type_number
with pd.ExcelWriter('sfcoutput.xlsx',mode='a',engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name = sheetname, index = False)


print("---------------------------End of script!---------------------------")
