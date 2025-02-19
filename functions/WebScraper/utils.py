from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui

def getGrau(driver, graus):
    try:
        dropdown_grau = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[3]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container-group[3]/transform/div/div[2]/visual-container[1]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div/i'))
        )
        dropdown_grau.click()
        print("Dropdown de Grau encontrado e expandido.")
    except:
        print("Erro: O dropdown de Grau não foi encontrado ou não pôde ser expandido.")
        driver.quit()
        exit()  # Sai do script se o dropdown não for encontrado

    try:
        # Encontrar e clicar na checkbox "1º Grau"
        primeiro_grau_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@title="1º Grau"]/div[@class="slicerCheckbox"]/span'))
        )
        primeiro_grau_checkbox.click()
        print("Checkbox '1º Grau' encontrada e clicada.")

        # Encontrar e clicar na checkbox "2º Grau"
        #segundo_grau_checkbox = WebDriverWait(driver, 10).until(
        #    EC.element_to_be_clickable((By.XPATH, '//*[@title="2º Grau"]/div[@class="slicerCheckbox"]/span'))
        #)
        #segundo_grau_checkbox.click()
        #print("Checkbox '2º Grau' encontrada e clicada.")
            
    except:
        print("Erro: As checkboxes '1º Grau' ou '2º Grau' não foram encontradas ou não puderam ser clicadas.")
        driver.quit()
        exit()  # Sai do script se as opções não forem encontradas


def getIndicador(driver, indicadores):
    try:
        dropdown_grau = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[3]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container-group[2]/transform/div/div[2]/visual-container[1]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div/i'))
        )
        dropdown_grau.click()
        print("Dropdown de Indicador encontrado e expandido.")
    except:
        print("Erro: O dropdown de Indicador não foi encontrado ou não pôde ser expandido.")
        driver.quit()
        exit()  # Sai do script se o dropdown não for encontrado

    #pegando o indicador "julgados"
    try:
        dropdown_grau = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@title="Julgados"]/div[@class="slicerCheckbox"]/span'))
        )
        dropdown_grau.click()
        print("Dropdown de Julgado encontrado e expandido.")
    except:
            print("Erro: O dropdown de Julgado não foi encontrado ou não pôde ser expandido.")
            driver.quit()
            exit()  # Sai do script se o dropdown não for encontrado

def getTribunal(driver, tribunais):
        # 9. Clicar no dropdown de Tribunal para expandir as opções uma vez
        try:
            dropdown_grau = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[3]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container-group[1]/transform/div/div[2]/visual-container[1]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div'))
            )
            dropdown_grau.click()
            print("Dropdown de Tribunal encontrado e expandido.")
            time.sleep(3)
        except:
            print("Erro: O dropdown de Tribunal não foi encontrado ou não pôde ser expandido.")
            driver.quit()
            exit()  # Sai do script se o dropdown não for encontrado

        # 10. Clicar no dropdown de Tribunal no TRTx para expandir as opções uma vez
        try:
            # Usar pyautogui para escrever "TRTx"
            tribunal_text = f"TRT8"
            pyautogui.hotkey('ctrl', 'a')  # Seleciona tudo
            pyautogui.press('backspace')   # Apaga o texto selecionado
            pyautogui.write(tribunal_text)
            time.sleep(1)  # Pausa para permitir que o filtro seja aplicado
            print(f"Texto '{tribunal_text}' digitado no dropdown de Tribunal para filtragem.")
            
            # Clicar na opção "TRTx" após o filtro
            trt1_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@title="{tribunal_text}"]/div[@class="slicerCheckbox"]/span'))
            )
            trt1_option.click()
            print(f"Checkbox '{tribunal_text}' encontrada e clicada.")
        except:
            print(f"Erro: O dropdown de {tribunal_text} não foi encontrado ou não pôde ser expandido.")
            driver.quit()
            exit()  # Sai do script se o dropdown não for encontrado

        # 11. Clicar no dropdown de Tribunal para expandir as opções uma vez
        try:
            dropdown_grau = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[3]/transform/div/div[2]/visual-container-group/transform/div/div[2]/visual-container-group[1]/transform/div/div[2]/visual-container[1]/transform/div/div[3]/div/div/visual-modern/div/div/div[2]/div'))
            )
            dropdown_grau.click()
            print("Dropdown de Tribunal encontrado e expandido.")
            time.sleep(3)
        except:
            print("Erro: O dropdown de Tribunal não foi encontrado ou não pôde ser expandido.")
            driver.quit()
            exit()  # Sai do script se o dropdown não for encontrado

        download(driver)

def download(driver):
    try:
        dropdown_grau = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-group[3]/transform/div/div[2]/visual-container[3]/transform/div/div[3]/div/div/visual-modern/div/iframe'))
        )
        dropdown_grau.click()
        print("Download encontrado e expandido.")
        time.sleep(40)
    except:
        print("Erro: O download não foi encontrado ou não pôde ser expandido.")
        driver.quit()
        exit()  # Sai do script se o dropdown não for encontrado