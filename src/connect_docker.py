import docker

docker_client = docker.from_env()

def make_docker_image(name):
    print("Dockerfileからimage生成")
    docker_client.images.build(
            path="./",
            tag= name
        )
    return


def run_docker_container(name,cpu_size,memory_size):
    print("docker起動")
    docker = docker_client.containers.run(name,mem_limit= memory_size, cpu_period= cpu_size,detach=True,network_mode= "bridge")
    print("docker起動完了")
    docker_id = docker.id
    return docker_id

def set_docker_network(docker_id,ipAddress,name):
    print("dockerのネットワークを作成")
    dockerNetWork = docker_client.networks.create(name,driver="bridge")
    print("コンテナを作成したネットワークに繋げてIP Addressを付与")
    dockerNetWork.connect(container = docker_id,ipv4_address=ipAddress)
       
    return 

def stop_docker_container(docker_id):
    print("dockerコンテナを取得") 
    docker_stop = docker_client.containers.get(docker_id)
    print("dockerを停止ししにいく")
    docker_stop.stop()

    return 

def delete_docker(name,docker_stop):
    print("コンテナ・imageの削除")
    docker_stop.remove()
    docker_client.images.remove(image = name)

    return 