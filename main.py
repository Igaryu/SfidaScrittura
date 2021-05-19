#!/usr/bin/env python3
'''
   Prima fase: inport delle varie funzioni dai vari moduli
   a seguire verificare se esiste il file database e:
   se esiste 
   	calcolare il numero di righe per nazione IT
   se non esiste
	segnalare all'utente
	uscre con -9
   calcola il numero di record per entrambe le tavole ed assegna i 
   rispettivi valori alle variabili TotRecStep1 e TotRecStep1
'''

#from SaveRestoreSettings import SaveRestoreSettings
from colorama import Fore, Back, Style, init
from os import name, system
from os.path import exists
from sys import exit
from random import randint 
import sqlite3

DEBUG = False
def cls():
	'''
		Definisce cosa usare per pulire lo schermo in base al sistema
		dando per scontato che se non è Linux o Mac sarà Windows.
	'''
	if name == 'posix':
		system('clear')
	else:
		system('cls')

def intesta():
    '''
    Funzione per scrivere una intestazione ripetitiva
    '''
    cls()
    print("\nSfida Scrittura							Ver 1.0")
    print("\nUna spinta verso la scrittura creativa\n\n")

def menu() -> int:
    ''' 
    Visulizza il menu a tre voci ed ritorna il valore letto se 
    entro il range, altrimenti ritorna zero.
    '''
    
    risp=0
    while ((risp < 1) or (risp > 3)):
        intesta()
        print("\n\n\n\n\n")
        print("\t\t\t[ 1 ] Avvia storia\n\n")
        print("\t\t\t[ 2 ] Impostazioni\n\n")
        print("\t\t\t[ 3 ] Esci\n\n")
        risp=input('\n\n Seleziona voce menu [ 1 - 3 ] ')
        if risp in "123":
            risp=int(risp)
        else:
            risp=0
        return(risp)
  


if exists("Steps.sqlite3") is False:
    cls()
    print('\n\nDatabase definizinoi Steps.sqlite3 non presente: non posso proseguire.\n\n')
    exit(-9)
else:
	data_base = sqlite3.connect("Steps.sqlite3")
	cur=data_base.cursor()

Lang = 'IT'

intesta()
print("Caricamento dati in corso...")
for numero_record in data_base.execute(f"select * from Steps1 where Lingua='{Lang}';"):
    pass

TotRecStep1 = numero_record[0]
if DEBUG:
    input(f'Numero record presenti in Step1: {TotRecStep1}.')

for numero_record in data_base.execute(f"select * from Steps2 where Lingua='{Lang}';"):
    pass

TotRecStep2 = numero_record[0]
if DEBUG:
    input(f'Numero record presenti in Step1: {TotRecStep2}.')

def chiudi_db(cur: sqlite3.Cursor, data_base: sqlite3.Connection ) -> bool:
    '''
    1. Ripristina a 0 tutti campi GiaUsato sia nella tavola Steps1
       che in Steps2 laddove siano settati ad 1
    2. commita.
    3. chiudi correttamente il database.
    '''
    cur.execute("update Steps1 set GiaUsato=0;")
    cur.execute("update Steps2 set GiaUsato=0;")
    data_base.commit() 
    data_base.close()
    return True


def core(TotRecStep1: int, TotRecStep2: int) -> bool:
    '''
    Funzione  master del programma:
    setta l'auto resete del'init di colorama
    genera numero casuale tra 0 e TotRecStep1 (da far diventare parametro??)
    setta tmpGiaUsato per permettere ciclo finche non trovaa record con
    campo GiaUsato con valore 0
    ciclca quando sopra sino ad accettazione da parte dell'utente
    genera numero casuale tra 0 e TotRecStep2 (da far diventare parametro??)
    setta tmpGiaUsato per permettere ciclo finche non trovaa record con
    campo GiaUsato con valore 0
    ciclca quando sopra sino ad accettazione da parte dell'utente
    
    Da aggiungere:
    verifica se non esistono piu record con GiaUsato a zero e segnalarlo all'utente
    
    '''
    intesta()
    init(autoreset=True)
    print("Inizia un racconto che ...\n")
    tmpRand=randint(1,TotRecStep1)
    tmpGiaUsato = -1
    while tmpGiaUsato != 0:
        cur.execute(f"select Frase,GiaUsato from Steps1 where Lingua='{Lang}' and indStep={tmpRand};")
        riga=cur.fetchone()
        tmpGiaUsato = riga[1]
        tmpRand1 = tmpRand
             
    print(f"\n{Fore.BLACK} {Back.WHITE}{riga[0]}")
    locRisp=""
    while locRisp != 'a' and locRisp != 'c' and locRisp != 'u':
        locRisp=input("\n\t\t[ A ]ccetti o [ C ]cambi o vuoi [ U ]scire? [A/C/U]: ").lower()
        if locRisp == 'c':
            tmpRand=randint(1,TotRecStep1)
            tmpGiaUsato = -1
            while tmpGiaUsato != 0:
                cur.execute(f"select Frase,GiaUsato from Steps1 where Lingua='{Lang}' and indStep={tmpRand};")
                riga=cur.fetchone()
                if DEBUG:
                	print(f'{Fore.RED} Riga estratta: {riga}')
                tmpGiaUsato=riga[1]
                tmpRand1 = tmpRand
                while tmpRand == tmpRand1:
                    tmpRand=randint(1,TotRecStep1)
            print(f"\n{Fore.BLACK} {Back.WHITE}{riga[0]}")
            cur.execute(f"update Steps1 set GiaUsato=1 where indStep={tmpRand1}")
            data_base.commit()
            locRisp=''
        elif locRisp == 'u':
            chiudi_db(cur, data_base)
            exit(0)
    
    
    tmpRand=randint(1,TotRecStep2)
    cls()
    print("\ne continua il raccontoto seguendo le indicazioni che seguono...\n")
    tmpGiaUsato = -1
    while tmpGiaUsato != 0:
        cur.execute(f"select Frase,GiaUsato from Steps2 where Lingua='{Lang}' and indStep={tmpRand};")
        riga=cur.fetchone()
        tmpGiaUsato = riga[1]
        tmpRand1 = tmpRand
            
    print(f"\n{Fore.BLACK} {Back.WHITE}{riga[0]}")
    locRisp=""
    while locRisp != 'a' and locRisp != 'c' and locRisp != 'u':
        locRisp=input("\n\t\t[ A ]ccetti o [ C ]cambi o vuoi [ U ]scire? [A/C/U]: ").lower()
        if locRisp == 'c' or locRisp == 'a':
            cur.execute(f"update Steps2 set GiaUsato=1 where indStep={tmpRand}")
            data_base.commit()

            tmpRand=randint(1,TotRecStep2)
            tmpRand1 = tmpRand
            while tmpRand == tmpRand1:
                tmpRand=randint(1,TotRecStep2)
            
            tmpGiaUsato = -1
            while tmpGiaUsato != 0:
                cur.execute(f"select Frase,GiaUsato from Steps2 where Lingua='{Lang}' and indStep={tmpRand};")
                riga=cur.fetchone()

                tmpGiaUsato = riga[1]

                cur.execute(f"update Steps2 set GiaUsato=1 where indStep={tmpRand}")
                data_base.commit()
                if DEBUG:
                    print(f'{Fore.RED} Riga estratta: {riga}')
                
 
                tmpRand1 = tmpRand
                while tmpRand == tmpRand1:
	                tmpRand=randint(1,TotRecStep2)
                
            print(f"\n{Fore.BLUE} {Back.WHITE}{riga[0]}")
            cur.execute(f"update Steps2 set GiaUsato=1 where indStep={tmpRand}")
            data_base.commit()
            locRisp=''
        elif locRisp == 'u':
            chiudi_db(cur,data_base)
            exit(0)
    

    input("\n\nPremi un tato per continuare...")

    return True


######################################
# Fine aree funzioni
######################################

intesta()
risp=0
while(risp != 3):
	risp=menu()
	if (risp == 1):
		core(TotRecStep1, TotRecStep2)
	if (risp == 2):
		pass
	if (risp == 3):
		print("\n\nFine sessione.")
		if chiudi_db(cur, data_base):exit(0)
		else:exit(-9)


'''
    Verificare perche il conteggio dello steps2 non corrisponde 
    alla somma degli accetta + cambia...
'''
