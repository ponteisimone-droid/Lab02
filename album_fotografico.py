def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = []
    import csv
    try:
        with open(file_path, 'r', encoding='utf_8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for campi in reader:
                codice = campi['codice']
                titolo = campi['titolo']
                autore = campi['autore']
                mese = int(campi['mese'])
                anno = int(campi['anno'])
                foto = {"Codice": codice, "Titolo": titolo, "Autore": autore, "Mese": mese, "Anno": anno}

                anno_trovato = False
                for anni in album:
                    if anni[0] == anno:
                        anni[1].append(foto)
                        anno_trovato = True
                        break

                if not anno_trovato:
                    album.append([anno, [foto]])
        return album
    except FileNotFoundError:
        print('il file non esiste')
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12:
        print("il mese deve essere compreso tra 1 e 12")
        return None
    for anni in album:
        for f in anni[1]:
            if f["Codice"] == codice:
                print("La foto è già stata inserita")
                return None

    nuova_foto = {"Codice": codice, "Titolo": titolo, "Autore": autore, "Mese": mese, "Anno": anno}

    anno_trovato = False
    for anni in album:
        if anni[0] == anno:
            anni[1].append(nuova_foto)
            anno_trovato = True
            break

    if not anno_trovato:
        album.append([anno, [nuova_foto]])

    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{codice},{titolo},{autore},{mese},{anno}")
    except FileNotFoundError:
        print("Il file non è stato trovato")
        return None
    return nuova_foto



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""

    for anni in album:
        for foto in anni[1]:
            if foto["Codice"] == codice:
                return f"{foto['Codice']},{foto['Titolo']},{foto['Autore']},{foto['Mese']},{foto['Anno']}"
    return None



def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    for anni in album:
        if anni[0] == anno:
            titoli = []
            for foto in anni[1]:
                titoli.append(foto["Titolo"])
            titoli.sort()
            return titoli
    return None



def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
