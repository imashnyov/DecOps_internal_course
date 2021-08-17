import re
from datetime import datetime, timedelta

MAIN_REGEX = r'(?P<h>\S*) \((?P<forwarded>.*?)\) (?P<l>\S*) (?P<u>\S*) \[(?P<t>.*?)\] \"(?P<r>.*?)\" (?P<s>\d*) (?P<b>\-|\d*) (?P<T>\S*) (?P<D>\S*) \"(?P<referers>.*?)\" \"(?P<user_agents>.*?)\" \"(?P<balancer>.*?)\"'

def log_parser(log_file):
    with open(log_file, 'r') as f:
        for line in f:
            mathes = re.search(MAIN_REGEX, line)
            yield mathes.groupdict()

def ip_parser():
    ip_dict = {}
    for i in log_parser('access_log'):
        parsed_ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', i['forwarded'])[0]
        ip_dict[parsed_ip] = ip_dict.get(parsed_ip, 0) + 1
    return ip_dict


def time_often():
    dict_ip_time_often = {}
    for i in log_parser('access_log'):
        parsed_time = re.findall(r'\d+\/\w+\/\d+:\d+:\d+', i['t'])[0]
        dict_ip_time_often[parsed_time] = dict_ip_time_often.get(parsed_time, 0) + 1
    return dict_ip_time_often


def agents_often():
    dict_parsed_agents_often = {}
    for i in log_parser('access_log'):
        parsed_agent = i['user_agents']
        dict_parsed_agents_often[parsed_agent] = dict_parsed_agents_often.get(parsed_agent, 0) + 1
    a = sorted(dict_parsed_agents_often.items(), key = lambda x : x[1], reverse = True)
    return a[:3]

    
def error_often():
    dict_error_often = {}
    for i in log_parser('access_log'):
        parsed_error = re.findall(r'\d+\/\w+\/\d+:\d+:\d+', i['t'])[0]
        if re.match(r'50\d', i['s']):
            dict_error_often[parsed_error] = dict_error_often.get(parsed_error, 0) + 1
    return dict_error_often

def request_lenght():
    parsed_requests = []
    for i in log_parser('access_log'):
        parsed_requests.append(i['r'])
    parsed_requests.sort(key=len)
    max_len="\n\t".join(parsed_requests[:-4:-1])
    min_len="\n\t".join(parsed_requests[:3])
    return f'3 MAX lenght request is:\n\t{max_len} \n\n and 3 MIN lenght request is:\n\t{min_len}'

def request_dir():
    request_dict = {}
    for i in log_parser('access_log'):
        parsed_request = re.findall(r'"GET(.*?\/.*?\/)', i['r'])[0]
        request_dict[parsed_request] = request_dict.get(parsed_request, 0) + 1
    a = sorted(request_dict.items(), key = lambda x : x[1], reverse = True)
    return a[:3]

def balancer():
    balancer_dict = {}
    for i in log_parser('access_log'):
        parsed_balancer = i['balancer']
        balancer_dict[parsed_balancer] = balancer_dict.get(parsed_balancer, 0) + 1
    return balancer_dict

def referers():
    referers_dict = {}
    for i in log_parser('access_log'):
        parsed_referers = i['referers']
        referers_dict[parsed_referers] = referers_dict.get(parsed_referers, 0) + 1
    return referers_dict

#-----------------------------------------------------------------------------------------

def get_interval_for_time(dt: timedelta, time_val: datetime):
    """ Return start of the time interval for time value
    Args:
        dt (timedelta): interval duration
        time_val (datetime): time value

    Returns:
        datetime: starting time for interval
    """
    zero_year = datetime(2000, 1, 1, tzinfo=time_val.tzinfo)
    interval_start = zero_year + ((time_val - zero_year) // dt) * dt
    return interval_start

def group_upstreams_by_time(dT = timedelta(minutes=1)):
    intervals = {}
    for i in log_parser('access_log'):
        # get upstream
        upstream = i['balancer']
        # convert string time to datetime
        time = datetime.strptime(i['t'], '%d/%b/%Y:%H:%M:%S %z')
        # get start of timeinterval that contains this time and convert it to string
        time_interval = get_interval_for_time(dT, time).strftime('%d/%b/%Y:%H:%M:%S')
        # get upstreams dict by interval as a key
        upstreams = intervals.setdefault(time_interval, {})
        # count upstream
        upstreams[upstream] = upstreams.get(upstream, 0) + 1
    return intervals

def group_requests_count_by_time(dT = timedelta(minutes=1), n: int = 1):
    intervals = {}
    for i in log_parser('access_log'):
        # convert string time to datetime
        time = datetime.strptime(i['t'], '%d/%b/%Y:%H:%M:%S %z')
        # get start of timeinterval that contains this time and convert it to string
        time_interval = get_interval_for_time(dT, time).strftime('%d/%b/%Y:%H:%M:%S')
        # get upstreams dict by interval as a key
        intervals[time_interval] = intervals.get(time_interval, 0) + 1
    result = sorted(intervals.items(), key = lambda x : x[1], reverse = True)
    return result[:n]


# print(ip_parser())
# print(time_often())
# print(agents_often())
# print(error_often())
# print(request_lenght())
# print(request_dir()) #print(request_up_to_slash())
# print(balancer())
# print(referers())
#print(group_upstreams_by_time(dT=3))
print(group_requests_count_by_time(n=3))