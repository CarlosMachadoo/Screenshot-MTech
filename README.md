# Screenshot MTech

Aplicação desktop desenvolvida em Python para **automação de capturas de tela**, permitindo realizar capturas manuais ou programadas de diferentes áreas do computador, com execução imediata ou agendada.
O projeto foi desenvolvido como parte dos estudos práticos de desenvolvimento de software e também como um dos primeiros produtos da **MTech**, iniciativa voltada à criação de soluções de tecnologia e automação.

## Funcionalidades

- Captura da janela do Google Chrome
- Captura da tela inteira
- Captura de uma área previamente definida
- Recorte manual utilizando a ferramenta nativa do Windows
- Execução imediata
- Agendamento por período e horário
- Capturas recorrentes em intervalos definidos
- Cancelamento da automação em execução
- Seleção da pasta de destino
- Definição personalizada do nome dos arquivos
- Geração automática de data e horário nos nomes das capturas
- Interface gráfica em modo escuro

## Interface

A aplicação possui uma interface gráfica desenvolvida com **CustomTkinter**, permitindo configurar a automação sem necessidade de utilizar o terminal.

Principais configurações disponíveis:

- URL do site
- Pasta de salvamento
- Nome dos arquivos
- Tipo de captura
- Tipo de execução
- Data inicial e final
- Horário inicial e final
- Intervalo entre capturas

## Tecnologias utilizadas

### Linguagem

- Python

### Interface

- CustomTkinter
- Tkinter
- tkcalendar

### Automação

- Selenium
- PyAutoGUI

### Capturas

- Pillow
- Windows Screen Clipping
- ImageGrab

### Empacotamento

- PyInstaller

## Estrutura do projeto

```text
Screenshot-MTech/
│
├── BACK/
│   ├── agendamento.py
│   ├── captura.py
│   ├── main.py
│   └── navegador.py
│
├── FRONT/
│   └── interface.py
│
├── version.py
│
├── .gitignore
│
└── README.md
```

### BACK

Responsável pela lógica e funcionalidades da aplicação.

- `main.py` — coordenação principal da automação
- `agendamento.py` — criação e gerenciamento dos agendamentos
- `captura.py` — funções relacionadas às capturas de tela
- `navegador.py` — abertura e controle do Google Chrome através do Selenium

### FRONT

Responsável pela interface gráfica da aplicação.

- `interface.py` — criação da interface e interação com o usuário

### version.py

Responsável pelo controle da versão da aplicação.

## ⚙️ Como funciona

O usuário configura os parâmetros da automação através da interface.

A aplicação então pode executar uma captura imediatamente ou seguir um agendamento configurado.

Exemplo:

```text
Usuário
   │
   ▼
Configura automação
   │
   ├── URL
   ├── Pasta
   ├── Tipo de captura
   ├── Data
   ├── Horário
   └── Intervalo
   │
   ▼
Screenshot MTech
   │
   ▼
Google Chrome
   │
   ▼
Captura
   │
   ▼
Arquivo .PNG
```

## 📸 Tipos de captura

### 1. Navegador

Realiza uma captura da página aberta no Google Chrome utilizando Selenium.

### 2. Tela inteira

Realiza uma captura de toda a tela do Windows.

### 3. Área definida

Permite selecionar uma área uma única vez e reutilizar essa mesma região nas capturas seguintes.

### 4. Recorte manual

Utiliza a ferramenta nativa de recorte do Windows para realizar uma nova seleção a cada captura.

## Sistema de agendamento

A aplicação permite definir:

- Data inicial
- Data final
- Horário de início
- Horário de término
- Intervalo entre capturas

Durante a execução, o sistema monitora o horário programado e realiza as capturas automaticamente.

A automação também pode ser cancelada através do botão **Finalizar Automação**.

## Nome dos arquivos

Os arquivos são gerados automaticamente seguindo um padrão semelhante a:

```text
captura_mtech_30.09.26_22.48.15_chrome.png
```

O nome contém:

```text
[nome]_[data]_[horário]_[tipo].png
```

Caracteres inválidos para nomes de arquivos do Windows são tratados automaticamente.

## Versionamento

O projeto utiliza versionamento para acompanhar a evolução da aplicação.

Versão inicial:

```text
v1.0.0
```

A ideia é utilizar versões futuras para representar:

- Correções de bugs
- Melhorias
- Novas funcionalidades
- Alterações estruturais

## Objetivo do projeto

O Screenshot MTech começou como um projeto prático para desenvolver conhecimentos em:

- Desenvolvimento de aplicações desktop
- Automação com Python
- Selenium
- Manipulação de arquivos
- Interfaces gráficas
- Threads e execução em segundo plano
- Agendamento de tarefas
- Organização de projetos
- Empacotamento de aplicações
- Controle de versões com Git

Além do objetivo educacional, o projeto serve como base para explorar a criação de **soluções de automação voltadas a situações reais**.

## Próximos passos

Algumas funcionalidades planejadas para futuras versões:

- [ ] Instalador para Windows
- [ ] Sistema de atualização da aplicação
- [ ] Verificação automática de novas versões
- [ ] Melhorias na experiência da interface
- [ ] Registro de logs
- [ ] Configurações persistentes
- [ ] Melhor tratamento de erros
- [ ] Novas opções de automação
- [ ] Evolução da arquitetura da aplicação

## Status

**Versão atual: `v1.0.0`**

Primeira versão funcional do Screenshot MTech.
O projeto continua em desenvolvimento e novas funcionalidades serão adicionadas conforme sua evolução.

## Autor

Desenvolvido por **Carlos Eduardo** como projeto prático de desenvolvimento de software e automação.

**MTech — Tecnologia e Automação**
