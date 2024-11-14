import json
from split_word import Split
import time


if __name__ == "__main__":

    start = time.time()

    # path1 = "./dataset/selected_book_top_1200_data_tag.csv"
    path1 = "./dataset/test_book.csv"
    path2 = "./dataset/stopwords_hit.txt"
    # path3 = "./result/book_keyword.json"
    path3 = "./result/booktest_jieba_search.json"
    book_test = Split(path1, path2, path3)
    book_test.get_info()
    book_test.get_stop_word_list()

    for info in book_test.info:
        book_test.split_info(info['Tags'],"snowNLP")
        # book_test.single_id_info.append(info['Tags'])
        book_test.combine_single_info(info)
    book_test.save_to_json()

    start = time.time()
    print('Running time: %s Seconds' % (end - start))