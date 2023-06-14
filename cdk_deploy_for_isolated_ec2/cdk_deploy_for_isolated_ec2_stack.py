from aws_cdk import (
    Duration,
    Stack,
    aws_events as eventBridge,
    aws_events_targets as targets, 
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct
from os import path 

class CdkDeployForIsolatedEc2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #creating a new secret
        ip_address = "0.0.0.0"  # Replace with your desired IP address

        cfn_secret = secretsmanager.CfnSecret(self, "MyCfnSecret",                                
            name="SecretIpForense",
            secret_string=ip_address
        )


        #creating Lambda for ec2 isolation
        lambdaIsolation = lambda_.Function(self, "LambdaForIsolation",
                runtime = lambda_.Runtime.PYTHON_3_9,
                handler = "ec2_isolation.lambda_handler",
                code = lambda_.Code.from_asset(path.join("functions")),
                timeout = 7,
        )

        #adding the iam roles 
        lambdaIsolation.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'ec2:*',
                'autoscaling:*'
            ],
            resources=[
                '*',
            ],
        ))

        #creating event bridge for aws guardduty findings 
        broker = eventBridge.Rule(self, "guardduty-broker-lambda",
                         event_pattern=eventBridge.EventPattern(
                                source=["aws.guardduty"]  
                            )
                         )
        broker.add_target(targets.LambdaFunction(lambdaIsolation, retry_attempts=2))
        
