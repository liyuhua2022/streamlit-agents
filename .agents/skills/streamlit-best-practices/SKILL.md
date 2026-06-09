---
name: streamlit-best-practices
description: |
  Expert guidance for building production-ready Streamlit applications.
  Use when creating Streamlit pages, managing session state, optimizing performance,
  or structuring multi-page Streamlit projects.

  Emphasizes: page structure, session_state management, caching strategies,
  component composition, and Python backend separation.
allowed-tools: ["Read", "Edit", "Write", "Bash", "Grep", "Glob"]
---

# Streamlit Best Practices Skill

This skill provides expert guidance for building professional, maintainable Streamlit applications following industry best practices.

## When to Use This Skill

Use this skill when:
- Creating new Streamlit pages or multi-page apps
- Managing session state and user data
- Implementing caching for performance optimization
- Building reusable Streamlit components
- Structuring Streamlit projects with Python backend logic
- Optimizing Streamlit app performance

## Core Principles

### 1. Project Structure

**Recommended Streamlit Project Structure:**
```
your-project/
├── src/
│   ├── app.py              # Main entry point (streamlit run src/app.py)
│   ├── pages/              # Multi-page apps
│   │   ├── home.py
│   │   ├── analysis.py
│   │   └── settings.py
│   ├── components/         # Reusable UI components
│   │   ├── charts.py
│   │   ├── forms.py
│   │   └── tables.py
│   ├── utils/              # Backend logic (non-Streamlit Python)
│   │   ├── data_processor.py
│   │   ├── api_client.py
│   │   └── validators.py
│   └── config.py           # App configuration
├── tests/
├── pyproject.toml
└── .streamlit/
    └── config.toml         # Streamlit configuration
```

**Key Principle:** Keep Streamlit UI code separate from pure Python business logic.

### 2. Page Structure

**Good Streamlit Page Pattern:**
```python
"""Page: Home / Data Overview"""

import streamlit as st
from src.utils.data_processor import process_data
from src.components.charts import render_summary_chart


def main() -> None:
    # Page configuration
    st.set_page_config(
        page_title="Data Dashboard",
        page_icon="📊",
        layout="wide"
    )

    # Initialize session state
    _init_session_state()

    # Page header
    st.title("📊 Data Dashboard")
    st.markdown("Welcome to the data analysis platform")

    # Main content
    _render_filters()
    _render_data_summary()
    _render_chart()


def _init_session_state() -> None:
    """Initialize required session state variables."""
    if "filters" not in st.session_state:
        st.session_state.filters = {}
    if "last_update" not in st.session_state:
        st.session_state.last_update = None


def _render_filters() -> None:
    """Render filter controls."""
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.date_input(
            "Select date range",
            value=[],
            help="Filter data by date"
        )
    with col2:
        category = st.selectbox(
            "Category",
            options=["All", "A", "B", "C"],
            help="Filter by category"
        )

    # Update session state
    st.session_state.filters = {
        "date_range": date_range,
        "category": category
    }


def _render_data_summary() -> None:
    """Render data summary metrics."""
    data = process_data(st.session_state.filters)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", f"{data.shape[0]:,}")
    col2.metric("Total Value", f"${data['value'].sum():,.2f}")
    col3.metric("Categories", data['category'].nunique())


def _render_chart() -> None:
    """Render main chart."""
    st.subheader("Trend Analysis")
    chart_data = process_data(st.session_state.filters)
    render_summary_chart(chart_data)


if __name__ == "__main__":
    main()
```

### 3. Session State Management

**Session State Best Practices:**

```python
# Good: Explicit initialization with defaults
def init_session_state() -> None:
    """Initialize all session state variables with defaults."""
    defaults = {
        "user_id": None,
        "preferences": {"theme": "light", "page_size": 50},
        "cache": {},
        "form_data": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# Good: Type-safe session state access
def get_user_id() -> int | None:
    """Get user ID from session state with type hint."""
    return st.session_state.get("user_id")


# Bad: Implicit state access
def process_something() -> None:
    # This can fail if key doesn't exist
    user_id = st.session_state["user_id"]
```

**Session State for Multi-Page Apps:**
```python
# src/utils/navigation.py
from typing import Protocol

class SessionStateManager(Protocol):
    """Protocol for session state management."""
    def get(self, key: str, default: ... = None) -> ...: ...
    def set(self, key: str, value: ...) -> None: ...
    def clear(self) -> None: ...


def navigate_to(page: str, **query_params) -> None:
    """Navigate to a page with query parameters stored in session."""
    st.session_state.current_page = page
    st.session_state.query_params = query_params
    st.rerun()
```

### 4. Caching Strategies

**When to Use Each Cache Type:**

| Cache Type | Use Case | Example |
|------------|----------|---------|
| `@st.cache_data` | Data fetching, processing | API calls, pandas operations |
| `@st.cache_resource` | ML models, database connections | Loaded models, DB connections |
| Manual cache | Complex state management | Session-based caching |

**Examples:**
```python
import streamlit as st
from functools import lru_cache

# Data fetching - use st.cache_data
@st.cache_data(ttl=3600, show_spinner="Fetching data...")
def fetch_data_from_api(endpoint: str, params: dict) -> dict:
    """Fetch data from API with 1-hour cache."""
    import requests
    response = requests.get(endpoint, params=params)
    return response.json()


# ML Model - use st.cache_resource
@st.cache_resource
def load_ml_model(model_path: str):
    """Load ML model once, reuse across sessions."""
    import joblib
    return joblib.load(model_path)


# Expensive computation with parameters
@st.cache_data(ttl=300)
def compute_analytics(df: pd.DataFrame, group_by: list[str]) -> pd.DataFrame:
    """Compute analytics with 5-minute cache."""
    return df.groupby(group_by).agg(["mean", "std", "count"])
```

**When NOT to Cache:**
- User-specific data that changes frequently
- Real-time data that must be fresh
- Large objects that exceed memory

### 5. Component Composition

**Reusable Component Pattern:**
```python
# src/components/forms.py
import streamlit as st
from typing import Callable, Any

def render_filter_form(
    on_submit: Callable[[dict[str, Any]], None],
    key: str = "filter_form"
) -> None:
    """Render a reusable filter form component.

    Args:
        on_submit: Callback function when form is submitted
        key: Unique key for this form instance
    """
    with st.form(key=key):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

        submit = st.form_submit_button("Apply Filters", type="primary")

        if submit:
            on_submit({
                "start_date": start_date,
                "end_date": end_date
            })


# src/components/charts.py
import streamlit as st
import plotly.express as px
from pandas import DataFrame

def render_bar_chart(
    df: DataFrame,
    x: str,
    y: str,
    title: str = "Chart",
    height: int = 400
) -> None:
    """Render a styled bar chart using Plotly.

    Args:
        df: DataFrame with chart data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        height: Chart height in pixels
    """
    fig = px.bar(df, x=x, y=y, title=title)
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
```

### 6. Error Handling

**Graceful Error Handling in Streamlit:**
```python
import streamlit as st
import logging

logger = logging.getLogger(__name__)


def safe_data_load(data_path: str) -> pd.DataFrame | None:
    """Load data with graceful error handling.

    Returns:
        DataFrame if successful, None if error occurred
    """
    try:
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {data_path}")
        logger.error(f"File not found: {data_path}")
        return None
    except pd.errors.EmptyDataError:
        st.warning(f"Empty file: {data_path}")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        logger.exception("Error loading data")
        return None


def render_data_view(df: pd.DataFrame | None) -> None:
    """Render data view with error boundary."""
    if df is None:
        st.info("No data to display. Please upload a file or adjust filters.")
        return

    st.dataframe(df, use_container_width=True)
```

### 7. Multi-Page App Structure

**Main App Entry Point (app.py):**
```python
import streamlit as st

st.set_page_config(
    page_title="My App",
    page_icon=":wave:",
    layout="wide"
)

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.user_preferences = {}

# Navigation is handled automatically by Streamlit's multi-page structure
# Place pages in src/pages/ directory
```

**Page File Naming Convention:**
```
src/pages/1_home.py        # Home page (runs first)
src/pages/2_analysis.py     # Analysis page
src/pages/3_settings.py    # Settings page
```

**Page Pattern:**
```python
# src/pages/2_analysis.py
import streamlit as st

st.set_page_config(page_title="Analysis", page_icon="📈")

st.title("📈 Data Analysis")
st.markdown("Analyze your data with advanced tools")

# Page-specific content
```

### 8. Performance Optimization

**Optimization Techniques:**
```python
# 1. Use container width properly
st.dataframe(df, use_container_width=True)

# 2. Limit data display with pagination
def render_paginated_table(data: list, page_size: int = 50) -> None:
    total_pages = (len(data) + page_size - 1) // page_size
    page = st.number_input(
        "Page", min_value=1, max_value=total_pages, value=1
    )
    start = (page - 1) * page_size
    end = start + page_size
    st.dataframe(data[start:end])

# 3. Use columns for parallel rendering
col1, col2, col3 = st.columns(3)
with col1:
    expensive_operation_1()
with col2:
    expensive_operation_2()
with col3:
    expensive_operation_3()

# 4. Lazy loading with st.empty()
placeholder = st.empty()
if show_detail:
    result = expensive_computation()
    placeholder.plotly_chart(result)
```

### 9. Testing Streamlit Components

**Test Pattern:**
```python
# tests/test_components.py
import pytest
from streamlit.testing.v1 import AppTest

def test_home_page_renders():
    """Test that home page renders correctly."""
    app = AppTest.from_file("src/pages/home.py")
    app.run()
    assert app.title[0].value == "Home"
    assert len(app.button) > 0


def test_filter_form_submission():
    """Test filter form submission updates session state."""
    app = AppTest.from_file("src/pages/analysis.py")
    app.run()
    # Interact with form
    app.number_input[0].set_value("2024-01-01")
    app.button["Apply Filters"].click()
    app.run()
    # Verify state change
    assert app.session_state["filters"]["start_date"] == "2024-01-01"
```

## Best Practices Checklist

When building Streamlit apps, ensure:

- ✅ Page structure follows single responsibility (UI in pages/, logic in utils/)
- ✅ All session state variables are explicitly initialized
- ✅ Appropriate caching is used (@st.cache_data or @st.cache_resource)
- ✅ Error handling is graceful with user-friendly messages
- ✅ Components are reusable and composable
- ✅ Heavy computations are cached or lazy-loaded
- ✅ Multi-page apps use numbered file prefixes for ordering
- ✅ Streamlit UI code is separated from pure Python business logic
- ✅ pyproject.toml includes streamlit as a dependency
- ✅ .streamlit/config.toml exists for app configuration

## Common Patterns

### Data Loading Pattern:
```python
@st.cache_data(ttl=3600)
def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def main():
    df = load_data("data.csv")
    st.dataframe(df)
```

### Form Pattern:
```python
with st.form(key="my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Submit")

    if submitted:
        process_form(name, email)
        st.success("Form submitted!")
```

### Callback Pattern:
```python
def on_option_change():
    st.session_state.selected = st.session_state.temp_value

option = st.selectbox(
    "Choose",
    options=["A", "B", "C"],
    key="temp_value",
    on_change=on_option_change
)
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Awesome Streamlit](https://awesome-streamlit.org/)
- [Streamlit Components](https://streamlit.io/components)