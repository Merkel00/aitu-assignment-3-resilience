# AITU Assignment 3 — deliverable package

## Files
- `Assignment_3_AITU_Resilience_Report.docx` and `.pdf`: completed technical case-study report.
- `config/registration-deployment.yaml`: Deployment + ClusterIP Service, with 2 replicas.
- `config/namespace.yaml`: namespace setup.
- `config/registration-demo-app.py` and `config/Dockerfile`: a **demo** application with `/healthz`, `/readyz`, and `/register` endpoints. No real university services are used.
- `diagrams/`: architecture drawing and before/after availability chart.
- `experiments/run_simulations.py`: deterministic failure model.
- `experiments/evidence/`: generated CSV, JSON and three labeled **MODEL EVENT TRACES**.

## Reproduce the deterministic failure simulations
`python3 experiments/run_simulations.py`

These simulations **are not live Kubernetes experiments**. The assumed failure-detection and recovery timings are inputs to the model and should not be represented as actual cluster metrics. No fabricated kubectl screenshots are supplied.

## Optional real cluster walkthrough
Requires Docker + kubectl + a working local Kubernetes cluster, e.g. kind/minikube. Not performed for this package:

```bash
cd config
docker build -t registration-demo:1.0.0 -f Dockerfile .
# Import image into the local cluster, e.g. `kind load docker-image registration-demo:1.0.0`
kubectl apply -f namespace.yaml
kubectl apply -f registration-deployment.yaml
kubectl -n aitu-demo rollout status deploy/registration
kubectl -n aitu-demo get pods -l app=registration -o wide
kubectl -n aitu-demo get service registration
kubectl -n aitu-demo delete pod <ONE_OF_THE_TWO_POD_NAMES>
kubectl -n aitu-demo get pods -w
kubectl -n aitu-demo describe deployment registration
```

For experiment 2, simulate a controller-level outage using `kubectl -n aitu-demo scale deployment registration --replicas=0` and later restore `--replicas=2`; unlike a pod crash, **scaling to zero prevents automatic self-healing**, so it must be recorded as a distinct failure model. For experiment 3, the demo app uses the `DB_AVAILABLE` environment variable, not a real database; changing it to `false` is an application-level **emulation**, not an actual DB incident. Record pod events, timestamps and HTTP response status for real measurements.

## Important limitations
- Baseline and improved availability estimates assume independent component failures and successful DB failover.
- No real cluster validation, deployment, load tests, or 500 ms latency measurements occurred here.
- RTO ≤15 minutes and RPO ≤5 minutes are design **targets**, not demonstrated guarantees.
- Replace student information, personal evidence and institution-assigned variant truthfully before submission.
