import time

import click
import boto3 as boto3
from botocore.config import Config
from rich.progress import track
from rich import print
from rich.console import Console

csse6400_config = Config(
    region_name='us-east-1'
)


@click.command()
@click.option('--name', required=True, help="Name of the Queue to connect to")
@click.option('--client-name', required=True, help="Name of this client")
@click.option('--send/--receive', default=True, help="Whether this application should be sending")
@click.option('--prepend', default='', help="Prepends to the front of a message")
def cmd(name: str, client_name: str, send: bool, prepend: str):
    print('''
    [bold purple]
      __________
     |   \XX/   |
     | T. \/ .T |      [bold white]University of Queensland[/bold white]
     | XX:  :XX |          [bold white]Faculty of EAIT[/bold white]
     T L' /\ 'J T
      \  /XX\  /         [bold white]CSSE6400 Queue Prac[/bold white]
    @\_ '____' _/@       [bold white]csse6400.uqcloud.net[/bold white]
    \_X\_ __ _/X_/       
     \=/\----/\=/  
    [/bold purple]
    
    ''')

    sqs = boto3.resource('sqs', config=csse6400_config)
    try:
        queue = sqs.get_queue_by_name(QueueName=name)
    except:
        print(f'Unable to find a Queue by this name {name}')
        return

    print(f'Connected to {name}')

    if send:
        print('Sending Messages:')
        for id in track(range(100)):
            if name.endswith('.fifo'):
                queue.send_message(MessageBody=f'{prepend}Message {id}',
                                   MessageAttributes={'client': {'StringValue': client_name, 'DataType': 'String'}},
                                   MessageGroupId="default")
            else:
                queue.send_message(MessageBody=f'{prepend}Message {id}',
                                   MessageAttributes={'client': {'StringValue': client_name, 'DataType': 'String'}})
    else:
        console = Console()

        with console.status("[bold green]Waiting for messages...") as status:
            while True:
                for message in queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=1,
                                                      MessageAttributeNames=['client']):
                    client = message.message_attributes.get('client').get('StringValue')
                    console.log(f'{client}: {message.body}')
                    message.delete()


if __name__ == '__main__':
    cmd()
