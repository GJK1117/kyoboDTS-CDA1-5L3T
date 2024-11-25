## 일반소설 S3 to RDS 수정/삭제 람다 함수 설정값

### CLI CMD (조회)

```
aws lambda get-function --function-name datasync_S3toRDS_generalbooks
```

````json
{
	"Configuration": {
		"FunctionName": "datasync_S3toRDS_generalbooks",
		"FunctionArn": "arn:aws:lambda:ap-northeast-2:390402565508:function:datasync_S3toRDS_generalbooks",
		"Runtime": "python3.11",
		"Role": "arn:aws:iam::390402565508:role/service-role/datasync_S3toRDS_generalbooks-role-absdjxh9",
		"Handler": "lambda_function.lambda_handler",
		"CodeSize": 1656,
		"Description": "RDS 일반도서 EDIT/DELETE",
		"Timeout": 3,
		"MemorySize": 128,
		"LastModified": "2024-11-22T08:22:17.000+0000",
		"CodeSha256": "1ZMc+0J8TAHKWGNxFro/xLriNK3aHS286WQ/8VKi5VI=",
		"Version": "$LATEST",
		"VpcConfig": {
			"SubnetIds": [
				"subnet-0b9114afd3cd1f916",
				"subnet-05b05d422e9b7a9ee",
				"subnet-08234318acf8eff6d",
				"subnet-074965305830349ce"
			],
			"SecurityGroupIds": [
				:

````
