from graphics_isn import *

# Permet de changer la valeur des cases vides et sers de guide pour le board.
# Toutefois, il faut aussi modifier le contenu de 'board'.
tiles_dict = {"black_pawn": 0, "white_pawn": 1, "blank": 2, "exploded": 3}

board = [
                [2, 2, 2, 0, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 1, 2, 2, 2]
        ]

tile_color = couleur_RGB(255, 206, 158)         # Couleur des cases libres
border_color = couleur_RGB(208, 138, 71)        # Couleur de la bordure


def show_board():
    """
    Affiche la variable 'board' dans la console. 
    Ne sers qu'à debug le script.
    """
    print("\n")
    for elt in board:
        print(f"  {elt}")


def init_board():
    """
    Dessine le plateau et positionne les pions pour un début de partie
    """

    init_graphic(800, 650, "Isola", white)

    # Dessine le plateau
    x = 85
    y = 85
    for k in range(7):
        for i in range(7):
            P1 = Point(x, y)
            draw_fill_rectangle(P1, 90, 90, border_color)
            draw_fill_rectangle(P1, 70, 70, tile_color)
            x += 80
        x = 85
        y += 80

    # Dessine les pions
    draw_pawn(1, 6, 3)
    draw_pawn(2, 0, 3)

    # Dessine l'indicateur de tour
    turn_indicator_box = Point(705, 195)
    draw_fill_rectangle(turn_indicator_box, 150, 75, black)
    draw_fill_rectangle(turn_indicator_box, 140, 65, couleur_RGB(63, 63, 63))
    
    turn_indicator_txt = Point(646, 168)
    aff_pol("Au tour de :", 18, turn_indicator_txt, white, text_bold=True)


def explode_tile(row, column):
    """
    Détruit une case graphiquement et change sa valeur dans 'board'
    
    row : ligne de la case
    column : colonne de la case
    """
    x = 85 + 80 * column
    y = 85 + 80 * row
    P1 = Point(x, y)
    draw_fill_rectangle(P1, 70, 70, border_color)
    board[row][column] = 3


def getPos(player):
    """
    Renvoie la ligne et la colonne du joueur selon la variable 'board'
    
    player : joueur dont on veut la position
    """
    playerPos = []
    for i in range(len(board)):
        if player in board[i]:
            playerPos.append(i)
            playerPos.append(board[i].index(player))
            return playerPos


def draw_pawn(player, row, column):
    """Dessine un pion sur la case dont la colonne est 'column' et la ligne 'row'

    Args :
        player : joueur qu'il faut dessiner
        row : ligne où l'on veut dessiner le pion
        column : colonne où l'on veut dessiner le pion
    """
    color = white if player == 1 else black

    x = 85 + 80 * column
    y = 85 + 80 * row
    P1 = Point(x, y)
    draw_fill_circle(P1, 25, color)


def clear_tile(row, column):
    """Dessine une case vide sur la case dont la colonne est 'column' et la ligne 'row'

    Args :
        row : ligne de la case 
        column : colonne de la case
    """
    x = 85 + 80 * column
    y = 85 + 80 * row
    P1 = Point(x, y)
    draw_fill_rectangle(P1, 70, 70, tile_color)
    
    
def turn_icon(player):
    """Dessine un symbole indiquant le joueur dont c'est le tour

    Args :
        player : joueur dont c'est le tour
    """
    icon_color = {0: "black", 1: "white"}
    P5 = Point(703, 210)
    draw_fill_circle(P5, 10, icon_color[player])


def move(player, row, column):
    """
    Déplace un joueur sur la case dont la colonne est 'column' et la ligne 'row'

    Args :
        player (int): joueur qu'on déplace
        row : ligne où l'on veut déplacer le pion
        column : colonne où l'on veut déplacer le pion
    """
    playerPos = getPos(player)                                                                      # récupère la position avant déplacement du joueur
    playerColumn = playerPos[1]
    playerRow = playerPos[0]                            

    board[row][column] = player                                                                     # déplace le pion dans 'board'
    draw_pawn(player, row, column)                                                                  # dessine le pion sur sa nouvelle position
    board[playerRow][playerColumn] = tiles_dict["blank"]                                            # remplace l'ancienne case par une case vide dans 'board'
    clear_tile(playerRow, playerColumn)                                                             # remplace l'ancienne case par une case vide graphiquement


def lose_condition(player):
    """Vérifie si le joueur 'player' a perdu

    Args :
        player (int) : joueur dont on vérifie la condition de défaite

    Returns :
        bool : True si le joueur a perdu sinon False
    """
    playerPos = getPos(player)                                                                      # récupère la position avant déplacement du joueur
    playerColumn = playerPos[1]
    playerRow = playerPos[0]
    
    possibilities = []                                                                              # ensemble des cases autour du pion
    for row in range(-1, 2):
        if row + playerRow != -1:                                                                   # pour éviter de regarder la dernière ligne même si elle n'est pas à côté
            for column in range(-1, 2):
                if column + playerColumn != -1:                                                     # pour éviter de regarder la dernière colonne même si elle n'est pas à côté
                    try:
                        possibilities.append(board[playerRow + row][playerColumn + column])
                    except IndexError:                                                              # pour éviter que le script s'arrête si on tente de vérifier une ligne/colonne après la dernière
                        pass

    has_lose = False if 2 in possibilities else True
    
    return has_lose


def winner(player):
    """Annonce le gagnant

    Args :
        player : joueur qui a gagné
        
    Returns :
        bool : 1 si le joueur a perdu sinon 0
    """

    looser = 1 if player == 0 else 2                                                                # Définit qui a perdu pour le message print
    
    if player == 0:                                                                                 # Dans notre jeu le joueur 2 a pour valeur 0
        player = 2                                                                                  # Donc on fait le changement si joueur 2 gagne

    print(f"Le joueur {looser} n'est plus capable de bouger. La victoire revient donc au joueur {player} !")
    
    win_txt_point = Point(640, 270)  
    aff_pol(f"Player {player} won", 20, win_txt_point, black)                                       # Affiche le gagnant sur la fenêtre graphique


# -----------------------------------------------------------------------------------------

def turn(player):
    """Effectue le tour du joueur 'player'
    
    Args :
        player : joueur dont c'est le tour
    """
    
    lose = lose_condition(player)                                                                   # Vérifie si le joueur a perdu
    if lose is True:
        return 1                                                                                    # S'il a perdu, sort de la fonction et renvoie 1

    playerPos = getPos(player)                                                                      # Récupère la position du joueur
    playerColumn = playerPos[1]
    playerRow = playerPos[0]

    has_move = 0
    while has_move == 0:                                                                            # On attend jusqu'à ce que le joueur se soit déplacé 
        click = wait_clic()
        x = click[0]
        y = click[1]

        clickInGrid = 50 < x < 600 and 50 < y < 600  # définit la zone dans le plateau
        clickNotOnBorder = ((x - 40) % 80) > 10 and ((y - 40) % 80) > 10                            # Vérifie si le clic n'était pas sur une bordure entre 2 cases

        if clickInGrid and clickNotOnBorder:                                                        # vérifie si le clic du joueur était sur une case et non une bordure/en dehors du plateau
            clickColumn = (x - 40) // 80
            clickRow = (y - 40) // 80
            posTooFar = abs(playerColumn - clickColumn) > 1 or abs(playerRow - clickRow) > 1        # vérifie si l'endroit où veut aller le joueur n'est pas trop loin
            canMove = board[clickRow][clickColumn] != tiles_dict["blank"] or posTooFar              # vérifie si la case cliquée est libre n'est pas trop loin

            if not canMove:
                move(player, clickRow, clickColumn)
                has_move = 1

    has_explode = 0
    while has_explode == 0:                                                                         # On attend jusqu'à ce que le joueur ait détruit une case
        click = wait_clic()
        x = click[0]
        y = click[1]

        clickInGrid = 50 < x < 600 and 50 < y < 600  # définit la zone dans le plateau
        clickNotOnBorder = ((x - 40) % 80) > 10 and ((y - 40) % 80) > 10                            # Vérifie si le clic n'était pas sur une bordure entre 2 cases

        if clickInGrid and clickNotOnBorder:                                                        # vérifie si le clic du joueur était sur une case et non une bordure/en dehors du plateau
            clickColumn = (x - 40) // 80
            clickRow = (y - 40) // 80

            if board[clickRow][clickColumn] != tiles_dict["blank"]:                                 # vérifie si la case est une case vide
                pass
            else:
                explode_tile(clickRow, clickColumn)
                has_explode = 1

    return 0


# -----------------------------------------------------------------------------------------

def main():
    init_board()

    player = 0
    end = 0

    while end == 0:
        player = 1 - player
        turn_icon(player)
        end = turn(player)
        
    winner(1 - player)

    wait_escape("")
    return 0

# -----------------------------------------------------------------------------------------


main()
