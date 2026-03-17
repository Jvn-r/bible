# ── Stage 1: base image ──────────────────────────────────────────────────────
# We start from an official Python image. "3.11-slim" means Python 3.11
# on a minimal Linux — no bloat, small image size.
FROM python:3.11-slim

# ── Stage 2: set working directory ───────────────────────────────────────────
# This is where all your app files will live INSIDE the container.
# Think of it as the "home folder" for your app.
WORKDIR /app

# ── Stage 3: install dependencies ────────────────────────────────────────────
# We copy requirements.txt FIRST (before the rest of the code).
# Why? Docker caches layers. If your code changes but requirements don't,
# Docker skips reinstalling packages. Faster rebuilds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 4: copy your app code ──────────────────────────────────────────────
# Now copy everything else into /app inside the container.
COPY . .

# ── Stage 5: expose the port ─────────────────────────────────────────────────
# Tells Docker "this container talks on port 8000".
# Doesn't actually open it to the world — docker-compose handles that.
EXPOSE 8000

# ── Stage 6: run the app ─────────────────────────────────────────────────────
# This is the command that runs when the container starts.
# We use 0.0.0.0 so it's reachable from outside the container.
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
