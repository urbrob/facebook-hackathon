from sourcecracker.middlewares.current_user import CurrentUserMiddleware
from googleapiclient.discovery import build


def current_user():
    return CurrentUserMiddleware.get_current_user()


def ask_google(content):
    GOOGLE_SEARCH_API_KEY = 'AIzaSyDaHglOsFZotvJmk9QNJXXbmqZozpjVPYA'
    GOOGLE_SEARCH_ENGINE_ID = '007667251584105741499:c7q_0n2lcqi'
    GOOGLE_SEARCH_API_VERSION = 'v1'
    GOOGLE_SEARCH_RESULTS_PER_PAGE = 3
    GOOGLE_SEARCH_MAX_PAGES = 1
    service = build("customsearch", GOOGLE_SEARCH_API_VERSION,
                        developerKey=GOOGLE_SEARCH_API_KEY)
    results = service.cse().list(
        q=content,
        start=1,
        num=GOOGLE_SEARCH_RESULTS_PER_PAGE,
        cx=GOOGLE_SEARCH_ENGINE_ID,
    ).execute()
    return {data['title']: data['link'] for data in results['items']}
