# recommendations/recommendations.py
from concurrent import futures
import random
import grpc
from recommendations_pb2 import (
 BookCategory,
 BookRecommendation,
 RecommendationResponse,
)
import recommendations_pb2_grpc
books_by_category = {
 BookCategory.MYSTERY: [
 BookRecommendation(id=1, title=    "Мальтийский сокол"),
 BookRecommendation(id=2, title=    "Убийство в Восточном экспрессе"),
 BookRecommendation(id=3, title=    "Собака Баскервилей"),
 BookRecommendation(id=4, title=    "Автостопом по галактике"),
 BookRecommendation(id=5, title=    "Игра Эндера"),
 BookRecommendation(id=6, title=    "Сто имен"),
 BookRecommendation(id=7, title=    "Книга духов"),
 BookRecommendation(id=8, title=    "Дети зимы"),
 BookRecommendation(id=9, title=    "The Sandman. Песочный человек. Книга 2. Кукольный домик"),
 BookRecommendation(id=10, title=   "Ошибка Ведьмака"),
 ],
 BookCategory.SCIENCE_FICTION: [
 BookRecommendation(id=11, title=   "Дюна"),
 BookRecommendation(id=12, title=   "Кристалл Альвандера"),
 BookRecommendation(id=13, title=   "Форпост. Найди и убей"),
 BookRecommendation(id=14, title=   "Стоя на краю"),
 BookRecommendation(id=15, title=   "Большая охота"),
 BookRecommendation(id=16, title=   "Возвращение Астровитянки"),
 BookRecommendation(id=17, title=   "Поле боя"),
 BookRecommendation(id=18, title=   "Страна багровых туч"),
 BookRecommendation(id=19, title=   "Эффект энтропии"),
 BookRecommendation(id=20, title=   "Синий реванш"),
 ],
 BookCategory.SELF_HELP: [
 BookRecommendation(id=21, title=   "Семь навыков высокоэффективных людей"),
 BookRecommendation(id=22, title=   "Как завоёвывать друзей и оказывать влияние на людей"),
 BookRecommendation(id=23, title=   "Человек в поисках смысла"),
 BookRecommendation(id=24, title=   "Экономика для «чайников»"),
 BookRecommendation(id=25, title=   "Самый богатый человек в Вавилоне"),
 BookRecommendation(id=26, title=   "Футболономика. Почему Англия проигрывает, Германия и Бразилия выигрывают, а США, Япония, Австралия, Турция и даже Ирак выходят на первый план"),
 BookRecommendation(id=27, title=   "НЛП для бизнеса и жизни: искусство гипнотического убеждения"),
 BookRecommendation(id=28, title=   "Лидер без титула. Современная притча об истинном успехе"),
 BookRecommendation(id=29, title=   "Дао Жизни"),
 BookRecommendation(id=30, title=   "Достижение максимума. Стратегии и навыки, которые разбудят ваши скрытые силы и помогут вам достичь успеха"),
 ],
}
class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):

 def Recommend(self, request, context):
  if request.category not in books_by_category:
   context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
  books_for_category = books_by_category[request.category]
  num_results = min(request.max_results, len(books_for_category))
  books_to_recommend = random.sample(books_for_category, num_results)

  return RecommendationResponse(recommendations=books_to_recommend)
def serve():
 server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
 recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
 RecommendationService(), server
 )
 server.add_insecure_port("[::]:50051")
 server.start()
 server.wait_for_termination()
if __name__ == "__main__":
 serve()
