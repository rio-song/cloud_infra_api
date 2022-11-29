import paramiko
import connect_docker 

def connect_ssh():
    with paramiko.SSHClient() as client:

        HOSTNAME = '127.0.0.2'
        USERNAME = 'riosong2'
        PASSWORD = '*pwd*'

        # SSH接続
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # パスワード認証認証方式
        client.connect(hostname=HOSTNAME, port=22, username=USERNAME, password=PASSWORD)
   
    return client

def connect_utm2_make_docker_image(name):

    client = connect_ssh()
    client.exec_command(connect_docker.make_docker_image(name))
    client.close()
       
    return

def connect_utm2_make_docker_image(name):

    client = connect_ssh()
    client.exec_command(connect_docker.make_docker_image(name))
    client.close()
       
    return

def connect_utm2_run_docker_container(name,cpu_size,memory_size):

    client = connect_ssh()
    docker_id = client.exec_command(connect_docker.run_docker_container(name,cpu_size,memory_size))
    client.close()
       
    return docker_id

def connect_utm2_set_docker_network(docker_id,ipAddress,name):

    client = connect_ssh()
    client.exec_command(connect_docker.set_docker_network(docker_id,ipAddress,name))
    client.close()
       
    return

def connect_utm2_stop_docker_container(docker_id):

    client = connect_ssh()
    client.exec_command(connect_docker.stop_docker_container(docker_id))
    client.close()
       
    return

def connect_utm2_delete_docker(name,docker_stop):

    client = connect_ssh()
    client.exec_command(connect_docker.stop_docker_container(name,docker_stop))
    client.close()
       
    return

def connect_utm2_connect_container_by_ssh(id_rsa):

    client = connect_ssh()
    client.exec_command("ssh root@localhost -i " + id_rsa, get_pty=True)
    client.close()
       
    return




    