from django.test import TestCase, Client, LiveServerTestCase
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.conf import settings
from selenium import webdriver
from datetime import datetime
import json
import logging
import time
import os
import subprocess


class AdicionarCulturaTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    def teste_adicionarCultura(self):
        driver = self.driver

        driver.get("http://localhost:8000/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_junta_se")))
        btn_junta_se = driver.find_element(By.NAME, "btn_junta_se")
        time.sleep(1)
        btn_junta_se.click()
        time.sleep(1)

        driver.get("http://localhost:8000/accounts/signup/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email-usuario")))
        email_registro = driver.find_element(By.ID, "email-usuario")
        senha1 = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        btn_registrar = driver.find_element(By.NAME, "btn_registar")

        email_registro.send_keys("userteste@gmail.com")
        senha1.send_keys("@MinhasenhaForte1234")
        senha2.send_keys("@MinhasenhaForte1234")
        time.sleep(2)
        btn_registrar.send_keys(Keys.ENTER)
        time.sleep(1)

        driver.get("http://localhost:8000/accounts/signin/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_email")))
        email_login = driver.find_element(By.ID, "id_email")
        senhalogin = driver.find_element(By.ID, "id_password")
        btn_logar = driver.find_element(By.NAME, "btn_logar")

        email_login.send_keys("userteste@gmail.com")
        senhalogin.send_keys("@MinhasenhaForte1234")
        time.sleep(1)
        btn_logar.send_keys(Keys.ENTER)
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_addEvento")))
        btn_addEvento = driver.find_element(By.NAME, "btn_addEvento")
        btn_addEvento.click()

        time.sleep(3)

        nomeEvento_cultura = driver.find_element(By.ID, "id_title")
        tipo_cultura = Select(driver.find_element(By.ID, "id_type"))
        cultura_cultura = Select(driver.find_element(By.ID, "id_cultura"))
        local_cultura = driver.find_element(By.ID, "id_local")
        descricao_cultura = driver.find_element(By.ID, "id_description")
        dataInicio_cultura = driver.find_element(By.ID, "id_start_time")
        dataFim_cultura = driver.find_element(By.ID, "id_end_time")
        salvar_btn = driver.find_element(By.CSS_SELECTOR, ".save-btn")

        print("Passo 1: Tentando salvar sem preencher nenhum campo.")
        salvar_btn.click()
        time.sleep(2)

        print("Passo 2: Preenchendo apenas o título e tentando salvar.")
        nomeEvento_cultura.send_keys("Nome teste para a cultura")
        time.sleep(1)
        salvar_btn.click()
        time.sleep(2)

        print("Passo 3: Preenchendo título e tipo, e tentando salvar.")
        tipo_cultura.select_by_visible_text("Preparo")
        time.sleep(1)
        salvar_btn.click()
        time.sleep(2)

        print("Passo 4: Preenchendo título, tipo e cultura, e tentando salvar.")
        cultura_cultura.select_by_visible_text("Alface")
        time.sleep(1)
        salvar_btn.click()
        time.sleep(2)

        print("Passo 5: Preenchendo o local e tentando salvar.")
        local_cultura.send_keys("Lote 08H3 - linha 4")
        time.sleep(1)
        salvar_btn.click()
        time.sleep(2)

        print("Passo 6: Preenchendo a descrição e tentando salvar.")
        descricao_cultura.send_keys("Texto teste para descrição da cultura teste.")
        time.sleep(1)
        salvar_btn.click()
        time.sleep(2)

        print("Passo 7: Preenchendo as datas e horas e tentando salvar.")
        dataInicio_cultura.clear()
        dataInicio_cultura.send_keys("28/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("10:00")
        time.sleep(1)

        dataFim_cultura.clear()
        dataFim_cultura.send_keys("30/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("16:00")
        time.sleep(1)

        print("Finalizado o passo a passo de preenchimento incremental.")
        salvar_btn.click()
        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        btn_gerenciarCultura.click()
        time.sleep(3)
        assert "Nome teste para a cultura" in driver.page_source

        time.sleep(3)


class SugerirColheitaTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    def teste_sugerirColheita(self):
        driver = self.driver

        driver.get("http://localhost:8000/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_junta_se")))
        btn_junta_se = driver.find_element(By.NAME, "btn_junta_se")
        time.sleep(1)
        btn_junta_se.click()
        time.sleep(1)

        driver.get("http://localhost:8000/accounts/signup/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email-usuario")))
        email_registro = driver.find_element(By.ID, "email-usuario")
        senha1 = driver.find_element(By.NAME, "password1")
        senha2 = driver.find_element(By.NAME, "password2")
        btn_registrar = driver.find_element(By.NAME, "btn_registar")

        email_registro.send_keys("userteste@gmail.com")
        senha1.send_keys("@MinhasenhaForte1234")
        senha2.send_keys("@MinhasenhaForte1234")
        time.sleep(2)
        btn_registrar.send_keys(Keys.ENTER)
        time.sleep(1)

        driver.get("http://localhost:8000/accounts/signin/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_email")))
        email_login = driver.find_element(By.ID, "id_email")
        senhalogin = driver.find_element(By.ID, "id_password")
        btn_logar = driver.find_element(By.NAME, "btn_logar")

        email_login.send_keys("userteste@gmail.com")
        senhalogin.send_keys("@MinhasenhaForte1234")
        time.sleep(1)
        btn_logar.send_keys(Keys.ENTER)
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_addEvento")))
        btn_addEvento = driver.find_element(By.NAME, "btn_addEvento")
        btn_addEvento.click()

        time.sleep(3)

        nomeEvento_cultura = driver.find_element(By.ID, "id_title")
        tipo_cultura = Select(driver.find_element(By.ID, "id_type"))
        cultura_cultura = Select(driver.find_element(By.ID, "id_cultura"))
        local_cultura = driver.find_element(By.ID, "id_local")
        descricao_cultura = driver.find_element(By.ID, "id_description")
        dataInicio_cultura = driver.find_element(By.ID, "id_start_time")
        dataFim_cultura = driver.find_element(By.ID, "id_end_time")
        salvar_btn = driver.find_element(By.CSS_SELECTOR, ".save-btn")

        nomeEvento_cultura.send_keys("Teste para sugestão de colheita - Alface")
        time.sleep(1)
        tipo_cultura.select_by_visible_text("Plantio")
        time.sleep(1)
        cultura_cultura.select_by_visible_text("Alface")
        time.sleep(1)
        local_cultura.send_keys("Lote 0001 - linha 44")
        time.sleep(1)
        descricao_cultura.send_keys("Descrição teste para o plantil de alface")
        time.sleep(1)
        dataInicio_cultura.send_keys("28/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("10:00")
        time.sleep(1)
        dataFim_cultura.send_keys("30/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("16:00")
        time.sleep(1)

        salvar_btn.click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "acceptSuggestion")))
        btn_aceitarsugest = driver.find_element(By.ID, "acceptSuggestion")
        btn_aceitarsugest.click()
        time.sleep(5)  

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        btn_gerenciarCultura.click()
        time.sleep(3)
        assert "Teste para sugestão de colheita - Alface" in driver.page_source
        assert "Teste para sugestão de colheita - Alface - Colheita" in driver.page_source

        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-next-button")))
        btn_proxMes = driver.find_element(By.CSS_SELECTOR, ".fc-next-button")
        for i in range(2):
            btn_proxMes.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_addEvento")))
        btn_addEvento = driver.find_element(By.NAME, "btn_addEvento")
        btn_addEvento.click()

        time.sleep(3)

        nomeEvento_cultura = driver.find_element(By.ID, "id_title")
        tipo_cultura = Select(driver.find_element(By.ID, "id_type"))
        cultura_cultura = Select(driver.find_element(By.ID, "id_cultura"))
        local_cultura = driver.find_element(By.ID, "id_local")
        descricao_cultura = driver.find_element(By.ID, "id_description")
        dataInicio_cultura = driver.find_element(By.ID, "id_start_time")
        dataFim_cultura = driver.find_element(By.ID, "id_end_time")
        salvar_btn = driver.find_element(By.CSS_SELECTOR, ".save-btn")

        nomeEvento_cultura.send_keys("Teste para sugestão de colheita - Tomate")
        time.sleep(1)
        tipo_cultura.select_by_visible_text("Plantio")
        time.sleep(1)
        cultura_cultura.select_by_visible_text("Tomate")
        time.sleep(1)
        local_cultura.send_keys("Lote 0002 - linha 20")
        time.sleep(1)
        descricao_cultura.send_keys("Descrição teste para o plantil de Tomate")
        time.sleep(1)
        dataInicio_cultura.send_keys("26/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("08:00")
        time.sleep(1)
        dataFim_cultura.send_keys("29/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("10:00")
        time.sleep(1)
    
        salvar_btn.click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "acceptSuggestion")))
        btn_aceitarsugest = driver.find_element(By.ID, "acceptSuggestion")
        btn_aceitarsugest.click()
        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        btn_gerenciarCultura.click()
        time.sleep(3)
        assert "Teste para sugestão de colheita - Tomate" in driver.page_source
        assert "Teste para sugestão de colheita - Tomate - Colheita" in driver.page_source
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-next-button")))
        btn_proxMes = driver.find_element(By.CSS_SELECTOR, ".fc-next-button")
        for i in range(4):
            btn_proxMes.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)