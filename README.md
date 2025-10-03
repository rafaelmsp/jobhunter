<h1 align="center">🧑‍💻 JobHunter (JOB-X versão 1.0 Alfa)</h1>

<p align="center">
  <img src="image.png" alt="Logo JobHunter" width="600">
</p>

<p align="center">
  Um <b>agregador de vagas de emprego</b> desenvolvido em <b>Python + Tkinter</b>, 
  que consulta a API do <b>Adzuna</b> para exibir oportunidades de trabalho 
  em uma interface gráfica moderna e intuitiva.
</p>

---

<h2>🚀 Funcionalidades</h2>
<ul>
  <li>🔎 Busca de vagas por palavra-chave (cargo, função, empresa).</li>
  <li>🌎 Seleção de país e estado (Brasil, EUA e Canadá).</li>
  <li>💼 Integração com a <b>API Adzuna</b>.</li>
  <li>📊 Exibição dos resultados em lista (Treeview) com:
    <ul>
      <li>Título</li>
      <li>Empresa</li>
      <li>Localização</li>
      <li>Faixa salarial (formato brasileiro 🇧🇷)</li>
      <li>Fonte</li>
    </ul>
  </li>
  <li>🔗 Acesso direto ao link de candidatura (duplo clique na vaga).</li>
  <li>🧹 Botão para limpar filtros e resultados.</li>
  <li>👨‍💻 Rodapé com informações do desenvolvedor.</li>
</ul>

---

<h2>🛠️ Tecnologias Utilizadas</h2>
<ul>
  <li><a href="https://www.python.org/">Python 3.12+</a></li>
  <li><a href="https://docs.python.org/3/library/tkinter.html">Tkinter</a> (interface gráfica)</li>
  <li><a href="https://pillow.readthedocs.io/">PIL (Pillow)</a> (tratamento de imagens)</li>
  <li><a href="https://docs.python-requests.org/">Requests</a> (requisições HTTP)</li>
  <li><a href="https://developer.adzuna.com/">Adzuna API</a> (busca de vagas)</li>
  <li><a href="https://docs.python.org/3/library/locale.html">Locale</a> (formatação de moeda brasileira)</li>
</ul>

---

<h2>📦 Instalação</h2>

```bash
# Clone o repositório
git clone https://github.com/rafaelmsp/jobhunter.git
cd jobhunter

# Crie e ative um ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
 ```
<h2>▶️ Como Executar</h2>
python jobhunter.py

<h2>📷 Captura de Tela</h2> <p align="center"> <img src="screen.png" alt="Tela JobHunter" width="800"> </p>
<h2>🔮 Futuras Implementações</h2> <ul> <li>Integração com <b>Jooble</b> e <b>Careerjet</b>.</li> <li>Filtro por <b>salário mínimo/máximo</b>.</li> <li>Exportação dos resultados em <b>CSV/Excel</b>.</li> <li>Versão executável para Windows (PyInstaller).</li> </ul>
<h2>👨‍💻 Desenvolvedor</h2> <p> <b>Rafael Moraes da Silva Passos</b><br> 📍 Rio de Janeiro - Brasil<br> 📱 (21) 96566-9055<br> 🔗 <a href="https://www.linkedin.com/in/rafael-passos-023648144/">LinkedIn</a><br> 🔗 <a href="https://github.com/rafaelmsp">GitHub</a> </p>
<h2>📜 Licença</h2> <p> Este projeto é distribuído sob a licença <b>MIT</b>.<br> Você pode utilizá-lo, modificá-lo e distribuí-lo livremente, desde que mantenha os devidos créditos. </p>
