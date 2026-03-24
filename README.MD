<div align="center">

![Logo](assets/neko_logo.jpg)

[English](docs/README_en.md) | [日本語](docs/README_ja.md)
# Project N.E.K.O. - Talking Twin Simulator (T.T.S.) :kissing_cat: <br>**T.T.S.，用虚拟形象为你讲述。**

> **为视频制作者设计的虚拟形象口播软件**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![QQ群](https://custom-icon-badges.demolab.com/badge/QQ群-1048307485-00BFFF?style=flat&logo=tencent-qq)](https://qm.qq.com/q/1048307485)

</div>

---

# Talking Twin Simulator (T.T.S.)

本项目（T.T.S.）是猫娘计划（Project N.E.K.O.）的衍生项目，专注于虚拟形象口播场景。用户输入文本后，虚拟形象将直接朗读该文本，无需LLM参与。

---

## 快速开始

```bash
uv sync
python main_server.py
```

启动后通过 `http://localhost:48911` 访问网页版。

## 进阶使用
<details>

#### 配置API Key

当你想要通过配置自己的API来获得额外功能时，您可以配置一个第三方AI服务（核心**必须支持 Realtime API**）。本项目目前推荐使用 *阶跃星辰* 或 *阿里云*。通过访问`http://localhost:48911/api_key`可以在Web界面中直接配置。

> 获取 *阿里云API*。在阿里云的百炼平台[官网](https://bailian.console.aliyun.com/)注册账号。新用户实名认证后可以获取大量免费额度。注册完成后，请访问[控制台](https://bailian.console.aliyun.com/api-key?tab=model#/api-key)获取API Key。

#### 修改人设

- 网页版访问`http://localhost:48911/chara_manager`即可进入人设编辑页面。

- 进阶人设主要包括**Live2D模型设置(live2d)**和**声音设置(voice_id)**。如果你想要更改**Live2D模型**，请先将模型目录复制到本项目中的`static`文件夹下。从进阶设置中可以进入Live2D模型管理界面，可以更换模型，并通过拖拽和鼠标滚轮调整模型的位置和大小。如果你想要更改**角色声音**，请准备一段5秒左右的连贯、干净的语音录音。通过进阶设置进入语音设置页面，上传录音即可完成自定义语音。

#### 记忆整理

- 通过访问`http://localhost:48911/memory_browser`可以浏览和校对近期记忆与摘要，一定程度上缓解模型复读、认知错误等问题。

</details>

# 项目细节
<details>

**项目架构**

```
T.T.S/
├── 📁 config/                   # ⚙️ 配置管理模块
│   ├── api_providers.json       # API服务商配置
│   ├── prompts_chara.py         # 角色提示词
│   └── prompts_sys.py           # 系统提示词
├── 📁 main_logic/              # 🔧 核心逻辑模块（负责对话）
│   ├── core.py                  # 核心对话模块
│   ├── cross_server.py         # 跨服务器通信
│   ├── omni_realtime_client.py  # 实时API客户端（Relatime API）
│   ├── omni_offline_client.py  # 文本API客户端（Response API）
│   └── tts_client.py            # 🔊 TTS引擎适配器
├── 📁 main_routers/             # 🌐 前端网页路由模块
├── 📁 memory/                   # 🧠 记忆管理系统
│   ├── store/                   # 记忆数据存储
├── 📁 static/                   # 🌐 前端静态资源
├── 📁 templates/                # 📄 前端HTML模板
├── 📁 utils/                    # 🛠️ 工具模块
├── main_server.py               # 🌐 主服务器
└── memory_server.py             # 🧠 记忆服务器
```

**数据流向**

![Framework](assets/framework.drawio.svg)

### 参与开发

本项目环境依赖非常简单，请执行`uv sync`即可。开发者建议加入QQ群1048307485。

本项目（T.T.S.）是猫娘计划（Project N.E.K.O.）的衍生项目。

</details>
