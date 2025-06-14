# QA 맛집 지도

이 프로젝트는 FastAPI와 SQLite를 사용하여 QA팀에서 검증한 맛집 정보를 관리하는 내부용 웹 API 입니다.

## 실행 방법

1. 의존성 설치

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

2. 서버 실행

```bash
uvicorn app.main:app --reload
```

실행 후 `http://localhost:8000/docs` 에서 Swagger UI를 통해 API를 확인할 수 있습니다.
