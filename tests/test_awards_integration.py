import os
from fastapi.testclient import TestClient
from pathlib import Path
from app.main import create_app

def test_awards_intervals_integration(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    csv_path = tmp_path / "movies.csv"
    csv_path.write_text(
        "year;title;studios;producers;winner\n"
        "1990;A;S;Producer A, Producer B;yes\n"
        "2000;B;S;Producer A;YES\n"
        "2001;C;S;Producer A and Producer B; yes \n"
        "2010;D;S;Producer A;\n"
        "1991;E;S;Producer B;yes\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CSV_PATH", str(csv_path))

    app = create_app()

    with TestClient(app) as client:
        resp = client.get("/api/producers/awards-intervals")

    assert resp.status_code == 200
    data = resp.json()
    print(data)

    assert "min" in data and "max" in data
    assert isinstance(data["min"], list)
    assert isinstance(data["max"], list)

    min_set = {(i["producer"], i["interval"], i["previousWin"], i["followingWin"]) for i in data["min"]}
    max_set = {(i["producer"], i["interval"], i["previousWin"], i["followingWin"]) for i in data["max"]}

    assert ("Producer A", 1, 2000, 2001) in min_set
    assert ("Producer B", 1, 1990, 1991) in min_set

    assert ("Producer A", 10, 1990, 2000) in max_set
    assert ("Producer B", 10, 1991, 2001) in max_set

def test_awards_intervals_integration_csv(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    project_csv = Path(__file__).resolve().parents[1] / "app" / "data" / "movielist.csv"
    monkeypatch.setenv("CSV_PATH", str(project_csv))

    app = create_app()

    with TestClient(app) as client:
        resp = client.get("/api/producers/awards-intervals")

    assert resp.status_code == 200
    data = resp.json()
    print(data)

    assert "min" in data and "max" in data
    assert isinstance(data["min"], list)
    assert isinstance(data["max"], list)

    min_set = {(i["producer"], i["interval"], i["previousWin"], i["followingWin"]) for i in data["min"]}
    max_set = {(i["producer"], i["interval"], i["previousWin"], i["followingWin"]) for i in data["max"]}

    assert ("Joel Silver", 1, 1990, 1991) in min_set    
    assert ("Matthew Vaughn", 13, 2002, 2015) in max_set