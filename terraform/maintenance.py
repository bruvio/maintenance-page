# %%
import boto3
import os
import sys


elbv2 = boto3.client("elbv2")


def list_rules(listener_arn):
    """List all rules for a given listener ARN."""
    response = elbv2.describe_rules(ListenerArn=listener_arn)
    return response["Rules"]





def modify_rule_priorities(rules, maintenance_mode):
    """Adjust rule priorities based on maintenance mode status, with revised checks."""
    modifications = []
    for rule in rules:
        if "Priority" in rule and rule["Priority"].isdigit():  # Skip the default rule
            original_priority = int(rule["Priority"])
            is_in_maintenance_range = 101 <= original_priority <= 5099

            if maintenance_mode and not is_in_maintenance_range:
                # Entering maintenance mode - increase priority by 100 if not already adjusted
                new_priority = original_priority + 100
                modifications.append(
                    {"RuleArn": rule["RuleArn"], "Priority": new_priority}
                )
            elif not maintenance_mode and is_in_maintenance_range:
                # Exiting maintenance mode - decrease priority by 100 to restore original state
                new_priority = max(
                    1, original_priority - 100
                )  # Ensure priority does not fall below 1
                modifications.append(
                    {"RuleArn": rule["RuleArn"], "Priority": new_priority}
                )

    return modifications


def update_rule_priorities(modifications):
    """Update rules with the new priorities."""
    if modifications:
        elbv2.set_rule_priorities(RulePriorities=modifications)


listener_arn = sys.argv[1]
maintenance_mode = sys.argv[2] == "true"
rules = list_rules(listener_arn)
print(rules)
print("\n\n\n")

modifications = modify_rule_priorities(rules, maintenance_mode)
print(modifications)
update_rule_priorities(modifications)
print("Rule priorities have been updated.")
