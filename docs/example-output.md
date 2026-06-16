# Example Output

## Health check

Command:

```powershell
python .\agent.py "Use the kubectl tool and check the health of my AKS lab"
```

Example output:

```text
What I checked
- I checked all pods across all namespaces using kubectl get pods -A.

What I found
- All expected pods are Running or Completed.
- No obvious CrashLoopBackOff, ImagePullBackOff or Pending pods were found.
- Core system pods are present.

What it means
- The cluster appears healthy from a pod status perspective.
- There are no obvious workload-level failures in the current output.

Suggested next step
- Check node health and ingress/service exposure if you want a broader cluster health view.
```

## Namespace check

Command:

```powershell
python .\agent.py "Use the kubectl tool and tell me what namespaces exist"
```

Example output:

```text
What I checked
- I listed namespaces in the cluster.

What I found
- Kubernetes system namespaces are present.
- Application or platform namespaces are also visible.

What it means
- Namespace segmentation is in place.
- This can be used to separate platform tooling from application workloads.

Suggested next step
- Review pods per namespace to confirm each namespace is running the expected workloads.
```

## Troubleshooting unhealthy pods

Command:

```powershell
python .\agent.py "Use the kubectl tool and investigate whether any pods in my AKS lab need troubleshooting. If any look unhealthy, describe them and check their logs."
```

Expected flow:

```text
1. Agent runs kubectl get pods -A
2. Agent identifies pods not Running or Completed
3. Agent describes the unhealthy pod
4. Agent checks recent logs
5. Agent explains likely cause
6. Agent suggests a manual next step
```
