# Kub-Project

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                    CI/CD + OBSERVABILITY + GITOPS FLOW (k3s + Docker Hub)                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐         ┌─────────────────┐         ┌──────────────┐
    │   GitHub     │────────►│  GitHub Actions │────────►│  Docker Hub  │
    │   Repo       │  push   │  (CI Pipeline)  │  push   │  (Registry)  │
    │              │◄────────│                 │  image  │              │
    │ • app code   │  commit │ • Build         │         └──────┬───────┘
    │ • k8s YAML   │  tag    │ • Test          │                │
    │ • Helm charts│         │ • Push image    │                │
    └──────┬───────┘         │ • Update YAML   │                │
           │                 └─────────────────┘                │
           │  Git pull (webhook/poll)                            │
           ▼                                                     │
    ┌──────────────┐                                            │
    │   Argo CD    │────────────────────────────────────────────┘
    │   (GitOps)   │     Sync & Deploy
    │              │
    │ • Repo Server│
    │ • App Ctrl   │
    └──────┬───────┘
           │ kubectl apply
           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  K3S CLUSTER (1 Server + 2 Agents) - AWS EC2                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  ┌─────────────────────────────────────────┐  ┌─────────────────────────────────────────┐       │
│  │  AGENT 1 (Infra + App)                  │  │  AGENT 2 (App)                          │       │
│  │  ┌─────────────┐ ┌─────────────┐        │  │  ┌─────────────┐                        │       │
│  │  │ Argo CD     │ │ Grafana     │        │  │  │ Your App    │                        │       │
│  │  │ • server    │ │ • dashboards│        │  │  │ Pods        │                        │       │
│  │  │ • redis     │ │ • alerts    │        │  │  │             │                        │       │
│  │  └─────────────┘ └──────┬──────┘        │  │  └─────────────┘                        │       │
│  │  ┌─────────────┐        │               │  │                                         │       │
│  │  │ Prometheus  │◄───────┘               │  │  Prometheus scrapes both agents         │       │
│  │  │ • metrics   │                        │  │                                         │       │
│  │  └─────────────┘                        │  │                                         │       │
│  │  ┌─────────────┐                        │  │                                         │       │
│  │  │ Your App    │                        │  │                                         │       │
│  │  │ Pods        │                        │  │                                         │       │
│  │  └─────────────┘                        │  │                                         │       │
│  └─────────────────────────────────────────┘  └─────────────────────────────────────────┘       │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │   Traefik    │────►│   Grafana    │     │   Argo CD    │
    │   (k3s LB)   │     │   :3000      │     │   :443       │
    └──────────────┘     └──────────────┘     └──────────────┘
         │                     │                     │
         └─────────────────────┴─────────────────────┘
                    Users access via ALB / Traefik Ingress
```

## Master and Worker Node Configuration

| Node | vCPU | RAM | Role |
|------|------|-----|------|
| **Master** | 1 | 2 GB | Control plane (k3s server) |
| **Worker Node 1** | 1 | 2 GB | Workloads (k3s agent) |
| **Worker Node 2** | 1 | 2 GB | Workloads (k3s agent) |

### Master (k3s server)

```bash
curl -sfL https://get.k3s.io | sh -
sudo systemctl status k3s
sudo cat /var/lib/rancher/k3s/server/node-token   # Save this token
```


#Token
K10012b51032919b95f7d7ee46ff03101108225b7a5f1756b157c50c29a8f9e1dac::server:4f058185a6c74770ad006e7f1334d032

### Worker Node 1 (k3s agent)

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://18.170.225.30:6443 K3S_TOKEN=K10012b51032919b95f7d7ee46ff03101108225b7a5f1756b157c50c29a8f9e1dac::server:4f058185a6c74770ad006e7f1334d032 sh -
```

### Worker Node 2 (k3s agent)

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://18.170.225.30:6443 K3S_TOKEN=K10012b51032919b95f7d7ee46ff03101108225b7a5f1756b157c50c29a8f9e1dac::server:4f058185a6c74770ad006e7f1334d032 sh -
```

> Replace `<MASTER_IP>` with the master node's private IP and `<TOKEN>` with the token from the master.

## Check Connected Nodes

```bash
# List all nodes (run on master)
sudo kubectl get nodes

# Detailed view
sudo kubectl get nodes -o wide

# Cluster info
sudo kubectl cluster-info

# Check master service
sudo systemctl status k3s

# Check worker service (run on worker nodes)
sudo systemctl status k3s-agent
```

**Expected output when connected:** All nodes show `STATUS: Ready`
