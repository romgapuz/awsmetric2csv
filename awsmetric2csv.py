import argparse
import csv
import utils

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
allowed_resources = ['ec2', 'rds']
if args.resource not in allowed_resources:
    print('Invalid resource %s provided. Valid resources: %s' % (
        args.resource, allowed_resources))
    exit(0)

# extract parameters
resource = args.resource
period = int(args.period) if args.period else 3600
days = int(args.days) if args.days else 7
filename = args.filename if args.filename else 'output.csv'

# get all instances
instances = utils.get_all_instances(resource)

# process and write to csv
with open(filename, 'wb') as csvfile:
    # initialize csv writer
    csvwriter = csv.writer(
        csvfile,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL)

    # write the headers to csv
    csvwriter.writerow(utils.csv_headers[resource])

    # loop through each instance
    for instance in instances:
        # get datapoints and process
        if resource == 'ec2':
            instance_id = instance.id
        elif resource == 'rds':
            instance_id = instance['DBInstanceIdentifier']
        result = utils.get_metric(resource, instance_id, period, days)
        item_list_arr = utils.process_metric(result)

        # write metrics to csv
        utils.write_to_csv(resource, csvwriter, instance, item_list_arr)

    print('CSV file %s created.' % filename)
