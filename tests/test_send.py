from send import is_retryable_status

def test_status_code_400_is_permanent():
    assert is_retryable_status(400) is False

def test_status_code_404_is_permanent():
    assert is_retryable_status(404) is False

def test_status_code_408_is_retryable():
    assert is_retryable_status(408) is True

def test_status_code_429_is_retryable():
    assert is_retryable_status(429) is True

def test_status_code_499_is_permanent():
    assert is_retryable_status(499) is False

def test_status_code_500_is_retryable():
    assert is_retryable_status(500) is True

def test_status_code_503_is_retryable():
    assert is_retryable_status(503) is True

def test_status_code_599_is_retryable():
    assert is_retryable_status(599) is True

def test_status_code_600_is_permanent():
    assert is_retryable_status(600) is False


