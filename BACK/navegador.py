from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def abre_navegador():

    try:

        driver = webdriver.Chrome()

        driver.maximize_window()

        return driver

    except WebDriverException as e:

        print(f"❌ Erro ao abrir o Google Chrome: {e}")

        return None


def acessar_pagina(driver, url):

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:

        driver.get(url)

        return True

    except WebDriverException:

        print(f"❌ Erro de conexão ao carregar " f"a página '{url}'.")

        return False


def recarregar_pagina(driver):

    try:

        driver.refresh()

    except WebDriverException:

        print("⚠️ Aviso: Falha ao tentar " "recarregar a página.")
