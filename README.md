
# AWS IAM Risk Review Tool

A Python-based AWS security assessment tool that uses boto3 to inspect customer-managed IAM policies and identify wildcard permissions requiring least-privilege review.

## Overview

This project demonstrates how Python can automate AWS IAM security reviews by retrieving policy documents, analyzing permission statements, and reporting potentially excessive permissions.

The tool uses AWS API calls and does not require hard-coded credentials.

## Features

- Retrieves customer-managed IAM policies using boto3.
- Inspects the default version of each policy.
- Parses IAM JSON policy statements.
- Evaluates `Allow` statements.
- Identifies unrestricted actions (`Action: "*"`).
- Identifies service-wide wildcard actions (`s3:*`, `iam:*`, `ec2:*`, etc.).
- Identifies wildcard resources (`Resource: "*"`).
- Prints findings for manual security review.

## Technologies

- Python 3
- AWS SDK for Python (boto3)
- AWS IAM
- AWS CLI
- Git

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/DBX1995/aws-iam-risk-review-python.git
cd aws-iam-risk-review-python
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure AWS authentication

Configure AWS credentials through a supported boto3 credential provider, such as an AWS CLI profile or IAM role.

The credentials require read-only access to list IAM policies and retrieve their policy versions.

Do not store AWS access keys in the source code.

### 5. Run the scanner

```powershell
python iam_risk_review.py
```

## Example Output

The following output was generated during testing with a temporary, unattached IAM policy:

```text
Reviewing 9 customer-managed IAM policies...

[REVIEW] dbx-iam-service-wildcard-test
  - Allows service-wide wildcard Action: "s3:*"
  - Uses wildcard Resource: "*"
```

## Security Validation

The scanner was validated using a controlled IAM test:

1. Created an unattached customer-managed IAM policy containing `Action: "s3:*"` and `Resource: "*"`.
2. Executed the Python scanner.
3. Verified both wildcard findings appeared.
4. Deleted the disposable test policy.
5. Reran the scanner and confirmed the test findings disappeared.

No active IAM identities or workloads were modified during testing.

## Current Limitations

- Reviews customer-managed IAM policies only.
- Uses a single `list_policies` response with `MaxItems=50`; pagination is not yet implemented.
- Flags exact global action wildcards and service-wide `:*` patterns.
- Does not evaluate effective permissions, policy conditions, permission boundaries, or service control policies.
- Wildcard findings indicate areas for security review, not confirmed vulnerabilities.

## Future Improvements

- AWS IAM policy pagination.
- More detailed findings and summary reporting.
- Additional least-privilege checks.

## Purpose

Developed as a hands-on AWS security engineering portfolio project for DBX Solutions, demonstrating Python automation, AWS API integration, IAM security analysis, and controlled security testing.
