import datetime

import pandas as pd



def get_today():
    d = datetime.date.today()
    month = d.month
    day = d.day

    if len(str(day)) == 1:
        day = f'0{day}'

    return f'{month}/{day}'


def rewrite_push(push):
    if push is None:
        push = 0
    elif '爆' in push:
        push = 100
    elif 'X' in push:
        push = 0
    else:
        push = int(push)
    
    return push


def get_posts_csv(posts):

    df = pd.DataFrame(posts, columns=['board', 'post_aid', 'push', 'date', 'title', 'website'])
    print(df)
    
    title = f'{posts[0][0]}_{get_today()[-2:]}'
    df.to_csv(f'{title}.csv')

