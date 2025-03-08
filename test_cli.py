import subprocess

def test_cli():
    result = subprocess.run(["ccparser", "4783400008389576|04|2027|744"], capture_output=True, text=True)
    assert "Card Number: 4783 4000 0838 9576" in result.stdout
    assert "Expiry Date: 04/27" in result.stdout
    assert "CVV: 744" in result.stdout
    assert "Card Type: Visa" in result.stdout
    assert "Valid: True" in result.stdout