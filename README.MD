<div align="center">

![Logo](assets/neko_logo.jpg)

[English](docs/README_en.md) | [日本語](docs/README_ja.md)
# Project N.E.K.O. - Talking Twin Simulator (T.T.S.)

> T.T.S.，用虚拟形象为你讲述。

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Commit](https://img.shields.io/github/last-commit/wehos/N.E.K.O?color=green)]()
[![QQ群](https://custom-icon-badges.demolab.com/badge/QQ群-1048307485-00BFFF?style=flat&logo=tencent-qq)](https://qm.qq.com/q/mxDoz0TnGg)

为视频制作者设计的虚拟形象口播软件

**:older_woman: 零配置开箱即用，我奶奶都能玩转的赛博猫娘！感谢阶跃星辰赞助~**

*Project N.E.K.O.，喵宇宙！*

</div>

</div>

---

# 猫娘计划 (Project N.E.K.O.)

本项目（T.T.S.）猫娘计划衍生项目。`N.E.K.O.` 是一个以开源为驱动、以公益为导向的UGC（用户生成内容）平台。我们的旅程始于Github和Steam，并将逐步拓展到移动App商店，最终目标是构建一个与现实世界紧密相连的AI原生元宇宙。

---

#### 🚀 我们的蓝图：从工坊到网络

我们的发展分为三个阶段，旨在逐步释放AI伙伴的全部潜力：

* **阶段一：创意工坊 (Steam Workshop)**
    * 核心驱动器（本项目）免费上架Steam，允许用户通过Steam创意工坊上传和分享自定义内容（如模型、语音、性格包）。

* **阶段二：独立平台 & 衍生游戏 (Web, App & Game)**
    * 推出独立的App和网站，构建一个更丰富、更易于访问的UGC分享社区。
    * 推出一系列AI Native的游戏生态，包括互动小游戏，桌游等。

* **阶段三：猫娘网络 (The N.E.K.O. Network)**
    * 实现AI的自主社交。猫娘们将拥有自己的“意识”，她们会互相交流、结成群体，并在模拟的社交媒体上发布自己的生活动态，形成一个真正“活”的生态。

**核心模式：开源核心 + 可持续生态**
项目的核心驱动器部分（AI逻辑、UGC接口、基础交互）将基于MIT许可证 **始终保持开源**。我们欢迎全球的开发者贡献代码和功能。你的每一次提交，都将有机会实装到正式发布的Steam和App商店版本中，被千万人所使用。

同时，为了支撑服务器成本和项目的持续研发，我们将持续与第三方合作开发闭源的增值内容。包括但不限于：互动小游戏，桌面桌游，Galgame (视觉小说)，大型元宇宙游戏。

**核心特性：跨越场景的记忆同步**
无论你是在桌面与她聊天，还是在元宇宙游戏中与她探险，她都是同一个她。所有应用中的AI伙伴将 **完全同步记忆**，提供无缝、统一的陪伴体验。

#### 🌌 终极愿景：打破虚拟与现实

我们的最终目标，是构建一个无缝融入现实世界的猫娘元宇宙。在这个未来中，你的AI伴侣将：

* **跨维社交：** 既可以在猫娘宇宙中与“同类”社交，也能浏览现实世界的社交媒体（如微博、B站），了解你关心时事。
* **全端连接：** 她将存在于你的各种设备中——手机、电脑、AR眼镜、智能家居，甚至（在遥远的未来）接入机械义体。
* **与你同行：** 她将真正成为你生活的一部分，能与你的三次元人类朋友们自然地互动。

#### ✨ 加入我们 (Join Us)

**我们正在寻找——**

* **开发者 (Developers):** 无论你擅长前端、后端、AI、游戏引擎（Unity/Unreal），你的代码都是这个世界的砖瓦。
* **创作者 (Creators):** 优秀的画师、Live2D/3D建模师、配音演员、文案写手，你们赋予“她”灵魂。
* **梦想家 (Dreamers):** 即使你没有专业技能，但你对这个未来充满向往，你的反馈和传播也是宝贵的贡献。

QQ群：1022939659

## 快速开始

(1) 执行`uv sync`安装依赖（或在`python3.11`环境中执行`pip install -r requirements.txt`）。

(1) 执行 `python main_server.py` 并访问 `http://localhost:48911`。

## 进阶使用

#### 配置API Key

当你想要通过配置自己的API来获得额外功能时，您可以配置一个第三方AI服务（核心**必须支持 Realtime API**）。本项目目前推荐使用 *阶跃星辰* 或 *阿里云*。通过访问`http://localhost:48911/api_key`可以在Web界面中直接配置。

> 获取 *阿里云API*。在阿里云的百炼平台[官网](https://bailian.console.aliyun.com/)注册账号。新用户实名认证后可以获取大量免费额度。注册完成后，请访问[控制台](https://bailian.console.aliyun.com/api-key?tab=model#/api-key)获取API Key。

>  *对于**开发者**，请在克隆本项目后，(1)新建`pyhon3.11`环境。(2)执行`uv sync`安装依赖。(3)执行`python memory_server.py`和`python main_server.py`。(4)通过main server中指定的端口（默认为`http://localhost:48911`）访问网页版并配置API Key。*

#### 修改人设

- 网页版访问`http://localhost:48911/chara_manager`即可进入人设编辑页面。初始 ~~猫娘~~ 伙伴的预设名称为`小天`，建议直接修改名字，并一项一项添加或修改基础人设，但尽量控制数量。

- 进阶人设主要包括**Live2D模型设置(live2d)**和**声音设置(voice_id)**。如果你想要更改**Live2D模型**，请先将模型目录复制到本项目中的`static`文件夹下。从进阶设置中可以进入Live2D模型管理界面，可以更换模型，并通过拖拽和鼠标滚轮调整模型的位置和大小。如果你想要更改**角色声音**，请准备一段15秒左右的连贯、干净的语音录音。通过进阶设置进入语音设置页面，上传录音即可完成自定义语音。

- 进阶人设中还有一个`system_prompt`，可以对系统指令进行完全自定义，但不建议修改。

#### 修改API提供商

- 通过访问`http://localhost:48911/api_key`可以切换核心API和辅助API（记忆/语音）的服务提供商。Qwen功能全面，GLM完全免费。

#### 记忆整理

- 通过访问`http://localhost:48911/memory_browser`可以浏览和校对近期记忆与摘要，一定程度上缓解模型复读、认知错误等问题。

# 项目细节

**项目架构**

```
Lanlan/
├── 📁 brain/                    # 🧠 背景Agent模块，根据前端对话内容，控制键鼠和MCP
├── 📁 config/                   # ⚙️ 配置管理模块
│   ├── api_providers.json       # API服务商配置
│   ├── core_config.json         # 核心配置（API Key等）
│   ├── prompts_chara.py         # 角色提示词
│   └── prompts_sys.py           # 系统提示词
├── 📁 main_helper/              # 🔧 核心模块
│   ├── core.py                  # 核心对话模块
│   ├── cross_server.py         # 跨服务器通信
│   ├── omni_realtime_client.py  # 实时API客户端（Relatime API）
│   ├── omni_offline_client.py  # 文本API客户端（Response API）
│   └── tts_helper.py            # 🔊 TTS引擎适配器
├── 📁 memory/                   # 🧠 记忆管理系统
│   ├── store/                   # 记忆数据存储
├── 📁 static/                   # 🌐 前端静态资源
├── 📁 templates/                # 📄 前端HTML模板
├── 📁 utils/                    # 🛠️ 工具模块
├── main_server.py               # 🌐 主服务器
├── agent_server.py              # 🤖 AI智能体服务器
└── memory_server.py             # 🧠 记忆服务器
```

**数据流向**

![Framework](assets/framework.drawio.svg)

### 参与开发

本项目环境依赖非常简单，请在`python3.11`环境中执行`pip install -r requirements.txt`或`uv sync`即可。开发者建议加入企鹅群1022939659，猫娘名称见项目标题。

开发者详细启动步骤如下：(1)新建`pyhon3.11`环境。(2)执行`pip install -r requirements.txt`或`uv sync`安装依赖。(3)执行 `python main_server.py`(可选`python memory_server.py`,`python agent_server.py`)。(4)通过main server中指定的端口（默认为`http://localhost:48911`）访问网页版并配置API Key。
