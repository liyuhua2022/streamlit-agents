"""Example: Caching patterns for Streamlit applications."""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps


# =============================================================================
# Pattern 1: st.cache_data for API calls and data fetching
# =============================================================================

@st.cache_data(ttl=3600, show_spinner="Fetching data from API...")
def fetch_api_data(endpoint: str, params: dict[str, str]) -> dict:
    """Fetch data from external API with 1-hour cache.

    Args:
        endpoint: API endpoint URL
        params: Query parameters

    Returns:
        Dictionary containing API response data
    """
    import time
    import requests

    # Simulate API call
    time.sleep(1)  # Simulate network latency

    response = requests.get(endpoint, params=params)
    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=1800, show_spinner="Loading dataset...")
def load_csv_data(file_path: str, parse_dates: bool = True) -> pd.DataFrame:
    """Load CSV file with 30-minute cache.

    Args:
        file_path: Path to CSV file
        parse_dates: Whether to parse date columns

    Returns:
        DataFrame containing the loaded data
    """
    df = pd.read_csv(file_path)

    if parse_dates:
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


# =============================================================================
# Pattern 2: st.cache_resource for ML models and heavy resources
# =============================================================================

@st.cache_resource
def load_ml_model(model_path: str):
    """Load ML model once, reuse across sessions.

    Args:
        model_path: Path to the model file

    Returns:
        Loaded model object
    """
    import joblib

    model = joblib.load(model_path)
    return model


@st.cache_resource
def init_database_connection(db_path: str):
    """Initialize database connection with caching.

    Args:
        db_path: Path to SQLite database file

    Returns:
        Database connection object
    """
    import sqlite3

    conn = sqlite3.connect(db_path)
    return conn


@st.cache_resource
def download_and_cache_model(model_url: str, cache_dir: str):
    """Download and cache a model from URL.

    Args:
        model_url: URL to download model from
        cache_dir: Directory to cache model in

    Returns:
        Path to cached model file
    """
    import os
    import hashlib
    from pathlib import Path
    import requests

    # Create cache directory
    Path(cache_dir).mkdir(parents=True, exist_ok=True)

    # Generate cache filename from URL hash
    cache_key = hashlib.md5(model_url.encode()).hexdigest()
    cached_path = Path(cache_dir) / f"{cache_key}.model"

    # Download if not cached
    if not cached_path.exists():
        response = requests.get(model_url, stream=True)
        response.raise_for_status()

        with open(cached_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    return str(cached_path)


# =============================================================================
# Pattern 3: Caching with parameters
# =============================================================================

@st.cache_data(ttl=600)
def compute_aggregations(
    df: pd.DataFrame,
    group_by_columns: list[str],
    agg_functions: list[str],
) -> pd.DataFrame:
    """Compute aggregations on DataFrame with caching.

    Args:
        df: Input DataFrame
        group_by_columns: Columns to group by
        agg_functions: Aggregation functions to apply

    Returns:
        Aggregated DataFrame
    """
    return df.groupby(group_by_columns).agg(agg_functions).reset_index()


@st.cache_data(ttl=300)
def filter_dataframe(
    df: pd.DataFrame,
    filter_conditions: dict[str, tuple],
) -> pd.DataFrame:
    """Filter DataFrame based on conditions with caching.

    Args:
        df: Input DataFrame
        filter_conditions: Dictionary mapping column names to
                          (operator, value) tuples

    Returns:
        Filtered DataFrame
    """
    result = df.copy()

    for column, (operator, value) in filter_conditions.items():
        if operator == "==":
            result = result[result[column] == value]
        elif operator == "!=":
            result = result[result[column] != value]
        elif operator == ">":
            result = result[result[column] > value]
        elif operator == ">=":
            result = result[result[column] >= value]
        elif operator == "<":
            result = result[result[column] < value]
        elif operator == "<=":
            result = result[result[column] <= value]
        elif operator == "in":
            result = result[result[column].isin(value)]
        elif operator == "contains":
            result = result[result[column].str.contains(value, na=False)]

    return result


# =============================================================================
# Pattern 4: Manual cache for complex state management
# =============================================================================

def get_manual_cache(key: str, factory_func, ttl_seconds: int = 3600):
    """Get or create cached value with TTL.

    This is useful when st.cache decorators don't fit the use case.

    Args:
        key: Cache key
        factory_func: Function to create value if not cached
        ttl_seconds: Time to live in seconds

    Returns:
        Cached value
    """
    if "manual_cache" not in st.session_state:
        st.session_state.manual_cache = {}

    cache = st.session_state.manual_cache

    if key in cache:
        cached_value, timestamp = cache[key]
        if datetime.now().timestamp() - timestamp < ttl_seconds:
            return cached_value

    # Create new value
    value = factory_func()
    cache[key] = (value, datetime.now().timestamp())

    return value


def clear_manual_cache(key: Optional[str] = None) -> None:
    """Clear manual cache entries.

    Args:
        key: Specific key to clear, or None to clear all
    """
    if "manual_cache" not in st.session_state:
        return

    if key is None:
        st.session_state.manual_cache = {}
    elif key in st.session_state.manual_cache:
        del st.session_state.manual_cache[key]


# =============================================================================
# Pattern 5: Caching expensive computations with large datasets
# =============================================================================

@st.cache_data(ttl=900, show_spinner="Processing data...")
def process_large_dataset(
    file_path: str,
    chunk_size: int = 10000,
    normalize: bool = True,
) -> pd.DataFrame:
    """Process large dataset in chunks with caching.

    Args:
        file_path: Path to CSV file
        chunk_size: Size of chunks to process
        normalize: Whether to normalize values

    Returns:
        Processed DataFrame
    """
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process each chunk
        if normalize:
            for col in chunk.select_dtypes(include=[np.number]).columns:
                chunk[col] = (chunk[col] - chunk[col].mean()) / chunk[col].std()

        chunks.append(chunk)

    return pd.concat(chunks, ignore_index=True)


# =============================================================================
# Pattern 6: Clear specific cache functions
# =============================================================================

def clear_all_caches() -> None:
    """Clear all cached data and resources."""
    st.cache_data.clear()
    st.cache_resource.clear()


def clear_specific_cache(cache_func, *args, **kwargs) -> None:
    """Clear a specific cache function.

    Args:
        cache_func: The cached function to clear
        *args: Positional arguments for the cache function
        **kwargs: Keyword arguments for the cache function
    """
    cache_func.clear(*args, **kwargs)


# =============================================================================
# Example usage in Streamlit page
# =============================================================================

def demonstrate_caching() -> None:
    """Demonstrate caching patterns in a Streamlit page."""
    st.title("📦 Caching Patterns Demo")

    # Example 1: Load data with cache
    st.header("Data Loading with Cache")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        # This will cache the data for subsequent renders
        df = load_csv_data(uploaded_file.name)
        st.dataframe(df)

        # Show cache info
        st.caching()
        st.info(f"Cached data shape: {df.shape}")

    # Example 2: Model loading with cache
    st.header("ML Model Loading")

    model_path = st.text_input("Model path", "models/classifier.pkl")

    if model_path:
        with st.spinner("Loading model..."):
            model = load_ml_model(model_path)
        st.success("Model loaded (cached)")

    # Example 3: Clear cache button
    st.header("Cache Management")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Clear all caches"):
            clear_all_caches()
            st.rerun()

    with col2:
        if st.button("Clear manual cache"):
            clear_manual_cache()
            st.rerun()


if __name__ == "__main__":
    demonstrate_caching()