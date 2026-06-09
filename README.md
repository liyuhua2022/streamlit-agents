# Streamlit Agents Hub

> Python & Streamlit 专属的 AI Agents 平台

本项目展示如何使用 Python 和 Streamlit 构建生产级 AI Agents 应用，包含完整的开发工作流和最佳实践。

---

## 🛠️ Available Skills

本项目包含两类 Skills：**通用开发技能** (.agents/) 和 **Claude Code 专用技能** (.claude/)。

### 通用开发技能 (.agents/skills/)

| Skill | Description | Key Features |
|-------|-------------|---------------|
| **python-best-practices** | Python 专业代码最佳实践 | PEP 8 规范、类型提示、模块化、DRY 原则、TDD、虚拟环境管理、Ruff/Black/Mypy 工具链 |
| **streamlit-best-practices** | 生产级 Streamlit 应用开发 | 项目结构、会话状态管理、缓存策略、组件组合、性能优化 |
| **skill-creator** | AI Skill 创建工具 | Skill 编写、评估、优化 |
| **test-driven-development** | TDD 开发模式 | 测试驱动、测试金字塔 |
| **requesting-code-review** | 代码审查流程 | 审查标准、反馈指南 |

### Claude Code 专用技能 (.claude/skills/)

| Skill | Description | Key Features |
|-------|-------------|---------------|
| **dev-workflow** | 完整开发工作流 | Planner → Coder → Reviewer → Tester 四阶段流程、Checkpoint 控制、自动重试机制 |
| **streamlit-extensions** | Streamlit 高级组件 | AgGrid 数据表格、ECharts 图表、option-menu 导航菜单、chatbox 聊天组件 |

---

## 🚀 如何使用 dev-workflow

`dev-workflow` 是一个完整的生产级开发流程，通过协调四个专业代理（Agent）按顺序执行，确保代码质量和交付可靠性。

### 工作流概览

```
[用户输入]
     │
     ▼
┌─────────────┐
│   PLANNER   │  → 制定计划 + 验收标准
└─────────────┘
     │
     ▼  ⚑ CHECKPOINT #1 — 计划审批（需人工确认）
┌─────────────┐
│    CODER    │  → 编写代码 + 单元测试
└─────────────┘
     │
     ▼  ⚑ CHECKPOINT #2 — 实现验证（需人工确认）
┌─────────────┐
│  REVIEWER   │  → 静态分析 + 质量检查
└─────────────┘
     │
  PASS? ──No──► [CODER 重试，最多 3 次]
     │
     ▼ Yes
┌─────────────┐
│   TESTER    │  → 执行测试 + 验证 AC
└─────────────┘
     │
  PASS? ──No──► [CODER 重试，最多 3 次]
     │
     ▼ Yes
  ✅ 完成 — 交付总结
```

### 工作流阶段详解

#### Phase 1: PLANNER（计划阶段）

**目标：** 定义任务范围、验收标准、测试需求

**输出格式：**
```markdown
## Task Summary
[任务概述，一段话说明要构建什么]

## Scope
- In scope: [要实现的内容]
- Out of scope: [明确排除的内容]
- Assumptions: [所做的假设]

## Implementation Tasks
- [ ] Task 1: [描述] — [受影响的文件]
- [ ] Task 2: [描述] — [受影响的文件]

## Unit Test Requirements
[每个模块/函数的测试用例规格]

## Acceptance Criteria (验收标准)
- AC1: Given [上下文], when [操作], then [预期结果]
- AC2: Given [上下文], when [操作], then [预期结果]

## Risks & Notes
[已知风险、难点、需要人工判断的事项]
```

**Checkpoint #1:** 展示计划后暂停，等待用户确认（"confirmed" 或 "change: 反馈"）

---

#### Phase 2: CODER（编码阶段）

**目标：** 根据计划实现所有任务，编写单元测试

**前置检查：**
1. 运行 `git status` — 确保工作区干净
2. 确认当前分支不是 main/master（如果是，创建新分支如 feat/）

**执行流程：**
- 按顺序实现每个 Task
- 每个 Task 完成后进行 git commit
- 为 Unit Test Requirements 中的每个函数编写测试

**输出格式：**
```markdown
## Implementation Summary

### Files Created
- [filepath]: [用途]

### Files Modified
- [filepath]: [修改了什么]

### Unit Tests Written
- [test file]: covers [模块/函数] — [测试用例列表]

### Deviations from Plan
- [任何偏离计划的地方] 或 "None — implemented as planned"
```

**Checkpoint #2:** 展示实现后暂停，要求用户运行应用验证 UI 效果

---

#### Phase 3: REVIEWER（审查阶段）

**目标：** 静态分析、质量门禁

**审查内容：**
- 代码正确性（是否符合计划）
- 代码质量（PEP 8、类型提示、文档）
- 安全性（凭据处理、输入验证）
- 错误处理
- 单元测试覆盖率

**输出格式：**
```markdown
## Review Result: [PASS | FAIL]

### Critical Issues (必须修复)
- [问题描述] — [文件:行号]

### Warnings (建议修复)
- [问题描述] — [文件:行号]

### Suggestions (可选改进)
- [建议内容]

### Unit Test Assessment
[测试覆盖情况]
```

**流程：**
- 如果 **PASS** → 自动进入 Phase 4
- 如果 **FAIL** → 重试循环（最多 3 次），每次让 Coder 修复 Critical Issues

---

#### Phase 4: TESTER（测试阶段）

**目标：** 执行测试、验证每个验收标准、补充边界情况测试

**验证内容：**
1. 运行所有单元测试
2. 验证每个 Acceptance Criteria
3. 执行额外的边界情况和错误处理测试

**输出格式：**
```markdown
## Test Result: [PASS | FAIL]

### Unit Tests (written by Coder)
- [测试名]: [PASS | FAIL]

### Acceptance Criteria Validation
- AC1: [PASS | FAIL] — [证据或失败原因]
- AC2: [PASS | FAIL] — [证据或失败原因]

### Additional Edge Cases (补充测试)
- [测试描述]: [PASS | FAIL]

### Overall Assessment
[总结：通过率、置信度]
```

**流程：**
- 如果 **PASS** → 进入 Phase 5 完成
- 如果 **FAIL** → 重试循环（最多 3 次），每次让 Coder 修复失败的测试

---

#### Phase 5: COMPLETION（完成阶段）

**输出：**
```markdown
─────────────────────────────────────────────────────
✅ WORKFLOW COMPLETE

Task: [原始用户请求]

── Results ──────────────────────────────────────────
Review attempts : [N] / 3  [PASSED | OVERRIDDEN]
Test attempts   : [N] / 3  [PASSED | OVERRIDDEN]

── Files Changed ────────────────────────────────────
Created  : [列表]
Modified : [列表]

── Acceptance Criteria ──────────────────────────────
✅ AC1: [标准文本]
✅ AC2: [标准文本]

── Overrides (如有) ─────────────────────────────────
[被跳过的 checkpoint 及原因]

─────────────────────────────────────────────────────
```

**自动执行：**
1. 更新 README.md
2. Git commit 所有更改

---

### 关键规则

| 规则 | 说明 |
|------|------|
| **Phase 隔离** | Planner/Coder/Reviewer/Tester 始终作为独立代理调用，不合并 |
| **Checkpoint #1/#2 强制** | 即使计划看起来简单，也必须暂停等待人工确认 |
| **结构化输出** | 任何代理必须按指定格式输出，否则重试 |
| **重试范围** | Reviewer/Test 失败时，只修复报告的问题，不重做全部 |
| **Abort 行为** | 用户说 "abort" 时停止，保留所有更改 |

### 如何调用

在 Claude Code 中输入：
```
/dev-workflow
```

然后描述你的任务，例如："帮我创建一个 Streamlit 登录页面"

---

## 📚 Skill 详细介绍

### streamlit-extensions

Streamlit 高级扩展组件库：

| Package | Purpose | Import |
|---------|---------|--------|
| `streamlit_aggrid` | 交互式数据表格 | `from st_aggrid import AgGrid, AgGridTheme` |
| `streamlit_echarts` | ECharts 可视化图表 | `from streamlit_echarts import st_echarts` |
| `streamlit_option_menu` | 水平导航菜单 | `from streamlit_option_menu import option_menu` |
| `streamlit_chatbox` | 聊天界面组件 | `from streamlit_chatbox import chatbox` |

---

### python-best-practices

Python 专业开发规范：

- **PEP 8**: 4空格缩进、79字符行宽、正确导入顺序
- **类型提示**: 函数签名、返回类型、泛型
- **模块化**: DRY 原则、单职责、类封装
- **测试**: pytest、测试驱动开发、Mock
- **工具链**: uv (包管理)、Ruff (linting)、Black (格式化)、Mypy (类型检查)

---

### streamlit-best-practices

Streamlit 生产级应用指南：

- **项目结构**: `src/app.py`, `src/pages/`, `src/components/`, `src/utils/`
- **会话状态**: 显式初始化、类型安全访问
- **缓存策略**: `@st.cache_data` (数据获取)、`@st.cache_resource` (ML 模型)
- **组件组合**: 可复用 UI 组件、业务逻辑分离

---

## 🎯 Project Example: 登录认证系统

本项目展示了如何使用 dev-workflow 构建一个完整的 Streamlit 登录认证系统。

### 功能特性

- 🔐 **用户登录认证** — 用户名/密码验证
- 💾 **会话持久化** — 登录状态存储在 JSON 文件
- 🔄 **刷新保持登录** — 页面刷新不丢失登录状态
- 🚪 **注销与重新登录** — 完整会话生命周期

### 项目结构

```
├── app.py              # Streamlit 主应用（使用 dev-workflow 开发）
├── auth.py             # 认证逻辑模块（遵循 python-best-practices）
├── auth_data.json      # 登录信息持久化存储
├── tests/
│   └── test_auth.py    # 14 个单元测试（pytest + TDD）
└── README.md
```

### 快速开始

```bash
# 安装依赖
pip install streamlit pytest

# 启动应用
streamlit run app.py

# 运行测试
pytest tests/ -v
```

### 默认登录凭据

- 用户名: `admin`
- 密码: `admin123`

### 自定义凭据（环境变量）

```bash
export APP_USERNAME=your_username
export APP_PASSWORD=your_password
streamlit run app.py
```

---

## 📦 依赖

```
streamlit>=1.28.0
pytest>=7.0.0

# 可选扩展（用于更复杂的 UI）
streamlit_aggrid~=1.0.5
streamlit_echarts==0.4.0
streamlit-option-menu==0.3.6
streamlit_chatbox==1.1.11
```

---

## License

MIT