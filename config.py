import os


class Config:
    RABBIT_AMQP = os.getenv("RABBIT_AMQP", "amqp://guest:guest@localhost:6672/")
    RABBIT_EXCHANGE = os.getenv("RABBIT_EXCHANGE", "action-outbound-exchange")
    RABBIT_QUEUE = os.getenv("RABBIT_QUEUE", "Action.Printer")
    RABBIT_ROUTE = os.getenv("RABBIT_ROUTING_KEY", "Action.Printer.binding")
    RABBIT_QUEUE_ARGS = {'x-dead-letter-exchange': 'action-deadletter-exchange',
                         'x-dead-letter-routing-key': RABBIT_ROUTE}

    SFTP_HOST = os.getenv('SFTP_HOST', 'localhost')
    SFTP_PORT = os.getenv('SFTP_PORT', '122')
    SFTP_USERNAME = os.getenv('SFTP_USERNAME', 'centos')
    SFTP_PASSWORD = os.getenv('SFTP_PASSWORD', 'JLibV2&XD,')
    SFTP_DIR = os.getenv('SFTP_DIR', 'Documents/sftp')
