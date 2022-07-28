import requests
import json
import csv
import time

VMID = "155774183"
URL = "https://api.bilibili.com/x/relation/stat?vmid={}&jsonp=jsonp".format(VMID)

def get_follower_count():
    result = requests.get(URL)
    data = json.loads(result.text)
    return data["data"]["follower"]

def main():
    follwer_count = get_follower_count()
    current_time = time.ctime().strip()

    with open("ttlarva-follower.csv", "a") as f:
        writer = csv.writer(f)
        print(follwer_count, current_time)
        writer.writerows([[follwer_count, current_time]])

    print("done")

if __name__ == "__main__":
    main()
