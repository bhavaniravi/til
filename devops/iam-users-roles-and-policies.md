---
added: Nov 27 2022
draft: false
image: null
layout: ../layouts/BlogPost.astro
slug: iam-users-roles-and-policies
sub_title: There are variety of ways to authenticate yourself with IAM Roles are one
  of the most commonly used. Here is a Cheatsheet to get you started
tags:
- aws
title: AWS IAM Users, Roles, and Policies
---

# IAM Users, Roles, and Policies

So you want to authenticate your apps to use AWS resources like S3 buckets, EC2 instances, and Glue jobs. IAM Roles helps you do that.

### Creating Role and User

- Go into your AWS console, create a role, and a user
- When creating a role, select a required policy, e.g., S3FullAccess, and copy the Role ARN
- When you create a user, make a note of the User ARN, `AWS_SECRET_KEY` and `AWS_ACCESS_KEY`

### Assigning Role to the User

Under the user permissions tab, click add inline policy. This lets the User we created create credentials dynamically to access S3.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": [
                "<role-arn>"
            ]
        }
    ]
}
```

### Adding AssumeRole Permissions Role

In roles under trusted relationship, add the **User ARN.**

```json
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "<user-arn>"
            },
            "Action": "sts:AssumeRole"
        }
```

That's it. You are all set to use AWS now

### Configure AWS CLI

After installing AWS CLI, run the following command. It will prompt you to add the secret and access key we noted when creating the User.

If you forgot to note it down, don't panic, you will find it under the User you created

```
aws configure
```

### Testing Assume Role

You can use the following CLI command or Python script to test the role

#### CLI command

```bash
aws sts assume-role --role-arn <role-arn> --role-session-name test
```

#### Python Script

<pre class="language-python"><code class="lang-python"><strong>ARN = "&#x3C;role-arn>"
</strong><strong>def assume_role():
</strong>    """aws sts assume-role --role-arn &#x3C;role-arn> --role-session-name example-role"""

    client = boto3.client('sts')
    response = client.assume_role(RoleArn=ARN, RoleSessionName="dummy")

    session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                    aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                    aws_session_token=response['Credentials']['SessionToken'])
    
    client = session.client('sts')
    account_id = client.get_caller_identity()["Account"]
    print(account_id)

    return client

assume_role()</code></pre>
