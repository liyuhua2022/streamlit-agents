import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth import load_auth_data, save_auth_data, verify_user, is_authenticated, login_user, logout_user


class TestLoadAuthData:
    """测试 load_auth_data() 函数"""

    def test_file_exists_normal_load(self):
        """文件存在正常加载"""
        test_data = {"username": "admin", "login_time": "2026-06-08T10:30:00"}
        with patch("auth.AUTH_FILE", Path("/tmp/test_auth_data.json")):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
                    result = load_auth_data()
                    assert result == test_data

    def test_file_not_exists_return_empty_dict(self):
        """文件不存在返回空字典"""
        with patch("auth.AUTH_FILE", Path("/tmp/test_auth_data.json")):
            with patch("pathlib.Path.exists", return_value=False):
                result = load_auth_data()
                assert result == {}

    def test_empty_json_file_return_empty_dict(self):
        """空 JSON 文件返回空字典"""
        with patch("auth.AUTH_FILE", Path("/tmp/test_auth_data.json")):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("builtins.open", mock_open(read_data="")):
                    result = load_auth_data()
                    assert result == {}


class TestSaveAuthData:
    """测试 save_auth_data() 函数"""

    def test_save_new_file(self):
        """保存新文件"""
        test_data = {"username": "admin", "login_time": "2026-06-08T10:30:00"}
        with patch("auth.AUTH_FILE", Path("/tmp/test_auth_data.json")):
            with patch("builtins.open", mock_open()) as mock_file:
                save_auth_data(test_data)
                mock_file.assert_called_once_with(Path("/tmp/test_auth_data.json"), "w", encoding="utf-8")

    def test_overwrite_existing_file(self):
        """覆盖已有文件"""
        test_data = {"username": "admin", "login_time": "2026-06-08T11:00:00"}
        with patch("auth.AUTH_FILE", Path("/tmp/test_auth_data.json")):
            with patch("builtins.open", mock_open()) as mock_file:
                save_auth_data(test_data)
                mock_file.assert_called_once()


class TestVerifyUser:
    """测试 verify_user() 函数"""

    def test_correct_credentials_return_true(self):
        """正确组合返回 True"""
        assert verify_user("admin", "admin123") is True

    def test_wrong_credentials_return_false(self):
        """错误组合返回 False"""
        assert verify_user("admin", "wrongpassword") is False
        assert verify_user("wronguser", "admin123") is False
        assert verify_user("wronguser", "wrongpassword") is False

    def test_empty_values_return_false(self):
        """空值返回 False"""
        assert verify_user("", "admin123") is False
        assert verify_user("admin", "") is False
        assert verify_user("", "") is False
        assert verify_user(None, "admin123") is False
        assert verify_user("admin", None) is False


class TestIsAuthenticated:
    """测试 is_authenticated()"""

    def test_logged_in_returns_true(self):
        """当 session_state.authenticated == True 时返回 True"""
        mock_session = {"authenticated": True, "username": "admin"}
        with patch("streamlit.session_state", mock_session):
            assert is_authenticated() is True

    def test_not_logged_in_returns_false(self):
        """当 session_state.authenticated == False 或不存在时返回 False"""
        mock_session = {"authenticated": False}
        with patch("streamlit.session_state", mock_session):
            assert is_authenticated() is False


class TestLoginUser:
    """测试 login_user()"""

    def test_login_user_updates_session_state(self):
        """登录用户更新 session_state"""
        mock_session = MagicMock()
        with patch("streamlit.session_state", mock_session):
            login_user("admin")
            assert mock_session.authenticated is True
            assert mock_session.username == "admin"

    def test_login_user_saves_to_file(self):
        """登录用户保存数据到 auth_data.json"""
        mock_session = MagicMock()
        with patch("streamlit.session_state", mock_session):
            with patch("auth.save_auth_data") as mock_save:
                login_user("admin")
                mock_save.assert_called_once()
                call_args = mock_save.call_args[0][0]
                assert call_args["username"] == "admin"
                assert "login_time" in call_args


class TestLogoutUser:
    """测试 logout_user()"""

    def test_logout_user_clears_session_state(self):
        """注销用户清除 session_state"""
        mock_session = MagicMock()
        mock_session.authenticated = True
        mock_session.username = "admin"
        with patch("streamlit.session_state", mock_session):
            logout_user()
            assert mock_session.authenticated is False
            assert mock_session.username is None

    def test_logout_user_clears_auth_file(self):
        """注销用户清除 auth_data.json"""
        mock_session = MagicMock()
        mock_session.authenticated = False
        mock_session.username = None
        with patch("streamlit.session_state", mock_session):
            with patch("auth.AUTH_FILE") as mock_file:
                mock_file.exists = MagicMock(return_value=True)
                mock_file.unlink = MagicMock()
                logout_user()
                mock_file.unlink.assert_called_once()