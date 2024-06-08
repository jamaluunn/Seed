import requests
import time
import json
from datetime import datetime

def post_request(url, headers):
    response = requests.post(url, headers=headers)
    try:
        return response.json() if response.text else None
    except ValueError:
        return None

def get_request(url, headers):
    response = requests.get(url, headers=headers)
    try:
        return response.json() if response.text else None
    except ValueError:
        return None

def coday(url, headers):
    if url == 'https://elb.seeddao.org/api/v1/seed/claim' or url == 'https://elb.seeddao.org/api/v1/tasks/7fdc46b3-6612-453a-9ef7-05471800f0ad':
        response = requests.post(url, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    return response.text

def print_banner():
    banner = """
\033[32m         ccee88oo   
\033[32m      C8O8O8Q8PoOb o8oo
\033[32m     dOB69QO8PdUOpugoO9bD
\033[32m   CgggbU8OU qOp qOdoUOdcb
\033[32m       6OuU  p u gcoUodpP
\033[32m        douUP   douUP
\033[32m           |  |
\033[32m           ||/\\
\033[32m           ||\\|  
\033[32m           |||||
\033[32m     .....//||||\\o....
\033[32m   ......./.||||||0.....
\033[32m       \033[0m"""

    print(banner)

print_banner()
print("\033[32mSEED AUTO BOT - @HylobatesMoloch\033[32m")

print("\033[37m1. Complete all task\033[37m")
print("\033[37m2. Upgrade Tree\033[37m")
print("\033[37m3. Upgrade Storage\033[37m")
print("\033[37m4. Checkin Daily\033[37m")
print("\033[37m5. Claim Seeds Repeatedly\033[37m")

choice = input("\033[33mMasukan Pilihan : \033[0m")

with open("data.txt", "r") as file:
    token_list = [line.strip() for line in file.readlines()]

headers_base = {
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://cf.seeddao.org',
    'referer': 'https://cf.seeddao.org/'
}

if choice != '5':
    for i, token in enumerate(token_list, start=1):
        headers = headers_base.copy()
        headers['telegram-data'] = token

        if choice == '1':
            tasks_response = get_request('https://elb.seeddao.org/api/v1/tasks/progresses', headers)
            if tasks_response:
                tasks_data = tasks_response.get('data', [])
                task_ids = [task['id'] for task in tasks_data]

                for task_id in task_ids:
                    complete_response = post_request(f'https://elb.seeddao.org/api/v1/tasks/{task_id}', headers)
                    if complete_response:
                        notification_id = complete_response.get('data')
                        if notification_id:
                            notification_response = get_request(f'https://elb.seeddao.org/api/v1/tasks/notification/{notification_id}', headers)
                            if notification_response:
                                notification_data = notification_response.get('data', {}).get('data', {})
                                
                                if notification_data and notification_data.get('completed'):
                                    reward_amount = notification_data.get('reward_amount', 0)
                                    print(f"Account {i} => Reward: {reward_amount / 1000000000:.6f}")
                                else:
                                    print(f"Account {i} => Task not completed.")
                            else:
                                print(f"Account {i} => Failed to fetch notification data.")
                        else:
                            print(f"Account {i} => Failed to complete task {task_id}.")
                    else:
                        print(f"Account {i} => Failed to complete task {task_id}.")
            else:
                print(f"Account {i} => Failed to fetch task progress.")

        elif choice == '2':
            upgrade_response = post_request('https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade', headers)
            if upgrade_response:
                print(f"Account {i} => {upgrade_response['code']}: {upgrade_response['message']}")
            else:
                print(f"Account {i} => Upgrade request failed.")

        elif choice == '3':
            upgrade_response = post_request('https://elb.seeddao.org/api/v1/seed/storage-size/upgrade', headers)
            if upgrade_response:
                print(f"Account {i} => {upgrade_response}")
            else:
                print(f"Account {i} => Upgrade request failed.")

        elif choice == '4':
            checkin_response = post_request('https://elb.seeddao.org/api/v1/login-bonuses', headers)
            if checkin_response and 'data' in checkin_response:
                checkin_data = checkin_response['data']
                no = checkin_data.get('no', 'Unknown')
                amount = checkin_data.get('amount', 0)

                print(f"Account {i} => Success Checkin {no} Reward: {amount / 1000000000:.6f}")
            else:
                print(f"Account {i} => Failed to check in.")

        else:
            exit()

elif choice == '5':
    while True:
        for index, line in enumerate(token_list):
            account_num = index + 1
            headers = headers_base.copy()
            headers['telegram-data'] = line

            current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            try:
                response1 = coday('https://elb.seeddao.org/api/v1/seed/claim', headers)
                data1 = json.loads(response1)

                response2 = coday('https://elb.seeddao.org/api/v1/profile/balance', headers)
                data2 = json.loads(response2)

                response3 = coday('https://elb.seeddao.org/api/v1/tasks/7fdc46b3-6612-453a-9ef7-05471800f0ad', headers)
                data3 = json.loads(response3)

                notification_url = f'https://elb.seeddao.org/api/v1/tasks/notification/{data3["data"]}'
                response4 = coday(notification_url, headers)
                data4 = json.loads(response4)

                amount = data1.get("data", {}).get("amount", 0)
                balance = data2.get("data", 0)
                message = data1.get("message", "No message")

                if amount > 1:
                    print(f"\033[32m[{current_time}] Account {account_num}: success claim {amount / 1000000000:.6f} [SEED Balance: {balance / 1000000000:.6f}] \033[0m")
                else:
                    print(f"\033[31m[{current_time}] Account {account_num}: {message} [SEED Balance: {balance / 1000000000:.6f}] \033[0m")

            except json.JSONDecodeError:
                print(f"\033[31m[{current_time}] Account {account_num}: Failed to decode JSON response \033[0m")
            except KeyError as e:
                print(f"\033[31m[{current_time}] Account {account_num}: Key error - {e} \033[0m")
            except requests.RequestException as e:
                print(f"\033[31m[{current_time}] Account {account_num}: Request error - {e} \033[0m")

        print("\033[31m===== [Wait 5 minutes] =====\033[0m")
        time.sleep(300)  # Wait for 5 minutes
else:
    exit()
