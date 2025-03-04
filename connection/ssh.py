import paramiko


def ssh_connection(host, user='', password='', port=22, private_key=None):
    print(f'Connecting to {host} on port {port}')
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if private_key:
            pkey = paramiko.RSAKey.from_private_key_file(private_key)
        else:
            pkey = None
        client.connect(hostname=host, username=user, password=password, port=port, pkey=pkey)
        return client
    except Exception as e:
        print(f"Error: {e}")
        return None
