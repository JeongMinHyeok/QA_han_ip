# QA 맛집 지도

이 프로젝트는 FastAPI를 이용한 내부용 맛집 리뷰 API입니다. 기본적으로 SQLite를 사용하지만 `DATABASE_URL` 환경 변수를 지정하면 외부 데이터베이스를 사용할 수 있습니다. AWS Lightsail 배포와 AWS RDS 연결을 염두에 두고 있습니다.

## 실행 방법

1. 의존성 설치

```bash
pip install -r requirements.txt
# 사용하려는 DB 드라이버도 함께 설치합니다. (예: psycopg2-binary, PyMySQL 등)
```

2. 서버 실행

```bash
uvicorn app.main:app --host 0.0.0.0 --port 80
```

서버 실행 전 `DATABASE_URL` 환경 변수에 AWS RDS 연결 문자열을 설정합니다. 환경 변수가 없으면 로컬 SQLite 데이터베이스(`app.db`)를 사용합니다.

실행 후 `http://localhost:8000/docs` 에서 Swagger UI를 통해 API를 확인할 수 있습니다.

## 지도 페이지 사용

`.env` 파일을 생성해 아래와 같이 구글 지도 API 키를 설정합니다. 이 값은 실제 운영 시 AWS Secrets Manager 등에서 불러올 수 있습니다.

```bash
GOOGLE_API_KEY=발급받은_api_key
```

`/map` 경로로 접속하면 `GOOGLE_API_KEY` 값을 사용해 구글 지도가 표시됩니다.
