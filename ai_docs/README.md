# AI Documentation - Quick Start

This folder contains documentation specifically designed for AI assistants to implement the Kubernetes Game Server Panel.

## Documentation Overview

### For AI Implementation

1. **SIMPLE_CHECKLIST.md** ⭐ START HERE
   - Complete task-by-task checklist
   - No code, just discrete actionable items
   - Check off tasks as you complete them
   - Covers entire project from setup to deployment

2. **FILE_STRUCTURE.md**
   - Exact directory and file structure
   - Shows where every file should be placed
   - Naming conventions
   - Import patterns

3. **IMPLEMENTATION_GUIDE.md**
   - Code examples and patterns for reference
   - Detailed implementation of major components
   - Use when you need to see how something should be coded

4. **COMMON_PITFALLS.md**
   - 60+ common mistakes to avoid
   - Best practices
   - Security considerations
   - Quick tips

### For Understanding the Project

See the `docs/` folder for:
- **PROJECT_OVERVIEW.md** - High-level vision and goals
- **ARCHITECTURE.md** - System design and components
- **REQUIREMENTS.md** - Detailed functional requirements
- **GLOSSARY.md** - Technical terms explained for beginners

## Quick Implementation Flow

1. Read `../docs/PROJECT_OVERVIEW.md` to understand what you're building
2. Skim `../docs/GLOSSARY.md` for any unfamiliar terms
3. Open `SIMPLE_CHECKLIST.md` and start from the top
4. Reference `FILE_STRUCTURE.md` when creating files
5. Reference `IMPLEMENTATION_GUIDE.md` when writing code
6. Consult `COMMON_PITFALLS.md` before committing code
7. Check off items in the checklist as you go

## Technology Summary

**Backend**: Flask (Python), PostgreSQL, Kubernetes Python client
**Frontend**: Jinja2, Alpine.js, HTMX, Tailwind CSS
**Infrastructure**: Kubernetes, Helm, Docker
**CI/CD**: GitHub Actions, ArgoCD, GitHub Container Registry
**Monitoring**: Prometheus, Grafana

## Key Requirements Quick Reference

- **Language**: Python 3.11+
- **Framework**: Flask
- **Database**: PostgreSQL
- **Auth**: Email/password with bcrypt
- **Permissions**: Fine-grained (user/server/action levels)
- **Console**: Web-based terminal with live streaming
- **File Manager**: Browse and edit server files in browser
- **Resources**: Predefined plans + custom allocation + quotas
- **Minecraft Types**: Vanilla, Paper/Spigot, Forge/Fabric
- **Storage**: PersistentVolumeClaims per server
- **Deployment**: Helm + ArgoCD
- **Registry**: GitHub Container Registry (ghcr.io)
- **Networking**: ClusterIP for now (panel and game servers)

## Project Inspiration

This project is inspired by [Pterodactyl Panel](https://pterodactyl.io/), adopting features like:
- Live web console
- File manager
- Fine-grained permissions
- Server templates (eggs)
- Sub-user support

But built Kubernetes-native from the ground up.

## Implementation Phases

### Phase 1 - MVP (Core Functionality)
- User authentication
- Server CRUD operations
- Web console
- Basic Kubernetes integration
- Helm chart
- CI/CD pipeline

### Phase 2 - Enhanced Features
- File manager
- Sub-user permissions
- Resource quotas
- Server templates

### Phase 3 - Advanced Features
- Scheduled tasks
- Backups
- Additional game types
- OAuth2 authentication

## Verification Steps

After implementing each major section:

```bash
# Syntax check
python -m py_compile app/module.py

# Run tests
pytest

# Lint code
black app/ --check
flake8 app/

# Build Docker
docker build -t server-panel .

# Lint Helm
helm lint helm/server-panel

# Check K8s resources
kubectl get all -n game-servers
```

## Getting Help

If you encounter unclear requirements:
1. Check `../docs/REQUIREMENTS.md` for detailed specs
2. Check `../docs/GLOSSARY.md` for term definitions
3. Check `COMMON_PITFALLS.md` for known issues
4. Reference `../docs/ARCHITECTURE.md` for design decisions

## Success Criteria

You'll know the implementation is complete when:
- [ ] All items in SIMPLE_CHECKLIST.md are checked
- [ ] Flask app runs without errors
- [ ] Can create and manage Minecraft servers via web UI
- [ ] Can interact with server console in browser
- [ ] Can browse and edit server files
- [ ] All tests pass
- [ ] Docker image builds successfully
- [ ] Helm chart deploys to Kubernetes
- [ ] GitHub Actions workflows pass
- [ ] Prometheus metrics are collected

## Important Notes for AI Assistants

- **Read requirements carefully** - Don't implement features not requested
- **Follow the checklist order** - Later tasks depend on earlier ones
- **Test frequently** - Verify each component works before moving on
- **Handle errors gracefully** - Add try/except blocks around external calls
- **Security first** - Validate inputs, check permissions, hash passwords
- **Clean up resources** - Delete K8s resources when servers are deleted
- **Use existing patterns** - Follow Flask blueprints structure consistently
- **Document as you go** - Add docstrings and comments

Good luck with the implementation!
