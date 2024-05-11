# Deploying File Store Application to Kind Cluster

This document provides step-by-step instructions on deploying the File Store application into a Kind (Kubernetes in Docker) cluster and accessing it.

## Prerequisites

- Kind installed on your local machine. Installation instructions can be found [here](https://kind.sigs.k8s.io/docs/user/quick-start/#installation).
- `kubectl` command-line tool installed and configured to communicate with your Kind cluster. Installation instructions can be found [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

## Steps

1. **Start Kind Cluster**:

   Start a Kind cluster using the following command:

   ```bash
   kind create cluster --name filestore-cluster
   ```

2. **Switch to the Assignment Context**:

   Switch to the `kind-assignment` context, which should already be configured to use the `assignment` namespace:

   ```bash
   kubectl config use-context kind-assignment
   ```

3. **Deploy Application**:

   Deploy the File Store application into the Kind cluster using the provided Kubernetes deployment and service files. Make sure you're in the directory where your Kubernetes configuration files are located:

   ```bash
   kubectl apply -f server-deployment.yaml
   kubectl apply -f server-service.yaml
   ```

4. **Accessing the Service**:

   Use port forwarding to access the service running in the Kind cluster. Run the following command:

   ```bash
   kubectl port-forward service/filestore-server 8080:5002
   ```

   This command forwards traffic from port `8080` on your local machine to port `5002` of the `filestore-server` service in the `assignment` namespace.

5. **Access the Service**:

   Once port forwarding is set up, you can access the service on your local machine at `http://localhost:8080`.

   ```bash
   curl http://localhost:8080/ls
   ```

   This command will send a GET request to the service to list files.

## Clean Up

To delete the Kind cluster and clean up resources:

```bash
kind delete cluster --name filestore-cluster
```

## Additional Notes

- Ensure that the port `8080` on your local machine is available and not being used by any other service.
