import csv
import os
import json

""" Recursive function to format DynamoDB items into standard dictionary format. """
def format_dict(item):
    for key, value in item.items():
        if 'S' in value:
            item[key] = value['S']
        elif 'N' in value:
            item[key] = value['N']
        elif 'BOOL' in value:
            item[key] = value['BOOL']
        elif 'NULL' in value:
            item[key] = None
        elif 'M' in value:
            item[key] = format_dict(value['M'])  # Recursively format nested dictionaries
        elif 'L' in value:
            new_list = []
            for i in value['L']:
                if 'M' in i:
                    new_list.append(format_dict(i['M']))
                else:
                    new_list.append(list(i.values())[0])
            item[key] = new_list
        elif 'SS' in value:
            item[key] = value['SS']
        elif 'NS' in value:
            item[key] = value['NS']
        elif 'BS' in value:
            item[key] = value['BS']
        elif 'B' in value:
            item[key] = value['B']
        else:
            continue
    return item

def results(args, dynamodb, db_table):
    csv_filename = args.retrieve_db_table
    json_filename = csv_filename[:-4] + ".json"

    response = dynamodb.query(
        TableName=db_table,
        KeyConditionExpression='UploadFileName = :UploadFileName',
        ExpressionAttributeValues={
            ':UploadFileName': {'S': csv_filename}
        }
    )
    items_list = response.get('Items', [])
    
    items = []
    for item in items_list:
        items.append(format_dict(item))

    while 'LastEvaluatedKey' in response:
        last_evaluated_key = response['LastEvaluatedKey']
        response = dynamodb.query(
            TableName=db_table,
            KeyConditionExpression='UploadFileName = :UploadFileName',
            ExpressionAttributeValues={
                ':UploadFileName': {'S': csv_filename}
            },
            ExclusiveStartKey=last_evaluated_key
        )
        items_list = response.get('Items', [])
        for item in items_list:
            items.append(format_dict(item))

    print(f"Retrieved {len(items)} items from DynamoDB table for {csv_filename}")
    
    if not items:
        items_headers = []
    else:
        all_keys = set()
        for item in items:
            all_keys.update(item.keys())
        items_headers = sorted(all_keys)
    
    os.makedirs("../results", exist_ok=True)
    with open(f"../results/{json_filename}", 'w', newline='', encoding='utf-8') as jsonfile:
        json.dump(items, jsonfile, indent=2)

    with open(f"../results/{csv_filename}", 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=items_headers)
        writer.writeheader()
        writer.writerows(items)
    print(f"Results saved to ../results/")

