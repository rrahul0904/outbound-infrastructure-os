from pathlib import Path

def test_foundation_files_exist():
    service = Path(__file__).resolve().parents[1]
    assert (service / "app" / "main.py").exists()
    assert (service.parents[1] / "infra" / "postgres" / "001_init.sql").exists()
