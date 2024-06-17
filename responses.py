import opggScraper
import API

def handle_responses(message) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return "Sure."

    if p_message.startswith('hello') and 'clive' in p_message:
        return "Sure."

    if p_message.startswith('$rank'):
        parts = p_message.split()
        try:
            scrape = opggScraper.scrape(parts[1].lower(), parts[2], parts[3])
            if scrape is not None:
                result = parts[2] + "'s " + "rank is " + scrape
                return result
            else:
                return "Can't find player. Check input."
        except Exception:
            return "Invalid input. '$help' for more information."
    
    if p_message.startswith('$register'):
        parts = p_message.split()
        try:
            middle = parts[2:-1]
            last = len(parts)
            name = ' '.join(middle)
            print(name)
            return opggScraper.register(parts[1], name.lower(), parts[last - 1])
        except Exception:
            return "Invalid input. '$help' for more information."
        
    if p_message == '$players':
        return opggScraper.view()
    
    if p_message == '$update':
        return opggScraper.updatePlayers()
    
    if p_message == '$clearErrors':
        return opggScraper.clearBogies()
    
    if p_message == '$stalk':
        return opggScraper.stalk()
    
    if p_message.startswith('$delete'):
        parts = p_message.split()
        try:
            middle = parts[1:]
            name = ' '.join(middle)
            return opggScraper.deletePlayer(name.lower())

        except Exception:
            return "Invalid input. '$help' for more information."
    
    if p_message == '$help':
        return """```
#Clive is slow with some commands so be patient
#Look up rank of person on op.gg
$rank [Server] [Summoner Name] [Riot ID] 

#Register player into Clive's player list
$register [Server] [Summoner Name] [Riot ID] 

#Look at Clive's player list
$players

#Update ranks in player list
$update

#Remove a player from list
$delete [Summoner Name]

#See players currently playing (OCE ONLY)
$stalk

#Remove NOT_FOUND players from list (Deleted/NameChanged Accounts)
$clearErrors```"""

    if p_message.startswith('!#$test'):
        parts = p_message.split()
        try:
            return API.getPuuid(parts[1], parts[2])
        except Exception:
            return "Invalid input. '$help' for more information."
        
    if p_message == '!#$view':
        print('hello')
        return opggScraper.devView()
        

        
