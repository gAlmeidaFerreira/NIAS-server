# NIAS-server

A schematic describing the server is illustrated below. 

![](images/Imagem-servidor.png)

## User Registry

First of all, to use this server the researcher must register it self in the server. To do so, one must ask for the server administrator to run the [user register](user-register.sh) file. this file works as follows:

  1. Informations of the new user must be provided, such as:
     - A user name, made as follows: firstname-lastname
     - The name of the user in the researcher's personal computer
     - The port that reponds to ssh in the researcher's personal computer
     - A passphrase for building the ssh key
     - the UFV-VPN IP address of the resercher's PC (This IP address must be fixed)
     
  2. With the above information, a new user will be created, he will be part of the docker group in addition to his own. the user home directory will use [skel-client](skel-client) to be build, this directory will contain the [job](job.sh) file (described later) and .ssh directory.
 
  3. Inside [ssh](skel-client/.ssh) directory, the researcher's PC will be registered as a ssh host, in order to be accessed later, during the [job](job.sh) routine

  4. To finish the registration, the server adminitrator must get in the newly created user and execute the commands to generate a new ssh key, using the passphrase provided, and send the public key to the researcher's PC  
