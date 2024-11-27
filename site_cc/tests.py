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
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
from unittest.mock import patch
from site_cc.views import calendar_view_new


class AdicionarCulturaTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
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
        time.sleep(6)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)


class SugerirColheitaTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
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
        driver.execute_script("arguments[0].click();", btn_aceitarsugest)
        time.sleep(5)  

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)

        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-next-button")))
        btn_proxMes = driver.find_element(By.CSS_SELECTOR, ".fc-next-button")
        for i in range(2):
            driver.execute_script("arguments[0].click();", btn_proxMes)
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
        driver.execute_script("arguments[0].click();", btn_aceitarsugest)
        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-next-button")))
        btn_proxMes = driver.find_element(By.CSS_SELECTOR, ".fc-next-button")
        for i in range(4):
            driver.execute_script("arguments[0].click();", btn_proxMes)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)


class EditarCulturaTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    def testeEditarCultura(self):
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

        nomeEvento_cultura.send_keys("Teste para editar cultura")
        time.sleep(1)
        tipo_cultura.select_by_visible_text("Preparo")
        time.sleep(1)
        cultura_cultura.select_by_visible_text("Rúcula")
        time.sleep(1)
        local_cultura.send_keys("Lote 222 - linha 10")
        time.sleep(1)
        descricao_cultura.send_keys("Descrição teste para o plantio de Rúcula ")
        time.sleep(1)
        dataInicio_cultura.send_keys("25/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("10:00")
        time.sleep(1)
        dataFim_cultura.send_keys("27/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("12:00")
        time.sleep(1)

        salvar_btn.click()
        time.sleep(6)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-daygrid-event")))
        cultura_excluida = driver.find_element(By.CSS_SELECTOR, ".fc-daygrid-event")
        cultura_excluida.click()

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "edit-event-button")))
        btn_editarCultura = driver.find_element(By.ID, "edit-event-button")
        btn_editarCultura.click()

        nomeEvento_culturaEditar = driver.find_element(By.ID, "id_title")
        salvar_btn = driver.find_element(By.CSS_SELECTOR, ".save-btn")

        time.sleep(2)
        nomeEvento_culturaEditar.clear()
        time.sleep(1)
        nomeEvento_culturaEditar.send_keys("Novo nome para o evento")
        time.sleep(2)

        salvar_btn.click()
        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-daygrid-event")))
        cultura_excluida = driver.find_element(By.CSS_SELECTOR, ".fc-daygrid-event")
        cultura_excluida.click()

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "edit-event-button")))
        btn_editarCultura = driver.find_element(By.ID, "edit-event-button")
        btn_editarCultura.click()

        cultura_cultura = Select(driver.find_element(By.ID, "id_cultura"))
        local_cultura = driver.find_element(By.ID, "id_local")
        dataInicio_cultura = driver.find_element(By.ID, "id_start_time")
        dataFim_cultura = driver.find_element(By.ID, "id_end_time")
        salvar_btn = driver.find_element(By.CSS_SELECTOR, ".save-btn")

        time.sleep(2)
        cultura_cultura.select_by_visible_text("Tomate")
        time.sleep(2)
        local_cultura.clear()
        local_cultura.send_keys("Novo lugar")
        time.sleep(2)
        dataInicio_cultura.clear()
        dataFim_cultura.clear()
        dataInicio_cultura.send_keys("29/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("10:00")
        time.sleep(1)
        dataFim_cultura.send_keys("30/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("12:00")
        time.sleep(1)

        salvar_btn.click()
        time.sleep(6)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)


class ExcluirCulturaTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    def testeExcluirCultura(self):
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

        nomeEvento_cultura.send_keys("Teste para excluir cultura")
        time.sleep(1)
        tipo_cultura.select_by_visible_text("Outros")
        time.sleep(1)
        cultura_cultura.select_by_visible_text("Batata")
        time.sleep(1)
        local_cultura.send_keys("Lote 230 - linha 90")
        time.sleep(1)
        descricao_cultura.send_keys("Descrição teste para o plantio de Batata")
        time.sleep(1)
        dataInicio_cultura.send_keys("22/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("10:00")
        time.sleep(1)
        dataFim_cultura.send_keys("24/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("12:00")
        time.sleep(1)

        salvar_btn.click()
        time.sleep(6)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-daygrid-event")))
        cultura_excluida = driver.find_element(By.CSS_SELECTOR, ".fc-daygrid-event")
        cultura_excluida.click()

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "delete-event-button")))
        btn_excluirCultura = driver.find_element(By.ID, "delete-event-button")
        btn_excluirCultura.click()

        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "confirmDeleteButton")))
        btn_confirmarExcluir = driver.find_element(By.ID, "confirmDeleteButton")
        btn_confirmarExcluir.click()
        time.sleep(6)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura1")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura1")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)


class ExibirClimaETempoTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    def testeMostrarTempo(self):
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

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "modeTempo")))
        btn_Clima = driver.find_element(By.ID, "modeTempo")
        driver.execute_script("arguments[0].click();", btn_Clima)

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wi.wi-day-cloudy.day-icon")))
        icone_climaTeste = driver.find_element(By.CSS_SELECTOR, ".wi.wi-day-cloudy.day-icon")
        icone_climaTeste.click()

        time.sleep(4)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fecharmodalClima")))
        fechar_modal = driver.find_element(By.ID, "fecharmodalClima")
        fechar_modal.click()

        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wi.wi-day-sprinkle.day-icon")))
        icone_climaTeste = driver.find_element(By.CSS_SELECTOR, ".wi.wi-day-sprinkle.day-icon")
        icone_climaTeste.click()

        time.sleep(4)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fecharmodalClima")))
        fechar_modal = driver.find_element(By.ID, "fecharmodalClima")
        fechar_modal.click()

    def testeMostrarFasesDaLua(self):
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

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "modeFasesLua")))
        btn_FasesLua = driver.find_element(By.ID, "modeFasesLua")
        btn_FasesLua.click()

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wi.wi-moon-new.moon-icon")))
        icone_LuaTeste = driver.find_element(By.CSS_SELECTOR, ".wi.wi-moon-new.moon-icon")
        icone_LuaTeste.click()

        time.sleep(4)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fecharmodalClima1")))
        fechar_modal = driver.find_element(By.ID, "fecharmodalClima1")
        fechar_modal.click()

        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wi.wi-moon-waxing-crescent-3.moon-icon")))
        icone_LuaTeste = driver.find_element(By.CSS_SELECTOR, ".wi.wi-moon-waxing-crescent-3.moon-icon")
        icone_LuaTeste.click()

        time.sleep(4)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fecharmodalClima1")))
        fechar_modal = driver.find_element(By.ID, "fecharmodalClima1")
        fechar_modal.click()

        time.sleep(2)


class AdicionarPragasTest(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
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

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)    

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pragas")))
        btn_calendar = driver.find_element(By.NAME, "pragas")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Batata")))
        btn_calendar = driver.find_element(By.NAME, "Batata")
        driver.execute_script("arguments[0].click();", btn_calendar)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "detalhes")))
        btn_calendar = driver.find_element(By.NAME, "detalhes")
        btn_calendar.send_keys("minha batata esta amarelada")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)    
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "botao_resolver")))
        btn_calendar = driver.find_element(By.NAME, "botao_resolver")
        driver.execute_script("arguments[0].click();", btn_calendar)
        time.sleep(3)
       

        doencas_container = driver.find_element(By.CLASS_NAME, "resultado-container")

        # Role para baixo dentro da seção específica usando JavaScript
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", doencas_container)

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "confirmarDoencasPragas")))
        btn_calendar = driver.find_element(By.ID, "confirmarDoencasPragas")
        driver.execute_script("arguments[0].click();", btn_calendar)
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "praga_Murcha-bacteriana")))
        btn_calendar = driver.find_element(By.ID, "praga_Murcha-bacteriana")
        driver.execute_script("arguments[0].click();", btn_calendar)
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "salvarSelecoes")))
        btn_calendar = driver.find_element(By.ID, "salvarSelecoes")
        driver.execute_script("arguments[0].click();", btn_calendar)
        time.sleep(2)

        # Verificar e aceitar o alerta antes de fazer o refresh
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())  # Espera pelo alerta
            alert = Alert(driver)
            alert.accept()  # Aceita o alerta
            print("Alerta aceito com sucesso.")
        except UnexpectedAlertPresentException as e:
            print(f"Erro ao lidar com o alerta: {str(e)}")
        except Exception as e:
            print(f"Outro erro ocorreu: {str(e)}")

        # Atualizar a página
        driver.refresh()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


class SolucoesPragasTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    def teste_Cultura(self):
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

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)    

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pragas")))
        btn_calendar = driver.find_element(By.NAME, "pragas")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Batata")))
        btn_calendar = driver.find_element(By.NAME, "Batata")
        driver.execute_script("arguments[0].click();", btn_calendar)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "detalhes")))
        btn_calendar = driver.find_element(By.NAME, "detalhes")
        btn_calendar.send_keys("minha batata esta amarelada")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)    
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "botao_resolver")))
        btn_calendar = driver.find_element(By.NAME, "botao_resolver")
        driver.execute_script("arguments[0].click();", btn_calendar)
        time.sleep(3)

        doencas_container = driver.find_element(By.CLASS_NAME, "resultado-container")

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", doencas_container)

        time.sleep(3)

        driver.get("http://127.0.0.1:8000/mainpage/")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_email")))
        email_login = driver.find_element(By.ID, "id_email")
        senhalogin = driver.find_element(By.ID, "id_password")
        btn_logar = driver.find_element(By.NAME, "btn_logar")

        email_login.send_keys("userteste@gmail.com")
        senhalogin.send_keys("@MinhasenhaForte1234")
        time.sleep(1)
        btn_logar.send_keys(Keys.ENTER)
        time.sleep(1)

        time.sleep(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pragas")))
        btn_calendar = driver.find_element(By.NAME, "pragas")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "cenoura")))
        btn_calendar = driver.find_element(By.NAME, "cenoura")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "detalhes")))
        btn_calendar = driver.find_element(By.NAME, "detalhes")
        btn_calendar.send_keys("minha cenoura esta verde")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)    
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "botao_resolver")))
        btn_calendar = driver.find_element(By.NAME, "botao_resolver")
        driver.execute_script("arguments[0].click();", btn_calendar)
        time.sleep(3)
       
        doencas_container = driver.find_element(By.CLASS_NAME, "resultado-container")

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", doencas_container)

        time.sleep(3)

        driver.get("http://127.0.0.1:8000/mainpage/")
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pragas")))
        btn_calendar = driver.find_element(By.NAME, "pragas")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "tomate")))
        btn_calendar = driver.find_element(By.NAME, "tomate")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "detalhes")))
        btn_calendar = driver.find_element(By.NAME, "detalhes")
        btn_calendar.send_keys("o tomate esta com cheiro de estragado")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)    
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "botao_resolver")))
        btn_calendar = driver.find_element(By.NAME, "botao_resolver")
        driver.execute_script("arguments[0].click();", btn_calendar)
        time.sleep(3)

        doencas_container = driver.find_element(By.CLASS_NAME, "resultado-container")

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", doencas_container)

        time.sleep(3)

        driver.get("http://127.0.0.1:8000/mainpage/")
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pragas")))
        btn_calendar = driver.find_element(By.NAME, "pragas")
        driver.execute_script("arguments[0].click();", btn_calendar)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Alface")))
        btn_calendar = driver.find_element(By.NAME, "Alface")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "detalhes")))
        btn_calendar = driver.find_element(By.NAME, "detalhes")
        btn_calendar.send_keys("o alface  esta com as folhas amareladas ")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)    
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "botao_resolver")))
        btn_calendar = driver.find_element(By.NAME, "botao_resolver")
        driver.execute_script("arguments[0].click();", btn_calendar)
        time.sleep(3)

        doencas_container = driver.find_element(By.CLASS_NAME, "resultado-container")

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", doencas_container)

        time.sleep(3)

        driver.get("http://127.0.0.1:8000/mainpage/")
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pragas")))
        btn_calendar = driver.find_element(By.NAME, "pragas")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "rucula")))
        btn_calendar = driver.find_element(By.NAME, "rucula")
        driver.execute_script("arguments[0].click();", btn_calendar)

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "detalhes")))
        btn_calendar = driver.find_element(By.NAME, "detalhes")
        btn_calendar.send_keys("o alface  esta com as folhas amareladas ")
        time.sleep(1)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "botao_resolver")))
        botao_resolver = driver.find_element(By.NAME, "botao_resolver")

        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", botao_resolver)
        time.sleep(2)

        botao_resolver.click()
        time.sleep(3)

        doencas_container = driver.find_element(By.CLASS_NAME, "resultado-container")

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", doencas_container)

        time.sleep(3)

        
class DashboardTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    def testeDashboard(self):
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

        nomeEvento_cultura.send_keys("Teste para DashBoard")
        time.sleep(1)
        tipo_cultura.select_by_visible_text("Outros")
        time.sleep(1)
        cultura_cultura.select_by_visible_text("Batata")
        time.sleep(1)
        local_cultura.send_keys("Lote 110 - linha 17")
        time.sleep(1)
        descricao_cultura.send_keys("Descrição teste para o plantio de Batata")
        time.sleep(1)
        dataInicio_cultura.send_keys("20/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("10:00")
        time.sleep(1)
        dataFim_cultura.send_keys("20/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("12:00")
        time.sleep(1)

        salvar_btn.click()
        time.sleep(6)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        # Aguarde o evento aparecer no DOM
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-daygrid-event")))

        # Localize o elemento
        cultura_excluida = driver.find_element(By.CSS_SELECTOR, ".fc-daygrid-event")

        # Role até o elemento usando Selenium
        actions = ActionChains(driver)
        actions.move_to_element(cultura_excluida).perform()

        # Aguarde até que o elemento seja clicável
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-daygrid-event")))

        # Clique no evento
        cultura_excluida.click()

        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "edit-event-button")))
        btn_editarCultura = driver.find_element(By.ID, "edit-event-button")
        btn_editarCultura.click()

        nomeEvento_culturaEditar = driver.find_element(By.ID, "id_title")
        salvar_btn = driver.find_element(By.CSS_SELECTOR, ".save-btn")

        time.sleep(2)
        nomeEvento_culturaEditar.clear()
        time.sleep(1)
        nomeEvento_culturaEditar.send_keys("Novo nome para o evento")
        time.sleep(2)

        salvar_btn.click()
        time.sleep(5)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
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

        nomeEvento_cultura.send_keys("Outra culura no DashBoard - Agora em andamento")
        time.sleep(1)
        tipo_cultura.select_by_visible_text("Preparo")
        time.sleep(1)
        cultura_cultura.select_by_visible_text("Rúcula")
        time.sleep(1)
        local_cultura.send_keys("Lote 1 - linha 2")
        time.sleep(1)
        descricao_cultura.send_keys("Descrição teste para o plantio de Rúcula")
        time.sleep(1)
        dataInicio_cultura.send_keys("29/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("10:00")
        time.sleep(1)
        dataFim_cultura.send_keys("30/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("12:00")
        time.sleep(1)

        salvar_btn.click()
        time.sleep(6)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(5)


class AlertaCriticoTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    @patch('site_cc.views.requests.get')
    def testeAlertaCritico(self, mock_get):
        mock_response = {
            'forecast': {
                'forecastday': [
                    {
                        'date': '22/11//2024',
                        'day': {
                            'maxtemp_c': 30,
                            'mintemp_c': 18,
                            'condition': {'text': 'Ensolarado', 'icon': '//cdn.weatherapi.com/weather/64x64/day/113.png'},
                            'avghumidity': 60,
                            'maxwind_kph': 15,
                            'totalprecip_mm': 0,
                            'uv': 7,
                        },
                        'astro': {
                            'moon_phase': 'Full Moon',
                            'moon_illumination': '100'
                        }
                    }
                ]
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

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

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "modeTempo")))
        btn_Clima = driver.find_element(By.ID, "modeTempo")
        driver.execute_script("arguments[0].click();", btn_Clima)

        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Clicar no ícone do clima
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".day-icon")))
        icone_climaTeste = driver.find_element(By.CSS_SELECTOR, ".day-icon")
        icone_climaTeste.click()

        time.sleep(4)

        # Verificar se o alerta crítico está visível
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "weatherModal")))
        alerta_critico = driver.find_element(By.ID, "criticalWarning")
        self.assertTrue(alerta_critico.is_displayed())

        # Fechar o modal
        fechar_modal = driver.find_element(By.ID, "fecharmodalClima")
        fechar_modal.click()
        time.sleep(2)


class InformarPlantiosTest(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()

    def teste_Cultura(self):
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

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "recomendacao")))
        btn_calendar = driver.find_element(By.NAME, "recomendacao")
        btn_calendar.click()
        time.sleep(1)

        select_element = driver.find_element(By.ID, "planta2")

        # Cria um objeto Select para manipular o dropdown
        dropdown = Select(select_element)

        # Seleciona a primeira opção (que não é o placeholder 'Escolha uma opção')
        dropdown.select_by_index(1)

        

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submit")))
        btn_calendar = driver.find_element(By.NAME, "submit")
        btn_calendar.click()
      

        
        select_element = driver.find_element(By.ID, "planta2")
        time.sleep(4)

        # Cria um objeto Select para manipular o dropdown
        dropdown = Select(select_element)

        # Seleciona a primeira opção (que não é o placeholder 'Escolha uma opção')
        dropdown.select_by_index(2)

        

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submit")))
        btn_calendar = driver.find_element(By.NAME, "submit")
        btn_calendar.click()
       

        select_element = driver.find_element(By.ID, "planta2")
        time.sleep(4)

        # Cria um objeto Select para manipular o dropdown
        dropdown = Select(select_element)

        # Seleciona a primeira opção (que não é o placeholder 'Escolha uma opção')
        dropdown.select_by_index(3)

        

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submit")))
        btn_calendar = driver.find_element(By.NAME, "submit")
        btn_calendar.click()
        

        select_element = driver.find_element(By.ID, "planta2")

        time.sleep(4)

        # Cria um objeto Select para manipular o dropdown
        dropdown = Select(select_element)

        # Seleciona a primeira opção (que não é o placeholder 'Escolha uma opção')
        dropdown.select_by_index(4)

        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submit")))
        btn_calendar = driver.find_element(By.NAME, "submit")
        btn_calendar.click()
        
        select_element = driver.find_element(By.ID, "planta2")

        time.sleep(4)

        dropdown = Select(select_element)

        # Seleciona a primeira opção (que não é o placeholder 'Escolha uma opção')

        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "submit")))
        btn_calendar = driver.find_element(By.NAME, "submit")
        btn_calendar.click()
        
        select_element = driver.find_element(By.ID, "planta2")

        time.sleep(4)
        


class ModalNotificacaoTest(LiveServerTestCase):

    
    @classmethod
    def setUpClass(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        subprocess.run(['python', 'manage.py', 'deleteusuarios'], check=True)
        super().tearDown()
    
    def teste_cultura(self):

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
        time.sleep(1)

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

        nomeEvento_cultura.send_keys("Teste para excluir cultura")
        time.sleep(1)
        tipo_cultura.select_by_visible_text("Colheita")
        time.sleep(1)
        cultura_cultura.select_by_visible_text("Batata")
        time.sleep(1)
        local_cultura.send_keys("Lote 230 - linha 90")
        time.sleep(1)
        descricao_cultura.send_keys("Descrição teste para o plantio de Batata")
        time.sleep(1)
        dataInicio_cultura.send_keys("25/11/2024")
        dataInicio_cultura.send_keys(Keys.TAB)
        dataInicio_cultura.send_keys("10:00")
        time.sleep(1)
        dataFim_cultura.send_keys("27/11/2024")
        dataFim_cultura.send_keys(Keys.TAB)
        dataFim_cultura.send_keys("20:00")
        time.sleep(1)

        salvar_btn.click()
        time.sleep(6)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_gerenciarCultura")))
        btn_gerenciarCultura = driver.find_element(By.NAME, "btn_gerenciarCultura")
        driver.execute_script("arguments[0].click();", btn_gerenciarCultura)
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "btn_calendario")))
        btn_calendar = driver.find_element(By.NAME, "btn_calendario")
        btn_calendar.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-daygrid-event")))
        cultura_excluida = driver.find_element(By.CSS_SELECTOR, ".fc-daygrid-event")
        cultura_excluida.click()

        time.sleep(3)

        try:
            warning_icon = driver.find_element(By.CLASS_NAME, "warning-icon")
            warning_icon.click()
            
            print("Ícone de alerta clicado com sucesso!")
        except Exception as e:
            print(f"Erro ao tentar clicar no ícone: {e}")
        
        time.sleep(8)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "genericModalMessage")))
        btn_calendar = driver.find_element(By.ID, "genericModalMessage")
        btn_calendar.click()    

        




       





