# awsmetric2csv

**awsmetric2csv** (AWS Metric to CSV) is a Python command-line utility to extract CloudWatch metric data from an AWS resources (e.g. EC2, RDS).

**Features:**
- Extract metric data from all EC2 instances
- Customize parameters: period, days and filename

**Upcoming Features:**
- Add RDS support

### Installation

This application requires Python 2.7 or above. If you don't have Python installed, please download it from here https://www.python.org/downloads/.

Clone the project:

`git clone https://github.com/romgapuz/awsmetric2csv.git`

Go to the project folder:

`cd awsmetric2csv`

Prior installing the packages below, you can optionally install and use [virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/).

Install packages:

`pip install -r requirements.txt`

Install AWS CLI:

`pip install awscli`

Configure the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html):

`aws configure`

### Usage

For usage help run:

`python awsmetric2csv.py -h`

To extract EC2 instances metrics, run:

`python awsmetric2csv.py ec2`

This will create the **output.csv** file.

### Issues

- When error **InvalidParameterCombination** is received. Reduced either period and days parameters.