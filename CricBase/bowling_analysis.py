import json
import pymysql

class BowlingAnalysis:
    def __init__(self, PlayerID, MatchID, TeamID, OversBowled, RunsConceded, Maidens, Wickets):
        self.PlayerID = PlayerID
        self.MatchID = MatchID
        self.TeamID = TeamID
        self.OversBowled = OversBowled
        self.RunsConceded = RunsConceded
        self.Maidens = Maidens
        self.Wickets = Wickets

    @staticmethod
    def from_database_row(row):
        return BowlingAnalysis(*row)

    @staticmethod
    def to_database_row(analysis):
        return (analysis.PlayerID, analysis.MatchID, analysis.TeamID, analysis.OversBowled, analysis.RunsConceded, analysis.Maidens, analysis.Wickets)

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return BowlingAnalysis(**data)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def read_from_database(conn, player_id, match_id, team_id):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BOWLING_ANALYSIS WHERE PlayerID=%s AND MatchID=%s AND TeamID=%s', (player_id, match_id, team_id))
        row = cursor.fetchone()
        if row is None:
            return None
        return BowlingAnalysis.from_database_row(row)
    
    @staticmethod
    def write_to_database(conn, analysis):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO BOWLING_ANALYSIS (PlayerID, MatchID, TeamID, OversBowled, RunsConceded, Maidens, Wickets) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                       BowlingAnalysis.to_database_row(analysis))
        conn.commit()
    
    @staticmethod
    def delete_from_database(conn, player_id, match_id, team_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BOWLING_ANALYSIS WHERE PlayerID=%s AND MatchID=%s AND TeamID=%s', (player_id, match_id, team_id))
        conn.commit()

    @staticmethod
    def read_from_database(conn, player_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BOWLING_ANALYSIS WHERE PlayerID=%s", (player_id))
        return cursor.fetchall()
    
