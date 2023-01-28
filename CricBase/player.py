import json
import datetime
class Player:
    def __init__(self, PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID):
        self.PlayerID = PlayerID
        self.FName = FName
        self.LName = LName
        self.DOB = DOB
        self.PrimarySkill = PrimarySkill
        self.SecondarySkill = SecondarySkill
        self.BowlingArm = BowlingArm
        self.BattingHand = BattingHand
        self.TeamID = TeamID
        self.DebutID = DebutID

    @staticmethod
    def from_database_row(row):
        return Player(*row)

    @staticmethod
    def to_database_row(player):
        return (player.PlayerID, player.FName, player.LName, player.DOB, player.PrimarySkill, player.SecondarySkill, player.BowlingArm, player.BattingHand, player.TeamID, player.DebutID)

    @staticmethod
    def from_json(json_string):
        #data = json.loads(json_string)
        return Player(**json_string)

    
    def json_default(self,value):
        if isinstance(value,datetime.date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__


    def to_json(self):
        return json.dumps(self, default=self.json_default, sort_keys=False, indent=4)

    @staticmethod
    def read_from_database(conn, player_id):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM PLAYER WHERE PlayerID=%s', (player_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Player.from_database_row(row)

    @staticmethod
    def write_to_database(conn, player):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO PLAYER (PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                       Player.to_database_row(player))
        conn.commit()

    @staticmethod
    def delete_from_database(conn, player_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM PLAYER WHERE PlayerID=%s', (player_id,))
        conn.commit()