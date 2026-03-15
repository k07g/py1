# ---- builder: 依存パッケージをインストール ----
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --target /deps -r requirements.txt

# ---- runtime: Lambda ベースイメージに最小限のファイルのみコピー ----
FROM public.ecr.aws/lambda/python:3.12

COPY --from=builder /deps ${LAMBDA_TASK_ROOT}
COPY src/ ${LAMBDA_TASK_ROOT}/src/

CMD ["src.main.handler"]
