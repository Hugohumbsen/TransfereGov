from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

import time

# Configurações do navegador
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Inicializa o driver
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=chrome_options)

# Remove o sinal de automação
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
    """
})

# Abre o site
driver.get("https://www.gov.br/transferegov/pt-br/sistemas/acesso-livre")
time.sleep(3)

# Tenta clicar no botão "Aceitar cookies"
try:
    botao_cookies = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-accept') and @aria-label='Aceitar cookies']")
    botao_cookies.click()
    print("Botão de cookies clicado.")
except NoSuchElementException:
    print("Botão de cookies não encontrado.")

time.sleep(2)

# Clica no link "Consultar Programas"
link = driver.find_element(By.LINK_TEXT, "Consultar Programas")
link.click()
time.sleep(3)

# Muda para a nova aba
abas = driver.window_handles
driver.switch_to.window(abas[1])

time.sleep(2)
# Selecionar a primeira opção do select "qualificacaoProponente"
qualificacao_select = Select(driver.find_element(By.ID, "consultarQualificacaoProponente"))
qualificacao_select.select_by_index(1)  # índice 0 é a opção vazia, 1 é "Proposta Voluntária"

# Preenche o campo "Ano do Programa"
ano_input = driver.find_element(By.ID, "consultarAnoPrograma")
ano_input.clear()
ano_input.send_keys("2025")

# Preenche o campo "Descrição"
descricao_textarea = driver.find_element(By.ID, "consultarDescricao")
descricao_textarea.clear()
descricao_textarea.send_keys("lgbtqia+")

# Selecionar a opção "Termo de Fomento" no select "modalidade"
modalidade_select = Select(driver.find_element(By.ID, "consultarModalidade"))
modalidade_select.select_by_visible_text("Termo de Fomento")

time.sleep(1)
checkboxes = driver.find_elements(By.NAME, "camposParaExibirAsArray")
values_to_check = {"0", "1", "6"}

for checkbox in checkboxes:
    valor = checkbox.get_attribute("value")
    if valor in values_to_check and not checkbox.is_selected():
        checkbox.click()


time.sleep(2)
programa_atende_checks = driver.find_elements(By.NAME, "programaAtendeAsArray")
for checkbox in programa_atende_checks:
    if checkbox.get_attribute("value") == "2" and not checkbox.is_selected():
        checkbox.click()
        break  # já achou e clicou, pode sair do loop
time.sleep(2)
valores_para_marcar = [str(i) for i in range(1, 28)]  # Valores de "1" até "27"
checkboxes_estados = driver.find_elements(By.NAME, "estadosHabilitadoAsArray")

for checkbox in checkboxes_estados:
    valor = checkbox.get_attribute("value")
    if valor in valores_para_marcar and not checkbox.is_selected():
        checkbox.click()


# Clica no botão "Consultar"
consultar_btn = driver.find_element(By.ID, "form_submit")
consultar_btn.click()


time.sleep(3)


abas = driver.window_handles
driver.switch_to.window([-1])

#time.sleep(10)
#driver.quit()
