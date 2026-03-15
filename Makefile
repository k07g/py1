.PHONY: install build deploy delete local local-db local-setup local-stop

VENV := .venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt uvicorn

build:
	sam build

deploy:
	sam deploy --guided

delete:
	sam delete

# DynamoDB Local をバックグラウンドで起動
local-db:
	docker compose up -d dynamodb-local

# テーブル作成
local-setup: local-db
	@echo "DynamoDB Local の起動を待機中..."
	@sleep 2
	$(PYTHON) scripts/create_table.py

# FastAPI をローカルで起動（DynamoDB Local に接続）
local: local-setup
	DYNAMODB_ENDPOINT=http://localhost:8000 $(VENV)/bin/uvicorn src.main:app --reload --port 8080

# DynamoDB Local を停止
local-stop:
	docker compose down
