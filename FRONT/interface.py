import threading

import tkinter.filedialog as filedialog

from tkinter import messagebox

import customtkinter as ctk

from tkcalendar import DateEntry

from BACK.agendamento import converter_horario

from BACK.main import iniciar_automacao

cancelar_evento = threading.Event()


# CONFIGURAÇÃO DA INTERFACE

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


janela = ctk.CTk()

janela.title("Screenshot MTech")

janela.geometry("850x700")

janela.resizable(False, False)


# ÁREA COM ROLAGEM

area_rolagem = ctk.CTkScrollableFrame(janela, width=760, height=620)

area_rolagem.pack(padx=20, pady=20, fill="both", expand=True)


# FUNÇÕES


def escolher_pasta():

    pasta = filedialog.askdirectory()

    if pasta:
        campo_pasta.delete(0, "end")
        campo_pasta.insert(0, pasta)


def atualizar_status(mensagem):

    status.configure(text=mensagem)


def atualizar_botao_automacao(rodando):

    if rodando:

        botao_iniciar.configure(
            text="■  FINALIZAR AUTOMAÇÃO",
            fg_color="#C62828",
            hover_color="#8E0000",
            state="normal",
        )

    else:

        botao_iniciar.configure(
            text="▶  INICIAR AUTOMAÇÃO",
            fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"],
            hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"],
            state="normal",
        )


def cancelar_automacao_interface():

    cancelar_evento.set()

    atualizar_status("🟠 Cancelando automação...")

    botao_iniciar.configure(state="disabled")


def executar_automacao_thread():

    try:

        link = campo_url.get().strip()

        pasta = campo_pasta.get().strip()

        nome = campo_nome.get().strip()

        tipo_print = tipo_captura.get()

        tipo_execucao = tipo_execucao_var.get()

        if not link:

            janela.after(0, messagebox.showerror, "Erro", "Informe a URL do site.")

            return

        if not pasta:

            janela.after(
                0, messagebox.showerror, "Erro", "Selecione uma pasta de salvamento."
            )

            return

        if not nome:

            janela.after(
                0, messagebox.showerror, "Erro", "Informe o nome dos arquivos."
            )

            return

        janela.after(0, atualizar_status, "🟡 Iniciando automação...")

        # ==================================================
        # EXECUTAR AGORA
        # ==================================================

        if tipo_execucao == "1":

            resultado = iniciar_automacao(
                link=link,
                pasta_salvamento=pasta,
                nome_base=nome,
                tipo_print=tipo_print,
                tipo_execucao=tipo_execucao,
                cancelar_evento=cancelar_evento,
            )

        # ==================================================
        # EXECUÇÃO AGENDADA
        # ==================================================

        else:

            data_inicio = campo_data_inicio.get_date()

            data_fim = campo_data_fim.get_date()

            horario_inicio = converter_horario(campo_inicio.get().strip())

            horario_fim = converter_horario(campo_fim.get().strip())

            intervalo = int(campo_intervalo.get().strip())

            resultado = iniciar_automacao(
                link=link,
                pasta_salvamento=pasta,
                nome_base=nome,
                tipo_print=tipo_print,
                tipo_execucao=tipo_execucao,
                data_inicio=data_inicio,
                data_fim=data_fim,
                horario_inicio=horario_inicio,
                horario_fim=horario_fim,
                intervalo_segundos=intervalo,
                cancelar_evento=cancelar_evento,
            )

        # ==================================================
        # RESULTADO
        # ==================================================

        if cancelar_evento.is_set():

            janela.after(0, atualizar_status, "🟠 Automação cancelada.")

        elif resultado:

            janela.after(0, atualizar_status, "🟢 Automação concluída!")

        else:

            janela.after(0, atualizar_status, "🔴 A automação falhou.")

    except ValueError as erro:

        janela.after(0, messagebox.showerror, "Erro", str(erro))

        janela.after(0, atualizar_status, "🔴 Configuração inválida.")

    except Exception as erro:

        janela.after(0, messagebox.showerror, "Erro inesperado", str(erro))

        janela.after(0, atualizar_status, "🔴 Ocorreu um erro.")

    finally:

        cancelar_evento.clear()

        janela.after(0, atualizar_botao_automacao, False)


def iniciar_automacao_interface():

    cancelar_evento.clear()

    atualizar_botao_automacao(True)

    atualizar_status("🟡 Preparando automação...")

    thread = threading.Thread(target=executar_automacao_thread, daemon=True)

    thread.start()


def controlar_automacao():

    if botao_iniciar.cget("text").startswith("■"):

        cancelar_automacao_interface()

    else:

        iniciar_automacao_interface()


# TÍTULO

titulo = ctk.CTkLabel(area_rolagem, text="Screenshot MTech", font=("Arial", 28, "bold"))

titulo.pack(pady=(25, 5))


subtitulo = ctk.CTkLabel(
    area_rolagem, text="Automação de capturas de tela", font=("Arial", 14)
)

subtitulo.pack(pady=(0, 20))


# URL

card_url = ctk.CTkFrame(area_rolagem)

card_url.pack(padx=40, pady=8, fill="x")


texto_url = ctk.CTkLabel(card_url, text="🌐 URL do site", font=("Arial", 14, "bold"))

texto_url.pack(anchor="w", padx=20, pady=(15, 5))


campo_url = ctk.CTkEntry(card_url, placeholder_text="https://exemplo.com", height=35)

campo_url.pack(padx=20, pady=(5, 15), fill="x")


# PASTA

card_pasta = ctk.CTkFrame(area_rolagem)

card_pasta.pack(padx=40, pady=8, fill="x")


texto_pasta = ctk.CTkLabel(
    card_pasta, text="📁 Pasta de salvamento", font=("Arial", 14, "bold")
)

texto_pasta.pack(anchor="w", padx=20, pady=(15, 5))


linha_pasta = ctk.CTkFrame(card_pasta)

linha_pasta.pack(padx=20, pady=(5, 15), fill="x")


campo_pasta = ctk.CTkEntry(linha_pasta, placeholder_text="Selecione uma pasta")

campo_pasta.pack(side="left", padx=(0, 10), fill="x", expand=True)


botao_pasta = ctk.CTkButton(
    linha_pasta, text="Escolher", width=100, command=escolher_pasta
)

botao_pasta.pack(side="right")


# NOME

card_nome = ctk.CTkFrame(area_rolagem)

card_nome.pack(padx=40, pady=8, fill="x")


texto_nome = ctk.CTkLabel(
    card_nome, text="📝 Nome dos arquivos", font=("Arial", 14, "bold")
)

texto_nome.pack(anchor="w", padx=20, pady=(15, 5))


campo_nome = ctk.CTkEntry(card_nome, placeholder_text="Ex: captura_mtech")

campo_nome.pack(padx=20, pady=(5, 15), fill="x")


# TIPO DE CAPTURA

card_captura = ctk.CTkFrame(area_rolagem)

card_captura.pack(padx=40, pady=8, fill="x")


texto_captura = ctk.CTkLabel(
    card_captura, text="📸 Tipo de captura", font=("Arial", 14, "bold")
)

texto_captura.pack(anchor="w", padx=20, pady=(15, 5))


tipo_captura = ctk.StringVar(value="1")


radio_chrome = ctk.CTkRadioButton(
    card_captura, text="Navegador", variable=tipo_captura, value="1"
)

radio_chrome.pack(side="left", padx=(20, 10), pady=(5, 15))


radio_tela = ctk.CTkRadioButton(
    card_captura, text="Tela inteira", variable=tipo_captura, value="2"
)

radio_tela.pack(side="left", padx=10, pady=(5, 15))


radio_area = ctk.CTkRadioButton(
    card_captura, text="Área definida", variable=tipo_captura, value="3"
)

radio_area.pack(side="left", padx=10, pady=(5, 15))


radio_recorte = ctk.CTkRadioButton(
    card_captura, text="Recorte manual", variable=tipo_captura, value="4"
)

radio_recorte.pack(side="left", padx=10, pady=(5, 15))


# EXECUÇÃO

card_execucao = ctk.CTkFrame(area_rolagem)

card_execucao.pack(padx=40, pady=8, fill="x")


texto_execucao = ctk.CTkLabel(
    card_execucao, text="⏰ Execução", font=("Arial", 14, "bold")
)

texto_execucao.pack(anchor="w", padx=20, pady=(15, 5))


tipo_execucao_var = ctk.StringVar(value="1")


radio_agora = ctk.CTkRadioButton(
    card_execucao, text="Executar agora", variable=tipo_execucao_var, value="1"
)

radio_agora.pack(side="left", padx=(20, 10), pady=(5, 15))


radio_agendada = ctk.CTkRadioButton(
    card_execucao, text="Agendar", variable=tipo_execucao_var, value="2"
)

radio_agendada.pack(side="left", padx=10, pady=(5, 15))


# PERÍODO

card_periodo = ctk.CTkFrame(area_rolagem)

card_periodo.pack(padx=40, pady=8, fill="x")


texto_periodo = ctk.CTkLabel(
    card_periodo, text="📅 Período da automação", font=("Arial", 14, "bold")
)

texto_periodo.pack(anchor="w", padx=20, pady=(15, 10))


linha_datas = ctk.CTkFrame(card_periodo)

linha_datas.pack(padx=20, pady=(0, 15), fill="x")


texto_data_inicio = ctk.CTkLabel(linha_datas, text="Data inicial:")

texto_data_inicio.pack(side="left", padx=(0, 8))


campo_data_inicio = DateEntry(linha_datas, width=12, date_pattern="dd/mm/yyyy")

campo_data_inicio.pack(side="left", padx=(0, 30))


texto_data_fim = ctk.CTkLabel(linha_datas, text="Data final:")

texto_data_fim.pack(side="left", padx=(0, 8))


campo_data_fim = DateEntry(linha_datas, width=12, date_pattern="dd/mm/yyyy")

campo_data_fim.pack(side="left")


# HORÁRIOS

card_horarios = ctk.CTkFrame(area_rolagem)

card_horarios.pack(padx=40, pady=8, fill="x")


texto_horarios = ctk.CTkLabel(
    card_horarios, text="🕐 Horários", font=("Arial", 14, "bold")
)

texto_horarios.pack(anchor="w", padx=20, pady=(15, 10))


linha_horarios = ctk.CTkFrame(card_horarios)

linha_horarios.pack(padx=20, pady=(0, 15), fill="x")


texto_inicio = ctk.CTkLabel(linha_horarios, text="Início:")

texto_inicio.pack(side="left", padx=(0, 5))


campo_inicio = ctk.CTkEntry(linha_horarios, width=100, placeholder_text="HH:MM:SS")

campo_inicio.pack(side="left", padx=(0, 25))


texto_fim = ctk.CTkLabel(linha_horarios, text="Término:")

texto_fim.pack(side="left", padx=(0, 5))


campo_fim = ctk.CTkEntry(linha_horarios, width=100, placeholder_text="HH:MM:SS")

campo_fim.pack(side="left", padx=(0, 25))


texto_intervalo = ctk.CTkLabel(linha_horarios, text="Intervalo:")

texto_intervalo.pack(side="left", padx=(0, 5))


campo_intervalo = ctk.CTkEntry(linha_horarios, width=100, placeholder_text="segundos")

campo_intervalo.pack(side="left")


# STATUS

status = ctk.CTkLabel(area_rolagem, text="🟢 Pronto para iniciar", font=("Arial", 13))

status.pack(pady=(15, 5))


# BOTÃO INICIAR

botao_iniciar = ctk.CTkButton(
    area_rolagem,
    text="▶  INICIAR AUTOMAÇÃO",
    height=45,
    font=("Arial", 15, "bold"),
    command=controlar_automacao,
)

botao_iniciar.pack(padx=40, pady=(5, 25), fill="x")


# INICIAR INTERFACE

janela.mainloop()
