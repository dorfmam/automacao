from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import psycopg2

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='xxxxxxx', # Utilize sua própria senha do seu banco de dados.
    host='localhost',
    port='5432'    
)

cur = conn.cursor()

cur.execute('SELECT nome, email, idade, telefone FROM "usuarios";')
users = cur.fetchall()

cur.close()
conn.close()

url = 'https://docs.google.com/forms/d/e/1FAIpQLSeA5zkB0F2e78PvFGaMBAjp-HFkIQ8Nw-wulrusp4sTF2IutQ/viewform'
driver.get(url)

time.sleep(3)

for user in users:
    nome, email, idade, telefone = user

    user_name = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/textarea')
    user_email = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    user_age = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    user_phone = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')

    user_name.send_keys(nome)
    user_email.send_keys(email)
    user_age.send_keys(idade)
    user_phone.send_keys(telefone)

    send_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    send_button.click()

    time.sleep(3)
    driver.refresh()

driver.quit()