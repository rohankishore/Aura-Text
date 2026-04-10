<!-- プロジェクトロゴ -->
<br />
<div align="center">
  
  ![aura text](https://github.com/user-attachments/assets/ebc56c38-c7c3-499a-b68b-28cfcdd4ab6d)
  
  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/rohankishore/Aura-Text/total.svg"/>
  </a>  <a href='https://ko-fi.com/V7V7QZ7GS' target='_blank'><img height='10' style='border:0px;height:22px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=3' border='1' alt='Buy Me a Coffee at ko-fi.com' /></a>
      
  <p align="center">
    Pythonで完全に作られたIDE
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/wiki"><strong>ドキュメントを見る »</strong></a>   
    <br />
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/issues">バグを報告する</a>
    ·   
    <a href="https://github.com/rohankishore/Aura-Text/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=">機能をリクエストする</a>
    
  *Aura TextはmacOSに[matthewyang204](https://github.com/matthewyang204)によってポートされています。リポジトリは[こちら](https://github.com/matthewyang204/Aura-Text-Mac)*
  
  </p>
</div>    
<br>
<hr>
<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#-プロジェクトについて">プロジェクトについて</a>
    </li>
    <li>
      <a href="#-始め方">始め方</a>
      <ul>
        <li><a href="#前提条件">前提条件</a></li>
        <li><a href="#インストール">インストール</a></li>
      </ul>
    </li>
    <li><a href="#開発">開発</a></li>
    <li><a href="#ロードマップ">ロードマップ</a></li>
    <li><a href="#-貢献">貢献</a></li>
    <li><a href="#-ライセンス">ライセンス</a></li>
    <li><a href="#-連絡先">連絡先</a></li>
  </ol>
</details>
<!-- 言語切替 -->
<details>
  <summary>READMEを表示する言語:</summary>
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
    <li><a><strong>日本語</strong></a></li>
    <li><a href="README_PT.md">Português</a></li>
    <li><a href="README_RU.md">Русский</a></li>
    <li><a href="ZH-CN/README_ZH-CN.md">简体中文</a></li>
  </ol>
</details>
<br>
<hr>
<!-- プロジェクトについて -->
## 📖 プロジェクトについて

<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/17399995-7032-4d90-957e-5cef278ceb6e" />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/7eb477ed-1469-4303-bce2-8124efcd8114" />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/c65eace4-8cc5-4390-bc9c-97d17c31c17c" />

Aura Textは、幅広い必須ツールを提供する優れたテキスト/コードエディタです。PyQt6とPythonで構築され、これらの技術のパワーと柔軟性を活用しています。
Aura Textを使用すると、ユーザーは多用途で強力な編集環境にアクセスできます。小さなスクリプトから複雑なプロジェクトまで、Aura Textはワークフローを効率化するために必要なすべての機能を提供します。シンタックスハイライトやコード補完から、スマートインデントや高度なターミナルまで、Aura TextはPCへの負荷を最小限に抑えながら、効率的で楽しいコーディング体験を保証します。

<br>

***Aura Textの主な特徴:***
- ファイルの編集
- 30言語以上のサポート
- 自動補完
- Python用コードリンティング（ベータ版）
- インタラクティブなリベースとグラフを使ったGit Clone、Commit、Push
- タスクを素早く実行するためのコマンドパレット
- カスタムタイトルバー
- 分割ペインMarkdownエディタ
- 履歴付きターミナル
- Pythonコンソール
- プラグインサポート
- Material Themingサポートを含む広範なテーマ
- 極めてカスタマイズ可能
  
<!-- 始め方 -->
## 🏃 始め方

PCにAura Textをセットアップしましょう！

### 前提条件
- Windows 10 x64以降
- Python 3.9以降
- PythonインストールはpipでBootstrapされています
- （推奨）`python -m venv venv`で新しいvenvを作成し、`venv\Scripts\activate`で有効化
- `pip install -r requirements.txt`で`requirements.txt`の内容をインストール
- （インストーラーを作成する場合）Inno Setup 6.4.3以降
  
### インストール

リリースからビルド済みインストーラーをダウンロードするか、自分でビルドできます。

#### インストーラーのビルド

1. リポジトリをクローンまたはtarballをダウンロード
2. すべての前提条件をインストール
3. `python build.py`でプログラムをコンパイル
4. `.iss` Inno Setupスクリプトを開き、Ctrl+F9または`Build > Compile`でコンパイル — インストーラーは`Output`フォルダにあります

##### インストーラーの使用

`.exe`ファイルを実行するだけです。

### テスト

主にテスト目的でインストールなしで実行したい人向けです。
`pythonw main.py`でログなしで実行するか、`python main.py`でデバッグできます。

<br>

## 🧑🏻‍💻 開発 

![Alt](https://repobeats.axiom.co/api/embed/c478f91eea3690c7415f891646a2a15a62b4fb20.svg "Repobeats analytics image")
<br>

## 🛣️ ロードマップ

- <strike> PyCharmのような機能を持つ下部ステータスバーの作成 </strike>
- <strike> カスタムテーマ </strike>
- <strike> キーエミュレーション </strike>
- <strike> 分割編集 </strike>
- プロジェクトマネージャー
- <strike> Pythonコードリンティング </strike>
<b> さらに多くの機能... </b>

<!-- 貢献 -->
## 🛂 貢献

コントリビューションはオープンソースコミュニティを学び、インスパイアし、創造するための素晴らしい場所にします。あなたの貢献は**大変ありがたい**です。
改善の提案がある場合は、リポジトリをフォークしてプルリクエストを作成してください。「enhancement」タグを付けてイシューを開くこともできます。
プロジェクトにスターを付けることを忘れずに！ありがとうございます！

1. プロジェクトをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/AmazingFeature`）
3. 変更をコミット（`git commit -m 'Add some AmazingFeature'`）
4. ブランチにプッシュ（`git push origin feature/AmazingFeature`）
5. プルリクエストを開く

### コントリビューター
<a href="https://github.com/rohankishore/Aura-Text/graphs/contributors">
  <img class="dark-light" src="https://contrib.rocks/image?repo=rohankishore/Aura-Text&anon=0&columns=25&max=100&r=true" />
</a>

<br>

<!-- ライセンス -->
## 🪪 ライセンス

MITライセンスの下で配布されています。詳細は`LICENSE.txt`を参照してください。

## GitAdsスポンサーシップ
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=rohankishore/aura-text@github)](https://gitads.dev/v1/ad-track?source=rohankishore/aura-text@github)
