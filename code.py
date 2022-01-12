import discord
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

client = discord.Client()

driver = webdriver.Chrome(ChromeDriverManager().install())

BrightspaceURL = "https://nscconline.desire2learn.com/"
#insecure, put in .env
token = "BOT TOKEN"
username = "INSERT EMAIL"
password = "INSERT PASSWORD"
def parser(page):
    page = page.replace('&amp;quot;', '')
    page = page.replace('&quot;', '')
    new = []
    smallerbits = []
    almostfinal = []
    pagelist = page.split('title=\\"')
    for i in range(len(pagelist)):
        smol = pagelist[i].split('\\')
        new.append(smol[0])

    new.pop(0)
    for i in range(len(new)):
        if new[i].startswith("Received") == True:
            new[i] = ""

    for i in range(len(new)):
        if new[i].startswith("Grade") == True:
            new[i] = ""

    for i in range(len(new)):
        if len(new[i]) < 30:
            new[i] = ''
    while("" in new) :
        new.remove("")

    for i in range(len(new)):
        smallerbits.append(new[i].split(", "))
    for i in range(len(smallerbits)):
        for j in range(len(smallerbits[i])):
            if smallerbits[i][j].find(" - ") > 0:
                smallerbits[i][j] = smallerbits[i][j].partition(" - ")[0]
            if smallerbits[i][j].startswith("Received") == True:
                smallerbits[i][j] = ''
                smallerbits[i][j+1] = ''
                smallerbits[i][j+2] = ''
    smallerbits = list(filter(None,[list(filter(None,l)) for l in smallerbits]))
    for i in range(len(smallerbits)):
        almostfinal.append(' '.join(smallerbits[i]))
    del almostfinal[1::2]
    for i in range(len(almostfinal)):
        almostfinal[i] = almostfinal[i].replace("/", " - ")
        almostfinal[i] = almostfinal[i].replace("4349", "")
        almostfinal[i] = almostfinal[i].replace("3451", "")
        almostfinal[i] = almostfinal[i].replace("3320", "")
        almostfinal[i] = almostfinal[i].replace("created", "")
    um = []
    for i in range(len(almostfinal)):
        um.append(almostfinal[i].split(" - "))
        um[i].pop(1)
        um[i].pop(1)
    return um

def login(email, password):
    global driver
    driver.get(BrightspaceURL + 'd2l/home')
    time.sleep(4)
    emailInput = driver.find_element_by_id("i0116")
    emailInput.send_keys(email)
    emailInput.send_keys(Keys.ENTER)
    time.sleep(4)
    passwordInput = driver.find_element_by_id("passwordInput")
    passwordInput.send_keys(password)
    time.sleep(2)
    passwordInput.send_keys(Keys.ENTER)
    time.sleep(3)
    driver.find_element_by_id("idSIButton9").click()

    
def alert():
    global driver
    time.sleep(2)
    while True:
        try:
            driver.get(BrightspaceURL + "d2l/MiniBar/6606/ActivityFeed/GetAlertsDaylight?Category=1")
            print(driver.page_source)
            break
        except:
            pass
    return  driver.page_source
login(username, password)

@client.event
async def on_message(message):
    if "!list" in message.content and len(message.content.split()) == 1: 
        page = alert()
        pagelist = parser(page)
        await message.channel.send(f"{message.author.mention} New Brightspace Events:")
        for i in range(len(pagelist)):
            pagelist[i][1] = pagelist[i][1].replace(" ", "", 1)
            if pagelist[i][1].endswith(" "):
              pagelist[i][1] = pagelist[i][1][:-1] 
            await message.channel.send('>>> ' + '**' + pagelist[i][0] + ': ** ' + pagelist[i][1] + '\n')
client.run(token)
