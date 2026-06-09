# Streamlit Best Practices — Quick Reference

## Common Commands

```bash
# Run Streamlit app
streamlit run src/app.py

# Run with specific port
streamlit run src/app.py --server.port 8501

# Run in headless mode (for deployment)
streamlit run src/app.py --server.headless true

# Show Streamlit config
streamlit config show

# Clear cache
streamlit cache clear
```

## Session State

```python
# Initialize
if "key" not in st.session_state:
    st.session_state.key = default_value

# Access with default
value = st.session_state.get("key", default_value)

# Update
st.session_state.key = new_value

# Clear all
for key in list(st.session_state.keys()):
    del st.session_state[key]
```

## Caching

```python
# Data fetching (TTL = 1 hour)
@st.cache_data(ttl=3600, show_spinner="Loading...")
def fetch_data(endpoint: str) -> pd.DataFrame:
    ...

# ML models, DB connections
@st.cache_resource
def load_model(path: str):
    ...

# Clear specific cache
fetch_data.clear()
load_model.clear()
```

## Page Structure

```python
# src/pages/1_home.py
import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")
st.title("🏠 Home")
# ... content
```

## Common Widget Patterns

```python
# Form
with st.form(key="my_form"):
    name = st.text_input("Name")
    submitted = st.form_submit_button("Submit")
    if submitted:
        process(name)

# Callbacks
def on_change():
    st.session_state.selected = st.session_state._temp

st.selectbox("Options", ["A", "B"], key="_temp", on_change=on_change)

# Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Label", "Value")

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Content 1")
```

## Error Handling

```python
try:
    result = risky_operation()
except SpecificError as e:
    st.error(f"Error: {e}")
    logger.error(f"Details: {e}")
    result = None

if result is None:
    st.info("No data available")
else:
    st.dataframe(result)
```

## Data Display

```python
# Table
st.dataframe(df, use_container_width=True)

# Editable table
st.data_editor(df)

# Chart
st.line_chart(df)
st.bar_chart(df)
st.plotly_chart(fig)

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Label", "Value", "delta")
```

## Project Structure Template

```
my-app/
├── src/
│   ├── app.py              # Main entry
│   ├── pages/
│   │   ├── 1_home.py
│   │   ├── 2_analysis.py
│   │   └── 3_settings.py
│   ├── components/
│   │   ├── charts.py
│   │   └── tables.py
│   └── utils/
│       ├── data.py
│       └── api.py
├── tests/
├── pyproject.toml
└── .streamlit/
    └── config.toml
```

## Config.toml Example

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[theme]
primaryColor = "#4F46E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[client]
showErrorDetails = false
```

## Testing

```python
from streamlit.testing.v1 import AppTest

def test_page_loads():
    app = AppTest.from_file("src/pages/home.py")
    app.run()
    assert app.title[0].value == "Home"
```

## Performance Tips

1. Use `use_container_width=True` for responsive charts
2. Cache expensive computations with `@st.cache_data`
3. Use `st.empty()` for conditional content
4. Limit data with pagination for large datasets
5. Use `st.fragment` for partial reruns (Streamlit 1.28+)