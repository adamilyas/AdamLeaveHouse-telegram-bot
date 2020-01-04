from datetime import datetime
from config import data_mall_key
import requests as rq
import re

data_mall_url = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2'
p = re.compile('^2\d{3}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')

def data_mall_service(bus_stop_id):
    response = get_bus_stop_data(bus_stop_id)
    if response.status_code != 200:
        return f'Status: {response.status_code}'

    content = response.json()
    return format_telegram_message(content)

def get_bus_stop_data(bus_stop_id):
    response = rq.get(
        data_mall_url,
        params={'BusStopCode': bus_stop_id},
        headers={'AccountKey': data_mall_key, 'Accept': 'application/json'}
    )
    return response

def time_delta_isoformat(isoformat_timestamp: str) -> float:
    """
    Returns
        float: time_delta in seconds 
    """
    arrival_dt = datetime.fromisoformat(isoformat_timestamp) # offset-aware datetime obj
    arrival_timestamp = arrival_dt.timestamp() # https://www.unixtimestamp.com/
    
    current_timestamp = datetime.now().timestamp()
    return arrival_timestamp - current_timestamp

def format_result_string(service_no, minutes_to_arrival, minutes_to_arrival2):
    return f'Bus: {str(service_no).rjust(4, " ")}   Next: {str(minutes_to_arrival).rjust(2, " ")} mins   Next2: {str(minutes_to_arrival2).ljust(4, " ")}\n'

def get_minutes_to_arrival(service, next=1):
        NextBus = 'NextBus'
        if next == 2:
            NextBus = 'NextBus2'

        next_bus = service[NextBus]
        estimated_arrival = next_bus['EstimatedArrival']
        if not p.match(estimated_arrival):
            return 'NA'

        minutes_to_arrival = int(time_delta_isoformat(next_bus['EstimatedArrival'])//60)
        return minutes_to_arrival

def format_telegram_message(content):
    service_list = content['Services']
    if len(service_list) == 0:
        return '**No Bus Available**'

    result = "\n"
    for service in service_list:
        service_no = service['ServiceNo']
        minutes_to_arrival = get_minutes_to_arrival(service)
        minutes_to_arrival2 = get_minutes_to_arrival(service, 2)
        
        result_string = format_result_string(service_no, minutes_to_arrival, minutes_to_arrival2)
        result += result_string

    return f'```{result}```'

if __name__ == "__main__":
    content = {'odata.metadata': 'http://datamall2.mytransport.sg/ltaodataservice/$metadata#BusArrivalv2/@Element', 'BusStopCode': '70259', 'Services': [{'ServiceNo': '135', 'Operator': 'SBST', 'NextBus': {'OriginCode': '54009', 'DestinationCode': '54009', 'EstimatedArrival': '2020-01-04T22:46:41+08:00', 'Latitude': '1.328296', 'Longitude': '103.885517', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus2': {'OriginCode': '54009', 'DestinationCode': '54009', 'EstimatedArrival': '2020-01-04T22:57:10+08:00', 'Latitude': '1.3484126666666667', 'Longitude': '103.8723205', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus3': {'OriginCode': '54009', 'DestinationCode': '54009', 'EstimatedArrival': '2020-01-04T23:09:39+08:00', 'Latitude': '1.3676161666666666', 'Longitude': '103.85064883333334', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}}, {'ServiceNo': '135A', 'Operator': 'SBST', 'NextBus': {'OriginCode': '54009', 'DestinationCode': '93201', 'EstimatedArrival': '2020-01-04T23:16:14+08:00', 'Latitude': '0', 'Longitude': '0', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus2': {'OriginCode': '', 'DestinationCode': '', 'EstimatedArrival': '', 'Latitude': '', 'Longitude': '', 'VisitNumber': '', 'Load': '', 'Feature': '', 'Type': ''}, 'NextBus3': {'OriginCode': '', 'DestinationCode': '', 'EstimatedArrival': '', 'Latitude': '', 'Longitude': '', 'VisitNumber': '', 'Load': '', 'Feature': '', 'Type': ''}}, {'ServiceNo': '137', 'Operator': 'SBST', 'NextBus': {'OriginCode': '94009', 'DestinationCode': '80289', 'EstimatedArrival': '2020-01-04T22:47:24+08:00', 'Latitude': '1.3269929999999999', 'Longitude': '103.90153133333334', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus2': {'OriginCode': '94009', 'DestinationCode': '80289', 'EstimatedArrival': '2020-01-04T23:01:42+08:00', 'Latitude': '1.335734', 'Longitude': '103.91808283333333', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus3': {'OriginCode': '94009', 'DestinationCode': '80289', 'EstimatedArrival': '2020-01-04T23:14:55+08:00', 'Latitude': '1.3258108333333334', 'Longitude': '103.93537666666667', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}}, {'ServiceNo': '154', 'Operator': 'SBST', 'NextBus': {'OriginCode': '22009', 'DestinationCode': '82009', 'EstimatedArrival': '2020-01-04T22:49:29+08:00', 'Latitude': '1.3312428333333333', 'Longitude': '103.87883816666667', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus2': {'OriginCode': '22009', 'DestinationCode': '82009', 'EstimatedArrival': '2020-01-04T22:49:34+08:00', 'Latitude': '1.3292283333333332', 'Longitude': '103.87974533333333', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus3': {'OriginCode': '22009', 'DestinationCode': '82009', 'EstimatedArrival': '2020-01-04T23:03:13+08:00', 'Latitude': '1.3232825', 'Longitude': '103.81648766666666', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}}, {'ServiceNo': '24', 'Operator': 'SBST', 'NextBus': {'OriginCode': '54009', 'DestinationCode': '54009', 'EstimatedArrival': '2020-01-04T22:48:23+08:00', 'Latitude': '1.3421828333333332', 'Longitude': '103.88392416666667', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus2': {'OriginCode': '54009', 'DestinationCode': '54009', 'EstimatedArrival': '2020-01-04T22:57:55+08:00', 'Latitude': '1.3556858333333333', 'Longitude': '103.85667633333334', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus3': {'OriginCode': '54009', 'DestinationCode': '54009', 'EstimatedArrival': '2020-01-04T23:04:15+08:00', 'Latitude': '0', 'Longitude': '0', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}}, {'ServiceNo': '28', 'Operator': 'SBST', 'NextBus': {'OriginCode': '52009', 'DestinationCode': '75009', 'EstimatedArrival': '2020-01-04T22:45:15+08:00', 'Latitude': '1.333584', 'Longitude': '103.88908583333334', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus2': {'OriginCode': '52009', 'DestinationCode': '75009', 'EstimatedArrival': '2020-01-04T22:54:46+08:00', 'Latitude': '1.3435156666666668', 'Longitude': '103.85906833333334', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus3': {'OriginCode': '52009', 'DestinationCode': '75009', 'EstimatedArrival': '2020-01-04T23:04:33+08:00', 'Latitude': '0', 'Longitude': '0', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}}, {'ServiceNo': '43', 'Operator': 'GAS', 'NextBus': {'OriginCode': '65009', 'DestinationCode': '94009', 'EstimatedArrival': '2020-01-04T22:55:35+08:00', 'Latitude': '1.3507883333333333', 'Longitude': '103.87327566666667', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus2': {'OriginCode': '65009', 'DestinationCode': '94009', 'EstimatedArrival': '2020-01-04T23:07:03+08:00', 'Latitude': '1.3792551666666668', 'Longitude': '103.88466866666667', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus3': {'OriginCode': '', 'DestinationCode': '', 'EstimatedArrival': '', 'Latitude': '', 'Longitude': '', 'VisitNumber': '', 'Load': '', 'Feature': '', 'Type': ''}}, {'ServiceNo': '70M', 'Operator': 'SBST', 'NextBus': {'OriginCode': '55509', 'DestinationCode': '55509', 'EstimatedArrival': '2020-01-04T22:50:44+08:00', 'Latitude': '1.3511655', 'Longitude': '103.879244', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}, 'NextBus2': {'OriginCode': '55509', 'DestinationCode': '55509', 'EstimatedArrival': '2020-01-04T23:03:28+08:00', 'Latitude': '1.3744275', 'Longitude': '103.87712633333334', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus3': {'OriginCode': '55509', 'DestinationCode': '55509', 'EstimatedArrival': '2020-01-04T23:15:25+08:00', 'Latitude': '1.3924218333333334', 'Longitude': '103.852671', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'SD'}}, {'ServiceNo': '76', 'Operator': 'SBST', 'NextBus': {'OriginCode': '55509', 'DestinationCode': '82009', 'EstimatedArrival': '2020-01-04T22:57:46+08:00', 'Latitude': '1.3683911666666666', 'Longitude': '103.87612316666667', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus2': {'OriginCode': '55509', 'DestinationCode': '82009', 'EstimatedArrival': '2020-01-04T23:00:54+08:00', 'Latitude': '1.3713683333333333', 'Longitude': '103.871457', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus3': {'OriginCode': '55509', 'DestinationCode': '82009', 'EstimatedArrival': '2020-01-04T23:16:24+08:00', 'Latitude': '1.3712214999999999', 'Longitude': '103.83663466666667', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}}, {'ServiceNo': '80', 'Operator': 'SBST', 'NextBus': {'OriginCode': '67009', 'DestinationCode': '14009', 'EstimatedArrival': '2020-01-04T22:46:44+08:00', 'Latitude': '1.335327', 'Longitude': '103.8884685', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus2': {'OriginCode': '67009', 'DestinationCode': '14009', 'EstimatedArrival': '2020-01-04T22:55:39+08:00', 'Latitude': '1.3603048333333332', 'Longitude': '103.8854675', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}, 'NextBus3': {'OriginCode': '67009', 'DestinationCode': '14009', 'EstimatedArrival': '2020-01-04T23:00:31+08:00', 'Latitude': '1.3664195000000001', 'Longitude': '103.8919365', 'VisitNumber': '1', 'Load': 'SEA', 'Feature': 'WAB', 'Type': 'DD'}}]}
    result = format_telegram_message(content)
    print(result)