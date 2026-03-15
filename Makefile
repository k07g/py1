.PHONY: help install install-dev test build push deploy update delete local local-db local-setup local-stop

# 設定（環境変数で上書き可）
AWS_REGION  ?= ap-northeast-1
AWS_ACCOUNT ?= $(shell aws sts get-caller-identity --query Account --output text)
IMAGE_NAME  ?= books-api
IMAGE_TAG   ?= latest
ECR_REPO     = $(AWS_ACCOUNT).dkr.ecr.$(AWS_REGION).amazonaws.com/$(IMAGE_NAME)
IMAGE_URI    = $(ECR_REPO):$(IMAGE_TAG)

VENV   := .venv
PYTHON := $(VENV)/bin/python3
PIP    := $(VENV)/bin/pip

## ヘルプ
help: ## ターゲット一覧を表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# -------------------------------------------------------------------
## ローカル開発
# -------------------------------------------------------------------

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV) ## 依存パッケージを仮想環境にインストール
	$(PIP) install -r requirements.txt uvicorn

install-dev: $(VENV) ## 開発・テスト用パッケージをインストール
	$(PIP) install -r requirements-dev.txt uvicorn

test: ## テストを実行
	$(VENV)/bin/pytest tests/ -v

local-db: ## DynamoDB Local をバックグラウンドで起動
	docker compose up -d dynamodb-local

local-setup: local-db ## DynamoDB Local 起動 + テーブル作成
	@echo "DynamoDB Local の起動を待機中..."
	@sleep 2
	$(PYTHON) scripts/create_table.py

local: local-setup ## FastAPI をローカルで起動 (port 8080)
	DYNAMODB_ENDPOINT=http://localhost:8000 $(VENV)/bin/uvicorn src.main:app --reload --port 8080

local-stop: ## DynamoDB Local を停止
	docker compose down

# -------------------------------------------------------------------
## コンテナ
# -------------------------------------------------------------------

build: ## Docker イメージをマルチステージビルド
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

push: build ## ECR にログインしてイメージをプッシュ
	aws ecr get-login-password --region $(AWS_REGION) \
	  | docker login --username AWS --password-stdin $(ECR_REPO)
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(IMAGE_URI)
	docker push $(IMAGE_URI)
