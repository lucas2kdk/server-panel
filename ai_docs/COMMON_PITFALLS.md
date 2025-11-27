# Common Pitfalls for AI Implementation

This document lists common mistakes and issues to avoid when implementing the game server panel.

## Database & Models

### Pitfall 1: Forgetting to commit database changes
**Problem**: Making changes to models but not calling `db.session.commit()`
**Solution**: Always call `db.session.commit()` after add/update/delete operations

### Pitfall 2: Not handling database connection failures
**Problem**: Application crashes when database is unreachable
**Solution**: Add try/except blocks around database operations and handle gracefully

### Pitfall 3: Creating circular imports
**Problem**: Importing models in config.py while config imports models
**Solution**: Keep imports in functions or at the bottom of files when needed

### Pitfall 4: Not creating tables before first run
**Problem**: Application fails because tables don't exist
**Solution**: Use `db.create_all()` in app factory or use migrations

### Pitfall 5: Hardcoding database credentials
**Problem**: Passwords in source code, committed to Git
**Solution**: Use environment variables for all credentials

## Kubernetes Integration

### Pitfall 6: Not handling Kubernetes API exceptions
**Problem**: Any K8s API failure crashes the application
**Solution**: Wrap all K8s API calls in try/except blocks

### Pitfall 7: Creating invalid Kubernetes resource names
**Problem**: Server names with spaces/capitals cause K8s errors
**Solution**: Generate K8s-compliant names (lowercase, alphanumeric + hyphens only)

### Pitfall 8: Not checking if resources already exist
**Problem**: Trying to create a resource that already exists throws error
**Solution**: Check for existence first or handle AlreadyExists exception

### Pitfall 9: Forgetting to clean up resources on deletion
**Problem**: Deleting server in database but leaving K8s resources running
**Solution**: Delete StatefulSet, PVC, and Service before deleting database record

### Pitfall 10: Using wrong namespace
**Problem**: Creating resources in default namespace instead of game-servers
**Solution**: Always specify namespace in K8s API calls

### Pitfall 11: Not waiting for pod to be ready
**Problem**: Trying to exec into pod before it's running
**Solution**: Check pod status before operations like exec and logs

### Pitfall 12: Insufficient RBAC permissions
**Problem**: ServiceAccount lacks permissions for required operations
**Solution**: Ensure Role includes all necessary verbs (create, delete, get, list, watch, update, patch)

## Authentication & Security

### Pitfall 13: Storing plaintext passwords
**Problem**: Passwords visible in database
**Solution**: Always hash passwords with bcrypt before storing

### Pitfall 14: Missing authentication checks
**Problem**: Routes accessible without login
**Solution**: Use `@login_required` decorator on all protected routes

### Pitfall 15: Missing authorization checks
**Problem**: Users can access other users' servers
**Solution**: Check ownership/permissions in every route

### Pitfall 16: No CSRF protection
**Problem**: Vulnerable to cross-site request forgery
**Solution**: Enable Flask-WTF CSRF protection or manually validate

### Pitfall 17: Not validating user input
**Problem**: SQL injection, command injection, path traversal vulnerabilities
**Solution**: Validate and sanitize all user inputs

### Pitfall 18: Exposing internal errors to users
**Problem**: Stack traces visible in browser
**Solution**: Use custom error handlers, log details server-side only

## WebSocket & Console

### Pitfall 19: Not authenticating WebSocket connections
**Problem**: Unauthenticated users can connect to console
**Solution**: Check `current_user.is_authenticated` in connect handler

### Pitfall 20: Memory leaks from unclosed log streams
**Problem**: Log streaming threads never terminate
**Solution**: Implement cleanup on disconnect and use daemon threads

### Pitfall 21: Not handling WebSocket disconnections
**Problem**: Errors when client disconnects during log stream
**Solution**: Add try/except in streaming loops and check connection status

### Pitfall 22: Blocking the event loop
**Problem**: Long-running operations freeze WebSocket
**Solution**: Use background threads for log streaming

## File Manager

### Pitfall 23: Path traversal vulnerabilities
**Problem**: Users can access files outside server directory using `../`
**Solution**: Validate and sanitize file paths, use absolute paths

### Pitfall 24: Not escaping special characters in filenames
**Problem**: Files with quotes or spaces break commands
**Solution**: Properly escape or quote file paths in shell commands

### Pitfall 25: Large file operations blocking
**Problem**: Reading/writing large files freezes the application
**Solution**: Stream large files or add size limits

### Pitfall 26: Not handling file operation errors
**Problem**: Crashes when file doesn't exist or permissions denied
**Solution**: Wrap file operations in try/except, return meaningful errors

## Resource Management

### Pitfall 27: Not enforcing resource quotas
**Problem**: Users create unlimited servers, exhausting cluster resources
**Solution**: Check quotas before allowing server creation

### Pitfall 28: Race conditions in quota checking
**Problem**: Two simultaneous requests can exceed quota
**Solution**: Use database transactions or locks during quota checks

### Pitfall 29: Not updating server status
**Problem**: Database shows wrong status (e.g., "running" when pod is crashed)
**Solution**: Periodically sync status from Kubernetes or update on every view

### Pitfall 30: Resource limits too low
**Problem**: Minecraft servers can't start due to insufficient memory
**Solution**: Set appropriate minimums (at least 2Gi RAM for Minecraft)

## Docker & Containers

### Pitfall 31: Running containers as root
**Problem**: Security vulnerability
**Solution**: Create non-root user in Dockerfile and use it

### Pitfall 32: Large Docker images
**Problem**: Slow builds and deploys
**Solution**: Use multi-stage builds, Alpine base images, clean up cache

### Pitfall 33: Hardcoded configuration in image
**Problem**: Can't change config without rebuilding image
**Solution**: Use environment variables and ConfigMaps

### Pitfall 34: No health checks
**Problem**: Kubernetes can't detect when app is unhealthy
**Solution**: Implement /health endpoint and configure probes

## Helm Charts

### Pitfall 35: Invalid YAML indentation
**Problem**: Chart fails to install due to syntax errors
**Solution**: Use `helm lint` and validate YAML carefully

### Pitfall 36: Missing required values
**Problem**: Chart breaks when values not provided
**Solution**: Set defaults in values.yaml, use `required` function for critical values

### Pitfall 37: Hardcoded values in templates
**Problem**: Can't customize deployment
**Solution**: Parameterize everything via values.yaml

### Pitfall 38: Not templating resource names
**Problem**: Can't install multiple releases in same cluster
**Solution**: Use `{{ include "chart.fullname" . }}` for all resource names

### Pitfall 39: Secrets in values.yaml
**Problem**: Sensitive data committed to Git
**Solution**: Use external secrets or require secrets to be created separately

## CI/CD

### Pitfall 40: Tests not isolated
**Problem**: Tests fail due to shared state or database
**Solution**: Use test database, rollback transactions after each test

### Pitfall 41: Workflows with hardcoded values
**Problem**: Can't reuse workflows across environments
**Solution**: Use GitHub Actions inputs and variables

### Pitfall 42: Not tagging images properly
**Problem**: Can't identify which code is in which image
**Solution**: Tag with commit SHA and branch/tag name

### Pitfall 43: Pushing 'latest' tag in production
**Problem**: Unpredictable deployments, can't rollback easily
**Solution**: Use semantic versioning or commit SHAs

### Pitfall 44: No rollback strategy
**Problem**: Bad deployment breaks production with no recovery
**Solution**: Keep previous images, test in staging first

## Monitoring & Logging

### Pitfall 45: Not logging enough
**Problem**: Can't debug production issues
**Solution**: Log all important operations, errors, and user actions

### Pitfall 46: Logging too much
**Problem**: Logs fill disk, sensitive data exposed
**Solution**: Use appropriate log levels, don't log passwords/tokens

### Pitfall 47: No structured logging
**Problem**: Hard to parse and search logs
**Solution**: Use JSON logging format

### Pitfall 48: Not monitoring metrics
**Problem**: Don't know when system is degraded
**Solution**: Track key metrics (latency, errors, resource usage)

## Performance

### Pitfall 49: N+1 query problem
**Problem**: Loading servers list causes hundreds of database queries
**Solution**: Use eager loading (`joinedload`) in SQLAlchemy

### Pitfall 50: No connection pooling
**Problem**: Opening new database connection for every request
**Solution**: Configure SQLAlchemy connection pool

### Pitfall 51: Synchronous operations blocking
**Problem**: Waiting for Kubernetes API makes requests slow
**Solution**: Use background tasks for long operations

### Pitfall 52: No caching
**Problem**: Repeatedly fetching same data
**Solution**: Cache frequently accessed, rarely changing data

## General Python

### Pitfall 53: Missing dependencies
**Problem**: Application fails on fresh install
**Solution**: Keep requirements.txt updated and accurate

### Pitfall 54: Python version incompatibility
**Problem**: Code uses features not available in target Python version
**Solution**: Specify Python version requirement, test with target version

### Pitfall 55: Not using virtual environments
**Problem**: Dependency conflicts with system Python
**Solution**: Always use venv or virtualenv

### Pitfall 56: Ignoring linter warnings
**Problem**: Code quality issues, potential bugs
**Solution**: Run and fix black, flake8, mypy regularly

## Testing

### Pitfall 57: No tests
**Problem**: Breaking changes not caught
**Solution**: Write tests for critical functionality

### Pitfall 58: Tests that don't actually test anything
**Problem**: False confidence in code quality
**Solution**: Ensure tests validate expected behavior, not just syntax

### Pitfall 59: Flaky tests
**Problem**: Tests pass/fail randomly
**Solution**: Avoid timing dependencies, properly seed random data

### Pitfall 60: Not mocking external services
**Problem**: Tests fail when Kubernetes/database unavailable
**Solution**: Mock K8s API and use test database

## Best Practices to Follow

1. **Always validate user input** before using it
2. **Check permissions** on every operation
3. **Handle errors gracefully** - never let exceptions crash the app
4. **Log important operations** for debugging
5. **Use transactions** for database operations that must succeed/fail together
6. **Clean up resources** - don't leave orphaned K8s resources
7. **Test error paths** - don't just test happy path
8. **Use environment variables** for configuration
9. **Version everything** - database schema, API, Docker images
10. **Document assumptions** in code comments
