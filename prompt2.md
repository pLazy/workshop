
### System:

# SQL Query Generator Assistant
      
  You are a specialized SQL query generator that creates correct, executable SQL queries based on database schemas and natural language requests.
  
  ## Your Task
  - Analyze the provided database schema
  - Interpret the user's natural language request
  - Generate a precise SQL query that answers the user's question
  - Ensure the query is syntactically correct and optimized
  
  ## Guidelines
  - Use only tables and columns defined in the schema
  - Consider appropriate JOINs when data spans multiple tables
  - Apply proper filtering conditions based on the request
  - Format your response as a valid SQL query
  - Identify the connections between tables based on the name of the columns
      
    
### User:
The database schema is as follows:
```sql
CREATE TABLE all_star (
    player_id TEXT,
    year INTEGER,
    game_num INTEGER,
    game_id TEXT,
    team_id TEXT,
    league_id TEXT,
    gp NUMERIC,
    starting_pos NUMERIC);

CREATE TABLE appearances (
    year INTEGER,
    team_id TEXT,
    league_id TEXT,
    player_id TEXT,
    g_all NUMERIC,
    gs NUMERIC,
    g_batting INTEGER,
    g_defense NUMERIC,
    g_p INTEGER,
    g_c INTEGER,
    g_1b INTEGER,
    g_2b INTEGER,
    g_3b INTEGER,
    g_ss INTEGER,
    g_lf INTEGER,
    g_cf INTEGER,
    g_rf INTEGER,
    g_of INTEGER,
    g_dh NUMERIC,
    g_ph NUMERIC,
    g_pr NUMERIC);

CREATE TABLE manager_award (
    player_id TEXT,
    award_id TEXT,
    year INTEGER,
    league_id TEXT,
    tie TEXT,
    notes NUMERIC);

CREATE TABLE player_award (
    player_id TEXT,
    award_id TEXT,
    year INTEGER,
    league_id TEXT,
    tie TEXT,
    notes TEXT);

CREATE TABLE manager_award_vote (
    award_id TEXT,
    year INTEGER,
    league_id TEXT,
    player_id TEXT,
    points_won INTEGER,
    points_max INTEGER,
    votes_first INTEGER);

CREATE TABLE player_award_vote (
    award_id TEXT,
    year INTEGER,
    league_id TEXT,
    player_id TEXT,
    points_won NUMERIC,
    points_max INTEGER,
    votes_first NUMERIC);

CREATE TABLE batting (
    player_id TEXT,
    year INTEGER,
    stint INTEGER,
    team_id TEXT,
    league_id TEXT,
    g INTEGER,
    ab NUMERIC,
    r NUMERIC,
    h NUMERIC,
    double NUMERIC,
    triple NUMERIC,
    hr NUMERIC,
    rbi NUMERIC,
    sb NUMERIC,
    cs NUMERIC,
    bb NUMERIC,
    so NUMERIC,
    ibb NUMERIC,
    hbp NUMERIC,
    sh NUMERIC,
    sf NUMERIC,
    g_idp NUMERIC);

CREATE TABLE batting_postseason (
    year INTEGER,
    round TEXT,
    player_id TEXT,
    team_id TEXT,
    league_id TEXT,
    g INTEGER,
    ab INTEGER,
    r INTEGER,
    h INTEGER,
    double INTEGER,
    triple INTEGER,
    hr INTEGER,
    rbi INTEGER,
    sb INTEGER,
    cs NUMERIC,
    bb INTEGER,
    so INTEGER,
    ibb NUMERIC,
    hbp NUMERIC,
    sh NUMERIC,
    sf NUMERIC,
    g_idp NUMERIC);

CREATE TABLE player_college (
    player_id TEXT,
    college_id TEXT,
    year INTEGER);

CREATE TABLE fielding (
    player_id TEXT,
    year INTEGER,
    stint INTEGER,
    team_id TEXT,
    league_id TEXT,
    pos TEXT,
    g INTEGER,
    gs NUMERIC,
    inn_outs NUMERIC,
    po NUMERIC,
    a NUMERIC,
    e NUMERIC,
    dp NUMERIC,
    pb NUMERIC,
    wp NUMERIC,
    sb NUMERIC,
    cs NUMERIC,
    zr NUMERIC);

CREATE TABLE fielding_outfield (
    player_id TEXT,
    year INTEGER,
    stint INTEGER,
    glf NUMERIC,
    gcf NUMERIC,
    grf NUMERIC);

CREATE TABLE fielding_postseason (
    player_id TEXT,
    year INTEGER,
    team_id TEXT,
    league_id TEXT,
    round TEXT,
    pos TEXT,
    g INTEGER,
    gs NUMERIC,
    inn_outs NUMERIC,
    po INTEGER,
    a INTEGER,
    e INTEGER,
    dp INTEGER,
    tp INTEGER,
    pb NUMERIC,
    sb NUMERIC,
    cs NUMERIC);

CREATE TABLE hall_of_fame (
    player_id TEXT,
    yearid INTEGER,
    votedby TEXT,
    ballots NUMERIC,
    needed NUMERIC,
    votes NUMERIC,
    inducted TEXT,
    category TEXT,
    needed_note TEXT);

CREATE TABLE home_game (
    year INTEGER,
    league_id TEXT,
    team_id TEXT,
    park_id TEXT,
    span_first TEXT,
    span_last TEXT,
    games INTEGER,
    openings INTEGER,
    attendance INTEGER);

CREATE TABLE manager (
    player_id TEXT,
    year INTEGER,
    team_id TEXT,
    league_id TEXT,
    inseason INTEGER,
    g INTEGER,
    w INTEGER,
    l INTEGER,
    rank NUMERIC,
    plyr_mgr TEXT);

CREATE TABLE manager_half (
    player_id TEXT,
    year INTEGER,
    team_id TEXT,
    league_id TEXT,
    inseason INTEGER,
    half INTEGER,
    g INTEGER,
    w INTEGER,
    l INTEGER,
    rank INTEGER);

CREATE TABLE player (
    player_id TEXT,
    birth_year NUMERIC,
    birth_month NUMERIC,
    birth_day NUMERIC,
    birth_country TEXT,
    birth_state TEXT,
    birth_city TEXT,
    death_year NUMERIC,
    death_month NUMERIC,
    death_day NUMERIC,
    death_country TEXT,
    death_state TEXT,
    death_city TEXT,
    name_first TEXT,
    name_last TEXT,
    name_given TEXT,
    weight NUMERIC,
    height NUMERIC,
    bats TEXT,
    throws TEXT,
    debut TEXT,
    final_game TEXT,
    retro_id TEXT,
    bbref_id TEXT);

CREATE TABLE park (
    park_id TEXT,
    park_name TEXT,
    park_alias TEXT,
    city TEXT,
    state TEXT,
    country TEXT);

CREATE TABLE pitching (
    player_id TEXT,
    year INTEGER,
    stint INTEGER,
    team_id TEXT,
    league_id TEXT,
    w INTEGER,
    l INTEGER,
    g INTEGER,
    gs INTEGER,
    cg INTEGER,
    sho INTEGER,
    sv INTEGER,
    ipouts NUMERIC,
    h INTEGER,
    er INTEGER,
    hr INTEGER,
    bb INTEGER,
    so INTEGER,
    baopp NUMERIC,
    era NUMERIC,
    ibb NUMERIC,
    wp NUMERIC,
    hbp NUMERIC,
    bk INTEGER,
    bfp NUMERIC,
    gf NUMERIC,
    r INTEGER,
    sh NUMERIC,
    sf NUMERIC,
    g_idp NUMERIC);

CREATE TABLE pitching_postseason (
    player_id TEXT,
    year INTEGER,
    round TEXT,
    team_id TEXT,
    league_id TEXT,
    w INTEGER,
    l INTEGER,
    g INTEGER,
    gs INTEGER,
    cg INTEGER,
    sho INTEGER,
    sv INTEGER,
    ipouts INTEGER,
    h INTEGER,
    er INTEGER,
    hr INTEGER,
    bb INTEGER,
    so INTEGER,
    baopp TEXT,
    era NUMERIC,
    ibb NUMERIC,
    wp NUMERIC,
    hbp NUMERIC,
    bk NUMERIC,
    bfp NUMERIC,
    gf INTEGER,
    r INTEGER,
    sh NUMERIC,
    sf NUMERIC,
    g_idp NUMERIC);

CREATE TABLE salary (
    year INTEGER,
    team_id TEXT,
    league_id TEXT,
    player_id TEXT,
    salary INTEGER);

CREATE TABLE college (
    college_id TEXT,
    name_full TEXT,
    city TEXT,
    state TEXT,
    country TEXT);

CREATE TABLE postseason (
    year INTEGER,
    round TEXT,
    team_id_winner TEXT,
    league_id_winner TEXT,
    team_id_loser TEXT,
    league_id_loser TEXT,
    wins INTEGER,
    losses INTEGER,
    ties INTEGER);

CREATE TABLE team (
    year INTEGER,
    league_id TEXT,
    team_id TEXT,
    franchise_id TEXT,
    div_id TEXT,
    rank INTEGER,
    g INTEGER,
    ghome NUMERIC,
    w INTEGER,
    l INTEGER,
    div_win TEXT,
    wc_win TEXT,
    lg_win TEXT,
    ws_win TEXT,
    r INTEGER,
    ab INTEGER,
    h INTEGER,
    double INTEGER,
    triple INTEGER,
    hr INTEGER,
    bb INTEGER,
    so NUMERIC,
    sb NUMERIC,
    cs NUMERIC,
    hbp NUMERIC,
    sf NUMERIC,
    ra INTEGER,
    er INTEGER,
    era NUMERIC,
    cg INTEGER,
    sho INTEGER,
    sv INTEGER,
    ipouts INTEGER,
    ha INTEGER,
    hra INTEGER,
    bba INTEGER,
    soa INTEGER,
    e INTEGER,
    dp NUMERIC,
    fp NUMERIC,
    name TEXT,
    park TEXT,
    attendance NUMERIC,
    bpf INTEGER,
    ppf INTEGER,
    team_id_br TEXT,
    team_id_lahman45 TEXT,
    team_id_retro TEXT);

CREATE TABLE team_franchise (
    franchise_id TEXT,
    franchise_name TEXT,
    active TEXT,
    na_assoc TEXT);

CREATE TABLE team_half (
    year INTEGER,
    league_id TEXT,
    team_id TEXT,
    half INTEGER,
    div_id TEXT,
    div_win TEXT,
    rank INTEGER,
    g INTEGER,
    w INTEGER,
    l INTEGER);

```

    
# Examples
Here are some examples of how to generate SQL queries:
Given the text: "Show all players that won an award and the college they attended."
The SQL query should be: 
```sql
  SELECT DISTINCT p.name_first || ' ' || p.name_last AS player_name,
      pa.award_id,
      pa.year,
      c.name_full AS college_name
  FROM player_award pa
  JOIN player p ON pa.player_id = p.player_id
  JOIN player_college pc ON pa.player_id = pc.player_id
  JOIN college c ON pc.college_id = c.college_id
  ORDER BY pa.year DESC, player_name 
```


Given the text: "Show Hall of Fame players and their salary for the years they played. The result should be ordered by year."
The SQL query should be: 
```sql
  SELECT p.name_first || ' ' || p.name_last AS player_name,
      s.year,
      s.salary,
      h.inducted
  FROM hall_of_fame h
  JOIN player p ON h.player_id = p.player_id
  JOIN salary s ON p.player_id = s.player_id
  WHERE h.inducted = 'Y'
```

Given the text: "Show which players participated in the All-Star game."
The SQL query should be:

```sql
  SELECT DISTINCT p.name_first || ' ' || p.name_last AS player_name,
       a.league_id
  FROM all_star a
  JOIN player p ON a.player_id = p.player_id
```


Given the text: "List manager names, the award they won, and the team they managed that season."
The SQL query should be: 

```sql
  SELECT p.name_first || ' ' || p.name_last AS manager_name,
        ma.award_id,
        t.name AS team_name,
        ma.year
  FROM manager_award ma
  JOIN manager m ON ma.player_id = m.player_id AND ma.year = m.year
  JOIN team t ON m.team_id = t.team_id AND m.year = t.year
  JOIN player p ON m.player_id = p.player_id
```
    

**Important**: Always return the result as a JSON object with the following keys:
* "description": a short explanation of how the sql is generated
* "sql": → the SQL query itself as a string.

**Example**: 
```json
    {
  "description": "Select the table 'manager'. Join it with the table 'team'. Filter on the team name to be 'Boston Red Stockings'. Selects the manager first name and last name and concatenate them.",
  "sql": "SELECT m.name_first || ' ' ||mp.name_last AS manager_name FROM manager m JOIN team t ON m.team_id = t.team_id WHERE t.name = 'Boston Red Stockings'"
  }
```

# User Request
""" 
{user_request}
""" 
