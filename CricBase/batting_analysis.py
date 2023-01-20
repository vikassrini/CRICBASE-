import json
import pymysql

class BattingAnalysis:
    def __init__(self, PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes):
        self.PlayerID = PlayerID
        self.MatchID = MatchID
        self.TeamID = TeamID
        self.BallsFaced = BallsFaced
        self.RunsScored = RunsScored
        self.DismissalStatus = DismissalStatus
        self.Fours = Fours
        self.Sixes = Sixes

    @staticmethod
    def from_database_row(row):
        return BattingAnalysis(*row)

    @staticmethod
    def to_database_row(analysis):
        return (analysis.PlayerID, analysis.MatchID, analysis.TeamID, analysis.BallsFaced, analysis.RunsScored, analysis.DismissalStatus, analysis.Fours, analysis.Sixes)


    @staticmethod
    def from_json(json_string):
        #data = json.loads(json_string)
        return BattingAnalysis(**json_string)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    @staticmethod
    def read_from_database(conn, player_id, match_id, team_id):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BATTING_ANALYSIS WHERE PlayerID=%s AND MatchID=%s AND TeamID=%s', (player_id, match_id, team_id))
        row = cursor.fetchone()
        if row is None:
            return None
        return BattingAnalysis.from_database_row(row)

    @staticmethod
    def write_to_database(conn, analysis):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO BATTING_ANALYSIS (PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                       BattingAnalysis.to_database_row(analysis))
        conn.commit()

    @staticmethod
    def delete_from_database(conn, player_id, match_id, team_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BATTING_ANALYSIS WHERE PlayerID=%s AND MatchID=%s AND TeamID=%s', (player_id, match_id, team_id))
        conn.commit()
