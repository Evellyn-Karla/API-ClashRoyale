from backend.database.mongodb import get_database

class Player:
    def __init__(self, nickname, trophies, level, wins, lossses, battleCount, clan):
        self.nickname = nickname
        self.trophies = trophies
        self.level = level
        self.wins = wins
        self.losses = lossses
        self.battleCount = battleCount
        self.clan = clan

    def save_to_db(self):
        db = get_database()
        db.players.insert_one(self.__dict__)
    
    @staticmethod
    def get_player_by_tag(player_tag):
        db = get_database()
        return db.players.find_one({'tag': player_tag})
