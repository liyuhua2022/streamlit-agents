"""Example: Well-structured Streamlit page demonstrating best practices."""

import streamlit as st
import pandas as pd
from datetime import date
from typing import Optional

# Import from project's utils (non-Streamlit Python)
from src.utils.data_processor import (
    load_dataset,
    filter_by_date_range,
    calculate_summary_stats,
)
from src.components.charts import render_line_chart, render_bar_chart
from src.components.tables import render_data_table


def main() -> None:
    """Main entry point for the Analysis page."""
    _configure_page()
    _init_session_state()

    st.title("📊 Data Analysis")
    st.markdown("Analyze your data with advanced filtering and visualization")

    filters = _render_filters()
    data = _load_and_filter_data(filters)

    if data is not None:
        _render_summary_metrics(data)
        _render_visualizations(data)
        _render_data_table(data)
    else:
        _render_empty_state()


def _configure_page() -> None:
    """Configure page settings."""
    st.set_page_config(
        page_title="Analysis - Data Dashboard",
        page_icon="📊",
        layout="wide",
    )


def _init_session_state() -> None:
    """Initialize required session state variables."""
    defaults: dict[str, object] = {
        "date_range": [],
        "selected_category": "All",
        "chart_type": "line",
        "initialized": True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _render_filters() -> dict[str, object]:
    """Render filter controls and return filter values.

    Returns:
        Dictionary containing filter values.
    """
    st.sidebar.header("🔍 Filters")

    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=st.session_state.date_range,
        help="Filter data by date range",
    )

    # Category filter
    categories = ["All", "Electronics", "Clothing", "Food", "Books"]
    selected_category = st.sidebar.selectbox(
        "Category",
        options=categories,
        index=categories.index(st.session_state.selected_category)
        if st.session_state.selected_category in categories
        else 0,
    )

    # Chart type filter
    chart_options = ["line", "bar", "area"]
    chart_type = st.sidebar.radio(
        "Chart Type",
        options=chart_options,
        index=chart_options.index(st.session_state.chart_type),
    )

    # Update session state
    st.session_state.date_range = date_range
    st.session_state.selected_category = selected_category
    st.session_state.chart_type = chart_type

    return {
        "date_range": date_range,
        "category": selected_category,
        "chart_type": chart_type,
    }


def _load_and_filter_data(filters: dict[str, object]) -> Optional[pd.DataFrame]:
    """Load and filter data based on filter values.

    Args:
        filters: Dictionary containing filter values.

    Returns:
        Filtered DataFrame or None if no data available.
    """
    with st.spinner("Loading data..."):
        try:
            # Use cached data loading
            data = load_dataset("data/sales.csv")

            if data is None:
                return None

            # Apply filters
            if filters["date_range"]:
                data = filter_by_date_range(
                    data,
                    start_date=filters["date_range"][0]
                    if len(filters["date_range"]) > 0
                    else None,
                    end_date=filters["date_range"][1]
                    if len(filters["date_range"]) > 1
                    else None,
                )

            if filters["category"] != "All":
                data = data[data["category"] == filters["category"]]

            return data

        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None


def _render_summary_metrics(data: pd.DataFrame) -> None:
    """Render summary metric cards.

    Args:
        data: DataFrame containing the data to summarize.
    """
    stats = calculate_summary_stats(data)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{stats['record_count']:,}",
        help="Number of records in the dataset",
    )

    col2.metric(
        "Total Revenue",
        f"${stats['total_revenue']:,.2f}",
        help="Sum of all revenue",
    )

    col3.metric(
        "Average Order Value",
        f"${stats['avg_order_value']:,.2f}",
        help="Average revenue per order",
    )

    col4.metric(
        "Unique Customers",
        f"{stats['unique_customers']:,}",
        help="Number of unique customers",
    )


def _render_visualizations(data: pd.DataFrame) -> None:
    """Render data visualizations.

    Args:
        data: DataFrame containing the data to visualize.
    """
    st.subheader("📈 Sales Trend")

    chart_type = st.session_state.chart_type

    if chart_type == "line":
        render_line_chart(data, x="date", y="revenue", title="Revenue Over Time")
    elif chart_type == "bar":
        render_bar_chart(data, x="date", y="revenue", title="Revenue by Date")
    else:
        st.area_chart(data, x="date", y="revenue", use_container_width=True)


def _render_data_table(data: pd.DataFrame) -> None:
    """Render interactive data table.

    Args:
        data: DataFrame containing the data to display.
    """
    st.subheader("📋 Detailed Data")

    # Add download button
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv",
    )

    # Render table with pagination
    render_data_table(
        data,
        page_size=50,
        columns=["date", "category", "product", "revenue", "quantity"],
    )


def _render_empty_state() -> None:
    """Render empty state when no data is available."""
    st.info(
        "📭 No data available for the selected filters. "
        "Please adjust your filter criteria or upload new data."
    )

    if st.button("🔄 Reset Filters"):
        st.session_state.date_range = []
        st.session_state.selected_category = "All"
        st.rerun()


if __name__ == "__main__":
    main()