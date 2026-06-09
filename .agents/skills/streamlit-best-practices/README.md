# Streamlit Best Practices Skill

A comprehensive Claude Code skill for building production-ready Streamlit applications with proper structure, caching, and component composition.

## Overview

This skill provides expert guidance on:

- **Project Structure**: Clean separation of Streamlit UI and Python backend
- **Page Patterns**: Best practices for Streamlit page development
- **Session State**: Proper initialization and management
- **Caching**: Strategic use of `@st.cache_data` and `@st.cache_resource`
- **Component Composition**: Building reusable UI components
- **Multi-Page Apps**: Structuring complex Streamlit applications
- **Performance**: Optimization techniques for Streamlit apps
- **Error Handling**: Graceful error handling with user feedback

## When to Use This Skill

The skill is automatically invoked when you:

- Create new Streamlit pages or multi-page apps
- Manage session state and user data
- Implement caching for performance optimization
- Build reusable Streamlit components
- Structure Streamlit projects with Python backend logic
- Optimize Streamlit app performance

## File Structure

```
streamlit-best-practices/
├── SKILL.md              # Main skill instructions for Claude
├── QUICK_REFERENCE.md     # Quick lookup guide
├── README.md             # This file
└── examples/
    ├── page_structure.py        # Well-structured page example
    ├── caching_patterns.py      # Caching examples
    └── components.py            # Reusable components
```

## Quick Start

### Setting Up a New Streamlit Project

1. **Create project structure:**
```bash
mkdir my_streamlit_app
cd my_streamlit_app
mkdir -p src/pages src/components src/utils
touch src/__init__.py src/pages/__init__.py
```

2. **Create pyproject.toml:**
```toml
[project]
name = "my-streamlit-app"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "streamlit>=1.28.0",
    "pandas>=2.0.0",
    "plotly>=5.18.0",
]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy", "streamlit-nightly"]
```

3. **Create .streamlit/config.toml:**
```toml
[server]
headless = true
port = 8501

[theme]
primaryColor = "#4F46E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
```

4. **Create main app (src/app.py):**
```python
import streamlit as st

st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Welcome")
st.markdown("Your app description here")
```

5. **Run the app:**
```bash
streamlit run src/app.py
```

## Core Principles

1. **Separate UI from Logic**: Keep Streamlit code in pages/, pure Python in utils/
2. **Initialize Session State**: Always explicitly initialize session state variables
3. **Cache Strategically**: Use `@st.cache_data` for data, `@st.cache_resource` for resources
4. **Handle Errors Gracefully**: Provide user-friendly error messages
5. **Build Reusable Components**: Create composable UI components in components/

## Integration with Claude Code

When Claude Code uses this skill, it will:

1. **Enforce proper project structure** for Streamlit apps
2. **Suggest appropriate session state patterns** for state management
3. **Recommend caching strategies** based on use case
4. **Build reusable components** that can be shared across pages
5. **Optimize performance** with lazy loading and pagination
6. **Separate concerns** between UI (Streamlit) and backend (pure Python)
7. **Follow Streamlit conventions** for multi-page apps

## Best Practices Checklist

- ✅ PEP 8 compliant Python code
- ✅ All functions have type hints
- ✅ Public functions have comprehensive docstrings
- ✅ No code duplication (DRY principle)
- ✅ Session state variables explicitly initialized
- ✅ Appropriate caching for expensive operations
- ✅ Error handling with user feedback
- ✅ Components are reusable and composable
- ✅ Tests exist for new functionality

## Resources

### Official Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Streamlit Components](https://streamlit.io/components)

### Community
- [Streamlit Forum](https://discuss.streamlit.io/)
- [Awesome Streamlit](https://awesome-streamlit.org/)
- [Streamlit Gallery](https://streamlit.io/gallery)

## Version History

- **0.1.0** (Initial Release)
  - Project structure guidelines
  - Session state management patterns
  - Caching strategies (@st.cache_data, @st.cache_resource)
  - Component composition patterns
  - Multi-page app structure
  - Performance optimization techniques
  - Error handling best practices
  - Testing patterns