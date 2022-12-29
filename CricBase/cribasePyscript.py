from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "root123"
app.config['MYSQL_DATABASE_DB'] = 'CRICBASE'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
# player 
@app.route('/players/<int:player_id>', methods=['GET'])
def get_players(player_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    select_query = "SELECT * FROM PLAYER where PlayerID = %s"
    cursor.execute(select_query, (player_id,))
    resp = jsonify(cursor.fetchone())
    resp.status_code = 200
    return resp

@app.route('/players', methods=['POST'])
def create_player():
    conn = mysql.connect()
    cursor = conn.cursor()
    player_data = request.get_json()
    player_id = player_data.get('PlayerID')
    fname = player_data.get('FName')
    lname = player_data.get('LName')
    dob = player_data.get('DOB')
    primary_skill = player_data.get('PrimarySkill')
    secondary_skill = player_data.get('SecondarySkill')
    bowling_arm = player_data.get('BowlingArm')
    batting_hand = player_data.get('BattingHand')
    team_id = player_data.get('TeamID')
    debut_id = player_data.get('DebutID')
    insert_query = "INSERT INTO PLAYER (PlayerID, FName, LName, DOB, PrimarySkill, SecondarySkill, BowlingArm, BattingHand, TeamID, DebutID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (player_id, fname, lname, dob, primary_skill, secondary_skill, bowling_arm, batting_hand, team_id, debut_id))
    conn.commit()
    resp = jsonify({'message': 'Player created successfully'})
    resp.status_code = 201
    return resp

@app.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    delete_query = "DELETE FROM PLAYER WHERE PlayerID=%s"
    cursor.execute(delete_query, (player_id,))
    conn.commit()
    resp = jsonify({'message': 'Player deleted successfully'})
    resp.status_code = 200
    return resp

#teams 
@app.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    select_query = "SELECT * FROM TEAM where TeamID = %s"
    cursor.execute(select_query, (team_id,))
    resp = jsonify(cursor.fetchone())
    resp.status_code = 200
    return resp

@app.route('/teams', methods=['POST'])
def create_team():
    conn = mysql.connect()
    cursor = conn.cursor()
    team_data = request.get_json()
    team_id = team_data.get('TeamID')
    name = team_data.get('Name')
    division = team_data.get('Division')
    level = team_data.get('Level')
    insert_query = "INSERT INTO TEAM (TeamID, Name, Division, Grade) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (team_id, name, division, level))
    conn.commit()
    resp = jsonify({'message': 'Team created successfully'})
    resp.status_code = 201
    return resp

@app.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    delete_query = "DELETE FROM TEAM WHERE TeamID=%s"
    cursor.execute(delete_query, (team_id,))
    conn.commit()
    resp = jsonify({'message': 'Team deleted successfully'})
    resp.status_code = 200
    return resp

# tournament
@app.route('/tournaments/<int:tournament_id>', methods=['GET'])
def get_tournament(tournament_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    select_query = "SELECT * FROM TOURNAMENT where TournamentID = %s"
    cursor.execute(select_query, (tournament_id,))
    resp = jsonify(cursor.fetchone())
    resp.status_code = 200
    return resp

@app.route('/tournaments', methods=['POST'])
def create_tournament():
    conn = mysql.connect()
    cursor = conn.cursor()
    tournament_data = request.get_json()
    tournament_id = tournament_data.get('TournamentID')
    name = tournament_data.get('TournamentName')
    start_year = tournament_data.get('StartYear')
    level = tournament_data.get('Level')
    end_year = tournament_data.get('EndYear')
    insert_query = "INSERT INTO TOURNAMENT (TournamentID, TournamentName, StartYear, Grade, EndYear) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (tournament_id, name, start_year, level, end_year))
    conn.commit()
    resp = jsonify({'message': 'Tournament created successfully'})
    resp.status_code = 201
    return resp

@app.route('/tournaments/<int:tournament_id>', methods=['DELETE'])
def delete_tournament(tournament_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    delete_query = "DELETE FROM TOURNAMENT WHERE TournamentID=%s"
    cursor.execute(delete_query, (tournament_id,))
    conn.commit()
    resp = jsonify({'message': 'Tournament deleted successfully'})
    resp.status_code = 200
    return resp

# matches
@app.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    select_query = "SELECT * FROM MATCHES where MatchID = %s"
    cursor.execute(select_query, (match_id,))
    resp = jsonify(cursor.fetchone())
    resp.status_code = 200
    return resp

@app.route('/matches', methods=['POST'])
def create_match():
    conn = mysql.connect()
    cursor = conn.cursor()
    match_data = request.get_json()
    match_id = match_data.get('MatchID')
    tournament_id = match_data.get('TournamentID')
    team_id1 = match_data.get('TeamID1')
    team_id2 = match_data.get('TeamID2')
    venue = match_data.get('Venue')
    date = match_data.get('Date')
    insert_query = "INSERT INTO MATCHES (MatchID, TournamentID, TeamID1, TeamID2, Venue, Date) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (match_id, tournament_id, team_id1, team_id2, venue, date))
    conn.commit()
    resp = jsonify({'message': 'Match created successfully'})
    resp.status_code = 201
    return resp

@app.route('/matches/<int:match_id>', methods=['DELETE'])
def delete_match(match_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    delete_query = "DELETE FROM MATCHES WHERE MatchID=%s"
    cursor.execute(delete_query, (match_id,))
    conn.commit()
    resp = jsonify({'message': 'Match deleted successfully'})
    resp.status_code = 200
    return resp


# batting analysis
@app.route('/batting-analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['GET'])
def get_batting_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    select_query = "SELECT * FROM BATTING_ANALYSIS where PlayerID = %s AND MatchID = %s AND TeamID = %s"
    cursor.execute(select_query, (player_id, match_id, team_id))
    resp = jsonify(cursor.fetchone())
    resp.status_code = 200
    return resp

@app.route('/batting-analysis', methods=['POST'])
def create_batting_analysis():
    conn = mysql.connect()
    cursor = conn.cursor()
    analysis_data = request.get_json()
    player_id = analysis_data.get('PlayerID')
    match_id = analysis_data.get('MatchID')
    team_id = analysis_data.get('TeamID')
    balls_faced = analysis_data.get('BallsFaced')
    runs_scored = analysis_data.get('RunsScored')
    is_dismissed = analysis_data.get('isDismissed')
    fours = analysis_data.get('Fours')
    sixes = analysis_data.get('Sixes')
    insert_query = "INSERT INTO BATTING_ANALYSIS (PlayerID, MatchID, TeamID, BallsFaced, RunsScored, isDismissed, Fours, Sixes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (player_id, match_id, team_id, balls_faced, runs_scored, is_dismissed, fours, sixes))
    conn.commit()
    resp = jsonify({'message': 'Batting analysis created successfully'})
    resp.status_code = 201
    return resp

@app.route('/batting-analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE'])
def delete_batting_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    delete_query = "DELETE FROM BATTING_ANALYSIS WHERE PlayerID=%s AND MatchID=%s AND TeamID=%s"
    cursor.execute(delete_query, (player_id, match_id, team_id))
    conn.commit()
    resp = jsonify({'message': 'Batting analysis deleted successfully'})
    resp.status_code = 200
    return resp

# bowling analysis
@app.route('/bowling-analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['GET'])
def get_bowling_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    select_query = "SELECT * FROM BOWLING_ANALYSIS WHERE PlayerID = %s AND MatchID = %s AND TeamID = %s"
    cursor.execute(select_query, (player_id, match_id, team_id))
    resp = jsonify(cursor.fetchone())
    resp.status_code = 200
    return resp

@app.route('/bowling-analysis', methods=['POST'])
def create_bowling_analysis():
    conn = mysql.connect()
    cursor = conn.cursor()
    bowling_analysis_data = request.get_json()
    player_id = bowling_analysis_data.get('PlayerID')
    match_id = bowling_analysis_data.get('MatchID')
    team_id = bowling_analysis_data.get('TeamID')
    overs_bowled = bowling_analysis_data.get('OversBowled')
    runs_conceded = bowling_analysis_data.get('RunsConceded')
    maidens = bowling_analysis_data.get('Maidens')
    wickets = bowling_analysis_data.get('Wickets')
    insert_query = "INSERT INTO BOWLING_ANALYSIS (PlayerID, MatchID, TeamID, OversBowled, RunsConceded, Maidens, Wickets) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (player_id, match_id, team_id, overs_bowled, runs_conceded, maidens, wickets))
    conn.commit()
    resp = jsonify({'message': 'Bowling analysis created successfully'})
    resp.status_code = 201
    return resp

@app.route('/bowling-analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE'])
def delete_bowling_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    delete_query = "DELETE FROM BOWLING_ANALYSIS WHERE PlayerID = %s AND MatchID = %s AND TeamID = %s"
    cursor.execute(delete_query, (player_id, match_id, team_id))
    conn.commit()
    resp = jsonify({'message': 'Bowling analysis deleted successfully'})
    resp.status_code = 200
    return resp

# fielding analysis 
@app.route('/fielding_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['GET'])
def get_fielding_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    select_query = "SELECT * FROM FIELDING_ANALYSIS WHERE PlayerID = %s AND MatchID = %s AND TeamID = %s"
    cursor.execute(select_query, (player_id, match_id, team_id))
    resp = jsonify(cursor.fetchone())
    resp.status_code = 200
    return resp

@app.route('/fielding_analysis', methods=['POST'])
def create_fielding_analysis():
    conn = mysql.connect()
    cursor = conn.cursor()
    fielding_analysis_data = request.get_json()
    player_id = fielding_analysis_data.get('PlayerID')
    match_id = fielding_analysis_data.get('MatchID')
    team_id = fielding_analysis_data.get('TeamID')
    catches = fielding_analysis_data.get('Catches')
    stumpings = fielding_analysis_data.get('Stumpings')
    run_outs = fielding_analysis_data.get('RunOuts')
    insert_query = "INSERT INTO FIELDING_ANALYSIS (PlayerID, MatchID, TeamID, Catches, Stumpings, RunOuts) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (player_id, match_id, team_id, catches, stumpings, run_outs))
    conn.commit()
    resp = jsonify({'message': 'Fielding analysis created successfully'})
    resp.status_code = 201
    return resp

@app.route('/fielding_analysis/<int:player_id>/<int:match_id>/<int:team_id>', methods=['DELETE'])
def delete_fielding_analysis(player_id, match_id, team_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    delete_query = "DELETE FROM FIELDING_ANALYSIS WHERE PlayerID = %s AND MatchID = %s AND TeamID = %s"
    cursor.execute(delete_query, (player_id, match_id, team_id))
    conn.commit()
    resp = jsonify({'message': 'Fielding analysis deleted successfully'})
    resp.status_code = 200
    return resp

# dismissal table 
@app.route('/dismissals/<int:match_id>/<int:batter_id>', methods=['GET'])
def get_dismissal(match_id, batter_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    select_query = "SELECT * FROM DISMISSAL WHERE MatchID = %s AND BatterID = %s"
    cursor.execute(select_query, (match_id, batter_id))
    resp = jsonify(cursor.fetchone())
    resp.status_code = 200
    return resp

@app.route('/dismissals', methods=['POST'])
def create_dismissal():
    conn = mysql.connect()
    cursor = conn.cursor()
    dismissal_data = request.get_json()
    match_id = dismissal_data.get('MatchID')
    batter_id = dismissal_data.get('BatterID')
    bowler_id = dismissal_data.get('BowlerID')
    fielder_id = dismissal_data.get('FielderID')
    nature_of_dismissal = dismissal_data.get('NatureOfDismissal')
    insert_query = "INSERT INTO DISMISSAL (MatchID, BatterID, BowlerID, FielderID, NatureOfDismissal) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (match_id, batter_id, bowler_id, fielder_id, nature_of_dismissal))
    conn.commit()
    resp = jsonify({'message': 'Dismissal created successfully'})
    resp.status_code = 201
    return resp

@app.route('/dismissals/<int:match_id>/<int:batter_id>', methods=['DELETE'])
def delete_dismissal(match_id, batter_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    delete_query = "DELETE FROM DISMISSAL WHERE MatchID = %s AND BatterID = %s"
    cursor.execute(delete_query, (match_id, batter_id))
    conn.commit()
    resp = jsonify({'message': 'Dismissal deleted successfully'})
    resp.status_code = 200
    return resp


