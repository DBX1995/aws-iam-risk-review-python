import boto3

# Create a boto3 client for AWS IAM.
iam = boto3.client("iam")

# Retrieve up to 10 IAM roles from the AWS account.
response = iam.list_roles(MaxItems=10)

roles = response["Roles"]

print(f"Retrieved {len(roles)} IAM roles:\n")

for role in roles:
    print(f"- {role['RoleName']}")