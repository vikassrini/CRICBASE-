import json
from player import Player
from batting_analysis import BattingAnalysis
from bowling_analysis import BowlingAnalysis
import datetime
class PlayerSummary(Player):
    def __init__(self, PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID, Matches, Runs, Average, StrikeRate, Overs, Wickets, BowlingAverage, BowlingStrikeRate):
        super().__init__(PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID)
        self.Matches = Matches
        self.Runs = Runs
        self.Average = Average
        self.StrikeRate = StrikeRate
        self.Overs = Overs
        self.Wickets = Wickets
        self.BowlingAverage = BowlingAverage
        self.BowlingStrikeRate = BowlingStrikeRate
    
    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return PlayerSummary(**data)
    
    def json_default(self,value):
        if isinstance(value,datetime.date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

    def to_json(self):
        return json.dumps(self, default=self.json_default, sort_keys=True, indent=4)
    
    @staticmethod
    def read_from_database(conn, player_id):
        player = Player.read_from_database(conn, player_id)
        Matches = 0
        Runs = 0
        ballsFaced = 0
        notOuts = 0

        for row in BattingAnalysis.read_from_database(conn, player_id):
            Matches += 1
            Runs += row[4]
            ballsFaced += row[3]
            if(row[5] == 'DNB' or row[5] == "NOT OUT"):
                notOuts += 1
            
        Average = Runs/(Matches - notOuts)
        StrikeRate = Runs/ballsFaced
        print(Average,StrikeRate)
        Overs = 0
        Wickets = 0
        RunsConceded = 0
         
        for row in BowlingAnalysis.read_from_database(conn, player_id):
            print(row)
            Overs += row[3]
            RunsConceded += row[4]
            Wickets += row[6]
        try:
            BowlingAverage = RunsConceded/Wickets
            BowlingStrikeRate = Wickets/(Overs * 6)
        except:
            BowlingAverage = 0.0
            BowlingStrikeRate = 0.0



        
        playerSummary = PlayerSummary(player_id, player.FName, player.LName, player.DOB,player.PrimarySkill, player.SecondarySkill, player.BowlingArm, player.BattingHand,player.TeamID, player.DebutID, Matches,Runs, Average, StrikeRate, Overs, Wickets, BowlingAverage, BowlingStrikeRate)
        
        return playerSummary