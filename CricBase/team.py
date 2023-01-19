import json
import pymysql

class Team:
    def __init__(self, TeamID, Name, Division, Level):
        self.TeamID = TeamID
        self.Name = Name
        self.Division = Division
        self.Level = Level

    @staticmethod
    def from_database_row(row):
        return Team(*row)

    @staticmethod
    def to_database_row(team):
        return (team.TeamID, team.Name, team.Division, team.Level)

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return Team(**data)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    @staticmethod
    def read_from_database(conn, team_id):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM TEAM WHERE TeamID=%s', (team_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Team.from_database_row(row)

    @staticmethod
    def write_to_database(conn, team):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO TEAM (TeamID, Name, Division, Level) VALUES (%s, %s, %s, %s)', Team.to_database_row(team))
        conn.commit()

    @staticmethod
    def delete_from_database(conn, team_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM TEAM WHERE TeamID=%s', (team_id,))
        conn.commit()
