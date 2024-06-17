from bs4 import BeautifulSoup
import API
import requests
import sqlite3
from tabulate import tabulate

#The web scraper
def exists(server, name, id):
    page = "https://www.op.gg/summoners/" + server + "/" + name + "-" + id
    page_to_scrape = requests.get(page)
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    if soup.find("strong", {"class": "css-ao94tw e1swkqyq1"}) is not None:
        return soup

#Find rank of player
def scrape(server, name, id):
    exist = exists(server, name, id)

    if exist is not None:
        try:
            rank = exist.find("div", {"class": "tier"})
            return rank.text
        
        except Exception:
            return "unranked"
    else:
        return None

#Create and add to database
def register(server, name, riot_id):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puuid TEXT NOT NULL,
            server TEXT NOT NULL,
            name TEXT NOT NULL,
            riotID TEXT NOT NULL,
            rank TEXT NOT NULL,
            rankVal INTEGER NOT NULL
        )
    ''')
    conn.commit()
    exist = exists(server, name, riot_id)
    alreadyReg = playerRegistered(server, name, riot_id)
    puuid = API.getPuuid(name, riot_id)
    rank = scrape(server, name, riot_id)
    rValue = rankValue(rank)


    if exist is not None:
        if alreadyReg == False:
            cursor.execute('INSERT INTO players (puuid, server, name, riotID, rank, rankVal) VALUES (?, ?, ?, ?, ?, ?)', (puuid, server, name, riot_id, rank, rValue))
            conn.commit()
        else:
            conn.close()
            return "Player already registered."
    else:
        conn.close()
        return None

    conn.close()

    result = name + ' has been registered!'

    return result

#Calculate value of player's rank
def rankValue(rank):
    ranklist = ['iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', 'grandmaster', 'challenger']
    value = 0

    word = rank.split()
    if word[0] in ranklist:
        value += (ranklist.index(word[0]))*4
        value += 5 - int(word[1])
    return value

#return player database as a table in the form of a string
def view():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    cursor.execute('SELECT server, name, riotID, rank FROM players ORDER BY rankVal DESC')
    rows = cursor.fetchall()

    headers = [description[0] for description in cursor.description]
    table = tabulate(rows, headers, tablefmt='grid')

    conn.close()
    return f"```\n{table}\n```"

def devView():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM players ORDER BY rankVal DESC')
    rows = cursor.fetchall()

    headers = [description[0] for description in cursor.description]
    table = tabulate(rows, headers, tablefmt='grid')

    conn.close()
    print(f"```\n{table}\n```")
    return None

#Check if player is registered already
def playerRegistered(server, name, riot_id):
    if searchPlayers(server, name, riot_id):
        return True
    else:
        return False

#Search database for player
def searchPlayers(server, name, riot_id):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    cursor.execute('SELECT server, name, riotID FROM players WHERE server = ? AND name = ? AND riotID = ?', (server, name, riot_id))
    matches = cursor.fetchall()
    conn.close()
    return matches

#Update current rankings of all players
def updatePlayers():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, server, name, riotID FROM players')
    players = cursor.fetchall()
    for player in players:
        rank = scrape(player[1], player[2], player[3])
        if rank is not None:
            rankVal = rankValue(rank)
            cursor.execute('UPDATE players SET rank = ?, rankVal = ? WHERE id = ?', (rank, rankVal, player[0]))

        else:
            cursor.execute('UPDATE players SET rank = ? WHERE id = ?', ('NOT_FOUND', player[0]))
    conn.commit()

    conn.close()
    return view()

#List players currently online LIVE
def stalk():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    cursor.execute('SELECT puuid, server, name, riotID FROM players')
    players = cursor.fetchall()
    
    table = [["Player", "Status (OCE ONLY)"]]
    for player in players:
        try:
            link = API.gametype(player[0])
            if link is not None:
                line = [player[2] + '#' + player[3], f"{player[2]} is playing a {link} game."]
                table.append(line)
        except Exception:
            continue

    conn.close()
    
    if len(table) > 1:
        return f"```\n{tabulate(table, headers='firstrow', tablefmt='grid')}\n```"
    else:
        return "No online player detected!"

#Remove players not found on op.gg
def clearBogies():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM players WHERE rank = ?', ('NOT_FOUND',))
    conn.commit()
    
    conn.close()
    return 'NOT_FOUND players removed!'

#Remove a player
def deletePlayer(name):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM players WHERE name = ?', (name,))

    conn.commit()
    
    conn.close()
    return 'Player has been removed!'
