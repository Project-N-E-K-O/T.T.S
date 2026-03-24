<div align="center">

![Logo](https://raw.githubusercontent.com/Project-N-E-K-O/N.E.K.O/main/assets/neko_logo.jpg)

[中文](https://github.com/Project-N-E-K-O/N.E.K.O/blob/main/README.MD) | [日本語](README_ja.md)

# Project N.E.K.O. - Talking Twin Simulator (T.T.S.) :kissing_cat: <br>**T.T.S., tell your story with virtual characters.**

> **Virtual character narration software designed for video creators.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Project-N-E-K-O/N.E.K.O/blob/main/LICENSE)
[![QQ Group](https://custom-icon-badges.demolab.com/badge/QQ群-1048307485-00BFFF?style=flat&logo=tencent-qq)](https://qm.qq.com/q/1048307485)

</div>

---

# Talking Twin Simulator (T.T.S.)

This project (T.T.S.) is a derivative of Project N.E.K.O., focused on virtual character narration scenarios. Users input text, and the virtual character reads it aloud directly without LLM involvement.

---

## Quick Start

```bash
uv sync
python main_server.py
```

After launching, access the web interface at `http://localhost:48911`.

## Advanced Usage

#### Configuring API Key

When you want to obtain additional features by configuring your own API, you can configure a third-party AI service (core API **must support Realtime API**). This project currently recommends using *StepFun* or *Alibaba Cloud*. Visit `http://localhost:48911/api_key` to configure directly through the Web interface.

> Obtaining *Alibaba Cloud API*: Register an account on Alibaba Cloud's Bailian platform [official website](https://bailian.console.aliyun.com/). New users can receive substantial free credits after real-name verification. After registration, visit the [console](https://bailian.console.aliyun.com/api-key?tab=model#/api-key) to get your API Key.

#### Modifying Character Persona

- Access `http://localhost:48911/chara_manager` on the web version to enter the character editing page.

- Advanced persona settings mainly include **Live2D model settings (live2d)** and **voice settings (voice_id)**. If you want to change the **Live2D model**, first copy the model directory to the `static` folder in this project. You can enter the Live2D model management interface from advanced settings, where you can switch models and adjust their position and size by dragging and scrolling. If you want to change the **character voice**, prepare a continuous, clean voice recording of about 5 seconds. Enter the voice settings page through advanced settings and upload the recording to complete custom voice setup.

#### Memory Review

- Visit `http://localhost:48911/memory_browser` to browse and proofread recent memories and summaries, which can somewhat alleviate issues like model repetition and cognitive errors.

# Project Details

**Project Architecture**

```
T.T.S/
├── 📁 config/                   # ⚙️ Configuration management
│   ├── api_providers.json       # API provider configuration
│   ├── prompts_chara.py         # Character prompts
│   └── prompts_sys.py           # System prompts
├── 📁 main_logic/              # 🔧 Core modules
│   ├── core.py                  # Core dialogue module
│   ├── cross_server.py         # Cross-server communication
│   ├── omni_realtime_client.py  # Realtime API client (Realtime API)
│   ├── omni_offline_client.py  # Text API client (Response API)
│   └── tts_client.py            # 🔊 TTS engine adapter
├── 📁 main_routers/             # 🌐 API router modules
├── 📁 memory/                   # 🧠 Memory management system
│   ├── store/                   # Memory data storage
├── 📁 static/                   # 🌐 Frontend static resources
├── 📁 templates/                # 📄 Frontend HTML templates
├── 📁 utils/                    # 🛠️ Utility modules
├── main_server.py               # 🌐 Main server
└── memory_server.py             # 🧠 Memory server
```

**Data Flow**

![Framework](https://raw.githubusercontent.com/Project-N-E-K-O/N.E.K.O/main/assets/framework.drawio.svg)

### Contributing to Development

This project has very simple environment dependencies. Just run `uv sync` to get started. Developers are encouraged to join QQ group 1048307485.

This project (T.T.S.) is a derivative of Project N.E.K.O.
