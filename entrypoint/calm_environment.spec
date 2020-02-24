{
  "spec": {
	"name": "<name>",
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
        	"disable_readiness_probe": false,
        	"login_credential_local_reference": {
          	"kind": "app_credential",
          	"uuid": "<ahv_uuid>"
        	}
      	},
      	"editables": {
        	"readiness_probe": {
          	"connection_type": true,
          	"delay_secs": true,
          	"connection_port": true
        	},
        	"create_spec": {
          	"name": true,
          	"resources": {
            	"nic_list": {
              	"0": {
                	"subnet_reference": true
              	}
            	},
            	"serial_port_list": {},
            	"num_vcpus_per_socket": true,
            	"num_sockets": true,
            	"memory_size_mib": true,
            	"disk_list": {
              	"0": {
                	"data_source_reference": true,
                	"device_properties": {
                  	"device_type": true,
                  	"disk_address": {
                    	"adapter_type": true
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
          	"is_secret_modified": true
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
          	"is_secret_modified": true
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
	"owner_reference": {
  	"kind": "user",
  	"uuid": "00000000-0000-0000-0000-000000000000",
  	"name": "admin"
	},
	"name": "<name>"
  }
}
