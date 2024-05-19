from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from consts import FAQ_QA

def only_words_str(s):
    return s.replace("?", "").replace(",", "").lower()

def get_most_similar_faq(new_question):
    faq_questions = []
    faq_id = []
    for i in range(len(FAQ_QA)):
        for j in range(len(FAQ_QA[i][0])):
            faq_questions.append(only_words_str(FAQ_QA[i][0][j]))
            faq_id.append((i, j))
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(faq_questions)
    new_question_vector = vectorizer.transform([only_words_str(new_question)])
    similarity_scores = cosine_similarity(new_question_vector, question_vectors).flatten()
    sort_id = []
    for i, score in enumerate(similarity_scores):
        sort_id.append((-score, faq_id[i][0], faq_id[i][1]))
    sort_id.sort()
    i1, j1 = sort_id[0][1], sort_id[0][2]
    x = 1
    i2, j2 = sort_id[x][1], sort_id[x][2]
    while i2 == i1:
        x += 1
        i2, j2 = sort_id[x][1], sort_id[x][2]
    return (FAQ_QA[i1][0][j1], FAQ_QA[i1][1]), (FAQ_QA[i2][0][j2], FAQ_QA[i2][1])