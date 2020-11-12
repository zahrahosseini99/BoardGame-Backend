from game.models import game
from boardgamegeek import BGGClient


def run():
    bgg = BGGClient()
    game_ids = list(range(20))
    games = bgg.game_list(game_ids)
    for g in games:
        obj = game.objects.create(id=g.id,
                                  name=g.name,
                                  description=g.description,
                                  category=g.categories,
                                  image=g.image,
                                  min_players=g.min_players,
                                  max_players=g.max_players,
                                  difficulty=g.rating_average_weight,
                                  rate=g.rating_average)
        obj.save()
