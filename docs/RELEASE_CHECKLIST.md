# Release checklist

## Version

1.0.0

## Validations

- Backend tests executed with `python3 -m pytest backend/tests -v`
- Backend lint executed with `python3 -m ruff check backend`
- Frontend tests executed with `npm run test`
- Frontend production build executed with `npm run build`

## URLs

- Frontend: http://localhost:5173
- Swagger: http://localhost:8000/api-docs
- Health: http://localhost:8000/api/health
