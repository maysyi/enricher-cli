def list(args, dynamodb, db_table):
    if len(args.list_completed_tasks) == 1: # Only argument is filename, check for whether all functions completed
        filename = args.list_completed_tasks[0]
        status_list = ['vt', 'ss', 'html', 'whois', 'dns', 'cert', 'hist'] # ALL
        filter_expression = ' AND '.join(
            f"({status}_status <> :status)" for status in status_list
        )
        response = dynamodb.query(
            TableName = db_table,
            Select='COUNT',
            KeyConditionExpression='UploadFileName = :UploadFileName',
            FilterExpression=filter_expression,
            ExpressionAttributeValues={
                ':UploadFileName': {'S': filename},
                ':status': {'S': '0'}
            }
        )
        count = response['Count']
        while 'LastEvaluatedKey' in response:
            last_evaluated_key = response['LastEvaluatedKey']
            response = dynamodb.query(
                TableName = db_table,
                Select='COUNT',
                KeyConditionExpression='UploadFileName = :UploadFileName',
                FilterExpression=filter_expression,
                ExpressionAttributeValues={
                    ':UploadFileName': {'S': filename},
                    ':status': {'S': '0'}
                },
                ExclusiveStartKey=last_evaluated_key
            )
            count += response['Count']
        print(f"Number of completed tasks for {filename}: {count}")
    else:
        filename = args.list_completed_tasks[0]
        status_list = args.list_completed_tasks[1:]
        if "none" in status_list: # If none is argument, check for number of items (completed or not)
            response = dynamodb.query(
                TableName = db_table,
                Select='COUNT',
                KeyConditionExpression='UploadFileName = :UploadFileName',
                ExpressionAttributeValues={
                    ':UploadFileName': {'S': filename}
                }
            )
            count = response['Count']
            while 'LastEvaluatedKey' in response:
                last_evaluated_key = response['LastEvaluatedKey']
                response = dynamodb.query(
                    TableName = db_table,
                    Select='COUNT',
                    KeyConditionExpression='UploadFileName = :UploadFileName',
                    ExpressionAttributeValues={
                        ':UploadFileName': {'S': filename}
                    },
                    ExclusiveStartKey=last_evaluated_key
                )
                count += response['Count']
        else: # If specified functions are input as arguments, check the entries where these functions are completed
            filter_expression = ' AND '.join(
                f"({status}_status <> :status)" for status in status_list
            )
            response = dynamodb.query(
                TableName = db_table,
                Select='COUNT',
                KeyConditionExpression='UploadFileName = :UploadFileName',
                FilterExpression=filter_expression,
                ExpressionAttributeValues={
                    ':UploadFileName': {'S': filename},
                    ':status': {'S': '0'}
                }
            )
            count = response['Count']
            while 'LastEvaluatedKey' in response:
                last_evaluated_key = response['LastEvaluatedKey']
                response = dynamodb.query(
                    TableName=db_table,
                    Select='COUNT',
                    KeyConditionExpression='UploadFileName = :UploadFileName',
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues={
                        ':UploadFileName': {'S': filename},
                        ':status': {'S': '0'}
                    },
                    ExclusiveStartKey=last_evaluated_key
                )
                count += response['Count']
        print(f"Number of completed tasks for {filename}: {count}")
