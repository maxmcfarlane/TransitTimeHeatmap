import googlemaps
import datetime
import pandas as pd
import pickle
import math
import os
from tqdm import tqdm
QUEH = (55.8626549675043, -4.339570424412862)

DEPARTURES = {
    'home': (55.872449036837395, -4.318167046624427)
}


def get_travel_time(departures: list, destination=QUEH, arrival_time=None, weekend=False):
    # now = datetime.datetime.now()
    now = pickle.loads(b'\x80\x04\x95*\x00\x00\x00\x00\x00\x00\x00\x8c\x08datetime\x94\x8c\x08datetime\x94\x93\x94C\n\x07\xe6\x0c\x10\x0e\x1b\x05\x05\x17z\x94\x85\x94R\x94.')
    tomorrow = now + datetime.timedelta(days=1)
    arrival_time = datetime.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day,
                      hour=6, minute=55, second=0)

    while not weekend and arrival_time.weekday() > 4:
        arrival_time = arrival_time + datetime.timedelta(days=1)

    key = pd.read_json('./key.json')

    # Replace YOUR_API_KEY with your actual API key
    gmaps = googlemaps.Client(key=key['key'].squeeze())
    _travel_times = []
    inputs_ = pd.DataFrame({
        'coordinates': departures,
        'destination': [destination] * len(departures),
        'arrival_time': [arrival_time] * len(departures),
        'key': zip(departures, [destination] * len(departures), [arrival_time] * len(departures))})


    if os.path.exists('./results.p'):
        results = pickle.load(open('./results.p', 'rb'))
        results = results.drop_duplicates()
        pickle.dump(results, open('./results.p', 'wb'))
        results_dict = results.set_index(['coordinates', 'destination', 'arrival_time']).to_dict()['travel_time']
        results['key'] = list(zip(results['coordinates'], results['destination'], results['arrival_time']))
        # rnd = 4
        # agg_dict = {k: ((round(k[0][0], rnd), round(k[0][1], rnd)), k[1], k[2]) for k in results['key']}
        # agg_dict_rev = {v: k for k, v in agg_dict.items()}
        results = pd.concat([results, inputs_]).drop_duplicates(subset=['coordinates', 'destination', 'arrival_time'])
        results['travel_time'] = results['key'].map(results_dict)
        # results['agg_key'] = results['key'].map(agg_dict)
        # print(results.groupby('agg_key')['travel_time'].std().fillna(0))
    else:
        results_dict = {}
        results = pd.DataFrame(results_dict)

    if len(results) == 0:

        for coordinates in tqdm(departures, total=len(departures)):
            # Specify the starting and ending locations, and the mode of transportation
            try:
                travel_time = results_dict[(coordinates, destination, arrival_time)]
            except KeyError:
                try:
                    result = gmaps.directions(coordinates,
                                              destination,
                                              mode="transit",
                                              arrival_time=arrival_time,
                                              )
            # result = pickle.loads(b'\x80\x04\x95\xdb\x12\x00\x00\x00\x00\x00\x00]\x94}\x94(\x8c\x06bounds\x94}\x94(\x8c\tnortheast\x94}\x94(\x8c\x03lat\x94G@K\xef\xc4\x07+ml\x8c\x03lng\x94G\xc0\x11E\xd4\xb3K\x1b\x87u\x8c\tsouthwest\x94}\x94(h\x06G@K\xeeeI/\xf4\xbah\x07G\xc0\x11^fD\xd8w%uu\x8c\ncopyrights\x94\x8c\x0fMap data \xc2\xa92022\x94\x8c\x04legs\x94]\x94}\x94(\x8c\x0carrival_time\x94}\x94(\x8c\x04text\x94\x8c\t6:50\xe2\x80\xafAM\x94\x8c\ttime_zone\x94\x8c\rEurope/London\x94\x8c\x05value\x94J\xbcf\x9dcu\x8c\x0edeparture_time\x94}\x94(h\x11\x8c\t6:38\xe2\x80\xafAM\x94h\x13\x8c\rEurope/London\x94h\x15J\xf5c\x9dcu\x8c\x08distance\x94}\x94(h\x11\x8c\x063.6 km\x94h\x15M\x12\x0eu\x8c\x08duration\x94}\x94(h\x11\x8c\x0712 mins\x94h\x15M\xc7\x02u\x8c\x0bend_address\x94\x8c8Queen Elizabeth University Hospital, Glasgow G51 4TF, UK\x94\x8c\x0cend_location\x94}\x94(h\x06G@K\xeekt\xc3 |h\x07G\xc0\x11[\xb4}J\xaezu\x8c\rstart_address\x94\x8c"Crathie Drive, Glasgow G11 7QY, UK\x94\x8c\x0estart_location\x94}\x94(h\x06G@K\xef\xacA<\nrh\x07G\xc0\x11E\xd4\xb3K\x1b\x87u\x8c\x05steps\x94]\x94(}\x94(h\x1a}\x94(h\x11\x8c\x060.4 km\x94h\x15Mg\x01uh\x1d}\x94(h\x11\x8c\x064 mins\x94h\x15M\x0c\x01uh"}\x94(h\x06G@K\xefvd\xe1+)h\x07G\xc0\x11H\xd9\xaf3^\xd2u\x8c\x11html_instructions\x94\x8c\x1bWalk to Auchentorlie Street\x94\x8c\x08polyline\x94}\x94\x8c\x06points\x94\x8c?wq_tItkjYXDdBTb@FJB\\DZFd@Hj@F`@F?tC?P?bADN@H?p@ATAPAPCTGv@EXEb@\x94sh&}\x94(h\x06G@K\xef\xacA<\nrh\x07G\xc0\x11E\xd4\xb3K\x1b\x87uh(]\x94(}\x94(h\x1a}\x94(h\x11\x8c\x060.2 km\x94h\x15K\xc5uh\x1d}\x94(h\x11\x8c\x062 mins\x94h\x15K\x87uh"}\x94(h\x06G@K\xefr\xa1\xde\x0b\xb9h\x07G\xc0\x11F=z\xb4\xd2\x04uh0\x8cBHead <b>south</b> on <b>Thornwood Ave</b> toward <b>Crathie Dr</b>\x94h2}\x94h4\x8c wq_tItkjYXDdBTb@FJB\\DZFd@Hj@F`@F\x94sh&}\x94(h\x06G@K\xef\xacA<\nrh\x07G\xc0\x11E\xd4\xb3K\x1b\x87u\x8c\x0btravel_mode\x94\x8c\x07WALKING\x94u}\x94(h\x1a}\x94(h\x11\x8c\x060.1 km\x94h\x15Kbuh\x1d}\x94(h\x11\x8c\x051 min\x94h\x15KNuh"}\x94(h\x06G@K\xefq\x98\xc9\x90\x01h\x07G\xc0\x11G\xd5K\xf7OWuh0\x8c*Turn <b>right</b> onto <b>Dumbarton Rd</b>\x94\x8c\x08maneuver\x94\x8c\nturn-right\x94h2}\x94h4\x8c\x18yf_tIdnjY?tC?P?bADN@H?p@\x94sh&}\x94(h\x06G@K\xefr\xa1\xde\x0b\xb9h\x07G\xc0\x11F=z\xb4\xd2\x04uhB\x8c\x07WALKING\x94u}\x94(h\x1a}\x94(h\x11\x8c\x0464 m\x94h\x15K@uh\x1d}\x94(h\x11\x8c\x051 min\x94h\x15K7uh"}\x94(h\x06G@K\xefvd\xe1+)h\x07G\xc0\x11H\xd9\xaf3^\xd2uh0\x8cqKeep <b>left</b> to stay on <b>Dumbarton Rd</b><div style="font-size:0.9em">Destination will be on the left</div>\x94hK\x8c\tkeep-left\x94h2}\x94h4\x8c\x19qf_tI|wjYATAPAPCTGv@EXEb@\x94sh&}\x94(h\x06G@K\xefq\x98\xc9\x90\x01h\x07G\xc0\x11G\xd5K\xf7OWuhB\x8c\x07WALKING\x94uehB\x8c\x07WALKING\x94u}\x94(h\x1a}\x94(h\x11\x8c\x063.0 km\x94h\x15M\xd2\x0buh\x1d}\x94(h\x11\x8c\x065 mins\x94h\x15M\x1f\x01uh"}\x94(h\x06G@K\xeex \xa3\r\xb7h\x07G\xc0\x11^fD\xd8w%uh0\x8c\x11Bus towards Govan\x94h2}\x94h4Xy\x02\x00\x00cg_tIh~jYKEI|@CN?H?B?J@F@LDHBFDFB@F@HBFDDFDFDL@NBN?J@@AT?L?BAJCJCJ?BADCHCHEFABABCBABCBABC@ABMBWr@CFq@zCCHMl@CFQp@i@v@cArCWp@IVId@a@dAm@vAWn@CHSh@CHg@fAM`@CJCLCLAJ?J?L?B@H@PBNDLFLDHBDHHDFlAr@n@^rAr@VJrAn@JFx@^v@\\HBj@Tz@Xx@TLB`@HPDx@N^DdAJb@Bb@DXBH@b@BN?R@dJJdCDp@AT@Xe@DKBKDO@MBUH_ABS@QBMDQDIBIFILOJMLODODMDOD[@Y?Q@[BS@QBM@KDKBIBIDIBMBKBS?c@@c@?I@MBGBE?ABAD@DBDBVRDHBHDL@J?D?D?FAHALANCLELEHEHEFI?ADABGDIBGBEAGFEHADGTAF?HCRALAL?N?J?RAdAANCp@?T?DCpAAtACbBAd@?HAZ?FAN?JAV?HAXAXC\\CRE^CPAFC^G`@AFCRAJAJAJAFAHFF@HEHAHAFAJEZEXKr@CTMfAEf@ADCDCHGj@G`@In@Gj@_@jC?BQrAKn@UrASdAa@|BKj@f@\\jDbCtBjAh@TTRbA`@JDRHHFDDDDBFBFDJBL@F@H@J?R?T@d@?JALAV?@HH\x94sh&}\x94(h\x06G@K\xeft}\x80^_h\x07G\xc0\x11H\xe2\x12\xaf/-u\x8c\x0ftransit_details\x94}\x94(\x8c\x0carrival_stop\x94}\x94(\x8c\x08location\x94}\x94(h\x06G@K\xeex \xa3\r\xb7h\x07G\xc0\x11^fD\xd8w%u\x8c\x04name\x94\x8c"Queen Elizabeth Hospitals (Stop 1)\x94uh\x0f}\x94(h\x11\x8c\t6:48\xe2\x80\xafAM\x94h\x13\x8c\rEurope/London\x94h\x15J f\x9dcu\x8c\x0edeparture_stop\x94}\x94(hl}\x94(h\x06G@K\xeft}\x80^_h\x07G\xc0\x11H\xe2\x12\xaf/-uhn\x8c\x13Auchentorlie Street\x94uh\x16}\x94(h\x11\x8c\t6:43\xe2\x80\xafAM\x94h\x13\x8c\rEurope/London\x94h\x15J\x01e\x9dcu\x8c\x08headsign\x94\x8c\x05Govan\x94\x8c\x04line\x94}\x94(\x8c\x08agencies\x94]\x94}\x94(hn\x8c\rFirst Glasgow\x94\x8c\x03url\x94\x8c(http://www.firstgroup.com/ukbus/glasgow/\x94ua\x8c\x05color\x94\x8c\x07#306fb6\x94hn\x8c\x19Glasgow - Glasgow Airport\x94\x8c\nshort_name\x94\x8c\x0277\x94\x8c\ntext_color\x94\x8c\x07#ffffff\x94\x8c\x07vehicle\x94}\x94(\x8c\x04icon\x94\x8c2//maps.gstatic.com/mapfiles/transit/iw2/6/bus2.png\x94hn\x8c\x03Bus\x94\x8c\x04type\x94\x8c\x03BUS\x94uu\x8c\tnum_stops\x94K\x03uhB\x8c\x07TRANSIT\x94u}\x94(h\x1a}\x94(h\x11\x8c\x060.2 km\x94h\x15K\xd9uh\x1d}\x94(h\x11\x8c\x063 mins\x94h\x15K\x9buh"}\x94(h\x06G@K\xeekt\xc3 |h\x07G\xc0\x11[\xb4}J\xaezuh0\x8c@Walk to Queen Elizabeth University Hospital, Glasgow G51 4TF, UK\x94h2}\x94h4\x8c/kw}sIjaoY@A@W@M?KAe@T@?oBAUAOASTUAY?]tAaDQKGEI?\x94sh&}\x94(h\x06G@K\xeey\xe6u\xeb?h\x07G\xc0\x11^Z5\xd6{\xa2uh(]\x94(}\x94(h\x1a}\x94(h\x11\x8c\x0428 m\x94h\x15K\x1cuh\x1d}\x94(h\x11\x8c\x051 min\x94h\x15K\x14uh"}\x94(h\x06G@K\xeeyB\xe1\xfc\xdeh\x07G\xc0\x11]\xe5\x15\x98\xeeyuh0\x8c(Head <b>east</b> on <b>Hospital Blvd</b>\x94h2}\x94h4\x8c\x14kw}sIjaoY@A@W@M?KAe@\x94sh&}\x94(h\x06G@K\xeey\xe6u\xeb?h\x07G\xc0\x11^Z5\xd6{\xa2uhB\x8c\x07WALKING\x94u}\x94(h\x1a}\x94(h\x11\x8c\x0412 m\x94h\x15K\x0cuh\x1d}\x94(h\x11\x8c\x051 min\x94h\x15K\nuh"}\x94(h\x06G@K\xeeu\xbbm\xff\xb8h\x07G\xc0\x11]\xe6\x14\x9co7uh0\x8c\x11Turn <b>right</b>\x94hK\x8c\nturn-right\x94h2}\x94h4\x8c\x0bgw}sIp~nYT@\x94sh&}\x94(h\x06G@K\xeeyB\xe1\xfc\xdeh\x07G\xc0\x11]\xe5\x15\x98\xeeyuhB\x8c\x07WALKING\x94u}\x94(h\x1a}\x94(h\x11\x8c\x0453 m\x94h\x15K5uh\x1d}\x94(h\x11\x8c\x051 min\x94h\x15K&uh"}\x94(h\x06G@K\xeev\xf1\xce\xe4\xd5h\x07G\xc0\x11]\x07O\x7f\x9a\x14uh0\x8c\x10Turn <b>left</b>\x94hK\x8c\tturn-left\x94h2}\x94h4\x8c\x12qv}sIr~nY?oBAUAOAS\x94sh&}\x94(h\x06G@K\xeeu\xbbm\xff\xb8h\x07G\xc0\x11]\xe6\x14\x9co7uhB\x8c\x07WALKING\x94u}\x94(h\x1a}\x94(h\x11\x8c\x0414 m\x94h\x15K\x0euh\x1d}\x94(h\x11\x8c\x051 min\x94h\x15K\nuh"}\x94(h\x06G@K\xeesEq\xfa\x18h\x07G\xc0\x11\\\xeb\xe3\xe9I\x04uh0\x8c\x11Turn <b>right</b>\x94hK\x8c\nturn-right\x94h2}\x94h4\x8c\x0bwv}sIhynYTU\x94sh&}\x94(h\x06G@K\xeev\xf1\xce\xe4\xd5h\x07G\xc0\x11]\x07O\x7f\x9a\x14uhB\x8c\x07WALKING\x94u}\x94(h\x1a}\x94(h\x11\x8c\x0488 m\x94h\x15KXuh\x1d}\x94(h\x11\x8c\x051 min\x94h\x15K>uh"}\x94(h\x06G@K\xeeeI/\xf4\xbah\x07G\xc0\x11[\xcb\xf3\x88\xf98uh0\x8c\x10Turn <b>left</b>\x94hK\x8c\tturn-left\x94h2}\x94h4\x8c\x11av}sIrxnYAY?]tAaD\x94sh&}\x94(h\x06G@K\xeesEq\xfa\x18h\x07G\xc0\x11\\\xeb\xe3\xe9I\x04uhB\x8c\x07WALKING\x94u}\x94(h\x1a}\x94(h\x11\x8c\x0422 m\x94h\x15K\x16uh\x1d}\x94(h\x11\x8c\x051 min\x94h\x15K\x0fuh"}\x94(h\x06G@K\xeekt\xc3 |h\x07G\xc0\x11[\xb4}J\xaezuh0\x8c\x10Turn <b>left</b>\x94hK\x8c\tturn-left\x94h2}\x94h4\x8c\x0fms}sIxqnYQKGEI?\x94sh&}\x94(h\x06G@K\xeeeI/\xf4\xbah\x07G\xc0\x11[\xcb\xf3\x88\xf98uhB\x8c\x07WALKING\x94uehB\x8c\x07WALKING\x94ue\x8c\x13traffic_speed_entry\x94]\x94\x8c\x0cvia_waypoint\x94]\x94ua\x8c\x11overview_polyline\x94}\x94h4Xj\x01\x00\x00wq_tItkjYnDf@jC^`@F?tC?tAFXAfAOpBK|@JDKEMlA?L@RFVHNJBPHJNF\\BZ?h@If@O`@U\\MBWr@u@bDg@pBi@v@cArCa@hAId@a@dAeAfCWr@k@pAQl@GZAh@BZH\\Zf@rAz@bCrApDbB`A`@fBn@zBh@xAThBNjBNnORfA?^q@N_ARsBVo@X]R_@J]Fu@FsANo@Pm@Bw@@m@H]H?JF\\\\HV@^It@KVKPI?ADIHQFMDGNI\\Gx@AtBE|AOnJCfAOjB[nCCRAHFFCRCPYtBYjCGNOlAq@jF]bCi@xCm@hDrE`DtBjAh@TTRbA`@^NNLR`@Hj@@zACd@HJIKBe@Aq@T@?oBCe@ASTUAw@tAaDQKQE\x94s\x8c\x07summary\x94\x8c\x00\x94\x8c\x08warnings\x94]\x94\x8chWalking directions are in beta. Use caution \xe2\x80\x93 This route may be missing sidewalks or pedestrian paths.\x94a\x8c\x0ewaypoint_order\x94]\x94ua.')
                    travel_time = result[0]['legs'][0]['duration']['value']/60
                except:
                     travel_time = 0
            _travel_times.append(travel_time)
        results_ = [{'coordinates': c, 'destination': destination, 'arrival_time': arrival_time,
                    'travel_time': _travel_times[idc]} for idc, c in enumerate(departures)]
        results_ = pd.DataFrame.from_records(results_)
    else:
        # for idr, r in results.sort_values(by='travel_time', ascending=False).iloc[2:10].iterrows():
        #     result = gmaps.directions(r['coordinates'],
        #                               r['destination'],
        #                               mode="transit",
        #                               arrival_time=r['arrival_time'],
        #                               )
        #     break
        for idr, r in tqdm(results.loc[results['travel_time'].isna(), :].iterrows(),
                           total=len(results.loc[results['travel_time'].isna(), :])):
            try:
                result = gmaps.directions(r['coordinates'],
                                          r['destination'],
                                          mode="transit",
                                          arrival_time=r['arrival_time'],
                                          )
                travel_time = result[0]['legs'][0]['duration']['value'] / 60
            except:
                travel_time = 0
            _travel_times.append(travel_time)

        results_ = results.loc[results['travel_time'].isna(), :]
        results_['travel_time'] = _travel_times

    results = pd.concat([results, results_]).dropna().drop_duplicates()
    pickle.dump(results, open('./results.p', 'wb'))
    travel_times = inputs_['key'].map(results.set_index(['coordinates', 'destination', 'arrival_time']).to_dict()['travel_time']).tolist()
    return travel_times
