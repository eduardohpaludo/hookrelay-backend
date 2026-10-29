import pytest
import requests

from send import is_retryable_status, send_webhook


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code == 500:
            raise requests.exceptions.HTTPError("500")


def test_send_webhook_success(monkeypatch):
    def fake_post(url, **kwargs):
        return FakeResponse(200)

    monkeypatch.setattr(requests, "post", fake_post)

    result = send_webhook("http://any.url", {"event": "test"})

    assert result["ok"] is True
    assert result["status_code"] == 200
    assert result["error"] is None
    assert result["retryable"] is False


def test_send_webhook_error_500(monkeypatch):
    def fake_post(url, **kwargs):
        return FakeResponse(500)

    monkeypatch.setattr(requests, "post", fake_post)

    result = send_webhook("http://any.url", {"event": "test"})

    assert result["ok"] is False
    assert result["status_code"] == 500
    assert "500" in result["error"]
    assert result["retryable"] is True


def test_send_webhook_error_timeout(monkeypatch):
    def fake_post(url, **kwargs):
        raise requests.exceptions.Timeout("Timeout")

    monkeypatch.setattr(requests, "post", fake_post)

    result = send_webhook("http://any.url", {"event": "test"})

    assert result["ok"] is False
    assert result["error"] == "Timeout"
    assert result["status_code"] is None
    assert result["retryable"] is True


@pytest.mark.parametrize(
    "status_code, is_retryable",
    [
        (400, False),
        (404, False),
        (408, True),
        (429, True),
        (499, False),
        (500, True),
        (503, True),
        (599, True),
        (600, False),
    ],
)
def test_status_code(status_code, is_retryable):
    assert is_retryable_status(status_code) is is_retryable
