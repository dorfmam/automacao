from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import InvalidArgumentException
import os
import time
import logging
import psycopg2

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
window = driver.maximize_window()

conn = None

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    
    cur = conn.cursor()

    cur.execute("""
        SELECT name, email, age, phone FROM employees;
    """)


    cur.execute("""
        INSERT INTO employees (name, email, age, phone)
        VALUES
            ("John Doe", "johndoe@example.com", 30, "555-123-4567"),
            ("Jane Smith", "janesmith@example.com", 28, "555-987-6543"),
            ("Alice Johnson", "alicej@example.com", 35, "555-246-8109"),
            ("Bob Brown", "bobb@example.com", 40, "555-369-1470"),
            ("Charlie Davis", "charlied@example.com", 25, "555-852-9631"),
            ("Daniel Evans", "danielev@example.com", 32, "555-741-2580"),
            ("Eva Green", "evag@example.com", 29, "555-159-3572"),
            ("Frank Harris", "frankh@example.com", 45, "555-753-9514"),
            ("Grace White", "gracew@example.com", 27, "555-321-6789"),
            ("Henry Moore", "henrym@example.com", 38, "555-654-3210"),
            ("Ivy King", "ivyk@example.com", 33, "555-908-1726"),
            ("Jack Lee", "jackl@example.com", 26, "555-135-7924"),
            ("Kara Scott", "karas@example.com", 31, "555-284-6375"),
            ("Leo Carter", "leoc@example.com", 36, "555-777-8888"),
            ("Mia Adams", "miaa@example.com", 22, "555-909-1122"),
            ("Nathan Baker", "nathanb@example.com", 34, "555-600-4321"),
            ("Olivia Hall", "oliviah@example.com", 30, "555-333-2221"),
            ("Peter Allen", "petera@example.com", 37, "555-800-9000"),
            ("Quinn Turner", "quinnt@example.com", 29, "555-412-7856"),
            ("Ryan Phillips", "ryanp@example.com", 41, "555-626-4848");
    """)

    conn.commit()

    cur.execute("SELECT name, email, age, phone FROM employees;")
    users = cur.fetchall()

except psycopg2.OperationalError as error:
    logging.error("Erro ao tentar conectar com o PostgreSQL")
    raise

finally:
    if conn:
        conn.close()

try:
    url = "http://localhost:3000"
    driver.get(url)
except InvalidArgumentException as error:
    print("Não foi possível acessar a página. Verifique se o servidor está ativo")

time.sleep(3)

for user in users:
    name, email, age, phone = user

    user_name = driver.find_element(By.ID, "nome")
    user_email = driver.find_element(By.ID, "email")
    user_age = driver.find_element(By.ID, "idade")
    user_phone = driver.find_element(By.ID, "telefone")

    user_name.send_keys(name)
    time.sleep(1)
    user_email.send_keys(email)
    time.sleep(1)
    user_age.send_keys(age)
    time.sleep(1)
    user_phone.send_keys(phone)
    time.sleep(1)

    send_button = driver.find_element(By.ID, "enviar")
    send_button.click()
    
    time.sleep(3)
    driver.get(url)

driver.quit()