# LinkedIn Post Draft

I have been experimenting with AI agents in a practical cloud infrastructure context.

As a home lab project, I built a read-only AKS troubleshooting agent using Python, the OpenAI Agents SDK and controlled kubectl tooling.

The agent can inspect an AKS cluster using approved read-only commands, including:

- kubectl get pods -A
- kubectl get nodes
- kubectl get namespaces
- kubectl get svc -A
- kubectl get ingress -A
- kubectl describe pod
- kubectl logs

The important part for me was the safety model.

Rather than giving the agent unrestricted shell access, I used a command allowlist, input validation and read-only tooling. The agent can investigate and explain what it finds, but it cannot delete, patch, scale, restart or modify anything.

This was a useful exercise in combining cloud platform engineering with agentic AI patterns:

- LLM reasoning
- tool calling
- Kubernetes diagnostics
- safe automation boundaries
- operational troubleshooting workflows

It is only a lab project, but it helped me think through how AI agents could support platform teams in a controlled and auditable way.

Next steps: add Kubernetes events, deployment/service descriptions, Prometheus/Grafana checks and possibly containerise it for an internal platform-tools namespace.
