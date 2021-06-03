import time
from collections import Counter

from PyPtt import PTT

from gadget import get_today, rewrite_push


class PttPost:

    def __init__(self, boards):
        self.boards = boards
        self.ptt_bot = PTT.API()
        self.ptt_bot.login('ACCOUNT', 'PASSWORD')
        self.info_lst = []


    def crawl(self, amount=100, today=False):
        

        for board in self.boards:
            newest_index = self.ptt_bot.get_newest_index(PTT.data_type.index_type.BBS, board)
            index = newest_index

            run_times = 0
            while index > 0:
                post = self.ptt_bot.get_post(board, post_index=index, query=True)
                print(board, post.index)
                if post.index is None:
                    index += -1
                    continue

                if run_times == amount:
                    break
                if today == True and post.list_date != get_today():
                    print(f'{board}: {newest_index-index}篇')
                    break

                push = rewrite_push(post.push_number)
                info = (board, post.aid, push, post.list_date, post.title, post.web_url)
                self.info_lst.append(info)
                run_times += 1
                index += -1


    def crawl_push(self, amount=100, today=False, push_min='1'):

        search_list = [(PTT.data_type.post_search_type.PUSH, push_min)]
            
        for board in self.boards:
            run_times = 0

            try:
                newest_index = self.ptt_bot.get_newest_index(PTT.data_type.index_type.BBS, 
                    board, search_list=search_list)
                index = newest_index

            except PTT.exceptions.NoSearchResult as e:
                print(board, e)
                continue
            
            while index > 0:
                post = self.ptt_bot.get_post(board, 
                    post_index=index, 
                    search_list=search_list, 
                    query=True
                    )
                if post.index is None:
                    index += -1
                    continue

                if run_times == amount:
                    break
                if today == True and post.list_date != get_today():
                    break
                
                push = rewrite_push(post.push_number)
                info = (board, post.aid, push, post.list_date, post.title, post.web_url)
                self.info_lst.append(info)
                run_times += 1
                index += -1
                    
    

    def crawl_keyword(self, keyword, amount=100):
        search_list = [(PTT.data_type.post_search_type.KEYWORD, keyword)]

        for board in self.boards:
            run_times = 0

            try:
                index = self.ptt_bot.get_newest_index(PTT.data_type.index_type.BBS, 
                    board, search_list=search_list)

            except PTT.exceptions.NoSearchResult as e:
                print(board, e)
                continue

            while index > 0:
                post = self.ptt_bot.get_post(board, 
                    post_index=index, 
                    search_list=search_list, 
                    query=True
                    )
                if post.index is None:
                    index += -1
                    continue

                if run_times  == amount:
                    break
                
                push = rewrite_push(post.push_number)
                info = (board, post.aid, push, post.list_date, post.title, post.web_url)
                self.info_lst.append(info)
                run_times += 1
                index += -1
        
    
    def push_distribution(self, amount):
        self.crawl(amount)

        board_dict = {}
        for info in self.info_lst:
            push_s = info[2] // 10

            if info[0] not in board_dict:
                board_dict[info[0]] = [push_s]
            else:
                board_dict[info[0]] += [push_s]

        board_push_lst = []
        for board, push_lst in board_dict.items():
            push_counter = Counter(push_lst)
            lst = []
            for i in range(11):
                if i not in push_counter:
                    push_counter[i] = 0
            for key, value in push_counter.items():
                lst.append((key, value))
            
            lst.sort()
            push_lst = [element[1] for element in lst]
            info = [board, *push_lst]
            
            board_push_lst.append(info)
        
        return board_push_lst
        


