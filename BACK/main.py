import os
import time
from datetime import datetime

from BACK.navegador import (
    abre_navegador,
    acessar_pagina,
    recarregar_pagina,
)

from BACK.captura import (
    tirar_print_chrome,
    tirar_print_da_tela_toda,
    capturar_coordenadas_via_recorte_nativo,
    tirar_print_area_salva,
    capturar_recorte_nativo,
)

from BACK.agendamento import (
    criar_agendamento,
    gerar_periodos_diarios,
    esperar_horario_inicio,
    calcular_proximo_horario,
    deve_encerrar,
)

# Guarda as coordenadas da captura de área automática
coordenadas_salvas = None


def limpar_nome_arquivo(nome):
    caracteres_invalidos = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]

    for caractere in caracteres_invalidos:
        nome = nome.replace(caractere, "_")

    return nome


def gerar_nome_arquivo(pasta, nome_base, tipo_print):
    horario = datetime.now().strftime("%d.%m.%y_%H.%M.%S")

    nome_base = limpar_nome_arquivo(nome_base)

    tipos = {
        "1": "chrome",
        "2": "windows",
        "3": "area",
        "4": "recorte",
    }

    tipo = tipos.get(tipo_print, "captura")

    nome = f"{nome_base}_{horario}_{tipo}.png"

    return os.path.join(pasta, nome)


def executar_captura(
    driver,
    pasta_salvamento,
    nome_base,
    tipo_print,
    cancelar_evento=None,
):
    global coordenadas_salvas

    if cancelar_evento and cancelar_evento.is_set():
        print("🛑 Captura cancelada pelo usuário.")
        return False

    os.makedirs(pasta_salvamento, exist_ok=True)

    nome_completo = gerar_nome_arquivo(
        pasta_salvamento,
        nome_base,
        tipo_print,
    )

    # 1 - PRINT DO CHROME

    if tipo_print == "1":
        return tirar_print_chrome(driver, nome_completo)

    # 2 - PRINT DA TELA INTEIRA

    if tipo_print == "2":
        return tirar_print_da_tela_toda(nome_completo)

    # 3 - PRINT DE ÁREA AUTOMÁTICA

    if tipo_print == "3":

        if cancelar_evento and cancelar_evento.is_set():
            print("🛑 Captura cancelada pelo usuário.")
            return False

        if coordenadas_salvas is None:
            print("\n🎯 Primeira captura da área.")
            print("Será necessário selecionar a área que será monitorada.")

            coordenadas_salvas = capturar_coordenadas_via_recorte_nativo()

            if coordenadas_salvas is None:
                print("❌ Não foi possível definir a área.")
                return False

        return tirar_print_area_salva(
            coordenadas_salvas,
            nome_completo,
        )

    # 4 - RECORTE MANUAL

    if tipo_print == "4":

        if cancelar_evento and cancelar_evento.is_set():
            print("🛑 Captura cancelada pelo usuário.")
            return False

        return capturar_recorte_nativo(nome_completo)

    print("❌ Tipo de captura inválido.")

    return False


def abrir_e_configurar_navegador(link):
    print("\n🌐 Abrindo Google Chrome...")

    driver = abre_navegador()

    if not driver:
        print("❌ Não foi possível abrir o navegador.")
        return None

    print("⏳ Navegador iniciado.")
    print("🌐 Acessando endereço...")

    sucesso = acessar_pagina(driver, link)

    if not sucesso:
        print("❌ Não foi possível acessar a página.")

        driver.quit()

        return None

    print("🔄 Recarregando página...")

    recarregar_pagina(driver)

    time.sleep(1)

    return driver


def executar_agora(
    link,
    pasta_salvamento,
    nome_base,
    tipo_print,
    cancelar_evento=None,
):
    if cancelar_evento and cancelar_evento.is_set():
        print("🛑 Automação cancelada antes de iniciar.")
        return False

    driver = abrir_e_configurar_navegador(link)

    if not driver:
        return False

    try:
        if cancelar_evento and cancelar_evento.is_set():
            print("🛑 Automação cancelada.")

            return False

        print("\n📸 Realizando captura...")

        sucesso = executar_captura(
            driver,
            pasta_salvamento,
            nome_base,
            tipo_print,
            cancelar_evento,
        )

        return sucesso

    finally:
        print("\n🌐 Fechando Google Chrome...")

        try:
            driver.quit()
        except Exception:
            pass

        print("✅ Navegador fechado.")


def executar_agendamento(
    link,
    pasta_salvamento,
    nome_base,
    tipo_print,
    data_inicio,
    data_fim,
    horario_inicio,
    horario_fim,
    intervalo_segundos,
    cancelar_evento=None,
):
    global coordenadas_salvas

    # CRIA O AGENDAMENTO

    agendamento = criar_agendamento(
        data_inicio,
        data_fim,
        horario_inicio,
        horario_fim,
        intervalo_segundos,
    )

    print("\n========================================")
    print("📅 AGENDAMENTO INICIADO")
    print(f"📆 De: {data_inicio.strftime('%d/%m/%Y')}")
    print(f"📆 Até: {data_fim.strftime('%d/%m/%Y')}")
    print(f"🕐 Horário inicial: {horario_inicio.strftime('%H:%M:%S')}")
    print(f"🕐 Horário final: {horario_fim.strftime('%H:%M:%S')}")
    print(f"⏱️ Intervalo: {intervalo_segundos} segundos")
    print("========================================")

    # GERA OS PERÍODOS DE CADA DIA

    periodos = gerar_periodos_diarios(
        agendamento["data_inicio"],
        agendamento["data_fim"],
        agendamento["horario_inicio"],
        agendamento["horario_fim"],
    )

    # PERCORRE CADA DIA

    for inicio, fim in periodos:

        if cancelar_evento and cancelar_evento.is_set():
            print("\n🛑 AGENDAMENTO CANCELADO PELO USUÁRIO.")

            return False

        agora = datetime.now()

        # Se o período daquele dia já acabou
        if agora >= fim:
            print(
                f"\n⏭️ Período de " f"{inicio.strftime('%d/%m/%Y')} " f"já encerrado."
            )

            continue

        print("\n========================================")
        print(f"📅 DATA: {inicio.strftime('%d/%m/%Y')}")
        print(f"🕐 INÍCIO: {inicio.strftime('%H:%M:%S')}")
        print(f"🕐 FIM: {fim.strftime('%H:%M:%S')}")
        print("========================================")

        # ESPERA ATÉ O HORÁRIO DE INÍCIO

        if datetime.now() < inicio:

            while datetime.now() < inicio:

                if cancelar_evento and cancelar_evento.is_set():
                    print("\n🛑 AGENDAMENTO CANCELADO PELO USUÁRIO.")

                    return False

                tempo_restante = (inicio - datetime.now()).total_seconds()

                time.sleep(min(1, max(0.1, tempo_restante)))

        # DEFINE PRIMEIRO HORÁRIO DE CAPTURA

        proximo = max(datetime.now(), inicio)

        # LOOP DAS CAPTURAS

        while not deve_encerrar(proximo, fim):

            if cancelar_evento and cancelar_evento.is_set():
                print("\n🛑 AGENDAMENTO CANCELADO PELO USUÁRIO.")

                return False

            agora = datetime.now()

            if agora >= fim:
                break

            print("\n----------------------------------------")
            print(f"📸 Captura programada para " f"{agora.strftime('%H:%M:%S')}")
            print("----------------------------------------")

            # ABRE O CHROME

            driver = abrir_e_configurar_navegador(link)

            if driver:

                try:

                    if cancelar_evento and cancelar_evento.is_set():
                        print("🛑 Cancelamento solicitado.")

                        return False

                    # REALIZA A CAPTURA

                    sucesso = executar_captura(
                        driver,
                        pasta_salvamento,
                        nome_base,
                        tipo_print,
                        cancelar_evento,
                    )

                    if sucesso:
                        print("✅ Captura realizada com sucesso!")

                    else:
                        if cancelar_evento and cancelar_evento.is_set():
                            print("🛑 Captura cancelada pelo usuário.")

                            return False

                        print("❌ Falha na captura.")

                finally:

                    # FECHA O CHROME

                    print("🌐 Fechando Google Chrome...")

                    try:
                        driver.quit()
                    except Exception:
                        pass

                    print("✅ Navegador fechado.")

            else:
                print("❌ Não foi possível abrir " "o navegador para esta captura.")

            if cancelar_evento and cancelar_evento.is_set():
                print("\n🛑 AGENDAMENTO CANCELADO PELO USUÁRIO.")

                return False

            # CALCULA PRÓXIMO HORÁRIO

            proximo = calcular_proximo_horario(
                agora,
                intervalo_segundos,
            )

            # VERIFICA SE O PRÓXIMO HORÁRIO
            # JÁ PASSOU DO FIM

            if proximo >= fim:
                break

            tempo_espera = (proximo - datetime.now()).total_seconds()

            if tempo_espera > 0:

                print(f"\n⏳ Próxima captura em " f"{tempo_espera:.1f} segundos.")

                # Espera em pequenos intervalos para
                # conseguir detectar o cancelamento.

                tempo_decorrido = 0

                while tempo_decorrido < tempo_espera:

                    if cancelar_evento and cancelar_evento.is_set():
                        print("\n🛑 AGENDAMENTO CANCELADO " "PELO USUÁRIO.")

                        return False

                    passo = min(0.5, tempo_espera - tempo_decorrido)

                    time.sleep(passo)

                    tempo_decorrido += passo

    print("\n========================================")
    print("✅ AGENDAMENTO CONCLUÍDO!")
    print("========================================")

    return True


def iniciar_automacao(
    link,
    pasta_salvamento,
    nome_base,
    tipo_print,
    tipo_execucao,
    data_inicio=None,
    data_fim=None,
    horario_inicio=None,
    horario_fim=None,
    intervalo_segundos=None,
    cancelar_evento=None,
):

    # EXECUÇÃO IMEDIATA

    if tipo_execucao == "1":

        return executar_agora(
            link,
            pasta_salvamento,
            nome_base,
            tipo_print,
            cancelar_evento,
        )

    # EXECUÇÃO AGENDADA

    if tipo_execucao == "2":

        return executar_agendamento(
            link,
            pasta_salvamento,
            nome_base,
            tipo_print,
            data_inicio,
            data_fim,
            horario_inicio,
            horario_fim,
            intervalo_segundos,
            cancelar_evento,
        )

    print("❌ Tipo de execução inválido.")

    return False
