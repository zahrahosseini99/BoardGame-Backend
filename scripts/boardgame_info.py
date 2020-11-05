# scripts/delete_all_questions.py

from game.models import game
from boardgamegeek import BGGClient

def run():
    # Fetch all questions
    bgg = BGGClient()
    game_ids = list(range(20))
    games = bgg.game_list(game_ids)
    for g in games:
        print("************************************",g.name)
        obj = game.objects.create(name=g.name,
        description=g.description,
        category=g.categories,
        images=g.image,
        min_players=g.min_players,
        max_players=g.max_players)
        obj.save()
    # Delete questions
    #print(game.objects.all())

    """
    from boardgamegeek import BGGClient

bgg = BGGClient()
g = bgg.game("Android: Netrunner")

lis = list(range(1000))
# print(lis)

games = bgg.game_list(lis)

# Desc .description
# Image .image
# Name .name
# Genre .categories
# Min_player .min_players - .max_players
# Difficulty .rating_average_weight


for g in games:
# print('_'*10)
print(g.name)
# print('_'*10)
    """