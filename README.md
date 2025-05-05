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