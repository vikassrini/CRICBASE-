import json

class PlayerBowlingSummary:
    def __init__(self, PlayerID, OversBowled, RunsConceded, Wickets, Maidens, BowlingAverage, BowlingStrikeRate):
        self.PlayerID = PlayerID
        self.OversBowled = OversBowled
        self.Wickets = Wickets
        self.Maidens = Maidens
        self.RunsConceded = RunsConceded
        self.BowlingAverage = BowlingAverage
        self.BowlingStrikeRate = BowlingStrikeRate

    @staticmethod
    def from_database_row(row):
        return PlayerBowlingSummary(*row)

    def to_json(self):
        return json.dumps(self, default= lambda o: o.__dict__, sort_keys=False, indent=4)
    
    @staticmethod
    def read_from_database(conn, player_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PLAYER_BOWLING_SUMMARY WHERE PlayerID=%s", (player_id))
        row = cursor.fetchone()
        if row is None:
            return None
        
        return PlayerBowlingSummary.from_database_row(row)
