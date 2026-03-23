# 多智能体药品成本分析系统 (Multi-Agent Drug Cost Analysis System)

本项目是一个基于大模型（LLM）和多智能体协同架构的现代化 Web 应用程序，旨在为医药企业提供自动化、全维度的药品成本测算、定价策略制定及供应链优化建议。

## 📦 项目依赖清单

本项目采用前后端分离架构，主要依赖如下：

### 前端依赖 (Frontend - React + Vite)
前端主要技术栈位于 `frontend/` 目录：
- **核心框架**: `react` (^18.3.1), `react-dom`
- **路由与状态**: `react-router-dom`, `zustand`
- **UI 组件库**: `antd` (^5.20.0), `@ant-design/charts` (可视化图表)
- **样式方案**: `tailwindcss`, `@ant-design/cssinjs`
- **网络请求**: `axios`
- **国际化**: `i18next`, `react-i18next`
- **测试框架**: `vitest`, `@testing-library/react`
- **构建工具**: `vite`, `typescript`

### 后端依赖 (Backend - Python FastAPI)
后端主要技术栈位于 `backend/` 目录及项目根目录，通过 `requirements.txt` 和 `.venv` 管理：
- **Web 框架**: `fastapi`, `uvicorn` (ASGI 服务器)
- **数据库驱动**: 
  - `redis` (消息总线与缓存)
  - `pymongo` (MongoDB 持久化存储)
  - `neo4j` (知识图谱图数据库)
- **加密与安全**: `pycryptodome` (AES 加密), `python-jose[cryptography]` (JWT 鉴权)
- **事件驱动**: `cloudevents`
- **报告生成**: `reportlab` (PDF 导出), `python-docx` (Word 导出)
- **数据验证与环境变量**: `pydantic`, `python-dotenv`
- **测试框架**: `pytest`, `httpx`
- **大模型与 RAG**: `sentence-transformers`, `chromadb` (向量库), 大模型 API SDK (SiliconFlow/Ollama 等)

---

## 🚀 如何启动这个项目

为了顺利运行该项目，请确保你的本地环境已安装以下基础软件：
- **Node.js** (推荐 v18+)
- **Python** (推荐 v3.10+)
- **Redis** 服务 (默认端口 6379)
- **MongoDB** 服务 (默认端口 27017)

### 步骤 1：启动后端服务

1. 打开终端，进入项目根目录。
2. 激活 Python 虚拟环境（如果尚未激活）：
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
3. 安装或更新后端依赖：
   ```bash
   pip install -r backend/requirements.txt
   pip install reportlab python-docx pytest httpx
   ```
4. 配置环境变量：
   确保根目录存在 `.env` 文件，并包含必需的 API Key 和数据库连接字符串：
   ```env
   SILICONFLOW_API_KEY=your_api_key_here
   REDIS_URL=redis://localhost:6379/0
   MONGO_URL=mongodb://localhost:27017
   MONGO_DB=multi_agent_db
   ```
5. 启动 FastAPI 服务端（系统会自动拉起后台的智能体监听线程）：
   ```bash
   python backend/main.py
   ```
   > 成功启动后，后端服务将运行在 `http://localhost:8000`。可访问 `http://localhost:8000/docs` 查看 API 文档。

### 步骤 2：启动前端服务

1. 新开一个终端窗口，进入 `frontend` 目录：
   ```bash
   cd frontend
   ```
2. 安装前端依赖（使用 `--legacy-peer-deps` 防止版本冲突）：
   ```bash
   npm install --legacy-peer-deps
   ```
3. 启动 Vite 开发服务器：
   ```bash
   npm run dev
   ```
   > 成功启动后，终端会打印出本地访问地址（通常为 `http://localhost:5173`）。在浏览器中打开该地址即可访问系统。

### 步骤 3：运行测试 (可选)
- **前端测试**: 在 `frontend` 目录下运行 `npm run test` 或 `npm run coverage`。
- **后端测试**: 在根目录下运行 `pytest backend/tests/`。

---

## 📤 如何将此项目上传到 GitHub

如果你想将这个项目推送到你的 GitHub 仓库，请按照以下步骤操作：

### 1. 准备工作
**注意：** 确保你的电脑上已经安装了 Git。如果你在终端输入 `git init` 时看到类似“无法将 git 项识别为 cmdlet、函数、脚本文件或可运行程序的名称”的错误，说明你还没有安装 Git 或没有将其添加到系统环境变量中。

**如何安装 Git：**
- **Windows 用户**：请访问 [Git for Windows 官网](https://gitforwindows.org/) 下载安装包。安装时一直点击“下一步”（保持默认配置即可）。安装完成后，**请重启你的代码编辑器（如 Trae / VSCode）或终端**，然后重新尝试。
- **Mac 用户**：在终端输入 `xcode-select --install` 或通过 Homebrew 安装 `brew install git`。

检查项目根目录是否已有 `.gitignore` 文件。
如果没有，请创建一个 `.gitignore` 并添加以下内容以防止上传冗余文件：
```gitignore
# Python
.venv/
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/

# Node
node_modules/
dist/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env

# Databases & Reports
vector_dbs/
generated_reports/
*.jsonl
```

### 2. 初始化 Git 仓库并提交代码
在项目根目录（`e:\aproj\cxy`）打开终端，依次执行：

```bash
# 初始化 git 仓库（如果尚未初始化）
git init

# 将所有文件添加到暂存区
git add .

# 提交代码到本地仓库
git commit -m "Initial commit: Multi-Agent Drug Cost Analysis System"
```

### 3. 在 GitHub 创建远程仓库
1. 登录 [GitHub](https://github.com/)。
2. 点击右上角的 `+` -> `New repository`。
3. 填写 Repository name（如 `drug-cost-analysis`），选择 Public 或 Private。
4. **不要**勾选 "Initialize this repository with a README"（因为本地已经有了）。
5. 点击 `Create repository`。

### 4. 推送到远程仓库
在刚刚创建好的 GitHub 仓库页面中，找到 "…or push an existing repository from the command line" 部分的命令，复制并在你的终端中运行：

```bash
# 将 origin 替换为你的实际仓库地址
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 更改主分支名称为 main（新版 Git 默认要求）
git branch -M main

# 将本地代码推送到 GitHub
git push -u origin main
```

推送完成后，刷新 GitHub 页面，你的代码就已经成功上传了！
