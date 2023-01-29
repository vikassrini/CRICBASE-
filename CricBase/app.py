
from flask import Flask, request, jsonify, render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort

from flaskext.mysql import MySQL
from player import Player
from batting_analysis import BattingAnalysis
from bowling_analysis import BowlingAnalysis
from dismissal import Dismissal
from matches import Match
from team import Team
from tournament import Tournament
from fielding_analysis import FieldingAnalysis
from player_summary import PlayerSummary
from player_fielding_summary import PlayerFieldingSummary
from player_bowling_summary import PlayerBowlingSummary
from player_batting_summary import PlayerBattingSummary


import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
mysql = MySQL()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "awbo22Oct!"
app.config['MYSQL_DATABASE_DB'] = 'CRICO'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#front end
#basic pages
#####################################################################################################
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home_page')
def home():
    return render_template('home.html')
@app.route('/view_info')
def view_info():
    return render_template('view_info.html')

@app.route('/mod_info')
def mod_info():
    return render_template('mod_info.html')

@app.route('/delete_info')
def delete_info():
    return render_template('delete_info.html')


#the following methods are for displaying information 
########################################################################################################
@app.route('/display_tournament')
def disp_tourn():
    cnx = mysql.connect()
    cursor = cnx.cursor()

    query = "select * from tournament"
    column = ['TournamentID', 'TournamentName', 'StartYear', 'Grade', 'EndYear']
    cursor.execute(query)

    rows = cursor.fetchall()
    #rows.append(column) 
    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows , column =column)

@app.route('/display_team')
def disp_team():
    cnx = mysql.connect()
    cursor = cnx.cursor()

    query = "select * from team"
    column = ['TeamID', 'Name', 'Division', 'Grade']
    cursor.execute(query)

    rows = cursor.fetchall()
    #rows.append(column) 
    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows , column =column)

@app.route('/display_player')
def display_player():
    cnx = mysql.connect()
    cursor = cnx.cursor()

    query = "select * from player"
    column = ['PlayerID', 'FName', 'LName', 'DOB', 'PrimarySkill', 'SecondarySkill', 'BowlingArm', 'BattingHand', 'TeamID', 'DebutID']
    cursor.execute(query)

    rows = cursor.fetchall()
    #rows.append(column) 
    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows , column =column)

@app.route('/display_matches')
def disp_matches():
    cnx = mysql.connect()
    cursor = cnx.cursor()

    query = "select * from matches"
    column = ["MatchID", 'TournamentID', 'TeamID1', 'TeamID2', 'Venue', 'DatePlayed']
    cursor.execute(query)

    rows = cursor.fetchall()
    #rows.append(column) 
    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows , column =column)

@app.route('/display_fielding_analysis')
def disp_fielding_analysis():
    cnx = mysql.connect()
    cursor = cnx.cursor()

    query = "select * from fielding_analysis"
    column = ['PlayerID', 'MatchID', 'TeamID', 'Catches', 'Stumpings', 'RunOuts']
    cursor.execute(query)

    rows = cursor.fetchall()
    #rows.append(column) 
    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows , column =column)
    
@app.route('/display_dismissal')
def disp_dismissal():
    cnx = mysql.connect()
    cursor = cnx.cursor()

    query = "select * from dismissal"
    column = ['MatchID', 'BatterID', 'BowlerID', 'FielderID', 'NatureOfDismissal']
    cursor.execute(query)

    rows = cursor.fetchall()
    #rows.append(column) 
    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows , column =column)
    
@app.route('/display_bowling_analysis')
def disp_bowling_analysis():
    cnx = mysql.connect()
    cursor = cnx.cursor()

    query = "select * from bowling_analysis"
    column = ['PlayerID', 'MatchID', 'TeamID', 'OversBowled', 'RunsConceded','Maidens','Wickets']
    cursor.execute(query)

    rows = cursor.fetchall()
    #rows.append(column) 
    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows , column =column)
    
@app.route('/display_batting_analysis')
def disp_batting_analysis():
    cnx = mysql.connect()
    cursor = cnx.cursor()

    query = "select * from batting_analysis"
    column = ['PlayerID', 'MatchID', 'TeamID', 'BallsFaced', 'RunsScored', 'DismissalStatus', 'Fours', 'Sixes']
    cursor.execute(query)

    rows = cursor.fetchall()
    #rows.append(column) 
    cursor.close()
    cnx.close()

    return render_template('index.html', rows=rows , column =column)
    

@app.route('/display_player_summary')
def display_player_summary():
    cnx = mysql.connect()
    cursor = cnx.cursor()
    rows = list()
    column = ['PLayerID','FName','LName','TeamID','Matches','Innings','Runs','Average','StrikeRate','Overs','RunsConceded','Wickets','Maidens','BowlingAverage','BowlingStrikeRate','Catches','RunOuts','Stumpings']
    cursor.execute("SELECT PlayerID from PLAYER WHERE PlayerID != 23")
    player_ids = cursor.fetchall()
    for i in player_ids:
        cursor.callproc('getSummary',(i,))
        rows.append(cursor.fetchone())
    
    return render_template('index.html', rows = rows, column = column)

# insert info end points start from here
# this section is more of a testing point for the frontend
########################################################################################################################################################################################################################
@app.route('/render_insert_player_info')    #link here to html insert nav bar
def player_form():
    return render_template('insert_player.html')

@app.route('/submit_player_info', methods=['POST'])
def submit_player():
    playerID = request.form['PlayerID']
    fname = request.form['FName']
    lname = request.form['LName']
    dob = request.form['DOB']
    primarySkill = request.form['PrimarySkill']
    secondarySkill = request.form['SecondarySkill']
    bowlingArm = request.form['BowlingArm']
    battingHand = request.form['BattingHand']
    teamID = request.form['TeamID']
    debutID = request.form['DebutID']
    
    # Validate input data
    if not playerID.isdigit() or int(playerID) < 1:
        return "Invalid PlayerID. Please enter a valid number"
    if not fname or not lname:
        return "Please enter a first and last name"
    if not dob:
        return "Please enter a valid date of birth"
    if not primarySkill:
        return "Please enter a primary skill"
    if not secondarySkill:
        return "Please enter a secondary skill"
    if not bowlingArm:
        return "Please enter a bowling arm"
    if not battingHand:
        return "Please enter a batting hand"
    if not teamID.isdigit() or int(teamID) < 1:
        return "Invalid TeamID. Please enter a valid number"
    if not debutID.isdigit() or int(debutID) < 1:
        return "Invalid DebutID. Please enter a valid number"
    
    # Connect to MySQL
    conn = mysql.connect()
    cursor = conn.cursor()

    # Prepare and execute SQL query
    sql = "INSERT INTO player(PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (playerID, fname, lname, dob, primarySkill, secondarySkill, bowlingArm, battingHand, teamID, debutID)
    cursor.execute(sql, data)
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return "Data inserted successfully"

@app.route('/render_team_insert_info')    #link here to html insert nav bar
def team_form():
    return render_template('insert_team.html')

@app.route('/submit_team_info', methods=['POST'])
def submit_team():
    team_id = request.form.get('TeamID')
    name = request.form.get('Name')
    division = request.form.get('Division')
    grade = request.form.get('Grade')

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO team (TeamID, Name, Division, Grade) VALUES (%s, %s, %s, %s)", (team_id, name, division, grade))
    conn.commit()
    cursor.close()
    conn.close()

    return "Data inserted successfully"

@app.route('/render_tournament_insert_info')    #link here to html insert nav bar
def tournament_form():
    return render_template('insert_tournament.html')

@app.route('/submit_tournament_info',methods=['POST'])
def submit_tournament():
   # Fetch form data
        tournament_id = request.form['TournamentID']
        tournament_name = request.form['TournamentName']
        start_year = request.form['StartYear']
        grade = request.form['Grade']
        end_year = request.form['EndYear']
        
        # Validate form data
        if tournament_id and tournament_name and start_year and grade and end_year:
            # Create cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute("INSERT INTO tournament(TournamentID, TournamentName, StartYear, Grade, EndYear) VALUES(%s, %s, %s, %s, %s)", (tournament_id, tournament_name, start_year, grade, end_year))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()
        return "Data inserted successfully"

@app.route('/render_matches_insert_info')    #link here to html insert nav bar
def matches_form():
    return render_template('insert_matches.html')

@app.route('/submit_matches_info',methods=['POST'])
def submit_matches():
    match_id = request.form['MatchID']
    tournament_id = request.form['TournamentID']
    team_id1 = request.form['TeamID1']
    team_id2 = request.form['TeamID2']
    venue = request.form['Venue']
    date_played = request.form['DatePlayed']

    # Validate the form data 
    if not match_id or not tournament_id or not team_id1 or not team_id2 or not venue or not date_played:
        return "Please fill in all the fields"

    # Connect to the MySQL database
    cnx = mysql.connector.connect(user='your_username', password='your_password', host='your_host', database='your_dbname')
    cursor = cnx.cursor()

    # Insert the data into the matches table
    query = "INSERT INTO matches (MatchID, TournamentID, TeamID1, TeamID2, Venue, DatePlayed) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (match_id, tournament_id, team_id1, team_id2, venue, date_played))
    cnx.commit()
    cursor.close()
    cnx.close()

    return "Match submitted successfully"

@app.route('/render_fielding_analysis')    #link here to html insert nav bar
def fielding_analysis_form():
    return render_template('insert_fielding_analysis.html')

@app.route('/submit_fielding_analysis_info',methods=['POST'])
def submit_fielding_analysis():
        player_id = request.form.get('PlayerID')
        match_id = request.form.get('MatchID')
        team_id = request.form.get('TeamID')
        catches = request.form.get('Catches')
        stumpings = request.form.get('Stumpings')
        run_outs = request.form.get('RunOuts')
        
        # Validate form data
        if not player_id or not match_id or not team_id or not catches or not stumpings or not run_outs:
            return "Please fill out all fields."
        
        # Insert data into MySQL database
        cursor = mysql.connect().cursor()
        sql = "INSERT INTO fielding_analysis (PlayerID, MatchID, TeamID, Catches, Stumpings, RunOuts) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (player_id, match_id, team_id, catches, stumpings, run_outs))
        mysql.connect().commit()
        cursor.close()
        
        return "Data successfully inserted into database."

@app.route('/render_dismissals')    #link here to html insert nav bar
def dismissals_form():
    return render_template('insert_dismissals.html')

@app.route('/submit_dismissals_info',methods=['POST'])
def submit_dismissals():
     # Get form data
        MatchID = request.form['MatchID']
        BatterID = request.form['BatterID']
        BowlerID = request.form['BowlerID']
        FielderID = request.form['FielderID']
        NatureOfDismissal = request.form['NatureOfDismissal']

        
        # Validate form data
        if not MatchID or not BatterID or not BowlerID or not FielderID or not NatureOfDismissal:
            return "Please fill in all the fields"
        if not str(MatchID).isdigit() or not str(BatterID).isdigit() or not str(BowlerID).isdigit() or not str(FielderID).isdigit():
            return "MatchID, BatterID, BowlerID, FielderID should be integer"
        # Insert data into MySQL database
        cursor = mysql.connect().cursor()
        sql = "INSERT INTO fielding_analysis (MatchID, BatterID, BowlerID, FielderID,NatureOfDismissal) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (MatchID, BatterID, BowlerID, FielderID,NatureOfDismissal))
        mysql.connect().commit()
        cursor.close()
        
        return "Data successfully inserted into database."

@app.route('/render_batting_analysis')    #link here to html insert nav bar
def batting_analysis_form():
    return render_template('insert_batting_analysis.html')

@app.route('/submit_batting_analysis_info',methods=['POST'])
def submit_batting_analysis():
     # Get form data
        player_id = request.form['PlayerID']
        match_id = request.form['MatchID']
        team_id = request.form['TeamID']
        balls_faced = request.form['BallsFaced']
        runs_scored = request.form['RunsScored']
        dismissal_status = request.form['DismissalStatus']
        fours = request.form['Fours']
        sixes = request.form['Sixes']
        
        # Validate form data
        if player_id and match_id and team_id and balls_faced and runs_scored and dismissal_status and fours and sixes:
            cursor = mysql.connect.cursor()
            query = "INSERT INTO batting_analysis (PlayerID, MatchID, TeamID, BallsFaced, RunsScored, DismissalStatus, Fours, Sixes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (player_id, match_id, team_id, balls_faced, runs_scored, dismissal_status, fours, sixes)
            cursor.execute(query, values)
            mysql.connect().commit()
            cursor.close()
            return 'Data inserted successfully'
        else:
           return 'Please fill in all the fields'

@app.route('/render_bowling_analysis')    #link here to html insert nav bar
def bowling_analysis_form():
    return render_template('insert_bowling_analysis.html')

@app.route('/submit_bowling_analysis_info',methods=['POST'])
def submit_bowling_analysis():
    if request.method == 'POST':
        player_id = request.form['PlayerID']
        match_id = request.form['MatchID']
        team_id = request.form['TeamID']
        overs_bowled = request.form['OversBowled']
        runs_conceded = request.form['RunsConceded']
        maidens = request.form['Maidens']
        wickets = request.form['Wickets']
        
        # Validate the input data
        error = None
        if not player_id:
            error = 'Player ID is required'
        elif not match_id:
            error = 'Match ID is required'
        elif not team_id:
            error = 'Team ID is required'
        elif not overs_bowled:
            error = 'Overs Bowled is required'
        elif not runs_conceded:
            error = 'Runs Conceded is required'
        elif not maidens:
            error = 'Maidens is required'
        elif not wickets:
            error = 'Wickets is required'
        if error is None:
    
            cursor = mysql.connect.cursor()
            # Insert the data into the database
            query = "INSERT INTO bowling_analysis (PlayerID, MatchID, TeamID, OversBowled, RunsConceded, Maidens, Wickets) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (player_id, match_id, team_id, overs_bowled, runs_conceded, maidens, wickets)
            cursor.execute(query, values)
            mysql.connect().commit()
            cursor.close()
            return'Data inserted successfully'
#######################################################################################################################################################################
# more efficiently written code starts from here 

# player 
@app.route('/player/<int:player_id>', methods=['GET'])
def get_players(player_id):
    conn = mysql.connect()
    player = Player.read_from_database(conn, player_id)
    if player is None:
        return "No Player found", 404
    return player.to_json(), 200

@app.route('/player', methods=['POST'])
def create_player():
    conn = mysql.connect()
    data = request.get_json()
    player = Player.from_json(data)
    Player.write_to_database(conn, player)
    return jsonify({'message': 'Player created successfully'}), 201

@app.route('/delete_player_render')
def render_player():
    return render_template('delete_player.html')

@app.route('/player/<int:player_id>', methods=['DELETE'])   #done
def delete_player(player_id):
    conn = mysql.connect()
    Player.delete_from_database(conn, player_id)
    return jsonify({'message': 'Player deleted successfully'}), 200

#teams 
@app.route('/team/<int:team_id>', methods=['GET'])
def get_team(team_id):
    conn = mysql.connect()
    team = Team.read_from_database(conn, team_id)
    if team is None:
        return "No entry found", 404
    return team.to_json(), 200

@app.route('/team', methods=['POST'])
def create_team():
    conn = mysql.connect()
    data = request.get_json()
    team = Team.from_json(data)
    Team.write_to_database(conn, team)
    return jsonify({'message': 'Team created successfully'}), 201

@app.route('/delete_team_render')
def render_team():
    return render_template('delete_teams.html')

@app.route('/team/<int:team_id>', methods=['DELETE'])   #done
def delete_team(team_id):
    conn = mysql.connect()
    Team.delete_from_database(conn, team_id)
    return jsonify({'message': 'Team deleted successfully'}), 200

# tournament
@app.route('/tournament/<int:tournament_id>', methods=['GET'])
def get_tournament(tournament_id):
    conn = mysql.connect()
    tournament = Tournament.read_from_database(conn, tournament_id)
    if tournament is None:
        return "No entry found", 404
    return tournament.to_json(), 200

@app.route('/tournament', methods=['POST'])
def create_tournament():
    conn = mysql.connect()
    data = request.get_json()
    tournament = Tournament.from_json(data)
    Tournament.write_to_database(conn, tournament)
    return jsonify({'message': 'Tournament created successfully'}), 201

@app.route('/delete_tournament_render')
def render_delete_tournament():
    return render_template('delete_tournament.html')

@app.route('/tournament/<int:tournament_id>', methods=['DELETE']) #done
def delete_tournament(tournament_id):
    conn = mysql.connect()
    Tournament.delete_from_database(conn, tournament_id)
    return jsonify({'message': 'Tournament deleted successfully'}), 200

# matches
@app.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    conn = mysql.connect()
    match = Match.read_from_database(conn, match_id)
    if match is None:
        return "No entry found", 404
    return match.to_json(), 200

@app.route('/matches', methods=['POST'])
def create_match():
    conn = mysql.connect()
    data = request.get_json()
    match = Match.from_json(data)
    Match.write_to_database(conn, match)
    resp = jsonify({'message': 'Match created successfully'})
    resp.status_code = 201
    return resp

@app.route('/delete_matches_render')
def render_delete_matches():
    return render_template('delete_matches.html')



@app.route('/matches/<int:match_id>', methods=['DELETE']) #done
def delete_match(match_id):
    conn = mysql.connect()
    Match.delete_from_database(conn, match_id)
    resp = jsonify({'message': 'Match deleted successfully'})
    resp.status_code = 200
    return resp


# batting analysis
@app.route('/batting_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['GET'])
def get_batting_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    battingAnalysis = BattingAnalysis.read_from_database(conn, player_id, match_id, team_id)
    if battingAnalysis is None:
        return "No entry found", 404
    return battingAnalysis.to_json(), 200

@app.route('/batting_analysis', methods=['POST'])
def create_batting_analysis():
    conn = mysql.connect()
    data = request.get_json()
    battingAnalysis = BattingAnalysis.from_json(data)
    BattingAnalysis.write_to_database(conn, battingAnalysis)
    resp = jsonify({'message': 'Batting analysis created successfully'})
    resp.status_code = 200
    return resp

@app.route('/delete_batting_analysis_render')
def render_delete_battinng_analysis():
    return render_template('delete_batting_analysis.html')

@app.route('/batting_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE']) #done
def delete_batting_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    BattingAnalysis.delete_from_database(conn,player_id, match_id, team_id)
    resp = jsonify({'message': 'Batting analysis deleted successfully'})
    resp.status_code = 200
    return resp

# bowling analysis
@app.route('/bowling_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['GET'])
def get_bowling_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    bowlingAnalysis = BowlingAnalysis.read_from_database(conn, player_id, match_id, team_id)
    if bowlingAnalysis is None:
        return "No entry found", 404
    return bowlingAnalysis.to_json(), 200

@app.route('/bowling_analysis', methods=['POST'])
def create_bowling_analysis():
    conn = mysql.connect()
    data = request.get_json()
    bowlingAnalysis = BowlingAnalysis.from_json(data)
    BowlingAnalysis.write_to_database(conn, bowlingAnalysis)
    resp = jsonify({'message': 'Bowling analysis created successfully'})
    resp.status_code = 201
    return resp

@app.route('/delete_bowling_analysis_render')
def render_delete_bowling_analysis():
    return render_template('delete_bowling_analysis.html')

@app.route('/bowling_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE']) #done
def delete_bowling_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    BowlingAnalysis.delete_from_database(conn, player_id, match_id, team_id)
    resp = jsonify({'message': 'Bowling analysis deleted successfully'})
    resp.status_code = 200
    return resp

# fielding analysis 
@app.route('/fielding_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['GET'])
def get_fielding_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    fielding = FieldingAnalysis.read_from_database(conn, player_id, match_id, team_id)
    if fielding is None:
        return "No entry found", 404
    return fielding.to_json(), 200

@app.route('/fielding_analysis', methods=['POST'])
def create_fielding_analysis():
    conn = mysql.connect()
    data = request.get_json()
    fielding = FieldingAnalysis.from_json(data)
    FieldingAnalysis.write_to_database(conn, fielding)
    resp = jsonify({'message': 'Fielding analysis created successfully'})
    resp.status_code = 201
    return resp

@app.route('/delete_fielding_analysis_render')
def render_delete_fielding_analysis():
    return render_template('delete_fielding_analysis.html')

@app.route('/fielding_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE']) #done
def delete_fielding_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    FieldingAnalysis.delete_from_database(conn, player_id, match_id, team_id)
    resp = jsonify({'message': 'Fielding analysis deleted successfully'})
    resp.status_code = 200
    return resp

# dismissal table 
@app.route('/dismissals/<int:match_id>/<int:batter_id>', methods=['GET'])
def get_dismissal(match_id, batter_id):
    conn = mysql.connect()
    dismissal = Dismissal.read_from_database(conn, match_id, batter_id)
    if dismissal is None:
        return "No entry found", 404
    return dismissal.to_json(), 200

@app.route('/dismissals', methods=['POST'])
def create_dismissal():
    conn = mysql.connect()
    data = request.get_json()
    dismissal = Dismissal.from_json(data)
    Dismissal.write_to_database(conn, dismissal)
    resp = jsonify({'message': 'Dismissal created successfully'})
    resp.status_code = 201
    return resp

@app.route('/delete_dismissals_render')
def render_delete_dismissal():
    return render_template('delete_dismissals.html')

@app.route('/dismissals/<int:match_id>/<int:batter_id>', methods=['DELETE'])#done
def delete_dismissal(match_id, batter_id):
    conn = mysql.connect()
    Dismissal.delete_from_database(conn, match_id, batter_id)
    resp = jsonify({'message': 'Dismissal deleted successfully'})
    resp.status_code = 200
    return resp
###################################################################################################
#generates summaries 
@app.route('/player_fielding_summary/<int:player_id>', methods=['GET'])
def get_player_fielding_summary(player_id):
    conn = mysql.connect()
    fieldingSummary = PlayerFieldingSummary.read_from_database(conn, player_id)
    return fieldingSummary.to_json(), 200

@app.route('/player_bowling_summary/<int:player_id>', methods=['GET'])
def get_player_bowling_summary(player_id):
    conn = mysql.connect()
    summary = PlayerBowlingSummary.read_from_database(conn, player_id)
    return summary.to_json(), 200

@app.route('/player_batting_summary/<int:player_id>', methods=['GET'])
def get_player_batting_summary(player_id):
    conn = mysql.connect()
    sum = PlayerBattingSummary.read_from_database(conn, player_id)
    return sum.to_json(), 200

@app.route('/playerSummary/<int:player_id>')
def get_player_summary(player_id):
    conn = mysql.connect()
    playerSummary = PlayerSummary.read_from_database(conn=conn, player_id=player_id)
    return playerSummary.to_json(),200

if __name__ == '__main__':
    app.run(debug=True)

