import os

def upload(args, s3, s3_bucket):
    filenames = []
    if len(args.upload) == 1 and args.upload[0].endswith('/'):
        # If only one argument is a directory, upload all files in that directory
        directory = args.upload[0]
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            if os.path.isfile(full_path):
                filenames.append(full_path)
    else:
        for filename in args.upload:
            filenames.append(filename)

    function_list = ["vt_status", "ss_status", "html_status", "whois_status", "dns_status", "cert_status", "hist_status"]
    enable_list = []
    for function in [args.vt, args.ss, args.html, args.whois, args.dns, args.cert, args.hist]:
        if function==True:
            enable_list.append("0")
        else:
            enable_list.append("-1")

    if args.all == True:
        enable_list = ["0"] * len(function_list)
    
    if enable_list == ["-1"] * len(function_list):
        print("No function enabled, exiting...")
        exit()

    function_dict = dict(zip(function_list, enable_list))

    for filename in filenames:
        s3.upload_file(
            Filename=filename,
            Bucket=s3_bucket,
            Key=f"upload/{filename.split('/')[-1]}",
            ExtraArgs={
                'Metadata': function_dict
            }
        )

    print(f"{filenames} uploaded successfully to S3")