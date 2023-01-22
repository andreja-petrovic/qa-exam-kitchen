import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

ORGANIZER = 'Gordon Ramsay'
BDAY_PERSON = 'Harley Morenstein'
AGE = '1985'
DATE = '2023-01-01'
TIME = '16:30'
PERSONS = '21+'
ALLERGIES = 'Yes'
ALRG_TYPES = 'Wallnuts,Shrimp'


def test_zadatak_1_forma():
    driver = webdriver.Chrome()
    driver.get('http://10.15.1.204:3000/reserve')

    organizer = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,'input[class="form-control org"]')))

    organizer.send_keys(ORGANIZER)
    organizer.send_keys(Keys.ENTER)

    storage_org = driver.execute_script(f'return localStorage.getItem("Organizer")')
    assert storage_org == ORGANIZER

    birthday_person = driver.find_element(By.CSS_SELECTOR, 'input[class="form-control bp"]')
    birthday_person.send_keys(BDAY_PERSON)
    birthday_person.send_keys(Keys.ENTER)

    storage_bp = driver.execute_script(f'return localStorage.getItem("Birthday_Person")')
    assert storage_bp == BDAY_PERSON

    age = driver.find_element(By.CSS_SELECTOR, '#age')
    age.send_keys(AGE)
    age.send_keys(Keys.ENTER)

    storage_age = driver.execute_script(f'return localStorage.getItem("Age")')
    assert storage_age == AGE

    date = driver.find_element(By.CSS_SELECTOR, '#date')
    date.send_keys(Keys.UP)
    date.send_keys(Keys.RIGHT)
    date.send_keys(Keys.UP)
    date.send_keys(Keys.RIGHT)
    date.send_keys(Keys.UP)

    storage_date = driver.execute_script(f'return localStorage.getItem("Date")')
    assert storage_date == DATE

    time_of = driver.find_element(By.CSS_SELECTOR, '#time')
    time_of.send_keys(TIME)
    time_of.send_keys(Keys.ENTER)

    storage_time = driver.execute_script(f'return localStorage.getItem("Time")')
    assert storage_time == TIME

    guests = driver.find_element(By.CSS_SELECTOR, 'option[value="4"]')
    guests.click()

    storage_pers = driver.execute_script(f'return localStorage.getItem("Number_Of_People")')
    assert storage_pers == PERSONS

    allergies = driver.find_element(By.CSS_SELECTOR, f'input[value="{ALLERGIES}"]')
    allergies.click()

    if ALLERGIES == 'Yes' or ALLERGIES == 'Maybe':
        allergies_walnuts = driver.find_element(By.CSS_SELECTOR, 'input[value="Wallnuts"]')
        allergies_walnuts.click()
        allergy_shrimp = driver.find_element(By.CSS_SELECTOR, 'input[value="Shrimp"]')
        allergy_shrimp.click()

        storage_allergies = driver.execute_script(f'return localStorage.getItem("alergies")')
        assert storage_allergies == ALRG_TYPES

    storage_allergies = driver.execute_script(f'return localStorage.getItem("alergy")')
    assert storage_allergies == ALLERGIES

    organize_button = driver.find_element(By.CSS_SELECTOR, 'a[class="btn btn-primary px-5 py-3"]')
    organize_button.click()

    celebrant_modal = driver.find_element(By.CSS_SELECTOR, '#cbr')
    organizer_modal = driver.find_element(By.CSS_SELECTOR, '#orr')
    age_modal = driver.find_element(By.CSS_SELECTOR, '#agr')
    date_modal = driver.find_element(By.CSS_SELECTOR, '#dtr')
    time_of_modal = driver.find_element(By.CSS_SELECTOR, '#tmr')
    guests_modal = driver.find_element(By.CSS_SELECTOR, '#gur')
    allergies_modal = driver.find_element(By.CSS_SELECTOR, '#alr')

    ### Na modalu se ne prikazuje tip alergija, samo se vidi da li postoje ili ne (Yes, No, Maybe)
    assert celebrant_modal.text == BDAY_PERSON
    assert organizer_modal.text == ORGANIZER
    assert age_modal.text == AGE
    assert date_modal.text == DATE
    assert time_of_modal.text == TIME
    assert guests_modal.text == PERSONS
    assert allergies_modal.text == ALLERGIES

    driver.quit()


def test_zadatak_2_preporuka():
    driver = webdriver.Chrome()
    driver.get('http://10.15.1.204:3000/questionaire')

    answer_id = 1
    text_id = 1
    list_of_left_answers = ['Leto', 'Caj', 'Belo', 'Slatko', 'Kiselo', 'Kasika', 'Duboki', 'Voce', 'Koktel']
    list_of_right_answers = ['Zima', 'Kafa', 'Crno', 'Slano', 'Ljuto', 'Viljuska', 'Plitki', 'Povrce', 'Pivo']

    while answer_id < 18:   # klikce na sve leve odgovore
        answer_button = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, f'#btn{answer_id}')))
        time.sleep(0.5)
        answer_button.click()
        answer_id = answer_id + 2

    for answer_left in list_of_left_answers:    # proverava da li su se pojavili svi levi odgovori iz liste
        answer_text = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, f'.resultText{text_id}')))
        assert answer_text.text == answer_left
        text_id = text_id + 1

    driver.refresh()

    answer_id = 2
    text_id = 1

    while answer_id < 20: # klikce na sve desne odgovore
        answer_button = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, f'#btn{answer_id}')))
        time.sleep(0.5)
        answer_button.click()
        answer_id = answer_id + 2

    for answer_right in list_of_right_answers:  # proverava da li su se pojavili svi desni odgovori iz liste
        answer_text = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, f'.resultText{text_id}')))
        assert answer_text.text == answer_right
        text_id = text_id + 1

    driver.refresh()

    ## Za svaku grupu score-a (0-1, 2-3, 4-5, 6-7, 8-9) proveri da li se dobija odgovarajuce jelo

    ################# SCORE 0 and 1 #################

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Avocado Benedict'

    driver.refresh()

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    answer_button = driver.find_element(By.CSS_SELECTOR, '#btn1')
    answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Avocado Benedict'

    driver.refresh()

    ################# SCORE 2 and 3 #################

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    for i in range(1, 4, 2):
        answer_button = driver.find_element(By.CSS_SELECTOR, f'#btn{i}')
        time.sleep(0.5)
        answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Strawberry Sundae'

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    driver.refresh()

    for i in range(1, 6, 2):
        answer_button = driver.find_element(By.CSS_SELECTOR, f'#btn{i}')
        time.sleep(0.5)
        answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Strawberry Sundae'

    driver.refresh()

    ################# SCORE 4 and 5 #################

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    for i in range(1, 8, 2):
        answer_button = driver.find_element(By.CSS_SELECTOR, f'#btn{i}')
        time.sleep(0.5)
        answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Soy Salmon'

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    driver.refresh()

    for i in range(1, 10, 2):
        answer_button = driver.find_element(By.CSS_SELECTOR, f'#btn{i}')
        time.sleep(0.5)
        answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Soy Salmon'

    driver.refresh()

    ################# SCORE 6 and 7 #################

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    for i in range(1, 12, 2):
        answer_button = driver.find_element(By.CSS_SELECTOR, f'#btn{i}')
        time.sleep(0.5)
        answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Culiflower Dipper'

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    driver.refresh()

    for i in range(1, 14, 2):
        answer_button = driver.find_element(By.CSS_SELECTOR, f'#btn{i}')
        time.sleep(0.5)
        answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Culiflower Dipper'

    driver.refresh()

    ################# SCORE 8 and 9 #################

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    for i in range(1, 16, 2):
        answer_button = driver.find_element(By.CSS_SELECTOR, f'#btn{i}')
        time.sleep(0.5)
        answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Blonde'

    top = driver.find_element(By.CSS_SELECTOR, '.overlay')
    driver.execute_script("arguments[0].scrollIntoView();", top)

    driver.refresh()

    for i in range(1, 18, 2):
        answer_button = driver.find_element(By.CSS_SELECTOR, f'#btn{i}')
        time.sleep(0.5)
        answer_button.click()

    read_my_mind = driver.find_element(By.CSS_SELECTOR, '#readmymind')
    driver.execute_script("arguments[0].scrollIntoView();", read_my_mind)
    read_my_mind.click()

    recommendation = WebDriverWait(driver, 5).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#recHeader')))
    assert recommendation.text == 'Blonde'

    driver.quit()


def test_zadatak_3_meni_i_korpa():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://10.15.1.204:3000/menu')

    random_list = [random.randrange(0, 6) for i in range(6)]    # krira niz od 6 nasumicnih brojeva sa ponavljanjem

    for i in random_list:   # klikce na 6 jela sa rednim brojem koji dobija iz niza
        scroll = driver.find_element(By.XPATH, '/html/body/section[2]/div/div[2]/div[2]/div[1]/h3')
        driver.execute_script("arguments[0].scrollIntoView();", scroll)
        add_food = driver.find_elements(By.CSS_SELECTOR, 'button[class="btn btn-primary btnPlus"]')[i]
        time.sleep(3)
        add_food.click()

    time.sleep(3)

    price_list = []     # nalazi i sabira cene svih izabranih jela i poredi sa ukupnom cenom u korpi
    for i in random_list:
        price_filed = driver.find_elements(By.CSS_SELECTOR, '.price')[i]
        price = int(price_filed.text[1:])
        price_list.append(price)

    total_price_list = sum(price_list)
    total_cart = driver.find_elements(By.CSS_SELECTOR, '#ukupno')

    assert total_price_list == int(total_cart[0].text)

    driver.quit()
