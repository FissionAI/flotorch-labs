"""
AWS IAM Role & OpenSearch Policy Management for Advanced RAG

This script automates the creation of IAM roles, policies, and OpenSearch Serverless configurations
required for an Advanced Retrieval-Augmented Generation (RAG) setup using Amazon Bedrock & Amazon SageMaker.

Key functionalities:
1. **IAM Role Creation**:
   - Creates an Amazon Bedrock execution role with permissions to:
     - Invoke Bedrock foundation models
     - Access S3 for data storage and retrieval
     - Invoke a custom chunking Lambda function

2. **IAM Policy Management**:
   - Defines and attaches policies for:
     - Bedrock foundation models (`bedrock:InvokeModel`)
     - S3 storage (`s3:GetObject`, `s3:PutObject`, etc.)
     - Lambda invocation (`lambda:InvokeFunction`)
     - OpenSearch Serverless API access (`aoss:APIAccessAll`)

3. **OpenSearch Serverless Policies**:
   - Creates security, network, and data access policies for OpenSearch Serverless.
   - Enables encryption, public access settings, and fine-grained permissions.

This script is designed for use in an AWS environment with proper permissions.
"""

import boto3
import json
import urllib.parse
from sagemaker import get_execution_role

# Initialize AWS clients
s3 = boto3.client("s3")
iam = boto3.client("iam")
aoss = boto3.client("opensearchserverless")

# Retrieve AWS credentials and session
credentials = boto3.Session().get_credentials()
boto3_session = boto3.session.Session()


class AdvancedRagIamRoles:
    def __init__(self, account_number, region_name):
        self.account_number = account_number
        self.region_name = region_name

    # Function to create Amazon Bedrock Execution Role
    def create_bedrock_execution_role(self, bucket_name):
        """Creates an Amazon Bedrock execution role with permissions for Bedrock, S3, and Lambda."""

        # Define Bedrock foundation model policy
        foundation_model_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["bedrock:InvokeModel"],
                    "Resource": [f"arn:aws:bedrock:{self.region_name}::foundation-model/*"]
                }
            ]
        }

        # Define S3 policy with access restrictions
        s3_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
                    "Resource": [
                        f'arn:aws:s3:::{bucket_name}',
                        f'arn:aws:s3:::{bucket_name}/*',
                        f'arn:aws:s3:::{bucket_name}-custom-chunk',
                        f'arn:aws:s3:::{bucket_name}-custom-chunk/*'
                    ],
                    "Condition": {
                        "StringEquals": {"aws:ResourceAccount": self.account_number}
                    }
                }
            ]
        }

        # Define Lambda policy for invoking a custom chunking function
        lambda_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["lambda:InvokeFunction"],
                    "Resource": [
                        f'arn:aws:lambda:{self.region_name}:{self.account_number}:function:advanced-rag-custom-chunk:*'
                    ],
                    "Condition": {
                        "StringEquals": {"aws:ResourceAccount": self.account_number}
                    }
                }
            ]
        }

        # Define trust policy for Bedrock execution role
        assume_role_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "bedrock.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        # Create policies
        fm_policy = iam.create_policy(
            PolicyName=f"advanced-rag-fm-policy-{self.region_name}",
            PolicyDocument=json.dumps(foundation_model_policy_document),
            Description="Policy for accessing foundation models",
        )

        s3_policy = iam.create_policy(
            PolicyName=f"advanced-rag-s3-policy-{self.region_name}",
            PolicyDocument=json.dumps(s3_policy_document),
            Description="Policy for accessing S3 storage"
        )

        lambda_policy = iam.create_policy(
            PolicyName=f"advanced-rag-lambda-policy-{self.region_name}",
            PolicyDocument=json.dumps(lambda_policy_document),
            Description="Policy for invoking Lambda functions"
        )

        # Create Bedrock execution role
        bedrock_kb_execution_role = iam.create_role(
            RoleName=f"advanced-rag-workshop-bedrock_execution_role-{self.region_name}",
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
            Description="Amazon Bedrock Knowledge Base Execution Role",
            MaxSessionDuration=3600
        )

        # Attach policies to the Bedrock execution role
        iam.attach_role_policy(RoleName=bedrock_kb_execution_role["Role"]["RoleName"], PolicyArn=fm_policy["Policy"]["Arn"])
        iam.attach_role_policy(RoleName=bedrock_kb_execution_role["Role"]["RoleName"], PolicyArn=s3_policy["Policy"]["Arn"])
        iam.attach_role_policy(RoleName=bedrock_kb_execution_role["Role"]["RoleName"], PolicyArn=lambda_policy["Policy"]["Arn"])

        return bedrock_kb_execution_role

    # Function to add OpenSearch Vector Collection access to Bedrock Execution Role
    def create_oss_policy_attach_bedrock_execution_role(self, collection_id, bedrock_kb_execution_role):
        """Creates and attaches an OpenSearch Serverless (OSS) policy to the Bedrock execution role."""
        
        oss_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["aoss:APIAccessAll"],
                    "Resource": [
                        f"arn:aws:aoss:{self.region_name}:{self.account_number}:collection/{collection_id}"
                    ]
                }
            ]
        }

        oss_policy = iam.create_policy(
            PolicyName=f"advanced-rag-oss-policy-{self.region_name}",
            PolicyDocument=json.dumps(oss_policy_document),
            Description="Policy for accessing OpenSearch Serverless",
        )

        # Attach the policy to the Bedrock execution role
        iam.attach_role_policy(
            RoleName=bedrock_kb_execution_role["Role"]["RoleName"],
            PolicyArn=oss_policy["Policy"]["Arn"]
        )

        return None

    # Function to create OpenSearch Serverless security, network, and data access policies
    def create_policies_in_oss(self, vector_store_name, aoss_client, bedrock_kb_execution_role_arn):
        try:
            try:
                # Check if the encryption policy exists
                encryption_policy = aoss_client.create_security_policy(
                    name="advanced-rag-enc-policy2",
                    policy=json.dumps(
                        {
                            'Rules': [{'Resource': ['collection/' + vector_store_name],
                                       'ResourceType': 'collection'}],
                            'AWSOwnedKey': True
                        }),
                    type='encryption'
                )
            except Exception as e:
                print(f"Encryption policy already exists or error: {str(e)}")
        
            try:
                # Check if the network policy exists
                network_policy = aoss_client.create_security_policy(
                    name="advanced-rag-network-policy2",
                    policy=json.dumps(
                        [
                            {'Rules': [{'Resource': ['collection/' + vector_store_name],
                                        'ResourceType': 'collection'}],
                             'AllowFromPublic': True}
                        ]),
                    type='network'
                )
            except Exception as e:
                print(f"Network policy already exists or error: {str(e)}")
        
            try:
                # Check if the access policy exists
                access_policy = aoss_client.create_access_policy(
                    name="advanced-rag-access-policy2",
                    policy=json.dumps(
                        [
                            {
                                'Rules': [
                                    {
                                        'Resource': ['collection/' + vector_store_name],
                                        'Permission': [
                                            'aoss:CreateCollectionItems',
                                            'aoss:DeleteCollectionItems',
                                            'aoss:UpdateCollectionItems',
                                            'aoss:DescribeCollectionItems'],
                                        'ResourceType': 'collection'
                                    },
                                    {
                                        'Resource': ['index/' + vector_store_name + '/*'],
                                        'Permission': [
                                            'aoss:CreateIndex',
                                            'aoss:DeleteIndex',
                                            'aoss:UpdateIndex',
                                            'aoss:DescribeIndex',
                                            'aoss:ReadDocument',
                                            'aoss:WriteDocument'],
                                        'ResourceType': 'index'
                                    }],
                                'Principal': [get_execution_role(), bedrock_kb_execution_role_arn],
                                'Description': 'Easy data policy'}
                        ]),
                    type='data'
                )
            except Exception as e:
                print(f"Access policy already exists or error: {str(e)}")
        
            return encryption_policy, network_policy, access_policy
        except Exception as e:
            print(f"Error: {str(e)}")


import boto3
import json

def configure_sagemaker_role_permissions(role_name: str, region_name: str = 'us-east-1'):
    iam = boto3.client('iam', region_name=region_name)
    policy_name = 'FullSageMakerEndpointAccessPolicy'

    # Policy document allowing all actions on any SageMaker endpoint resources
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "sagemaker:*"
                ],
                "Resource": "*",
                "Effect": "Allow"
            },
            {
                "Action": [
                    "sts:*",
                    "ecr:*"
                ],
                "Resource": "*",
                "Effect": "Allow"
            }
        ]
    }

    try:
        print(f"Attaching inline policy '{policy_name}' to role '{role_name}'...")
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        print("✅ Policy attached successfully.")
    except Exception as e:
        print("❌ Error attaching policy:", e)

    # Trust policy for SageMaker
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "sagemaker.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        print(f"Updating trust relationship for role '{role_name}'...")
        iam.update_assume_role_policy(
            RoleName=role_name,
            PolicyDocument=json.dumps(trust_policy)
        )
        print("✅ Trust policy updated successfully.")
    except Exception as e:
        print("❌ Error updating trust policy:", e)



