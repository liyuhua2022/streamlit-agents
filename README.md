# Streamlit Agents Hub

> Python & Streamlit 专属的 AI Agents 平台

一个基于 Streamlit 构建的登录认证示例项目，展示如何实现会话状态管理、登录信息持久化、以及页面刷新保持登录状态等功能。

## 功能特性

- 🔐 **用户登录认证** — 支持用户名/密码验证
- 💾 **会话持久化** — 登录状态存储在 JSON 文件中
- 🔄 **刷新保持登录** — 页面刷新不丢失登录状态
- 🚪 **注销功能** — 支持注销并重新登录
- 🔧 **环境变量配置** — 支持通过环境变量配置凭据

## 项目结构

```
├── app.py              # Streamlit 主应用入口
├── auth.py             # 认证逻辑模块
├── auth_data.json      # 登录信息持久化存储（自动生成）
├── tests/
│   └── test_auth.py    # 单元测试
└── README.md
```

## 快速开始

### 安装依赖

```bash
pip install streamlit pytest
```

### 启动应用

```bash
streamlit run app.py
```

### 默认登录凭据

- 用户名: `admin`
- 密码: `admin123`

### 自定义凭据

通过环境变量配置：

```bash
export APP_USERNAME=your_username
export APP_PASSWORD=your_password
streamlit run app.py
```

## 运行测试

```bash
pytest tests/ -v
```

## 技术栈

- **Python 3.8+**
- **Streamlit** — Web 框架
- **JSON** — 会话持久化

## License

MIT