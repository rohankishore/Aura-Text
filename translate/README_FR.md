<!-- LOGO DU PROJET -->
<br />
<div align="center">
  
  ![aura text](https://github.com/user-attachments/assets/ebc56c38-c7c3-499a-b68b-28cfcdd4ab6d)
  
  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/rohankishore/Aura-Text/total.svg"/>
  </a>  <a href='https://ko-fi.com/V7V7QZ7GS' target='_blank'><img height='10' style='border:0px;height:22px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=3' border='1' alt='Buy Me a Coffee at ko-fi.com' /></a>
      
  <p align="center">
    Un IDE entièrement créé avec Python
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/wiki"><strong>Explorer la documentation »</strong></a>   
    <br />
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/issues">Signaler un bug</a>
    ·   
    <a href="https://github.com/rohankishore/Aura-Text/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=">Demander une fonctionnalité</a>
    
  *Aura Text est également porté sur macOS par [matthewyang204](https://github.com/matthewyang204). Voir le dépôt [ici](https://github.com/matthewyang204/Aura-Text-Mac)*
  
  </p>
</div>    
<br>
<hr>
<!-- TABLE DES MATIÈRES -->
<details>
  <summary>Table des matières</summary>
  <ol>
    <li>
      <a href="#-à-propos-du-projet">À propos du projet</a>
    </li>
    <li>
      <a href="#-pour-commencer">Pour commencer</a>
      <ul>
        <li><a href="#prérequis">Prérequis</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#développement">Développement</a></li>
    <li><a href="#feuille-de-route">Feuille de route</a></li>
    <li><a href="#-contribuer">Contribuer</a></li>
    <li><a href="#-licence">Licence</a></li>
    <li><a href="#-contact">Contact</a></li>
  </ol>
</details>
<!-- SÉLECTEUR DE LANGUE -->
<details>
  <summary>Voir le README en :</summary>
  <ol>
    <li>    
      <a href="README_HN.md">हिन्दी 🇮🇳</a>
    </li>
    <li>
      <a href="README_DE.md">Deutsch</a>
    </li>
    <li><a href="README_ES.md">Español</a></li>
    <li><a href="README_TA.md">தமிழ் 🇮🇳</a></li>
    <li><a><strong>Français</strong></a></li>
    <li><a href="README_JA.md">日本語</a></li>
    <li><a href="README_PT.md">Português</a></li>
    <li><a href="README_RU.md">Русский</a></li>
    <li><a href="ZH-CN/README_ZH-CN.md">简体中文</a></li>
  </ol>
</details>
<br>
<hr>
<!-- À PROPOS DU PROJET -->
## 📖 À propos du projet

<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/17399995-7032-4d90-957e-5cef278ceb6e" />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/7eb477ed-1469-4303-bce2-8124efcd8114" />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/c65eace4-8cc5-4390-bc9c-97d17c31c17c" />

Aura Text est un excellent éditeur de texte/code qui offre une large gamme d'outils essentiels. Construit avec PyQt6 et Python, il exploite la puissance et la flexibilité de ces technologies.
Avec Aura Text, les utilisateurs peuvent accéder à un environnement d'édition polyvalent et puissant. Que vous travailliez sur un petit script ou un projet complexe, Aura Text vous équipe de toutes les fonctionnalités nécessaires pour rationaliser votre flux de travail. De la coloration syntaxique et de l'autocomplétion à l'indentation intelligente et au terminal avancé, Aura Text assure que votre expérience de codage est efficace et agréable tout en étant extrêmement légère sur votre PC.

<br>

***Les points forts d'Aura Text sont :***
- Éditer des fichiers
- Prise en charge jusqu'à 30 langages
- Autocomplétion
- Linting de code pour Python (BÊTA)
- Git Clone, Commit et Push avec rebase interactif et graphes
- Palette de commandes pour l'exécution rapide des tâches
- Barres de titre personnalisées
- Éditeur Markdown à volets divisés
- Terminal avec historique
- Console Python
- Support de plugins
- Thématisation étendue incluant le support Material Theming
- Extrêmement personnalisable
  
<!-- POUR COMMENCER -->
## 🏃 Pour commencer

Configurons Aura Text sur votre PC !

### Prérequis
- Windows 10 x64 ou ultérieur
- Python 3.9 ou ultérieur
- L'installation Python est bootstrappée avec pip
- (Recommandé) Un nouveau venv créé avec `python -m venv venv` et activé avec `venv\Scripts\activate`
- Le contenu de `requirements.txt` installé via `pip install -r requirements.txt`
- (Si vous créez un installateur) Inno Setup 6.4.3 ou ultérieur
  
### Installation

Vous pouvez télécharger un installateur précompilé depuis les Releases ou en créer un vous-même.

#### Créer l'installateur

1. Cloner le dépôt ou télécharger une archive
2. Installer tous les prérequis
3. `python build.py` pour compiler le programme d'abord
4. Ouvrir le script Inno Setup `.iss` et le compiler via Ctrl+F9 ou `Build > Compile` — l'installateur se trouve dans le dossier `Output`

##### Utiliser l'installateur

Il suffit d'exécuter le fichier `.exe`.

### Tests

Pour ceux qui souhaitent simplement exécuter sans installation à des fins de test.
Utilisez `pythonw main.py` pour exécuter sans logs dans le terminal, ou `python main.py` pour déboguer.

<br>

## 🧑🏻‍💻 Développement 

![Alt](https://repobeats.axiom.co/api/embed/c478f91eea3690c7415f891646a2a15a62b4fb20.svg "Repobeats analytics image")
<br>

## 🛣️ Feuille de route

- <strike> Créer une barre d'état en bas avec des fonctionnalités similaires à PyCharm ou d'autres IDEs </strike>
- <strike> Thématisation personnalisée </strike>
- <strike> Émulation de touches </strike>
- <strike> Édition divisée </strike>
- Gestionnaire de projet
- <strike> Linting de code Python </strike>
<b> et bien plus encore... </b>

<!-- CONTRIBUER -->
## 🛂 Contribuer

Les contributions font de la communauté open-source un endroit incroyable pour apprendre, s'inspirer et créer. Toute contribution que vous faites est **grandement appréciée**.
Si vous avez une suggestion qui améliorerait cela, veuillez forker le dépôt et créer une pull request. Vous pouvez également ouvrir simplement un problème avec le tag "enhancement".
N'oubliez pas de donner une étoile au projet ! Merci encore !

1. Forker le projet
2. Créer votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committer vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pousser vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Contributeurs
<a href="https://github.com/rohankishore/Aura-Text/graphs/contributors">
  <img class="dark-light" src="https://contrib.rocks/image?repo=rohankishore/Aura-Text&anon=0&columns=25&max=100&r=true" />
</a>

<br>

<!-- LICENCE -->
## 🪪 Licence

Distribué sous la licence MIT. Voir `LICENSE.txt` pour plus d'informations.

## Parrainage GitAds
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=rohankishore/aura-text@github)](https://gitads.dev/v1/ad-track?source=rohankishore/aura-text@github)
