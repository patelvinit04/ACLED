from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_iam as iam
)
from constructs import Construct


class AcledStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # niu_VPC
        self.vpc = ec2.Vpc.from_lookup(self, "niu_VPC", vpc_name="niu_VPC")

        ### Lambda
        self.acled_lambda = _lambda.DockerImageFunction(
            self,
            'acled_etl_lambda',
            function_name='acled-etl-lambda',
            memory_size=512,
            timeout=Duration.minutes(10),
            vpc=self.vpc,
            security_groups=[],
            code=_lambda.DockerImageCode.from_image_asset("./")
        )

        self.acled_lambda.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:*Object",
                "s3:ListBucket"
            ],
            resources=["arn:aws:s3:::acled-data",
                "arn:aws:s3:::acled-data/*"]
        ))
        self.acled_lambda.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "secretsmanager:GetSecretValue"
            ],
            resources=["arn:aws:secretsmanager:us-west-2:278808910769:secret:ACLED-YKz9fY"]
        ))