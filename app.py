from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv('config/db.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Standing(db.Model):
    __tablename__ = 'standings'
    
    season = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(50))
    games_played = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    goals_for = db.Column(db.Integer)
    goals_against = db.Column(db.Integer)
    goal_difference = db.Column(db.Integer)
    points = db.Column(db.Integer)


@app.route('/')
def home():
    return render_template('index.html')


# Get all standings with optional filters
@app.route('/standings')
def get_all_standings():
    try:
        # Get query parameters
        season = request.args.get('season', type=int)
        team = request.args.get('team')
        min_points = request.args.get('min_points', type=int)
        max_position = request.args.get('max_position', type=int)
        
        # Start with base query
        query = Standing.query
        
        # Apply filters based on query parameters
        if season:
            query = query.filter_by(season=season)
        if team:
            query = query.filter(Standing.team.ilike(f'%{team}%'))
        if min_points:
            query = query.filter(Standing.points >= min_points)
        if max_position:
            query = query.filter(Standing.position <= max_position)
            
        standings = query.order_by(Standing.season, Standing.position).all()
        
        result = []
        for standing in standings:
            result.append({
                'season': standing.season,
                'position': standing.position,
                'team': standing.team,
                'games_played': standing.games_played,
                'wins': standing.wins,
                'draws': standing.draws,
                'losses': standing.losses,
                'goals_for': standing.goals_for,
                'goals_against': standing.goals_against,
                'goal_difference': standing.goal_difference,
                'points': standing.points
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get standings by season
@app.route('/standings/<int:season>')
def get_standings_by_season(season):
    try:
        standings = Standing.query.filter_by(season=season).order_by(Standing.position).all()
        result = []
        for standing in standings:
            result.append({
                'season': standing.season,
                'position': standing.position,
                'team': standing.team,
                'games_played': standing.games_played,
                'wins': standing.wins,
                'draws': standing.draws,
                'losses': standing.losses,
                'goals_for': standing.goals_for,
                'goals_against': standing.goals_against,
                'goal_difference': standing.goal_difference,
                'points': standing.points
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get team performance using query parameters
@app.route('/team')
def get_team_performance_query():
    try:
        team_name = request.args.get('name')
        season = request.args.get('season', type=int)
        
        if not team_name:
            return jsonify({"error": "Team name is required"}), 400
            
        query = Standing.query.filter_by(team=team_name)
        
        if season:
            query = query.filter_by(season=season)
            
        standings = query.order_by(Standing.season).all()
        
        result = []
        for standing in standings:
            result.append({
                'season': standing.season,
                'position': standing.position,
                'team': standing.team,
                'games_played': standing.games_played,
                'wins': standing.wins,
                'draws': standing.draws,
                'losses': standing.losses,
                'goals_for': standing.goals_for,
                'goals_against': standing.goals_against,
                'goal_difference': standing.goal_difference,
                'points': standing.points
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Search teams with flexible parameters
@app.route('/search')
def search_teams():
    try:
        team = request.args.get('team')
        season_start = request.args.get('season_start', type=int)
        season_end = request.args.get('season_end', type=int)
        position_start = request.args.get('position_start', type=int)
        position_end = request.args.get('position_end', type=int)
        
        query = Standing.query
        
        if team:
            query = query.filter(Standing.team.ilike(f'%{team}%'))
        if season_start:
            query = query.filter(Standing.season >= season_start)
        if season_end:
            query = query.filter(Standing.season <= season_end)
        if position_start:
            query = query.filter(Standing.position >= position_start)
        if position_end:
            query = query.filter(Standing.position <= position_end)
            
        standings = query.order_by(Standing.season, Standing.position).all()
        
        result = []
        for standing in standings:
            result.append({
                'season': standing.season,
                'position': standing.position,
                'team': standing.team,
                'games_played': standing.games_played,
                'wins': standing.wins,
                'draws': standing.draws,
                'losses': standing.losses,
                'goals_for': standing.goals_for,
                'goals_against': standing.goals_against,
                'goal_difference': standing.goal_difference,
                'points': standing.points
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test database connection
@app.route('/test-db')
@app.route('/api/test-db')
def test_db():
    try:
        # Simple query to test connection
        result = db.session.execute(db.text('SELECT 1')).scalar()
        return jsonify({"message": "Database connection successful!", "result": result})
    except Exception as e:
        return jsonify({"error": f"Database connection failed: {str(e)}"}), 500

# Check what tables exist in the database
@app.route('/tables')
@app.route('/api/tables')
def list_tables():
    try:
        # Query to list all tables in the current database
        result = db.session.execute(db.text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)).fetchall()
        tables = [row[0] for row in result]
        return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
