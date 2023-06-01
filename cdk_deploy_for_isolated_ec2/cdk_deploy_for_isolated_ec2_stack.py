from aws_cdk import (
    Duration,
    Stack,
    aws_events as eventBridge,
    aws_lambda as lambda_,
    aws_iam as iam,
    triggers,
)
from constructs import Construct
from os import path 

class CdkDeployForIsolatedEc2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaIsolation = lambda_.Function(self, "LambdaForIsolation",
                runtime = lambda_.Runtime.PYTHON_3_10,
                handler = "ec2_isolation.lambda_handler",
                code = lambda_.Code.from_asset(path.join("functions")),
        )

        lambdaStream.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'ec2:*',
                'autoscaling:*'
            ],
            resources=[
                '*',
            ],
        ))

        
        broker = eventBridge.Rule(self, "guardduty-broker-lambda",
                         event_pattern=events.EventPattern(
                                source=["aws.guardduty"]  
                            )
                         )
        broker.add_target(targets.LambdaFunction(lambdaIsolation, retry_attempts=2))
        
        trigger = triggers.Trigger(self, "MyTrigger",
            handler=function_,

            # the properties below are optional
            execute_after=[broker]
        )
