---
name: streamlit-extensions
description: Guide for building rich Streamlit apps using specialized extensions including AgGrid, ECharts, option-menu, and chatbox. Use this skill when you need to add interactive data grids, charts, navigation menus, or chat interfaces to a Streamlit application.
---

## Overview

This skill covers Streamlit extension packages that add advanced UI components. These extensions work alongside core Streamlit and should be imported after `streamlit`.

## Packages Covered

| Package | Purpose | Import |
|---------|---------|--------|
| `streamlit_aggrid` | Interactive data grid with filtering, sorting, exporting | `from st_aggrid import AgGrid, JsCode` |
| `streamlit_echarts` | Interactive ECharts visualizations | `from streamlit_echarts import st_echarts` |
| `streamlit-option-menu` | Horizontal navigation / option menu | `from streamlit_option_menu import option_menu` |
| `streamlit_chatbox` | Chat UI components | `from streamlit_chatbox import chatbox` |

---

## streamlit-aggrid

**Use case:** Display large tabular data with Excel-like filtering, sorting, pagination, and column operations.

### Basic Usage

```python
from st_aggrid import AgGrid, AgGridTheme
import pandas as pd

df = pd.DataFrame({...})

grid_options = {
    "columnDefs": [
        {"field": "name", "headerName": "Name", "filter": True},
        {"field": "value", "headerName": "Value", "filter": True, "editable": True},
    ],
    "defaultColDef": {"sortable": True, "resizable": True},
    "pagination": True,
    "paginationPageSize": 20,
}

response = AgGrid(
    df,
    gridOptions=grid_options,
    theme=AgGridTheme.ALpine,
    height=500,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=False,
)

# Access selected rows
selected_rows = response["selected_rows"]
```

### Key Features

- **Filtering:** Set `filter: True` in columnDefs
- **Sorting:** Set `sortable: True` in defaultColDef (default is True)
- **Pagination:** `pagination: True` with `paginationPageSize`
- **Row Selection:** `enable_checkbox: True` for multi-select, access via `response["selected_rows"]`
- **Editable Cells:** `editable: True` in columnDefs, get edits via `response["data"]`
- **Column Resize:** `resizable: True` in defaultColDef
- **Fit Columns:** `fit_columns_on_grid_load=True` to auto-size columns

### Theme Options

```python
from st_aggrid import AgGridTheme

AgGridTheme.ALPINE        # Default, clean modern look
AgGridTheme.ALPINE_DARK  # Dark mode
AgGridTheme.BALHAM       # Professional, compact
AgGridTheme.BALHAM_DARK  # Dark mode
AgGridTheme.MATERIAL     # Google Material design
```

### Advanced: Custom Cell Renderers with JsCode

```python
from st_aggrid import AgGrid, JsCode

# Custom status renderer
status_renderer = JsCode("""
function(params) {
    const value = params.value;
    const color = value === 'Active' ? 'green' : 'red';
    return `<span style="color:${color}">${value}</span>`;
}
""")

grid_options = {
    "columnDefs": [
        {"field": "status", "headerName": "Status", "cellRenderer": status_renderer},
    ],
}
```

### Return Value

`AgGrid()` returns a dict with keys:
- `data`: Edited dataframe (if cells are editable)
- `selected_rows`: List of selected row dicts
- `rows`: All grid rows

---

## streamlit-echarts

**Use case:** Interactive charts (line, bar, pie, scatter, map, etc.) powered by ECharts.

### Basic Usage

```python
from streamlit_echarts import st_echarts

option = {
    "title": {"text": "Sales Overview"},
    "tooltip": {"trigger": "item"},
    "legend": {"data": ["Sales", "Profit"]},
    "xAxis": {"type": "category", "data": ["Jan", "Feb", "Mar"]},
    "yAxis": {"type": "value"},
    "series": [
        {"name": "Sales", "type": "bar", "data": [120, 200, 150]},
        {"name": "Profit", "type": "line", "data": [80, 150, 100]},
    ],
}

st_echarts(option, height="500px")
```

### Common Chart Types

**Line Chart:**
```python
option = {
    "xAxis": {"type": "category", "data": ["Mon", "Tue", "Wed", "Thu", "Fri"]},
    "yAxis": {"type": "value"},
    "series": [{"type": "line", "data": [820, 932, 901, 934, 1290]}],
}
st_echarts(option)
```

**Pie Chart:**
```python
option = {
    "series": [{
        "type": "pie",
        "radius": ["40%", "70%"],
        "data": [
            {"name": "Category A", "value": 400},
            {"name": "Category B", "value": 300},
            {"name": "Category C", "value": 200},
        ],
    }]
}
st_echarts(option)
```

**Scatter Chart:**
```python
option = {
    "xAxis": {"type": "value"},
    "yAxis": {"type": "value"},
    "series": [{
        "type": "scatter",
        "symbolSize": 20,
        "data": [[10, 20], [15, 30], [25, 18], [30, 25]],
    }]
}
```

### Dynamic Charts with st_echarts

For charts that update based on user input, use `st.session_state` to store options and rerun:

```python
import streamlit as st
from streamlit_echarts import st_echarts

if "chart_option" not in st.session_state:
    st.session_state.chart_option = {
        "xAxis": {"type": "category", "data": ["A", "B", "C"]},
        "yAxis": {"type": "value"},
        "series": [{"type": "bar", "data": [10, 20, 30]}],
    }

tab1, tab2 = st.tabs(["Chart", "Settings"])

with tab1:
    st_echarts(st.session_state.chart_option, height="400px")

with tab2:
    if st.button("Update Data"):
        st.session_state.chart_option["series"][0]["data"] = [30, 50, 20]
        st.rerun()
```

### Chart Themes

```python
st_echarts(option, theme="dark")  # Dark theme
st_echarts(option, theme="light") # Light theme (default)
```

---

## streamlit-option-menu

**Use case:** Horizontal navigation bar with icons and dropdown menus, similar to a website nav.

### Basic Usage

```python
from streamlit_option_menu import option_menu
import streamlit as st

selected = option_menu(
    menu_title="Main Menu",
    options=["Home", "Settings", "About"],
    icons=["house", "gear", "info-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

st.write(f"You selected: {selected}")
```

### With Sub-Navigation

```python
selected = option_menu(
    menu_title="Dashboard",
    options=["Overview", "Analytics", "Reports", "Settings"],
    icons=["grid-1x2", "bar-chart", "file-text", "gear"],
    menu_icon="cast",
    default_index=0,
    styles={
        "container": {"padding": "5px", "background-color": "#f0f0f0"},
        "nav-link": {"font-size": "15px", "text-align": "left"},
        "nav-link-selected": {"background-color": "#4CAF50"},
    }
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `menu_title` | str | Title displayed at top of menu |
| `options` | list | List of menu item labels |
| `icons` | list | Bootstrap Icons names (without "bi-") |
| `menu_icon` | str | Icon for the menu button |
| `default_index` | int | Initially selected item (0-based) |
| `orientation` | str | "horizontal" or "vertical" |
| `styles` | dict | Custom CSS overrides |

### Style Customization

```python
styles = {
    "container": {"padding": "0!important", "background-color": "#1a1a2e"},
    "nav-link": {
        "font-size": "16px",
        "text-align": "left",
        "margin": "0px",
        "padding": "10px 15px",
    },
    "nav-link-selected": {
        "background-color": "#e94560",
    },
    "icon": {"font-size": "18px"},
}
```

---

## streamlit-chatbox

**Use case:** Chat interface for building LLM-powered chatbots or conversational UIs.

### Basic Usage

```python
from streamlit_chatbox import chatbox
import streamlit as st

chatbox.init()

# AI message
chatbox.ai("Hello! How can I help you today?")

# User message
chatbox.user("I need help with my order.")
```

### Full Chat Example with History

```python
from streamlit_chatbox import chatbox
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

chatbox.init()

# Display history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        chatbox.user(msg["content"])
    else:
        chatbox.ai(msg["content"])

# Input
user_input = st.text_input("Your message:", key="user_input")
if st.button("Send"):
    if user_input:
        chatbox.user(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # AI response (placeholder)
        ai_response = f"Echo: {user_input}"
        chatbox.ai(ai_response)
        st.session_state.messages.append({"role": "ai", "content": ai_response})

        st.rerun()
```

### Markdown Support in Chat

```python
chatbox.ai("""
Here is a **bold** and *italic* response.

```python
print("code block")
```

- Item 1
- Item 2
""")
```

### Control Chat Elements

```python
# Clear all messages
chatbox.clear()

# Reset (clear + reset history)
chatbox.reset()

# Show loading indicator
chatbox.ai("Thinking...")  # then update later
```

---

## Combining Extensions

These extensions work well together for rich Streamlit apps:

```python
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, AgGridTheme

# Navigation
page = option_menu(
    menu_title=None,
    options=["Dashboard", "Data Explorer", "Chat"],
    icons=["grid-1x2", "table", "chat-left-text"],
    orientation="horizontal",
)

if page == "Dashboard":
    st.title("Dashboard")

    # ECharts for visualization
    chart_option = {
        "title": {"text": "Revenue"},
        "xAxis": {"type": "category", "data": ["Q1", "Q2", "Q3", "Q4"]},
        "yAxis": {"type": "value"},
        "series": [{"type": "bar", "data": [100, 150, 120, 180]}],
    }
    st_echarts(chart_option, height="350px")

elif page == "Data Explorer":
    st.title("Data Explorer")

    # AgGrid for tabular data
    df = load_data()
    AgGrid(df, theme=AgGridTheme.ALPINE, height=400, pagination=True)

elif page == "Chat":
    st.title("AI Assistant")
    from streamlit_chatbox import chatbox
    chatbox.init()
    # ... chat implementation
```

---

## Dependencies

These packages must be installed:

```
streamlit_aggrid~=1.0.5
streamlit_echarts==0.4.0
streamlit-option-menu==0.3.6
streamlit_chatbox==1.1.11
```

All are already included in the project's `requirements.txt`.