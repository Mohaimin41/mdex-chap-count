import requests
import json
from time import sleep

creds = {
'''
first time activating the api client and getting access & refresh token
'''
    "grant_type": "password",
    "username": "<username>",
    "password": "<password>",
    "client_id": "<client_id>",
    "client_secret": "<client_secret>"
'''
access token using refresh token part
'''
    # "grant_type": "refresh_token",
    # "refresh_token": "<refresh_token>",
    # "client_id": "<client_id>",
    # "client_secret": "<client_secret>"
}

r = requests.post(
    "https://auth.mangadex.org/realms/mangadex/protocol/openid-connect/token",
    data=creds,
)

access_token = r.json()["access_token"]
refresh_token = r.json()["refresh_token"]

headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

prev_len = 0

total_files = 0

# looping till 100th offset or the end of follow, very unlikely to have so many manga in follow
for i in range(100):
    file = open(f"manga_p{i}.json", "w+")
    offset = 0
    if (i > 0):
        offset = prev_len

    manga_list_response = requests.get("https://api.mangadex.org/user/follows/manga?limit=90&offset=524", headers=headers)
    
    res = manga_list_response.json()
    
    prev_len = len(res["data"])
    
    if (prev_len == 0):
        break

    file.write(json.dumps(res))
    total_files += 1
    file.close()

    sleep(0.2)


manga_names = []
manga_ids = []
manga_last_chaps = []

# listing manga uuid, name, chapter list
for i in range(total_files):

    with open(f'manga_p{i}.json', 'r') as json_file:
        data = json.load(json_file)

        for manga in data["data"]:
            manga_ids.append(manga["id"])
            manga_last_chaps.append(manga["attributes"]["lastChapter"])
            names = (manga["attributes"]["title"])
            if ("en" in names):
                manga_names.append(names["en"])
            else:
                all_lang = list(names.keys())
                manga_names.append(names[all_lang[0]])

print("Total manga in follow list: ", len(manga_ids))

# storing manga uuid name chapter count
with open("manga_ids.txt", "w+") as out:
    for i in range(len(manga_ids)):
        out.write(manga_ids[i] + " " + manga_names[i] + "\n")
        out.write(str(manga_last_chaps[i]) + "\n")


total_count = 0
total_chaps = 0

log = open(r"chap_count_log.txt", "w+")

for i in range(len(manga_ids)):
    id = manga_ids[i]
    manga = manga_names[i]
    chaps = manga_last_chaps[i]

    # another route to get manga chapter counts
    if (chaps == "" or chaps == 'None' or chaps == None):
        response_manga_chaps_list = requests.get(
            f'''https://api.mangadex.org/chapter?limit=10&manga={id}&translatedLanguage%5B%5D=en&contentRating%5B%5D=safe&contentRating%5B%5D=suggestive&contentRating%5B%5D=erotica&contentRating%5B%5D=pornographic&order%5BcreatedAt%5D=asc&order%5BupdatedAt%5D=asc&order%5BpublishAt%5D=asc&order%5BreadableAt%5D=asc&order%5Bvolume%5D=asc&order%5Bchapter%5D=asc'''
        )
        chaps = int(response_manga_chaps_list.json()["total"])
    
    sleep(0.2)

    # route to get manga chapters that are read
    response_manga_chaps_list_2 = requests.get(
        f"https://api.mangadex.org/manga/{id}/read", headers=headers)

    res = response_manga_chaps_list_2.json()

    total_chaps += int(chaps)
    total_count += max(int(chaps) - len(res["data"]),0)
    
    # logging result for each manga
    log.write(id + " " + manga + " " + ", total: " + str(chaps)
                + " , read: " + str(len(res["data"])) + "\n")

    sleep(0.2)

    # if (i == 14):
    #     break

    if ((i + 1) % 100 == 0):
        print(f"{i+1} manga done out of {len(manga_ids)}")

log.write("\nTotal chapters: " + str(total_chaps) + ", total unread: " + str(total_count))

print("Total available chapters in English in follow: " + str(total_chaps) + ", total unread: " + str(total_count))