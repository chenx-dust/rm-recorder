import requests

import config


def get_matches() -> list:
    req = requests.get(config.SCHEDULE_URL)
    if req.status_code != 200:
        raise Exception(f'Status code: {req.status_code}')

    zones = req.json()['data']['event']['zones']['nodes']
    fit_zones = list(filter(lambda node: node['id'] == config.ZONE_ID, zones))

    if len(fit_zones) != 1:
        raise Exception(f"Unexpected zones fitted: {len(fit_zones)}")

    matches = []
    if fit_zones[0]['groupMatches']:
        matches.extend(fit_zones[0]['groupMatches'])
    if fit_zones[0]['knockoutMatches']:
        matches.extend(fit_zones[0]['knockoutMatches'])
    return matches

def check_done(matches: list, match_id: str) -> bool:
    fit_matches = list(filter(lambda node: node['id'] == match_id, matches))

    if len(fit_matches) != 1:
        raise Exception(f"Unexpected matches with id {match_id}: {len(fit_matches)}")
    
    match fit_matches[0]['status']:
        case 'DONE' | 'PENDING':
            return True
        case 'STARTED' | 'WAITING':
            return False
        case _unexpected:
            raise Exception(f"Unexpected match status: {_unexpected}")

def get_now_match(matches: list) -> dict:
    fit_matches = list(filter(lambda node: node['status'] == 'STARTED', matches))

    if len(fit_matches) != 1:
        raise Exception(f"Unexpected matches started: {len(fit_matches)}")

    return fit_matches[0]

if __name__ == '__main__':
    match_info = get_now_match(get_matches())
    print("Now Match: "
        f"Blue {match_info['blueSide']['player']['team']['collegeName']} {match_info['blueSide']['player']['team']['name']} "
        "versus "
        f"Red {match_info['redSide']['player']['team']['collegeName']} {match_info['redSide']['player']['team']['name']} ")
