import boto3
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

PRICING = {
    't2.micro': 0.0152,
    't3.micro': 0.0136,
}

ec2 = boto3.client('ec2', region_name='ap-southeast-1')

def get_hourly_price(instance_type):
    return PRICING.get(instance_type, 0.05)

def list_instances():
    response = ec2.describe_instances()

    if not response['Reservations']:
        print("Instance does not exist.")
        return
    
    print(f"{'Instance_ID':<20} {'Name':<25} {'Type':<15} {'State':<15}")

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']

            name = 'N/A'
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']

            if state == 'running':
                state = Fore.GREEN + state + Style.RESET_ALL
            elif state == 'pending':
                state = Fore.YELLOW + state + Style.RESET_ALL
            elif state == 'stopped':
                state = Fore.RED + state + Style.RESET_ALL

            print(f"{instance_id:<20} {name:<25} {instance_type:<15} {state:<15}")

def show_costs():
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']

            if state == 'running':
                hourly_price = get_hourly_price(instance_type)
                monthly_cost = hourly_price * 730

                print(f"{instance_id} ({instance_type}): ${monthly_cost:.2f}/month")

def top_cost():
    response = ec2.describe_instances()

    highest_cost = 0
    highest_instance_id = None

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_type = instance['InstanceType']
            state = instance['State']['Name']

            if state == 'running':
                hourly_price = get_hourly_price(instance_type)
                monthly_cost = hourly_price * 730

                if monthly_cost > highest_cost:
                    highest_cost = monthly_cost
                    highest_instance_id = instance_id

    print(f"Most expensive instance: {highest_instance_id} at ${highest_cost:.2f}/month")

def get_instance_info(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]

    print(f"Instance ID:      {instance['InstanceId']}")
    print(f"Instance Type:    {instance['InstanceType']}")
    print(f"State:            {instance['State']['Name']}")
    print(f"Public IP:        {instance.get('PublicIpAddress', 'N/A')}")
    print(f"Launch Time:      {instance['LaunchTime']}")

def main():
    parser = argparse.ArgumentParser(description='EC2 Cost Tracker')
    parser.add_argument('action', choices=['list', 'cost', 'topcost', 'info'])
    parser.add_argument('--instance-id', help='EC2 Instance ID')

    args = parser.parse_args()

    if args.action == 'list':
        list_instances()
    elif args.action == 'cost':
        show_costs()
    elif args.action == 'topcost':
        top_cost()
    elif args.action == 'info':
        get_instance_info(args.instance_id)

if __name__ == '__main__':
    main()
