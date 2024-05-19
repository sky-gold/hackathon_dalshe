from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

faq_qa = [
    (("Узнать свой риск рака груди", "Как узнать вероятность рака груди у меня"), "В этом калькуляторе вы можете узнать свой риск рака груди: https://www.dalshefond.ru/check/"),
    (("Подозрение на рак"), "Персональное обращение к онкологу: https://vmesteplus.ru/personal/personalized-help/oncologist/"),
    (("Пособие по профилактике", "Как сохранить здоровье груди"), "Пособие по профилактике, https://dalshefond.ru/prevention-manual/"),
]

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_most_similar_faq(new_question):
    faq_questions = []
    faq_id = []
    for i in range(len(faq_qa)):
        for j in range(len(faq_qa[i][0])):
            faq_questions.append(faq_qa[i][0][j].lower())
            faq_id.append((i, j))
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(faq_questions)
    new_question_vector = vectorizer.transform([new_question])
    similarity_scores = cosine_similarity(new_question_vector, question_vectors).flatten()
    sort_id = []
    for i, score in enumerate(similarity_scores):
        sort_id.append((-score, faq_id[i][0], faq_id[i][1]))
    sort_id.sort()
    i1, j1 = sort_id[0][1], sort_id[0][2]
    i2, j2 = sort_id[1][1], sort_id[1][2]
    return (faq_qa[i1][0][j1], faq_qa[i1][1]), (faq_qa[i2][0][j2], faq_qa[i2][1])