import json
import pymysql

class Dismissal:
    def __init__(self, MatchID, BatterID, BowlerID, FielderID, NatureOfDismissal):
        self.MatchID = MatchID
        self.BatterID = BatterID
        self.BowlerID = BowlerID
        self.FielderID = FielderID
        self.NatureOfDismissal = NatureOfDismissal

    @staticmethod
    def from_database_row(row):
        return Dismissal(*row)

    @staticmethod
    def to_database_row(dismissal):
        return (dismissal.MatchID, dismissal.BatterID, dismissal.BowlerID, dismissal.FielderID, dismissal.NatureOfDismissal)

    @staticmethod
    def from_json(json_string):
        #data = json.loads(json_string)
        return Dismissal(**json_string)

    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)

    @staticmethod
    def read_from_database(conn, match_id, batter_id):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM DISMISSAL WHERE MatchID=%s AND BatterID=%s', (match_id, batter_id))
        row = cursor.fetchone()
        if row is None:
            return None
        return Dismissal.from_database_row(row)

    @staticmethod
    def write_to_database(conn, dismissal):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO DISMISSAL (MatchID, BatterID, BowlerID, FielderID, NatureOfDismissal) VALUES (%s, %s, %s, %s,%s)',
                        Dismissal.to_database_row(dismissal=dismissal))
        conn.commit()


    @staticmethod
    def delete_from_database(conn, match_id, batter_id):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM DISMISSAL WHERE MatchID=%s AND BatterID=%s', (match_id, batter_id))
        conn.commit()
