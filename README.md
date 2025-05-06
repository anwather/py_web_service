# Test Web Connectivity Service

A lightweight web service designed to verify network connectivity and provide basic system information. This service is particularly useful for testing connectivity to virtual machines or container environments, validating network paths, and verifying deployment configurations.

## Features

- Simple web interface with built-in documentation
- Hostname endpoint to identify the host machine
- Health check endpoint for monitoring and readiness probes
- Configurable via YAML file
- Deployable as a VM service or containerized application

## Quick Start

### Running Locally

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the service:
   ```bash
   python app.py
   ```

3. Access the service at http://localhost:5000

### Deploy on an Ubuntu VM

1. Copy the files to your server
2. Make the deployment script executable:
   ```bash
   chmod +x deploy.sh
   ```
3. Run the deployment script with sudo:
   ```bash
   sudo ./deploy.sh
   ```

### Run as a Container

1. Build the Docker image:
   ```bash
   docker build -t web-connectivity-service .
   ```

2. Run the container:
   ```bash
   docker run -d -p 5000:5000 --name connectivity-test web-connectivity-service
   ```

3. Access the service at http://localhost:5000

## Deployment Options

### Using Azure Container Registry (ACR)

To build and store your container in Azure Container Registry:

1. Create an Azure Container Registry (if you don't have one already):
   ```bash
   az group create --name myResourceGroup --location eastus
   az acr create --resource-group myResourceGroup --name myContainerRegistry --sku Basic --admin-enabled true
   ```

2. **Option A: Build using ACR Tasks (Recommended)**
   
   Build the container image directly in Azure Container Registry without Docker installed locally:
   
   ```bash
   # Quick task from local source code
   az acr build --registry myContainerRegistry --image web-connectivity-service:v1.0.0 --file Dockerfile .
   
   # Or from a Git repository
   az acr build --registry myContainerRegistry \
     --image web-connectivity-service:v1.0.0 \
     --file Dockerfile \
     https://github.com/yourusername/web-connectivity-service.git
   ```
   
   **Benefits of ACR Tasks:**
   - No local Docker installation required
   - Builds run in Azure (cloud-native)
   - Automatic OS and framework patching
   - Triggers on source code commits and base image updates
   - Multi-step tasks support with YAML

3. **Option B: Set up automated builds with triggers**

   Create a task that automatically rebuilds your image when source code changes:
   
   ```bash
   # Create a task that monitors a GitHub repository
   az acr task create \
     --registry myContainerRegistry \
     --name web-connectivity-build \
     --image web-connectivity-service:{{.Run.ID}} \
     --context https://github.com/yourusername/web-connectivity-service.git \
     --file Dockerfile \
     --git-access-token <personal-access-token>
   
   # Manually trigger the task
   az acr task run --registry myContainerRegistry --name web-connectivity-build
   ```

4. **Option C: Traditional local build and push**

   If you prefer building locally:
   
   ```bash
   # Authenticate to ACR
   az acr login --name myContainerRegistry
   
   # Build and tag the image
   docker build -t mycontainerregistry.azurecr.io/web-connectivity-service:v1.0.0 .
   
   # Push to ACR
   docker push mycontainerregistry.azurecr.io/web-connectivity-service:v1.0.0
   ```

5. Deploy from ACR to Azure services:

   **Azure Container Instances (ACI) with Managed Identity**:
   ```bash
   # Create a user-assigned managed identity
   az identity create --resource-group myResourceGroup --name myACIIdentity
   
   # Get the identity resource ID
   identityResourceId=$(az identity show --resource-group myResourceGroup --name myACIIdentity --query id --output tsv)
   
   # Assign AcrPull role to the identity
   acrResourceId=$(az acr show --name myContainerRegistry --resource-group myResourceGroup --query id --output tsv)
   az role assignment create --assignee-object-id $(az identity show --resource-group myResourceGroup --name myACIIdentity --query principalId --output tsv) --scope $acrResourceId --role AcrPull
   
   # Create container instance with managed identity
   az container create \
     --resource-group myResourceGroup \
     --name web-connectivity-service \
     --image mycontainerregistry.azurecr.io/web-connectivity-service:v1.0.0 \
     --assign-identity $identityResourceId \
     --registry-login-server mycontainerregistry.azurecr.io \
     --dns-name-label web-connectivity-service \
     --ports 5000
   ```

   **Azure App Service with Managed Identity (Recommended)**:
   ```bash
   # Create an App Service plan
   az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux

   # Create the web app
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myWebApp --deployment-container-image-name mycontainerregistry.azurecr.io/web-connectivity-service:v1.0.0

   # Enable managed identity
   az webapp identity assign --resource-group myResourceGroup --name myWebApp

   # Assign AcrPull role to the web app's managed identity
   principalId=$(az webapp identity show --resource-group myResourceGroup --name myWebApp --query principalId --output tsv)
   acrId=$(az acr show --name myContainerRegistry --resource-group myResourceGroup --query id --output tsv)
   az role assignment create --assignee $principalId --scope $acrId --role AcrPull

   # Configure web app to use managed identity for ACR
   az webapp config set --resource-group myResourceGroup --name myWebApp --generic-configurations '{"acrUseManagedIdentityCreds": true}'
   ```

### Azure Container Instances

Deploy to Azure Container Instances using the Azure CLI:

```bash
az container create \
  --resource-group myResourceGroup \
  --name web-connectivity-service \
  --image web-connectivity-service \
  --ports 5000 \
  --dns-name-label web-connectivity-service \
  --location eastus
```

### Azure App Service

Deploy as a containerized web app:

```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name web-connectivity-service \
  --deployment-container-image-name web-connectivity-service
```

## Configuration

The service can be configured by modifying the `config.yaml` file:

```yaml
server:
  port: 5000  # Change the port number
  host: '0.0.0.0'  # Change the host binding
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface with documentation |
| `/hostname` | GET | Returns the hostname of the server |
| `/health` | GET | Returns the health status of the service |
| `/network` | GET | Returns network information including IP address and DNS servers |

## Security Considerations

When deploying this service:

- Consider running behind a reverse proxy for TLS termination
- Configure appropriate network security rules to restrict access
- Use a non-root user for containerized deployments (implemented in the Dockerfile)
- Follow the principle of least privilege when setting up service accounts

## Testing with WSL (Windows Subsystem for Linux)

To test the container using WSL on your Windows machine:

1. Ensure WSL2 is installed and running:
   ```bash
   wsl --status
   ```

2. Start Docker Desktop and ensure WSL2 integration is enabled in Docker Desktop settings

3. Open a WSL terminal and navigate to your project directory:
   ```bash
   cd /mnt/c/Source/py_web_service  # Adjust path as needed
   ```

4. Build the container from WSL:
   ```bash
   docker build -t web-connectivity-service .
   ```

5. Run the container:
   ```bash
   docker run -d -p 5000:5000 --name connectivity-test web-connectivity-service
   ```

6. Test connectivity from WSL:
   ```bash
   curl http://localhost:5000/health
   curl http://localhost:5000/hostname
   curl http://localhost:5000/network
   ```

7. Access from Windows browser:
   - Open http://localhost:5000 in your Windows browser

8. Stop and clean up:
   ```bash
   docker stop connectivity-test
   docker rm connectivity-test
   ```

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Azure Container Instances Documentation](https://docs.microsoft.com/en-us/azure/container-instances/)