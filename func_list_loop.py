import time
from func_list import list

# Simulate args for list()
class Args:
    def __init__(self, filename, func):
        self.list_completed_tasks = [filename] + func


def list_loop(args, dynamodb, db_table):
    filename = args.list_loop_completed_tasks
    print(f"Tracking progress for {filename}")
    while True:
        print(f"\n--- Checking status at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        statuses = ['vt', 'ss', 'html', 'whois', 'dns', 'cert', 'hist']
        for status in statuses:
            args = Args(filename, [status])
            print("-----{status}-----".format(status=status))
            list(args, dynamodb, db_table)
        time.sleep(3 * 60)  # 3 minutes
