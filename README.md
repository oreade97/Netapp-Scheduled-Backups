This repository contains a Google Cloud Function that automates the creation and management of NetApp volume backups. The function ensures a maximum of 24 backups created by the function are retained, appending a specific label to these backups. When more than 24 backups exist, the oldest backup is deleted before creating a new one.
The function is designed to be triggered by Cloud Scheduler through a Pub/Sub topic, ensuring backups are created on a regular schedule.

### **How it works**
#### **Architecture Diagram**

![[Pasted image 20241203101853.png]]
#### **Prerequisites**
##### APIs
The following APIs need to be enabled in your GCP project
- Cloud Functions API
- Cloud Build API
- Pub/Sub API
- NetApp API
- Cloud Scheduler API
The "apis.tf" file automatically enables the apis needed through Terraform.
##### **Permissions**
The user needs to have the Google cloud NetApp Volumes "NetApp Admin" role to use this script successfully. If deploying through terraform, then the terraform service account needs this role. 
The "iam.tf" file automatically grants the service account this role through Terraform

#### **Usage**

Clone the repository
```
git clone https://github.com/oreade97/Netapp-Scheduled-Backups.git
```

Enter the "Terraform Files" folder and add a ".tfvars" file to store the variables below

| Variable                 | Description                                                               |
|--------------------------|---------------------------------------------------------------------------|
| project_id               | The google cloud project id                                               |
| region                   | The region where netapp resources exist and the function will be deployed |
| service_account_key_file | The file containing your service account keys                             |
| volume_name              | Name of the volume to schedule backups for                                |
| backup_schedule          | Frequency and Time of backup in cron format                               |
| backup_vault_name        | The name of the backup vault to be created                                |

Enter "backup.tf" and change location to the region where you would like to create the backup vault. The region should be the same as the region where the volume is.

Once done, you can enter the "Backup Function" folder and edit the main.py file

| Variable           | Description                           |
|--------------------|---------------------------------------|
| BACKUP_LABEL_KEY   | Label key for the scheduled backups   |
| BACKUP_LABEL_VALUE | Label value for the scheduled backups |
| MAX_BACKUPS        | Total number of backups to keep       |

Once done, zip up the backup function folder and name it "backup.zip" or the name that was provided in the "cloudfunction.tf" file.

You can now initialize terraform in the folder with 
```
terraform init
```

Run a terraform plan to see the output of resources to be deployed
```
terraform plan
```

Apply the pan and deploy the resources with
```
terraform apply
```


#### Contributions
If you would like to contribute to this project, please create a new issue.