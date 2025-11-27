# Database Migrations

This directory contains Flask-Migrate (Alembic) migrations for the server-panel database.

## How to Run Migrations

### Local Development

```bash
# Apply all pending migrations
flask db upgrade

# Or use the custom CLI command
flask db-upgrade
```

### Kubernetes/Production

**Option 1: Using kubectl exec**
```bash
# Apply migrations in the running pod
kubectl exec -it deployment/server-panel -n default -- flask db upgrade
```

**Option 2: Using the migration script**
```bash
# Copy and run the migration script
kubectl exec -it deployment/server-panel -n default -- bash run_migration.sh
```

**Option 3: Init container (Recommended for automation)**
Add an init container to your Helm deployment that runs migrations before the app starts.

## Migration Files

- `env.py` - Alembic environment configuration
- `alembic.ini` - Alembic configuration file
- `script.py.mako` - Template for generating new migrations
- `versions/` - Directory containing all migration scripts

## Current Migrations

1. **20251127_add_namespace_columns.py** - Adds namespace support for per-user Kubernetes namespaces
   - Adds `k8s_namespace` column to `users` table
   - Adds `namespace` column to `servers` table
   - Migrates existing data

## Creating New Migrations

```bash
# Auto-generate a migration based on model changes
flask db migrate -m "Description of changes"

# Create an empty migration for manual changes
flask db revision -m "Description of changes"
```

## Migration Best Practices

1. Always review auto-generated migrations before applying
2. Test migrations on a development database first
3. Back up production database before applying migrations
4. Migrations should be reversible when possible
5. Don't modify existing migrations after they've been deployed
