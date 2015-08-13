from fantasy_sport import FantasySport
from yahoo_oauth import OAuth1
from fantasy_sport.utils import pretty_json, pretty_xml
import json
import datetime

# Inputs
gameID = 346
leagueID = 1328
teamID = 12
playerID = 8781
input_date = '2015-08-13'
###

today = False
current_date = str(datetime.date.today())

if current_date == input_date:
    today = True
    
    
def make_league_code(gameid, leagueid):
    return [str(gameid) + '.l.' + str(leagueid)]

def make_team_code(gameid, leagueid, teamid):
    return [str(gameid) + '.l.' + str(leagueid) + '.t.' + str(teamid)]
    
def make_player_code(gameid, playerid):
    return [str(gameid) + '.p.' + str(playerid)]
    
    
def get_roster_data():
    """Pull league info and parse into useable roster
    """
    team_code = make_team_code(gameID, leagueID, teamID) #make team code
    response = yfs.get_roster_players(team_code, date=input_date) #call API function
    data = response.json() #get response
    return parse_set_roster(data) #organize response 
    
def parse_set_roster(data):
    """cleans API set_roster response
    """
    roster_info = (data['fantasy_content']['team'][1]['roster']['0']['players'])
    
    batters = []
    pitchers = []
    
    for p in roster_info:
        player_info = roster_info[p]
        
        #ignore players on DL for setting lineup
        try:
            if 'on_disabled_list' in player_info['player'][0][4]: continue
        except TypeError:
            continue
        
        try: #don't get caught on irregular output
            name_info = player_info['player'][0][2]
        except TypeError:
            continue
            
        name = name_info['name']['ascii_first'] + ' ' + name_info['name']['ascii_last']
        
        try:
            position_info = player_info['player'][0][12]
        except TypeError:
            continue
            
        eligible_positions = position_info['eligible_positions']
        
        positions = set()
        #create set of eligible positions for each player
        [positions.add(x['position']) for x in eligible_positions]

        #include current position of player
        current_position = player_info['player'][1]['selected_position'][1]['position']
        
        #include if has game, and if running on today's date, then if starting
        starting = True
        editable = True
        
        if today:
            try:
                if 'starting_status' in player_info['player'][2]:
                    if 0 == player_info['player'][2]['starting_status'][1]['is_starting']:
                        starting = False
                        print starting
                if 0 == player_info['player'][3]['is_editable']:
                    editable = False
                    
            except TypeError:
                continue
                    
        #tuple of information for a player
        #player = (name, (current_position, positions))
        
        player = (name, ((current_position, positions), (starting, editable)))
        
        #append to list based on batter or pitcher
        try:
            if 'B' in player_info['player'][0][11]['position_type']:
                batters.append(player)
            else:
                pitchers.append(player)
        except TypeError:
            continue
       
    return (batters, pitchers)
    
"""    
#def get_player_projections(batter_names, pitcher_names):
def get_player_projections():
    #Connect to Rudy's db and get projections
    
    batters_proj = []
    pitchers_proj = []
    
    batters_projection_list = [30,20,10,25,15,5,6,7,13,19,40,34,14,26,33]
    
    for i in batter_names:
        batters_proj.append(batters_projection_list[i])
    
    return (batters_proj, pitchers_proj)
    
#def optimal_batting(batters):
def optimal_batting():
    #Finds optimal hitting lineup
    
    position_list = ['C', '1B', '2B']
    
    #Batters = (name, ((current_pos, positions), projection)
    
    for i in position_list:
        eligible_players = [(name, proj) for (name, ((current_pos, elig_pos), projection) in inputs if i in elig_pos]
        
    return None
    
#def optimal_pitching(pitchers):
def optimal_pitching():
    return None
    
def optimal_lineup():
    #Take in current roster, projections
    #find optimal hitting and pitching lineup
    
    batting, pitching = get_roster_data()
    
    batter_names = [name for (name, _) in batting]
    
    bat_projection, pitch_projection = get_player_projections()
    
    batters = zip(batting, bat_projection)
    
    #x = optimal_batting(batters)
    #y = optimal_pitching(pitchers)
    
    return None
     
"""
###             

oauth = OAuth1(None, None, from_file='oauth.json',base_url='http://fantasysports.yahooapis.com/fantasy/v2/')
yfs = FantasySport(oauth)

roster_data = get_roster_data()
print roster_data