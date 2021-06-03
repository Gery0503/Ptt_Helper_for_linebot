import pandas as pd

import ptt_class
from gadget import get_posts_csv, get_today
from HerokuData import QueryTable as QT
from TempData import *


def push_count_csv(boards, amount):

    ptt_board = ptt_class.PttPost(boards)
    board_push_lst = ptt_board.push_distribution(amount)
    print(board_push_lst)

    df = pd.DataFrame(board_push_lst, 
        columns=['board', '0~9', '10~19', '20~29', '30~39', '40~49', '50~59',
            '60~69', '70~79', '80~89', '90~99', '100'])
    
    print(df)
    
    title = f'{board_push_lst[0][0]}_{get_today()[-2:]}'
    df.to_csv(f'{title}.csv')


def closure_yesterday(date):
    
    dailypost = QT('dailypost')
    rows = dailypost.select_date(date)

    posts_in_past = QT('posts_in_past')
    posts_in_past.insert(rows)

    if posts_in_past.select_date(date):
        dailypost.delete_date(date)    
    else:
        print('insert fail')


def ptt_amount(boards):
    ptt_board = ptt_class.PttPost(boards)
    ptt_board.crawl(100)

    posts = ptt_board.info_lst

    posts_100 = QT('posts_100')
    posts_100.delete_all()
    posts_100.insert(posts)

    get_posts_csv(posts)


def ptt_today(boards):

    ptt_board = ptt_class.PttPost(boards)
    ptt_board.crawl(today=True)

    posts = ptt_board.info_lst

    QT('dailypost').upsert(posts)
    get_posts_csv(posts)


def filter_dailypost():
    notice_info = QT('notice').select()
    post_info = []

    for info in notice_info:
        board = info[0]
        if info[1] == True:
            rows = QT('dailypost').select_board(board)
            post_info.extend(rows)
            continue
        
        elif isinstance(info[2], int):
            rows = QT('dailypost').select_push(board, info[2])
            post_info.extend(rows)
        
        elif isinstance(info[3], str):
            keywords_lst = info[3].split(',')
            dailypost = QT('dailypost').select_board(board)
            rows = []
            for post in dailypost:
                for keyword in keywords_lst:
                    if keyword in post[4]:
                        rows.append(post)
                        continue
            post_info.extend(rows)
    
    dailyfilter = QT('dailyfilter')
    dailyfilter.upsert(post_info)



"""function invoke"""
# closure_yesterday('6/02')
# ptt_amount(board_1)
# ptt_today(board_1)
# filter_dailypost()

