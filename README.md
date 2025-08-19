
# La Liga Analysis

A Flask web application for analyzing Spanish La Liga standings, team performance, and historical data with interactive visualizations. Data is fetched with scraper.

## Features

- **Interactive Standings** - Browse and filter standings by season, team, and position
- **Statistical Charts** - Team performance trends with Chart.js visualizations
- **Data Export** - Download filtered data as CSV files
- **API Monitoring** - Real-time database connection status
- **Responsive Design** - Mobile-friendly Bootstrap interface

## Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database setup**
   - Create PostgreSQL database named `laliga`
   - Configure connection in `config/db.env`:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/laliga
   ```

3. **Run application**
   ```bash
   cd src && python app.py
   ```

4. **Access app**
   ```
   http://localhost:5000
   ```

## Database Schema

Requires a `standings` table with columns:
- `season`, `position`, `team`
- `games_played`, `wins`, `draws`, `losses`
- `goals_for`, `goals_against`, `goal_difference`, `points`

## Pages

- **Home** - Team search and quick statistics
- **Standings** - Full table with advanced filtering
- **Statistics** - Championship charts and performance trends
- **API Status** - System health monitoring

## Tech Stack

**Backend:** Flask + SQLAlchemy  
**Database:** PostgreSQL  
**Frontend:** Bootstrap 5 + Chart.js

## Tech Stack

Flask • PostgreSQL • Bootstrap • Chart.js