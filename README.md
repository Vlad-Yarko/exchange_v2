```
uv venv
```
```
.venv\Scripts\activate
```

ENVIRONMENT VARIABLES

```
alembic upgrade head
```

```
mkdir backend/src/keys
```
```
openssl genpkey -algorithm RSA -out backend/src/keys/private_key.pem
```
```
openssl rsa -in backend/src/keys/private_key.pem -pubout -out backend/src/keys/public_key.pem
```

```
cd backend
```
```
uvicorn main:app
```

ANOTHER TERMINAL

```
cd frontend
```
```
npm install
```
```
npm run dev
```
