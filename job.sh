#! /bin/bash

echo "Digite o nome do usuário do usuário"
read user
while ! [ -e /home/$user ]
do
	echo "Usuário não existe, digite novamente ou digite 'out' para sair e solicite a criação de um novo usuário "
	read user

	if [ $user = out ]
	then
		exit
	fi
done

echo "Digite o nome do projeto"
read projeto
echo "Digite o caminho completo para a pasta de origem do projeto"
read path
echo "Digite python ou p para projetos em python, matlab ou m para projetos em matlab"
read tipo

while [ $tipo != python ] && [ $tipo != p ] && [ $tipo != matlab ] && [ $tipo != m ]
	# TODO: Procurar fzf(https://github.com/junegunn/fzf#installation)
do
	echo "Tipo inválido, digite novamente (python ou p para projetos em python, matlab ou m para projetos em matlab)"
	read tipo
done

docker_build_run () {
	
	docker build -t $projeto:latest /home/$user/$projeto/
	docker run --rm -it \
		-v /home/$user/$projeto/project/output:/output \
		$projeto:latest
	}

mkdir /home/$user/$projeto
scp -r $user:$path /home/$user/$projeto

case $tipo in
	python | p)
		cp /home/templates/dockerfile-python /home/$user/$projeto/Dockerfile
		;;

	matlab | m)
		cp /home/templates/dockerfile-matlab /home/$user/$projeto/Dockerfile
		;;

	esac
# TODO: Fazer script para scp 
docker_build_run
