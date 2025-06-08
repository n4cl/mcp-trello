FROM python:3.13-bullseye

WORKDIR /app

# Install uv
RUN pip install uv

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/uv uv pip install --system -r requirements.txt

# Placeholder for application code
COPY . .

# Default command to run the FastMCP server, assuming main.py will be created later
EXPOSE 8000
CMD ["fastmcp", "run", "main.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
