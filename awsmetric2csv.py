import argparse
import boto3
import datetime
import numpy as np
import csv

# parse argument
parser = argparse.ArgumentParser()
parser.add_argument("resource")
parser.add_argument("--period", help="""
    The granularity, in seconds, of the returned data points.
    A period can be as short as one minute (60 seconds) and must
    be a multiple of 60. The default value is 3600.""")
parser.add_argument("--days", help="""
    The number of days to backtrack and extract metric data.
    Default is 7 days.""")
parser.add_argument("--filename", help="""
    The name of the output csv file. Default is output.csv.""")
args = parser.parse_args()

# check if resource parameter is valid
allowed_resources = ['ec2']
if args.resource not in allowed_resources:
    print('Invalid resource %s provided. Valid resources: %s' % (
        args.resource, allowed_resources))
    exit(0)

# extract parameters
period = int(args.period) if args.period else 3600
days = int(args.days) if args.days else 7
filename = args.filename if args.filename else 'output.csv'

# get current time
now = datetime.datetime.now()

# create boto clients
cw = boto3.client('cloudwatch')
ec2 = boto3.resource('ec2')

# get all running instances
instances = ec2.instances.filter(
    Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']}])

with open(filename, 'wb') as csvfile:
    # initialize csv writer
    csvwriter = csv.writer(
        csvfile,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL)

    # write the headers to csv
    csvwriter.writerow([
        'name',
        'instance',
        'type',
        'hypervisor',
        'virtualization_type',
        'architecture',
        'ebs_optimized',
        'image_id',
        'key_name',
        'metric',
        'low',
        'high',
        'ave',
        'median',
        'launch_time',
        'subnet_id',
        'vpc_id'
    ])

    # loop through each instance
    for instance in instances:
        # get EC2 datapoints
        metric_name = 'CPUUtilization'
        result = cw.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[{
                'Name': 'InstanceId',
                'Value': instance.id
            }],
            StartTime=now - datetime.timedelta(days=days),
            EndTime=now,
            Period=period,
            Statistics=['Maximum'],
            Unit='Percent'
        )

        # get all datapoints and add to list
        item_list = []
        for datapoint in result['Datapoints']:
            item_list.append(float(datapoint['Maximum']))

        # on empty datapoints, append zero to avoid zero-size array error
        if len(item_list) == 0:
            item_list.append(0)

        # convert list to numpy array
        item_list_arr = np.array(item_list)

        # get instance name
        if instance.tags:
            name_dict = next(
                (i for i in instance.tags if i['Key'] == 'Name'),
                None)
        else:
            name_dict = None

        # write data rows
        csvwriter.writerow([
            '' if name_dict is None else name_dict.get('Value'),
            instance.id,
            instance.instance_type,
            instance.hypervisor,
            instance.virtualization_type,
            instance.architecture,
            instance.ebs_optimized,
            instance.image_id,
            instance.key_name,
            metric_name,
            np.min(item_list_arr),
            np.max(item_list_arr),
            np.round(np.average(item_list_arr), 2),
            np.median(item_list_arr),
            instance.launch_time,
            instance.subnet_id,
            instance.vpc_id
        ])
