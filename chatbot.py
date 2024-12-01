from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats, leaguegamefinder, leaguestandings, boxscoretraditionalv2
import pandas as pd
import speech_recognition as sr
from rich.console import Console

console = Console()


def search_player(player_name):
    """Rechercher un joueur par nom."""
    player_list = players.find_players_by_full_name(player_name)
    if player_list:
        console.print("\nRésultats de recherche :", style="bold green")
        for player in player_list:
            console.print(f"ID : {player['id']} - Nom : {player['full_name']}", style="cyan")
    else:
        console.print("Aucun joueur trouvé.", style="bold red")


def get_player_stats_by_name(player_name):
    """Obtenir les statistiques d'un joueur en utilisant son nom."""
    player_list = players.find_players_by_full_name(player_name)
    if player_list:
        player_id = player_list[0]['id']
        try:
            career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
            stats = career_stats.get_data_frames()[0]
            console.print(f"\nStatistiques de carrière de {player_name} :", style="bold green")
            console.print(stats, style="cyan")
        except Exception as e:
            console.print("Impossible de récupérer les statistiques.", style="bold red")
            console.print(f"Erreur : {e}", style="bold red")
    else:
        console.print("Joueur non trouvé. Vérifiez le nom.", style="bold red")


def get_team_games(team_name):
    """Lister les derniers matchs d'une équipe."""
    team_list = teams.find_teams_by_full_name(team_name)
    if team_list:
        team_id = team_list[0]['id']
        try:
            games = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id).get_data_frames()[0]
            console.print(f"\nDerniers matchs de {team_name} :", style="bold green")
            console.print(games[['GAME_DATE', 'MATCHUP', 'WL']], style="cyan")
        except Exception as e:
            console.print("Impossible de récupérer les matchs.", style="bold red")
            console.print(f"Erreur : {e}", style="bold red")
    else:
        console.print("Équipe non trouvée.", style="bold red")


def get_team_info(team_name):
    """Obtenir des informations sur une équipe."""
    team_list = teams.find_teams_by_full_name(team_name)
    if team_list:
        team = team_list[0]
        console.print(f"\nInformations sur l'équipe {team['full_name']} :", style="bold green")
        for key, value in team.items():
            console.print(f"{key.capitalize()} : {value}", style="cyan")
    else:
        console.print("Équipe non trouvée.", style="bold red")


def get_standings():
    """Afficher le classement des équipes NBA."""
    console.print("\nClassement des équipes NBA :", style="bold green")
    standings = leaguestandings.LeagueStandings().get_data_frames()[0]
    for index, team in standings.iterrows():
        console.print(f"{index + 1}. {team['TeamName']} - {team['Conference']} - {team['WinPCT']*100:.2f}% victoires", style="cyan")


def get_match_details(game_id):
    """Afficher les détails d'un match spécifique."""
    try:
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
        stats = boxscore.get_data_frames()[0]
        console.print("\nDétails du match :", style="bold green")
        for player in stats.itertuples():
            console.print(f"{player.PLAYER_NAME} - Points: {player.PTS}, Rebonds: {player.REB}, Passes: {player.AST}", style="cyan")
    except Exception as e:
        console.print("Impossible de récupérer les détails du match.", style="bold red")
        console.print(f"Erreur : {e}", style="bold red")


def get_mvp_history():
    """Afficher les MVP des saisons passées."""
    mvp_list = [
        {"Season": "2022-2023", "Player": "Joel Embiid"},
        {"Season": "2021-2022", "Player": "Nikola Jokic"},
        {"Season": "2020-2021", "Player": "Nikola Jokic"},
        {"Season": "2019-2020", "Player": "Giannis Antetokounmpo"},
    ]
    console.print("\nHistorique des MVP :", style="bold green")
    for mvp in mvp_list:
        console.print(f"{mvp['Season']} : {mvp['Player']}", style="cyan")


def listen_for_query():
    """Rechercher une question en utilisant la reconnaissance vocale."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        console.print("Parlez maintenant...", style="bold yellow")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language="fr-FR")
        console.print(f"Vous avez dit : {query}", style="bold green")
        return query
    except sr.UnknownValueError:
        console.print("Je n'ai pas compris. Réessayez.", style="bold red")
        return None
    except sr.RequestError:
        console.print("Erreur de service vocal.", style="bold red")
        return None


if __name__ == "__main__":
    console.print("Bienvenue dans le chatbot NBA ! 🏀", style="bold blue")

    while True:
        console.print("\nQue voulez-vous faire ?", style="bold yellow")
        console.print("1. Rechercher un joueur")
        console.print("2. Obtenir les statistiques d'un joueur par nom")
        console.print("3. Lister les derniers matchs d'une équipe")
        console.print("4. Obtenir des informations sur une équipe")
        console.print("5. Classement des équipes NBA")
        console.print("6. Détails d'un match")
        console.print("7. Historique des MVP")
        console.print("8. Recherche vocale")
        console.print("9. Quitter")

        choice = input("Entrez le numéro de votre choix : ")

        if choice == "1":
            player_name = input("Entrez le nom d'un joueur : ")
            search_player(player_name)
        elif choice == "2":
            player_name = input("Entrez le nom d'un joueur : ")
            get_player_stats_by_name(player_name)
        elif choice == "3":
            team_name = input("Entrez le nom d'une équipe : ")
            get_team_games(team_name)
        elif choice == "4":
            team_name = input("Entrez le nom d'une équipe : ")
            get_team_info(team_name)
        elif choice == "5":
            get_standings()
        elif choice == "6":
            game_id = input("Entrez l'ID du match : ")
            get_match_details(game_id)
        elif choice == "7":
            get_mvp_history()
        elif choice == "8":
            query = listen_for_query()
            if query:
                console.print(f"Recherche pour : {query}", style="cyan")
        elif choice == "9":
            console.print("Au revoir ! 🏀", style="bold blue")
            break
        else:
            console.print("Option invalide. Veuillez réessayer.", style="bold red")
