import boto3


ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


instance_iterator = client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Owner',
            'Values': [
                'Bruna'
            ],
        },
        {
            'Name': 'instance-state-name',
                'Values':[
                    'running',
                    'pending'
                ]
        },
    ]
)

instacias = instance_iterator['Reservations']
if len(instacias) !=0:
    for i in instacias:
        for e in i['Instances']:
            id_instacia = str(e['InstanceId'])

            deleta_instancia = client.terminate_instances(
                InstanceIds=[
                    id_instacia,
                ]
            )
            print('Maquina {0} deletada'.format(id_instacia))

    print('Maquinas deletadas')

else:
    print('Nao ha maquinas ativas')
    
while len(instacias) !=0:
    instance_iterator = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'Bruna',
                ],
            },
            {
                'Name': 'instance-state-name',
                    'Values':[
                        'running',
                        'shutting-down'
                    ]
            },
        ]
    )
    instacias = instance_iterator['Reservations']
    
# import keypair as kp
# import security as sg

nome = "APS2"
describe = client.describe_security_groups(
    Filters=[
        {
            'Name': 'group-name',
            'Values': [
                nome,
            ]
        },
    ]
)

idsg = str(describe['SecurityGroups'][0]['GroupId'])

ip_db = client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Owner',
            'Values': [
                'Banco'
            ],
        },
        {
            'Name': 'instance-state-name',
                'Values':[
                    'running',
                    'pending'
                ]
        },
    ]
)

instance = ec2.create_instances(
    ImageId='ami-0ac019f4fcb7cb7e6',
    InstanceType='t2.micro',
    KeyName='apsbru',
    MaxCount=3,
    MinCount=3,
    SecurityGroupIds=[
        idsg
    ],
    SecurityGroups=[
        nome
    ],
    UserData='''#!/bin/bash
                cd /home/ubuntu
                git clone https://github.com/BrunaKimura/APS_Cloud.git
                cd APS_Cloud
                export DB_HOST={0}
                chmod a+x install1.sh 
                ./install1.sh'''.format(ip_db),
    TagSpecifications=[
        {
            'ResourceType':'instance',
            'Tags': [
                {
                    'Key': 'Owner',
                    'Value': 'Bruna'
                },
            ]
        },
    ]
)

print('Maquinas criadas com sucesso!')