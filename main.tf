provider "google" {
    credentials = file("../sa/tf-sa.json")
}


# locals {
#   apis_enable = ["iam.googleapis.com","compute.googleapis.com","storage.googleapis.com"]
# }

resource "google_project" "test-proj" {
    name = "terraform-foundation"
    project_id = "terraform-foundation-2424"
    org_id = "137290607384"
    billing_account = "010B72-FF5807-E920FD"
}

# resource "google_project_service" "apis_enable" {
#     count = length(local.apis_enable)
#     project = "terraform-foundation-2424"
#     service = local.apis_enable[count.index]
#     disable_dependent_services = true
# }

resource "google_project_service" "enable_api" {
    count = length(var.api_enable_list)
    project = "terraform-foundation-2424"
    service = var.api_enable_list[count.index]
    disable_dependent_services = true
}

# resource "google_project_service" "api_enable" {
#     project = "terraform-foundation-2424"
#     for_each = toset(var.api_enable_list)
#     service = each.value
# }

variable "api_enable_list" {
    type = list(string)
    description = "apis to be enabled for the project"
    default = [ "iam.googleapis.com","storage.googleapis.com",
                "compute.googleapis.com" ]
    
}

#VM
resource "google_compute_instance" "first_vm" {
  name         = "terraform-vm-2"
  machine_type = "e2-small"
  project      = var.project_id
  zone         = "asia-east1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network            = data.google_compute_network.custom-network.id
    subnetwork         = data.google_compute_subnetwork.cutom-subnet.id
    subnetwork_project = data.google_compute_subnetwork.cutom-subnet.project
  }

  service_account {
    email  = google_service_account.service_account.email
    scopes = ["cloud-platform"]
  }

  allow_stopping_for_update = true
}

#data source

data "google_compute_network" "custom-network" {
  name    = "custom-vpc-2"
  project = var.project_id
}

data "google_compute_subnetwork" "cutom-subnet" {
  name    = "subnet-1"
  project = var.project_id
  region  = "asia-east1"
}

#instance template

resource "google_compute_instance_template" "nirma_template" {
  name = "nirma-review-instance-template"
  #name_prefix = "instance-template-"
  description = "template to create vm instances for the blog app"

  instance_description = "instance with startup script"
  machine_type         = "e2-medium"
  project              = var.project_id

  disk {
    source_image = "debian-cloud/debian-11"
  }

  network_interface {
    network            = data.google_compute_network.custom-network.id
    subnetwork         = data.google_compute_subnetwork.cutom-subnet.id
    subnetwork_project = var.project_id
  }
  service_account {
    email  = google_service_account.service_account.email
    scopes = ["cloud-platform"]
  }

  lifecycle {
    create_before_destroy = true
  }

  #metadata_startup_script = 

}

#mig

resource "google_compute_instance_group_manager" "nirma-server" {
  name               = "nirma-igm"
  base_instance_name = "blog-app"
  zone               = "asia-east1-b"
  project            = var.project_id

  version {
    instance_template = google_compute_instance_template.nirma_template.self_link_unique
  }

  target_pools = [google_compute_target_pool.default-target-pool.id]
}

#target pool
resource "google_compute_target_pool" "default-target-pool" {
  name    = "nirma-target-pool"
  region  = "asia-east1"
  project = var.project_id
}

#auto scaler. so no need to define target in resource igm.
resource "google_compute_autoscaler" "default-autoscaler" {

  name    = "nirma-autoscaler"
  zone    = "asia-east1-b"
  project = var.project_id
  target  = google_compute_instance_group_manager.nirma-server.id

  autoscaling_policy {
    max_replicas    = 3
    min_replicas    = 1
    cooldown_period = 60

    cpu_utilization {
      target = 0.6
    }
  }
}

#sa

#creating a new sa to deploy a compute engine
resource "google_service_account" "service_account" {
  account_id   = "compute-engine-sa"
  display_name = "service account to create compute engine"
  project      = var.project_id
}

# resource "google_service_account_iam_binding" "compute_engine_editor_binding" {
#   role    = "roles/editor"
#   members = ["compute-engine-sa@terraform-foundation-2424.iam.gserviceaccount.com"]
#   depends_on = [
#     google_service_account.service_account
#   ]
#   service_account_id = google_service_account.service_account.name
# }

#VPC

resource "google_compute_network" "custom_vpc_network" {
  name                    = "custom-vpc"
  project                 = var.project_id
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
}

resource "google_compute_subnetwork" "subnet-1" {
  name          = "subnet-mumbai"
  region        = "asia-south1"
  ip_cidr_range = "10.10.1.0/28"
  project       = var.project_id
  network       = google_compute_network.custom_vpc_network.id
}

resource "google_compute_subnetwork" "subnet-2" {
  name          = "subnet-delhi"
  region        = "asia-south2"
  ip_cidr_range = "172.16.0.0/24"
  project       = var.project_id
  network       = google_compute_network.custom_vpc_network.id
}

output "network_op" {
  value = google_compute_network.custom_vpc_network.id
}

output "network_op2" {
  value = google_compute_network.custom_vpc_network.self_link
}

