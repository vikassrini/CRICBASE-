import json
import pymysql

class Tournament:
    def __init__(self, TournamentID, TournamentName, StartYear, Level, EndYear):
        self.TournamentID = TournamentID
        self.TournamentName = TournamentName
        self.StartYear = StartYear
        self.Level = Level
        self.EndYear = EndYear

    @staticmethod
    def from_database_row(row):
        return Tournament(*row)

    @staticmethod
    def to_database_row(tournament):
        return (tournament.TournamentID, tournament.TournamentName, tournament.StartYear, tournament.Level, tournament.EndYear)

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return Tournament(**data)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def read_from_database(conn, tournament_id):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM TOURNAMENT WHERE TournamentID=%s', (tournament_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Tournament.from_database_row(row)

    @staticmethod
    def write_to_database(conn, tournament):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO TOURNAMENT (TournamentID, TournamentName, StartYear, Level, EndYear) VALUES (%s, %s, %s, %s, %s)', Tournament.to_database_row(tournament))
        conn.commit()

    @staticmethod
    def delete_from_database(conn, tournament_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM TOURNAMENT WHERE TournamentID=%s', (tournament_id,))
        conn.commit()
