import paramiko as paramiko

from config import Config

class SftpUtility:
    def __init__(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=Config.SFTP_HOST,
                                port=int(Config.SFTP_PORT),
                                username=Config.SFTP_USERNAME,
                                password=Config.SFTP_PASSWORD,
                                look_for_keys=False,
                                timeout=120)

    def __enter__(self):
        self._sftp_client = self.ssh_client.open_sftp()
        return self

    def __exit__(self, *_):
        self._sftp_client.close()
        self.ssh_client.close()

    def write_file_to_sftp(self, file_name, data):
        file_path = Config.SFTP_DIR + '/' + file_name
        file = self._sftp_client.open(file_path, "a", -1)
        file.write(data)
        file.flush()
