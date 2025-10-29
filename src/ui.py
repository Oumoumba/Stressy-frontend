import streamlit as st

def inject_theme_class(light: bool) -> None:
    """
    Adds 'light' class to <html> when light=True so our CSS switches themes.
    Call this once per page after reading the sidebar toggles.
    """
    cls = "light" if light else ""
    st.markdown(f"<script>document.documentElement.className='{cls}'</script>", unsafe_allow_html=True)

def stress_badge(level: str) -> None:
    """
    Pills for Low / Moderate / High stress.
    """
    color = {"Low": "#22c55e", "Moderate": "#f59e0b", "High": "#ef4444"}.get(level, "#9aa3ad")
    st.markdown(
        f'''
        <span class="badge">
            <span class="dot" style="background:{color}"></span>
            <b>{level}</b>
        </span>
        ''',
        unsafe_allow_html=True
    )

def kpi(label: str, value: str, sub: str | None = None) -> None:
    """
    Compact KPI card. Example: kpi("Current EDA", "0.52", "+0.03 vs 1h")
    """
    sub_html = f'<div class="label" style="margin-top:4px;opacity:.7">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="kpi">
          <div class="label">{label}</div>
          <div class="value">{value}</div>
          {sub_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def header(title: str, subtitle: str = "") -> None:
    """
    Simple sticky header used at the top of the page.
    """
    st.markdown(
        f"""
        <div class="app-header">
          <div class="app-title">{title}</div>
          <div class="app-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
)

