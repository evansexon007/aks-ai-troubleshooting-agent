import sys
sys.stdout.reconfigure(encoding="utf-8")

import asyncio
import os
import re
import subprocess
from typing import Optional

from agents import Agent, Runner, function_tool


ALLOWED_COMMANDS = {
    "kubectl config current-context": ["kubectl", "config", "current-context"],
    "kubectl get nodes": ["kubectl", "get", "nodes"],
    "kubectl get namespaces": ["kubectl", "get", "namespaces"],
    "kubectl get pods -A": ["kubectl", "get", "pods", "-A"],
    "kubectl get svc -A": ["kubectl", "get", "svc", "-A"],
    "kubectl get ingress -A": ["kubectl", "get", "ingress", "-A"],
}

SAFE_K8S_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,252}$")


def debug(message: str) -> None:
    """Print debug messages only when DEBUG_TOOLS=1 is set."""
    if os.getenv("DEBUG_TOOLS") == "1":
        print(f"[debug] {message}", flush=True)


def is_safe_k8s_name(value: str) -> bool:
    """Validate Kubernetes-style names before passing them to kubectl."""
    if not value:
        return False

    return bool(SAFE_K8S_NAME.match(value))


def run_command(args: list[str], timeout: int = 30) -> str:
    """Run a command safely without shell expansion."""
    result = subprocess.run(
        args,
        shell=False,
        capture_output=True,
        text=True,
        timeout=timeout,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        return "Command failed:\n" + result.stderr

    return result.stdout


@function_tool
def run_kubectl(command: str) -> str:
    """
    Run one approved read-only kubectl command.

    Allowed commands:
    - kubectl config current-context
    - kubectl get nodes
    - kubectl get namespaces
    - kubectl get pods -A
    - kubectl get svc -A
    - kubectl get ingress -A
    """

    command = command.strip()

    debug(f"run_kubectl called with: {command}")

    if command not in ALLOWED_COMMANDS:
        return (
            "Command blocked. Only these read-only commands are allowed:\n"
            + "\n".join(ALLOWED_COMMANDS.keys())
        )

    return run_command(ALLOWED_COMMANDS[command])


@function_tool
def describe_pod(namespace: str, pod: str) -> str:
    """
    Describe a specific Kubernetes pod in a namespace.

    This is read-only and is useful for investigating:
    - CrashLoopBackOff
    - ImagePullBackOff
    - Pending pods
    - readiness/liveness probe failures
    - scheduling issues
    - mount/volume issues
    """

    namespace = namespace.strip()
    pod = pod.strip()

    debug(f"describe_pod called with namespace={namespace}, pod={pod}")

    if not is_safe_k8s_name(namespace):
        return "Blocked: namespace name contains unsafe characters."

    if not is_safe_k8s_name(pod):
        return "Blocked: pod name contains unsafe characters."

    return run_command(
        ["kubectl", "describe", "pod", pod, "-n", namespace],
        timeout=30,
    )


@function_tool
def get_pod_logs(
    namespace: str,
    pod: str,
    tail_lines: int = 100,
    container: Optional[str] = None,
) -> str:
    """
    Get recent logs for a specific Kubernetes pod.

    This is read-only and is useful for checking application errors.
    If the pod has multiple containers, provide the container name.
    """

    namespace = namespace.strip()
    pod = pod.strip()

    debug(
        f"get_pod_logs called with namespace={namespace}, pod={pod}, "
        f"tail_lines={tail_lines}, container={container}"
    )

    if not is_safe_k8s_name(namespace):
        return "Blocked: namespace name contains unsafe characters."

    if not is_safe_k8s_name(pod):
        return "Blocked: pod name contains unsafe characters."

    if container is not None:
        container = container.strip()
        if not is_safe_k8s_name(container):
            return "Blocked: container name contains unsafe characters."

    if tail_lines < 1:
        tail_lines = 100

    if tail_lines > 500:
        tail_lines = 500

    args = [
        "kubectl",
        "logs",
        pod,
        "-n",
        namespace,
        "--tail",
        str(tail_lines),
    ]

    if container:
        args.extend(["-c", container])

    return run_command(args, timeout=30)


agent = Agent(
    name="AKS Troubleshooting Agent",
    instructions="""
    You are an AKS home lab troubleshooting agent.

    IMPORTANT:
    When the user asks you to check, inspect, review, list, diagnose,
    troubleshoot, or investigate the AKS lab, use the available kubectl tools.

    Investigation approach:
    - For general health, first call run_kubectl with: kubectl get pods -A
    - For node health, call run_kubectl with: kubectl get nodes
    - For namespaces, call run_kubectl with: kubectl get namespaces
    - For services or load balancers, call run_kubectl with: kubectl get svc -A
    - For ingress, call run_kubectl with: kubectl get ingress -A
    - If a pod is not Running or Completed, use describe_pod.
    - If a pod looks unhealthy, use get_pod_logs after describe_pod.
    - If logs fail because the pod has multiple containers, ask for or infer the container name from describe_pod.

    Safety rules:
    - Only use read-only commands.
    - Never delete, restart, scale, patch, apply, drain, cordon, or modify resources.
    - If a fix requires a change, recommend it as a manual next step only.
    - Do not claim you cannot inspect the cluster. Use the tools.

    Answer format:
    - What I checked
    - What I found
    - What it means
    - Suggested next step

    Keep answers practical and concise.
    Use plain ASCII only.
    Avoid curly quotes, arrows, emojis and special symbols.
    """,
    tools=[
        run_kubectl,
        describe_pod,
        get_pod_logs,
    ],
)


async def main() -> None:
    if len(sys.argv) < 2:
        print("Usage:")
        print('python .\\agent.py "your question here"')
        print()
        print("Example:")
        print('python .\\agent.py "Use the kubectl tool and check the health of my AKS lab"')
        return

    question = " ".join(sys.argv[1:])

    result = await Runner.run(agent, question)

    print()
    print(result.final_output)
    print()


if __name__ == "__main__":
    asyncio.run(main())
