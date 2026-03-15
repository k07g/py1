from unittest.mock import patch

# database モジュールをモック対象のパスで指定
DB = "src.routers.books.database"


class TestCreateBook:
    def test_success(self, client, sample_book):
        with patch(f"{DB}.put_book", return_value=sample_book):
            resp = client.post("/books", json={"title": "Clean Code", "author": "Robert C. Martin"})

        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Clean Code"
        assert data["author"] == "Robert C. Martin"
        assert "id" in data
        assert "created_at" in data

    def test_missing_title(self, client):
        resp = client.post("/books", json={"author": "Someone"})
        assert resp.status_code == 422

    def test_missing_author(self, client):
        resp = client.post("/books", json={"title": "Some Book"})
        assert resp.status_code == 422

    def test_invalid_isbn(self, client):
        resp = client.post("/books", json={"title": "T", "author": "A", "isbn": "invalid"})
        assert resp.status_code == 422

    def test_optional_fields_omitted(self, client, sample_book):
        with patch(f"{DB}.put_book", return_value=sample_book):
            resp = client.post("/books", json={"title": "T", "author": "A"})
        assert resp.status_code == 201


class TestGetBook:
    def test_success(self, client, sample_book):
        with patch(f"{DB}.get_book", return_value=sample_book):
            resp = client.get(f"/books/{sample_book['id']}")

        assert resp.status_code == 200
        assert resp.json()["id"] == sample_book["id"]

    def test_not_found(self, client):
        with patch(f"{DB}.get_book", return_value=None):
            resp = client.get("/books/nonexistent")

        assert resp.status_code == 404
        assert resp.json()["detail"] == "Book not found"


class TestListBooks:
    def test_success(self, client, sample_book):
        with patch(f"{DB}.list_books", return_value=([sample_book], None)):
            resp = client.get("/books")

        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] == 1
        assert len(data["items"]) == 1

    def test_empty(self, client):
        with patch(f"{DB}.list_books", return_value=([], None)):
            resp = client.get("/books")

        assert resp.status_code == 200
        assert resp.json() == {"items": [], "count": 0, "last_evaluated_key": None}

    def test_pagination(self, client, sample_book):
        with patch(f"{DB}.list_books", return_value=([sample_book], "next-key")) as mock:
            resp = client.get("/books?limit=1")
            mock.assert_called_once_with(limit=1, last_key=None)

        assert resp.json()["last_evaluated_key"] == "next-key"

    def test_invalid_limit(self, client):
        resp = client.get("/books?limit=0")
        assert resp.status_code == 422

    def test_limit_over_max(self, client):
        resp = client.get("/books?limit=101")
        assert resp.status_code == 422


class TestUpdateBook:
    def test_success(self, client, sample_book):
        updated = {**sample_book, "title": "New Title"}
        with patch(f"{DB}.update_book", return_value=updated):
            resp = client.patch(f"/books/{sample_book['id']}", json={"title": "New Title"})

        assert resp.status_code == 200
        assert resp.json()["title"] == "New Title"

    def test_not_found(self, client):
        with patch(f"{DB}.update_book", return_value=None):
            resp = client.patch("/books/nonexistent", json={"title": "T"})

        assert resp.status_code == 404

    def test_empty_body(self, client):
        resp = client.patch("/books/some-id", json={})
        assert resp.status_code == 400
        assert resp.json()["detail"] == "No fields to update"


class TestDeleteBook:
    def test_success(self, client, sample_book):
        with patch(f"{DB}.delete_book", return_value=True):
            resp = client.delete(f"/books/{sample_book['id']}")

        assert resp.status_code == 204

    def test_not_found(self, client):
        with patch(f"{DB}.delete_book", return_value=False):
            resp = client.delete("/books/nonexistent")

        assert resp.status_code == 404


class TestHealthCheck:
    def test_success(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
