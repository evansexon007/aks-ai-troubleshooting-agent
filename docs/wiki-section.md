# AI Agent Home Lab - AKS Troubleshooting Agent

## Purpose

This lab builds a simple AI agent that can inspect an AKS cluster using safe, read-only `kubectl` commands.

The goal is to move beyond a normal chatbot and create an agent that can:

- Receive a natural language question
- Decide which Kubernetes command to run
- Run a safe read-only tool
- Inspect live AKS output
- Explain what it found
- Suggest next steps without making changes automatically

Example question:

```text
Use the kubectl tool and check the health of my AKS lab
```

---

## High-Level Architecture

```text
User question
  |
  v
Python AI agent
  |
  v
OpenAI Agents SDK
  |
  v
Safe Python tool functions
  |
  v
kubectl read-only commands
  |
  v
AKS cluster
  |
  v
Agent explains result
```

The agent runs locally from a Python virtual environment.

The AKS cluster is accessed using the local `kubectl` context.

---

## What Makes This an Agent?

A normal chatbot only responds with text.

This agent can use tools.

In this lab, the tool is a Python function that safely runs approved `kubectl` commands.

The agent can:

```text
Reason about the user request
Choose a tool
Run kubectl
Read the output
Explain the cluster state
Recommend a next step
```

---

## Safety Model

The agent is intentionally read-only.

The Python code uses:

```text
Command allowlist
Safe Kubernetes name validation
shell=False for subprocess calls
Timeouts on commands
Tail limit on logs
No destructive commands
```

This means the agent can inspect the AKS lab but cannot change it.

Any remediation action should be recommended as a manual next step, not executed automatically.

---

## Current Capabilities

The agent supports these read-only checks:

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

## Running the Agent

Basic health check:

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

Check ingress:

```powershell
python .\agent.py "Use the kubectl tool and check ingress in my cluster"
```

Investigate unhealthy pods:

```powershell
python .\agent.py "Use the kubectl tool and investigate whether any pods in my AKS lab need troubleshooting. If any look unhealthy, describe them and check their logs."
```

---

## Possible Next Enhancements

```text
Add kubectl get events -A
Add deployment describe support
Add service describe support
Add ingress describe support
Add Prometheus or Grafana API checks
Add Azure CLI read-only checks
Add Markdown report output
Add memory using SQLite or Postgres
Containerise the agent
Run it inside AKS in a platform-tools namespace
Expose it internally through ingress
Add approval workflow for any future write actions
```
