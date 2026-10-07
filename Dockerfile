FROM python:3.14

WORKDIR /app 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . .

RUN pip install uv


RUN uv sync 



EXPOSE 8000


CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0"]