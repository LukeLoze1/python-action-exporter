import datetime
import logging
import pika
import xmltodict as xmltodict
from structlog import wrap_logger

from config import Config
from sftp_utility import SftpUtility

logger = wrap_logger(logging.getLogger(__name__))
 

def create_file_name():
    return datetime.datetime.now().strftime("%Y%m%d%H%M") + ".csv"


def callback(ch, method, properties, body):
    csv_line = msg_body_to_csv(body)

    filename = create_file_name()

    with SftpUtility() as sftp_utility:
        sftp_utility.write_file_to_sftp(filename, csv_line)




def main():
    channel = init_rabbitmq()

    channel.basic_consume(callback,
                          queue=Config.RABBIT_QUEUE,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def init_rabbitmq(rabbitmq_amqp=Config.RABBIT_AMQP,
                  binding_key=Config.RABBIT_ROUTE,
                  exchange_name=Config.RABBIT_EXCHANGE,
                  queue_name=Config.RABBIT_QUEUE,
                  queue_args=Config.RABBIT_QUEUE_ARGS):

    logger.debug('Connecting to rabbitmq', url=rabbitmq_amqp)
    rabbitmq_connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_amqp))
    channel = rabbitmq_connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue_name, durable=True, arguments=queue_args)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)
    logger.info('Successfully initialised rabbitmq', exchange=exchange_name, binding=binding_key)

    return channel


def msg_body_to_csv(body):
    # should be template
    action_request = msg_to_dict(body)
    address = action_request['address']

    csv_line =  (
        f'{action_request["iac"]}|'
        f'ARID_NOT_IN_MSG|'
        f'{address["line1"]}|'
        f'{address["line2"]}|'
        f'Line3 missing|'
        f'{address["townName"]}|'
        f'{address["postcode"]}|'
        f'pack_code_place_holder\n'
    )

    return csv_line


def msg_to_dict(body):
    xml_str = body.decode('utf-8')
    xml_action = xmltodict.parse(xml_str)
    action_instruction = xml_action['ns2:actionInstruction']
    action_request = action_instruction['actionRequest']

    return action_request


if __name__ == '__main__':
    main()
