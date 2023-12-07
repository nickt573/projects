import random
import time

def main():
    print("-------\nWelcome to BlackJack! Type START to begin or HELP for an explanation of rules") # setup game
    help = 0
    while True:
        inpt = input(">").upper()
        if inpt == "START":
            break
        if inpt == "HELP":
            help = 1
            break
        print("Please enter a valid command.")

    if help: # explains rules here
        move = True
        while move:
            print("In BlackJack, each player starts with two cards: one card that is private to you (represented by "
            "[square brackets]) and one that all players can see.\nYour goal is to get the sum of all of your cards (represented by (parentheses)) to be as close to 21 "
            "as possible without going over.\nEach round, a player can choose to either HIT (add a new card to their hand) "
            "or HOLD (keep your cards at the same value).\nRemember, the cards in the deck range from 1 to 11, and there are no repeats.\n"
            "After all players are holding or all cards have been drawn, the player closest to 21 without going over is the winner!")
            time.sleep(4)
            while True:
                yorn = input("-------\nReady? (Y/N)\n>").upper()
                if yorn == "Y":
                    move = False
                    break
                elif yorn != "N":
                    print("Please enter a valid command.")
                else: 
                    break
                

    print("-------\nLet's begin!")
    time.sleep(1)


    #establishing starting cards
    used = []
    pused = [] 
    cused = []
    c_hid = nonseed(used)
    c_known = seed(used, cused)
    pstart1 = nonseed(used)
    pstart2 = seed(used, pused)

    c_total = c_hid + c_known
    p_total = pstart1 + pstart2

    # game begin
    print(f"Your hidden card is {pstart1}.  Your first card is {pstart2}.")
    time.sleep(1)
    end = 0 # = 1 if both hold (obsolete tbh)
    phold = 0 # player is holding
    chold = 0 # computer is holding
    out = 0 # seeing if all cards are used
    while True:
        if all(i in used for i in range(1, 12)) or end:
            if end != 1:
                out = 1
            break

        # player card
        print(f"Player Cards:   [{pstart1}]", end='')
        for i in range(len(pused)):
            print(f" + {pused[i]}", end='')
        if p_total > 21:
            print(f" (\033[91m{p_total}\033[0m/21)")
        else:
            print(f" ({p_total}/21)")


        # computer cards
        time.sleep(.5)
        print(f"Computer Cards: [?]", end='')
        for i in range(len(cused)):
            print(f" + {cused[i]}", end='')
        if c_total - c_hid > 21:
             print(f" (? + \033[91m{c_total - c_hid}\033[0m/21)")
        else:
            print(f" (? + {c_total - c_hid}/21)")

        

        # hit/hold for player
        if phold == 1:
            time.sleep(2)
            print("You are still holding")
            time.sleep(2)
        
        while not phold:
            print("Type HIT or HOLD")
            inpt = input(">").upper()
            if inpt == "HOLD":
                phold = 1
                print("You have decided to HOLD")
                break
            if inpt == "HIT":
                break
            print("Please enter a valid command")
        if not phold:
            num = seed(used, pused)
            p_total += num
            if p_total > 21:
                print(f"New card: {num} (\033[91m{p_total}\033[0m)")
            else:
                print(f"New card: {num} ({p_total})")


        if phold == 1 and chold == 1: # check for end
            end = 1
            break
    
        # computer move
        if chold == 1:
            time.sleep(2)
            print("Computer is still holding")
        if c_total >= 21: #hold if win or guaranteed lose
            chold = 1

        time.sleep(2)
        cchoice = calculate(pused, cused, c_total) # computer's choice (1 = hit, 2 = hold)
        if cchoice == 2: # if computer holds
            chold = 1
            print(f"Computer has decided to HOLD")
            time.sleep(1)

        if not chold: # computer hits
            num = seed(used, cused)
            c_total += num
            print("Computer decided to HIT")
            time.sleep(2)
            if c_total - c_hid > 21:
                print(f"New card: {num} (? + \033[91m{c_total - c_hid}\033[0m)")
            else:
                print(f"New card: {num} (? + {c_total - c_hid})")
            time.sleep(2)
        
        
        if phold == 1 and chold == 1: # check for end
            end = 1
            break

    if out != 1:
        print("Both players have now selected HOLD.  It is now time to reveal the cards!")
    else: 
        print("All cards have been used.  It is now time to reveal the cards!")
    time.sleep(1.5)
    if p_total > 21:
        print(f"Player's score: \033[91m{p_total}\033[0m")
    else:
        print(f"Player's score: {p_total}")

    time.sleep(1)
    print("Computer's score: ", end='')
    time.sleep(1)
    if c_total > 21:   
        print(f"\033[91m{c_total}\033[0m")
    else:
        print(f"{c_total}")
    time.sleep(.5)
   
    # score
    if (c_total > p_total and c_total <= 21) or (c_total < p_total and p_total > 21 and c_total <= 21):
        print("Computer wins!")
    elif p_total > c_total and p_total <= 21 or (p_total < c_total and c_total > 21 and p_total <= 21):
        print("Player wins!")
    elif p_total == c_total and c_total <= 21:
        print("It's a tie!")
    elif p_total > 21 and c_total > 21:
        print("Both lose!")


def nonseed(used):
    while True:
        card = random.randint(1,11)
        if card not in used:
            used.append(card)
            return card
        
def calculate(p, c, tot):
    shit = 0
    shold = 0
    for i in range(len(p)):
        if tot + p[i] <= 21:
            shit += 1
        elif tot + p[i] > 21:
            shold += 1 
    for i in range(len(c)):
        if tot + c[i] <= 21:
            shit += 1
        elif tot + c[i] > 21:
            shold += 1 

    if shit > shold:
        return 1
    elif shit == shold:
        return random.randint(1,2)
    elif shit < shold and shit != 0: 
        l = random.randint(1,3)
        if l == 1 or l == 2:
            return 2
        else:
            return 1
    elif shit < shold and shit == 0:
        return 2


def seed(used, personused):
    while True:
        card = random.randint(1,11)
        if card not in used:
            used.append(card)
            personused.append(card)
            return card


main()