import json

class PlayerBattingSummary:
    def __init__(self, PlayerID, Matches, Innings, NotOuts, Runs, Balls, Average, StrikeRate):
        self.PlayerID = PlayerID
        self.Matches = Matches
        self.Innings = Innings
        self.NotOuts = NotOuts
        self.Runs = Runs
        self.Balls = Balls
        self.Average = Average
        self.StrikeRate = StrikeRate

    @staticmethod
    def from_database_row(row):
        return PlayerBattingSummary(*row)
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
    
    @staticmethod
    def read_from_database(conn, player_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PLAYER_BATTING_SUMMARY WHERE PlayerID=%s", (player_id))
        row = cursor.fetchone()
        if row is None:
            return None
        
        return PlayerBattingSummary.from_database_row(row)

    
