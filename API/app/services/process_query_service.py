from rapidfuzz import process

def process_query_with_rapidfuzz(query, data_list, n=5, score_cutoff=50):
    return process.extract(query, data_list, limit=n, score_cutoff=score_cutoff)
