# -*- coding: utf-8 -*-
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchAttributeException,
    NoSuchElementException,
    ElementNotInteractableException,
    ElementNotVisibleException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchCookieException,
)
from decimal import Decimal, ROUND_DOWN
from datetime import datetime
import pandas as pd
import traceback
import re
import random
import time
import sys
import subprocess
from pynput import keyboard
from personal_data.config import CHROME_PROFILE_PATH, PASSWORD, EMAIL
from IPython.display import display


def run_automation():

    with open("valid_proxies.txt", "r") as f:
        proxies = f.read().split("/n")

        proxy_counter = 0

    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)
    options.add_argument(f"proxy-server={proxies[proxy_counter]}")
    options.add_argument("--lang=en")
    options.add_argument("--debuggerAddress=localhost:9348")
    options.add_argument("--remote-debugging-port=9348")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-logging")
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("detach", True)
    service = ChromeService(ChromeDriverManager().install())
    driver = uc.Chrome(service=service, options=options, enable_cdp_events=True)
    wait = WebDriverWait(driver, timeout=50, poll_frequency=0.1)

    print("abc")

    # ------------------------------global Functions -----------------------------

    def click(driver, locator):
        # driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # element.click()
        max_retries = 25
        retry_count = 0
        while retry_count < max_retries:
            try:
                driver.execute_script(
                    """
                arguments[0].scrollIntoView(true);
                arguments[0].click();
                """,
                    wait.until(EC.presence_of_element_located(locator)),
                )
                break  # Break out of the while loop if the code execution is successful
            except Exception as e:
                # Print the error message
                print(f"Error: {str(e)}retrying...")
                time.sleep(0.20)
                # Increment the retry count
                retry_count += 1

    def send_Keys(driver, locator, value):
        max_retries = 25
        retry_count = 0
        while retry_count < max_retries:
            try:
                element = wait.until(EC.presence_of_element_located(locator))
                driver.execute_script(
                    """
                arguments[0].scrollIntoView(true);
                """,
                    element,
                )
                print(f"send keys: {value}")
                element.send_keys(select_delete)
                element.send_keys(value)

                return element.text  # Return the text of the element

            except Exception as e:
                # Print the error message
                print(f"Error: {str(e)}, retrying...")
                time.sleep(0.20)
                # Increment the retry count
                retry_count += 1

    def getText(driver, locator):
        max_retries = 25
        retry_count = 0
        while retry_count < max_retries:
            try:
                element = wait.until(EC.presence_of_element_located(locator))
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                return element.text  # Return the text of the element
            except Exception as e:
                # Print the error message
                print(f"Error: {str(e)}, retrying...")
                time.sleep(0.2)
                # Increment the retry count
                retry_count += 1

        print("Couldn't get text")
        return None  # Return None if the element is not found after retries

    # def get_random_values(dictionary):
    #     random_driver = random.choice(list(dictionary["Cinco Estrelas"].keys()))
    #     while random_driver == "":
    #         random_driver = random.choice(list(dictionary["Cinco Estrelas"].keys()))
    #     random_plate = dictionary["Cinco Estrelas"][random_driver]
    #     return random_driver, random_plate

    # def ToCommaTo5DigitAfter(toBeConverted: str) -> str:
    #     number = float(toBeConverted)
    #     formatted_number = format(number, '.5f')
    #     integer_part, decimal_part = formatted_number.split('.')
    #     decimal_part = decimal_part.ljust(4, '0')
    #     result = str(integer_part + ',' + decimal_part)
    #     return result

    # def goToFinalPage():

    #     start_time = time.time()
    #     while len(driver.find_elements(By.CLASS_NAME, "paginate_active")) < 1 and time.time() - start_time < 3:
    #         time.sleep(0.5)
    #     click(driver, (By.XPATH, '//*[@id="tbMTRDestinador_last"]'))

    def F10Pressed():
        if driver.switch_to.active_element.send_keys(Keys.F10):
            return "yes"
        else:
            return "no"

    # def getUiStateActiveValue():
    #     time.sleep(0.5)

    #     start_time = time.time()
    #     while len(driver.find_elements(By.CLASS_NAME, "paginate_active")) < 1 and time.time() - start_time < 3:
    #         time.sleep(0.5)
    #     if len(driver.find_elements(By.CLASS_NAME, "paginate_active")) < 1:
    #         goToFinalPage()

    #     ui_state_active_value = int(getText(driver, (By.CLASS_NAME, "paginate_active")))

    #     return ui_state_active_value

    # def changingPageDown():
    #     click(driver, (By.ID, "tbMTRDestinador_previous"))

    # def changingPageUp():
    #     # time.sleep(1)
    #     button_page_up = driver.find_element(
    #         By.XPATH, "/html/body/app-root/app-navegacao/mat-sidenav-container/mat-sidenav-content/app-meus-mtrs/mat-sidenav-container/mat-sidenav-content/mat-card[2]/form/p-table/div/p-paginator/div/a[3]")
    #     driver.execute_script("arguments[0].scrollIntoView(true);", button_page_up)
    #     button_page_up.click()

    # def runningScript():
    #     page_num = 0
    #     while page_num < 15:
    #         page_num += 1
    #         div_num_card_body = 0
    #         while div_num_card_body < 15:
    #             div_num_card_body +=1
    #             received_link_card_body = getText(driver, (By.XPATH, f'//*[@id="serp-results"]/div[{div_num_card_body}]/div/h3/a'))
    #             print(received_link_card_body)

    #         click(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[4]/ul/li[14]/a/span[1]'))
    #         # click(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[4]/ul/li[14]/a'))

    def runningScript():

        # check if register page is gonna appear
        while (
            len(
                driver.find_elements(
                    By.XPATH,
                    '//*[@id="offcanvasBottom"]/div',
                )
            )
            < 1
        ):
            time_elapsed = 0
            while time_elapsed < 3:
                time_elapsed += 1
                time.sleep(random.uniform(0.5, 1))
                break
        else:
            print("logging in")
            time.sleep(random.uniform(0.5, 1))
            click(
                driver, (By.XPATH, '//*[@id="offcanvasBottom"]/div/div/ul/li/a')
            )  # click on google login
            time.sleep(random.uniform(0.5, 1))
            send_Keys(
                driver, (By.XPATH, '//*[@id="identifierId"]'), EMAIL
            )  # type email in email field
            time.sleep(random.uniform(0.5, 1))
            click(
                driver, (By.XPATH, '//*[@id="identifierNext"]/div/button/div[3]')
            )  # click on next after email
            time.sleep(random.uniform(0.5, 1))
            send_Keys(
                driver,
                (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'),
                PASSWORD,
            )  # type passowrd in password field
            time.sleep(random.uniform(0.5, 1))
            click(
                driver, (By.XPATH, '//*[@id="passwordNext"]/div/button/div[3]')
            )  # click on next after password
            time.sleep(random.uniform(0.5, 1))
            driver.get(
                "https://www.registrorural.com.br/search?q=latlng5km:-20.417733154196874,-40.35314798355103&page=2"
            )

        time.sleep(random.uniform(0.5, 1))
        print("click on next tab")
        click(
            driver, (By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[4]/ul/li[14]/a")
        )  # Clicar em próxima aba da lista

        # //*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button/div[3] #XPATH do click em continue permissao do google pro site

        # //*[@id="user_profile_type_12"] #XPATH do conte mais sobre voce pop up - clickar em estudante
        # //*[@id="modalUserProfileType"]/div/div/div[3]/button[1] #XPATH do conte mais sobre voce pop up - clickar em salvar
        # //*[@id="modalUserProfileType"]/div/div/div[3]/button #XPATH do conte mais sobre voce pop up - clickar em fechar

    #     # time.sleep(1)
    #     for mtr_number in mtr_scans_dict.keys():
    #         # Do something with the mtr_number variable
    #         print(mtr_number)
    #         # random driver and random plate
    #         random_driver, random_plate = get_random_values(drivers_dict_dict)
    #         # time.sleep(1)
    #         send_Keys(driver, (By.XPATH, '//*[@id="txtCodigoMtrRecebimento"]'), mtr_number)
    #         click(driver, (By.XPATH, '//*[@id="btnReceberMtr"]'))
    #         while len(driver.find_elements(By.XPATH, "//font[@color='#B22222'][.//*[text()='Você não pode receber este MTR!']]")) < 1 and len(driver.find_elements(By.ID, "txtTransportadorNomeMotorista")) < 1:
    #             time.sleep(0.5)
    #         print("mtr window open:")
    #         print(len(driver.find_elements(By.ID, "txtTransportadorNomeMotorista")))
    #         print("window to close:")
    #         print(len(driver.find_elements(By.XPATH, '/html/body/div[19]/div[2]/font')))
    #         # time.sleep(1)
    #         if len(driver.find_elements(By.XPATH, "//font[@color='#B22222'][.//*[text()='Você não pode receber este MTR!']]")) < 1 and len(driver.find_elements(By.ID, "txtTransportadorNomeMotorista")) >= 1:
    #             print(f"Receiving - Nº {mtr_number} - \N{CHECK MARK}")
    #             # procurando por responsavel aloisio visivel (se já foi escolhido na sessão)
    #             if len(driver.find_elements(By.XPATH, '//*[@id="ui-id-14"]')) < 1:
    #                 click(driver,
    #                     (By.XPATH, '//*[@id="formRespRecebimento"]/fieldset[1]/table/tbody/tr/td[1]/a'))

    #                 # simbolo de confirmar ação de cargo
    #                 click(driver,
    #                     (By.XPATH,  '//*[@id="tabelaResRecebimento"]/tbody/tr/td[2]'))

    #             print("after aloisio")

    #             # Data de recebimento
    #             print("before date putting")
    #             click(driver,
    #                 (By.XPATH, '//*[@id="formRespRecebimento"]/table[1]/tbody/tr[2]/td[2]/img'))

    #             month_received = getText(driver, (By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/span[1]'))
    #             print(month_received)
    #             print(received_month)

    #             print(f"month_received: {month_received} received_month: {received_month}")
    #             while month_received != received_month:
    #                 print(f"month_received: {month_received} - received_month: {received_month}")
    #                 time.sleep(0.5)
    #                 driver.find_element(
    #                     By.XPATH, '//*[@id="ui-datepicker-div"]/div/a[1]/span').click()
    #                 time.sleep(0.5)
    #                 month_received = getText(driver, (By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/span[1]'))

    #             day_received_element = driver.find_elements(
    #                 By.CSS_SELECTOR, '[data-handler="selectDay"]')  # menu dias recebendo

    #             for element in day_received_element:  # menu dias recebendo
    #                 text_day_received = element.text
    #                 print(f"text_day_received: {text_day_received} - received_day: {received_day}")
    #                 if text_day_received == received_day:
    #                     element.click()
    #                     break
    #                 else:
    #                     pass

    #                 print("loop finished")
    #             print("after date putting")

    #             transportador_motorista = driver.find_element(
    #                 By.ID, "txtTransportadorNomeMotorista")  # Motorista
    #             transportador_motorista_value = transportador_motorista.get_attribute(
    #                 "value")          # Motorista
    #             if transportador_motorista_value == "":                                                 # Motorista
    #                 driver.find_element(By.ID, "txtTransportadorNomeMotorista").send_keys(
    #                     random_driver)  # Motorista
    #             transportador_placa = driver.find_element(
    #                 By.ID, "txtTransportadorPlacaVeiculo")  # Placa
    #             transportador_placa_value = transportador_placa.get_attribute(
    #                 "value")            # Placa
    #             if transportador_placa_value == "":                                           # Placa
    #                 driver.find_element(
    #                     By.ID, "txtTransportadorPlacaVeiculo").send_keys(random_plate)  # Placa

    #             tons_received = mtr_tons_dict[mtr_number]
    #             print(tons_received)

    #             tons_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[value='0,00000']")))

    #             tons_field.send_keys(tons_received)  # Toneladas recebidas

    #             time.sleep(0.5)

    #             actions = ActionChains(driver)
    #             actions.send_keys(Keys.TAB).perform()
    #             actions.send_keys(Keys.TAB).perform()
    #             actions.send_keys(Keys.TAB).perform()
    #             actions.send_keys(Keys.ENTER).perform() # Receber Finalizar

    #             close_received = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[13]/div[1]/button'))) # fechar janela recebido

    #             close_received.click() # fechar janela recebido
    #             print(f"Received - Nº {mtr_number} - \N{CHECK MARK}")

    #         elif len(driver.find_elements(By.XPATH, "//font[@color='#B22222'][.//*[text()='Você não pode receber este MTR!']]")) >= 1 and len(driver.find_elements(By.ID, "txtTransportadorNomeMotorista")) < 1:
    #             time.sleep(2)
    #             # time.sleep(1)
    #             while len(driver.find_elements(By.XPATH, '/html/body/div[19]/div[1]/button')) < 1:
    #                 print("MTR recebido anteriormente")
    #                 print(len(driver.find_elements(By.XPATH, '/html/body/div[19]/div[1]/button')))
    #                 time.sleep(0.5)
    #             click(driver, (By.XPATH, '/html/body/div[19]/div[1]/button'))
    #             click(driver, (By.XPATH, '/html/body/div[19]/div[1]/button'))

    #             time.sleep(0.5)

    #             # actions = ActionChains(driver)
    #             # close_button = driver.find_element(By.XPATH, '/html/body/div[19]')
    #             # actions.move_to_element
    #             # actions.send_keys(Keys.RETURN).perform()
    #             print("waiting for button to close")
    #             # time.sleep(5)

    # def convert_path(path):
    #     converted_path = path.replace("/", r"\\")
    #     return converted_path

    # def login():
    #     driver.find_element(By.ID, "txtCnpj").send_keys("04737150000133")
    #     time.sleep(2)
    #     driver.find_element(By.ID, "txtCnpj").send_keys(Keys.TAB)
    #     time.sleep(1)
    #     driver.find_element(By.ID, "txtCpfUsuario").send_keys("56073623704")
    #     time.sleep(1)
    #     driver.find_element(By.ID, "txtSenha").send_keys(IEMA_PASSWORD)
    #     driver.find_element(By.ID, "txtSenha").send_keys(Keys.TAB)
    #     driver.find_element(By.ID, "btEntrar").send_keys(Keys.ENTER)

    # -------------------------------- send_keys ---------------------------------

    select_delete = Keys.CONTROL + "a", Keys.DELETE
    select = Keys.CONTROL + "a"
    select_copy = Keys.CONTROL + "a", Keys.CONTROL + "c"
    copy = Keys.CONTROL + "c"
    paste = Keys.CONTROL + "v"

    # -------------------------------- send_keys ---------------------------------

    print("opening browser")
    # getting to page, maximizing window
    time.sleep(1)
    driver.get(
        "https://www.registrorural.com.br/search?q=latlng5km:-20.417733154196874,-40.35314798355103&page=2"
    )
    driver.maximize_window()

    time.sleep(2)

    # Informações
    print("browser opened")
    try:
        while F10Pressed() != "yes":
            time.sleep(1)
            while True:
                print("runningScript")
                runningScript()

    except (
        Exception,
        NoSuchAttributeException,
        NoSuchElementException,
        ElementNotInteractableException,
        ElementNotVisibleException,
        StaleElementReferenceException,
        ElementClickInterceptedException,
        NoSuchCookieException,
    ):
        traceback.print_exc()
        time.sleep(100)
        driver.get("https://www.youtube.com/watch?v=HrGjqPhzErs")
        time.sleep(20)

    print("code ended")
