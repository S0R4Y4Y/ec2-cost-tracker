# E2 Cost Tracker

A Python command-line tool that helps identify which AWS EC2 instances are costing the most money each month. It shows you which instances are running, estimates their monthly cost, and highlights your most expensive instance.

## Features
- 'list' - Show all EC2 instances with their status (color-coded: running/pending/stopped)
- 'cost' - Show the estimated monthly cost of each running instance
- 'topcost' - Identify the most expensive running instance 
- 'info' - Show detailed information about a specific instance (type, state, public IP, launch time)

## Prerequisites

- Python 3.6+
- AWS account with EC2 access
- 'boto3' and 'colorama' Python libraries
- AWS credentials configure ('aws configure')

## Installation

1. Clone the repository:
'''bash
git clone https://github.com/S0R4Y4Y/ec2-cost-tracker.git
cd ec2-cost-tracker
'''

2. Install dependencies:
'''bash 
pip3 install boto3 colorama
'''

3. Configure AWS credentials:
'''bash
aws configure
'''

## Usage

### List all instances
'''bash
python3 ec2_cost_tracker.py list
'''

### Show estimated monthly cost per running instance
'''bash
python3 ec2_cost_tracker.py cost
'''

### Show the most expensive running instance
'''bash
python3 ec2_cost_tracker.py topcost
'''

### Show detailed info for one instance
'''bash
python3 ec2_cost_tracker.py info --instance-id i-1234567890abcdef

## How it works

The tool uses 'boto3' (AWS's Python SDK) to call 'describe_instances()' and read live data on all EC2 instances in the account. Since AWS's EC2 API does not return pricing information directly, this tool uses a small dictionary of estimated hourly prices (for common instance types like 't2.micro', 't3.micro') to calculate approximate monthly cost (hourly price X 730). This gives a quick, practical way to spot cost outliers without needing to set up more complex AWS Cost Explorer or Price List APIs.

## Technologies Used

- **Python 3** - Core Language
- **boto3** - AWS SDK for Python
- **colorama** - Colored terminal output
 
