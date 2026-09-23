# SentinelMesh

Agentic Network Intrusion Detection & Threat Intelligence Platform.

## Runtime
- Python 3.14
- Node.js 24 LTS
- Angular 22

## First slice
The first slice is intentionally small:
- FastAPI application
- `/api/v1/health`
- typed settings from environment
- pytest smoke test
- pinned direct Python dependencies

No agent framework, ML model, database abstraction, or extra service is added yet. We will add each only when the corresponding slice requires it.
