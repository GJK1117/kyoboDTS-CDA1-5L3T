## 연재소설 S3 to RDS 수정/삭제 람다 함수 설정값

### CLI CMD (조회)

````
aws lambda get-function --function-name datasync_S3toRDS_updates
````

````json
{
    "Configuration": {
        "FunctionName": "datasync_S3toRDS_updates",
        "FunctionArn": "arn:aws:lambda:ap-northeast-2:390402565508:function:datasync_S3toRDS_updates",
        "Runtime": "python3.11",
        "Role": "arn:aws:iam::390402565508:role/service-role/datasync_S3toRDS_updates-role-8gl3xv8x",
        "Handler": "lambda_function.lambda_handler",
        "CodeSize": 1559,
        "Description": "연재소설 데이터 sync ",
        "Timeout": 20,
        "MemorySize": 128,
        "LastModified": "2024-11-23T14:10:38.000+0000",
        "CodeSha256": "5VUkkv7KwwCjbj8AozPgKOy1y9G1LMwrOETuMV2wgns=",
        "Version": "$LATEST",
        "VpcConfig": {
            "SubnetIds": [
                "subnet-0b9114afd3cd1f916",
                "subnet-05b05d422e9b7a9ee",
                "subnet-08234318acf8eff6d",
                "subnet-074965305830349ce"
            ],
            "SecurityGroupIds": [
                "sg-0091edac20ef19f93"
            ],
            :
````