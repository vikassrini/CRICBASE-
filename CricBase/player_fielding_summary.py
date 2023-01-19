import json

class PlayerFieldingSummary:
    def __init__(self, PlayerID, Catches, Stumpings, RunOuts):
        self.PlayerID = PlayerID
        self.Catches = Catches
        self.Stumpings = Stumpings
        self.RunOuts = RunOuts
    
    @staticmethod
    def from_database_row(row):
        return PlayerFieldingSummary(*row)
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
    
    @staticmethod
    def read_from_database(conn, player_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PLAYER_FIELDING_SUMMARY WHERE PlayerID=%s", (player_id))
        row = cursor.fetchone()
        if row is None:
            return None
        
        return PlayerFieldingSummary.from_database_row(row)