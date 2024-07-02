import json
import botocore.session
import boto3
import botocore


def create_vpc_endpoints(account_session, service_names: list[str],vpc_id:str, security_groups_ids:list[str], subnet_ids:list[str]) -> None:
    ''' Creates VPC Interface endpoints.'''

    vpc_client = account_session.client('ec2',region_name = 'us-east-1')

    result = None

    for service_name in service_names:

        try:
            response = vpc_client.create_vpc_endpoint(
                VpcEndpointType = 'Interface',
                VpcId = vpc_id,
                ServiceName = service_name,
                SecurityGroupIds = security_groups_ids,
                SubnetIds =  subnet_ids
            )

            result =  {'endpoint_id': response['VpcEndpoint']['VpcEndpointId'],
                       'service_name': response['VpcEndpoint']['ServiceName'],
                       'status': 'success'
            }

            return result

        except Exception as exception:

            exception = str(exception)
            print(f'Error on create_vpc_endpoints. {exception}')

            result =  {'endpoint_id': None,
                       'service_name': None,
                       'status': 'error'
            }

            return result


def lambda_handler(event, context) -> json:
    ''' Lambda handler. Process the vpc interface endpoint creation.'''

    create_vpc_endpoints('ec2.us-east-1.amazonaws.com','vpc-123')

    return {
        'statuCode': 200,
        'body': json.dumps('Success')
    }