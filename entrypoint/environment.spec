{
  "spec": {
	"name": "<name_uuid>",
	"resources": {
  	"substrate_definition_list": [
    	{
      	"uuid": "<substrate_uuid>",
      	"action_list": [],
      	"readiness_probe": {
        	"connection_type": "SSH",
        	"connection_port": 22,
        	"address": "@@{platform.status.resources.nic_list[0].ip_endpoint_list[0].ip}@@",
        	"delay_secs": "60",
        	"disable_readiness_probe": False,
        	"login_credential_local_reference": {
          	"kind": "app_credential",
          	"uuid": "<ahv_uuid>"
        	}
      	},
      	"editables": {
        	"readiness_probe": {
          	"connection_type": True,
          	"delay_secs": True,
          	"connection_port": True
        	},
        	"create_spec": {
          	"name": True,
          	"resources": {
            	"nic_list": {
              	"0": {
                	"subnet_reference": True
              	}
            	},
            	"serial_port_list": {},
            	"num_vcpus_per_socket": True,
            	"num_sockets": True,
            	"memory_size_mib": True,
            	"disk_list": {
              	"0": {
                	"data_source_reference": True,
                	"device_properties": {
                  	"device_type": True,
                  	"disk_address": {
                    	"adapter_type": True
                  	}
                	}
              	}
            	}
          	}
        	}
      	},
      	"os_type": "Linux",
      	"type": "AHV_VM",
      	"create_spec": {
        	"name": "lin-@@{calm_array_index}@@-@@{calm_time}@@",
        	"resources": {
          	"nic_list": [
            	{
              	"subnet_reference": {
                	"uuid": "<nic_uuid>"
              	}
            	}
          	],
          	"num_vcpus_per_socket": 1,
          	"num_sockets": 2,
          	"memory_size_mib": 4096,
          	"boot_config": {
            	"boot_device": {
              	"disk_address": {
                	"device_index": 0,
                	"adapter_type": "SCSI"
              	}
            	}
          	},
          	"disk_list": [
            	{
              	"data_source_reference": {
                	"kind": "image",
                	"name": "<image_name>",
                	"uuid": "<image_uuid>"
              	},
              	"device_properties": {
                	"disk_address": {
                  	"device_index": 0,
                  	"adapter_type": "SCSI"
                	},
                	"device_type": "DISK"
              	}
            	}
          	]
        	}
      	},
      	"variable_list": [],
      	"name": "Untitled"
    	}
  	],
  	"credential_definition_list": [
    	{
      	"name": "<name>",
      	"type": "PASSWORD",
      	"username": "<username>",
      	"secret": {
        	"attrs": {
          	"is_secret_modified": True
        	},
        	"value": "<password>"
      	},
      	"uuid": "<random_uuid>"
    	},
    	{
      	"name": "<name>",
      	"type": "KEY",
      	"username": "<username>",
      	"secret": {
        	"attrs": {
          	"is_secret_modified": True
        	},
        	"value": "<ssh_private_key>"
      	},
      	"uuid": "<random_uuid>"
    	}
  	]
	}
  },
  "api_version": "3.1.0",
  "metadata": {
	"kind": "environment",
	"uuid": "<env_uuid>",
	"owner_reference": {
  	"kind": "user",
  	"uuid": "00000000-0000-0000-0000-000000000000",
  	"name": "admin"
	},
	"name": "<name_uuid>"
  }
}
