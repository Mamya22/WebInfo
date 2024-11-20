import pickle

# 布尔查询优化
# 优先查询较小频率的词条
# ID升序排列
def load_reverted_dict(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def boolean_search(reverted_dict, query_terms):
    result_ids = None
    for term in query_terms:
        if term in reverted_dict:
            term_ids = set(reverted_dict[term])
            if result_ids is None:
                result_ids = term_ids
            else:
                result_ids &= term_ids
        else:
            return []
    return sorted(result_ids)

def display_results(result_ids):
    for result_id in result_ids:
        # Assuming you have a function to fetch details by ID
        details = fetch_details_by_id(result_id)
        print(f"ID: {details['id']}, Author: {details['author']}, Content: {details['content']}")

def fetch_details_by_id(result_id):
    # Placeholder function to fetch details by ID
    # Replace this with actual implementation
    return {
        'id': result_id,
        'author': 'Author Name',
        'content': 'Content of the document'
    }

if __name__ == "__main__":
    reverted_dict = load_reverted_dict('./result/book_compressed_revert_dict.bin')
    query = input("Enter boolean search terms: ").split()
    result_ids = boolean_search(reverted_dict, query)
    display_results(result_ids)