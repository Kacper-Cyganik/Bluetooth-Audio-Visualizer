from youtube_search import YoutubeSearch


def YouTube(keyword):
    results = YoutubeSearch(keyword, max_results=1).to_dict()
    data = {"title" : dict(results[0])["title"],
            "duration" : dict(results[0])["duration"],
            "url" : f"https://www.youtube.com{dict(results[0])['url_suffix']}",
            "channel" : dict(results[0])["channel"],
            "views" : dict(results[0])["views"]}
    return data

