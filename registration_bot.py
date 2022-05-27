from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from zoneinfo import ZoneInfo
import time


def script(username, password, times):
    try:
        # go to iroar
        PATH = 'geckodriver.exe'
        driver = webdriver.Firefox(service=Service(PATH))
        driver.get('https://iroar.app.clemson.edu/dashboard/index.php')
        wait = WebDriverWait(driver, 7)


        # submit info
        user_form = driver.find_element(By.ID, 'username')
        pass_form = driver.find_element(By.ID, 'password')
        user_form.send_keys(username)
        pass_form.send_keys(password)
        pass_form.send_keys(Keys.ENTER)

        # validate info
        try:
            wait.until(EC.presence_of_element_located((By.ID, 'auth_methods')))
        except Exception as e:
            raise Exception('incorrect username and/or password')

        time.sleep(2)

        # wait for authentication
        WebDriverWait(driver, 60).until(EC.invisibility_of_element((By.ID, 'auth_methods')))

        # go to registration home page
        driver.get('https://regssb.sis.clemson.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=registration')

        # waits for loading animation
        def wait_to_load():
            wait.until(EC.invisibility_of_element((By.ID, 'splash')))
            wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'loading')))

        # clicks after waiting
        def click_after_load(by, value):
            temp = wait.until(EC.element_to_be_clickable((by, value)))
            wait_to_load()
            temp.click()

        # click register class link
        click_after_load(By.ID, 'registerLink')
        click_after_load(By.ID, 's2id_txt_term')

        # select newest semester
        select_results = driver.find_element(By.ID, 'select2-results-1')
        wait_to_load()
        select_results.find_element(By.TAG_NAME, 'li').click()

        # set start time
        hour, minute = times
        current_day = datetime.now(tz=ZoneInfo('America/New_York'))
        task_date = datetime(current_day.year, current_day.month, current_day.day, hour, minute,
                             tzinfo=ZoneInfo('America/New_York'))

        def quick_register():
            click_after_load(By.ID, 'term-go')
            click_after_load(By.ID, 'loadPlans-tab')
            click_after_load(By.XPATH, '//*[contains(text(), \'Add All\')]')
            click_after_load(By.ID, 'saveButton')

        # set up scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(quick_register, 'date', run_date=task_date)

        if task_date < current_day:
            raise Exception('Start Time has already passed')

        # start task
        scheduler.start()

        # wait until user closes window
        while True:
            try:
                _ = driver.window_handles
            except BaseException as e:
                break
            time.sleep(10)

    finally:
        print('script exited')
        driver.quit()
