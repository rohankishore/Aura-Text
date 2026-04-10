<!-- LOGO DO PROJETO -->
<br />
<div align="center">
  
  ![aura text](https://github.com/user-attachments/assets/ebc56c38-c7c3-499a-b68b-28cfcdd4ab6d)
  
  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/rohankishore/Aura-Text/total.svg"/>
  </a>  <a href='https://ko-fi.com/V7V7QZ7GS' target='_blank'><img height='10' style='border:0px;height:22px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=3' border='1' alt='Buy Me a Coffee at ko-fi.com' /></a>
      
  <p align="center">
    Uma IDE feita inteiramente com Python
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/wiki"><strong>Explorar a documentação »</strong></a>   
    <br />
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/issues">Reportar Bug</a>
    ·   
    <a href="https://github.com/rohankishore/Aura-Text/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=">Solicitar Funcionalidade</a>
    
  *Aura Text também está sendo portado para macOS por [matthewyang204](https://github.com/matthewyang204). Veja o repositório [aqui](https://github.com/matthewyang204/Aura-Text-Mac)*
  
  </p>
</div>    
<br>
<hr>
<!-- ÍNDICE -->
<details>
  <summary>Índice</summary>
  <ol>
    <li>
      <a href="#-sobre-o-projeto">Sobre o Projeto</a>
    </li>
    <li>
      <a href="#-primeiros-passos">Primeiros Passos</a>
      <ul>
        <li><a href="#pré-requisitos">Pré-requisitos</a></li>
        <li><a href="#instalação">Instalação</a></li>
      </ul>
    </li>
    <li><a href="#desenvolvimento">Desenvolvimento</a></li>
    <li><a href="#roteiro">Roteiro</a></li>
    <li><a href="#-contribuindo">Contribuindo</a></li>
    <li><a href="#-licença">Licença</a></li>
    <li><a href="#-contato">Contato</a></li>
  </ol>
</details>
<!-- SELETOR DE IDIOMA -->
<details>
  <summary>Ver o README em:</summary>
  <ol>
    <li>    
      <a href="README_HN.md">हिन्दी 🇮🇳</a>
    </li>
    <li>
      <a href="README_DE.md">Deutsch</a>
    </li>
    <li><a href="README_ES.md">Español</a></li>
    <li><a href="README_TA.md">தமிழ் 🇮🇳</a></li>
    <li><a href="README_FR.md">Français</a></li>
    <li><a href="README_JA.md">日本語</a></li>
    <li><a><strong>Português</strong></a></li>
    <li><a href="README_RU.md">Русский</a></li>
    <li><a href="ZH-CN/README_ZH-CN.md">简体中文</a></li>
  </ol>
</details>
<br>
<hr>
<!-- SOBRE O PROJETO -->
## 📖 Sobre o Projeto

<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/17399995-7032-4d90-957e-5cef278ceb6e" />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/7eb477ed-1469-4303-bce2-8124efcd8114" />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/c65eace4-8cc5-4390-bc9c-97d17c31c17c" />

Aura Text é um excelente editor de texto/código que oferece uma ampla gama de ferramentas essenciais. Construído com PyQt6 e Python, aproveita o poder e a flexibilidade dessas tecnologias.
Com Aura Text, os usuários podem acessar um ambiente de edição versátil e poderoso. Seja trabalhando em um pequeno script ou em um projeto complexo, Aura Text fornece todos os recursos necessários para otimizar seu fluxo de trabalho. Desde realce de sintaxe e autocompletar código até indentação inteligente e terminal avançado, Aura Text garante que sua experiência de codificação seja eficiente e agradável, sendo extremamente leve no seu PC.

<br>

***Os principais destaques do Aura Text são:***
- Editar arquivos
- Suporte a até 30 linguagens
- Autocompletar
- Linting de código para Python (BETA)
- Git Clone, Commit e Push com rebase interativo e gráficos
- Paleta de comandos para execução rápida de tarefas
- Barras de título personalizadas
- Editor Markdown com painel dividido
- Terminal com histórico
- Console Python
- Suporte a plugins
- Temas extensivos incluindo suporte ao Material Theming
- Extremamente personalizável
  
<!-- PRIMEIROS PASSOS -->
## 🏃 Primeiros Passos

Vamos configurar o Aura Text no seu PC!

### Pré-requisitos
- Windows 10 x64 ou posterior
- Python 3.9 ou posterior
- A instalação do Python é bootstrapped com pip
- (Recomendado) Um venv novo criado com `python -m venv venv` e ativado com `venv\Scripts\activate`
- O conteúdo de `requirements.txt` instalado via `pip install -r requirements.txt`
- (Se estiver criando um instalador) Inno Setup 6.4.3 ou posterior
  
### Instalação

Você pode baixar um instalador pré-compilado dos Releases ou criar um você mesmo.

#### Construindo o instalador

1. Clone o repositório ou baixe um tarball
2. Instale todos os pré-requisitos
3. `python build.py` para compilar o programa primeiro
4. Abra o script Inno Setup `.iss` e compile via Ctrl+F9 ou `Build > Compile` — o instalador pode ser encontrado na pasta `Output`

##### Usando o instalador

Apenas execute o arquivo `.exe`.

### Testes

Para quem deseja executar sem instalação para fins de teste.
Use `pythonw main.py` para executar sem logs no terminal, ou `python main.py` para depuração.

<br>

## 🧑🏻‍💻 Desenvolvimento 

![Alt](https://repobeats.axiom.co/api/embed/c478f91eea3690c7415f891646a2a15a62b4fb20.svg "Repobeats analytics image")
<br>

## 🛣️ Roteiro

- <strike> Criar uma barra de status na parte inferior com recursos semelhantes ao PyCharm ou outros IDEs </strike>
- <strike> Temas personalizados </strike>
- <strike> Emulação de teclas </strike>
- <strike> Edição dividida </strike>
- Gerenciador de projetos
- <strike> Linting de código Python </strike>
<b> e muito mais... </b>

<!-- CONTRIBUINDO -->
## 🛂 Contribuindo

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer é **muito apreciada**.
Se você tem uma sugestão que tornaria isso melhor, por favor faça um fork do repositório e crie um pull request. Você também pode simplesmente abrir um issue com a tag "enhancement".
Não se esqueça de dar uma estrela ao projeto! Obrigado novamente!

1. Faça um fork do projeto
2. Crie sua branch de funcionalidade (`git checkout -b feature/AmazingFeature`)
3. Commite suas alterações (`git commit -m 'Add some AmazingFeature'`)
4. Envie para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Contribuidores
<a href="https://github.com/rohankishore/Aura-Text/graphs/contributors">
  <img class="dark-light" src="https://contrib.rocks/image?repo=rohankishore/Aura-Text&anon=0&columns=25&max=100&r=true" />
</a>

<br>

<!-- LICENÇA -->
## 🪪 Licença

Distribuído sob a Licença MIT. Consulte `LICENSE.txt` para mais informações.

## Patrocínio GitAds
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=rohankishore/aura-text@github)](https://gitads.dev/v1/ad-track?source=rohankishore/aura-text@github)
