from datetime import datetime, timedelta
import time


def converter_horario(horario):

    return datetime.strptime(horario, "%H:%M:%S").time()


def converter_data(data):

    return datetime.strptime(data, "%d/%m/%Y").date()


def criar_datetime(data, horario):

    return datetime.combine(data, horario)


def validar_periodo(data_inicio, data_fim):

    if data_fim < data_inicio:

        raise ValueError("A data final não pode ser " "anterior à data inicial.")


def validar_intervalo(intervalo_segundos):

    if intervalo_segundos <= 0:

        raise ValueError("O intervalo precisa ser " "maior que zero.")


def criar_agendamento(
    data_inicio, data_fim, horario_inicio, horario_fim, intervalo_segundos
):

    validar_periodo(data_inicio, data_fim)

    validar_intervalo(intervalo_segundos)

    return {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "horario_inicio": horario_inicio,
        "horario_fim": horario_fim,
        "intervalo": intervalo_segundos,
    }


def gerar_periodos_diarios(data_inicio, data_fim, horario_inicio, horario_fim):

    data_atual = data_inicio

    while data_atual <= data_fim:

        inicio = criar_datetime(data_atual, horario_inicio)

        fim = criar_datetime(data_atual, horario_fim)

        if fim <= inicio:

            fim += timedelta(days=1)

        yield inicio, fim

        data_atual += timedelta(days=1)


def esperar_horario_inicio(horario_inicio):

    while True:

        agora = datetime.now()

        if agora >= horario_inicio:

            break

        tempo_restante = (horario_inicio - agora).total_seconds()

        print(f"\r⏳ Iniciando em " f"{tempo_restante:.1f} segundos...", end="")

        time.sleep(min(1, tempo_restante))

    print("\n🚀 Horário de início atingido!")


def calcular_proximo_horario(horario_atual, intervalo_segundos):

    return horario_atual + timedelta(seconds=intervalo_segundos)


def deve_encerrar(agora, horario_fim):

    return agora >= horario_fim
