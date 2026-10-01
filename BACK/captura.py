import ctypes
import subprocess
import time

import pyautogui
from PIL import ImageGrab


def tirar_print_chrome(driver, nome_do_arquivo):

    time.sleep(3)

    try:

        driver.save_screenshot(nome_do_arquivo)

        print(f"📸 Captura do Chrome salva em: " f"{nome_do_arquivo}")

        return True

    except Exception as e:

        print(f"❌ Falha ao salvar captura " f"do Chrome: {e}")

        return False


def tirar_print_da_tela_toda(nome_do_arquivo):

    time.sleep(3)

    try:

        pyautogui.screenshot(nome_do_arquivo)

        print(f"🖥️ Captura do Windows salva em: " f"{nome_do_arquivo}")

        return True

    except Exception as e:

        print(f"❌ Falha ao salvar captura " f"do Windows: {e}")

        return False


def limpar_area_de_transferencia():

    try:

        ctypes.windll.user32.OpenClipboard(0)

        ctypes.windll.user32.EmptyClipboard()

        ctypes.windll.user32.CloseClipboard()

    except Exception as e:

        print(f"⚠️ Não foi possível limpar " f"o clipboard: {e}")


def abrir_ferramenta_recorte():

    try:

        subprocess.Popen(["powershell", "-Command", "Start-Process 'ms-screenclip:'"])

        return True

    except Exception as e:

        print(f"❌ Erro ao abrir a ferramenta " f"de recorte: {e}")

        return False


def capturar_recorte_nativo(nome_do_arquivo, tempo_limite=30):

    print("\n✂️ Abrindo a Ferramenta de " "Captura do Windows...")

    print("🖱️ Selecione a área desejada " "com o mouse.")

    limpar_area_de_transferencia()

    if not abrir_ferramenta_recorte():

        return False

    print("⏳ Aguardando você realizar " "o recorte...")

    inicio = time.time()

    while time.time() - inicio < tempo_limite:

        time.sleep(0.5)

        imagem = ImageGrab.grabclipboard()

        if imagem is not None and hasattr(imagem, "save"):

            try:

                imagem.save(nome_do_arquivo)

                print(f"📸 Recorte manual salvo em: " f"{nome_do_arquivo}")

                return True

            except Exception as e:

                print(f"❌ Erro ao salvar " f"o recorte: {e}")

                return False

    print("\n❌ Nenhum recorte foi detectado.")

    print("⚠️ O tempo limite foi atingido.")

    return False


def capturar_coordenadas_via_recorte_nativo():

    print("\n✂️ Definição da área automática")

    print("🖱️ Selecione a área que deverá " "ser monitorada.")

    limpar_area_de_transferencia()

    if not abrir_ferramenta_recorte():

        return None

    print("⏳ Aguardando você fazer " "a seleção...")

    imagem_recortada = None

    inicio = time.time()

    while time.time() - inicio < 30:

        time.sleep(0.5)

        conteudo = ImageGrab.grabclipboard()

        if conteudo is not None and hasattr(conteudo, "save"):

            imagem_recortada = conteudo

            break

    if imagem_recortada is None:

        print("❌ Nenhuma seleção foi detectada.")

        return None

    try:

        print("🔍 Tentando localizar " "a área selecionada...")

        posicao = pyautogui.locateOnScreen(imagem_recortada, confidence=0.9)

        if posicao:

            coordenadas = (
                int(posicao.left),
                int(posicao.top),
                int(posicao.width),
                int(posicao.height),
            )

            print(f"🎯 Área mapeada com sucesso: " f"{coordenadas}")

            return coordenadas

        print("⚠️ Não foi possível localizar " "automaticamente a área.")

        return None

    except Exception as e:

        print(f"⚠️ Erro ao calcular " f"coordenadas: {e}")

        return None


def tirar_print_area_salva(coordenadas, nome_do_arquivo):

    try:

        pyautogui.screenshot(nome_do_arquivo, region=coordenadas)

        print(f"✂️ Captura automática " f"da área salva: " f"{nome_do_arquivo}")

        return True

    except Exception as e:

        print(f"❌ Falha ao realizar " f"captura da área: {e}")

        return False
