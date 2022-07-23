from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import date
from datetime import time
import time as t
import pandas as pd

from config import login, password


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
delay = 3
#login

driver.get("https://passport.yandex.ru/")   

t.sleep(delay)

inputFieldLogin = driver.find_element(By.ID, "passp-field-login") #passp-field-login
inputFieldLogin.send_keys(login)

t.sleep(delay)

button1Login = driver.find_element(By.CSS_SELECTOR, "button#passp\:sign-in")
button1Login.click()

t.sleep(delay)

inputFieldPass = driver.find_element(By.ID, "passp-field-passwd")
inputFieldPass.send_keys(password)

t.sleep(delay)

button1Pass = driver.find_element(By.CSS_SELECTOR, "button#passp\:sign-in")
button1Pass.click()

#go to mailbox
t.sleep(delay)

userpic = driver.find_element(By.CSS_SELECTOR, "img.user-pic__image")
userpic.click()

t.sleep(delay)

mailLink = driver.find_element(By.XPATH, "//a[@href='https://mail.yandex.ru']")
mailLink.click()
t.sleep(3)

t.sleep(delay)

#get the letters
listOfMails = driver.find_element(By.XPATH, "//div[@class='ns-view-container-desc mail-MessagesList js-messages-list']")
soup = BeautifulSoup(driver.page_source, 'html.parser')
mailsContainer = soup.find('div', attrs={'class':'ns-view-container-desc mail-MessagesList js-messages-list'})
mails = mailsContainer.find_all('div', attrs = {'class':'mail-MessageSnippet-Content'})

months = {
    'января': 1,'февраля': 2,'марта': 3,'апреля': 4,'мая': 5,'июня': 6,
    'июля': 7,'августа': 8,'сентября': 9,'октября': 10,'ноября': 11,'декабря': 12
}

mails_array=[]
for i in mails:
    mail_from = i.find('span', attrs={'class':'mail-MessageSnippet-FromText'}).text
    mail_title = i.find('span', attrs={'class':'mail-MessageSnippet-Item mail-MessageSnippet-Item_subject'}).text
    row = i.find('span', attrs={'class':'mail-MessageSnippet-Item_dateText'})['title'].split(" ")
    year = 2022 # :(
    month = months[row[2]]
    day = row[1]
    hr, mnt = row[-1].split(':')
    mail_date = date(int(year), int(month), int(day))
    mail_time = time(int(hr), int(mnt))
    
    mails_array.append([mail_from, mail_title, mail_date, mail_time])

#print emails array in terminal
for i in mails_array:
    print(i)

df = pd.DataFrame(mails_array)
df.columns = ['from', 'title', 'date', 'time']
print('\n\n\n')
print(df)


###sending emails from drafts
draftFolder = driver.find_element(By.XPATH, "//div[@data-react-focusable-id='6']")
draftFolder.click()

def sendDraftLetter():
    draftFolder = driver.find_element(By.XPATH, "//div[@data-react-focusable-id='6']")
    draftFolder.click()
    t.sleep(delay)
    draftLetter = driver.find_element(By.XPATH, "//span[@class='mail-MessageSnippet-Item mail-MessageSnippet-Item_sender js-message-snippet-sender']")
    draftLetter.click()
    t.sleep(delay)
    sendButton = driver.find_element(By.XPATH, "//button[@class='Button2 Button2_pin_circle-circle Button2_view_default Button2_size_l']")
    sendButton.click()
    t.sleep(delay)
    try:
        backLink = driver.find_element(By.XPATH, "//div[@class='ComposeDoneScreen-Actions']")
        backLink.click()
    finally:    
        draftFolder.click()
    sendAllDraftLetters()

count_letters = 0
def sendAllDraftLetters():
    try:
        h1element = driver.find_element(By.CSS_SELECTOR, "h1 span")
        text_h1 = h1element.text
    except:
        text_h1 = ''
    if text_h1 != 'В папке «Черновики» нет писем':
        global count_letters
        count_letters+=1
        sendDraftLetter()
    else:
        if count_letters == 0:
            print('В папке «Черновики» нет писем')
        else:
            print('{} {} {}'.format("Отправлено писем", count_letters, "шт"))

###sending
sendAllDraftLetters()


###creating drafts
def makeDraftLetter(number):
    writeLetterButton = driver.find_element(By.XPATH, "//a[@aria-describedby='tooltip-0-1']")
    writeLetterButton.click()
    t.sleep(2)
    writeLetterTo = driver.find_element(By.XPATH, "//div[@title='Кому']")
    writeLetterTo.send_keys("test-test@gmail.com")
    writeLetterTitle = driver.find_element(By.XPATH, "//input[@class='composeTextField ComposeSubject-TextField']")
    writeLetterTitle.send_keys("Title " + str(number))
    closeLetterButtonX = driver.find_element(By.XPATH, "//button[@aria-label='Закрыть']")
    closeLetterButtonX.click()
for i in range(1, 11):
    makeDraftLetter(i)

renewLettersList = driver.find_element(By.XPATH, "//button[@class='Button2 Button2_view_action Button2_size_m Layout-m__sync--1YGpp qa-LeftColumn-SyncButton']")
renewLettersList.click()