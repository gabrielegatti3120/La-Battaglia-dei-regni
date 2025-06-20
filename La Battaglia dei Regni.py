from abc import ABC,abstractmethod
from random import random,shuffle,choice,uniform,randrange

class Soldato(ABC):

    def __init__(self,nome,costo,attacco,difesa,salute): # Costruttore
        self.__nome = nome
        self.__costo = costo
        self.__attacco = attacco
        self.__difesa = difesa
        self.__salute = salute
        self.__vivo = True
    # Metodi getter
    def get_nome(self): return self.__nome
    def get_costo(self): return self.__costo
    def get_attacco(self): return self.__attacco
    def get_difesa(self): return self.__difesa
    def get_salute(self): return self.__salute
    def get_vivo(self): return self.__vivo


    # Metodi setter
    def set_nome(self,nome): self.__nome = nome
    def set_costo(self,costo): self.__costo = costo
    def set_attacco(self,attacco): self.__attacco = attacco
    def set_difesa(self,difesa): self.__difesa = difesa
    def set_salute(self,salute): self.__salute = salute
    def set_vivo(self,morte:bool): self.__vivo = morte

    @abstractmethod
    def attacca(self,avversario):
        pass

    def difenditi(self,danno):
        if danno > self.__difesa:
            self.__salute -= danno - self.__difesa
            if self.get_salute() > 0:
                print(f"{self.__nome} ha subito {danno-self.__difesa} danni. Salute rimanente {self.__salute}")
            else:
                self.set_vivo(False)
                print(f"{self.__nome} ha subito {danno-self.__difesa} danni ed è morto")
        else: 
            print("Nessun danno!")


    def vivo(self): # inutile
        if self.__vivo: return True
        else: return False

    @abstractmethod
    def stato(self):
        pass


class Cavaliere(Soldato):
    def __init__(self, nome):
        super().__init__(nome, 500, 60, 100, 200)
        
    def stato(self):
        print(f"{self.get_nome()} Classe: Cavaliere")
    
    def attacca(self,avversario,crit = 0.2):
        if random() < crit:
            print("Colpo critico!")
            danno = 2*self.get_attacco()
            avversario.difenditi(danno)
        else: 
            danno = self.get_attacco()
            avversario.difenditi(danno)

class Arciere(Soldato):
    def __init__(self, nome):
        super().__init__(nome, 250, 90, 30, 150)
        
    def stato(self):
        print(f"{self.get_nome()} Classe: Arciere")
    
    def attacca(self,avversario):
            danno = self.get_attacco()
            avversario.difenditi(danno)

class Guaritore(Soldato):
    def __init__(self, nome):
        super().__init__(nome, 200, 25, 30, 130)

    def stato(self):
        print(f"{self.get_nome()} Classe: Guaritore")
    
    def attacca(self,compagni:list,self_index,en_index,nemici):
        ally = choice(compagni)
        while True:
            if len(compagni) != 1:
                ally = choice(compagni)
                if ally.get_vivo():
                    ally.set_salute(ally.get_salute()*1.1)
                    break
            else:
                if self_index <= en_index-1:
                    danno = self.get_attacco()
                    nemici[self_index].difenditi(danno)
                else:
                    danno = self.get_attacco()
                    nemici[en_index-1].difenditi(danno)



class Mago(Soldato):
    def __init__(self, nome):
        super().__init__(nome, 450, 100, 30, 200)
        
    def stato(self):
        print(f"{self.get_nome()} Classe: Mago")
    
    def attacca(self,avversario):
            if random() < 0.25:
                print(f"{self.get_nome()} sta ciondolando!")
            else:
                danno = self.get_attacco() * uniform(0,2)
                avversario.difenditi(danno)


def Formazione_unità(budget:int,squadra:list,Soldato):
    if budget >= Soldato.get_costo():
        budget -= Soldato.get_costo()
        squadra.append(Soldato)
        return True,budget
    else: return False,budget


def scelta_giocatore(budget1,Squadra1):
    while True:
        if budget1 < 200: break
        print(f"Hai a disposizione {budget1} monete")
        print("Puoi scegliere tra: Cavaliere (c), Arciere(a), Guaritore(g), Mago(m), oppure E per uscire")
        s = input("Cosa scegli? ")
        if s.lower() == "c":
            print("Hai scelto il cavaliere!")
            nome = input("Come si chiama? ")
            c = Cavaliere(nome)
            f,budget1 = Formazione_unità(budget1,Squadra1,c)
            if f: print("Unità aggiunta")
            else:
                print("L'unità costa troppo! Scegli altro.")
                continue
        elif s.lower() == "a":
            print("Hai scelto l'arciere!")
            nome = input("Come si chiama? ")
            c = Arciere(nome)
            f,budget1 = Formazione_unità(budget1,Squadra1,c)
            if f: print("Unità aggiunta")
            else:
                print("L'unità costa troppo! Scegli altro.")
                continue
        elif s.lower() == "m":
            print("Hai scelto il mago!")
            nome = input("Come si chiama? ")
            c = Mago(nome)
            f,budget1 = Formazione_unità(budget1,Squadra1,c)
            if f: print("Unità aggiunta")
            else:
                print("L'unità costa troppo! Scegli altro.")
                continue
        elif s.lower() == "g":
            print("Hai scelto il guaritore!")
            nome = input("Come si chiama? ")
            c = Guaritore(nome)
            f,budget1 = Formazione_unità(budget1,Squadra1,c)
            if f: print("Unità aggiunta")
            else:
                print("L'unità costa troppo! Scegli altro.")
                continue
        elif s.lower() == "e":
            print("Schieramento terminato")
            break
        else: print("Esegui un'azione consentita")
    return Squadra1,budget1

def scelta_Ia(budget2,Squadra2):
    Prezzi = [500,250,200,450]
    #count = 0
    while True:
        scelta = randrange(0,3,1)
        if Prezzi[scelta] <= budget2:
            #count += 1
            budget2 -= Prezzi[scelta]
            if scelta == 0: Squadra2.append(Cavaliere("Cavaliere"))
            elif scelta == 1: Squadra2.append(Arciere("Arciere"))
            elif scelta == 2: Squadra2.append(Guaritore("Guaritore"))
            else: Squadra2.append(Mago("Mago"))
        else: break
    #return count
    return Squadra2,budget2




def turno_battaglia(Player:list,Ia:list):
    p = len(Player)
    q = len(Ia)

    # Attacchi arciere
    for i in range(p):
        if isinstance(Player[i],Arciere):
            if i < q: Player[i].attacca(Ia[i])
            else: Player[i].attacca(Ia[q-1])
    for j in range(q):
        if isinstance(Ia[j],Arciere):
            if j < p: Ia[j].attacca(Player[j])
            else: Ia[j].attacca(Player[p-1])
    #Attacchi degli altri
    for i in range(p):
        if isinstance(Player[i],Guaritore) and Player[i].get_vivo(): # guaritore
            Player[i].attacca(Player,i,q,Ia)
        elif not isinstance(Player[i],Arciere) and Player[i].get_vivo():
            if i < q: Player[i].attacca(Ia[i])
            else: Player[i].attacca(Ia[q-1])
    for j in range(q):
        if isinstance(Ia[j],Guaritore) and Ia[j].get_vivo(): # guaritore
            Ia[j].attacca(Ia,j,p,Player)
        elif not isinstance(Ia[j],Arciere) and Ia[j].get_vivo():
            if j < p: Ia[j].attacca(Player[j])
            else: Ia[j].attacca(Player[p-1])
    
    return Player,Ia
        
def Battaglia(Player:list,Ia:list,budgetP:int, budgetI:int):
    turni = 0
    while len(Player) != 0 and len(Ia) != 0:
        Player,Ia = turno_battaglia(Player,Ia)
        for i in Player:
            if not i.get_vivo(): 
                Player.remove(i)
                print("RIMOZIONE")
        for j in Ia:
            if not j.get_vivo(): 
                Ia.remove(j)
                print("Rimozione")
        turni += 1
        if len(Player) != 0 and len(Ia) != 0:
            budgetP += 300
            budgetI += 300
            Player,budgetP = scelta_giocatore(budgetP,Player)
            Ia,budgetI = scelta_Ia(budgetI,Ia)

        else: 
            print("Battaglia finita hai vinto!") if len(Ia) == 0 else print("Hai perso")
            break
    if len(Ia) == 0: return Player,turni
    else: return Ia,turni




# Persona
Squadra1 = []
budget1 = 1000 

# IA
Squadra2 = []
budget2 = 1000 

Squadra1,budget1 = scelta_giocatore(budget1,Squadra1)
print("Ecco la tua squadra:")
for i in Squadra1: i.stato()
print("\n")
Squadra2,budget2 = scelta_Ia(budget2,Squadra2)
print("Ecco contro chi combatterai:")
for i in Squadra2: i.stato()
print("\n")
Vincitore,turni = Battaglia(Squadra1,Squadra2,budget1,budget2)

print(f"Vittoria in {turni}")
print("Squadra vincente:")
for i in Vincitore:
    i.stato()
