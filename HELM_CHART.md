# Helm Chart Documentation

Complete Helm chart for deploying the Kubernetes Game Server Panel.

## Overview

The Helm chart deploys:
- Flask web application
- PostgreSQL database
- RBAC resources for game server management
- Optional ingress, autoscaling, and monitoring

## Quick Start

### Installation

```bash
# Add the game-servers namespace will be created automatically
helm install server-panel ./helm/server-panel

# With custom values
helm install server-panel ./helm/server-panel -f custom-values.yaml

# Development environment
helm install server-panel ./helm/server-panel -f ./helm/server-panel/values-dev.yaml

# Production environment
helm install server-panel ./helm/server-panel \
  -f ./helm/server-panel/values-prod.yaml \
  --set config.secretKey="your-production-secret" \
  --set postgresql.auth.password="secure-password"
```

### Verification

```bash
# Check deployment status
kubectl get pods -n default

# Check game-servers namespace was created
kubectl get namespace game-servers

# View service
kubectl get svc server-panel

# Access logs
kubectl logs -l app.kubernetes.io/name=server-panel -f
```

### Access the Application

```bash
# Port forward to access locally
kubectl port-forward svc/server-panel 8080:5000

# Then visit http://localhost:8080
```

## Configuration

### Required Values

The following values should be set in production:

```yaml
config:
  secretKey: "your-secure-random-secret-key"  # REQUIRED - change in production

postgresql:
  auth:
    password: "your-secure-database-password"  # REQUIRED - change in production
```

### Key Configuration Options

#### Application Settings

```yaml
replicaCount: 3  # Number of pod replicas

image:
  repository: ghcr.io/lucas2kdk/server-panel
  tag: "1.0.0"
  pullPolicy: IfNotPresent

config:
  secretKey: "your-secret-key"
  flaskEnv: "production"  # or "development"
  kubernetesNamespace: "game-servers"
  inCluster: "true"  # Set to "false" for development
```

#### Resources

```yaml
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi
```

#### Auto-scaling

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

#### Ingress

```yaml
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: panel.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: server-panel-tls
      hosts:
        - panel.example.com
```

#### PostgreSQL

```yaml
postgresql:
  enabled: true
  auth:
    username: postgres
    password: "secure-password"
    database: serverpanel
  primary:
    persistence:
      enabled: true
      size: 50Gi
      storageClass: "fast-ssd"
    resources:
      limits:
        cpu: 2000m
        memory: 4Gi
      requests:
        cpu: 1000m
        memory: 2Gi
```

#### RBAC

```yaml
rbac:
  create: true
  gameServersNamespace: "game-servers"

serviceAccount:
  create: true
  name: ""  # Auto-generated if empty
```

#### Monitoring

```yaml
monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 30s
```

## Helm Values Files

### values.yaml (Default)
- Base configuration
- ClusterIP service
- 1 replica
- PostgreSQL with 10Gi storage

### values-dev.yaml
- Development environment
- No persistence for PostgreSQL
- Lower resource limits
- develop image tag

### values-prod.yaml
- Production environment
- 3 replicas with auto-scaling
- Persistent storage (50Gi)
- Ingress enabled
- Pod anti-affinity
- Monitoring enabled

## Templates

### Core Resources
- `deployment.yaml` - Main application deployment
- `service.yaml` - ClusterIP service
- `configmap.yaml` - Application configuration
- `secret.yaml` - Sensitive data
- `serviceaccount.yaml` - Pod identity

### Optional Resources
- `ingress.yaml` - External access
- `hpa.yaml` - Horizontal pod autoscaling

### RBAC Resources
- `rbac/namespace.yaml` - game-servers namespace
- `rbac/role.yaml` - Permissions for managing game servers
- `rbac/rolebinding.yaml` - Binds role to service account

### PostgreSQL Resources
- `postgresql/statefulset.yaml` - Database
- `postgresql/service.yaml` - Database service

### Monitoring
- `monitoring/servicemonitor.yaml` - Prometheus scraping

## Commands

### Installation

```bash
# Install with default values
helm install server-panel ./helm/server-panel

# Install in specific namespace
helm install server-panel ./helm/server-panel -n panel --create-namespace

# Dry run to see generated manifests
helm install server-panel ./helm/server-panel --dry-run --debug

# Install with custom values
helm install server-panel ./helm/server-panel \
  --set replicaCount=2 \
  --set config.secretKey="my-secret"
```

### Upgrade

```bash
# Upgrade to new version
helm upgrade server-panel ./helm/server-panel

# Upgrade with new values
helm upgrade server-panel ./helm/server-panel -f new-values.yaml

# Upgrade with specific image tag
helm upgrade server-panel ./helm/server-panel --set image.tag=1.1.0
```

### Rollback

```bash
# View release history
helm history server-panel

# Rollback to previous version
helm rollback server-panel

# Rollback to specific revision
helm rollback server-panel 2
```

### Uninstall

```bash
# Uninstall release (keeps PVCs by default)
helm uninstall server-panel

# Delete everything including PVCs
helm uninstall server-panel
kubectl delete pvc -l app.kubernetes.io/instance=server-panel
kubectl delete namespace game-servers
```

### Inspection

```bash
# List installed releases
helm list

# Get release status
helm status server-panel

# Get values used in deployment
helm get values server-panel

# Get all manifests
helm get manifest server-panel

# View chart information
helm show chart ./helm/server-panel

# View all values
helm show values ./helm/server-panel
```

### Linting and Testing

```bash
# Lint chart
helm lint ./helm/server-panel

# Template without installing
helm template server-panel ./helm/server-panel

# Template with specific values
helm template server-panel ./helm/server-panel -f values-prod.yaml

# Validate against Kubernetes
helm template server-panel ./helm/server-panel | kubectl apply --dry-run=client -f -
```

## RBAC Permissions

The ServiceAccount has these permissions in the `game-servers` namespace:

### Apps API Group
- **StatefulSets**: get, list, watch, create, update, patch, delete

### Core API Group
- **PersistentVolumeClaims**: get, list, watch, create, update, patch, delete
- **Services**: get, list, watch, create, update, patch, delete
- **Pods**: get, list, watch
- **Pods/log**: get, list
- **Pods/exec**: create
- **Events**: get, list, watch

## Deployment Scenarios

### Local Development (Minikube/Kind)

```bash
# Use development values
helm install server-panel ./helm/server-panel -f helm/server-panel/values-dev.yaml

# Enable port forwarding
kubectl port-forward svc/server-panel 8080:5000
```

### Staging Environment

```bash
helm install server-panel ./helm/server-panel \
  --set image.tag="develop" \
  --set replicaCount=2 \
  --set config.flaskEnv="production" \
  --set config.secretKey="staging-secret"
```

### Production Environment

```bash
helm install server-panel ./helm/server-panel \
  -f helm/server-panel/values-prod.yaml \
  --set config.secretKey="${SECRET_KEY}" \
  --set postgresql.auth.password="${DB_PASSWORD}" \
  --set ingress.hosts[0].host="panel.example.com" \
  --set ingress.tls[0].hosts[0]="panel.example.com"
```

## Monitoring

If monitoring is enabled, metrics are exposed at `/metrics`:

```bash
# Check metrics endpoint
kubectl port-forward svc/server-panel 8080:5000
curl http://localhost:8080/metrics
```

### Prometheus Integration

The ServiceMonitor will be automatically discovered by Prometheus if you have the Prometheus Operator installed:

```bash
# Check ServiceMonitor
kubectl get servicemonitor server-panel

# View Prometheus targets
# Navigate to Prometheus UI -> Status -> Targets
```

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/name=server-panel

# View pod logs
kubectl logs -l app.kubernetes.io/name=server-panel

# Describe pod for events
kubectl describe pod -l app.kubernetes.io/name=server-panel
```

### Database connection issues

```bash
# Check PostgreSQL pod
kubectl get pods -l app.kubernetes.io/component=database

# View PostgreSQL logs
kubectl logs -l app.kubernetes.io/component=database

# Test database connection
kubectl exec -it deployment/server-panel -- env | grep DATABASE_URL
```

### RBAC permission issues

```bash
# Check ServiceAccount
kubectl get serviceaccount server-panel

# Check Role in game-servers namespace
kubectl get role -n game-servers server-panel

# Check RoleBinding
kubectl get rolebinding -n game-servers server-panel

# Describe for details
kubectl describe role -n game-servers server-panel
```

### Ingress not working

```bash
# Check ingress
kubectl get ingress

# Describe for events
kubectl describe ingress server-panel

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

## Upgrading

### Version Upgrade Process

1. **Backup database**:
```bash
kubectl exec -it deployment/server-panel-postgresql -- pg_dump -U postgres serverpanel > backup.sql
```

2. **Update image tag**:
```bash
helm upgrade server-panel ./helm/server-panel --set image.tag=1.1.0
```

3. **Verify deployment**:
```bash
kubectl rollout status deployment/server-panel
```

4. **Test application**:
```bash
kubectl port-forward svc/server-panel 8080:5000
# Visit http://localhost:8080
```

### Rolling Back

If issues occur:
```bash
helm rollback server-panel
```

## Security Considerations

1. **Change default passwords**:
   - Set unique `config.secretKey`
   - Set secure `postgresql.auth.password`

2. **Use secrets management**:
   - External Secrets Operator
   - Sealed Secrets
   - HashiCorp Vault

3. **Enable TLS**:
   - Configure ingress with cert-manager
   - Use valid certificates

4. **Limit RBAC permissions**:
   - Review Role permissions
   - Use least privilege principle

5. **Network policies**:
   - Restrict pod-to-pod communication
   - Allow only necessary traffic

## Best Practices

1. **Use specific image tags** (not `latest`)
2. **Set resource limits and requests**
3. **Enable pod disruption budgets** for HA
4. **Use persistent storage** in production
5. **Enable monitoring and alerting**
6. **Implement proper backup strategy**
7. **Test upgrades in staging first**
8. **Keep chart and app versions in sync**

## Contributing

To modify the Helm chart:

1. Make changes to templates or values
2. Run `helm lint ./helm/server-panel`
3. Test with `helm template` and `--dry-run`
4. Update Chart.yaml version
5. Update CHANGELOG
6. Create pull request

## Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [PostgreSQL Helm Charts](https://github.com/bitnami/charts/tree/main/bitnami/postgresql)
