terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

#Set SSH key
variable "pvt_key" {}

#Digital Ocean token
variable "do_token" {}


#Specify Terraform provider
provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_ssh_key" "digital_ocean1" {
  name = "digital_ocean1"
}

resource "digitalocean_droplet" "web" {
  image              = "ubuntu-18-04-x64"
  name               = "web-1"
  region             = "lon1"
  #size               = "s-1vcpu-1gb"
  size               = "s-4vcpu-8gb"
  ssh_keys = [
    data.digitalocean_ssh_key.digital_ocean1.id
  ]

  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    private_key = file(var.pvt_key)
    timeout = "2m"
  }

  provisioner "file" {
    source = "docker-airflow-setup.sh"
    destination = "~/docker-airflow-setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "useradd -c 'ronan' -m ronan -s /bin/bash",
      "echo ronan:ronan | chpasswd",
      "usermod -aG sudo ronan",
      "rsync --archive --chown=ronan:ronan ~/.ssh /home/ronan",
      "chmod 600 /home/ronan/.ssh/authorized_keys",
      "chmod 700 /home/ronan/.ssh",
      #"su ronan -c 'echo ronan | sudo -S chmod +x /root/docker-airflow-setup.sh'",
      #"su ronan -c 'echo ronan | sudo -S /root/docker-airflow-setup.sh'"
    ]
  }

}
