import uuid

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e

PASSWORD = "SecurePass123!"


def _unique_user() -> dict:
    suffix = uuid.uuid4().hex[:10]
    return {
        "username": f"user_{suffix}",
        "email": f"user_{suffix}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": PASSWORD,
    }


def _fill_register(page: Page, base_url: str, user: dict, password: str, confirm: str):
    page.goto(f"{base_url}register")
    page.fill("#username", user["username"])
    page.fill("#email", user["email"])
    page.fill("#first_name", user["first_name"])
    page.fill("#last_name", user["last_name"])
    page.fill("#password", password)
    page.fill("#confirm_password", confirm)
    page.click("button[type=submit]")


def _register_via_ui(page: Page, base_url: str, user: dict):
    _fill_register(page, base_url, user, user["password"], user["password"])
    expect(page.locator("#successMessage")).to_contain_text("Registration successful")


def _login(page: Page, base_url: str, username: str, password: str):
    page.goto(f"{base_url}login")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button[type=submit]")


def test_register_positive(page: Page, fastapi_server: str):
    _register_via_ui(page, fastapi_server, _unique_user())


def test_login_positive(page: Page, fastapi_server: str):
    user = _unique_user()
    _register_via_ui(page, fastapi_server, user)

    _login(page, fastapi_server, user["username"], user["password"])
    expect(page.locator("#successMessage")).to_contain_text("Login successful")
    page.wait_for_url("**/dashboard")
    assert page.evaluate("localStorage.getItem('access_token')")


def test_register_short_password_negative(page: Page, fastapi_server: str):
    user = _unique_user()
    _fill_register(page, fastapi_server, user, "Ab1!", "Ab1!")
    expect(page.locator("#errorMessage")).to_contain_text("at least 8 characters")


def test_login_wrong_password_negative(page: Page, fastapi_server: str):
    user = _unique_user()
    _register_via_ui(page, fastapi_server, user)

    _login(page, fastapi_server, user["username"], "WrongPass999!")
    expect(page.locator("#errorAlert")).to_be_visible()
    expect(page.locator("#errorMessage")).to_contain_text("Invalid")
    assert page.evaluate("localStorage.getItem('access_token')") is None
