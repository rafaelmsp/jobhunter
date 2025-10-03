import time
import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from contextlib import contextmanager

@contextmanager
def iniciar_navegador():
    """Gerencia a inicialização e fechamento do navegador."""
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        yield driver
    finally:
        driver.quit()

def buscar_vagas(email, senha, vaga, local):
    """Busca vagas no LinkedIn e retorna uma lista de resultados."""
    print(f"[INFO] Buscando vagas para: {vaga} em {local}")
    
    with iniciar_navegador() as driver:
        try:
            # Acessar página de login
            print("[DEBUG] Acessando página de login do LinkedIn")
            driver.get("https://www.linkedin.com/login")
            
            # Preencher credenciais
            print("[DEBUG] Preenchendo credenciais")
            username_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username")))
            username_field.send_keys(email)
            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys(senha)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            # Verificar CAPTCHA ou erro de login
            print("[DEBUG] Verificando redirecionamento após login")
            if "security-check" in driver.current_url or "challenge" in driver.current_url:
                messagebox.showerror("Erro", "CAPTCHA detectado. Faça login manualmente no navegador.")
                return []
            if "login" in driver.current_url:
                messagebox.showerror("Erro", "Falha no login. Verifique email e senha.")
                return []

            # Esperar redirecionamento para a página inicial
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "global-nav-search")))

            # Navegar para a página de vagas
            print("[DEBUG] Acessando página de vagas")
            driver.get("https://www.linkedin.com/jobs")

            # Preencher campo de cargo
            print("[DEBUG] Localizando campo de cargo")
            try:
                campo_vaga = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "jobs-search-box-keyword-id"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", campo_vaga)
                campo_vaga.click()
                campo_vaga.clear()
                print("[DEBUG] Digitando cargo")
                for char in vaga:
                    campo_vaga.send_keys(char)
                    time.sleep(0.05)
            except (TimeoutException, ElementNotInteractableException) as e:
                messagebox.showerror("Erro", f"Falha ao preencher campo de cargo: {str(e)}")
                return []

            # Preencher campo de localização
            print("[DEBUG] Localizando campo de localização")
            try:
                campo_local = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "jobs-search-box-location-id"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", campo_local)
                campo_local.click()
                campo_local.clear()
                print("[DEBUG] Digitando localização")
                for char in local:
                    campo_local.send_keys(char)
                    time.sleep(0.05)
                campo_local.send_keys(Keys.RETURN)
            except (TimeoutException, ElementNotInteractableException) as e:
                messagebox.showerror("Erro", f"Falha ao preencher campo de localização: {str(e)}")
                return []

            # Esperar resultados
            print("[DEBUG] Aguardando resultados")
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container")))
            
            # Extrair até 10 vagas
            print("[DEBUG] Extraindo vagas")
            cards = driver.find_elements(By.CLASS_NAME, "job-card-container")
            resultados = []
            for card in cards[:10]:
                try:
                    titulo = card.find_element(By.CLASS_NAME, "job-card-list__title").text.strip()
                    empresa = card.find_element(By.CLASS_NAME, "job-card-container__company-name").text.strip()
                    localizacao = card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text.strip()
                    resultados.append((titulo, empresa, localizacao))
                except NoSuchElementException:
                    continue

            print(f"[INFO] Encontradas {len(resultados)} vagas")
            return resultados

        except TimeoutException as e:
            messagebox.showerror("Erro", f"Tempo limite excedido: {str(e)}")
            return []
        except NoSuchElementException as e:
            messagebox.showerror("Erro", f"Elemento não encontrado: {str(e)}")
            return []
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            return []

def criar_interface():
    """Cria a interface gráfica com Tkinter."""
    def buscar():
        email = entrada_email.get()
        senha = entrada_senha.get()
        vaga = entrada_vaga.get()
        local = entrada_local.get()

        if not all([email, senha, vaga, local]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        # Limpar tabela e mostrar indicador de carregamento
        tree.delete(*tree.get_children())
        btn_buscar.config(state="disabled")
        label_status = tk.Label(janela, text="Buscando vagas...", fg="blue")
        label_status.grid(row=2, column=0, columnspan=4, pady=5)
        janela.update()

        # Executar busca
        resultados = buscar_vagas(email, senha, vaga, local)

        # Atualizar interface
        label_status.destroy()
        btn_buscar.config(state="normal")

        if not resultados:
            messagebox.showinfo("Resultado", "Nenhuma vaga encontrada.")
        else:
            for titulo, empresa, localizacao in resultados:
                tree.insert("", tk.END, values=(titulo, empresa, localizacao))

    # Configurar janela principal
    janela = tk.Tk()
    janela.title("LinkedIn JobHunter")
    janela.geometry("900x500")
    janela.configure(bg="#f0f0f0")

    # Frame para credenciais
    frame_login = tk.Frame(janela, bg="#f0f0f0")
    frame_login.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

    tk.Label(frame_login, text="Email:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
    entrada_email = tk.Entry(frame_login, width=30)
    entrada_email.grid(row=0, column=1, padx=5)

    tk.Label(frame_login, text="Senha:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
    entrada_senha = tk.Entry(frame_login, show="*", width=20)
    entrada_senha.grid(row=0, column=3, padx=5)

    # Frame para busca
    frame_busca = tk.Frame(janela, bg="#f0f0f0")
    frame_busca.grid(row=1, column=0, columnspan=4, pady=10, padx=10, sticky="ew")

    tk.Label(frame_busca, text="Cargo:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
    entrada_vaga = tk.Entry(frame_busca, width=30)
    entrada_vaga.grid(row=0, column=1, padx=5)

    tk.Label(frame_busca, text="Local:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
    entrada_local = tk.Entry(frame_busca, width=30)
    entrada_local.grid(row=0, column=3, padx=5)

    # Botão de busca
    btn_buscar = tk.Button(janela, text="Buscar Vagas", command=buscar, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
    btn_buscar.grid(row=2, column=0, columnspan=4, pady=10)

    # Tabela de resultados
    tree = ttk.Treeview(janela, columns=("Título", "Empresa", "Localização"), show="headings", height=15)
    tree.heading("Título", text="Título da Vaga")
    tree.heading("Empresa", text="Empresa")
    tree.heading("Localização", text="Localização")
    tree.column("Título", width=400, stretch=True)
    tree.column("Empresa", width=200, stretch=True)
    tree.column("Localização", width=200, stretch=True)
    tree.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

    # Scrollbar para a tabela
    scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tree.yview)
    scrollbar.grid(row=3, column=4, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Configurar redimensionamento
    janela.grid_rowconfigure(3, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    # Rodapé
    rodape = tk.Label(janela, text="Desenvolvido por Rafael Passos | Atenção: Scraping pode violar os termos do LinkedIn", 
                      font=("Helvetica", 9), bg="#f0f0f0", fg="gray")
    rodape.grid(row=4, column=0, columnspan=4, sticky="se", pady=5)

    janela.mainloop()

if __name__ == "__main__":
    criar_interface()