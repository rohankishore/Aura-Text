<!-- PROJECT LOGO -->
<br />
<div align="center">

  ![aura text](https://github.com/user-attachments/assets/ebc56c38-c7c3-499a-b68b-28cfcdd4ab6d)


  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/rohankishore/Aura-Text/total.svg"/>
  </a>  <a href='https://ko-fi.com/V7V7QZ7GS' target='_blank'><img height='10' style='border:0px;height:22px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=3' border='1' alt='Buy Me a Coffee at ko-fi.com' /></a>
      
  <p align="center">
    An IDE made entirely with Python
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/wiki"><strong>Explore the docs »</strong></a>   
    <br />
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/issues">Report Bug</a>
    ·   
    <a href="https://github.com/rohankishore/Aura-Text/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=">Request Feature</a>

  *Aura Text is also being ported to macOS by [matthewyang204](https://github.com/matthewyang204). Take a look at the repository [here](https://github.com/matthewyang204/Aura-Text-Mac)*
  </p>
</div>    

<br>
<hr>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#-about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#-getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <ul>
        <li><a href="#with-nuitka">With Nuitka</a></li>
        <li><a href="#-as-a-python-file">As a Python File</a></li>
      </ul>
      </ul>
    </li>
    <li><a href="#development">Development</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#-contributing">Contributing</a></li>
    <li><a href="#-license">License</a></li>
    <li><a href="#-contact">Contact</a></li>
  </ol>
</details>

<!-- LANGUAGE SWITCHER -->
<details>
  <summary>View the README In:</summary>
  <ol>
    <li>    
      <a href="translate/README_HN.md">Hindi 🇮🇳</a>
    </li>
    <li>
      <a href="translate/README_DE.md">German</a>
    </li>
    <li><a href="translate/README_ES.md">Español</a></li>
    <li><a href="#-contributing">Russian</a></li>
    <li><a href="translate/ZH-CN/README_ZH-CN.md">简体中文</a></li>
  </ol>
</details>

<br>
<hr>

<!-- ABOUT THE PROJECT -->
## 📖 About The Project

<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/62ba55aa-3add-4f71-bb42-2ecb0f1a0bea" />

![image](https://github.com/user-attachments/assets/fca92d3e-4218-4550-96ca-dfa85dbc27dc)

Aura Text is an excellent text/code editor that offers a wide array of essential tools. Built with PyQt6 and Python, it harnesses the power and flexibility of these technologies.

With Aura Text, users can access a versatile and powerful editing environment. Whether working on a small script or a complex project, Aura Text equips you with all the necessary features to streamline your workflow. From syntax highlighting and code completion to smart indentation and advanced terminal, Aura Text ensures that your coding experience is efficient and enjoyable while being extremely light on your PC.

<br>


***The main highlights of Aura Text are:***
- Edit files (duh)
- Support up to 30 languages
- Autocompletion
- Git Clone, Commit and Push with interactive rebase and graphs
- Custom title bars
- Split pane Markdown editor
- Terminal with history
- Python Console
- Plugin support
- Extensive theming including Material Theming support
- Extremely customisable
  
<!-- GETTING STARTED -->
## 🏃 Getting Started

Let's set up Aura Text on your PC!

### Prerequisites
- Windows 10 x64 or later
- Python 3.9 or later
- Python installation is bootstrapped with pip
- (Recommended) A fresh venv created with `python -m venv venv` and activated with `venv\Scripts\activate`
- The contents of `requirements.txt` installed via `pip install -r requirements.txt`
- (If building an installer) Inno Setup 6.4.3 or later

### Installation
You can download a prebuilt installer from the Releases or build one yourself. If using prebuilt installers, just skip to the use section.

#### Building the installer
1. Clone the repo or download a tarball
2. Install all prerequisites
3. `python build.py` to compile the program first
4. Open up the `.iss` Inno Setup script and compile it via Ctrl+F9 or `Build > Compile` - installer can be found in `Output` folder

##### Using the installer
Just run the `.exe` file, duh.

### Testing
This is for people who solely just want to run without installation for mostly testing purposes.

We need the prerequisites above. After getting them, you can run the program with `pythonw main.py` to run it without flooding your terminal with logging, or you can just run with `python main.py` to troubleshoot errors and debug it.

<br>

## 🧑🏻‍💻 Development 

![Alt](https://repobeats.axiom.co/api/embed/c478f91eea3690c7415f891646a2a15a62b4fb20.svg "Repobeats analytics image")


<br>

## 🛣️ Roadmap

- <strike> Make a status bar at the bottom with features similar to PyCharm or other IDEs (Read-only toggle, breadcrumbs, etc) </strike>
- <strike> Custom Theming </strike>
-  <strike> Key Emulation </strike>
- Split Editing
- Project Manager
- <strike> Python Code Linting </strike>

<b> and much much more... </b>


<b>

<!-- CONTRIBUTING -->
## 🛂 Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contributors

<a href="https://github.com/rohankishore/Aura-Text/graphs/contributors">
  <img class="dark-light" src="https://contrib.rocks/image?repo=rohankishore/Aura-Text&anon=0&columns=25&max=100&r=true" />
</a>

<b>

<!-- GitAds-Verify: WQAFQASC2KGFLIXDWYMOWLYFQMBXX9GJ -->

<!-- LICENSE -->
## 🪪 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

