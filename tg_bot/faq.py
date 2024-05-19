from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

faq_qa = [
    (("Узнать свой риск рака груди", "Как узнать вероятность рака груди у меня"), "В этом калькуляторе вы можете узнать свой риск рака груди: https://www.dalshefond.ru/check/"),
    (("Подозрение на рак", "Обратится к онкологу"), "Персональное обращение к онкологу: https://vmesteplus.ru/personal/personalized-help/oncologist/"),
    (("Пособие по профилактике", "Как сохранить здоровье груди"), "Пособие по профилактике, https://dalshefond.ru/prevention-manual/"),
    (("Как рак груди лечится", "Лечение рака молочный железы"), "Онлайн курс 'Что важно знать о раке молочной железы': https://vmesteplus.ru/distance-programs/oncologist-course/"),
    (("Получить консультацию медицинского юриста"), "Консультация медицинского юриста: https://vmesteplus.ru/personal/personalized-help/lawyer/"),
    (("Групповая психотерапия"), "Консультация медицинского юриста: https://vmesteplus.ru/personal/personalized-help/lawyer/"),
]
def only_words_str(s):
    return s.replace("?", "").replace(",", "").lower()

def get_most_similar_faq(new_question):
    faq_questions = []
    faq_id = []
    for i in range(len(faq_qa)):
        for j in range(len(faq_qa[i][0])):
            faq_questions.append(only_words_str(faq_qa[i][0][j]))
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
    return (faq_qa[i1][0][j1], faq_qa[i1][1]), (faq_qa[i2][0][j2], faq_qa[i2][1])