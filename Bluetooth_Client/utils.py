from youtube_search import YoutubeSearch

# Print menu in terminal
def show_menu():
    print(' __________________________ ')
    print('| \tOPTIONS\t\t   |')
    print('| T : Search YouTube\t   |')
    print('| P : Pause/Resume\t   |')
    print('| + : Change volume (1-10) |')
    print('| - : Change volume (1-10) |')
    print('| X : Exit\t\t   |')
    print('|__________________________|\n')

# Find music -> returns dictionary with searched audio data
def YouTube(keyword):
    results = YoutubeSearch(keyword, max_results=1).to_dict()
    data = {"title": dict(results[0])["title"],
            "duration": dict(results[0])["duration"],
            "url": f"https://www.youtube.com{dict(results[0])['url_suffix']}",
            "channel": dict(results[0])["channel"],
            "views": dict(results[0])["views"]}
    return data