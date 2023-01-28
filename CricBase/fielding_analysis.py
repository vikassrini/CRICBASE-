import json
import pymysql

class FieldingAnalysis:
    def __init__(self, PlayerID, MatchID, TeamID, Catches, Stumpings, RunOuts):
        self.PlayerID = PlayerID
        self.MatchID = MatchID
        self.TeamID = TeamID
        self.Catches = Catches
        self.Stumpings = Stumpings
        self.RunOuts = RunOuts

    @staticmethod
    def from_database_row(row):
        return FieldingAnalysis(*row)

    @staticmethod
    def to_database_row(analysis):
        return (analysis.PlayerID, analysis.MatchID, analysis.TeamID, analysis.Catches, analysis.Stumpings, analysis.RunOuts)

    @staticmethod
    def from_json(json_string):
        #data = json.loads(json_string)
        return FieldingAnalysis(**json_string)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    @staticmethod
    def read_from_database(conn, player_id, match_id, team_id):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM FIELDING_ANALYSIS WHERE PlayerID=%s AND MatchID=%s AND TeamID=%s', (player_id, match_id, team_id))
        row = cursor.fetchone()
        if row is None:
            return None
        return FieldingAnalysis.from_database_row(row)

    @staticmethod
    def write_to_database(conn, analysis):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO FIELDING_ANALYSIS (PlayerID, MatchID, TeamID, Catches, Stumpings, RunOuts) VALUES (%s, %s, %s, %s, %s, %s)',
                        FieldingAnalysis.to_database_row(analysis))
        conn.commit()

    @staticmethod
    def delete_from_database(conn, player_id, match_id, team_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM FIELDING_ANALYSIS WHERE PlayerID=%s AND MatchID=%s AND TeamID=%s', (player_id, match_id, team_id))
        conn.commit()