# CLI tool for Enricher V2
Updated: 31/07/2025

# Installation
1. Clone the repository into a local folder (directory) of your choice 
2. On your machine's terminal, move into that directory to use the CLI tool

# Enricher CLI Tool Guide

## 🆙 Uploading Files

### 1. Set Up AWS CLI

```bash
# First-time setup
aws configure
# or
aws configure sso
```

- If using access key & secret (e.g. DAI admin), leave region and output format blank.
- If using SSO, you'll need to run `aws sso login` when prompted in the future.

---

### 2. Update `main.py` Configuration

Edit the following lines in `main.py`:

```python
s3_bucket = "your-s3-bucket-name"
db_table = "your-dynamodb-table-name"
```

> Find these values in `outputs.json` (after deployment) under `s3bucketname` and `dbtablename`.

---

### 3. (Optional) Split Large CSV Files

```bash
python main.py -f [file1.csv] [file2.csv] ...
```

- Creates smaller `.csv` files with **≤10,000 rows each**
- Output saved in `split_files/` directory
- Supports:
  - Multiple files: `file1.csv file2.csv`
  - Folder: `../Domains/` (must end with `/`)
    - All files inside must be `.csv`

---

### 4. Upload CSV Files

```bash
python main.py -u [file(s) or folder/] [function flags]
```

Examples:
```bash
python main.py -u ../Domains/List.csv ../IPs/IPs.csv --vt --ss --whois
python main.py -u ../Domains/ --all
```

#### Function Flags

| Function                        | Short Flag | Long Flag     |
|---------------------------------|------------|---------------|
| VirusTotal Enrichment          | `-v`       | `--vt`        |
| Screenshot                     | `-s`       | `--ss`        |
| HTML/JS/APK Parsing            | `-j`       | `--html`      |
| WHOIS Information              | `-w`       | `--whois`     |
| DNS Information                | `-d`       | `--dns`       |
| SSL/TLS Certificate Info       | `-c`       | `--cert`      |
| Historical Web Content         | `-i`       | `--hist`      |
| Run All Enrichments            | `-a`       | `--all`       |

---

## 📥 Retrieving Processed Data

### Retrieve Summary or Results

| Command                                | Description                                                      | Example |
|----------------------------------------|------------------------------------------------------------------|---------|
| `-l [file.csv]`                        | Show count of **fully completed** entries                        | `python main.py -l ListOfDomains.csv` |
| `-l [file.csv] [vt ss html ...]`      | Show count of entries completed for specific enrichments         | `python main.py -l ListOfDomains.csv vt ss html` |
| `-l [file.csv] none`                  | Show count of all entries regardless of status                   | `python main.py -l ListOfDomains.csv none` |
| `-r [file.csv]`                       | Re-check completion progress every 3 minutes                     | `python main.py -r ListOfDomains.csv` |
| `-t [file.csv]`                       | Download final DynamoDB results as `.csv` into `../results`      | `python main.py -t ListOfDomains.csv` |
| `-b [folder path]`                    | Download all objects in a specific S3 folder                     | `python main.py -b ListOfDomains.csv/html/` |
