import requests



import json

import os


ENVS = {
    'qa': 'backend-qa.usummitapp.com',
    'dev': 'backend-dev.usummitapp.com'
}

CHECKS = ['Cache', 'Database', 'Email']


def main(env):
    """Run development sites health-checks

    This function goes to a corresponding env site, gets current health checks
    state

    """
    print(
    f"Env: {env}")

    if env not in ENVS:
        raise Exception(f'{env} environment is not available')

    checks_params = '&'\
                .join([f'checks=i' for i in CHECKS])
    domain = ENVS[env]
    health_check_url=f'https://{domain}/api/v1/utils/health-check/' \
        f'?{checks_params}'
    http_response = requests.get(health_check_url, timeout=20)
    status_code = http_response.status_code
    data = json.loads(http_response)
    print(f'Health check: status {status_code}, content: {json.dumps(data)}')

    if status_code != 200:
        print(f'Env: {env} error (unknown) [{status_code}] status')
        raise Exception('HealthCheck: unknown error')

    errors =[k for k, v in data if v != 'OK']
    if errors:
        print(f'Env: {env} error - {", ".join(errors)}')
        raise Exception(f'HealthCheck: {", ".join(errors)} errors')

    print(f"Env: {env} success - {json.dumps(data)}")
    return 'HealthCheck: ok'


if __name__ == '__main__':
    main('test')
