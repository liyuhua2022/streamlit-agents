import streamlit as st
from auth import verify_user, login_user, logout_user, is_authenticated, load_auth_data

# 页面配置
st.set_page_config(page_title="登录应用", page_icon="🔐")

# 初始化会话状态（尝试从持久化存储恢复）
if "authenticated" not in st.session_state:
    auth_data = load_auth_data()
    st.session_state.authenticated = bool(auth_data.get("username"))
    st.session_state.username = auth_data.get("username")


def main():
    if st.session_state.authenticated:
        # 主页
        st.title(f"欢迎回来，{st.session_state.username}！")
        st.success("你已成功登录。")
        if st.button("注销"):
            logout_user()
            st.rerun()
    else:
        # 登录页
        st.title("🔐 登录")
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")

        if st.button("登录"):
            if verify_user(username, password):
                login_user(username)
                st.rerun()
            else:
                st.error("Invalid username or password")

        # 显示注册信息提示
        st.info("演示账号: admin / admin123")


if __name__ == "__main__":
    main()