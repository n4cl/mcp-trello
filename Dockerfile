FROM python:3.13-bullseye

WORKDIR /app

# Install uv
RUN pip install uv

# Install fastmcp using uv, utilizing cache for faster builds
RUN --mount=type=cache,target=/root/.cache/uv uv pip install --system fastmcp

# Placeholder for application code
COPY . .

# Default command to run the FastMCP server, assuming main.py will be created later
CMD ["python", "main.py"]
