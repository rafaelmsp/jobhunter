import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import locale
import webbrowser
import os
import sys

# Função para obter o caminho dos recursos (imagem) de forma correta, seja no script Python ou no executável
def resource_path(relative_path):
    """Obtém o caminho absoluto para recursos, funciona para o executável e o script Python"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Configurando o formato monetário brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Dicionário com estados de países
estados_paises = {
    "Brasil": ["Todos os estados", "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
               "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará",
               "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul",
               "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"],
    "Estados Unidos": ["Todos os estados", "Alabama", "Alasca", "Arizona", "Arkansas", "Califórnia", "Colorado", "Connecticut"],
    "Canadá": ["Todos os estados", "Alberta", "British Columbia", "Manitoba", "Nova Scotia", "Ontario", "Quebec"]
}

# Função para formatar o salário no formato brasileiro
def formatar_salario(valor):
    if valor and valor != 'Não especificado' and float(valor) > 0:
        try:
            valor = float(valor) / 10  # Dividir por 10 para remover o último dígito extra
            salario_formatado = locale.currency(valor, grouping=True)
            return salario_formatado
        except ValueError:
            return 'Não especificado'
    return 'Não especificado'

# Função para buscar vagas na API do Adzuna
def buscar_vagas_adzuna(app_id, app_key, palavra_chave, localizacao, num_paginas=1):
    try:
        vagas_adzuna = []
        url = f"https://api.adzuna.com/v1/api/jobs/br/search/{num_paginas}?app_id={app_id}&app_key={app_key}&results_per_page=10&what={palavra_chave}&where={localizacao}"
        resposta = requests.get(url)
        dados = resposta.json()

        for vaga in dados['results']:
            salario_min = vaga.get('salary_min', 'Não especificado')
            salario_max = vaga.get('salary_max', 'Não especificado')
            salario = f"{formatar_salario(salario_min)} - {formatar_salario(salario_max)}" if salario_min != 'Não especificado' else 'Não especificado'
            
            vagas_adzuna.append({
                'Título': vaga.get('title', 'N/A'),
                'Empresa': vaga.get('company', {}).get('display_name', 'N/A'),
                'Localização': vaga.get('location', {}).get('display_name', 'N/A'),
                'Salário': salario,
                'Fonte': 'Adzuna',
                'Cadastro': vaga.get('redirect_url', 'N/A')  # Link de cadastro
            })
        
        return vagas_adzuna
    except Exception as e:
        print(f"Erro ao buscar vagas no Adzuna: {e}")
        return []

# Função principal para buscar vagas usando todas as APIs
def buscar_vagas(palavra_chave, localizacao):
    adzuna_app_id = '5477d8a6'
    adzuna_app_key = '3d02b1db4853e19b1cf44023decb4e8c'

    # Coletando as vagas de Adzuna
    vagas_adzuna = buscar_vagas_adzuna(adzuna_app_id, adzuna_app_key, palavra_chave, localizacao)

    return vagas_adzuna

# Função para buscar as vagas e exibir na interface
def buscar_e_exibir_vagas():
    global vagas
    palavra_chave = entry_oq.get()
    pais = combobox_pais.get()
    estado = combobox_estado.get()

    # Se o país for Brasil e o estado for "Todos os estados", buscar em todo o Brasil
    localizacao = estado if pais == "Brasil" and estado != "Todos os estados" else pais

    if not palavra_chave or not localizacao:
        messagebox.showwarning("Campos Obrigatórios", "Por favor, insira a vaga e a localização.")
        return
    
    for item in tree.get_children():
        tree.delete(item)

    vagas = buscar_vagas(palavra_chave, localizacao)

    if not vagas:
        messagebox.showinfo("Sem Resultados", "Nenhuma vaga encontrada para a busca realizada.")
        return

    for vaga in vagas:
        tree.insert('', 'end', values=(vaga['Título'], vaga['Empresa'], vaga['Localização'], vaga['Salário'], vaga['Fonte']))

# Função para abrir o link da vaga no navegador
def abrir_link(cadastro_url):
    if cadastro_url != 'N/A':
        webbrowser.open(cadastro_url)
    else:
        messagebox.showwarning("Link indisponível", "Nenhum link de cadastro disponível para esta vaga.")

# Função para exibir os detalhes da vaga selecionada
def exibir_detalhes(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        vaga_titulo = item['values'][0]

        for vaga in vagas:
            if vaga['Título'] == vaga_titulo:
                detalhes = (
                    f"Título: {vaga['Título']}\n"
                    f"Empresa: {vaga['Empresa']}\n"
                    f"Localização: {vaga['Localização']}\n"
                    f"Salário: {vaga['Salário']}\n"
                    f"Fonte: {vaga['Fonte']}\n"
                    f"Cadastro: {vaga['Cadastro']}"
                )

                detalhes_janela = tk.Toplevel(janela)
                detalhes_janela.title("Detalhes da Vaga")

                text_box = tk.Text(detalhes_janela, wrap='word', font=("Helvetica", 12))
                text_box.insert('1.0', detalhes)
                text_box.config(state='normal')
                text_box.pack(expand=True, fill='both', padx=10, pady=10)

                botao_link = tk.Button(detalhes_janela, text="Candidatar-se à Vaga", command=lambda: abrir_link(vaga['Cadastro']), bg="#004080", fg="white", font=("Helvetica", 12), relief='flat', bd=0)
                botao_link.pack(pady=10)

                break

# Função para limpar os campos de busca e a lista de resultados
def limpar_busca():
    entry_oq.delete(0, 'end')
    combobox_pais.current(0)  # Brasil como padrão
    atualizar_estados()  # Atualizar lista de estados
    combobox_estado.current(0)  # Todos os estados como padrão
    combobox_fonte.current(0)  # Adzuna como padrão
    for item in tree.get_children():
        tree.delete(item)

# Função para atualizar os estados conforme o país selecionado
def atualizar_estados(event=None):
    pais = combobox_pais.get()
    combobox_estado['values'] = estados_paises.get(pais, ["Todos os estados"])
    combobox_estado.current(0)

# Função para remover o placeholder quando o usuário começa a digitar
def on_entry_click(event):
    if entry_oq.get() == 'vaga, empresa, função':
        entry_oq.delete(0, "end")  # Limpa o conteúdo do campo
        entry_oq.config(fg='black')

# Função para restaurar o placeholder se o campo estiver vazio
def on_focusout(event):
    if entry_oq.get() == '':
        entry_oq.insert(0, 'vaga, empresa, função')
        entry_oq.config(fg='grey')

# Função para criar a interface
def criar_interface():
    global janela, tree, entry_oq, combobox_estado, combobox_pais, combobox_fonte

    janela = tk.Tk()
    janela.title("Agregador de Vagas")
    janela.state('zoomed')  # Iniciar em fullscreen
    janela.configure(bg="#F7F7F7")

    # Estilo personalizado para botões arredondados
    style = ttk.Style()
    style.configure("Rounded.TButton", font=("Helvetica", 12), background="#004080", foreground="white", padding=10)
    style.map("Rounded.TButton", background=[('active', '#003060')])

    # Título "JOB-X versão 1.0 Alfa"
    titulo_label = tk.Label(janela, text="JOB-X versão 1.0 Alfa", font=("Helvetica", 20, "bold"), bg="#F7F7F7", fg="#004080")
    titulo_label.pack(pady=10)

    # Carregando a imagem de fundo
    imagem_fundo = Image.open(resource_path("image.png"))
    imagem_fundo = imagem_fundo.resize((900, 250), Image.Resampling.LANCZOS)
    imagem_fundo_tk = ImageTk.PhotoImage(imagem_fundo)
    
    label_imagem_fundo = tk.Label(janela, image=imagem_fundo_tk)
    label_imagem_fundo.pack(fill='x')

    # Frame para os campos de busca centralizado
    frame_busca = tk.Frame(janela, bg="#F7F7F7")
    frame_busca.pack(pady=10)

    # Campo de busca para "Vaga" com placeholder
    label_oq = tk.Label(frame_busca, text="Vaga:", font=("Helvetica", 12), bg="#F7F7F7")
    label_oq.grid(row=0, column=0, padx=5, pady=5)
    
    entry_oq = tk.Entry(frame_busca, font=("Helvetica", 12), width=30, fg='grey')
    entry_oq.insert(0, 'vaga, empresa, função')  # Placeholder inicial
    entry_oq.bind('<FocusIn>', on_entry_click)   # Remove placeholder ao clicar
    entry_oq.bind('<FocusOut>', on_focusout)     # Restaura placeholder ao perder o foco
    entry_oq.grid(row=0, column=1, padx=5, pady=5)

    # Combobox para seleção de fonte
    label_fonte = tk.Label(frame_busca, text="Fonte:", font=("Helvetica", 12), bg="#F7F7F7")
    label_fonte.grid(row=1, column=0, padx=5, pady=5)

    combobox_fonte = ttk.Combobox(frame_busca, font=("Helvetica", 12), values=["Adzuna", "Jooble", "Careerjet", "Todos os buscadores"], width=20)
    combobox_fonte.grid(row=1, column=1, padx=5, pady=5)
    combobox_fonte.current(0)  # Definir Adzuna como padrão

    # Combobox para seleção de país
    label_pais = tk.Label(frame_busca, text="País:", font=("Helvetica", 12), bg="#F7F7F7")
    label_pais.grid(row=0, column=2, padx=5, pady=5)

    combobox_pais = ttk.Combobox(frame_busca, font=("Helvetica", 12), values=list(estados_paises.keys()), width=20)
    combobox_pais.grid(row=0, column=3, padx=5, pady=5)
    combobox_pais.current(0)  # Brasil como padrão
    combobox_pais.bind("<<ComboboxSelected>>", atualizar_estados)  # Atualiza estados ao mudar o país

    # Combobox para seleção de estado
    label_estado = tk.Label(frame_busca, text="Estado (se Brasil):", font=("Helvetica", 12), bg="#F7F7F7")
    label_estado.grid(row=0, column=4, padx=5, pady=5)

    combobox_estado = ttk.Combobox(frame_busca, font=("Helvetica", 12), width=20)
    combobox_estado.grid(row=0, column=5, padx=5, pady=5)
    atualizar_estados()  # Carrega os estados ao iniciar

    # Botão de buscar vagas
    botao_buscar = tk.Button(frame_busca, text="Buscar Vagas", bg="#004080", fg="white", font=("Helvetica", 12), relief='flat', bd=0, command=buscar_e_exibir_vagas)
    botao_buscar.grid(row=0, column=6, padx=10, pady=5)

    # Botão para limpar a busca
    botao_limpar = tk.Button(frame_busca, text="Limpar Busca", bg="#004080", fg="white", font=("Helvetica", 12), relief='flat', bd=0, command=limpar_busca)
    botao_limpar.grid(row=0, column=7, padx=10, pady=5)

    # Frame para Treeview com Scrollbar
    frame_lista = tk.Frame(janela)
    frame_lista.pack(fill='both', expand=True, padx=20, pady=20)

    # Barra de rolagem vertical
    scroll_y = tk.Scrollbar(frame_lista, orient='vertical')

    # Treeview para exibir os resultados
    tree = ttk.Treeview(frame_lista, columns=("Título", "Empresa", "Localização", "Salário", "Fonte"), show='headings', height=15, yscrollcommand=scroll_y.set)
    tree.heading("Título", text="Título")
    tree.heading("Empresa", text="Empresa")
    tree.heading("Localização", text="Localização")
    tree.heading("Salário", text="Salário")
    tree.heading("Fonte", text="Fonte")

    tree.column("Título", width=200)
    tree.column("Empresa", width=150)
    tree.column("Localização", width=150)
    tree.column("Salário", width=100)
    tree.column("Fonte", width=100)

    tree.pack(expand=True, fill='both')

    scroll_y.config(command=tree.yview)
    scroll_y.pack(side='right', fill='y')

    tree.bind("<Double-1>", exibir_detalhes)

    # Rodapé com informações do desenvolvedor
    rodape_label = tk.Label(janela, text="Desenvolvedor Rafael Passos (21)965669055", font=("Helvetica", 50), bg="#F7F7F7", fg="gray")
    rodape_label.pack(side="bottom", pady=10)

    janela.mainloop()

# Executa a interface gráfica
criar_interface()
