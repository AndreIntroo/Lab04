class Espositore:
    def __init__(self, codice, nome, cognome):
        self.__codice = codice
        self.__nome = nome
        self.__cognome = cognome
    #metto solo i getter e non i setter poiche non devo modificare parametri come nome, cognome o codice che sono fissi e non variano.
    #metto i getter poiche la classe lingotto fiere ha bisogno di accede a questi attributi
    @property
    def codice(self):
        return self.__codice
    @property
    def nome(self):
        return self.__nome
    @property
    def cognome(self):
        return self.__cognome

    def __str__(self):
        return f"[ESPOSITORE] codice: {self.__codice} | nome: {self.__nome} | Cognome: {self.__cognome} "

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.__codice== other.__codice
        return None


class Stand:
    def __init__(self, codice, metri_q, padiglione, prezzo_base):
        self.__codice = codice
        self.__metri_q = float(metri_q)
        self.__padiglione = padiglione
        self.__prezzo_base = float(prezzo_base)
        self.__espositore_assegnato = None
# anche in questo casoo metto getter e non i setter per lo stesso motivo scritto nella classe precedente

    @property
    def codice(self):
        return self.__codice
    @property
    def metri_q(self):
        return self.__metri_q
    @property
    def padiglione(self):
        return self.__padiglione
    @property
    def prezzo_base(self):
        return self.__prezzo_base
    @property
    def espositore_assegnato(self):
        return self.__espositore_assegnato
    @espositore_assegnato.setter
    def espositore_assegnato(self, espositore_assegnato):
        self.__espositore_assegnato = espositore_assegnato

    def calcola_prezzo(self):
        return self.prezzo_base

#funzione che dice se lo stand sia disponibile oppure assegnato ad un espositore
    def stand_disponibile(self):
        return self.espositore_assegnato is None

    def __str__(self):
        if not self.stand_disponibile():
            stato =f" assegnato a {self.espositore_assegnato.codice}"
        else:
            stato = f"Disponibile"
        return f"STAND: {self.codice} | padiglione: {self.padiglione} | superficie: {self.metri_q}| prezzo :{self.calcola_prezzo():.2f} | stato:{stato}"
    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return None
    def __lt__(self, other):
        if isinstance(other, Stand):
            return self.calcola_prezzo() < other.calcola_prezzo()
        return None


class StandStandard (Stand):
    def __init__(self,codice, metri_q, padiglione, prezzo_base):
        super().__init__(codice, metri_q, padiglione, prezzo_base)

    def calcola_prezzo(self):
        return super().calcola_prezzo()

    def __str__(self):
        return "[STANDARD]" + super().__str__()

class StandPremium(Stand):
    def __init__(self, codice , metri_q, padiglione, prezzo_base, localizzazione ):
        super().__init__(codice , metri_q, padiglione, prezzo_base)
        self.__localizzazione = localizzazione

    @property
    def localizzazione(self ):
        return self.__localizzazione
    @localizzazione.setter
    def localizzazione(self, localizzazione):
        self.__localizzazione = localizzazione



    def calcola_prezzo(self ):
        return self.prezzo_base + self.prezzo_base*0.3

    def __str__(self):
        return "[PREMIUM]" + super().__str__()

class StandPreseExtra(StandStandard):
    def __init__(self,codice, metri_q, padiglione, prezzo_base, prese):
        super().__init__(codice, metri_q, padiglione, prezzo_base)
        self.__prese = int(prese)

    @property
    def prese(self):
        return self.__prese


    def calcola_prezzo(self):
        return self.prezzo_base*(1+0.07*self.prese)

    def __str__(self):
        return f" prese aggiuntive {self.prese} |" + super().__str__()

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        # TODO
        self.__nome = nome
        self.espositori = []
        self.stand = []

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome


    """Aggiungere setter e getter se necessari"""
    # TODO

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, 'r', encoding = 'utf_8') as file:
                for line in file:
                    campi = line.strip().split(",")
                    codice = campi[0]

                    if codice.startswith("S"):
                        metri_q, padiglione, prezzo_base = campi[1], campi[2], campi[3]
                        if len(campi) == 4:
                            self.stand.append(StandStandard(codice, metri_q , padiglione , prezzo_base))
                        elif len(campi) ==5 :
                            aggiunta = campi[4]
                            if campi[4].isdigit():
                                self.stand.append(StandPreseExtra(codice, metri_q, padiglione , prezzo_base, aggiunta))
                            else:
                                self.stand.append(StandPremium(codice, metri_q, padiglione, prezzo_base, aggiunta))
                    elif codice.startswith("E"):
                        nome, cognome = campi[1], campi[2]
                        self.espositori.append(Espositore(codice, nome, cognome))
                    else:
                        raise Exception("ERRORE: codice sbagliato e non classificabile tra fornitori o espositori")
        except FileNotFoundError:
            print("ERRORE: il percorso del file non è stato trovato nella cartella ")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        s_assegnare = None
        for s in self.stand:
            if s.codice == codice_stand:
                s_assegnare = s
        e_assegnare = None
        for e in self.espositori:
            if e.codice == codice_espositore:
                e_assegnare = e
        if s_assegnare is None:
            raise Exception("ERRORE: non è stato trovato alcuno stand con quel codice")
        if e_assegnare is None:
            raise Exception("ERRORE: non è stato identificato nessun espositore con quel codice")
        if not s_assegnare.stand_disponibile():
            raise Exception("ERRORE: lo stand è gia assegnato ad un espositore ")
        for s in self.stand:
            if s.espositore_assegnato == e_assegnare:
                raise Exception("l'espositore possiede gia uno stand")

        s_assegnare.espositore_assegnato = e_assegnare



    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        elenco_completo = []
        for e in self.espositori:
            stand_assegnato = None
            for s in self.stand:
                if s.espositore_assegnato== e:
                    stand_assegnato = s
                    break
            espositore_stampa = str(e)
            if stand_assegnato is not None:
                espositore_stampa = espositore_stampa +f"[ASSEGNATO ALLO STAND {stand_assegnato.codice}]"
            else:
                espositore_stampa = espositore_stampa +"[NESSUNO STAND ASSEGNATO]"
            elenco_completo.append(espositore_stampa)
        return elenco_completo

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand)
