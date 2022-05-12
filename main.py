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
from operator import truediv
from colorama import Fore, Back, Style, init
from os import name, system
from os.path import exists
from sys import exit
from random import randint 
import sqlite3

'''
    Variabili Switch
    DEBUG = True -> granularizza i messaggi durante l'esecuzione per il debug 
    DEBUG = False -> Non visulizza la messaggistica di aiuto per il debug
    SOFT = True -> Utilizzo della parte SOFT dei suggerimenti durante l'esecuzione dello scirpt
    SOFT = False -> Utilizzo della parte HARD (porno) dei suggerimenti durante l'esecuzione dello scirpt
'''
#DEBUG = True
#SOFT = False
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
    Visulizza il menu a quattro voci e ritorna il valore letto se 
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
    setta l'auto reset del'init di colorama
    genera numero casuale tra 0 e TotRecStep1 (da far diventare parametro??)
    setta tmpGiaUsato per permettere ciclo finche non trovaa record con
    campo GiaUsato con valore pari a 0
    ciclca quando sopra sino ad accettazione da parte dell'utente
    genera numero casuale tra 0 e TotRecStep2 (da far diventare parametro??)
    setta tmpGiaUsato per permettere ciclo finche non trovaa record con
    campo GiaUsato con valore pari a 0
    ciclca quando sopra sino ad accettazione da parte dell'utente
    
    Da aggiungere:
    verifica se non esistono piu record con GiaUsato a zero e segnalarlo all'utente
    DA DECIDERE: 
        va resettato l'intero set a giaUsato pari a zero 
    oppure
        interrompo la sesione?
        
    
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
            ''' se si vuole mantenere uscita progamma tenere in funziona la chiamata alla chiusura del DB
                altrimenti commentarla per eventuali accessi a nuove generazioe stimoli
                Se si commenta lasciando il return si avranno probelmi perche il db sarà chiuso 
                e non si potrà piu acedere al db
            '''
            return(0)       # Chiude sessione e torna al menu principale: VERIFICARE se ci son problemi con il db rientrando
            # chiudi_db(cur,data_base)
            # exit(0)       # Chiude sessione ed esce dal programma
    

    input("\n\nPremi un tato per continuare...")

    return True

def Non_Disponibile():
    intesta()
    print ("\n\n\n\t\t LA FUNZIONE RICHIESTA NON E' STATA ANCORA SVILUPPATA!!!\n\n")
    input("\t\t PREMI INVIO PER TORNARE...")
    return(-5)

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

'''
    Da aggiungere qui la selezione della lingua e relativo settaggio della variabile Lang
'''
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
        Soft = True
        Non_Disponibile()
    if (risp == 4):
        ''' aggiunta la chiusra del db perché nelle rispettive procedure è stata
            tolta la chiusura cosi da poter avviare una nuova sessione senza
            dover riaprire il database
        '''
        chiudi_db(cur,data_base)
        print("\n\nFine sessione.\n\n")
        exit(0)


###
#    Verificare perche il conteggio dello steps2 non corrisponde 
#    alla somma degli accetta + cambia...
###

'''

  8E2C DB21 A55C A162 29C9 5FDE 69E9 C8DC FA4E 019C

# -----BEGIN PGP PUBLIC KEY BLOCK-----

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
N8M=
=xhDr
-----END PGP PUBLIC KEY BLOCK-----
'''
