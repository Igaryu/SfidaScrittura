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

#DEBUG = True
DEBUG = False
SOFT = True

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
    while ((risp < 1) or (risp > 4)):
        intesta()
        print("\n\n\n\n\n")
        print("\t\t\t[ 1 ] Avvia storia in versione soft\n\n")
        print("\t\t\t[ 2 ] Avvia storia in versione hard\n\n")
        print("\t\t\t[ 3 ] Impostazioni\n\n")
        print("\t\t\t[ 4 ] Esci\n\n")
        risp=input('\n\n Seleziona voce menu [ 1 - 4 ] ')
        if risp in "1234":
            risp=int(risp)
        else:
            risp=0
        return(risp)
  


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

def ResetGiaUsato(cur: sqlite3.Cursor, data_base: sqlite3.Connection ) -> bool:
    '''
    Operazione di reset campi GiaUsato trasformata in funzione
    per poterla lanciare anche all'avvio del programma così da
    resettare i campi anche all'avvio nel caso si sia usciti
    per qualche motivo usanto CTRL-C
    '''
    cur.execute("update Steps1 set GiaUsato=0;")
    cur.execute("update Steps2 set GiaUsato=0;")
    data_base.commit()     

def core(TotRecStep1: int, TotRecStep2: int, Soft: bool) -> bool:
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

    ResetGiaUsato(cur, data_base)

    print("Inizia un racconto che...\n")
    if Soft:
 #       tmpRand=randint(1,TotRecStep1)
        tmpRand=randint(1,51)
    else:
        tmpRand=randint(52,101) 
           
    tmpGiaUsato = -1
    while tmpGiaUsato != 0:
        if Soft:
            cur.execute(f"select Frase,GiaUsato from Steps1 where Lingua='{Lang}' and indStep={tmpRand} and Hard=0;")
        else:
            cur.execute(f"select Frase,GiaUsato from Steps1 where Lingua='{Lang}' and indStep={tmpRand} and Hard=1;")        
        
        riga=cur.fetchone()
        tmpGiaUsato = riga[1]
        tmpRand1 = tmpRand
             
    print(f"\n{Fore.GREEN} {riga[0]}")
    locRisp=""
    while locRisp != 'a' and locRisp != 'c' and locRisp != 'u' and locRisp != 'e':
        locRisp=input("\n\t\t[ A ]ccetti o [ C ]cambi o vuoi [ E ]sci? [A/C/E]: ").lower()
        if locRisp == 'c':
            if Soft:
                tmpRand=randint(1,51)
            else:
                tmpRand=randint(52,101) 
                
            tmpGiaUsato = -1
            while tmpGiaUsato != 0:
                if Soft:
                    cur.execute(f"select Frase,GiaUsato from Steps1 where Lingua='{Lang}' and indStep={tmpRand} and Hard=0;")
                else:
                    cur.execute(f"select Frase,GiaUsato from Steps1 where Lingua='{Lang}' and indStep={tmpRand} and Hard=1;")
                    
                riga=cur.fetchone()
                if DEBUG:
                    print(f'{Fore.GREEN} Riga estratta: {riga}')
                tmpGiaUsato = riga[1]
                tmpRand1 = tmpRand
                while tmpRand == tmpRand1:
                    if Soft:
                        tmpRand=randint(1,51)
                    else:
                        tmpRand=randint(52,101) 
                    
            print(f"\n{Fore.GREEN} {riga[0]}")
            cur.execute(f"update Steps1 set GiaUsato=1 where indStep={tmpRand1}")
            data_base.commit()
            locRisp=''
        elif locRisp == 'e':
            chiudi_db(cur, data_base)
            exit(0)
    
    
 #tmpRand=randint(1,TotRecStep2)
    if Soft:
        tmpRand=randint(1,100)
    else:
        tmpRand=randint(101,200) 
        
    cls()
    print("\ne continua il racconto seguendo le indicazioni che seguono...\n")
    tmpGiaUsato = -1
    while tmpGiaUsato != 0:
        if Soft :
            cur.execute(f"select Frase,GiaUsato from Steps2 where Lingua='{Lang}' and indStep={tmpRand};")
        else:
            cur.execute(f"select Frase,GiaUsato from Steps2 where Lingua='{Lang}' and indStep={tmpRand};")
        riga=cur.fetchone()
        tmpGiaUsato = riga[1]
        tmpRand1 = tmpRand
            
    print(f"\n{Fore.GREEN} {riga[0]}")
    locRisp=""
    while locRisp != 'a' and locRisp != 'c' and locRisp != 'e':
        locRisp=input("\n\t\t[ A ]ccetti o [ C ]cambi o [ E ]sci [A/C/E]: ").lower()
        if locRisp == 'c' or locRisp == 'a':
            cur.execute(f"update Steps2 set GiaUsato=1 where indStep={tmpRand}")
            data_base.commit()


            if Soft:
                tmpRand=randint(1,100)
            else:
                tmpRand=randint(101,200) 
            
            tmpRand1 = tmpRand
            while tmpRand == tmpRand1:
                if Soft:
                    tmpRand=randint(1,100)
                else:
                    tmpRand=randint(101,200) 
            if DEBUG:
                print(f" {Fore.GREEN}Valore pre errore linea 216 per tmpRand: {tmpRand}")
            tmpGiaUsato = -1
            while tmpGiaUsato != 0:
                if Soft :
                    cur.execute(f"select Frase,GiaUsato from Steps2 where Lingua='{Lang}' and indStep={tmpRand};")
                else:
                    cur.execute(f"select Frase,GiaUsato from Steps2 where Lingua='{Lang}' and indStep={tmpRand};")
            
                riga=cur.fetchone()

                tmpGiaUsato = riga[1]

                cur.execute(f"update Steps2 set GiaUsato=1 where indStep={tmpRand}")
                data_base.commit()
                if DEBUG:
                    print(f'{Fore.GREEN} Riga estratta: {riga}')
                
 
                tmpRand1 = tmpRand
                while tmpRand == tmpRand1:
                    if Soft:
                        tmpRand=randint(1,100)
                    else:
                        tmpRand=randint(101,200) 
                
            print(f"\n{Fore.GREEN} {riga[0]}")
            cur.execute(f"update Steps2 set GiaUsato=1 where indStep={tmpRand}")
            data_base.commit()
            locRisp = ''
        elif locRisp == 'e':
            chiudi_db(cur,data_base)
            exit(0)
    

    input("\n\nPremi un tato per continuare...")

    return True


######################################
# Fine area funzioni
######################################

if exists("Steps.sqlite3") is False:
    cls()
    print('\n\nDatabase definizinoi Steps.sqlite3 non presente: non posso proseguire.\n\n')
    exit(-9)

data_base = sqlite3.connect("Steps.sqlite3")
cur=data_base.cursor()
ResetGiaUsato(cur, data_base)

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

intesta()
risp=0
while(risp != 4):
    risp=menu()
    if (risp == 1) :
        Soft = True
        core(TotRecStep1, TotRecStep2, Soft)
    if (risp == 2):
        Soft = False
        core(TotRecStep1, TotRecStep2, Soft)
    if (risp == 3):
        pass
    if (risp == 4):
     print("\n\nFine sessione.")

if chiudi_db(cur, data_base):
     exit(0)
else:
     exit(-9)


'''
    Verificare perche il conteggio dello steps2 non corrisponde 
    alla somma degli accetta + cambia...
'''
