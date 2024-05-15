from dataclasses import dataclass
from typing import List
import requests

from . import config


@dataclass
class StreamInfo:
    name: str
    url: str

def get_streams() -> List[StreamInfo]:
    req = requests.get(config.LIVE_INFO_URL)
    if req.status_code != 200:
        raise Exception(f'Status code: {req.status_code}')

    zones = req.json()['eventData']
    fit_zones = list(
        filter(lambda node: node['zoneId'] == config.ZONE_ID, zones))

    if len(fit_zones) != 1:
        raise Exception(f"Unexpected zones fitted: {len(fit_zones)}")

    streams = []
    if config.MAIN_VIEW_RECORD:
        fit_sources = list(
            filter(lambda source: source['res'] == config.RESOLUTION, fit_zones[0]['zoneLiveString']['sources']))
        if len(fit_zones) != 1:
            print(f"Unexpected source fitted for {info['role']}: {len(fit_sources)}")

    fpv_info = fit_zones[0]['fpvData']
    for info in fpv_info:
        fit_sources = list(
            filter(lambda source: source['res'] == config.RESOLUTION, info['sources']))
        if len(fit_zones) != 1:
            print(f"Unexpected source fitted for {info['role']}: {len(fit_sources)}")
        streams.append(StreamInfo(
            name=info['role'],
            url=fit_sources[0]['src'],
        ))
    
    return streams

if __name__ == '__main__':
    print(get_streams())
