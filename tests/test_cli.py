import subprocess

def test_cli():
    result = subprocess.run(["ccparser", "4111111111111111|12|2030|123"], capture_output=True, text=True)
    assert "Card Number: 4111 1111 1111 1111" in result.stdout
    assert "Expiry Date: 12/30" in result.stdout
    assert "CVV: 123" in result.stdout
    assert "Card Type: Visa" in result.stdout
    assert "Valid: True" in result.stdout