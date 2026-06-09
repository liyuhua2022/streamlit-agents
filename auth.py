import json
import os
from pathlib import Path
from datetime import datetime

AUTH_FILE = Path("auth_data.json")

# Default credentials for demonstration purposes only.
# In production, use environment variables: APP_USERNAME, APP_PASSWORD
DEFAULT_USERNAME = os.environ.get("APP_USERNAME", "admin")
DEFAULT_PASSWORD = os.environ.get("APP_PASSWORD", "admin123")


def load_auth_data() -> dict:
    """加载 auth_data.json，如果不存在返回空字典"""
    if not AUTH_FILE.exists():
        return {}
    try:
        with open(AUTH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_auth_data(data: dict) -> None:
    """保存数据到 auth_data.json"""
    try:
        with open(AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        import streamlit as st
        st.error(f"保存失败: {e}")


def verify_user(username: str, password: str) -> bool:
    """验证用户名密码组合是否正确（admin/admin123）"""
    if not username or not password:
        return False
    return username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD


def is_authenticated() -> bool:
    """检查当前是否已认证（通过 session_state）"""
    import streamlit as st
    return st.session_state.get("authenticated", False)


def login_user(username: str) -> None:
    """登录用户：更新 session_state 和 auth_data.json"""
    import streamlit as st
    st.session_state.authenticated = True
    st.session_state.username = username
    save_auth_data({
        "username": username,
        "login_time": datetime.now().isoformat()
    })


def logout_user() -> None:
    """注销用户：清除 session_state 和 auth_data.json"""
    import streamlit as st
    st.session_state.authenticated = False
    st.session_state.username = None
    try:
        if AUTH_FILE.exists():
            AUTH_FILE.unlink()
    except OSError:
        pass  # Ignore file deletion failures