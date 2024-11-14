import json
from split_word import Split

if __name__ == "__main__":
    # path = "./dataset/selected_movie_top_1200_data_tag.csv"
    path1 = "./dataset/test_movie.csv"
    path2 = "./dataset/stopwords_hit.txt"
    path3 = "./result/movie_keyword.json"
    movie_test = Split(path1, path2, path3)
    movie_test.get_info()
    movie_test.get_stop_word_list()

    for info in movie_test.info:
        movie_test.split_info(info['Tags'],"jieba")
        movie_test.single_id_info.append(info['Tags'])
        movie_test.combine_single_info(info)
    movie_test.save_keyword_to_json()