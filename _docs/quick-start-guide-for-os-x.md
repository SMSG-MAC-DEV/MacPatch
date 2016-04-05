---
layout: default
title: "Quick Start Guide for OS X"
---


This is a quick start guide to getting MacPatch installed and running on a Mac OS X based system. For the purpose of this guide we will be installing on a Mac OS X 10.9.x system.

## Required Software
There are two prerequisites to installing the MacPatch server software. Java and Xcode command line tools need to be installed.

### Java
Java can be downloaded from Oracle at [http://www.oracle.com/technetwork/java/javase/downloads/index.html](http://www.oracle.com/technetwork/java/javase/downloads/index.html). Java 8 (JDK) is required.

### Xcode
Xcode is required to build the MacPatch software for Mac OS X. While you can install the GUI version of Xcode and download and install the command line tools from within Xcode. You will be installing the Xcode command line tools from the Terminal.app.

Test for Xcode

	% xcode-select --version

If you get back a version they are installed .

Install Xcode

	% xcode-select --install

### PIP (Python Modules)

	sudo easy_install pip  # if you don't already have pip
	sudo pip install requests
	sudo pip install argparse
	sudo pip install --allow-external mysql-connector-python mysql-connector-python
    
## Download and build the Server software
To download and build the MacPatch server software is just a few Terminal commands. Run the following commands to build and install the software.

Please note, you will be asked if you want to use the Jetty J2EE server. With MacPatch 2.5 Tomcat is now the default J2EE server. The Jetty distribution is old and may have security vulnerabilities. It is scheduled to be removed in the next release.

	sudo mkdir -p /Library/MacPatch/tmp
	cd /Library/MacPatch/tmp
	sudo git clone https://github.com/SMSG-MAC-DEV/MacPatch.git
	sudo /Library/MacPatch/tmp/MacPatch/scripts/MPBuildServer.sh
    
Once the compile and copy process is completed, the MacPatch server software is now installed and ready to be configured.

## MySQL Database
MacPatch requires the use of MySQL database. The database can be installed on the first server built or it can be installed on a separate host. MySQL version 5.5.x or higher is required. MySQL 5.6.x is recommended due to it's performance enhancements. Also, the MySQL InnoDB engine is required.

### Configure MySQL Database
Run the following commands via the Terminal.app.

#### Log in as the MySQL root user

	mysql -u root -p
    
#### Run the following MySQL commands
*Replace the word "Password" with your own password.*

	mysql> CREATE DATABASE MacPatchDB;
	mysql> CREATE USER 'mpdbadm'@'%' IDENTIFIED BY 'Password';
	mysql> GRANT ALL ON MacPatchDB.* TO 'mpdbadm'@'%' IDENTIFIED BY 'Password';
	mysql> GRANT ALL PRIVILEGES ON MacPatchDB.* TO 'mpdbadm'@'localhost' IDENTIFIED BY 'Password';
	mysql> CREATE USER 'mpdbro'@'%' IDENTIFIED BY 'Password';
	mysql> GRANT SELECT ON MacPatchDB.* TO 'mpdbro'@'%';
	mysql> SET GLOBAL log_bin_trust_function_creators = 1;
	mysql> FLUSH PRIVILEGES;
    
#### Delete MySQL anonymous accounts

	mysql> DROP USER ''@'localhost';
	mysql> DROP USER ''@'host_name';
	mysql> quit
    
#### Load Database Schema
The database schema files are located on the MacPatch server in the `/Library/MacPatch/Server/conf/Database/` directory. To load the tables and the views, copy the `MacPatchDB_Tables.sql` and `MacPatchDB_Views.sql` files to the Database host. The following commands are for a server that is also hosting the MacPatch database.

	% mysql MacPatchDB -u mpdbadm -p < /Library/MacPatch/Server/conf/Database/MacPatchDB_Tables.sql
	% mysql MacPatchDB -u mpdbadm -p < /Library/MacPatch/Server/conf/Database/MacPatchDB_Views.sql
    
## Setup MacPatch Server
The MacPatch server has five configuration script and should be run in the given order. The scripts are located on the server in `/Library/MacPatch/Server/conf/scripts/Setup/`.

Script	| Description | Server/Is Required
---|---|---
DataBaseLDAPSetup.py | The database setup is required for MacPatch to function. | Master/Required
WebAdminSetup.sh | The MacPatch admin web console is required to use MacPatch. This section is an option for those who wish to setup additional servers for large environments. | Master/Required
WebServicesSetup.sh | The MacPatch web services are required to use MacPatch. | Master, Distribution/Required
PatchLoaderSetup.py| MacPatch requires gathering all of Apple Software updates from an Apple Software Update server, so that Apple patches can be assigned to a patch group for patching. | Master, Distribution/Recommended
SymantecAntivirusSetup.py | MacPatch supports patching Symantec Antivirus definitions. Not all sites use SAV/SEP so this step is optional. | Master/Optional
StartServices.py | Depending on your choices this script will start all MacPatch services. Script has multiple arguments. <ul><li>Start All Services: StartServices.py --load All</li><li>Stop All Services - StartServices.py --unload All</li></lu> | Master, Distribution

### Download Content
#### Apple Updates
Apple patch content will download eventually on it's own cycle, but for the first time it's recommended to download it manually.

Run the following command via the Terminal.app on the Master MacPatch server.

	sudo -u _appserver /Library/MacPatch/Server/conf/scripts/MPSUSPatchSync.py --plist /Library/MacPatch/Server/conf/etc/gov.llnl.mp.patchloader.plist
    
#### Symantec AntiVirus Defs
If you have elected to deploy Symantec AntiVirus definitions via MacPatch then it's also recommended that you download the content manually for the first time.

	sudo -u _appserver /Library/MacPatch/Server/conf/scripts/MPAVDefsSync.py --plist /Library/MacPatch/Server/conf/etc/gov.llnl.mpavdl.plist
    
## Configure MacPatch - Admin Console
Now that the MacPatch server is up and running, you will need to configure the environment.

### First Login
The default user name is "mpadmin" and the password is "\*mpadmin\*". You will need to login for the first time with this account to do all of the setup tasks. Once these tasks are completed it's recommended that this accounts password be changed. This can be done by editing the siteconfig.xml file, which is located in /Library/MacPatch/Server/conf/etc/.

### Default Configuration
#### MacPatch Server Info
Each MacPatch server need to be added to the environment. By default we will be adding the first server, the Master to the list.

* Go to "Admin-> Server -> MacPatch Servers"
* Click the "Plus" button to add a new server

Example data for Master server:

* Server: server1.macpatch.com
* Port: 2600
* Use SSL: Yes
* Use SSL Auth: NO (Not Supported Yet)
* Is Master: Yes
* Is Proxy: No
* Active: Yes

#### Agent Configuration
Before you can upload the Agent software an client agent configuration need to be created.

* Go to "Admin -> Client Agents -> Configure"
* Click the "Create New Agent Config" button
* Name the first configuration "Default"
* Set the following 3 properties to be enforced
	* MPServerAddress
	* MPServerPort
	* MPServerSSL
* Click the save button
* Click the icon in the "Default" column for the default configuration. (Important Step)

Create Default Patch Group

* Go to "Patches -> Patch Groups"
* Click the "Plus" button to add a new group
* Set the following 2 properties
	* Patch Group: "RecommendedPatches"
	* Type: Production

To edit the contents for the patch group simply click the "Pencil" icon next to the group name. To add patches click the check boxes to add or subtract patches from the group. When done click the "Save" icon. (Important Step)

**Please note:** Only production patches will be visible to a production group.

#### Upload the Client Agent
To upload a client agent you will need to build the client first. Please follow the Building the Client document before continuing.

* Go to "Admin-> Client Agents -> Deploy"
* Download the "MacPatch Agent Uploader"
* Double Click the "Agent Uploader.app"
	* Enter the MacPatch Server
	* Choose the agent package (e.g. MPClientInstall.pkg.zip)
	* Click "Upload" button