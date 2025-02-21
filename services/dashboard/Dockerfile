# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install build dependencies for packages requiring compilation (e.g., hopsworks -> pyjks -> twofish)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Enable bytecode compilation and copy mode
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy lockfile and pyproject.toml first for dependency caching
COPY uv.lock pyproject.toml /app/

# Install project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copy the rest of the application
COPY . /app/

# Ensure the virtual environment is fully synced with project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place virtual environment executables in the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose Streamlit's default port
EXPOSE 8501

# Add a healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "dashboard_run.py", "--server.port=8501", "--server.address=0.0.0.0"]