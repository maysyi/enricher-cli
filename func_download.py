import os

def download(args, s3, s3_bucket):
    foldername = args.retrieve_s3_objects

    objects_list = []
    response = s3.list_objects_v2(
        Bucket=s3_bucket,
        Prefix=foldername
    )
    objects = response.get('Contents', [])
    for obj in objects:
        objects_list.append(obj['Key'])
    is_truncated = response.get('IsTruncated', False)
    while is_truncated:
        continuation_token = response.get('NextContinuationToken')
        response = s3.list_objects_v2(
            Bucket=s3_bucket,
            Prefix=foldername,
            ContinuationToken=continuation_token
        )
        objects = response.get('Contents', [])
        for obj in objects:
            objects_list.append(obj['Key'])
        is_truncated = response.get('IsTruncated', False)
    print(f"Found {len(objects_list)} objects in S3 bucket for {foldername}")

    count = 0
    for obj in objects_list:
        obj_name = obj.replace('.csv', '_csv')
        if len(obj_name) > 200:
            obj_folder = obj_name[:190] + obj_name[-10:] # Shorten long names while ensuring final file extension is preserved
        else:
            obj_folder = obj_name
        os.makedirs(os.path.dirname(f"../{obj_folder}"), exist_ok=True)
        try:
            s3.download_file(
                Bucket=s3_bucket,
                Key=obj,
                Filename=f"../{obj_folder}"
            )
            print(f"Downloaded {obj}")
            count += 1
        except Exception as e:
            print("Filename:", obj_folder)
            print(f"Error downloading {obj}: {e}")
            continue
    
    print(f"Downloaded {count} objects to ../{foldername}")