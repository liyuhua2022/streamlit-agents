"""Example: Reusable Streamlit components for building composable UIs."""

import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from typing import Callable, Any, Optional, Protocol
from dataclasses import dataclass


# =============================================================================
# Component: Metric Cards
# =============================================================================

@dataclass
class MetricCardConfig:
    """Configuration for a metric card."""
    label: str
    value: str | float | int
    delta: Optional[str] = None
    help: Optional[str] = None


def render_metric_cards(metrics: list[MetricCardConfig], columns: int = 4) -> None:
    """Render a row of metric cards.

    Args:
        metrics: List of MetricCardConfig objects
        columns: Number of columns to display (default 4)
    """
    cols = st.columns(min(columns, len(metrics)))

    for idx, metric in enumerate(metrics):
        with cols[idx % columns]:
            if metric.delta:
                st.metric(
                    label=metric.label,
                    value=metric.value,
                    delta=metric.delta,
                    help=metric.help,
                )
            else:
                st.metric(
                    label=metric.label,
                    value=metric.value,
                    help=metric.help,
                )


# =============================================================================
# Component: Chart Renderer
# =============================================================================

class ChartRenderer:
    """Reusable chart rendering component."""

    @staticmethod
    def line_chart(
        df: pd.DataFrame,
        x: str,
        y: str,
        title: str = "",
        height: int = 400,
        color: Optional[str] = None,
    ) -> None:
        """Render a line chart using Plotly.

        Args:
            df: DataFrame with chart data
            x: Column name for x-axis
            y: Column name for y-axis
            title: Chart title
            height: Chart height in pixels
            color: Optional column for color encoding
        """
        fig = px.line(
            df,
            x=x,
            y=y,
            title=title,
            color=color,
            template="plotly_white",
        )
        fig.update_layout(height=height, margin=dict(l=20, r=20, t=40, b=20))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="#E5E5E5")
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def bar_chart(
        df: pd.DataFrame,
        x: str,
        y: str,
        title: str = "",
        height: int = 400,
        orientation: str = "v",
    ) -> None:
        """Render a bar chart using Plotly.

        Args:
            df: DataFrame with chart data
            x: Column name for x-axis
            y: Column name for y-axis
            title: Chart title
            height: Chart height in pixels
            orientation: 'v' for vertical, 'h' for horizontal
        """
        fig = px.bar(
            df,
            x=x,
            y=y,
            title=title,
            orientation=orientation,
            template="plotly_white",
        )
        fig.update_layout(height=height, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def scatter_chart(
        df: pd.DataFrame,
        x: str,
        y: str,
        size: Optional[str] = None,
        color: Optional[str] = None,
        title: str = "",
        height: int = 400,
    ) -> None:
        """Render a scatter chart using Plotly.

        Args:
            df: DataFrame with chart data
            x: Column name for x-axis
            y: Column name for y-axis
            size: Optional column for point size
            color: Optional column for color encoding
            title: Chart title
            height: Chart height in pixels
        """
        fig = px.scatter(
            df,
            x=x,
            y=y,
            size=size,
            color=color,
            title=title,
            template="plotly_white",
        )
        fig.update_layout(height=height, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def pie_chart(
        df: pd.DataFrame,
        values: str,
        names: str,
        title: str = "",
        height: int = 400,
    ) -> None:
        """Render a pie chart using Plotly.

        Args:
            df: DataFrame with chart data
            values: Column name for values
            names: Column name for labels
            title: Chart title
            height: Chart height in pixels
        """
        fig = px.pie(
            df,
            values=values,
            names=names,
            title=title,
            template="plotly_white",
        )
        fig.update_layout(height=height, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# Component: Filter Form
# =============================================================================

@dataclass
class FilterField:
    """Configuration for a filter field."""
    key: str
    label: str
    field_type: str  # "select", "text", "date", "number", "multiselect"
    options: Optional[list[Any]] = None
    default: Any = None
    help: Optional[str] = None


class FilterForm:
    """Reusable filter form component."""

    def __init__(self, fields: list[FilterField], key: str = "filter_form"):
        """Initialize the filter form.

        Args:
            fields: List of FilterField configurations
            key: Unique key for this form instance
        """
        self.fields = fields
        self.key = key

    def render(self, on_submit: Callable[[dict[str, Any]], None]) -> None:
        """Render the filter form.

        Args:
            on_submit: Callback function when form is submitted
        """
        with st.form(key=self.key):
            cols = st.columns(min(3, len(self.fields)))

            values = {}
            for idx, field in enumerate(self.fields):
                with cols[idx % 3]:
                    values[field.key] = self._render_field(field)

            submitted = st.form_submit_button(
                "Apply Filters",
                type="primary",
                use_container_width=True,
            )

            if submitted:
                on_submit(values)

    def _render_field(self, field: FilterField) -> Any:
        """Render a single filter field.

        Args:
            field: FilterField configuration

        Returns:
            The value from the rendered field
        """
        if field.field_type == "select":
            return st.selectbox(
                field.label,
                options=field.options or [],
                index=field.options.index(field.default)
                if field.default in (field.options or [])
                else 0,
                help=field.help,
            )
        elif field.field_type == "text":
            return st.text_input(
                field.label,
                value=field.default or "",
                help=field.help,
            )
        elif field.field_type == "date":
            return st.date_input(
                field.label,
                value=field.default,
                help=field.help,
            )
        elif field.field_type == "number":
            return st.number_input(
                field.label,
                value=field.default or 0,
                help=field.help,
            )
        elif field.field_type == "multiselect":
            return st.multiselect(
                field.label,
                options=field.options or [],
                default=field.default,
                help=field.help,
            )


# =============================================================================
# Component: Data Table with Pagination
# =============================================================================

@dataclass
class TableConfig:
    """Configuration for a data table."""
    page_size: int = 25
    columns: Optional[list[str]] = None
    hide_index: bool = True


def render_data_table(
    df: pd.DataFrame,
    config: Optional[TableConfig] = None,
) -> None:
    """Render a paginated data table.

    Args:
        df: DataFrame to display
        config: Optional TableConfig object
    """
    if config is None:
        config = TableConfig()

    # Filter columns
    display_df = df[config.columns] if config.columns else df

    # Pagination
    total_pages = max(1, (len(display_df) + config.page_size - 1) // config.page_size)

    if total_pages > 1:
        page = st.number_input(
            f"Page (of {total_pages})",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
        )
        start_idx = (page - 1) * config.page_size
        end_idx = start_idx + config.page_size
        display_df = display_df.iloc[start_idx:end_idx]
    else:
        st.caption(f"Showing all {len(display_df)} rows")

    st.dataframe(
        display_df,
        hide_index=config.hide_index,
        use_container_width=True,
    )


# =============================================================================
# Component: Download Button
# =============================================================================

def render_download_button(
    data: str | bytes,
    filename: str,
    label: str = "Download",
    mime: str = "text/csv",
) -> None:
    """Render a download button.

    Args:
        data: Content to download
        filename: Filename for download
        label: Button label
        mime: MIME type for content
    """
    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime,
    )


# =============================================================================
# Component: Empty State
# =============================================================================

def render_empty_state(
    icon: str = "📭",
    title: str = "No Data",
    message: str = "No data available for the selected filters.",
    action_label: Optional[str] = None,
    action_callback: Optional[Callable[[], None]] = None,
) -> None:
    """Render an empty state message.

    Args:
        icon: Icon to display
        title: Empty state title
        message: Description message
        action_label: Optional button label
        action_callback: Optional button callback
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>{icon}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center;'>{title}</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'>{message}</p>", unsafe_allow_html=True)

        if action_label and action_callback:
            st.button(action_label, on_click=action_callback, type="primary")


# =============================================================================
# Component: Tabs with Content
# =============================================================================

class TabContainer:
    """Container for tabbed content."""

    def __init__(self, tabs: list[str]):
        """Initialize tab container.

        Args:
            tabs: List of tab names
        """
        self.tab_objects = st.tabs(tabs)

    def render(self, tab_name: str, content_func: Callable[[], None]) -> None:
        """Render content in a specific tab.

        Args:
            tab_name: Name of the tab to render content in
            content_func: Function that renders the content
        """
        # Find tab index
        # Note: st.tabs doesn't provide named access, so this requires tracking
        pass


# =============================================================================
# Example Usage
# =============================================================================

def demo_components() -> None:
    """Demonstrate all components in a sample page."""
    st.title("🎨 Component Library Demo")

    # Demo Metric Cards
    st.header("Metric Cards")
    metrics = [
        MetricCardConfig("Total Revenue", "$125,430", "+12.5%", "Total revenue this month"),
        MetricCardConfig("Orders", "1,234", "+8.2%", "Total orders placed"),
        MetricCardConfig("Avg Order Value", "$101.65", "-2.3%", "Average order value"),
        MetricCardConfig("Active Users", "892", "+15.7%", "Users active today"),
    ]
    render_metric_cards(metrics, columns=4)

    # Demo Chart
    st.header("Charts")
    chart_type = st.selectbox("Chart Type", ["line", "bar", "scatter", "pie"])

    # Sample data
    sample_df = pd.DataFrame({
        "category": ["A", "B", "C", "D", "E"],
        "values": [100, 200, 150, 300, 250],
        "values2": [50, 100, 75, 150, 125],
    })

    if chart_type == "line":
        ChartRenderer.line_chart(sample_df, "category", "values", title="Line Chart")
    elif chart_type == "bar":
        ChartRenderer.bar_chart(sample_df, "category", "values", title="Bar Chart")
    elif chart_type == "scatter":
        ChartRenderer.scatter_chart(sample_df, "values", "values2", title="Scatter Chart")
    elif chart_type == "pie":
        ChartRenderer.pie_chart(sample_df, "values", "category", title="Pie Chart")

    # Demo Filter Form
    st.header("Filter Form")
    filters = [
        FilterField("category", "Category", "select", ["All", "A", "B", "C"]),
        FilterField("date_range", "Date Range", "date"),
        FilterField("search", "Search", "text"),
    ]

    form = FilterForm(filters, key="demo_filter")

    def on_filter_submit(values):
        st.session_state.filter_values = values
        st.rerun()

    form.render(on_filter_submit)

    if "filter_values" in st.session_state:
        st.json(st.session_state.filter_values)

    # Demo Data Table
    st.header("Data Table")
    render_data_table(sample_df, TableConfig(page_size=5))

    # Demo Empty State
    st.header("Empty State")
    render_empty_state(
        icon="📭",
        title="No Results",
        message="No data matches your filters. Try adjusting your criteria.",
        action_label="Clear Filters",
        action_callback=lambda: st.info("Filters cleared!"),
    )


if __name__ == "__main__":
    demo_components()