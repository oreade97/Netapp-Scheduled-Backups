resource "google_cloud_scheduler_job" "netapp_backup_job" {
  name             = "netapp-backup-job"
  description      = "Scheduled job to trigger NetApp volume backup"
  schedule         = var.backup_schedule
  time_zone        = "UTC"
  pubsub_target {
    topic_name = google_pubsub_topic.netapp_backup_topic.id
    data       = base64encode("{\"message\": \"Trigger NetApp Volume Backup\"}")
  }
}
