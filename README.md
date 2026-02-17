# Tiny Web Service behind Reverse Proxy

A minimal, reproducible setup that runs a tiny web service behind an Nginx reverse proxy locally using Docker Compose.

Bonus: Kubernetes deployment using Kind and ingress-nginx.

---

# Architecture

## Docker Compose (Mandatory)

Client → Nginx (localhost:8080) → App (FastAPI)

### Reverse Proxy (Nginx)
- Listens on `localhost:8080`
- Forwards `/` to the app container
- Generates `X-Request-ID` if missing
- Passes `X-Request-ID` upstream
- Rate limits: 10 requests/sec per client IP
- Returns HTTP 429 when rate exceeded
- Only exposes port 8080

### App
Endpoint: `/healthz`

Returns:

```json
{
  "status": "ok",
  "service": "app",
  "env": "<ENV_NAME>"
}
```

Reads `ENV_NAME` from `.env` (default: `local`).

Includes Docker and Kubernetes health checks.

---

# Repository Structure

```
.
├── README.md
├── docker-compose.yml
├── .env.example
├── Makefile
├── nginx/
│   └── nginx.conf
├── app/
│   ├── Dockerfile
│   └── app.py
└── k8s/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
```

---

# Prerequisites

## Required
- Docker (>= 20.x)
- Docker Compose v2

## Bonus (Kubernetes)
- kind
- kubectl
- helm

---

# Docker Compose — How to Run

## 1. Configure environment

```bash
cp .env.example .env
```

Edit `.env` if needed:

```
ENV_NAME=local
```

---

## 2. Start services

```bash
make up
```

This will:
- Build the app image
- Create an isolated Docker network
- Start the app container
- Wait until app becomes healthy
- Start nginx
- Expose localhost:8080

---

## 3. Test service

```bash
make test
```

Or manually:

```bash
curl -s http://localhost:8080/healthz
```

Expected output:

```json
{"status":"ok","service":"app","env":"local"}
```

---

## 4. Check health status

```bash
docker ps
```

Both containers must show:

```
(healthy)
```

Inspect container details:

```bash
docker inspect <container_name>
```

---

## 5. View logs

```bash
make logs
```

---

## 6. Rate Limit Test

Send burst traffic:

```bash
for i in {1..20}; do \
  curl -s -o /dev/null -w "%{http_code}\n" \
  http://localhost:8080/healthz; \
done
```

Expected:
- Some responses: 200
- Some responses: 429

This confirms nginx rate limiting (10 req/sec per client) is working.

---

## 7. Stop and Cleanup

```bash
make down
```

This will:
- Stop containers
- Remove network
- Remove volumes

---

# Environment Variable Behavior

The app reads:

```
ENV_NAME
```

From `.env`.

Example:

```
ENV_NAME=staging
```

Restart:

```bash
make down
make up
```

Now:

```bash
curl http://localhost:8080/healthz
```

Returns:

```json
{"status":"ok","service":"app","env":"staging"}
```

---

# Security & Networking Notes

- Only Nginx exposes a port to host
- App is internal-only (Docker network)
- Rate limiting protects upstream service
- No unnecessary ports exposed
- Read-only nginx config mount

---

# Health Checks

## Docker
App:
- wget localhost:8000/healthz

Nginx:
- wget localhost:8080/healthz

## Kubernetes
- readinessProbe
- livenessProbe

Ensures:
- Proper startup ordering
- Automatic restart on failure

---

# Bonus — Kubernetes (Kind + Ingress)

Architecture:

Client → Ingress → Service → Deployment (App Pod)

---

## 1. Create Kind cluster

```bash
kind create cluster
```

Verify:

```bash
kubectl cluster-info
```

---

## 2. Install ingress-nginx

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress ingress-nginx/ingress-nginx
```

Wait until ingress controller pod is running:

```bash
kubectl get pods
```

---

## 3. Build image for Kind

```bash
docker build -t tiny-app:latest ./app
kind load docker-image tiny-app:latest
```

---

## 4. Apply Kubernetes manifests

```bash
kubectl apply -f k8s/
```

Verify:

```bash
kubectl get pods,svc,ingress
```

Expected:
- Pod running
- Service created
- Ingress created

---

## 5. Test via Ingress

```bash
curl http://localhost/healthz
```

Expected:

```json
{"status":"ok","service":"app","env":"local"}
```

---

# Acceptance Criteria — Docker Compose

- make up works without manual fixes
- Reverse proxy listens on localhost:8080
- /healthz returns HTTP 200 with JSON
- Rate limit returns 429 under burst
- .env controls ENV_NAME
- Health checks pass (docker ps shows healthy)
- make down cleans everything
- README is accurate and reproducible

---

# Acceptance Criteria — Kubernetes

- kubectl get pods,svc,ingress shows running resources
- Ingress routes /healthz correctly
- Probes configured
- App reachable at http://localhost/healthz

---

# Design Decisions

- FastAPI for minimal JSON service
- Nginx rate limiting (limit_req)
- Isolated Docker network
- Minimal config surface
- Clear reproducible commands
- No over-engineering

---

# Summary

This project demonstrates:

- Reverse proxy fundamentals
- Container networking
- Rate limiting
- Health checks
- Environment configuration
- Kubernetes basics
- Ingress routing

Minimal. Clear. Reproducible.
