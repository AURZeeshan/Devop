from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
import urllib
import urllib.request



# custom driver start -------
browser = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=browser)
url = 'https://www.trulia.com/'
driver.get(url)
List_page_window = driver.current_window_handle
# custom driver code END ---------- +

os.mkdir("Properties Images")



# Read a file code start ===========
enter_property_file = open('property.txt','r')
readlines_of_file= enter_property_file.readlines()
zips = readlines_of_file[0].replace('\n',' ')
category = readlines_of_file[1]


print(zips[0])

# condition if Rent or sale or sold enter present in the file or not
if category == "Rent" or category == "rent" or category == "for Rent" or category == "rent ":
    driver.find_element_by_xpath('//*[@class="HomePageBanner__ButtonContainer-sc-1t2xcfs-1 etwcnL"]/button[2]').click()
elif category == "sold" or category == "Sold" or category == "for sold":
    driver.find_element_by_xpath('//*[@class="HomePageBanner__ButtonContainer-sc-1t2xcfs-1 etwcnL"]/button[3]').click()
else:
    pass    
# Read a file code END here =========== ++





# send keys --------
searchbar = driver.find_element_by_id('banner-search')
searchbar.clear()
searchbar.send_keys(zips)
searchbar.send_keys(Keys.ENTER)
time.sleep(2)
# END send keys --------


# function for images download -------------------------------------------- function-1
def download_img(url , address):
    name = random.randrange(1,1000)
    global full_name
    try:
        full_name = str(address) 
        full_name += str(name) + '.jpg'

        urllib.request.urlretrieve(url,full_name)
        print('\t Your image is downloaded and saved.')
    except:
        full_name = None


# Download image function END ----------------------------------------------------


def detail(file,Place):
    print_me=[]
    Title = driver.find_elements_by_xpath('//*[@class="Text__TextBase-sc-1i9uasc-0 iAwkAJ"]')
    Address = driver.find_elements_by_xpath('//*[@class="Text__TextBase-sc-1i9uasc-0 irLYEY HomeSummaryShared__CityStateAddress-vqaylf-0 jFgJji"]')
    Price = driver.find_elements_by_xpath('//*[@class="Text__TextBase-sc-1i9uasc-0-div Text__TextContainerBase-sc-1i9uasc-1 qAaUO"]')
    
   
    
    nam = random.randrange(10,5000)
    os.chdir("Properties Images")
    prop = "Property " + str(nam)
    Word = os.getcwd()
    Word = Word + prop

    if os.path.isdir(Word):
        pass
    else:    
        os.mkdir(prop)
        os.chdir(prop)
        j = os.getcwd()
        images = driver.find_elements_by_xpath('//*[@class="HomeDetailsHero__Cell-hubkl0-3 HomeDetailsHero__CellWithBorder-hubkl0-9 bqbsdf"]/picture/source')
        e = 0
        while e < len(images):
            Imag1 = images[e].get_attribute('srcset')

            # Call a function Image to download images +++ =========
            path = j + "/img"
            download_img(Imag1,path)
            e+=1
            
            if e == 5:
                break
            
    
    k = os.getcwd()        
    os.chdir('..')
    os.chdir('..')
    
    d =0
    while d < len(Title):
        print_me.append(f"{Title[d].text},{Price[d].text.replace(',',' ')},{Address[d].text.replace(',',' ')},{Place},{k}")
        d=d+1

    for line in print_me:
        file.write(line+'\n')
        print(line)

    
    




# function for get detail of property -------------------------------------------------------------------  function-2
def get_Detail(Place):
    # check if file not exist in directroy condition start ----------------- IF
    if os.path.isfile('Trulia.csv'):
        filename=open("Trulia.csv", 'a')
        # open new Tab
        driver.execute_script("window.open('" + Place +"');")
        detail_page_window = driver.window_handles
        new_window = [x for x in detail_page_window if x != List_page_window][0]
        driver.switch_to.window(new_window)
        time.sleep(1)
        detail(filename,Place)
        filename.close()
        driver.close()
        driver.switch_to.window(List_page_window)    
    
    # check if file exist in directroy ELSE condition --------------- ELSE
    else:
        filename=open("Trulia.csv", 'w')
        driver.execute_script("window.open('" + Place +"');")
        detail_page_window = driver.window_handles
        new_window = [x for x in detail_page_window if x != List_page_window][0]
        driver.switch_to.window(new_window)
        filename.write(f'Title, Price, Address,Property URL, Image Path \n')
        detail(filename,Place)
        
        filename.close()
        driver.close()
        driver.switch_to.window(List_page_window)
# detail function END   ------------------------------------------------------





# start main code here ----------------------------
driver.execute_script("window.scroll(4000,4700)")
getpages= driver.find_elements_by_xpath('//*[@class="List__ListContainer-sc-1mezygb-0 kgdOJe SearchResultsPagination__PageLinkList-sc-1g9fbhd-1 cCOBPJ"]/li/a')

i = 0
while i < len(getpages):
    print("success",getpages[i].text)
    i+=1

    # Property Url to pass in function
    Places = driver.find_elements_by_xpath('//*[@class="Box-sc-8ox7qa-0 jDcCbK PropertyCard__PropertyCardContainer-sc-1ush98q-2 hQvvnw"]/a')

    # start while loop
    key = 0
    a = 0
    while a < len(Places):
        property_link = Places[a].get_attribute('href')
        print("Property No {} ,Property Link {}".format(property_link,key))
        a+=1
        # Call a function =====
        get_Detail(property_link)
        key +=1

# END main code here ------------------------------