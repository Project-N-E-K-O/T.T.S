<div align="center">

![ロゴ](https://raw.githubusercontent.com/Project-N-E-K-O/N.E.K.O/main/assets/neko_logo.jpg)

[中文](https://github.com/Project-N-E-K-O/N.E.K.O/blob/main/README.MD) | [English](README_en.md)

# Project N.E.K.O. - Talking Twin Simulator (T.T.S.) :kissing_cat: <br>**T.T.S.、仮想キャラクターであなたの物語を語る。**

> **動画制作者向けの仮想キャラクターナレーションソフトウェア。**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Project-N-E-K-O/N.E.K.O/blob/main/LICENSE)
[![QQグループ](https://custom-icon-badges.demolab.com/badge/QQ群-1048307485-00BFFF?style=flat&logo=tencent-qq)](https://qm.qq.com/q/1048307485)

</div>

---

# Talking Twin Simulator (T.T.S.)

本プロジェクト（T.T.S.）は猫娘計画（Project N.E.K.O.）の派生プロジェクトです。仮想キャラクターナレーションシーンに特化しています。ユーザーがテキストを入力すると、仮想キャラクターがLLMを介さずに直接そのテキストを読み上げます。

---

## クイックスタート

```bash
uv sync
python main_server.py
```

起動後、`http://localhost:48911`からウェブインターフェースにアクセスできます。

## 上級使用

#### API Keyの設定

追加機能を得るために独自のAPIを設定したい場合、サードパーティのAIサービスを設定できます（コアAPIは**Realtime APIに対応している必要があります**）。本プロジェクトは現在 *StepFun* または *Alibaba Cloud* の使用を推奨しています。`http://localhost:48911/api_key`にアクセスして、Web画面から直接設定できます。

> *Alibaba Cloud API*の取得：Alibaba CloudのBailian Platform[公式サイト](https://bailian.console.aliyun.com/)でアカウント登録します。新規ユーザーは実名認証後に大量の無料クレジットを取得できます。登録完了後、[コンソール](https://bailian.console.aliyun.com/api-key?tab=model#/api-key)にアクセスしてAPI Keyを取得してください。

#### キャラクター設定の変更

- ウェブ版で`http://localhost:48911/chara_manager`にアクセスするとキャラクター編集ページに入れます。

- 上級設定には主に**Live2Dモデル設定(live2d)**と**音声設定(voice_id)**が含まれます。**Live2Dモデル**を変更したい場合は、まずモデルディレクトリを本プロジェクトの`static`フォルダにコピーしてください。上級設定からLive2Dモデル管理画面に入り、モデルを切り替え、ドラッグとマウスホイールでモデルの位置とサイズを調整できます。**キャラクター音声**を変更したい場合は、約5秒の連続したクリーンな音声録音を準備してください。上級設定から音声設定ページに入り、録音をアップロードするとカスタム音声の設定が完了します。

#### 記憶整理

- `http://localhost:48911/memory_browser`にアクセスすると、最近の記憶と要約を閲覧および校正でき、モデルの繰り返しや認知エラーなどの問題をある程度緩和できます。

# プロジェクト詳細

**プロジェクトアーキテクチャ**

```
T.T.S/
├── 📁 config/                   # ⚙️ 設定管理モジュール
│   ├── api_providers.json       # APIプロバイダー設定
│   ├── prompts_chara.py         # キャラクタープロンプト
│   └── prompts_sys.py           # システムプロンプト
├── 📁 main_logic/              # 🔧 コアモジュール
│   ├── core.py                  # コア対話モジュール
│   ├── cross_server.py         # クロスサーバー通信
│   ├── omni_realtime_client.py  # リアルタイムAPIクライアント（Realtime API）
│   ├── omni_offline_client.py  # テキストAPIクライアント（Response API）
│   └── tts_client.py            # 🔊 TTSエンジンアダプター
├── 📁 main_routers/             # 🌐 APIルーターモジュール
├── 📁 memory/                   # 🧠 記憶管理システム
│   ├── store/                   # 記憶データストレージ
├── 📁 static/                   # 🌐 フロントエンド静的リソース
├── 📁 templates/                # 📄 フロントエンドHTMLテンプレート
├── 📁 utils/                    # 🛠️ ユーティリティモジュール
├── main_server.py               # 🌐 メインサーバー
└── memory_server.py             # 🧠 記憶サーバー
```

**データフロー**

![Framework](https://raw.githubusercontent.com/Project-N-E-K-O/N.E.K.O/main/assets/framework.drawio.svg)

### 開発への参加

本プロジェクトの環境依存は非常にシンプルです。`uv sync`を実行するだけで始められます。開発者はQQグループ1048307485への参加をお勧めします。

本プロジェクト（T.T.S.）は猫娘計画（Project N.E.K.O.）の派生プロジェクトです。
