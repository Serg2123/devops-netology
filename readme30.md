1.  
Cоздан аккаунт в AWS, создана техническая учетная запись для робота-терраформа (к ней примаплены директом нужные политики), создана одна виртуалка через web, вторая через консоль.  
```
vagrant@server4:/usr/bin$ aws configure list
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************CS7G              env
secret_key     ****************zzIz              env
    region                us-east-2      config-file    ~/.aws/config

vagrant@server4:/usr/bin$ aws iam list-users
{
    "Users": [
        {
            "Path": "/",
            "UserName": "terraform-robot",
            "UserId": "XXXXXXXXXXXXX",
            "Arn": "arn:aws:iam::000000000000:user/terraform-robot",
            "CreateDate": "2022-02-04T20:09:51Z"
        }
    ]
}

vagrant@server4:/usr/bin$ aws ec2 run-instances --image-id ami-0ba62214afa52bec7 --instance-type t2.micro --security-group-ids sg-a1969cd2
(вывод команды удален для экономии места, вывод конфигурации 2-х машин ниже в команде "ec2 describe-instances")

vagrant@server4:/usr/bin$ aws ec2 describe-instances
{
    "Reservations": [
        {
            "Groups": [],
            "Instances": [
                {
                    "AmiLaunchIndex": 0,
                    "ImageId": "ami-0231217be14a6f3ba",
                    "InstanceId": "i-05863298126a64553",
                    "InstanceType": "t2.micro",
                    "KeyName": "BaseSG",
                    "LaunchTime": "2022-02-04T20:44:27.000Z",
                    "Monitoring": {
                        "State": "disabled"
                    },
                    "Placement": {
                        "AvailabilityZone": "us-east-2a",
                        "GroupName": "",
                        "Tenancy": "default"
                    },
                    "PrivateDnsName": "ip-172-31-5-146.us-east-2.compute.internal",
                    "PrivateIpAddress": "172.31.5.146",
                    "ProductCodes": [],
                    "PublicDnsName": "ec2-52-15-102-24.us-east-2.compute.amazonaws.com",
                    "PublicIpAddress": "52.15.102.24",
                    "State": {
                        "Code": 16,
                        "Name": "running"
                    },
                    "StateTransitionReason": "",
                    "SubnetId": "subnet-eed17885",
                    "VpcId": "vpc-fcc74697",
                    "Architecture": "x86_64",
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": "/dev/xvda",
                            "Ebs": {
                                "AttachTime": "2022-02-04T20:44:28.000Z",
                                "DeleteOnTermination": true,
                                "Status": "attached",
                                "VolumeId": "vol-00c3371b776a51e5f"
                            }
                        }
                    ],
                    "ClientToken": "",
                    "EbsOptimized": false,
                    "EnaSupport": true,
                    "Hypervisor": "xen",
                    "NetworkInterfaces": [
                        {
                            "Association": {
                                "IpOwnerId": "amazon",
                                "PublicDnsName": "ec2-52-15-102-24.us-east-2.compute.amazonaws.com",
                                "PublicIp": "52.15.102.24"
                            },
                            "Attachment": {
                                "AttachTime": "2022-02-04T20:44:27.000Z",
                                "AttachmentId": "eni-attach-00caa76fa0123f2d3",
                                "DeleteOnTermination": true,
                                "DeviceIndex": 0,
                                "Status": "attached",
                                "NetworkCardIndex": 0
                            },
                            "Description": "",
                            "Groups": [
                                {
                                    "GroupName": "default",
                                    "GroupId": "sg-a1969cd2"
                                }
                            ],
                            "Ipv6Addresses": [],
                            "MacAddress": "02:e4:15:0c:5b:6a",
                            "NetworkInterfaceId": "eni-05dc11969a84285a3",
                            "OwnerId": "226394831183",
                            "PrivateDnsName": "ip-172-31-5-146.us-east-2.compute.internal",
                            "PrivateIpAddress": "172.31.5.146",
                            "PrivateIpAddresses": [
                                {
                                    "Association": {
                                        "IpOwnerId": "amazon",
                                        "PublicDnsName": "ec2-52-15-102-24.us-east-2.compute.amazonaws.com",
                                        "PublicIp": "52.15.102.24"
                                    },
                                    "Primary": true,
                                    "PrivateDnsName": "ip-172-31-5-146.us-east-2.compute.internal",
                                    "PrivateIpAddress": "172.31.5.146"
                                }
                            ],
                            "SourceDestCheck": true,
                            "Status": "in-use",
                            "SubnetId": "subnet-eed17885",
                            "VpcId": "vpc-fcc74697",
                            "InterfaceType": "interface"
                        }
                    ],
                    "RootDeviceName": "/dev/xvda",
                    "RootDeviceType": "ebs",
                    "SecurityGroups": [
                        {
                            "GroupName": "default",
                            "GroupId": "sg-a1969cd2"
                        }
                    ],
                    "SourceDestCheck": true,
                    "VirtualizationType": "hvm",
                    "CpuOptions": {
                        "CoreCount": 1,
                        "ThreadsPerCore": 1
                    },
                    "CapacityReservationSpecification": {
                        "CapacityReservationPreference": "open"
                    },
                    "HibernationOptions": {
                        "Configured": false
                    },
                    "MetadataOptions": {
                        "State": "applied",
                        "HttpTokens": "optional",
                        "HttpPutResponseHopLimit": 1,
                        "HttpEndpoint": "enabled",
                        "HttpProtocolIpv6": "disabled",
                        "InstanceMetadataTags": "disabled"
                    },
                    "EnclaveOptions": {
                        "Enabled": false
                    },
                    "PlatformDetails": "Linux/UNIX",
                    "UsageOperation": "RunInstances",
                    "UsageOperationUpdateTime": "2022-02-04T20:44:27.000Z",
                    "PrivateDnsNameOptions": {
                        "HostnameType": "ip-name",
                        "EnableResourceNameDnsARecord": true,
                        "EnableResourceNameDnsAAAARecord": false
                    }
                }
            ],
            "OwnerId": "226394831183",
            "ReservationId": "r-0956f2c828b32a995"
        },
        {
            "Groups": [],
            "Instances": [
                {
                    "AmiLaunchIndex": 0,
                    "ImageId": "ami-0ba62214afa52bec7",
                    "InstanceId": "i-0d7595d0a00e922cd",
                    "InstanceType": "t2.micro",
                    "LaunchTime": "2022-02-04T20:45:57.000Z",
                    "Monitoring": {
                        "State": "disabled"
                    },
                    "Placement": {
                        "AvailabilityZone": "us-east-2a",
                        "GroupName": "",
                        "Tenancy": "default"
                    },
                    "PrivateDnsName": "ip-172-31-4-227.us-east-2.compute.internal",
                    "PrivateIpAddress": "172.31.4.227",
                    "ProductCodes": [],
                    "PublicDnsName": "ec2-13-58-35-241.us-east-2.compute.amazonaws.com",
                    "PublicIpAddress": "13.58.35.241",
                    "State": {
                        "Code": 16,
                        "Name": "running"
                    },
                    "StateTransitionReason": "",
                    "SubnetId": "subnet-eed17885",
                    "VpcId": "vpc-fcc74697",
                    "Architecture": "x86_64",
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": "/dev/sda1",
                            "Ebs": {
                                "AttachTime": "2022-02-04T20:45:58.000Z",
                                "DeleteOnTermination": true,
                                "Status": "attached",
                                "VolumeId": "vol-0474685fc76a5146c"
                            }
                        }
                    ],
                    "ClientToken": "b4167d70-4f56-4965-9735-f6aa5ff16e14",
                    "EbsOptimized": false,
                    "EnaSupport": true,
                    "Hypervisor": "xen",
                    "NetworkInterfaces": [
                        {
                            "Association": {
                                "IpOwnerId": "amazon",
                                "PublicDnsName": "ec2-13-58-35-241.us-east-2.compute.amazonaws.com",
                                "PublicIp": "13.58.35.241"
                            },
                            "Attachment": {
                                "AttachTime": "2022-02-04T20:45:57.000Z",
                                "AttachmentId": "eni-attach-069b5e5709785eb7c",
                                "DeleteOnTermination": true,
                                "DeviceIndex": 0,
                                "Status": "attached",
                                "NetworkCardIndex": 0
                            },
                            "Description": "",
                            "Groups": [
                                {
                                    "GroupName": "default",
                                    "GroupId": "sg-a1969cd2"
                                }
                            ],
                            "Ipv6Addresses": [],
                            "MacAddress": "02:1f:a8:f9:2e:06",
                            "NetworkInterfaceId": "eni-0bd87b8321be005d8",
                            "OwnerId": "226394831183",
                            "PrivateDnsName": "ip-172-31-4-227.us-east-2.compute.internal",
                            "PrivateIpAddress": "172.31.4.227",
                            "PrivateIpAddresses": [
                                {
                                    "Association": {
                                        "IpOwnerId": "amazon",
                                        "PublicDnsName": "ec2-13-58-35-241.us-east-2.compute.amazonaws.com",
                                        "PublicIp": "13.58.35.241"
                                    },
                                    "Primary": true,
                                    "PrivateDnsName": "ip-172-31-4-227.us-east-2.compute.internal",
                                    "PrivateIpAddress": "172.31.4.227"
                                }
                            ],
                            "SourceDestCheck": true,
                            "Status": "in-use",
                            "SubnetId": "subnet-eed17885",
                            "VpcId": "vpc-fcc74697",
                            "InterfaceType": "interface"
                        }
                    ],
                    "RootDeviceName": "/dev/sda1",
                    "RootDeviceType": "ebs",
                    "SecurityGroups": [
                        {
                            "GroupName": "default",
                            "GroupId": "sg-a1969cd2"
                        }
                    ],
                    "SourceDestCheck": true,
                    "VirtualizationType": "hvm",
                    "CpuOptions": {
                        "CoreCount": 1,
                        "ThreadsPerCore": 1
                    },
                    "CapacityReservationSpecification": {
                        "CapacityReservationPreference": "open"
                    },
                    "HibernationOptions": {
                        "Configured": false
                    },
                    "MetadataOptions": {
                        "State": "applied",
                        "HttpTokens": "optional",
                        "HttpPutResponseHopLimit": 1,
                        "HttpEndpoint": "enabled",
                        "HttpProtocolIpv6": "disabled",
                        "InstanceMetadataTags": "disabled"
                    },
                    "EnclaveOptions": {
                        "Enabled": false
                    },
                    "PlatformDetails": "Red Hat Enterprise Linux",
                    "UsageOperation": "RunInstances:0010",
                    "UsageOperationUpdateTime": "2022-02-04T20:45:57.000Z",
                    "PrivateDnsNameOptions": {
                        "HostnameType": "ip-name",
                        "EnableResourceNameDnsARecord": false,
                        "EnableResourceNameDnsAAAARecord": false
                    }
                }
            ],
            "OwnerId": "226394831183",
            "ReservationId": "r-07b832b718048bb66"
        }
    ]
}
vagrant@server4:/usr/bin$
```
  
2.  
Конфиги терраформа тут:  
[конфиги](https://github.com/Serg2123/devops-netology/blob/main/terraform/)  
  
Terraform plan без ошибок:  
```
vagrant@server4:~/terraform$ terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # aws_instance.web-test will be created
  + resource "aws_instance" "web-test" {
      + ami                                  = "ami-039af3bfc52681cd5"
      + arn                                  = (known after apply)
      + associate_public_ip_address          = (known after apply)
      + availability_zone                    = (known after apply)
      + cpu_core_count                       = (known after apply)
      + cpu_threads_per_core                 = (known after apply)
      + disable_api_termination              = (known after apply)
      + ebs_optimized                        = (known after apply)
      + get_password_data                    = false
      + host_id                              = (known after apply)
      + id                                   = (known after apply)
      + instance_initiated_shutdown_behavior = (known after apply)
      + instance_state                       = (known after apply)
      + instance_type                        = "t2.micro"
      + ipv6_address_count                   = (known after apply)
      + ipv6_addresses                       = (known after apply)
      + key_name                             = "BaseSG"
      + monitoring                           = (known after apply)
      + outpost_arn                          = (known after apply)
      + password_data                        = (known after apply)
      + placement_group                      = (known after apply)
      + placement_partition_number           = (known after apply)
      + primary_network_interface_id         = (known after apply)
      + private_dns                          = (known after apply)
      + private_ip                           = (known after apply)
      + public_dns                           = (known after apply)
      + public_ip                            = (known after apply)
      + secondary_private_ips                = (known after apply)
      + security_groups                      = (known after apply)
      + source_dest_check                    = true
      + subnet_id                            = "subnet-eed17885"
      + tags                                 = {
          + "Name" = "Hello Netology!"
        }
      + tags_all                             = {
          + "Name" = "Hello Netology!"
        }
      + tenancy                              = (known after apply)
      + user_data                            = (known after apply)
      + user_data_base64                     = (known after apply)
      + vpc_security_group_ids               = (known after apply)

      + capacity_reservation_specification {
          + capacity_reservation_preference = (known after apply)

          + capacity_reservation_target {
              + capacity_reservation_id = (known after apply)
            }
        }

      + ebs_block_device {
          + delete_on_termination = (known after apply)
          + device_name           = (known after apply)
          + encrypted             = (known after apply)
          + iops                  = (known after apply)
          + kms_key_id            = (known after apply)
          + snapshot_id           = (known after apply)
          + tags                  = (known after apply)
          + throughput            = (known after apply)
          + volume_id             = (known after apply)
          + volume_size           = (known after apply)
          + volume_type           = (known after apply)
        }

      + enclave_options {
          + enabled = (known after apply)
        }

      + ephemeral_block_device {
          + device_name  = (known after apply)
          + no_device    = (known after apply)
          + virtual_name = (known after apply)
        }

      + metadata_options {
          + http_endpoint               = (known after apply)
          + http_put_response_hop_limit = (known after apply)
          + http_tokens                 = (known after apply)
          + instance_metadata_tags      = (known after apply)
        }

      + network_interface {
          + delete_on_termination = (known after apply)
          + device_index          = (known after apply)
          + network_interface_id  = (known after apply)
        }

      + root_block_device {
          + delete_on_termination = (known after apply)
          + device_name           = (known after apply)
          + encrypted             = (known after apply)
          + iops                  = (known after apply)
          + kms_key_id            = (known after apply)
          + tags                  = (known after apply)
          + throughput            = (known after apply)
          + volume_id             = (known after apply)
          + volume_size           = (known after apply)
          + volume_type           = (known after apply)
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + account_id          = "226394831183"
  + aws-reg             = "us-east-2"
  + caller_arn          = "arn:aws:iam::226394831183:user/terraform-robot"
  + external_ip_address = (known after apply)
  + internal_ip_address = (known after apply)
  + subnet_id           = "subnet-eed17885"
  + user_id             = "AIDATJNRO7FHUCUHFX2ZS"

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if
you run "terraform apply" now.
```
