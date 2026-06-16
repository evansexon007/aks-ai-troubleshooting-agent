# Architecture

## Overview

This project demonstrates a simple read-only AI agent for AKS troubleshooting.

```text
User question
  |
  v
Python command-line app
  |
  v
OpenAI Agents SDK
  |
  v
Agent reasoning and tool selection
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

## Components

### User

The user runs the agent locally and asks natural language questions.

Example:

```powershell
python .\agent.py "Use the kubectl tool and check the health of my AKS lab"
```

### Python app

`agent.py` is the main application entry point.

It:

- Reads the user question from the command line
- Defines safe tools
- Registers those tools with the agent
- Runs the OpenAI Agents SDK runner
- Prints the final output

### OpenAI Agents SDK

The SDK provides:

- Agent definition
- Instructions
- Tool registration
- Tool calling
- Agent execution

### Tool layer

The tools are normal Python functions decorated with `@function_tool`.

Current tools:

- `run_kubectl`
- `describe_pod`
- `get_pod_logs`

### Kubernetes access

The agent does not store cluster credentials.

It uses the local machine's existing `kubectl` context.

That means the user must already be able to run:

```powershell
kubectl get pods -A
```

before using the agent.

## Design principle

The agent can investigate and explain.

It cannot change the cluster.
