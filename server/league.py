

class Season:

    max_division = 21

    def __init__(
            self,
            season_number: int,
    ):
        self.season_number = season_number


class League:

    def __init__(
        self,
        division: int,
        score: int,
        game_count: int,
    ):
        self.division = division
        self.score = score
        self.game_count = game_count

    def update_division_scores(self, result: int,  rating: int):
        self.game_count += 1

        if self.game_count > 6 and self.division == 0:
            self.place_player(rating)
        elif self.game_count > 6:
            if result == 1:
                if (rating / 100 + 3) > self.division and self.division < Season.max_division:
                    boost = 1
                else:
                    boost = 0
                self.score += 1 + boost
            elif result == -1:
                self.score -= 1
            self.update_divisions()

    def update_divisions(self):
        if self.score >= 10 and self.division < Season.max_division:
            self.division += 1
            self.score = 2
        if self.score < 0:
            if self.division > 1:
                self.division -= 1
                self.score = 8
            else:
                self.score = 0

    def place_player(self, rating: int):
        if rating > 1800:
            self.division = Season.max_division
            self.score = 2
        else:
            self.division = int(rating / 100 -1)
            if self.division < 1:
                self.division = 1
            self.score = int((rating % 100) / 10)




