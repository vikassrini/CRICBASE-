
from flask import Flask, request, jsonify, render_template
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
app.config['MYSQL_DATABASE_PASSWORD'] = "root123"
app.config['MYSQL_DATABASE_DB'] = 'CRICO'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#front end
#basic pages
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


#the following methods are for displaying information 


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
    column = ['PLayerID','FName','LName','TeamID','Matches','Innings','Runs','Balls','Average','StrikeRate','Overs','RunsConceded','Wickets','Maidens', 'BowlingAverage','BowlingStrikeRate','Catches','RunOuts','Stumpings']
    cursor.execute("SELECT PlayerID from PLAYER WHERE PlayerID != 23")
    player_ids = cursor.fetchall()
    for i in player_ids:
        cursor.callproc('getSummary',(i,))
        rows.append(cursor.fetchone())
    
    return render_template('index.html', rows = rows, column = column)



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

@app.route('/player/<int:player_id>', methods=['DELETE'])
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

@app.route('/team/<int:team_id>', methods=['DELETE'])
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

@app.route('/tournament/<int:tournament_id>', methods=['DELETE'])
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

@app.route('/matches/<int:match_id>', methods=['DELETE'])
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

@app.route('/batting_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE'])
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

@app.route('/bowling_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE'])
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

@app.route('/fielding_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE'])
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

@app.route('/dismissals/<int:match_id>/<int:batter_id>', methods=['DELETE'])
def delete_dismissal(match_id, batter_id):
    conn = mysql.connect()
    Dismissal.delete_from_database(conn, match_id, batter_id)
    resp = jsonify({'message': 'Dismissal deleted successfully'})
    resp.status_code = 200
    return resp

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

