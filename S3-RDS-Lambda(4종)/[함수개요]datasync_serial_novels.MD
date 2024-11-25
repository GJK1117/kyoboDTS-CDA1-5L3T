## 연재소설 S3 to RDS PUT/입력 함수

### CLI CMD (조회)

````
aws lambda get-function --function-name datasync_serial_novels
````

```json
{
    "Configuration": {
        "FunctionName": "datasync_serial_novels",
        "FunctionArn": "arn:aws:lambda:ap-northeast-2:390402565508:function:datasync_serial_novels",
        "Runtime": "python3.11",
        "Role": "arn:aws:iam::390402565508:role/service-role/datasync_serial_novels-role-yi7xmjr8",
        "Handler": "lambda_function.lambda_handler",
        "CodeSize": 1503,
        "Description": "Serial_novels-RDS-Input",
        "Timeout": 30,
        "MemorySize": 256,
        "LastModified": "2024-11-23T14:13:21.000+0000",
        "CodeSha256": "URQIOATp8NjqjKgRwllAvJZdHoo5wO2UMuvl5pdzeuw=",
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
```