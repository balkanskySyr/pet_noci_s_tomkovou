# importy
import time
import datetime
import random

# počáteční hodnoty
zivoty = 10.0
maximalni_zivoty = 10.0
penize = 200
minimalni_penize = 0
inventar = {"svačina": 1}
cas = datetime.datetime.strptime("08:00", "%H:%M").time()
scena = 7 # Start at scene 7 for testing the fight directly
hra = True
tomkova_body = 0
jirasek_zije = True # This global variable seems unused in the provided fight logic for its outcome.

# pocatecni hodnoty pro rvacku (these are global and will be reset at the start of each fight instance)
rvacka = True 
rvacka_zivoty_hrac = 10.0 
rvacka_zivoty_jirasek = 10.0
rvacka_tah_hrac = True
rvacka_tah_jirasek = False

#pocatecni hodnoty pro obchod
pocet_bonbonu = 0
cena_bonbony = 60
cena_premium_toasty = 80
cena_zbran = 500

# definice vsech potrebnych itemu
krabicove_vino = "krabicové víno"
svacina = "svačina"
bonbony = "bonbony"
premium_toasty = "premium toasty"
zbran = "zbraň"
srdce_tomkove = "srdce paní profesorky"

# změna životů, aby nepřesáhly maximální hodnotu
def zmen_zivoty(hodnota_zivotu):
    global zivoty, maximalni_zivoty, hra 
    zivoty += hodnota_zivotu
    if zivoty <= 0:
        if srdce_tomkove in inventar:
            print("Těsně jsi unikl smrti. Naštěstí tě zachránilo srdce Tomkové, stejně jako Tomková\n" \
            "zachraňuje každou středu svou dvouhodinovkou. Nyní máš 0.5 životů.")
            zmen_item(srdce_tomkove, -1)
            zivoty = 0.5
        else:
            konec_hry() # CORRECTED: Call the function
            
    zivoty = min(zivoty, maximalni_zivoty)

# změna peněz, aby nepřesáhly minimální hodnotu
def zmen_penize(hodnota_penez):
    global penize, minimalni_penize
    penize += hodnota_penez
    penize = max(penize, minimalni_penize)

# změna itemů z listu
def zmen_item(item, zmena_itemu):
    global inventar 
    if item in inventar:
        inventar[item] += int(zmena_itemu)
        if inventar[item] <= 0:
            del inventar[item]
    elif zmena_itemu > 0:
        inventar[item] = int(zmena_itemu)

# výčet inventáře
def vycet_inventare():
    global inventar 
    if not inventar: # Check if inventory is empty first
        print("Inventář je prázdný", end="") # end="" to allow newline later or other text
        return

    item_strings = []
    for item, pocet in inventar.items():
        item_strings.append(f"{item.capitalize()} (x{pocet})")
    print(", ".join(item_strings), end="")

# defaultní menu, včetně inputů a interakcí se staty a inventářem
def menu():
    global zivoty, penize, inventar, cas 
    print("-----------------------------------------")
    print(f"Aktuálně je: {cas}\nŽivoty: {zivoty:.1f} \nPeníze: {penize}") # Display zivoty with one decimal
    print("Inventář: ", end="")
    vycet_inventare()
    print() # Newline after inventory list
    print("-----------------------------------------")
    print("Pokračovat v příběhu - 1.")
    print("Interakce s inventářem - 2.")
    print("Ukončit hru - 3.")
    print("-----------------------------------------")
    vstup = input(">")
    print("-----------------------------------------")
    return vstup

# obchod, který je průběžně dostupný
def obchod():
    global penize, inventar, cena_bonbony, cena_premium_toasty, cena_zbran, pocet_bonbonu
    while True:
        print("-----------------------------------------")
        print("             REFRESH BISTRO")
        print("-----------------------------------------")
        print(f"1. Premium Toast - {cena_premium_toasty} ")
        print(f"2. Bonbón - {cena_bonbony}")
        print(f"3. Zbraň - {cena_zbran}")
        print("4. Informace o předmětech")
        print("5. Zpět do hry")
        print("-----------------------------------------")
        vstup_obchod = input(">")
        print("-----------------------------------------")
        if vstup_obchod == "1":
            if penize >= cena_premium_toasty:
                zmen_penize(-cena_premium_toasty)
                zmen_item(premium_toasty , +1) 
                print("Úspěšně jsi získal Premium Toast.")
                cena_premium_toasty += 15
            else:
                print("Nemáš dostatek peněz na Premium Toast.")
        elif vstup_obchod == "2":
            if penize >= cena_bonbony and pocet_bonbonu < 3:
                zmen_penize(-cena_bonbony)
                zmen_item(bonbony , +1) 
                print("Úspěšně jsi získal bonbóny.")
                cena_bonbony += 40
                pocet_bonbonu += 1
            elif pocet_bonbonu >= 3 and penize >= cena_bonbony:
                    print("Nelze koupit víc bonbónů.")
            else:
                print("Nemáš dostatek peněz na bonbóny.")
        elif vstup_obchod == "3":
            if penize >= cena_zbran:
                zmen_penize(-cena_zbran)
                zmen_item(zbran , +1) 
                print("Úspěšně jsi získal zbraň.")
            else:
                print("Nemáš dostatek peněz na zbraň.")
        elif vstup_obchod == "4":
            print(f"{premium_toasty.capitalize()} - Základní potravina. Doplní 2 životy.")
            print(f"{bonbony.capitalize()} - výborné na uplácení - zvyšují všechny šance v příběhu o zhruba 10%.\n" \
            "Lze zakoupit víckrát pro ještě větší zvýšení šancí.")
            print(f"{zbran.capitalize()} - Standardní pistole s malorážkou. Ideální na Židáska.")
        elif vstup_obchod == "5":
            break
        else:
            print("Neplatný vstup.")

# dialog s koncem hry, druh konce asi podle boolean
def konec_hry():
    global hra
    print("Hra skončila. (Placeholder - 'teď to fakt psát nebudu')") 
    hra = False

# generování šancí
def sance(sance_zakladni):
    global pocet_bonbonu 
    return random.random() <= sance_zakladni + pocet_bonbonu * 0.1


# úvodní scéna s krátkým tutoriálem mimo hlavní smyčku
print()
print()
print("         SKORO PĚT NOCÍ S TOMKOVOU, ANEB VÝLET DO ÚSTÍ")
print()
print("Pokud jsi zapnul tento simulátor existenční krize v podobě")
print("textové adventure hry, rozhodně nebudeš zklamaný. Čeká tě")
print("pět dnů a čtyři noci pekla s jediným cílem - PŘEŽIJ. ")
print()
print("Pod sebou vidíš primitivní herní menu, které uvidíš mezi")
print("každou scénou. Na tomto menu můžeš vidět tři jednoduché")
print("sekce - životy, peníze a inventář. Pamatuj, že 10 je ")
print("maximální hodnota tvých životů a jakékoliv životy navíc")
print("se smažou. S některými předměty v tvém inventáři můžeš reagovat,")
print("ale jen mezi scénami. Na začátek jsi od maminky")
print(f"dostal {svacina}, která ti přidá 2.5 životů. Během hry se ti") # Used variable
print("také bude nepravidelně zobrazovat obchod, ve kterém se převážně")
print("kvůli Fialovi postupně zvyšují ceny.")
print("-----------------------------------------")
print("                    HODNĚ ŠTĚSTÍ")

# hlavní smyčka
while hra:
    vstup = menu()

    if vstup == "3":
      konec_hry() 

    elif vstup == "2":
        if len(inventar) < 1:
            print("Tvůj inventář je prázdný.")
        else:
            print("Se kterým z těchto předmětů si přeješ interagovat?")
            print("-----------------------------------------")
            inventar_list = list(inventar.keys())
            for index, item_name in enumerate(inventar_list, start=1):
                print(f"{index} - {item_name.capitalize()} (x{inventar[item_name]})")
            print("-----------------------------------------")
            vstup_item = input(">")
            print("-----------------------------------------")

            if vstup_item.isdigit():
                index_choice = int(vstup_item) # Renamed to avoid conflict
                if 1 <= index_choice <= len(inventar_list):
                    zvoleny_item = inventar_list[index_choice - 1]
                    
                    if zvoleny_item == svacina: 
                        print(f"Chcete zkonzumovat svoji {svacina} a přidat si 2.5 životů? y/n")
                        print("-----------------------------------------")
                        rozhodnuti_svacina = input(">").lower() 
                        print("-----------------------------------------")
                        if rozhodnuti_svacina == "y":
                            zmen_zivoty(2.5)
                            zmen_item(svacina, -1)
                            print(f"Úspěšně jste snědli svoji {svacina}. Nyní máte {zivoty:.1f} životů.")
                        elif rozhodnuti_svacina == "n":
                            print(f"Rozhodli jste nesníst svoji {svacina} a ponechat si svých {zivoty:.1f} životů.")
                        else:
                            print("Neplatná volba.")
                    elif zvoleny_item == krabicove_vino: 
                        print("S vínem prozatím nelze interagovat. Jeho čas ovšem přijde.")
                    elif zvoleny_item == premium_toasty:
                        print(f"Chcete sníst {premium_toasty} a doplnit si 2 životy? y/n")
                        print("-----------------------------------------")
                        rozhodnuti_toast = input(">").lower()
                        print("-----------------------------------------")
                        if rozhodnuti_toast == "y":
                            zmen_zivoty(2.0) 
                            zmen_item(premium_toasty, -1)
                            print(f"Snědl jsi {premium_toasty}. Nyní máš {zivoty:.1f} životů.")
                        elif rozhodnuti_toast == "n":
                            print(f"Nechal sis {premium_toasty}.")
                        else:
                            print("Neplatná volba.")
                    # Add other item interactions here
                    else:
                        print(f"S předmětem '{zvoleny_item.capitalize()}' nelze prozatím interagovat.")
                else:
                    print("Daný předmět se ve vašem inventáři nenachází (neplatný index).")
            else:
                print("Neplatný vstup pro výběr předmětu.")

    elif vstup == "1":
        if scena == 0:
            print("Je pondělí, osm hodin ráno. ...") # Shortened for brevity
            print("-----------------------------------------")
            print("Posadit se vedle Slačíka - 1.")
            print("Posadit se vedle Tomkový - 2.")
            print("Posadit se vedle Burgetový - 3.")
            print("-----------------------------------------")
            rozhodnuti_0 = input(">")
            print("-----------------------------------------")
            if rozhodnuti_0 == "1":
                print("Slačík s tebou soucítí ...")
                zmen_item(krabicove_vino, +1)
                zmen_penize(20)
                scena += 1 
            elif rozhodnuti_0 == "2":
                if svacina in inventar: 
                   print("Co sis jako kurva myslel? ...")
                   zmen_item(svacina, -1) 
                else:
                    print("Tak to byl hodně dementní nápad. ... Přicházíš o 4 životy.")
                    zmen_zivoty(-4.0) 
                scena += 1 
            elif rozhodnuti_0 == "3":
                print("Ze všech možností si vybereš tuhle? ... Přicházíš o dva životy.")
                zmen_zivoty(-2.0) 
                scena += 1 
            else:
                print("Neplatný vstup. Zkus to znovu.")
        elif scena == 1:
            print("Tvojí záchranou bylo, ...")
            scena += 1
        elif scena == 2:
            print("Z pokoje už jsi do večera radši nevyšel. ...")
            print("-----------------------------------------")
            print("Nechat to být - 1.")
            print("Nahlédnout za dveře - 2.")
            print("-----------------------------------------")
            valid_choice_made_sc2 = False
            while not valid_choice_made_sc2 and hra: 
                rozhodnuti_2 = input(">")
                print("-----------------------------------------")
                if rozhodnuti_2 == "1":
                    print("Pokusil jsi se usnout, ale jednoduše to nejde. Klepání pokračuje.")
                    print("-----------------------------------------")
                    print("Nechat to být - 1.") 
                    print("Nahlédnout za dveře - 2.")
                    print("-----------------------------------------")
                elif rozhodnuti_2 == "2":
                    print("Nahlédl jsi za dveře ...")
                    print("-----------------------------------------")
                    print("Mile mu vzkázat, ať se odebere ke spánku - 1.")
                    print("Začít ho finančně vydírat - 2.")
                    print("-----------------------------------------")
                    
                    valid_zidasek_choice = False
                    while not valid_zidasek_choice and hra: 
                        rozhodnuti_zidasek = input(">")
                        print("-----------------------------------------")
                        if rozhodnuti_zidasek == "1":
                            if sance(0.3):
                                print("Z nějakýho důvodu tohle zafungovalo. ... dvacetikorunovka.")
                                zmen_penize(+20)
                            else:
                                print("To bylo hodně naivní. ... zmizelo 20 korun.")
                                zmen_penize(-20)
                            valid_zidasek_choice = True
                            valid_choice_made_sc2 = True
                        elif rozhodnuti_zidasek == "2":
                            print("To nebyl zas tak hloupý nápad. ... nabídku - 100 korun ...")
                            print("-----------------------------------------")
                            print("Přijmout nabídku - 1.")
                            print("Říct si o víc - 2.")
                            print("-----------------------------------------")
                            rozhodnuti_zidasek_vydirani = input(">")
                            print("-----------------------------------------") 
                            if rozhodnuti_zidasek_vydirani == "1":
                                zmen_penize(+100)
                                print("Přijmul jsi Jiráskovu nabídku ... 100 korun.")
                            elif rozhodnuti_zidasek_vydirani == "2":
                                zidasek_vydirani_random = random.randint(1,2)
                                if zidasek_vydirani_random == 1:
                                    print("On má opravdu peněz na rozdávání. ... 200 korun.")
                                    zmen_penize(+200)
                                else:
                                    print("To bylo hodně naivní. ... zmizelo 20 korun ...")
                                    zmen_penize(-20)
                            else:
                                print("Neplatný vstup pro vydírání. Jiráskovi došla trpělivost a odešel.")
                            valid_zidasek_choice = True # Even if vydirani input is bad, this path is chosen
                            valid_choice_made_sc2 = True
                        else:
                            print("Neplatný vstup pro interakci s Jiráskem. Zkus to znovu.")
                else:
                    print("Neplatný vstup. Zkus to znovu.")
            if hra: scena +=1 # Only advance if game is still running
        elif scena == 3:
            print("Po nočním útoku ...")
            obchod()
            scena += 1
        elif scena == 4:
            if premium_toasty in inventar: 
                zmen_item(premium_toasty, -1)
                print("Výborně. Tomková byla nadšená z toastů ...")
                # Price might have changed, so use the value at time of purchase for refund logic
                # For simplicity, using current cena_premium_toasty, but this could be refined
                zmen_penize(cena_premium_toasty + 30) 
                zmen_zivoty(0.7)
            elif svacina in inventar:
                print("To bylo těsné, ještě že jsi pořád měl tu svačinu ...")
                zmen_item(svacina, -1)
            else:
                print("Proč jsi jí kurva něco nekoupil? ...")
                zmen_zivoty(-3.0)
                zmen_penize(-(cena_premium_toasty - 20)) 
            scena += 1
        elif scena == 5:
            print("Odpoledne se situace moc neposunula. ...")
            tomkova_body = 0 
            print("-----------------------------------------")
            print("Pověz mi, v jakém roce zavedla Marie Terezie povinnou školní docházku? ...")
            tomkova_terezie = input(">")
            print("-----------------------------------------")
            if tomkova_terezie == ("1"): tomkova_body +=1
            
            print("Pověz mi, v jakém roce byla zrušena nevolnictví? ...")
            tomkova_nevolnictvi = input(">")
            print("-----------------------------------------")
            if tomkova_nevolnictvi == ("2"): tomkova_body +=1

            print("Pověz mi, v jakém roce zemřela Marie Terezie? ...")
            tomkova_terezie_zemrela = input(">")
            print("-----------------------------------------")
            if tomkova_terezie_zemrela == ("1"): tomkova_body +=1

            if tomkova_body == 0:
                print("Tomková byla zklamaná ... Přicházíš o 4 životy.")
                zmen_zivoty(-4.0)
            elif tomkova_body == 1:
                print("Tomková byla zklamaná ... Přicházíš o 2 životy.")
                zmen_zivoty(-2.0)
            elif tomkova_body == 2:
                print("Solidní výkon, Tomková byla spokojená ... 135 peněz.")
                zmen_penize(135)
            elif tomkova_body ==3:
                print("Tomková je naprosto unešená. ... srdce paní profesorky.")
                zmen_item(srdce_tomkove, +1)
            scena += 1
        elif scena == 6:
            print("Aktivita kvízu zabrala celé odpoledne ...")
            scena += 1
        elif scena == 7:
            print("Probudil tě nepříliž výrazný zvuk kroků z chodby. Na tom by nebylo nic zvláštního, ale\n" \
            "všiml sis, že jsou otevřené dveře tvého pokoje. To je sice zvláštní, ale zkusil jsi to ignorovat\n" \
            "a dveře jsi zavřel. Když najednou, po prudkém zabouchnutí dveří, se ozvalo: 'Můžeš přestat mlátit\n" \
            "těma dveřma? Ty zvuky jsou nepříjemné!'. No jasně, že tě to nenapadlo. Ten žid se tě pokusil okrást\n" \
            "znova! Tentokrát už si to ale líbit nenecháš. Je třeba tomu hajzlovi domluvit, že tě má v noci nechat. ")
            print("-----------------------------------------")

            # --- START OF FIXED FIGHT LOGIC ---
            rvacka = True 
            rvacka_zivoty_hrac = 10.0 
            rvacka_zivoty_jirasek = 10.0
            rvacka_tah_hrac = True
            rvacka_tah_jirasek = False
            fight_outcome_special = False 

            while rvacka and hra: # Main fight loop, also check if game is still active
                if rvacka_tah_hrac:
                    print("            RVAČKA S JIRÁSKEM")
                    print("-----------------------------------------")
                    print(f"Tvoje životy - {rvacka_zivoty_hrac:.1f}") 
                    print(f"Jiráskovy životy - {rvacka_zivoty_jirasek:.1f}")
                    print("-----------------------------------------")
                    print("                Útočíš!")
                    print("-----------------------------------------")
                    print("1. Hodit po Jiráskovi ředkvičku")
                    print("2. Přiškrtit Jiráska drátovou myší")
                    print("3. Odlákat Jiráska desetikorunou")
                    print("-----------------------------------------")
                    rvacka_vstup = input(">")
                    print("-----------------------------------------")

                    if rvacka_vstup == "1": 
                        if sance(0.65):
                            print("Výborná práce. Jirásek nestihl uhnout a dostal 3 poškození.")
                            rvacka_zivoty_jirasek -= 3.0
                        else:
                            print("To se moc nepovedlo. Netrefil jsi se, asi nemáš mušku z bridže.")
                        rvacka_tah_hrac = False
                        rvacka_tah_jirasek = True
                    elif rvacka_vstup == "2": 
                        if sance(0.3):
                            print("Tohle byla skvělá technika. Jirásek se dusí a ztrácí 6 životů.\n" \
                            "Ještě k tomu můžeš útočit znovu.")
                            rvacka_zivoty_jirasek -= 6.0
                        else:
                            print("To se moc nepovedlo. Jirásek tě chytil za ruku a uštědřil ti 4 poškození.")
                            rvacka_zivoty_hrac -= 4.0
                            rvacka_tah_hrac = False
                            rvacka_tah_jirasek = True
                    elif rvacka_vstup == "3": 
                        if penize >= 10:
                            zmen_penize(-10) 
                            if sance(0.2):
                                print("Skvělá taktika. Židásek ti perfektně skočil na lep a po zbytek noci tě přestal\n" \
                                "otravovat. Zbytek noci se ti spalo perfektně.")
                                fight_outcome_special = True 
                                rvacka = False 
                            else:
                                print("Tohle bylo úplně k ničemu. Pod vlivem adrenalinu asi Židáska\n" \
                                "peníze tolik nezajímají.")
                                rvacka_tah_hrac = False
                                rvacka_tah_jirasek = True
                        else:
                            print("Ještě, kdyby jsi tu desetikorunu měl. Takhle ho sotva odlákáš.")
                            rvacka_tah_hrac = False 
                            rvacka_tah_jirasek = True
                    else:
                        print("Neplatný vstup. Zkus to znovu.")
                        continue 

                    if rvacka_zivoty_jirasek <= 0 or rvacka_zivoty_hrac <= 0:
                        rvacka = False 
                    
                    if not rvacka: 
                        continue

                if rvacka_tah_jirasek and hra: # Check hra here too
                    print("             RVAČKA S JIRÁSKEM")
                    print("-----------------------------------------")
                    print(f"Tvoje životy - {rvacka_zivoty_hrac:.1f}")
                    print(f"Jiráskovy životy - {rvacka_zivoty_jirasek:.1f}")
                    print("-----------------------------------------")
                    print("             Útočí Jirásek!     ")
                    print("-----------------------------------------")

                    if sance(0.5): 
                        print("Jirásek vytáhl svoji píšťalku! Zacpal si uši a je připraven k písknutí!")
                        print("-----------------------------------------")
                        print("1. Taky si zacpat uši a doufat")
                        print("2. Spustit Šalom Chaverim a pokusit se ho překřičet")
                        print("-----------------------------------------")
                        jirasek_utok_pistalka_vstup = input(">")
                        print("-----------------------------------------")
                        if jirasek_utok_pistalka_vstup == "1":
                            if sance(0.5):
                                print("Perfektní. Útok jsi úplně odrazil.")
                            else:
                                print("Doufal jsi zbytečně. Jiráska lze těžko přemoct v zacpávání uší.\n" \
                                "Přicházíš o tři životy.")
                                rvacka_zivoty_hrac -= 3.0
                        elif jirasek_utok_pistalka_vstup == "2":
                            if sance(0.25):
                                print("Fantastický nápad. Z ničeho nic se zjevila postava připomínající\n" \
                                "svou siluetou Sebastiana Skopového a po Židáskovi se málem slehla zem.\n" \
                                "Záhadná postava ti také za tvůj výkon přispěla 100 penězi.")
                                rvacka_zivoty_jirasek -= 7.0
                                zmen_penize(100)
                            else:
                                print("To byl hodně stupidní nápad. Co sis myslel? Že se Židásek lekne?\n" \
                                "Přicházíš o 3 životy.")
                                rvacka_zivoty_hrac -= 3.0
                        else:
                            print("Neplatný vstup pro obranu. Jirásek tě zasáhl, ztrácíš 1 život navíc za zmatkování.")
                            rvacka_zivoty_hrac -= 1.0 
                    else: 
                        print("Židásek se rozhodl, že zavolá Burgetovou, ať se na to přijde podívat.\n" \
                        "Únik před jejím smradem byl nevyhnutelný. Přicházíš o 2 životy." )
                        rvacka_zivoty_hrac -= 2.0
                    
                    rvacka_tah_jirasek = False
                    rvacka_tah_hrac = True

                    if rvacka_zivoty_jirasek <= 0 or rvacka_zivoty_hrac <= 0:
                        rvacka = False
            
            # This block executes after the 'while rvacka:' loop finishes or if 'hra' becomes False
            if hra: # Only print outcomes and advance scene if game didn't end mid-fight
                print("-----------------------------------------") 
                if fight_outcome_special:
                    # Message already printed
                    pass 
                elif rvacka_zivoty_hrac <= 0:
                    print("Celou bitvu s Jiráskem jsi prohrál. Sice tě nechal až do rána spát,\n" \
                    "nemohl jsi ovšem nic dělat s tím, že ti při jeho noční akci ukradl z pěněžěnky\n" \
                    "200 peněz.")
                    zmen_penize(-200)
                elif rvacka_zivoty_jirasek <= 0: 
                    print("Po tomto epickém souboji se ti podařilo Jiráskův útok odrazit. Odešel\n" \
                    "naprosto zdrcený a ještě ti zaplatil 200 za cenu toho, že ho už mlátit\n" \
                    "nebudeš. Následně jsi celou noc spal v pořádku.")
                    zmen_penize(200)
                
                scena += 1
            # --- END OF FIXED FIGHT LOGIC ---
            
        elif scena == 8:
            print("osma scena")
            print("Dorazil jsi do scény 8. Konec testu.")
            hra = False
        
        if not hra: # If any scene logic sets hra to False (e.g. zmen_zivoty -> konec_hry)
            continue # Skip to next iteration of outer while hra, which will then terminate

    else: # Fallback for main menu input
        if vstup != "3": # Option "3" is handled by konec_hry()
            print("Neplatný vstup. Zvolte 1, 2 nebo 3.")

if not hra: 
    print("-----------------------------------------")
    print("Hra byla ukončena.")
    print("-----------------------------------------")
