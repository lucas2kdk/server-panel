"""
Kubernetes client for managing game server resources.
"""
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import os
import logging

logger = logging.getLogger(__name__)


class KubernetesClient:
    """Client for interacting with Kubernetes API to manage game servers."""

    def __init__(self):
        """Initialize Kubernetes client."""
        # Load config based on environment
        if os.getenv('K8S_IN_CLUSTER', 'false').lower() == 'true':
            config.load_incluster_config()
        else:
            try:
                config.load_kube_config()
            except Exception as e:
                logger.warning(f"Could not load kube config: {e}. Using default configuration.")

        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()
        self.namespace = os.getenv('K8S_NAMESPACE', 'game-servers')

    def create_minecraft_server(self, server_name: str, server_config: dict) -> dict:
        """
        Create a Minecraft server in Kubernetes.

        Args:
            server_name: Kubernetes-compliant server name
            server_config: Configuration dict with server_type, server_version, cpu_cores, ram_mb, disk_gb

        Returns:
            Dict with pvc_name, pod_name, service_name

        Raises:
            ApiException: If Kubernetes API call fails
        """
        try:
            # Create StatefulSet (includes PVC via volumeClaimTemplates)
            statefulset = self._create_statefulset(server_name, server_config)

            # Create Service
            service = self._create_service(server_name)

            logger.info(f"Created Minecraft server: {server_name}")

            return {
                'pvc_name': f"{server_name}-data-{server_name}-0",
                'pod_name': f"{server_name}-0",
                'service_name': service.metadata.name
            }

        except ApiException as e:
            logger.error(f"Failed to create server {server_name}: {e}")
            raise

    def _create_statefulset(self, name: str, config: dict):
        """Create StatefulSet for Minecraft server."""
        # Container definition
        container = client.V1Container(
            name="minecraft",
            image=self._get_server_image(config['server_type']),
            ports=[client.V1ContainerPort(container_port=25565, name="minecraft")],
            env=[
                client.V1EnvVar(name="EULA", value="TRUE"),
                client.V1EnvVar(name="TYPE", value=config['server_type'].upper()),
                client.V1EnvVar(name="VERSION", value=config['server_version']),
                client.V1EnvVar(name="MEMORY", value=f"{config['ram_mb']}M"),
                client.V1EnvVar(name="JVM_OPTS", value=f"-Xms{config['ram_mb']}M -Xmx{config['ram_mb']}M"),
            ],
            resources=client.V1ResourceRequirements(
                requests={
                    'cpu': f"{config['cpu_cores']}",
                    'memory': f"{config['ram_mb']}Mi"
                },
                limits={
                    'cpu': f"{config['cpu_cores']}",
                    'memory': f"{config['ram_mb']}Mi"
                }
            ),
            volume_mounts=[
                client.V1VolumeMount(
                    name="data",
                    mount_path="/data"
                )
            ]
        )

        # Pod template
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={
                    "app": "minecraft",
                    "server": name
                }
            ),
            spec=client.V1PodSpec(
                containers=[container]
            )
        )

        # VolumeClaimTemplate
        volume_claim_template = client.V1PersistentVolumeClaim(
            metadata=client.V1ObjectMeta(name="data"),
            spec=client.V1PersistentVolumeClaimSpec(
                access_modes=["ReadWriteOnce"],
                resources=client.V1ResourceRequirements(
                    requests={'storage': f"{config['disk_gb']}Gi"}
                )
            )
        )

        # StatefulSet
        statefulset = client.V1StatefulSet(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1StatefulSetSpec(
                service_name=name,
                replicas=1,
                selector=client.V1LabelSelector(
                    match_labels={"app": "minecraft", "server": name}
                ),
                template=template,
                volume_claim_templates=[volume_claim_template]
            )
        )

        return self.apps_api.create_namespaced_stateful_set(
            namespace=self.namespace,
            body=statefulset
        )

    def _create_service(self, name: str):
        """Create Service for Minecraft server."""
        service = client.V1Service(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1ServiceSpec(
                selector={"app": "minecraft", "server": name},
                ports=[
                    client.V1ServicePort(
                        name="minecraft",
                        port=25565,
                        target_port=25565,
                        protocol="TCP"
                    )
                ],
                type="ClusterIP"
            )
        )

        return self.core_api.create_namespaced_service(
            namespace=self.namespace,
            body=service
        )

    def _get_server_image(self, server_type: str) -> str:
        """Get Docker image for server type."""
        images = {
            'vanilla': 'itzg/minecraft-server:latest',
            'paper': 'itzg/minecraft-server:latest',
            'spigot': 'itzg/minecraft-server:latest',
            'forge': 'itzg/minecraft-server:latest',
            'fabric': 'itzg/minecraft-server:latest'
        }
        return images.get(server_type, 'itzg/minecraft-server:latest')

    def delete_server(self, server_name: str) -> None:
        """
        Delete all Kubernetes resources for a server.

        Args:
            server_name: Kubernetes server name
        """
        try:
            # Delete StatefulSet
            self.apps_api.delete_namespaced_stateful_set(
                name=server_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions()
            )
            logger.info(f"Deleted StatefulSet: {server_name}")

            # Delete Service
            self.core_api.delete_namespaced_service(
                name=server_name,
                namespace=self.namespace
            )
            logger.info(f"Deleted Service: {server_name}")

            # Delete PVC
            pvc_name = f"{server_name}-data-{server_name}-0"
            self.core_api.delete_namespaced_persistent_volume_claim(
                name=pvc_name,
                namespace=self.namespace
            )
            logger.info(f"Deleted PVC: {pvc_name}")

        except ApiException as e:
            logger.error(f"Error deleting server {server_name}: {e}")
            raise

    def get_server_status(self, pod_name: str) -> str:
        """
        Get the status of a server pod.

        Args:
            pod_name: Name of the pod

        Returns:
            Status string: Running, Pending, Failed, Unknown
        """
        try:
            pod = self.core_api.read_namespaced_pod(
                name=pod_name,
                namespace=self.namespace
            )
            return pod.status.phase
        except ApiException as e:
            logger.error(f"Error getting pod status for {pod_name}: {e}")
            return 'Unknown'

    def start_server(self, server_name: str) -> None:
        """
        Start a stopped server by scaling StatefulSet to 1.

        Args:
            server_name: Kubernetes server name
        """
        try:
            # Patch StatefulSet to set replicas=1
            body = {'spec': {'replicas': 1}}
            self.apps_api.patch_namespaced_stateful_set(
                name=server_name,
                namespace=self.namespace,
                body=body
            )
            logger.info(f"Started server: {server_name}")

        except ApiException as e:
            logger.error(f"Error starting server {server_name}: {e}")
            raise

    def stop_server(self, server_name: str) -> None:
        """
        Stop a running server by scaling StatefulSet to 0.

        Args:
            server_name: Kubernetes server name
        """
        try:
            # Patch StatefulSet to set replicas=0
            body = {'spec': {'replicas': 0}}
            self.apps_api.patch_namespaced_stateful_set(
                name=server_name,
                namespace=self.namespace,
                body=body
            )
            logger.info(f"Stopped server: {server_name}")

        except ApiException as e:
            logger.error(f"Error stopping server {server_name}: {e}")
            raise

    def get_server_logs(self, pod_name: str, tail_lines: int = 100) -> str:
        """
        Get logs from a server pod.

        Args:
            pod_name: Name of the pod
            tail_lines: Number of lines to retrieve

        Returns:
            Log output as string
        """
        try:
            logs = self.core_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=self.namespace,
                tail_lines=tail_lines
            )
            return logs
        except ApiException as e:
            logger.error(f"Error fetching logs for {pod_name}: {e}")
            return f"Error fetching logs: {str(e)}"

    def exec_command(self, pod_name: str, command: list) -> str:
        """
        Execute a command in a pod.

        Args:
            pod_name: Name of the pod
            command: Command to execute as list

        Returns:
            Command output as string
        """
        try:
            resp = stream(
                self.core_api.connect_get_namespaced_pod_exec,
                pod_name,
                self.namespace,
                command=command,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False
            )
            return resp
        except ApiException as e:
            logger.error(f"Error executing command in {pod_name}: {e}")
            return f"Error: {str(e)}"

    def list_files(self, pod_name: str, path: str = '/data') -> str:
        """
        List files in a directory in the pod.

        Args:
            pod_name: Name of the pod
            path: Directory path

        Returns:
            ls command output
        """
        command = ['ls', '-la', '--time-style=+%Y-%m-%d %H:%M:%S', path]
        return self.exec_command(pod_name, command)

    def read_file(self, pod_name: str, filepath: str) -> str:
        """
        Read a file from the pod.

        Args:
            pod_name: Name of the pod
            filepath: Full path to file

        Returns:
            File contents
        """
        command = ['cat', filepath]
        return self.exec_command(pod_name, command)

    def write_file(self, pod_name: str, filepath: str, content: str) -> str:
        """
        Write content to a file in the pod.

        Args:
            pod_name: Name of the pod
            filepath: Full path to file
            content: Content to write

        Returns:
            Command output
        """
        # Escape content for shell
        safe_content = content.replace("'", "'\\''")
        command = ['sh', '-c', f"cat > {filepath} << 'EOF'\n{safe_content}\nEOF"]
        return self.exec_command(pod_name, command)
