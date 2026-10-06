import boto3

iam = boto3.client("iam")

# Retrieve customer-managed IAM policies.
response = iam.list_policies(
    Scope="Local",
    MaxItems=50
)

policies = response["Policies"]

print(f"Reviewing {len(policies)} customer-managed IAM policies...\n")


def to_list(value):
    """Convert a string or list value into a list."""
    if isinstance(value, list):
        return value
    return [value]


for policy in policies:
    policy_name = policy["PolicyName"]
    policy_arn = policy["Arn"]
    version_id = policy["DefaultVersionId"]

    version = iam.get_policy_version(
        PolicyArn=policy_arn,
        VersionId=version_id
    )

    document = version["PolicyVersion"]["Document"]
    statements = document.get("Statement", [])

    if isinstance(statements, dict):
        statements = [statements]

    findings = []

    for statement in statements:
        # Focus on permissions being allowed, not Deny statements.
        if statement.get("Effect") != "Allow":
            continue

        actions = to_list(statement.get("Action", []))
        resources = to_list(statement.get("Resource", []))

        # Detect unrestricted and service-wide wildcard actions.
        for action in actions:
            if action == "*":
                findings.append('Allows unrestricted Action: "*"')
            elif action.endswith(":*"):
                findings.append(
                    f'Allows service-wide wildcard Action: "{action}"'
                )

        # Detect wildcard resources.
        if "*" in resources:
            findings.append('Uses wildcard Resource: "*"')

    # Display findings for each policy.
    if findings:
        print(f"[REVIEW] {policy_name}")

        for finding in findings:
            print(f"  - {finding}")

        print()