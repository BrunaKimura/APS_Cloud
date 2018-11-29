import boto3

client = boto3.client('ec2')

key_name = 'apsbru'

with open ('/home/bruna/.ssh/id_rsa.pub', 'r') as file:
    keyp = file.read()
    
try:
    describe = client.describe_key_pairs(
        KeyNames=[
            key_name,
        ],
        DryRun=False
    )

    delete = client.delete_key_pair(
    KeyName=key_name,
    DryRun=False
    )

    print("chave deletada")

    response = client.import_key_pair(
        DryRun=False,
        KeyName=key_name,
        PublicKeyMaterial=keyp
  
    )
    print("chave criada")


except:
    create = client.create_key_pair(
        KeyName=key_name,
        DryRun=False
    )

    print("chave criada")

