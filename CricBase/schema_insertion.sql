CREATE TABLE TOURNAMENT (
  TournamentID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  TournamentName VARCHAR(255) NOT NULL,
  StartYear INTEGER,
  Grade VARCHAR(255) NOT NULL,
  EndYear INTEGER
);

CREATE TABLE TEAM (
  TeamID INTEGER PRIMARY KEY AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  Division VARCHAR(255) NOT NULL,
  Grade VARCHAR(255) NOT NULL
);

CREATE TABLE MATCHES(
  MatchID INTEGER PRIMARY KEY AUTO_INCREMENT,
  TournamentID INTEGER NOT NULL,
  TeamID1 INTEGER NOT NULL,
  TeamID2 INTEGER NOT NULL,
  Venue VARCHAR(255),
  DatePlayed DATE NOT NULL,
  FOREIGN KEY (TournamentID) REFERENCES TOURNAMENT(TournamentID) ON DELETE CASCADE,
  FOREIGN KEY (TeamID1) REFERENCES TEAM(TeamID) ON DELETE CASCADE,
  FOREIGN KEY (TeamID2) REFERENCES TEAM(TeamID) ON DELETE CASCADE
);


CREATE TABLE PLAYER (
  PlayerID INTEGER PRIMARY KEY AUTO_INCREMENT,
  FName VARCHAR(255) NOT NULL,
  LName VARCHAR(255),
  DOB DATE NOT NULL,
  PrimarySkill VARCHAR(255) NOT NULL,
  SecondarySkill VARCHAR(255),
  BowlingArm VARCHAR(255),
  BattingHand VARCHAR(255) NOT NULL,
  TeamID INTEGER NOT NULL,
  DebutID INTEGER NOT NULL,
  FOREIGN KEY (TeamID) REFERENCES TEAM (TeamID) ON DELETE CASCADE,
  FOREIGN KEY (DebutID) REFERENCES MATCHES (MatchID) ON DELETE CASCADE
);

CREATE TABLE BATTING_ANALYSIS (
  PlayerID INTEGER,
  MatchID INTEGER,
  TeamID INTEGER,
  BallsFaced INTEGER NOT NULL DEFAULT 0,
  RunsScored INTEGER NOT NULL DEFAULT 0,
  DismissalStatus VARCHAR(6) NOT NULL DEFAULT 'DNB',
  Fours INTEGER NOT NULL DEFAULT 0,
  Sixes INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (PlayerID, MatchID, TeamID),
  FOREIGN KEY (PlayerID) REFERENCES PLAYER (PlayerID) ON DELETE CASCADE,
  FOREIGN KEY (MatchID) REFERENCES MATCHES (MatchID) ON DELETE CASCADE,
  FOREIGN KEY (TeamID) REFERENCES TEAM (TeamID) ON DELETE CASCADE
);



CREATE TABLE BOWLING_ANALYSIS (
  PlayerID INTEGER,
  MatchID INTEGER,
  TeamID INTEGER,
  OversBowled INTEGER NOT NULL DEFAULT 0,
  RunsConceded INTEGER NOT NULL DEFAULT 0,
  Maidens INTEGER NOT NULL DEFAULT 0,
  Wickets INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (PlayerID, MatchID, TeamID),
  FOREIGN KEY (PlayerID) REFERENCES PLAYER (PlayerID) ON DELETE CASCADE,
  FOREIGN KEY (MatchID) REFERENCES MATCHES (MatchID) ON DELETE CASCADE,
  FOREIGN KEY (TeamID) REFERENCES TEAM (TeamID) ON DELETE CASCADE
);

CREATE TABLE FIELDING_ANALYSIS (
  PlayerID INTEGER,
  MatchID INTEGER,
  TeamID INTEGER,
  Catches INTEGER NOT NULL DEFAULT 0,
  Stumpings INTEGER NOT NULL DEFAULT 0,
  RunOuts INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (PlayerID, MatchID, TeamID),
  FOREIGN KEY (PlayerID) REFERENCES PLAYER (PlayerID) ON DELETE CASCADE,
  FOREIGN KEY (MatchID) REFERENCES MATCHES(MatchID) ON DELETE CASCADE,
  FOREIGN KEY (TeamID) REFERENCES TEAM (TeamID) ON DELETE CASCADE
);




CREATE TABLE DISMISSAL (
  MatchID INTEGER,
  BatterID INTEGER,
  BowlerID INTEGER NOT NULL,
  FielderID INTEGER NOT NULL,
  NatureOfDismissal VARCHAR(255) NOT NULL,
  PRIMARY KEY (MatchID, BatterID),
  FOREIGN KEY (MatchID) REFERENCES MATCHES(MatchID) ON DELETE CASCADE,
  FOREIGN KEY (BatterID) REFERENCES PLAYER (PlayerID) ON DELETE CASCADE,
  FOREIGN KEY (BowlerID) REFERENCES PLAYER (PlayerID) ON DELETE CASCADE,
  FOREIGN KEY (FielderID) REFERENCES PLAYER (PlayerID) ON DELETE CASCADE
);

CREATE TABLE PLAYER_BATTING_SUMMARY (
  PlayerID INTEGER,
  Matches INTEGER,
  Innings INTEGER,
  NotOuts INTEGER,
  Runs INTEGER,
  Balls INTEGER,
  Average FLOAT,
  StrikeRate FLOAT,
  PRIMARY KEY(PlayerID),
  FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID) ON DELETE CASCADE
);

CREATE TABLE PLAYER_BOWLING_SUMMARY (
  PlayerID INTEGER,
  Overs INTEGER,
  RunsConceded INTEGER,
  Wickets INTEGER,
  Maidens INTEGER,
  BowlingAverage FLOAT,
  BowlingStrikeRate FLOAT,
  PRIMARY KEY(PlayerID),
  FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID) ON DELETE CASCADE
);

CREATE TABLE PLAYER_FIELDING_SUMMARY (
  PlayerID INTEGER,
  Catches INTEGER,
  RunOuts INTEGER,
  Stumpings INTEGER,
  PRIMARY KEY(PlayerID),
  FOREIGN KEY (PlayerID) REFERENCES PLAYER(PlayerID) ON DELETE CASCADE
);

DELIMITER $$
CREATE TRIGGER update_player_batting_summary AFTER INSERT ON BATTING_ANALYSIS
FOR EACH ROW
BEGIN

        DECLARE runs INT;
        DECLARE matches INT;
        DECLARE average FLOAT;
        DECLARE strikeRate FLOAT;
        DECLARE innings INT;
        DECLARE notOuts INT;
        DECLARE balls INT;
        DECLARE dismissed INT;

        SELECT COUNT(MatchID) INTO matches FROM BATTING_ANALYSIS b where b.PlayerID=NEW.PlayerID;

        IF NEW.DismissalStatus != 'DNB' THEN
            SELECT SUM(RunsScored) INTO runs FROM BATTING_ANALYSIS b where b.PlayerID=NEW.PlayerID;
            SELECT COUNT(MatchID) INTO innings FROM BATTING_ANALYSIS b where b.PlayerID=NEW.PlayerID and b.DismissalStatus!='DNB';
            SELECT COUNT(MatchID) INTO notOuts FROM BATTING_ANALYSIS b where b.PlayerID=NEW.PlayerID and b.DismissalStatus='NOTOUT';
            SELECT SUM(BallsFaced) INTO balls FROM BATTING_ANALYSIS b where b.PlayerID=NEW.PlayerID;
            SELECT COUNT(MatchID) INTO dismissed FROM BATTING_ANALYSIS b where b.PlayerID=NEW.PlayerID and b.DismissalStatus='OUT';

            IF innings = 0 THEN
                SET average = NULL;
            ELSEIF dismissed = 0 THEN
                SET average = NULL;
            ELSE
                SET average = runs/dismissed;
            END IF;

            SET strikeRate = runs*100/balls;

            IF EXISTS(SELECT * FROM PLAYER_BATTING_SUMMARY WHERE PlayerID = NEW.PlayerID) THEN
                UPDATE PLAYER_BATTING_SUMMARY
                SET Runs = runs, Balls = balls, Matches = matches, Innings = innings, NotOuts = notOuts, Average = average, StrikeRate = strikeRate
                WHERE PlayerID=NEW.PlayerID;
            ELSE
                INSERT INTO PLAYER_BATTING_SUMMARY (PlayerID, Matches, Innings, NotOuts, Runs, Balls, Average, StrikeRate) VALUES (NEW.PlayerID, matches, innings, notOuts, runs, balls, average, strikeRate);
            END IF;
        ELSEIF EXISTS(SELECT * FROM PLAYER_BATTING_SUMMARY WHERE PlayerID = NEW.PlayerID) THEN
            UPDATE PLAYER_BATTING_SUMMARY SET Matches = matches where PlayerID = NEW.PlayerID;
        ELSE
            INSERT INTO PLAYER_BATTING_SUMMARY (PlayerID, Matches, Innings, NotOuts, Runs, Balls, Average, StrikeRate) VALUES (NEW.PlayerID, 1, 0, 0, 0, 0, 0.0, 0.0);
        END IF;
END $$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER update_bowling_summary
AFTER INSERT ON BOWLING_ANALYSIS
FOR EACH ROW
BEGIN

    IF EXISTS(SELECT * FROM PLAYER_BOWLING_SUMMARY WHERE PlayerID = NEW.PlayerID) THEN
        UPDATE PLAYER_BOWLING_SUMMARY
        SET Overs = Overs + NEW.OversBowled,
            Maidens = Maidens + NEW.Maidens,
            Wickets = Wickets + NEW.Wickets,
            RunsConceded = RunsConceded + NEW.RunsConceded
        WHERE PlayerID = NEW.PlayerID;

        UPDATE PLAYER_BOWLING_SUMMARY
        SET BowlingAverage = CASE
            WHEN Wickets = 0 THEN NULL
            ELSE RunsConceded/Wickets
            END
        WHERE PlayerID = NEW.PlayerID;

        UPDATE player_bowling_summary
        SET BowlingStrikeRate = CASE
            WHEN Wickets = 0 THEN NULL
            ELSE Overs*6/Wickets
            END
        WHERE PlayerID = NEW.PlayerID;

    ELSEIF NEW.Wickets != 0 THEN
        INSERT INTO PLAYER_BOWLING_SUMMARY (PlayerID, Overs, RunsConceded, Wickets, Maidens, BowlingAverage, BowlingStrikeRate)
        VALUES (NEW.PlayerID, NEW.OversBowled, NEW.RunsConceded, NEW.Wickets, NEW.Maidens,
                NEW.RunsConceded/NEW.Wickets, (NEW.OversBowled * 6)/NEW.Wickets);
    ELSE
        INSERT INTO PLAYER_BOWLING_SUMMARY (PlayerID, Overs, RunsConceded, Wickets, Maidens, BowlingAverage, BowlingStrikeRate)
                VALUES (NEW.PlayerID, NEW.OversBowled, NEW.RunsConceded, NEW.Wickets, NEW.Maidens,
                        NULL, NULL);
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER update_player_fielding_summary
AFTER INSERT ON FIELDING_ANALYSIS
FOR EACH ROW
BEGIN
    IF EXISTS(SELECT * FROM PLAYER_FIELDING_SUMMARY WHERE PlayerID = NEW.PlayerID) THEN
            UPDATE PLAYER_FIELDING_SUMMARY
            SET Catches = Catches + NEW.Catches,
                RunOuts = RunOuts + NEW.RunOuts,
                Stumpings = Stumpings + NEW.Stumpings
            WHERE PlayerID = NEW.PlayerID;
        ELSE
            INSERT INTO PLAYER_FIELDING_SUMMARY (PlayerID, Catches, RunOuts, Stumpings) VALUES (NEW.PlayerID, NEW.Catches, NEW.RunOuts, NEW.Stumpings);
    END IF;
END $$


CREATE PROCEDURE getSummary(IN player_id INT)
BEGIN
    SELECT p.PlayerID, p.FName, p.LName, p.TeamID,
    bs.Matches, bs.Innings, bs.Runs, bs.Balls, bs.Average, bs.StrikeRate,
    bw.Overs, bw.RunsConceded, bw.Wickets, bw.Maidens, bw.BowlingAverage, bw.BowlingStrikeRate,
    fs.Catches, fs.Stumpings, fs.RunOuts
    FROM PLAYER p
    JOIN PLAYER_BATTING_SUMMARY bs ON p.PlayerID = bs.PlayerID
    JOIN PLAYER_BOWLING_SUMMARY bw ON p.PlayerID = bw.PlayerID
    JOIN PLAYER_FIELDING_SUMMARY fs ON p.PlayerID = fs.PlayerID
    WHERE p.PlayerID = player_id;
END $$

DELIMITER ;


INSERT INTO TOURNAMENT VALUES (1,"FIRST DIVISION",2022, "CLUB",2022);

INSERT INTO TEAM(TeamID, Name, Division, Grade)
VALUES
(11, "VULTURES CRICKET CLUB", "1","SEMI PROFESSIONAL"),
( 12, "SWASTIK UNION CRICKET CLUB", "1","SEMI PROFESSIONAL");

INSERT INTO MATCHES(MatchID, TournamentID, TeamID1, TeamID2, Venue, DatePlayed) VALUES(111, 1,11,12, "MVIT CRICKET GROUND","2022-01-01"), (112, 1,11,12, "JSS CRICKET GROUND","2022-05-01");

INSERT INTO PLAYER(PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID)
VALUES
(1,"ISHAN","KISHAN","1995-09-09","WICKETKEEPER","BATSMAN",NULL,"L",11,111),
(2,"SHUBMAN","GILL","1995-09-09","BATSMAN",NULL,NULL,"R",11,111),
(3,"RAHUL","TRIPATHI","1995-09-09","BATSMAN",NULL,NULL,"R",11,111),
(4,"SURYAKUMAR","YADAV","1995-09-09","BATSMAN",NULL,NULL,"R",11,111),
(5,"HARDIK","PANDYA","1995-09-09","BATSMAN","FASTBOWLER","R","R",11,111),
(6,"DEEPAK","HOODA","1995-09-09","BATSMAN","OFFSPIN","R","R",11,111),
(7,"AXAR","PATEL","1995-09-09","LEFTARMSPIN","BATSMAN","L","L",11,111),
(8,"SHIVAM","MAVI","1995-09-09","FASTBOWLER","BATSMAN","R","R",11,111),
(9,"UMRAN","MALIK","1995-09-09","FASTBOWLER","BATSMAN","R","R",11,111),
(10,"YUZVENDRA","CHAHAL","1995-09-09"," LEGSPIN","BATSMAN","L","L",11,111),
(11,"ARSHDEEP","SINGH","1995-09-09","FASTBOWLER","BATSMAN","L","L",11,111),
(12,"KUSHAL","MENDIS","1995-09-09","WICKETKEEPER","BATSMAN",NULL,"L",12,111),
(13,"PATHUN","NISSANKA","1995-09-09","BATSMAN",NULL,NULL,"R",12,111),
(14,"AVISHKA","FERNANDO","1995-09-09","BATSMAN",NULL,NULL,"R",12,111),
(15,"ARAVINDA","deSILVA","1995-09-09","BATSMAN",NULL,NULL,"R",12,111),
(16,"CHARITH","ASALANKA","1995-09-09","BATSMAN","FASTBOWLER","R","R",12,111),
(17,"DIMUTH","SHANAKA","1995-09-09","BATSMAN","OFFSPIN","R","R",12,111),
(18,"WANINDU","HASARANGA","1995-09-09","LEFTARMSPIN","BATSMAN","L","L",12,111),
(19,"CHAMUTH","KARUNARATHNE","1995-09-09","FASTBOWLER","BATSMAN","R","R",12,111),
(20,"DILHARA","FERNANDO","1995-09-09","FASTBOWLER","BATSMAN","R","R",12,111),
(21,"CHAMINDA","VAAS","1995-09-09"," LEGSPIN","BATSMAN","L","L",12,111),
(22,"RANJIT","JAYASURYA","1995-09-09","FASTBOWLER","BATSMAN","L","L",12,111);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(1,111,11,2,1,"OUT",0,0),
(2,111,11, 36,46,"OUT",2,3),
(3,111,11,16,35,"OUT",5,2);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(4,111,11,51,112,"NOTOUT",7,9),
(5,111,11,4,4,"OUT",0,0),
(6,111,11,2,4,"OUT",1,0),
(7,111,12, 9,21,"NOTOUT",4,0);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(8,111,11,0,0,"DNB",0,0),
(9,111,11,0,0,"DNB",0,0),
(10,111,11,0,0,"DNB",0,0),
(11,111,11,0,0,"DNB",0,0);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(12,111,12,17,15,"OUT",3,0),
(13,111,12, 15,23,"OUT",2,2),
(14,111,12,3,1,"OUT",0,0),
(15,111,12,14,22,"OUT",2,1);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(16,111,12,14,19,"OUT",2,1),
(17,111,12,17,23,"OUT",0,2),
(18,111,12, 8,9,"OUT",1,0),
(19,111,12,2,0,"OUT",0,0);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(20,111,12,5,2,"OUT",0,0),
(21,111,12,4,9,"NOTOUT",2,0),
(22,111,12,2,1,"OUT",0,0);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(1,112,11,5,2,"OUT",0,0),
(2,112,11, 3,5,"OUT",1,0),
(3,112,11,5,5,"OUT",1,0),
(4,112,11,36,51,"OUT",3,3),
(5,112,11,12,12,"OUT",1,1),
(6,112,11,12,9,"OUT",0,0),
(7,112,11, 31,65,"OUT",3,6),
(8,112,11,15,26,"OUT",2,2),
(9,112,11,1,1,"NOTOUT",0,0);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(10,112,11,0,0,"DNB",0,0),
(11,112,11,0,0,"DNB",0,0),
(20,112,12,5,2,"DNB",0,0),
(21,112,12,4,9,"DNB",2,0),
(22,112,12,2,1,"DNB",0,0);

INSERT INTO BATTING_ANALYSIS(PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes)
VALUES
(12,112,12,31,52,"OUT",3,4),
(13,112,12, 35,33,"OUT",4,0),
(14,112,12,3,2,"OUT",0,0),
(15,112,12,6,3,"OUT",0,0),
(16,112,12,19,37,"OUT",0,4),
(17,112,12,22,56,"NOTOUT",2,6),
(18,112,12, 1,0,"OUT",0,0),
(19,112,12,10,11,"NOTOUT",1,0);


INSERT INTO BOWLING_ANALYSIS(PlayerID,MatchID,TeamID,OversBowled,RunsConceded,Maidens,Wickets)
VALUES
(5,111,11,4.0,30,0,2),
(11,111,11,2.4,20,0,3),
(8,111,11,1.0,6,0,0),
(7,111,11,3.0,19,0,1),
(9,111,11,3.0,31,0,2),
(10,111,11,3.0,30,0,2);

INSERT INTO BOWLING_ANALYSIS(PlayerID,MatchID,TeamID,OversBowled,RunsConceded,Maidens,Wickets)
VALUES
(18,111,12,4.0,55,0,2),
(19,111,12,4.0,35,1,1),
(20,111,12,4.0,48,0,0),
(21,111,12,4.0,52,0,1),
(22,111,12,4.0,36,0,1);

INSERT INTO BOWLING_ANALYSIS(PlayerID,MatchID,TeamID,OversBowled,RunsConceded,Maidens,Wickets)
VALUES
(5,112,11,2.0,13,0,0),
(11,112,11,2.0,37,0,0),
(8,112,11,4.0,53,0,0),
(7,112,11,4.0,24,0,2),
(9,112,11,4.0,48,0,3),
(10,112,11,4.0,30,0,1);

INSERT INTO BOWLING_ANALYSIS(PlayerID,MatchID,TeamID,OversBowled,RunsConceded,Maidens,Wickets)
VALUES
(18,112,12,3.0,41,0,1),
(19,112,12,4.0,41,0,1),
(20,112,12,4.0,33,0,0),
(21,112,12,4.0,22,0,2),
(22,112,12,4.0,45,0,2),
(17,112,12,1.0,40,0,2);

INSERT INTO BOWLING_ANALYSIS(PlayerID, MatchID, TeamID, OversBowled, RunsConceded, Maidens, Wickets)
VALUES
(1,111,11,0,0,0,0),
(1,112,11,0,0,0,0);

INSERT INTO BOWLING_ANALYSIS(PlayerID, MatchID, TeamID, OversBowled, RunsConceded, Maidens, Wickets)
VALUES
(2,111,11,0,0,0,0),
(2,112,11,0,0,0,0),
(3,111,11,0,0,0,0),
(3,112,11,0,0,0,0),
(4,111,11,0,0,0,0),
(4,112,11,0,0,0,0),
(6,111,11,0,0,0,0),
(6,112,11,0,0,0,0);

INSERT INTO BOWLING_ANALYSIS(PlayerID, MatchID, TeamID, OversBowled, RunsConceded, Maidens, Wickets)
VALUES
(17,111,12,0,0,0,0),
(16,111,12,0,0,0,0),
(16,112,12,0,0,0,0),
(15,111,12,0,0,0,0),
(15,112,12,0,0,0,0),
(14,111,12,0,0,0,0),
(14,112,12,0,0,0,0),
(13,111,12,0,0,0,0),
(13,112,12,0,0,0,0),
(12,111,12,0,0,0,0),
(12,112,12,0,0,0,0);

INSERT INTO FIELDING_ANALYSIS(PlayerID, MatchID, TeamID,Catches,Stumpings, RunOuts)
VALUES
(1,111,11,0,0,0),
(2,111,11,1,0,0),
(3,111,11,0,0,0),
(4,111,11,0,0,0),
(5,111,11,0,0,0),
(11,111,11,1,0,0),
(6,111,11,1,0,0),
(7,111,11,1,0,0),
(8,111,11,2,0,0),
(9,111,11,1,0,0),
(10,111,11,0,0,0),
(12,111,12,0,0,0),
(13,111,12,0,0,0),
(14,111,12,0,0,0),
(22,111,12,1,0,0),
(16,111,12,0,0,0),
(17,111,12,0,0,0),
(18,111,12,1,0,0),
(19,111,12,0,0,0),
(20,111,12,0,0,0),
(21,111,12,0,0,0);

INSERT INTO FIELDING_ANALYSIS(PlayerID, MatchID, TeamID,Catches,Stumpings, RunOuts)
VALUES
(1,112,11,0,0,0),
(2,112,11,1,0,0),
(3,112,11,1,0,0),
(4,112,11,0,0,0),
(5,112,11,0,0,0),
(11,112,11,0,0,0),
(6,112,11,1,0,0),
(7,112,11,0,0,0),
(8,112,11,0,0,0),
(9,112,11,0,0,0),
(10,112,11,0,0,0),
(12,112,12,2,0,0),
(13,112,12,0,0,0),
(14,112,12,0,0,0),
(15,112,12,1,0,0),
(22,112,12,0,0,0),
(16,112,12,0,0,0),
(17,112,12,0,0,0),
(18,112,12,1,0,0),
(19,112,12,1,0,0),
(20,112,12,2,0,0),
(21,112,12,0,0,0);

INSERT INTO PLAYER VALUES (23,"Dummy", DEFAULT, "2022-09-09","DFFNFD",DEFAULT,DEFAULT, "LR",11,12)

INSERT INTO DISMISSAL(MatchID,BatterID,BowlerID,FielderID,NatureOfDismissal)
VALUES
(111,2,18,23,"BOWLED"),
(111,3,19,22,"CAUGHT"),
(111,5,21,15,"CAUGHT"),
(111,6,22,18,"CAUGHT"),
(111,12,7,9,"CAUGHT"),
(111,13,11,9,"CAUGHT"),
(111,14,5,11,"CAUGHT"),
(111,15,10,2,"CAUGHT"),
(111,16,10,8,"CAUGHT"),
(111,17,11,7,"CAUGHT"),
(111,18,9,6,"CAUGHT"),
(111,19,5,23,"LBW"),
(111,20,9,23,"BOWLED"),
(111,22,11,23,"BOWLED"),
(112,1,21,23,"BOWLED"),
(112,2,21,20,"CAUGHT"),
(112,3,22,12,"CAUGHT"),
(112,4,22,18,"CAUGHT"),
(112,5,19,12,"CAUGHT"),
(112,6,18,15,"CAUGHT"),
(112,7,17,19,"CAUGHT"),
(112,8,17,20,"CAUGHT"),
(112,12,10,23,"LBW"),
(112,13,7,3,"CAUGHT"),
(112,14,9,23,"BOWLED"),
(112,15,7,6,"CAUGHT"),
(112,16,9,2,"CAUGHT"),
(112,18,9,23,"BOWLED");

