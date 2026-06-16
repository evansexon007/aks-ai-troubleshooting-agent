# AKS AI Troubleshooting Agent

A small home-lab project that demonstrates how to build a **read-only AI troubleshooting agent** for Azure Kubernetes Service (AKS).

The agent uses:

- Python
- OpenAI Agents SDK
- Controlled tool calling
- Safe read-only `kubectl` commands
- Kubernetes pod, node, service, ingress, describe and log checks

The aim is to show a practical pattern for combining AI agents with cloud platform operations without giving the agent unrestricted shell or cluster access.

---

## What this project does

This agent can answer questions such as:

```powershell
python .\agent.py "Use the kubectl tool and check the health of my AKS lab"
```

Example agent flow:

```text
User asks a question
  -> Agent decides which tool to call
  -> Python runs an approved read-only kubectl command
  -> AKS returns live cluster data
  -> Agent explains the result and suggests a safe next step
```

The agent can inspect:

- Pods
- Nodes
- Namespaces
- Services
- Ingress resources
- Specific pod descriptions
- Recent pod logs

---

## Why this is useful

This is not intended to be a production support tool.

It is a learning and portfolio project showing:

- AI agent development
- Tool calling
- Kubernetes troubleshooting
- Platform engineering automation
- Safe automation boundaries
- Read-only operational diagnostics

The important design principle is that the agent can investigate and explain, but it cannot modify the cluster.

---

## Safety model

The agent is intentionally read-only.

It does **not** allow:

- `kubectl delete`
- `kubectl apply`
- `kubectl patch`
- `kubectl scale`
- `kubectl drain`
- `kubectl cordon`
- Terraform apply/destroy
- Azure resource deletion or modification

The implementation uses:

- A command allowlist
- Safe Kubernetes name validation
- `shell=False` for subprocess calls
- Command timeouts
- Tail limits for logs
- Environment variables for secrets
- No kubeconfig or API keys in the repository

---

## Repository structure

```text
aks-ai-troubleshooting-agent/
  agent.py
  requirements.txt
  .env.example
  .gitignore
  README.md
  LICENSE
  docs/
    architecture.md
    security-model.md
    example-output.md
    wiki-section.md
    linkedin-post.md
  scripts/
    setup.ps1
```

---

## Prerequisites

You need:

- Python 3.12 or later
- Azure CLI
- kubectl
- Access to an AKS cluster
- An OpenAI API key
- A working local Kubernetes context

Check Python:

```powershell
python --version
```

Check kubectl:

```powershell
kubectl config current-context
kubectl get pods -A
```

Check AKS is running:

```powershell
az aks show `
  --resource-group <resource-group-name> `
  --name <aks-cluster-name> `
  --query "{name:name,powerState:powerState.code,provisioningState:provisioningState}" `
  -o table
```

If the cluster is stopped:

```powershell
az aks start `
  --resource-group <resource-group-name> `
  --name <aks-cluster-name>
```

Refresh kubeconfig:

```powershell
az aks get-credentials `
  --resource-group <resource-group-name> `
  --name <aks-cluster-name> `
  --overwrite-existing
```

---

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Set your OpenAI API key:

```powershell
$env:OPENAI_API_KEY = "paste-your-key-here"
```

Optional Windows console encoding fix:

```powershell
$env:PYTHONIOENCODING = "utf-8"
```

---

## Running the agent

General health check:

```powershell
python .\agent.py "Use the kubectl tool and check the health of my AKS lab"
```

Check nodes:

```powershell
python .\agent.py "Use the kubectl tool and check my AKS nodes"
```

Check namespaces:

```powershell
python .\agent.py "Use the kubectl tool and tell me what namespaces exist"
```

Check services:

```powershell
python .\agent.py "Use the kubectl tool and check what services are exposed"
```

Check ingress:

```powershell
python .\agent.py "Use the kubectl tool and check ingress in my cluster"
```

Investigate unhealthy pods:

```powershell
python .\agent.py "Use the kubectl tool and investigate whether any pods in my AKS lab need troubleshooting. If any look unhealthy, describe them and check their logs."
```

Describe a specific pod:

```powershell
python .\agent.py "Use the kubectl tool and describe pod <pod-name> in namespace <namespace>"
```

Get pod logs:

```powershell
python .\agent.py "Use the kubectl tool and get the last 100 logs for pod <pod-name> in namespace <namespace>"
```

---

## Current capabilities

The agent can use these read-only checks:

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

---

## Future enhancements

Possible next steps:

- Add `kubectl get events -A --sort-by=.lastTimestamp`
- Add deployment describe support
- Add service describe support
- Add ingress describe support
- Add Prometheus or Grafana API checks
- Add Azure CLI read-only checks
- Add markdown report output
- Add memory using SQLite or Postgres
- Containerise the agent
- Run it inside AKS in a `platform-tools` namespace
- Expose it internally through ingress
- Add an approval workflow for any future write actions

---

## Important note

This is a demo/home-lab project. Do not use it against production clusters without a proper security review, RBAC scoping, audit logging, approval flow and operational controls.
