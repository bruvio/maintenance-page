import argparse
import boto3
import json

def contains_any(main_string, substrings):
    # Iterate through each substring in the list
    for substring in substrings:
        # Check if the current substring is in the main string
        if substring in main_string:
            return True  # Return True if found
    return False  # Return False if none of the substrings are found

def get_alb_host_rules(alb_arn):
    """Query the specified ALB and grab all the host rules."""
    client = boto3.client('elbv2')
    # Get the listener for the ALB
    listeners = client.describe_listeners(LoadBalancerArn=alb_arn)['Listeners']
    
    rules = []
    for listener in listeners:
        # For each listener, get the rules
        listener_rules = client.describe_rules(ListenerArn=listener['ListenerArn'])['Rules']
        for rule in listener_rules:
            for action in rule.get('Actions', []):
                if action['Type'] == 'forward':
                    for condition in rule.get('Conditions', []):
                        if condition['Field'] == 'host-header':
                            rules.append({
                                'HostHeader': condition['Values'],
                                'TargetGroup': action['TargetGroupArn']
                            })
    return rules


def write_to_tfvars_with_priority_mapping(host_rules, output_file, env,exclusion_list):
    """Writes host headers with priorities into a Terraform variables file, filtering by the environment's domain."""
    import json
    from enum import Enum

    class Environment(Enum):
        DEV = "*.int.ngis.io"
        TEST = "*.test.genomics.nhs.uk"
        E2E = "*.e2e.genomics.nhs.uk"
        UAT = "*.uat.genomics.nhs.uk"
        PROD = "*.genomics.nhs.uk"

    # Getting the domain pattern for the given env
    domain_pattern = Environment[env.upper()].value.replace("*", "")

    # Filtering hosts based on the domain pattern of the given environment
    # hosts = [host for rule in host_rules for host in rule['HostHeader'] if domain_pattern in host]
    hosts = [host for rule in host_rules for host in rule['HostHeader']
             if domain_pattern in host and not any(exclude in host for exclude in exclusion_list)]

    # Generating priorities based on filtered hosts
    priorities = {host: 1 + i for i, host in enumerate(hosts)}

    # Writing the filtered hosts with priorities to the specified output file
    with open(f"{env}_{output_file}", 'w') as f:
        f.write(f"hosts = {json.dumps(priorities)}\n")



def write_to_tfvars(host_rules, output_file):
    """Writes host headers into a Terraform variables file."""
    hosts = [host['HostHeader'][0] for host in host_rules]  # Assuming each rule has exactly one host header
    with open(output_file, 'w') as f:
        f.write('hosts = ' + json.dumps(hosts) + '\n')

def write_to_tfvars_with_priority(host_rules, output_file,env):
    """Writes host headers with priorities into a Terraform variables file."""
    hosts = [host['HostHeader'][0] for host in host_rules]  # Assuming each rule has exactly one host header
    priorities = {host: 1 + i for i, host in enumerate(hosts)}
    with open(f"{env}_{output_file}", 'w') as f:
        f.write(f"hosts = {json.dumps(priorities)}\n")


def main():
    parser = argparse.ArgumentParser(description="Get ALB Host Rules")
    parser.add_argument("--alb-arn", required=True, help="ARN of the Application Load Balancer")
    parser.add_argument("--output-tfvars", help="Output hosts to a Terraform variables file")
    parser.add_argument("--env",help="AWS environment",default="dev")
    args = parser.parse_args()
    exclusion_list = ['biobank', "miportal"]
    rules = get_alb_host_rules(args.alb_arn)
    for rule in rules:
        print(f"Host Header: {rule['HostHeader']}, Target Group: {rule['TargetGroup']}")

    if args.output_tfvars:
        write_to_tfvars_with_priority_mapping(rules, args.output_tfvars,args.env,exclusion_list)
        print(f"Host headers written to {args.output_tfvars}")

if __name__ == "__main__":
    main()
