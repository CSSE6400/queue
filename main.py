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
def cmd(name: str, client_name: str, send: bool):
    print(f'Hello, [bold magenta]World[/bold magenta]')

    sqs = boto3.resource('sqs', config=csse6400_config)
    queue = sqs.get_queue_by_name(QueueName=name)
    print(f'Connected to the following Queue')

    if send:
        for id in track(range(100)):
            if name.endswith('.fifo'):
                queue.send_message(MessageBody=f'Message {id}', MessageAttributes={'client': {'StringValue': client_name, 'DataType': 'String'}}, MessageGroupId="default")
            else:
                queue.send_message(MessageBody=f'Message {id}', MessageAttributes={'client': {'StringValue': client_name, 'DataType': 'String'}})
    else:
        console = Console()

        with console.status("[bold green]Waiting for messages...") as status:
            while True:
                for message in queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=1, MessageAttributeNames=['client']):
                    client = message.message_attributes.get('client').get('StringValue')
                    console.log(f'{client}: {message.body}')
                    message.delete()


if __name__ == '__main__':
    cmd()
