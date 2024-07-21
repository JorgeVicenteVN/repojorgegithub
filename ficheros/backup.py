import subprocess
import os
from datetime import datetime

# Configura tus parámetros
NAMESPACE = 'default'
BACKUP_DIR = r'C:\\Users\\0020360\\CursoKubernetes\\backup'
DATE_STR = datetime.now().strftime('%Y%m%d_%H%M%S')

# Crea el directorio de respaldo si no existe
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Función para ejecutar comandos y capturar la salida
def run_command(command, output_file):
    """Ejecuta un comando del sistema y guarda la salida en un archivo."""
    print(f'Ejecutando comando: {command}')
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    with open(output_file, 'w') as f:
        f.write(result.stdout)
    print(f'Archivo guardado en: {output_file}')

def backup_kubernetes_resources():
    """Realiza una copia de seguridad de todos los recursos de Kubernetes en el namespace especificado."""
    print(f'Iniciando respaldo de recursos de Kubernetes en el namespace: {NAMESPACE}')
    
    # Obtener todos los recursos importantes
    resources = [
        'deployments', 'services', 'pods', 'configmaps', 'secrets', 'ingresses',
        'persistentvolumeclaims', 'statefulsets', 'daemonsets', 'replicasets'
    ]
    
    for resource in resources:
        # Definir la ruta para el archivo de respaldo de cada recurso
        resource_backup_file = os.path.join(BACKUP_DIR, f'{resource}_{DATE_STR}.yaml')
        command = f'kubectl get {resource} --namespace {NAMESPACE} -o yaml'
        run_command(command, resource_backup_file)

    print(f'Los recursos de Kubernetes han sido respaldados.')

def backup_postgresql():
    """Realiza una copia de seguridad de la base de datos PostgreSQL."""
    print('Iniciando respaldo de la base de datos PostgreSQL')

    # Obtener el nombre del pod de PostgreSQL
    command = "kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    pod_name = result.stdout.strip()
    
    if pod_name:
        # Comando para hacer respaldo de PostgreSQL
        command = f'docker exec -t {pod_name} pg_dump -U myuser mydb'
        backup_command = f'docker exec -t {pod_name} pg_dump -U myuser mydb > {os.path.join(BACKUP_DIR, f"postgres_backup_{DATE_STR}.sql")}'
        run_command(backup_command, os.path.join(BACKUP_DIR, f"postgres_backup_{DATE_STR}.sql"))
    else:
        print("No se encontró el pod de PostgreSQL.")

# Ejecuta las copias de seguridad
backup_kubernetes_resources()
backup_postgresql()
