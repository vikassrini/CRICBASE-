import json

class PlayerSummary():
    def __init__(self, PlayerID, FName, LName, TeamID, Matches, Innings, Runs, Balls, Average, StrikeRate, Overs, RunsConceded, Wickets, Maidens, BowlingAverage, BowlingStrikeRate, Catches, RunOuts, Stumpings):
        self.PlayerID = PlayerID
        self.FName = FName
        self.LName = LName
        self.TeamID = TeamID
        self.Matches = Matches
        self.Innings = Innings
        self.Runs = Runs
        self.Balls = Balls
        self.Average = Average
        self.StrikeRate = StrikeRate
        self.Overs = Overs
        self.RunsConceded = RunsConceded
        self.Wickets = Wickets
        self.Maidens = Maidens
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

