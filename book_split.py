import json
from split_word import Split


if __name__ == "__main__":


    path1 = "./dataset/selected_book_top_1200_data_tag.csv"
    # path1 = "./dataset/test_book.csv"
    path2 = "./dataset/stopwords_hit.txt"
    path3 = "./result/book_keyword_zip.json"
    # path3 = "./result/book_keyword_jiebasearch.json"
    book_test = Split(path1, path2, path3)
    book_test.get_info()
    book_test.get_stop_word_list()

    i = 0
    for info in book_test.info:
        book_test.split_info(info['Tags'],"jieba")
        book_test.combine_single_info(info)
        i = i + 1
        print(i)

    book_test.save_to_json()
