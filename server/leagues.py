from server.players import Player


class Season:

    max_division = 21

    def __init__(
            self,
            season_number: int,
    ):
        self.season_number = season_number


class Leagues:

    def __init__(
        self,
        division: int = 0,
        score: int = 0,
        game_count: int = 0,
    ):
        self.division = division
        self.score = score
        self.game_count = game_count

    def promote_player(self):
        if self.division < Season.max_division:
            self.division += 1
            self.score = 2

    def demote_player(self):
        if self.division > 1:
            self.division -= 1
            self.score = 8
        else:
            self.score = 0

    def calculate_new_divisions(self, player: Player, result: int):
        self.game_count += 1

        if self.game_count > 6:
            if result == 1:
                if self.score > 9:
                    self.promote_player()
                else:
                    self.score += 1
            elif result == -1:
                if self.score < 1:
                    self.demote_player()
                else:
                    self.score -= 1
        elif self.game_count == 6:
            self.place_player(player)
        else:
            if result == 1:
                self.score += 1
            if result == -1:
                if self.score < 1:
                    self.score = 0
                else:
                    self.score -= 1

    def place_player(self, player: Player):
        rating = player.ratings             # probably not correct
        if rating > 1800:
            self.division = Season.max_division
            self.score += 2
        else:
            self.division = int(rating / 100 -1)
            if self.division < 1:
                self.division = 1
            self.score = int((rating % 100) / 10)




