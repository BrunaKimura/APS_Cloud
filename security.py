import boto3

client = boto3.client('ec2')

nome = 'APS2'

try:
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
    print("id do Security Gruop: ", idsg)

    deleta = client.delete_security_group(
        GroupId= idsg,
        GroupName = nome
    )

    print("Security Group Deletado")

    cria_sg = client.create_security_group(
        Description='security gruop para APS3 de bruna',
        GroupName='APS2'
    )

    print("Security Group Criado")


except:
    cria_sg = client.create_security_group(
        Description='security gruop para APS3 de bruna',
        GroupName='APS2'
    )

    print("Security Group Criado")

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
print("id do Security Gruop: ", idsg)

autoriza = client.authorize_security_group_ingress(
    GroupId=idsg,
    IpPermissions=[
        {
            'FromPort': 22,
            'IpProtocol': 'tcp',
            'ToPort':22,
            'IpRanges': [
                {
                    'CidrIp':'0.0.0.0/0',
                    'Description': 'Test'
                },
            ]
        },
        {
            'FromPort': 5000,
                'IpProtocol': 'tcp',
                'ToPort':5000,
                'IpRanges': [
                    {
                        'CidrIp':'0.0.0.0/0',
                        'Description': 'Test'
                    },
                ]   
        }
    ]
)

print("autorização das portas 22 e 5000")