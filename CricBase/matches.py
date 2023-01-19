import json
import datetime

class Match:
    def __init__(self, MatchID, TournamentID, TeamID1, TeamID2, Venue, Date):
        self.MatchID = MatchID
        self.TournamentID = TournamentID
        self.TeamID1 = TeamID1
        self.TeamID2 = TeamID2
        self.Venue = Venue
        self.Date = Date

    @staticmethod
    def from_database_row(row):
        return Match(*row)

    @staticmethod
    def to_database_row(match):
        return (match.MatchID, match.TournamentID, match.TeamID1, match.TeamID2, match.Venue, match.Date)

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return Match(**data)

    def json_default(self,value):
        if isinstance(value,datetime.date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

    def to_json(self):
        return json.dumps(self, default=self.json_default, sort_keys=False, indent=4)

    @staticmethod
    def read_from_database(conn, match_id):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM MATCHES WHERE MatchID=%s', (match_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Match.from_database_row(row)

    @staticmethod
    def write_to_database(conn, match):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO MATCHES (MatchID, TournamentID, TeamID1, TeamID2, Venue, Date) VALUES (%s, %s, %s, %s, %s, %s)', Match.to_database_row(match))
        conn.commit()

    @staticmethod
    def delete_from_database(conn, match_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM MATCHES WHERE MatchID=%s', (match_id,))
        conn.commit()
