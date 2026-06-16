# Security Model

## Core principle

The agent is read-only.

It is designed to inspect AKS state and explain findings, not to modify infrastructure.

## What is allowed

The agent can run approved read-only commands:

```text
kubectl config current-context
kubectl get nodes
kubectl get namespaces
kubectl get pods -A
kubectl get svc -A
kubectl get ingress -A
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --tail <lines>
```

## What is blocked

The agent does not support destructive or mutating actions.

Blocked examples:

```text
kubectl delete
kubectl apply
kubectl patch
kubectl scale
kubectl drain
kubectl cordon
kubectl rollout restart
terraform apply
terraform destroy
az resource delete
```

## Controls in the code

### Command allowlist

General commands must match a predefined allowlist.

```python
ALLOWED_COMMANDS = {
    "kubectl get pods -A": ["kubectl", "get", "pods", "-A"],
}
```

### No shell expansion

Commands are run with:

```python
shell=False
```

This avoids shell expansion and reduces command injection risk.

### Name validation

Namespace, pod and container names are validated before being passed to `kubectl`.

### Timeout

Commands have a timeout to avoid hanging indefinitely.

### Log tail limit

Pod logs are capped to avoid retrieving too much data.

### Secrets handling

The OpenAI API key is read from the environment.

It must not be committed to the repository.

## Production considerations

Before using a pattern like this in production, consider:

- Dedicated read-only Kubernetes RBAC
- Separate service account
- Audit logging
- Network restrictions
- Approval workflows
- Prompt injection testing
- Secret scanning
- Logging and retention policy
- Human review for any write action
