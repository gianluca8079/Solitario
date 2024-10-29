import pygame
import random
import sys
import os


# Inizializza Pygame
pygame.init()

# Impostazioni della finestra di gioco
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
fps = 60
timer = pygame.time.Clock()
rows = 8
cols = 5
correct = [[0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0],
           [0,0,0,0,0]]
options_list = []
spaces = []
used = []
new_board = True
first_guess = False
second_guess = False
first_guess_num = 0
second_guess_num = 0
score = 0
matches = 0
game_over = False
max_swaps = 3
swap_count = 0

#create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gioco di Carte")
title_font = pygame.font.Font('freesansbold.ttf',56)
small_font = pygame.font.Font('freesansbold.ttf',28)


# Colori
GREEN = (34, 139, 34)  # Colore del tavolo verde
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
gray = (128,128,128)
green = (0,255,0)

def load_images():
    """Mappa ogni combinazione di carta con il suo percorso immagine"""
    image_directory = "carte/carte_napoletane"  # Sostituisci con il percorso della tua cartella di immagini
    image_map = {}

    if not os.path.isdir(image_directory) and not hasattr(sys, '_MEIPASS'):
        raise ValueError(f"La directory '{image_directory}' non esiste. Controlla il percorso.")

    # Definisci i semi e i valori delle carte
    semi = ['denari', 'spade', 'coppe', 'bastoni']
    valori = ['Asso', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    

    # Crea la mappatura tra carte e immagini
    for seme in semi:
        for valore in valori:
            # Creare il nome file dell'immagine basato su valore e seme
            file_name = f"{valore}_di_{seme.lower()}.jpg"  # Es: '1_di_cuori.png'

            if hasattr(sys, '_MEIPASS'):
                # Quando è in eseguibile
                 file_path = os.path.join(sys._MEIPASS, "carte/carte_napoletane", file_name)
                 file_path_p = os.path.join(sys._MEIPASS, "carte/carte_napoletane", "retro.jpg")



            else:
                file_path = os.path.join(image_directory, file_name)
                file_path_p = os.path.join(image_directory, "retro.jpg")

            try:
                image_map[(valore, seme)] = pygame.image.load(file_path)
                image_map[('X', 'placeholder')] = pygame.image.load(file_path_p)

            except pygame.error as e:
                print(f"Errore nel caricare l'immagine {file_name}: {e}")
                image_map[(valore, seme)] = None  # Placeholder in caso l'immagine non venga trovata
                                

    return image_map


def generate_cards():
    """Genera una lista di 40 carte, 4 semi e 10 carte per seme"""
    semi = ['coppe', 'spade', 'denari', 'bastoni']
    valori = ['Asso', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    board = [(valore, seme) for seme in semi for valore in valori]

    return board

def generate_placeholder():
    placeholder = ('X', 'placeholder')
    return placeholder


def generate_board(image_map):
    global options_list
    global spaces
    
    options_list = generate_cards()

    random.shuffle(options_list)

    spaces = options_list[:rows * cols]

    
        


def draw_backgrounds():
    top_menu = pygame.draw.rect(screen ,gray, [0, 0, SCREEN_WIDTH,100])
    title_text = title_font.render('Solitario', True, white)
    screen.blit(title_text, (10,20))
    board_space = pygame.draw.rect(screen ,GREEN, [0, 100, SCREEN_WIDTH,SCREEN_HEIGHT-200],0)
    bottom_menu = pygame.draw.rect(screen ,white, [0, SCREEN_HEIGHT-100, SCREEN_WIDTH,100],0)
    restart_button = pygame.draw.rect(screen,gray, [10, SCREEN_HEIGHT-90,200,80],0,5)
    restart_text = title_font.render('Restart',True,white)
    screen.blit(restart_text, (10,720))
    count_text = small_font.render('Scambi effettuati:' + str(swap_count), True,black)
    screen.blit(count_text,(300,720))
    check_button = pygame.draw.rect(screen,blue, [SCREEN_WIDTH-180,0, 300,100],0,5)
    check_text = title_font.render('Check',True,white)
    screen.blit(check_text, (SCREEN_WIDTH-170,20))


    return restart_button,check_button




def draw_board():
    global rows
    global cols
    global correct
    board_list = []
    for j in range(rows):
        for i in range(cols):
            index = j*cols + i
            if first_guess and first_guess_num == (index):
                pygame.draw.rect(screen, blue, [i*70+32, j*70+112, 50, 50], 2)  # Colore blu per la selezione
            elif second_guess and second_guess_num == (index):
                pygame.draw.rect(screen, black, [i*70+32, j*70+112, 50, 50], 2)  # Colore nero per il secondo clic
            piece = pygame.draw.rect(screen, white, [i*70+32, j*70+112, 50, 50], 0, 4)
            board_list.append(piece)
            
            card = spaces[index]

            # Controlla se la carta è la placeholder
            # if card == ('X', 'placeholder'):
            #     piece_text = small_font.render('Placeholder', True, gray)
            #     screen.blit(piece_text, (i*70+38, j*70+120))
            # else:
            #       # Recupera l'immagine della carta corrispondente dalla mappa
            card_image = image_map.get(card, None)

            if card_image:
                # Disegna l'immagine della carta
                card_image = pygame.transform.scale(card_image, (50, 50))
                screen.blit(card_image, (i*70+32, j*70+112))
                card_image = None
            # else:
            #     # Se non c'è un'immagine disponibile, visualizza un testo placeholder
            #     piece_text = small_font.render(f'{card[0]} {card[1]}', True, gray)
            #     screen.blit(piece_text, (i*70+38, j*70+120))
                
                


    return board_list

def swap_cards(first_index, second_index):
    #Scambia due carte nella board.
     global spaces
    # Scambia le carte negli indici specificati
     spaces[first_index], spaces[second_index] = spaces[second_index], spaces[first_index]

def remove_card(card_index):
    global spaces
    placeholder = generate_placeholder()
    # Rimuovi la carta all'indice specificato
    if 0 <= card_index < len(spaces):
        spaces.pop(card_index)
        spaces.append(placeholder)
        



def check_guesses(selected_card_index):
     global spaces
     global correct
     global score
     global matches


     # Calcola le coordinate della carta selezionata
     col = selected_card_index % cols

     row = selected_card_index // cols
     card_value = spaces[selected_card_index]

#     # Coordinate delle carte adiacenti
     adjacent_positions = [
        (row - 1, col),  # N
        (row + 1, col),  # S
       (row, col - 1),  # W
        (row, col + 1),  # E
        (row + 1, col + 1), # SE
        (row - 1, col + 1), # NE
        (row + 1, col - 1), # SW 
       (row - 1, col - 1)  # NW

    ]

     found_match = False  # Flag per segnalare se è stata trovata una corrispondenza
     for r, c in adjacent_positions:
        if 0 <= r < rows and 0 <= c < cols:  # Controlla se la posizione è valida
            adjacent_card_index = r * cols + c
            adjacent_card_value = spaces[adjacent_card_index]

             # Controlla se hanno lo stesso valore e non sono già state rimosse
            if adjacent_card_value and adjacent_card_value[0] == card_value[0]:  
                 found_match = True  # Imposta il flag a True

                 # Decidi quale carta rimuovere (quella più vicina all'inizio)
                 if selected_card_index < adjacent_card_index:
                     remove_card(selected_card_index)
                 else:
                     remove_card(adjacent_card_index) 

                   # Esci dal ciclo una volta trovata una corrispondenza
            
            

     return found_match

    





running = True
image_map = load_images()


 # Ciclo principale del gioco
while running:
    timer.tick(fps)
    screen.fill(white)
    if new_board:
        generate_board(image_map)
        new_board = False
    (restart,check) = draw_backgrounds()
    board = draw_board()

    

        # Gestione degli eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

            # if check_guesses(index):
            #     print(index)
            #     if spaces[index] != ('X', 'placeholder'):
            #         print(f"Rimosse carte adiacenti alla posizione: {index}")    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not first_guess:
                for i in range(len(board)):
                    button = board[i]
                    if button.collidepoint((event.pos)) and not first_guess:
                        first_guess = True
                        first_guess_num = i
                        print(f"primo clic sulla carta: {i}")
                        break
            
            elif first_guess and not second_guess:
                for i in range(len(board)):
                    button = board[i]
                    if button.collidepoint((event.pos)) and i != first_guess_num:
                        second_guess = True
                        second_guess_num = i
                        print(f"secondo clic sulla carta: {i}")

                        if swap_count < max_swaps:
                            swap_cards(first_guess_num, second_guess_num)  # Scambia le carte
                            swap_count += 1
                        first_guess = False
                        second_guess = False
            if check.collidepoint((event.pos)):
                for index in range(len(board)):
                    if check_guesses(index):
                        if spaces[index] != ('X', 'placeholder'):
                            print(f"Rimosse carte adiacenti alla posizione: {index}")



            if restart.collidepoint((event.pos)):
                options_list = []
                used = []
                spaces = []
                new_board = True
                score = 0
                matches = 0 
                first_guess = False
                second_guess = False
                correct = [[0,0,0,0,0],
                           [0,0,0,0,0],
                           [0,0,0,0,0],
                           [0,0,0,0,0],
                           [0,0,0,0,0],
                           [0,0,0,0,0],
                           [0,0,0,0,0],
                           [0,0,0,0,0]]
                game_over = False
                swap_count = 0

    
        # Aggiorna la finestra di gioco
    pygame.display.flip()

