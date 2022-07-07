from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
import time
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF.settings')
import django
django.setup()
from junho.models import CU, GS25, MINISTOP
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--incognito")
# options.add_argument("--disable-setuid-sandbox")
options.add_argument('window-size=1920,1080')
# options.add_argument("--remote-debugging-port=9222")


path='/var/www/html/DRF/chromedriver'
#driver = webdriver.Chrome(path,options=options)
######## GS25 1+1 크롤링 ####################



count1, count2, count3 = 0,1,2
itemlist = []
imglist = []
imgcount = 0
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('http://gs25.gsretail.com/gscvs/ko/products/event-goods#;')
    
count1, count2, count3 = 0,1,2
imgcount = 0
time.sleep(1)
a = driver.find_element_by_class_name('prod_list').text
b = driver.find_element_by_class_name('prod_list').find_elements_by_class_name('img')
itemlist = a.split('\n')

for i in range(0,len(b)):
        try:imglist.append(b[i].find_element_by_css_selector('img'))
        except:imglist.append('NULL')
        continue

for i in range(0,int(len(itemlist)/3)):
        if imglist[imgcount]=='NULL':
            GS25.objects.create(
        name = itemlist[count1],
        price = itemlist[count2],
        type = itemlist[count3],
        image = "사진 없습니다."
        )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 1
        else:
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = imglist[imgcount].get_attribute('src')
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 1
imglist = []
itemlist = [] 
while True:
    count1, count2, count3 = 0,1,2
    imgcount = 0
    breakitem = itemlist
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[1]/div/a[3]').click()
    time.sleep(1)
    a = driver.find_element_by_class_name('prod_list').text
    b = driver.find_element_by_class_name('prod_list').find_elements_by_class_name('img')
    itemlist = a.split('\n') 
    if breakitem == itemlist:
        break
    for i in range(0,len(b)):
        try:imglist.append(b[i].find_element_by_css_selector('img'))
        except:imglist.append('NULL')
        continue
      
    for i in range(0,int(len(itemlist)/3)):
        if imglist[imgcount]=='NULL':
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = "사진 없습니다."
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 1
        else:
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = imglist[imgcount].get_attribute('src')
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 1
    imglist = []

########## GS25 2+1 크롤링 ####################
count1, count2, count3 = 0,1,2
itemlist = []
imglist = []
imgcount = 0
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('http://gs25.gsretail.com/gscvs/ko/products/event-goods#;')
driver.find_element_by_xpath('//*[@id="TWO_TO_ONE"]').click()

count1, count2, count3 = 0,1,2
imgcount = 0
time.sleep(1)
a = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[2]').find_element_by_class_name('prod_list')
b = driver.find_element_by_class_name('prod_list').find_elements_by_class_name('img')
item = a.text
itemlist = item.split('\n')

for i in range(0,len(b)):
        try:imglist.append(b[i].find_element_by_css_selector('img'))
        except:imglist.append('NULL')
        continue

for i in range(0,int(len(itemlist)/3)):
        if imglist[imgcount]=='NULL':
            GS25.objects.create(
        name = itemlist[count1],
        price = itemlist[count2],
        type = itemlist[count3],
        image = "사진 없습니다."
        )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 1
        else:
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = imglist[imgcount].get_attribute('src')
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 1
imglist = []
itemlist = [] 
while True:
    count1, count2, count3 = 0,1,2
    imgcount = 0
    breakitem = itemlist
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[2]/div/a[3]').click()
    time.sleep(1)
    a = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[2]').find_element_by_class_name('prod_list')
    b = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[2]/ul').find_elements_by_class_name('img')
    item = a.text
    itemlist = item.split('\n')
    if breakitem == itemlist:
        break
    for i in range(0,len(b)):
        try:imglist.append(b[i].find_element_by_css_selector('img'))
        except:imglist.append('NULL')
        continue
      
    for i in range(0,int(len(itemlist)/3)):
        if imglist[imgcount]=='NULL':
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = "사진 없습니다."
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 1
        else:
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = imglist[imgcount].get_attribute('src')
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 1
    if int(len(itemlist)/3) < 8:
        break
    imglist = []


########## GS25 덤증정 크롤링 ####################
count1, count2, count3 = 0,1,2
itemlist = []
imglist = []
dumlist =[]
imgcount = 0
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('http://gs25.gsretail.com/gscvs/ko/products/event-goods#;')
time.sleep(2)
driver.find_element_by_xpath('//*[@id="GIFT"]').click()
time.sleep(2)
a = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[3]').find_element_by_class_name('prod_list')
b = driver.find_element_by_class_name('prod_list').find_elements_by_class_name('img')


item = a.text
itemlist = item.split('\n')
itemlist = [x for x in itemlist if x]
for i in range(0,len(b)):
        try:imglist.append(b[i].find_element_by_css_selector('img'))
        except:imglist.append('NULL')
        continue
for i in range(0,int(len(itemlist)/3)):
        if imglist[imgcount]=='NULL':
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = "사진 없습니다.",
            GIFTimage = imglist[imgcount+1].get_attribute('src')
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 2
        elif imglist[imgcount+1]=='NULL':
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = imglist[imgcount].get_attribute('src'),
            GIFTimage = '사진 없습니다.'
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 2
        else:
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = imglist[imgcount].get_attribute('src'),
            GIFTimage = imglist[imgcount+1].get_attribute('src')
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 2
imglist = [] 
itemlist=[]
while True:
    count1, count2, count3 = 0,1,2
    imgcount = 0
    breakitem = itemlist
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[3]/div/a[3]').click()
    time.sleep(1)
    a = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div/div/div[3]').find_element_by_class_name('prod_list')
    b = driver.find_element_by_class_name('prod_list').find_elements_by_class_name('img')
    item = a.text
    itemlist = item.split('\n')
    itemlist = [x for x in itemlist if x]
    if breakitem == itemlist:
        break
    for i in range(0,len(b)):
        try:imglist.append(b[i].find_element_by_css_selector('img'))
        except:imglist.append('NULL')
        continue
    
    for i in range(0,int(len(itemlist)/3)):
        if imglist[imgcount]=='NULL':
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = "사진 없습니다.",
            GIFTimage = imglist[imgcount+1].get_attribute('src')
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 2
        elif imglist[imgcount+1]=='NULL':
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = imglist[imgcount].get_attribute('src'),
            GIFTimage = '사진 없습니다.'
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 2
        else:
            GS25.objects.create(
            name = itemlist[count1],
            price = itemlist[count2],
            type = itemlist[count3],
            image = imglist[imgcount].get_attribute('src'),
            GIFTimage = imglist[imgcount+1].get_attribute('src')
            )
            count1 += 3
            count2 += 3
            count3 += 3
            imgcount += 2
    if int(len(itemlist)/3) < 8:
        break
    imglist = []

######### 미니스톱 1+1 크롤링 ####################
itemlist = []
count1, count2, count3 = 0,1,2
imgcount = 0
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://www.ministop.co.kr/MiniStopHomePage/page/event/plus1.do')

for i in range(20):
    driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]/div/a[1]').click()
    time.sleep(0.5)
     
a = driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]').text
b = driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]').find_elements_by_css_selector('img')
itemlist = a.split('\n')
itemlist.remove('더보기')  
itemlist.remove('맨위로')  
for i in range(0,int(len(itemlist)/3)):
    MINISTOP.objects.create(
        name = itemlist[count2],
        price = itemlist[count3],
        type = itemlist[count1],
        image = b[imgcount].get_attribute('src'),
        )
    count1 += 3
    count2 += 3
    count3 += 3
    imgcount += 1


######## 미니스톱 2+1 크롤링 ####################
itemlist = []
count1, count2, count3 = 0,1,2
imgcount = 0
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://www.ministop.co.kr/MiniStopHomePage/page/event/plus1.do')
driver.find_element_by_xpath('//*[@id="section"]/div[3]/ul/li[2]/a').click()

for i in range(40):
    driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]/div/a[1]').click()
    time.sleep(0.5)
     
a = driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]').text
b = driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]').find_elements_by_css_selector('img')
itemlist = a.split('\n')
itemlist.remove('더보기')  
itemlist.remove('맨위로')  
for i in range(0,int(len(itemlist)/3)):
    MINISTOP.objects.create(
        name = itemlist[count2],
        price = itemlist[count3],
        type = itemlist[count1],
        image = b[imgcount].get_attribute('src'),
        )
    count1 += 3
    count2 += 3
    count3 += 3
    imgcount += 1
######### 미니스톱 N+N 크롤링 ####################

itemlist = []
count1, count2, count3 = 0,1,2
imgcount = 0
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://www.ministop.co.kr/MiniStopHomePage/page/event/plus1.do')
driver.find_element_by_xpath('//*[@id="section"]/div[3]/ul/li[3]/a').click()

for i in range(10):
    driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]/div/a[1]').click()
    time.sleep(0.5)
     
a = driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]').text
b = driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]').find_elements_by_css_selector('img')
itemlist = a.split('\n')
itemlist.remove('더보기')  
itemlist.remove('맨위로')  
for i in range(0,int(len(itemlist)/3)):
    MINISTOP.objects.create(
        name = itemlist[count2],
        price = itemlist[count3],
        type = itemlist[count1],
        image = b[imgcount].get_attribute('src'),
        )
    count1 += 3
    count2 += 3
    count3 += 3
    imgcount += 1
######### 미니스톱 덤증정 크롤링 ####################

itemlist = []
count1, count2, count3, count4 = 0,1,2,3
imgcount = 0
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://www.ministop.co.kr/MiniStopHomePage/page/event/plus1.do')
driver.find_element_by_xpath('//*[@id="section"]/div[3]/ul/li[4]/a').click()

for i in range(10):
    driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]/div/a[1]').click()
    time.sleep(0.5)
     
a = driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]').text
b = driver.find_element_by_xpath('//*[@id="section"]/div[3]/div[3]').find_elements_by_css_selector('img')
itemlist = a.split('\n')
remove_set = {'더보기','맨위로','증정상품','증정행사','0원'}
itemlist = [i for i in itemlist if i not in remove_set]
print(itemlist)
for i in range(0,int(len(itemlist)/4)):
    MINISTOP.objects.create(
        name = itemlist[count2],
        price = itemlist[count3],
        type = itemlist[count1],
        GIFTname = itemlist[count4],
        image = b[imgcount].get_attribute('src'),
        GIFTimage = b[imgcount+1].get_attribute('src'),
        )
    count1 += 4
    count2 += 4
    count3 += 4
    count4 += 4
    imgcount += 2

######### CU 1+1 크롤링 ####################
count1, count2, count3, count4 = 0,1,2,3
imgcount = 0
imglist = []
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N')
time.sleep(2)
driver.find_element_by_xpath('//*[@id="contents"]/div[1]/ul/li[2]/a').click()
time.sleep(2)
for i in range(10):
    try:
        driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div/div/div[1]/a').click()
    except:
        pass
    time.sleep(3)     
a = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div').text
b = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div').find_elements_by_css_selector('img')
itemlist = a.split('\n')
remove_set = {'https://cu.bgfretail.com/images/icon/tag_new.png','https://cu.bgfretail.com/images/icon/tag_best.png','원'}
for i in b:
    imglist.append(i.get_attribute('src'))
imglist = [i for i in imglist if i not in remove_set]
itemlist = [i for i in itemlist if i not in remove_set]

for i in range(0,int(len(itemlist)/3)):
    CU.objects.create(
        name = itemlist[count1],
        price = itemlist[count2],
        type = itemlist[count3],
        image = imglist[imgcount],
        )
    count1 += 3
    count2 += 3
    count3 += 3
    imgcount += 1
######## CU 2+1 크롤링 ####################
driver.close()
count1, count2, count3, count4 = 0,1,2,3
imgcount = 0
imglist = []
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N')
time.sleep(2)
driver.find_element_by_xpath('//*[@id="contents"]/div[1]/ul/li[3]/a').click()
time.sleep(2)
for i in range(80):
    try:
        driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div/div/div[1]/a').click()
    except:
        pass
    time.sleep(3)     
a = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div').text
b = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div').find_elements_by_css_selector('img')
itemlist = a.split('\n')
remove_set = {'https://cu.bgfretail.com/images/icon/tag_new.png','https://cu.bgfretail.com/images/icon/tag_best.png','원'}
for i in b:
    imglist.append(i.get_attribute('src'))
imglist = [i for i in imglist if i not in remove_set]
itemlist = [i for i in itemlist if i not in remove_set]

for i in range(0,int(len(itemlist)/3)):
    CU.objects.create(
        name = itemlist[count1],
        price = itemlist[count2],
        type = itemlist[count3],
        image = imglist[imgcount],
        )
    count1 += 3
    count2 += 3
    count3 += 3
    imgcount += 1
driver.quit()