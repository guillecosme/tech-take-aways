import boto3
from moto import mock_aws

import pytest

from scripts.virtual.create_vpc_interface_endpoints.app import lambda_function


@mock_aws
def mock_assume_role():
    ''''''
    client = boto3.client('sts', region_name = 'us-eats-1')
    response = client.assume_role(
        RoleArn = 'arn:aws:iam::999999999999:role/AWSMockedROle',
        RoleSessionName = 'MockedSession'
    )

    session = boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'])
    
    return session

@mock_aws
def create_mocked_vpc():

    account_session =  mock_assume_role()
    ec2_client =  account_session.client('ec2', region_name = 'us-east-1')
    
    response = ec2_client.create_vpc(
        CidrBlock = '10.0.0.0/22'
    )

    vpc_id = response['Vpc']['VpcId']

    return vpc_id

@mock_aws 
def create_mocked_subnets(vpc_id):

    subnet_ids = []

    account_session =  mock_assume_role()
    ec2_client =  account_session.client('ec2', region_name = 'us-east-1')

    response = ec2_client.create_subnet(
        AvailabilityZone = 'us-east-1a',
        VpcId = vpc_id,
        CidrBlock = '10.0.0.0/24' )
    
    subnet_ids.append(response['Subnet']['SubnetId'])

    response = ec2_client.create_subnet(
    AvailabilityZone = 'us-east-1b',
    VpcId = vpc_id,
    CidrBlock = '10.0.1.0/24' )

    subnet_ids.append(response['Subnet']['SubnetId'])

    response = ec2_client.create_subnet(
    AvailabilityZone = 'us-east-1c',
    VpcId = vpc_id,
    CidrBlock = '10.0.2.0/24' )

    subnet_ids.append(response['Subnet']['SubnetId'])

    return subnet_ids

@mock_aws
def create_mocked_security_group(vpc_id):
    ''''''

    security_groups = []

    account_session =  mock_assume_role()
    ec2_client =  account_session.client('ec2', region_name = 'us-east-1')

    response = ec2_client.create_security_group(
        Description = 'MockedSG',
        GroupName = 'MockedSG',
        VpcId = vpc_id
    )
    
    security_groups.append(response['GroupId'])
    return security_groups

@mock_aws
def test_create_vpc_endpoints_sucessfull_scenario() -> None:    
    ''''''
    vpc_id = create_mocked_vpc()
    subnets = create_mocked_subnets(vpc_id)
    security_group_id = create_mocked_security_group(vpc_id)

    TEST_DATA = {
    'service_names': ['ec2.us-east-1.amazonaws.com'],
    'vpc_id': vpc_id,
    'security_groups_ids': security_group_id,
    'subnet_ids': subnets
    }   

    account_session = mock_assume_role()
    response = lambda_function.create_vpc_endpoints(account_session, TEST_DATA['service_names'],
                                    TEST_DATA['vpc_id'],
                                    TEST_DATA['security_groups_ids'],
                                    TEST_DATA['subnet_ids'])
    
    assert response['status'] ==  'success'


@mock_aws
def test_create_vpc_endpoints_non_existing_vpc_scenario() -> None:    
    ''''''

    TEST_DATA = {
    'service_names': ['ec2.us-east-1.amazonaws.com'],
    'vpc_id': 'vpc-99999999999999',
    'security_groups_ids': ['sg-9999999'],
    'subnet_ids': ['subnet-12123']
    }   

    account_session = mock_assume_role()
    response = lambda_function.create_vpc_endpoints(account_session, TEST_DATA['service_names'],
                                    TEST_DATA['vpc_id'],
                                    TEST_DATA['security_groups_ids'],
                                    TEST_DATA['subnet_ids'])

    assert response['status'] ==  'error'