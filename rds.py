import boto3
import datetime
import numpy as np

cw = boto3.client('cloudwatch')
rds = boto3.client('rds')

instances = rds.describe_db_instances()

now = datetime.datetime.now()

for instance in instances['DBInstances']:
    metric_name = 'CPUUtilization'
    result = cw.get_metric_statistics(
        Namespace='AWS/RDS',
        MetricName=metric_name,
        Dimensions=[{
            'Name': 'DBInstanceIdentifier',
            'Value': instance['DBInstanceIdentifier']
        }],
        StartTime=now - datetime.timedelta(days=3),
        EndTime=now,
        Period=180,
        Statistics=['Maximum'],
        Unit='Percent'
    )

    # get all datapoints and add to list
    item_list = []
    for datapoint in result['Datapoints']:
        print '-'
        item_list.append(float(datapoint['Maximum']))

    # on empty datapoints, append zero to avoid zero-size array error
    if len(item_list) == 0:
        item_list.append(0)

    # convert list to numpy array
    item_list_arr = np.array(item_list)

    print('%s, %s, %s, %s, %s' % (
        instance['DBInstanceIdentifier'],
        np.min(item_list_arr),
        np.max(item_list_arr),
        np.round(np.average(item_list_arr), 2),
        np.median(item_list_arr)
    ))
