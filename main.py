import boto3
import argparse

from func_upload import upload
from func_list import list
from func_results import results
from func_download import download
from func_list_loop import list_loop

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

s3_bucket = "XXXXX"  # NEED TO UPDATE
db_table = "XXXXX"  # NEED TO UPDATE

def main():
    parser = argparse.ArgumentParser(
        prog='Enricher V2',
        description='CLI tool to access basic Enricher functionality and information'
    )
    parser.add_argument("-f", "--split_large_file", type=str, nargs='+')
    parser.add_argument("-u", "--upload", type=str, nargs='+')
    parser.add_argument("-v", "--vt", action="store_true")
    parser.add_argument("-s", "--ss", action="store_true")
    parser.add_argument("-j", "--html", action="store_true")
    parser.add_argument("-w", "--whois", action="store_true")
    parser.add_argument("-d", "--dns", action="store_true")
    parser.add_argument("-c", "--cert", action="store_true")
    parser.add_argument("-i", "--hist", action="store_true")
    parser.add_argument("-a", "--all", action="store_true")
    parser.add_argument("-l", "--list_completed_tasks", type=str, nargs='+') # Succeed with name of uploaded file
    parser.add_argument("-r", "--list_loop_completed_tasks", type=str) # Succeed with name of uploaded file
    parser.add_argument("-t", "--retrieve_db_table", type=str) # Succeed with name of uploaded file
    parser.add_argument("-b", "--retrieve_s3_objects", type=str) # Succeed with folder name of contents you want to download.
    args = parser.parse_args()

    if args.split_large_file is not None:
        from func_split import split
        split(args)

    if args.upload is not None:
        upload(args, s3, s3_bucket)

    if args.list_completed_tasks is not None:
        list(args, dynamodb, db_table)

    if args.list_loop_completed_tasks is not None:
        list_loop(args, dynamodb, db_table)
    
    if args.retrieve_db_table is not None:
        results(args, dynamodb, db_table)
    
    if args.retrieve_s3_objects is not None:
        download(args, s3, s3_bucket)

if __name__ == '__main__':
    main()