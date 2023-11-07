#!/usr/bin/python3
"""Gather data from an API"""
import requests


def count_words(subreddit, word_list, after=None, word_count={}):
    """
    Queries the Reddit API, parses the title of all hot articles,
    and prints a sorted count of given keywords
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'My user Agent 1.0'}
    params = {'limit': 100, 'after': after}

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code == 200:
        data = response.json().get('data', {})
        children = data.get('children', [])
        for child in children:
            post = child.get('data', {})
            title = post.get('title', '')
            for word in word_list:
                if word.lower() in title.lower():
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1
        after = data.get('after', None)
        if after:
            return count_words(subreddit, word_list, after, word_count)
        else:
            if not len(word_count) > 0:
                return
            for key, value in sorted(word_count.items(),
                                     key=lambda item: item[1],
                                     reverse=True):
                print(f"{key}: {value}")
    else:
        return
