{
   "entities":[
      {
         "bp_name":"CentOS_IaaS",
         "mp_name":"CentOS",
         "icon_name":"CentOS",
         "app_source": "LOCAL",
         "bp_version":"1.0.0",
         "mp_description":"CentOS 7 1810 Developer Workstation with Gnome Desktop Environment installed. While launching the blueprint, the end user can specify their unique password.\\n#### Hardware Requirement:\\n*2 vCPU with 4 GiB of Memory\\n#### Lifecycle:\\n*Install NGT Apps\\n*Manage NGT Apps\\n*Uninstall NGT Apps\\n*Snapshot Create\\n*Snapshot Delete\\n*VM Restore\\n*App Update\\n*Clone"
      },
      {
         "bp_name":"MySQL",
         "mp_name":"MySQL",
         "icon_name":"MySQL",
         "app_source": "LOCAL",
         "bp_version":"1.0.0",
         "mp_description":"MySQL is an open source relational database management system (RDBMS) based on Structured Query Language (SQL). MySQL is an important component of LAMP stack based applications.\\n#### License:\\n* GPL Version 2.0\\n#### Hardware Requirement:\\n* Small_AHV Profile:\\n  * 1 VM at 4vCPUs and 6 GiB of Memory\\n* Large_AHV Profile:\\n  * 1 VM at 6vCPUs and 10 GiB of Memory\\n#### Resources Installed:\\n* Mysql-8.0\\n#### Operating System:\\n* CentOS Linux release 7.6.1810\\n#### Lifecycle:\\n* Backup\\n* Restore"
      },
      {
         "bp_name":"Wordpress",
         "mp_name":"Wordpress",
         "icon_name":"Wordpress",
         "app_source": "LOCAL",
         "bp_version":"1.0.0",
         "mp_description":"WordPress (WordPress.org) is a free and open-source content management system (CMS) based on PHP and MySQL. Features include a plugin architecture and a template system. It is most associated with blogging but supports other types of web content including more traditional mailing lists and forums, media galleries, and online stores.\\n#### License:\\n* General Public License v2.0\\n#### Hardware Requirement:\\n* Small_AHV Profile:\\n  * 1 MySQL VM at 2 vCPUs and 4 GiB of Memory\\n  * 1 Apache_PHP with Wordpress VM (can be scaled to 4) with 2 vCPUs and 2 GiB of Memory\\n  * 1 HaProxy VM with 2 vCPUs and 2 GiB of Memory\\n* Large_AHV Profile:\\n\\n  * 1 MySQL VM at 4 vCPUs and 6 GiB of Memory\\n  * 1 Apache_PHP with Wordpress VM (can be scaled to 6) with 4 vCPUs and 4 GiB of Memory\\n  * 1 HaProxy VM with 4 vCPUs and 4 GiB of Memory\\n#### Resources Installed:\\n* PHP\\n* MySQL\\n* Wordpress\\n* HAProxy\\n#### Operating System:\\n* CentOS Linux release 7.6.1810\\n#### Lifecycle:\\n* ScaleOut\\n* ScaleIn"
      },
      {
         "bp_name":"Redis",
         "mp_name":"Redis",
         "icon_name":"Redis",
         "app_source": "LOCAL",
         "bp_version":"1.0.0",
         "mp_description":"Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs and geospatial indexes with radius queries.\\nThis blueprint creates a Master-Slave cluster with one Master node and two slave nodes.\\n#### License:\\n* BSD License\\n#### Hardware Requirement:\\n* Small_AHV Profile:\\n  * 1 Master VM at 2vCPUs and 4 GiB of Memory\\n  * 1 Slave VM (can be scaled to 4) at 2 vCPUs and 2 GiB of Memory\\n* Large_AHV Profile:\\n  * 1 Master VM at 4vCPUs and 6 GiB of Memory\\n  * 2 Slave VM (can be scaled to 6) at 4vCPUs and 4 GiB of Memory\\n* Redis 3.2.10\\n#### Operating System:\\n* CentOS Linux release 7.6.1810\\n#### Lifecycle:\\n* ScaleOut\\n* ScaleIn\\n#### Other Instructions:\\n* Latest stable version of Redis will be installed."
      },
      {
         "bp_name":"Jenkins",
         "mp_name":"Jenkins",
         "icon_name":"Jenkins",
         "app_source": "LOCAL",
         "bp_version":"1.0.0",
         "mp_description":"Jenkins is an open source automation server written in Java. Jenkins helps to automate the non-human part of the software development process, with continuous integration and facilitating technical aspects of continuous delivery. It is a server-based system that runs in servlet containers such as Apache Tomcat.\\n#### License:\\n* MIT License\\n#### Hardware Requirement:\\n* Small_AHV Profile:\\n  * 1 Master VM at 2 vCPUs and 4 GiB of Memory\\n  * 1 Slave VM (can be scaled to 6) at 2 vCPUs and 4 GiB of Memory\\n* Large_AHV Profile:\\n  * 1 Master VM at 4 vCPUs and 6 GiB of Memory\\n  * 2 Slave VM (can be scaled to 6) at 4 vCPUs and 6 GiB of Memory\\n#### Resources Installed:\\n* Jenkins 2.190.3\\n* Java 1.8.0\\n#### Operating System:\\n* CentOS Linux release 7.6.1810\\n#### Lifecycle:\\n* Upgrade\\n* ScaleOut\\n* ScaleIn"
      }
   ]
}
