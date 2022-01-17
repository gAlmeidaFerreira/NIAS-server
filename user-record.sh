#! /bin/bash

# Recebendo informações para criação do usuário
echo "Digite o nome de usuário (primeironome-ultimonome)"
read user
echo "Digite o nome de usuário no computador pessoal do pesquisador "
read userclient
echo "Digite a porta destinada ao ssh no computador pessoal do pesquisador (aperte enter se sua porta for a padrão)"
read userport
if [ -z $userport ];then
	$userport = 22
fi

echo "Digite uma passphrase para a geração da chave ssh"
read passph

# Criando usuário
echo "Adicione uma senha para seu usuário no servidor"
useradd -m -k /etc/skel-client -G docker $user
passwd $user

# Recebendo ip do usuário
echo "Digite o ip correspondente à VPN da UFV da máquina do usuário"
read userip 

# Registrando computador do usuário como ssh host
echo "Host $user 
     HostName $userip
     User $userclient
     Port $userport" > /home/$user/.ssh/config

echo "Após registro do usuário devem ser executados os seguintes comandos para registro e envio de uma nova chave ssh"
echo "ssh-keygen -t rsa -N $passph -f /home/$user/.ssh/id_rsa"
echo "ssh-copy-id -p $userport $userclient@$userip"
su $user
