## 일반소설 S3 to RDS PUT/입력

### CLI CMD (조회)

````
aws lambda get-function --function-name datasync_general_book
````

````json
{
    "Configuration": {
        "FunctionName": "datasync_general_book",
        "FunctionArn": "arn:aws:lambda:ap-northeast-2:390402565508:function:datasync_general_book",
        "Runtime": "python3.11",
        "Role": "arn:aws:iam::390402565508:role/service-role/datasync_general_book-role-1tm6pw4y",
        "Handler": "lambda_function.lambda_handler",
        "CodeSize": 1462,
        "Description": "RDS 일반도서 PUT 함수 ",
        "Timeout": 30,
        "MemorySize": 128,
        "LastModified": "2024-11-22T08:50:37.000+0000",
        "CodeSha256": "V89gZWkqmY+7ja+2tiGK/555H5wmMXnBcLEbByGYxhE=",
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