<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h1 align="center"> Aura Text ⌨️ </h1>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/rohankishore/Aura-Text/total.svg"/>
  </a>  <a href='https://ko-fi.com/V7V7QZ7GS' target='_blank'><img height='10' style='border:0px;height:22px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=3' border='1' alt='Buy Me a Coffee at ko-fi.com' /></a>
  
  ![AURA TEXT](https://github.com/rohankishore/Aura-Text/assets/109947257/9b59cf71-e8f7-4244-be38-0ab647d8ded8)
    
  <p align="center">
    一个完全用Python制作的集成开发环境
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/wiki"><strong>探索文档 »</strong></a>   
    <br />
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/issues">提交议题</a>
    ·   
    <a href="https://github.com/rohankishore/Aura-Text/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=">功能请求</a>
  </p>
</div>    

<!-- TABLE OF CONTENTS -->
<details>
  <summary>目录</summary>
  <ol>
    <li>
      <a href="#-关于项目">关于项目</a>
    </li>
    <li>
      <a href="#-快速开始">快速开始</a>
      <ul>
        <li><a href="#先决条件">先决条件</a></li>
        <li><a href="#安装">安装</a></li>
        <ul>
        <li><a href="#使用Nuitka">使用Nuitka</a></li>
        <li><a href="#作为Python文件">作为Python文件</a></li>
      </ul>
      </ul>
    </li>
    <li><a href="#开发">开发</a></li>
    <li><a href="#路线图">路线图</a></li>
    <li><a href="#-贡献">贡献</a></li>
    <li><a href="#-许可证">许可证</a></li>
    <li><a href="#-联系方式">联系方式</a></li>
  </ol>
</details>

<!-- LANGUAGE SWITCHER -->
<details>
  <summary>查看其他语言的README：</summary>
  <ol>
    <li>    
      <a href="README_HN.md">Hindi 🇮🇳</a>
    </li>
    <li>
      <a href="README_DE.md">German</a>
    </li>
    <li><a href="README_ES.md">Español</a></li>
    <li><a href="#-contributing">Russian</a></li>
    <li><a><strong>简体中文</strong></a></li>
  </ol>
</details>

<br>

<!-- ABOUT THE PROJECT -->
## 📖 关于项目

![image](https://github.com/rohankishore/Aura-Text/assets/109947257/b75da351-6c2b-43a3-a72e-eb7b861fff27)

![image](https://github.com/rohankishore/Aura-Text/assets/109947257/febc6916-10a6-4919-9838-0eea2c103269)

Aura Text 是一个优秀的文本/代码编辑器，提供了各种必备工具。由 PyQt6 和 Python 构建，利用了这些技术的强大功能和灵活性。

使用 Aura Text，用户可以访问一个多功能且强大的编辑环境。无论是处理小脚本还是复杂项目，Aura Text 都为您提供所有必要的功能，以简化您的工作流程。从语法高亮和代码补全到智能缩进和高级终端，Aura Text 确保您的编码体验既高效又愉快，同时对您的计算机负担极小。

<br>

***Aura Text 的主要亮点是：***
- 编辑文件
- 支持多达30种语言
- 自动补全
- 自定义标题栏
- 拆分窗格 Markdown 编辑器
- 带历史记录的终端
- Python 控制台
- 插件支持
- 广泛的主题支持，包括 Material 主题支持
- 极高的可定制性

<!-- GETTING STARTED -->
## 🏃 快速开始

让我们在您的 PC 上安装 Aura Text！

### 先决条件

在终端中运行以下命令一次性安装依赖项：
  ```sh
  pip install -r requirements.txt
  ```

### 安装

#### 使用 Nuitka

_以下是使用 Nuitka 构建 Aura Text 的示例_

- 下载 / 克隆此仓库
- 将 `AuraText` 文件夹从 `LocalAppData` 文件夹移动到 `AppData/Local` 文件夹。
- 安装 Nuitka (`python -m pip install nuitka`)
- `python -m nuitka --windows-disable-console .\main.py`

#### 🐍 作为 Python 文件

- 下载 / 克隆此仓库
- 将 `AuraText` 文件夹从 `LocalAppData` 文件夹移动到 `AppData/Local` 文件夹。
- `python -m main.py`

<br>

## 🧑🏻‍💻 开发 

![Alt](https://repobeats.axiom.co/api/embed/c478f91eea3690c7415f891646a2a15a62b4fb20.svg "Repobeats analytics image")

<br>

## 🛣️ 路线图

- 在底部制作一个具有类似 PyCharm 或其他 IDE 功能的状态栏（只读切换，面包屑等）
- <strike>自定义主题</strike>
- <strike>键盘模拟</strike>
- 拆分编辑
- <strike>Python 代码静态分析</strike>

<b> 以及更多...... </b>

<!-- CONTRIBUTING -->
## 🛂 贡献

贡献是使开源社区成为一个令人惊叹的学习、启发和创造的地方。您所做的任何贡献都是**非常感谢**的。

如果您有建议可以改进此项目，请复刻 (fork) 此仓库并创建一个拉取请求(pull request)。您也可以直接打开一个带有“增强”(enhancement)标签的议题。
别忘了给项目加星！再次感谢！

1. 复刻(Fork)此仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个拉取请求(Pull Request)

### 贡献者

<a href="https://github.com/rohankishore/Aura-Text/graphs/contributors">
  <img class="dark-light" src="https://contrib.rocks/image?repo=rohankishore/Aura-Text&anon=0&columns=25&max=100&r=true" />
</a>

<b>

<!-- LICENSE -->
## 🪪 许可证

根据MIT许可证分发。有关详细信息，请参见 `LICENSE.txt`。