resource "google_netapp_backup_vault" "test_backup_vault" {
  name = "test-backup-vault"
  location = "us-east4"
  description = "Terraform created vault"
  labels = { 
    "creator": "testuser"
  }
}