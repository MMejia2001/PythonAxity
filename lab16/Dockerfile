FROM python:3.12-slim AS runtime

WORKDIR /app

# Copia Python instalado y el código
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Si usas estructura src/
ENV PYTHONPATH=/app/src

# Crear usuario sin privilegios
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Permisos mínimos: appuser dueño de /app
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
