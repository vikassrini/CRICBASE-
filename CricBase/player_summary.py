import json

from player import Player

class PlayerSummary(Player):
    def __init__(self, PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID, Matches, Runs, Average, StrikeRate, Overs, Wickets, BowlingAverage, BowlingStrikeRate, Catches: int = 0 , RunOuts: int = 0, Stumpings: int = 0):
        super().__init__(PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID)
        self.Matches = Matches
        self.Runs = Runs
        self.Average = Average
        self.StrikeRate = StrikeRate
        self.Overs = Overs
        self.Wickets = Wickets
        self.BowlingAverage = BowlingAverage
        self.BowlingStrikeRate = BowlingStrikeRate
        self.Catches = Catches
        self.RunOuts = RunOuts
        self.Stumpings = Stumpings


    @staticmethod
    def from_database_row(row):
        return PlayerSummary(*row)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    @staticmethod
    def read_from_database(conn, player_id):
        cursor = conn.cursor()
        cursor.callproc('get_player_summary', (player_id,))
        row = cursor.fetchone()
        return PlayerSummary.from_database_row(row)

