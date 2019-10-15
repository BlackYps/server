import logging

from server.abc.base_game import InitMode
from server.players import Player
from server.leagues import Leagues

from .game import Game, GameOutcome, ValidityState
from server.rating import RatingType

logger = logging.getLogger(__name__)


class LadderGame(Game):
    """Class for 1v1 ladder games"""
    init_mode = InitMode.AUTO_LOBBY

    def __init__(self, id_, *args, **kwargs):
        super(self.__class__, self).__init__(id_, *args, **kwargs)
        self.game_mode = 'ladder1v1'
        self.max_players = 2

    async def rate_game(self):
        if self.validity == ValidityState.VALID:
            new_ratings = self.compute_rating(RatingType.LADDER_1V1)
            await self.persist_rating_change_stats(new_ratings, RatingType.LADDER_1V1)
            await self.update_division_scores()

    async def update_division_scores(self):
        scores = []
        for player in self.players:
            army = self.get_player_option(player.id, 'Army')
            try:
                scores.append(self.get_army_score(army))
            except KeyError:
                return

        if scores[0] > scores[1]:
            # first player won
            await Leagues.calculate_new_divisions(self.players[0], 1)
            await Leagues.calculate_new_divisions(self.players[1], -1)
        elif scores[0] < scores[1]:
            # second player won
            await Leagues.calculate_new_divisions(self.players[0], 1)
            await Leagues.calculate_new_divisions(self.players[1], -1)
        else:
            # draw
            await Leagues.calculate_new_divisions(self.players[0], 0)
            await Leagues.calculate_new_divisions(self.players[1], 0)

    def is_winner(self, player: Player):
        return self.outcome(player) == GameOutcome.VICTORY

    def get_army_score(self, army: int) -> int:
        """
        We override this function so that ladder game scores are only reported
        as 1 for win and 0 for anything else.
        """
        for result in self._results.get(army, []):
            if result[1] == 'victory':
                return 1
        return 0
