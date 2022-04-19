from request import *

while True:
    print("Input the last.fm username:")
    x = input()
    hi = {}
    count = 0
    empty = 0
    url_list = []
    try:
        r = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={x}&limit=200"
                         f"&api_key=377330328a222709803420bb8748a1f3&format=json")
        for text in r.json()['topalbums']['album']:
            if count not in hi:
                hi[count] = list()
            hi[count].extend([text['name'], text['artist']['name'], text['playcount']])
            count += 1
        for album in hi.items():
            url_list.append(f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo"
                            f"&api_key=377330328a222709803420bb8748a1f3"f"&artist={album[1][1]}"
                            f"&album={album[1][0]}&format=json")
        len_list = []
        download_all(url_list, len_list)
        for i in range(len(hi.items())):
            try:
                hi[i].append(round(int(hi[i][2]) / len_list[i], 2))
            except ZeroDivisionError:
                hi[i].append(0)
                empty += 1
        sorted_list = dict(sorted(hi.items(), key=lambda item: item[1][3], reverse=True))
        count = 0
        for i in range(empty):
            sorted_list.popitem()
        for album in sorted_list.items():
            print(f"{count+1}. {album[1][0]} has {album[1][3]} plays (gained {int(album[0]) - count} places)")
            count += 1
        print(f"\n{empty} albums(s) were skipped!\n")
    except KeyError:
        print('No such user found, quitting.')
        break
