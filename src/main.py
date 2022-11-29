import data.repository as repository
import ssh.ssh_connect as ssh_connect
import ssh.connect_another_utm as connect_another_utm
import connect_docker 

def start_instance(name, cpu_size, memory_size):

    #dbのステータスをstarting変更しにいく。
    print("dbのステータスをstarting変更しにいく")
    regiser_starting = repository.add_instanse_status_starting(name)

    #DBの空き容量を確認する。
    #UTM1の合計メモリの取得
    utm = 1
    result = 'result'
    print("UTM1の合計メモリの取得")
    utm1_memory_size = repository.count_utm_memory_size(utm)
 
#utmの残りのメモリが2477mだったため、再上限を2470mに設定。
    if utm1_memory_size > 2470:
        #UTM2の合計メモリの取得
        utm = 2
        utm2_memory_size = repository.count_utm_memory_size(utm)

        #utmの残りのメモリが3422mだったため、再上限を3400mに設定。
        if utm2_memory_size > 3400:
            result = 'not_empty_error'
            return result
        return 
  
    private_key = ssh_connect.make_key()

    userId = regiser_starting[0]
    instanseId = regiser_starting[1]

    print("鍵をDBに登録")
    repository.register_private_key(userId, private_key)
    if utm == 1 : 
        connect_docker.make_docker_image(name)
    elif utm == 2 :
        connect_another_utm.connect_utm2_make_docker_image(name)
        return

    print("dbのステータスをintializingに変更しにいく")
    repository.add_instanse_status_intializing(instanseId)

    if utm == 1 :
        docker_id = connect_docker.run_docker_container(name,cpu_size,memory_size)
    elif utm == 2 :
        docker_id = connect_another_utm.connect_utm2_run_docker_container(name,cpu_size,memory_size)
        return docker_id

    print("DBへdocker情報を書き込みにいく。")    
    memory = memory_size.replace('m', '')
    repository.register_instance_info(instanseId,docker_id,memory,cpu_size,utm)
    
    print("dbのステータスをrunningに変更しにいく。")
    repository.add_instanse_status_running(instanseId)

    print("ネットワークの設定をする。")
    print("DBから未使用のIP Addressの取得")
    ipAddress = repository.getIpAddress()
    if ipAddress == None:
        result = 'not_found_unused_ipaddress'
        return result

    if utm == 1 :
        connect_docker.set_docker_network(docker_id,ipAddress,name)
    elif utm == 2 :
        connect_another_utm.connect_utm2_set_docker_network(docker_id,ipAddress,name)
        return

    print("IP Addressを使用ずみに変更")
    repository.chengeIpAddressUsed(ipAddress.id)

    return  result, userId, instanseId

def stop_instance(instanceId, userId):

    print("DBにdocker情報を取得しにいく")
    info = repository.instance_info(instanceId, userId)
    docker_id = info[5]
    utm = info[2]
    name = info[0]

    if utm == 1:
        docker_stop = connect_docker.stop_docker_container(docker_id)    
    elif utm == 2 :
        docker_stop = connect_another_utm.connect_utm2_stop_docker_container(docker_id)
        return docker_stop

    print("dbのステータスをstoppingに変更しにいく。")
    repository.update_instanse_status_stopping(instanceId)

    if utm == 1:
        connect_docker.delete_docker(name,docker_stop)    
    elif utm == 2 :
        connect_another_utm.connect_utm2_delete_docker(name,docker_stop)
        return 

    print(" DB情報の削除")
    repository.delete_all(userId,instanceId)
    
    return

def login_instance(instanceId, userId, command):

    print("DBにdocker情報を取得しにいく")
    info = repository.instance_info(instanceId, userId)
    utm = info[2]

    #プレゼン発表時のdockerを使用した接続方法↓
        # print('dockerコンテナの取得')
        # docker_login = docker_client.containers.get(info[5])

        # print('コマンドの実施')
        # result = docker_login.exec_run(cmd = command)
        # # aaa = docker_login.exec_run(cmd = 'cat /etc/issue')

    #python SDKを使用せずにssh接続でログインに変更↓
    print("private鍵情報の取得")
    id_rsa = repository.getUserInfo(userId)

    if utm == 1:
        ssh_connect.connect_container_by_ssh(id_rsa)
    elif utm == 2:
        connect_another_utm.connect_utm2_connect_container_by_ssh(id_rsa)
        return

    return