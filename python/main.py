import base64
import json
import datetime
import os
from google.cloud import netapp_v1

# Constants for backup management
BACKUP_LABEL_KEY = "createdby"
BACKUP_LABEL_VALUE = "hourly_backup_function"
NAME_PREFIX = "backup-"
MAX_BACKUPS = 24  # Number of backups to retain

def create_volume_backup(event, context):
    print("Received Pub/Sub trigger for NetApp Volume Backup creation.")
    
    # Decode Pub/Sub message
    message = base64.b64decode(event["data"]).decode()
    json_message = json.loads(message)
    
     # Retrieve configuration from environment variables
    myregion = os.environ.get("REGION")  # e.g., 'us-east4'
    myvolume = os.environ.get("VOLUME_NAME")  # e.g., 'standard-volume'
    myproject = os.environ.get("PROJECT_ID")  # e.g., 'rt11188354'
    backup_vault_id = os.environ.get("BACKUP_VAULT_NAME")  # e.g., 'test-backup
    
    # Generate a timestamped backup name
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"{NAME_PREFIX}{myvolume}-{timestamp}"
    
    # Create a client
    client = netapp_v1.NetAppClient()
    
    # Define the backup vault resource name and volume name
    backup_vault_name = f"projects/{myproject}/locations/{myregion}/backupVaults/{backup_vault_id}"
    volume_name = f"projects/{myproject}/locations/{myregion}/volumes/{myvolume}"
    
    try:
        # List existing backups with the specific label
        backups = client.list_backups(parent=backup_vault_name)
        
        # Filter backups with the specific label and sort by creation time
        labeled_backups = sorted(
            [backup for backup in backups if backup.labels.get(BACKUP_LABEL_KEY) == BACKUP_LABEL_VALUE],
            key=lambda b: b.create_time
        )
        
        # Check if there are already MAX_BACKUPS or more
        if len(labeled_backups) >= MAX_BACKUPS:
            # Delete the oldest backup first
            oldest_backup = labeled_backups[0]
            print(f"Deleting oldest backup: {oldest_backup.name}")
            delete_operation = client.delete_backup(name=oldest_backup.name)
            delete_operation.result()  # Wait for the delete operation to complete
            print(f"Oldest backup deleted: {oldest_backup.name}")
        
        # After deletion (if necessary), proceed to create the new backup
        print(f"Initiating new backup for volume {volume_name} in backup vault: {backup_vault_name}")
        
        # Define the backup creation request
        backup_request = netapp_v1.CreateBackupRequest(
            parent=backup_vault_name,
            backup_id=backup_name,
            backup=netapp_v1.Backup(
                source_volume=volume_name,
                labels={BACKUP_LABEL_KEY: BACKUP_LABEL_VALUE}
            )
        )
        
        # Make the request to create the backup
        operation = client.create_backup(request=backup_request)
        response = operation.result()
        print(f"Backup created successfully: {response.name}")
        
    except Exception as e:
        print(f"Error managing backups: {e}")
