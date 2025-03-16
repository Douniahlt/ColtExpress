from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from random import *
import pygame
import os

# Créer un module pour remplacer le module liste manquant
class ListeModule:
    def __init__(self):
        self.Actions = []
        # Initialiser les listes de butin pour chaque joueur
        self.butin_joueur1 = []
        self.butin_joueur2 = []
        self.butin_joueur3 = []
        self.butin_joueur4 = []
        
# Créer une instance du module
liste = ListeModule()

# Fonction pour charger et redimensionner une image
def load_and_resize_image(filename, width, height):
    """Charge et redimensionne une image à la taille spécifiée"""
    try:
        img = Image.open(filename)
        img = img.resize((width, height), Image.LANCZOS)  # LANCZOS donne une meilleure qualité
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image {filename}: {e}")
        # Créer une image de remplacement colorée
        placeholder = Image.new('RGB', (width, height), color=(200, 200, 200))
        draw = ImageDraw.Draw(placeholder)
        draw.rectangle([0, 0, width-1, height-1], outline=(0, 0, 0))
        draw.text((width//2, height//2), os.path.basename(filename), fill=(0, 0, 0))
        return ImageTk.PhotoImage(placeholder)

class Jeu(Tk):
    def __init__(self):
        super().__init__()
        
        # Obtenir la taille de l'écran
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # Calculer les facteurs d'échelle
        self.position_factor_x = self.screen_width / 1530  # 1530 étant la largeur originale
        self.position_factor_y = self.screen_height / 860  # 860 étant la hauteur originale
        
        # Images du jeu
        try:
            self.fond = Image.open("Fond.jpg")
            resized = self.fond.resize((self.screen_width, self.screen_height))
            self.fond = ImageTk.PhotoImage(resized)
            
            self.page1 = Label(self, image=self.fond)
            self.page1.place(x=0, y=0)
        except Exception as e:
            print(f"Erreur lors du chargement du fond: {e}")
            # Utiliser un Canvas comme fond de secours
            self.page1 = Canvas(self, bg="black", width=self.screen_width, height=self.screen_height)
            self.page1.place(x=0, y=0)
        
        # Créer un cadre pour le panneau de planification avec un fond semi-transparent
        planning_frame = Frame(self, bg="black", bd=2, relief=RAISED)
        planning_frame.place(
            x=int(10 * self.position_factor_x), 
            y=int(10 * self.position_factor_y),
            width=int(280 * self.position_factor_x), 
            height=int(300 * self.position_factor_y)
        )
        
        # Planification (maintenant placé dans le cadre)
        Planification = Label(planning_frame, text="PLANIFICATION :", bg="black", fg="white", font=("Arial", int(12 * self.position_factor_x), "bold"))
        Planification.pack(anchor=W, padx=10, pady=10)
        
        # Planification tours
        tour_frame = Frame(planning_frame, bg="black")
        tour_frame.pack(fill=X, padx=10, pady=5)
        
        planification_tour = Label(tour_frame, text="Nb de tour :", bg="black", fg="white")
        planification_tour.pack(side=LEFT)
        
        e_tour = Entry(tour_frame, width=15)
        e_tour.pack(side=LEFT, padx=5)
        
        # Constantes du jeu
        self.nb_joueurs = 4
        self.nb_wagons = 4
        self.nb_actions = 4
        self.nb_tours = 5
        
        # Actions stockées pour chaque joueur
        self.actions_joueur1 = []
        self.actions_joueur2 = []
        self.actions_joueur3 = []
        self.actions_joueur4 = []
        
        self.joueur_actuel = 1
        self.tour_actuel = 1
        
        # Positions des joueurs et du Marshall
        self.wagon_actuel_joueur1 = 1
        self.wagon_actuel_joueur2 = 1
        self.wagon_actuel_joueur3 = 1
        self.wagon_actuel_joueur4 = 1
        self.wagon_actuel_marshall = 9
        
        # Initialiser les butins
        self.butin_joueur1 = []
        self.butin_joueur2 = []
        self.butin_joueur3 = []
        self.butin_joueur4 = []
        
        # Valeurs des butins
        self.magot = 1000  # Magot (1000): à l'intérieur de la locomotive avec le Marshall
        self.bijou = 500   # Bijoux (500): auprès des passagers
        self.bourse = 100  # Bourse (100 ou 200): auprès des passagers
        
        # Initialiser les butins dans les wagons
        self.butins_wagon1 = ["bourse", "bourse", "bijou"]
        self.butins_wagon2 = ["bourse", "bijou"]
        self.butins_wagon3 = ["bourse", "bourse"]
        self.butins_wagon4 = ["bijou", "bourse"]
        self.butins_locomotive = ["magot"]
        
        # Créer des représentations visuelles des butins
        self.create_butin_displays()
        
        # Actions dans des frames séparés pour une meilleure organisation
        actions_frame = Frame(planning_frame, bg="black")
        actions_frame.pack(fill=X, padx=10, pady=5)
        
        # Liste des actions
        listeAction = ["Tir", "Braquer", "Haut", "Bas", "Avancer", "Reculer"]
        
        # Créer les labels et combobox pour les actions
        self.action_labels = []
        self.action_combos = []
        
        for i in range(4):
            action_frame = Frame(actions_frame, bg="black")
            action_frame.pack(fill=X, pady=5)
            
            action_label = Label(action_frame, text=f"Action {i+1} :", bg="black", fg="white")
            action_label.pack(side=LEFT)
            
            action_combo = ttk.Combobox(action_frame, values=listeAction, width=15)
            action_combo.current(0)
            action_combo.pack(side=LEFT, padx=5)
            
            self.action_labels.append(action_label)
            self.action_combos.append(action_combo)
        
        # Référence globale aux combobox
        global listeCombo1, listeCombo2, listeCombo3, listeCombo4
        listeCombo1 = self.action_combos[0]
        listeCombo2 = self.action_combos[1]
        listeCombo3 = self.action_combos[2]
        listeCombo4 = self.action_combos[3]
        
        # Bouttons ajustés et stylisés
        buttons_frame = Frame(planning_frame, bg="black")
        buttons_frame.pack(fill=X, padx=10, pady=10)
        
        btn_valider = Button(buttons_frame, text="Valider", command=self.valider, bg="#8B0000", fg="white", font=("Arial", int(10 * self.position_factor_x)))
        btn_valider.pack(side=LEFT, padx=5)
        
        self.btn_action = Button(buttons_frame, text="Actions", command=self.action_exe, bg="#8B0000", fg="white", font=("Arial", int(10 * self.position_factor_x)))
        self.btn_action.pack(side=LEFT, padx=5)
        
        # Scores et affichage dans un cadre distinct
        score_frame = Frame(planning_frame, bg="black")
        score_frame.pack(fill=X, padx=10, pady=5)

        self.result_label = Label(score_frame, text="", bg="black", fg="white")
        self.result_label.pack(anchor=W)
        
        self.score_label = Label(score_frame, text="Scores: J1: 0€ | J2: 0€ | J3: 0€ | J4: 0€", bg="black", fg="white")
        self.score_label.pack(anchor=W)
        
        
        
        # Bouton d'inventaire stylisé
        inventaire_btn = Button(self, text="Voir Inventaires", command=self.show_inventory, bg="#8B0000", fg="white")
        inventaire_btn.place(x=int(self.screen_width - 140 * self.position_factor_x), y=int(60 * self.position_factor_y))
        
        # Instructions intégrées dans le panneau de planification
        instructions_frame = Frame(planning_frame, bg="black", bd=1, relief=RIDGE)
        instructions_frame.pack(fill=X, padx=10, pady=10)
        
        instructions = Label(instructions_frame, text="1. Planifiez vos actions\n2. Validez\n3. Exécutez avec 'Actions'", 
                             bg="black", fg="white", justify=LEFT)
        instructions.pack(anchor=W)
        
        # Vérifier si la partie est terminée
        if self.tour_actuel > self.nb_tours:
            print("Fin du Jeu")
            self.afficher_resultats()
        
        # Taille des personnages adaptée à l'écran
        character_size = int(50 * min(self.position_factor_x, self.position_factor_y))
        
        # Charger les images des personnages
        try:
            self.personnage1 = load_and_resize_image("perso1.png", character_size, character_size)
            self.personnage2 = load_and_resize_image("perso2.jpeg", character_size, character_size)
            self.personnage3 = load_and_resize_image("perso3.png", character_size, character_size)
            self.personnage4 = load_and_resize_image("perso4.jpeg", character_size, character_size)
            self.marshall = load_and_resize_image("marshall.jpg", character_size, character_size)
            
            # Placer les personnages sur le plateau
            self.p1 = Label(self, image=self.personnage1)
            self.p2 = Label(self, image=self.personnage2)
            self.p3 = Label(self, image=self.personnage3)
            self.p4 = Label(self, image=self.personnage4)
            self.p5 = Label(self, image=self.marshall)
            
        except Exception as e:
            print(f"Erreur lors du chargement des personnages: {e}")
            # Créer des rectangles colorés pour représenter les personnages
            self.p1 = Canvas(self, width=character_size, height=character_size, bg="red")
            self.p1.create_text(character_size/2, character_size/2, text="J1", fill="white")
            
            self.p2 = Canvas(self, width=character_size, height=character_size, bg="blue")
            self.p2.create_text(character_size/2, character_size/2, text="J2", fill="white")
            
            self.p3 = Canvas(self, width=character_size, height=character_size, bg="green")
            self.p3.create_text(character_size/2, character_size/2, text="J3", fill="white")
            
            self.p4 = Canvas(self, width=character_size, height=character_size, bg="orange")
            self.p4.create_text(character_size/2, character_size/2, text="J4", fill="white")
            
            self.p5 = Canvas(self, width=character_size, height=character_size, bg="black")
            self.p5.create_text(character_size/2, character_size/2, text="M", fill="white")
        
        # Positions initiales des personnages ajustées
        self.p1.place(x=int(70 * self.position_factor_x), y=int(750 * self.position_factor_y))
        self.p2.place(x=int(120 * self.position_factor_x), y=int(750 * self.position_factor_y))
        self.p3.place(x=int(170 * self.position_factor_x), y=int(750 * self.position_factor_y))
        self.p4.place(x=int(220 * self.position_factor_x), y=int(750 * self.position_factor_y))
        self.p5.place(x=int(1350 * self.position_factor_x), y=int(670 * self.position_factor_y))
        
        # Charger les profils des joueurs
        self.profil()
        
        # Initialiser l'affichage des butins
        self.update_butin_displays()
        
        # Panneau d'information sur les butins avec style amélioré
        butin_info = Frame(self, bg="lightyellow", bd=2, relief=RAISED)
        butin_info.place(
            x=int(self.screen_width - 190 * self.position_factor_x), 
            y=int(100 * self.position_factor_y),
            width=int(180 * self.position_factor_x),
            height=int(120 * self.position_factor_y)
        )
        
        info_title = Label(butin_info, text="Valeurs des butins", bg="lightyellow", font=("Arial", int(10 * min(self.position_factor_x, self.position_factor_y)), "bold"))
        info_title.pack(pady=5)
        
        Label(butin_info, text=f"Bourse: {self.bourse}€", bg="lightyellow").pack(anchor=W, padx=10)
        Label(butin_info, text=f"Bijou: {self.bijou}€", bg="lightyellow").pack(anchor=W, padx=10)
        Label(butin_info, text=f"Magot: {self.magot}€", bg="lightyellow").pack(anchor=W, padx=10)
    
    def create_butin_displays(self):
        """Crée des représentations visuelles pour les butins dans chaque wagon"""
        butin_size = int(20 * min(self.position_factor_x, self.position_factor_y))
        
        # Coordonnées pour afficher les butins (sous les wagons)
        wagon1_x = int(70 * self.position_factor_x)
        wagon2_x = int(320 * self.position_factor_x)
        wagon3_x = int(600 * self.position_factor_x)
        wagon4_x = int(900 * self.position_factor_x)
        locomotive_x = int(1350 * self.position_factor_x)
        
        butin_y = int(800 * self.position_factor_y)
        
        # Style pour les affichages de butins
        butin_bg = "white"
        butin_fg = "darkblue"
        
        # Créer les affichages de butins
        self.butin_displays = {
            'wagon1': Label(self, text="", bg=butin_bg, fg=butin_fg, bd=1, relief=RIDGE),
            'wagon2': Label(self, text="", bg=butin_bg, fg=butin_fg, bd=1, relief=RIDGE),
            'wagon3': Label(self, text="", bg=butin_bg, fg=butin_fg, bd=1, relief=RIDGE),
            'wagon4': Label(self, text="", bg=butin_bg, fg=butin_fg, bd=1, relief=RIDGE),
            'locomotive': Label(self, text="", bg=butin_bg, fg=butin_fg, bd=1, relief=RIDGE)
        }
        
        # Placer les affichages avec une largeur ajustée
        self.butin_displays['wagon1'].place(x=wagon1_x, y=butin_y, width=200*self.position_factor_x)
        self.butin_displays['wagon2'].place(x=wagon2_x, y=butin_y, width=200*self.position_factor_x)
        self.butin_displays['wagon3'].place(x=wagon3_x, y=butin_y, width=200*self.position_factor_x)
        self.butin_displays['wagon4'].place(x=wagon4_x, y=butin_y, width=200*self.position_factor_x)
        self.butin_displays['locomotive'].place(x=locomotive_x, y=butin_y, width=200*self.position_factor_x)
        
        # Ajouter des étiquettes pour les wagons
        wagon_labels = [
            Label(self, text="Wagon 1", bg=butin_bg, fg="black", font=("Arial", 8, "bold")),
            Label(self, text="Wagon 2", bg=butin_bg, fg="black", font=("Arial", 8, "bold")),
            Label(self, text="Wagon 3", bg=butin_bg, fg="black", font=("Arial", 8, "bold")),
            Label(self, text="Wagon 4", bg=butin_bg, fg="black", font=("Arial", 8, "bold")),
            Label(self, text="Locomotive", bg=butin_bg, fg="black", font=("Arial", 8, "bold"))
        ]
        
        # Placer les étiquettes au-dessus des affichages de butins
        wagon_labels[0].place(x=wagon1_x, y=butin_y-25*self.position_factor_y)
        wagon_labels[1].place(x=wagon2_x, y=butin_y-25*self.position_factor_y)
        wagon_labels[2].place(x=wagon3_x, y=butin_y-25*self.position_factor_y)
        wagon_labels[3].place(x=wagon4_x, y=butin_y-25*self.position_factor_y)
        wagon_labels[4].place(x=locomotive_x, y=butin_y-25*self.position_factor_y)
    
    def update_butin_displays(self):
        """Met à jour l'affichage des butins dans chaque wagon"""
        # Compter les butins dans chaque wagon
        wagon1_content = self.format_butin_content(self.butins_wagon1)
        wagon2_content = self.format_butin_content(self.butins_wagon2)
        wagon3_content = self.format_butin_content(self.butins_wagon3)
        wagon4_content = self.format_butin_content(self.butins_wagon4)
        locomotive_content = self.format_butin_content(self.butins_locomotive)
        
        # Mettre à jour les labels
        self.butin_displays['wagon1'].config(text=f"{wagon1_content}")
        self.butin_displays['wagon2'].config(text=f"{wagon2_content}")
        self.butin_displays['wagon3'].config(text=f"{wagon3_content}")
        self.butin_displays['wagon4'].config(text=f"{wagon4_content}")
        self.butin_displays['locomotive'].config(text=f"{locomotive_content}")
    
    def format_butin_content(self, butin_list):
        """Formate la liste de butins pour l'affichage"""
        if not butin_list:
            return "vide"
        
        # Compter les types de butins
        bourse_count = butin_list.count("bourse")
        bijou_count = butin_list.count("bijou")
        magot_count = butin_list.count("magot")
        
        content = []
        if bourse_count > 0:
            content.append(f"{bourse_count} bourse(s)")
        if bijou_count > 0:
            content.append(f"{bijou_count} bijou(x)")
        if magot_count > 0:
            content.append(f"{magot_count} magot(s)")
            
        return ", ".join(content)
    
    def get_current_wagon(self, joueur_id):
        """Obtient la position actuelle du joueur spécifié"""
        if joueur_id == 1:
            return self.wagon_actuel_joueur1
        elif joueur_id == 2:
            return self.wagon_actuel_joueur2
        elif joueur_id == 3:
            return self.wagon_actuel_joueur3
        elif joueur_id == 4:
            return self.wagon_actuel_joueur4
        return 0
    
    def set_current_wagon(self, joueur_id, wagon):
        """Définit la position du joueur spécifié"""
        if joueur_id == 1:
            self.wagon_actuel_joueur1 = wagon
        elif joueur_id == 2:
            self.wagon_actuel_joueur2 = wagon
        elif joueur_id == 3:
            self.wagon_actuel_joueur3 = wagon
        elif joueur_id == 4:
            self.wagon_actuel_joueur4 = wagon
    
    def get_butin_joueur(self, joueur_id):
        """Récupère le butin du joueur spécifié"""
        if joueur_id == 1:
            return self.butin_joueur1
        elif joueur_id == 2:
            return self.butin_joueur2
        elif joueur_id == 3:
            return self.butin_joueur3
        elif joueur_id == 4:
            return self.butin_joueur4
        return []
    
    def get_actions_joueur(self, joueur_id):
        """Récupère les actions planifiées du joueur spécifié"""
        if joueur_id == 1:
            return self.actions_joueur1
        elif joueur_id == 2:
            return self.actions_joueur2
        elif joueur_id == 3:
            return self.actions_joueur3
        elif joueur_id == 4:
            return self.actions_joueur4
        return []
    
    def get_butin_wagon(self, wagon_number):
        """Récupère la liste des butins disponibles dans un wagon spécifique"""
        if wagon_number == 1:
            return self.butins_wagon1
        elif wagon_number == 2:
            return self.butins_wagon2
        elif wagon_number == 3:
            return self.butins_wagon3
        elif wagon_number == 4:
            return self.butins_wagon4
        elif wagon_number == 5:  # La locomotive
            return self.butins_locomotive
        return []
    
    def valider(self):
        """Valide les actions sélectionnées et passe au joueur suivant"""
        self.recup_action()
        self.action_joueur()
        
        if self.joueur_actuel >= self.nb_joueurs:
            # Passer à la phase d'action quand tous les joueurs ont planifié
            self.phase_label.config(text="Phase: Action")
            self.joueur_actuel = 1
            self.result_label.config(text="Début de la phase d'action. Cliquez sur 'Actions' pour exécuter.")
        else:
            self.joueur_actuel += 1
            self.result_label.config(text=f"Joueur {self.joueur_actuel}, planifiez vos actions.")
        
        # Mettre à jour l'image du joueur actuel
        self.profil()
        
        # Réinitialiser les combobox
        global listeCombo1, listeCombo2, listeCombo3, listeCombo4
        listeCombo1.current(0)
        listeCombo2.current(0)
        listeCombo3.current(0)
        listeCombo4.current(0)
        
        # Mettre à jour les scores
        self.update_scores()
    
    def profil(self):
        """Met à jour l'affichage du profil du joueur actuel"""
        profile_size = int(100 * min(self.position_factor_x, self.position_factor_y))
        
        try:
            # Charger les images des profils des joueurs
            self.joueur1 = load_and_resize_image("joueur1.jpg", profile_size, profile_size)
            self.joueur2 = load_and_resize_image("joueur2.jpg", profile_size, profile_size)
            self.joueur3 = load_and_resize_image("joueur3.jpg", profile_size, profile_size)
            self.joueur4 = load_and_resize_image("joueur4.jpg", profile_size, profile_size)
            
            # Sélectionner l'image en fonction du joueur actuel
            images = {
                1: self.joueur1,
                2: self.joueur2,
                3: self.joueur3,
                4: self.joueur4
            }
            
            self.img = images.get(self.joueur_actuel, self.joueur1)
            
            # Mettre à jour l'affichage
            if hasattr(self, 'page2'):
                self.page2.destroy()
            
            self.page2 = Label(self, image=self.img)
            self.page2.place(x=int(300 * self.position_factor_x), y=0)
        except Exception as e:
            print(f"Erreur lors du chargement du profil: {e}")
            # Créer un rectangle coloré comme profil de secours
            if hasattr(self, 'page2'):
                self.page2.destroy()
            
            self.page2 = Canvas(self, bg="lightgray", width=profile_size, height=profile_size)
            self.page2.place(x=int(300 * self.position_factor_x), y=0)
            self.page2.create_text(profile_size//2, profile_size//2, text=f"Joueur {self.joueur_actuel}")
        
        # Mise à jour du titre pour indiquer le joueur actuel
        self.title(f"Colt Express - Joueur {self.joueur_actuel}")
    
    def pos_joueur(self):
        """Met à jour l'affichage des positions de tous les joueurs"""
        # Positions des joueurs (coordonnées x,y pour chaque wagon) ajustées à l'écran
        positions_x = {
            1: [int(70 * self.position_factor_x), int(320 * self.position_factor_x), 
                int(600 * self.position_factor_x), int(900 * self.position_factor_x), 
                int(70 * self.position_factor_x), int(320 * self.position_factor_x), 
                int(600 * self.position_factor_x), int(900 * self.position_factor_x), 
                int(1540 * self.position_factor_x)],  # Joueur 1
            
            2: [int(110 * self.position_factor_x), int(360 * self.position_factor_x), 
                int(640 * self.position_factor_x), int(940 * self.position_factor_x), 
                int(110 * self.position_factor_x), int(360 * self.position_factor_x), 
                int(640 * self.position_factor_x), int(940 * self.position_factor_x), 
                int(1580 * self.position_factor_x)],  # Joueur 2
            
            3: [int(150 * self.position_factor_x), int(400 * self.position_factor_x), 
                int(680 * self.position_factor_x), int(980 * self.position_factor_x), 
                int(150 * self.position_factor_x), int(400 * self.position_factor_x), 
                int(680 * self.position_factor_x), int(980 * self.position_factor_x), 
                int(1620 * self.position_factor_x)],  # Joueur 3
            
            4: [int(190 * self.position_factor_x), int(440 * self.position_factor_x), 
                int(720 * self.position_factor_x), int(1020 * self.position_factor_x), 
                int(190 * self.position_factor_x), int(440 * self.position_factor_x), 
                int(720 * self.position_factor_x), int(1020 * self.position_factor_x), 
                int(1660 * self.position_factor_x)]  # Joueur 4
        }
        
        positions_y = {
            'interieur': int(750 * self.position_factor_y),  # Wagons 1-4
            'toit': int(625 * self.position_factor_y),       # Wagons 5-8 (toit)
            'locomotive': int(670 * self.position_factor_y)  # Wagon 9 (locomotive)
        }
        
        # Mettre à jour la position de chaque joueur
        for joueur_id in range(1, 5):
            wagon = self.get_current_wagon(joueur_id)
            
            
            # Récupérer le widget d'affichage du joueur
            joueur_widget = getattr(self, f"p{joueur_id}")
            
            # Déterminer les coordonnées x et y
            x = positions_x[joueur_id][min(8, wagon-1)]  # -1 pour l'index de 0-8
            
            if wagon == 9:  # Locomotive
                y = positions_y['locomotive']
            elif wagon >= 5:  # Toit
                y = positions_y['toit']
            else:  # Intérieur
                y = positions_y['interieur']
            
            # Mettre à jour la position
            joueur_widget.place(x=x, y=y)
    
    def pos_marshall(self):
        """Met à jour l'affichage de la position du Marshall"""
        # Positions du Marshall (coordonnées x,y pour chaque wagon) ajustées à l'écran
        positions_x = [
            int(230 * self.position_factor_x),
            int(480 * self.position_factor_x),
            int(760 * self.position_factor_x),
            int(1060 * self.position_factor_x),
            int(1350 * self.position_factor_x)
        ]  # Les 4 wagons + locomotive
        
        # Obtenir la position du Marshall
        if self.wagon_actuel_marshall == 9:  # Locomotive
            self.p5.place(x=positions_x[4], y=int(670 * self.position_factor_y))
        else:  # Wagon intérieur (1-4)
            self.p5.place(x=positions_x[self.wagon_actuel_marshall-1], y=int(750 * self.position_factor_y))
    
    def recup_action(self):
        """Récupère les actions sélectionnées dans les combobox"""
        global listeCombo1, listeCombo2, listeCombo3, listeCombo4
        liste.Actions = []

        # Récupérer les actions des combobox
        liste.Actions.append(listeCombo1.get())
        liste.Actions.append(listeCombo2.get())
        liste.Actions.append(listeCombo3.get())
        liste.Actions.append(listeCombo4.get())
        
        # Afficher les actions sélectionnées
        print("Actions sélectionnées:")
        for i, action in enumerate(liste.Actions, 1):
            print(f"Action {i}: {action}")
    
    def action_joueur(self):
        """Stocke les actions planifiées pour le joueur actuel"""
        if self.joueur_actuel == 1:
            self.actions_joueur1 = liste.Actions.copy()  # Utiliser copy() pour éviter des problèmes de référence
            print("Actions joueur 1:")
            print(self.actions_joueur1)
        
        elif self.joueur_actuel == 2:
            self.actions_joueur2 = liste.Actions.copy()
            print("Actions joueur 2:")
            print(self.actions_joueur2)
        
        elif self.joueur_actuel == 3:
            self.actions_joueur3 = liste.Actions.copy()
            print("Actions joueur 3:")
            print(self.actions_joueur3)
            
        elif self.joueur_actuel == 4:
            self.actions_joueur4 = liste.Actions.copy()
            print("Actions joueur 4:")
            print(self.actions_joueur4)
            
        else:
            print("Erreur: Joueur invalide")
    
    def action_exe(self):
        """Exécute l'action suivante du joueur actuel"""
        action_text = ""
        
        # Récupérer la liste d'actions du joueur actuel
        actions_joueur = self.get_actions_joueur(self.joueur_actuel)
        
        # S'il reste des actions à exécuter
        if actions_joueur:
            # Récupérer la prochaine action
            action = actions_joueur[0]
            
            # Exécuter l'action correspondante
            if action == "Avancer":
                self.avancer()
                action_text = f"Joueur {self.joueur_actuel} avance."
            elif action == "Reculer":
                self.reculer()
                action_text = f"Joueur {self.joueur_actuel} recule."
            elif action == "Haut":
                self.haut()
                action_text = f"Joueur {self.joueur_actuel} monte sur le toit."
            elif action == "Bas":
                self.bas()
                action_text = f"Joueur {self.joueur_actuel} descend du toit."
            elif action == "Tir":
                self.tir()
                action_text = f"Joueur {self.joueur_actuel} tire."
            elif action == "Braquer":
                self.braquer()
                action_text = f"Joueur {self.joueur_actuel} braque un passager."

                # Supprimer l'action exécutée
            del actions_joueur[0]
            
        print(f"Joueur actuel: {self.joueur_actuel}")
        print(f"Position des joueurs: {self.wagon_actuel_joueur1}, {self.wagon_actuel_joueur2}, {self.wagon_actuel_joueur3}, {self.wagon_actuel_joueur4}")
        print(f"Position du marshall: {self.wagon_actuel_marshall}")
        
        # Mettre à jour le label de résultat
        self.result_label.config(text=action_text)
        
        # Mettre à jour la position des joueurs
        self.pos_joueur()
        
        # Le Marshall se déplace après chaque action d'un joueur
        self.deplacement_marshall()
        
        # Mettre à jour la position du Marshall
        self.pos_marshall()
        
        # Vérifier si un joueur croise le Marshall
        self.lacheButtin()
        
        # Mettre à jour l'affichage des butins
        self.update_butin_displays()
        
        # Passer au joueur suivant
        if self.joueur_actuel >= self.nb_joueurs:
            self.joueur_actuel = 1
        else:
            self.joueur_actuel += 1
        
        # Mettre à jour l'image du joueur actuel
        self.profil()
        
        # Vérifier si toutes les actions sont complétées
        if not self.actions_joueur1 and not self.actions_joueur2 and not self.actions_joueur3 and not self.actions_joueur4:
            self.tour_actuel += 1
            self.phase_label.config(text="Phase: Planification")
            
            # Mettre à jour le compteur de tours
            self.tour_label.config(text=f"Tour: {self.tour_actuel}/{self.nb_tours}")
            
            # Vérifier si le jeu est terminé
            if self.tour_actuel > self.nb_tours:
                self.afficher_resultats()
        
        # Mettre à jour les scores
        self.update_scores()
    
    def avancer(self):
        """Déplace le joueur actuel d'un wagon vers l'avant"""
        wagon_actuel = self.get_current_wagon(self.joueur_actuel)
        
        # Règles de déplacement
        if wagon_actuel == 4:
            # Du dernier wagon à la locomotive
            self.set_current_wagon(self.joueur_actuel, 9)
        elif wagon_actuel not in [8, 9]:
            # Avancer normalement
            self.set_current_wagon(self.joueur_actuel, wagon_actuel + 1)
    
    def reculer(self):
        """Déplace le joueur actuel d'un wagon vers l'arrière"""
        wagon_actuel = self.get_current_wagon(self.joueur_actuel)
        
        # Règles de déplacement
        if wagon_actuel == 9:
            # De la locomotive au dernier wagon
            self.set_current_wagon(self.joueur_actuel, 4)
        elif wagon_actuel not in [1, 5]:
            # Reculer normalement
            self.set_current_wagon(self.joueur_actuel, wagon_actuel - 1)
    
    def haut(self):
        """Déplace le joueur actuel vers le toit de son wagon"""
        wagon_actuel = self.get_current_wagon(self.joueur_actuel)
        
        # Règles de déplacement vers le toit (ajouter 4)
        if 1 <= wagon_actuel <= 4:
            self.set_current_wagon(self.joueur_actuel, wagon_actuel + 4)
    
    def bas(self):
        """Déplace le joueur actuel vers l'intérieur de son wagon"""
        wagon_actuel = self.get_current_wagon(self.joueur_actuel)
        
        # Règles de déplacement vers l'intérieur (soustraire 4)
        if 5 <= wagon_actuel <= 8:
            self.set_current_wagon(self.joueur_actuel, wagon_actuel - 4)

    def tir(self):
        """Tire sur un autre joueur dans le même wagon"""
        print("tir")
        
        # Obtenir la position du tireur
        wagon_tireur = self.get_current_wagon(self.joueur_actuel)
        
        # Liste des joueurs qui peuvent être touchés (dans le même wagon)
        cibles_potentielles = []
        butin_cibles = []
        
        # Vérifier quels joueurs sont dans le même wagon
        for joueur_id in range(1, 5):
            if joueur_id != self.joueur_actuel and self.get_current_wagon(joueur_id) == wagon_tireur:
                butin = self.get_butin_joueur(joueur_id)
                if butin:  # Ne peut tirer que sur des joueurs ayant du butin
                    cibles_potentielles.append(joueur_id)
                    butin_cibles.append(butin)
        
        # S'il y a des cibles potentielles
        if cibles_potentielles:
            # Choisir une cible au hasard
            index_cible = randint(0, len(cibles_potentielles) - 1)
            joueur_cible = cibles_potentielles[index_cible]
            butin_cible = butin_cibles[index_cible]
            
            # Voler un butin au hasard
            butin_vole = choice(butin_cible)
            butin_cible.remove(butin_vole)
            
            # Ajouter le butin au joueur actuel
            self.get_butin_joueur(self.joueur_actuel).append(butin_vole)
            
            message = f"Joueur {self.joueur_actuel} tire sur Joueur {joueur_cible} et récupère un {butin_vole}!"
            print(message)
            self.result_label.config(text=message)
        else:
            message = f"Joueur {self.joueur_actuel} tire mais ne touche personne!"
            print(message)
            self.result_label.config(text=message)
    
    def braquer(self):
        """Braque un passager pour récupérer un butin"""
        print("braquer")
        
        # Obtenir le wagon actuel du joueur (convertir les valeurs spéciales comme 9 pour la locomotive)
        wagon_actuel = self.get_current_wagon(self.joueur_actuel)
        position_reelle = wagon_actuel
        
        # Sur le toit, impossible de braquer
        if 5 <= wagon_actuel <= 8:
            self.result_label.config(text="Impossible de braquer sur le toit!")
            return
            
        # Convertir la position de la locomotive
        if wagon_actuel == 9:
            position_reelle = 5  # Position 5 = locomotive pour l'accès au butin
        
        # Récupérer les butins disponibles dans ce wagon
        butins_disponibles = self.get_butin_wagon(position_reelle)
        
        # Si le Marshall est présent dans la locomotive, impossible de braquer
        if position_reelle == 5 and self.wagon_actuel_marshall == 9:
            self.result_label.config(text="Impossible de braquer avec le Marshall présent!")
            return
        
        # S'il y a des butins disponibles
        if butins_disponibles:
            # Prendre un butin au hasard
            index_butin = randint(0, len(butins_disponibles) - 1)
            butin = butins_disponibles.pop(index_butin)
            
            # Ajouter le butin au joueur
            self.get_butin_joueur(self.joueur_actuel).append(butin)
            
            message = f"Joueur {self.joueur_actuel} braque un {butin}!"
            print(message)
            self.result_label.config(text=message)
        else:
            message = "Il n'y a plus rien à braquer dans ce wagon!"
            print(message)
            self.result_label.config(text=message)
    
    def lacheButtin(self):
        """Vérifie si un joueur est dans le même wagon que le Marshall et lui fait lâcher un butin"""
        # Vérifier chaque joueur
        for joueur_id in range(1, 5):
            wagon_joueur = self.get_current_wagon(joueur_id)
            
            # Si le joueur est dans le même wagon que le Marshall et à l'intérieur (pas sur le toit)
            if wagon_joueur == self.wagon_actuel_marshall and wagon_joueur <= 4:
                butin_joueur = self.get_butin_joueur(joueur_id)
                
                # Si le joueur a du butin
                if butin_joueur:
                    # Choisir un butin au hasard à lâcher
                    butin = choice(butin_joueur)
                    butin_joueur.remove(butin)
                    
                    # Ajouter le butin au wagon
                    wagon_reel = wagon_joueur if wagon_joueur <= 4 else 5  # Convertir locomotive (9) en 5
                    self.get_butin_wagon(wagon_reel).append(butin)
                    
                    message = f"Le Marshall attrape Joueur {joueur_id} qui lâche un {butin}!"
                    print(message)
                    self.result_label.config(text=message)
                
                # Envoyer le joueur sur le toit
                self.fuit(joueur_id)
    
    def fuit(self, joueur_id=None):
        """Envoie le joueur spécifié (ou le joueur actuel) sur le toit de son wagon"""
        # Si aucun joueur spécifié, utiliser le joueur actuel
        if joueur_id is None:
            joueur_id = self.joueur_actuel
            
        wagon_joueur = self.get_current_wagon(joueur_id)
        
        # Si le joueur est à l'intérieur d'un wagon (1-4), l'envoyer sur le toit
        if 1 <= wagon_joueur <= 4:
            self.set_current_wagon(joueur_id, wagon_joueur + 4)
        # Si le joueur est dans la locomotive (9), il ne peut pas fuir sur le toit
    
    def deplacement_marshall(self):
        """Déplace le Marshall aléatoirement dans une direction"""
        n = random()
        if n <= 0.5:
            self.reculer_marshall()
        else:
            self.avancer_marshall()
        
        print(f"Le Marshall se déplace vers le wagon {self.wagon_actuel_marshall}")
    
    def avancer_marshall(self):
        """Déplace le Marshall d'un wagon vers l'avant"""
        if self.wagon_actuel_marshall == 1:
            pass  # Déjà au premier wagon
        elif self.wagon_actuel_marshall == 9:
            self.wagon_actuel_marshall = 4  # De la locomotive au dernier wagon
        else:
            self.wagon_actuel_marshall -= 1
    
    def reculer_marshall(self):
        """Déplace le Marshall d'un wagon vers l'arrière"""
        if self.wagon_actuel_marshall == 4:
            self.wagon_actuel_marshall = 9  # Du dernier wagon à la locomotive
        elif self.wagon_actuel_marshall == 9:
            pass  # Déjà dans la locomotive
        else:
            self.wagon_actuel_marshall += 1
    
    def calculate_score(self, butin_list):
        """Calcule le score total des butins d'un joueur"""
        score = 0
        for butin in butin_list:
            if butin == "bourse":
                score += self.bourse
            elif butin == "bijou":
                score += self.bijou
            elif butin == "magot":
                score += self.magot
        return score
    
    def update_scores(self):
        """Met à jour l'affichage des scores"""
        # Calculer les scores de chaque joueur
        scores = [
            self.calculate_score(self.butin_joueur1),
            self.calculate_score(self.butin_joueur2),
            self.calculate_score(self.butin_joueur3),
            self.calculate_score(self.butin_joueur4)
        ]
        
        # Mettre à jour le label des scores
        self.score_label.config(text=f"Scores: J1: {scores[0]}€ | J2: {scores[1]}€ | J3: {scores[2]}€ | J4: {scores[3]}€")

    def afficher_resultats(self):
        """Affiche la fenêtre des résultats finaux"""
        # Calculer les scores finaux
        scores = [
            self.calculate_score(self.butin_joueur1),
            self.calculate_score(self.butin_joueur2),
            self.calculate_score(self.butin_joueur3),
            self.calculate_score(self.butin_joueur4)
        ]
        
        # Déterminer le gagnant
        max_score = max(scores)
        gagnant = scores.index(max_score) + 1
        
        # Créer une fenêtre pour afficher les résultats
        result_window = Toplevel(self)
        result_window.title("Résultats")
        
        # Adapter la taille au facteur d'échelle
        result_window.geometry(f"{int(400 * self.position_factor_x)}x{int(300 * self.position_factor_y)}")
        
        # Titre
        title_label = Label(result_window, text="Fin de la partie !", font=("Arial", int(14 * min(self.position_factor_x, self.position_factor_y))))
        title_label.pack(pady=int(10 * self.position_factor_y))
        
        # Scores
        scores_label = Label(result_window, text=f"Scores finaux:\n" +
                                               f"Joueur 1: {scores[0]}€\n" +
                                               f"Joueur 2: {scores[1]}€\n" +
                                               f"Joueur 3: {scores[2]}€\n" +
                                               f"Joueur 4: {scores[3]}€",
                           font=("Arial", int(12 * min(self.position_factor_x, self.position_factor_y))))
        scores_label.pack(pady=int(10 * self.position_factor_y))
        
        # Gagnant
        winner_label = Label(result_window, text=f"Le joueur {gagnant} remporte la partie!",
                            font=("Arial", int(14 * min(self.position_factor_x, self.position_factor_y)), "bold"))
        winner_label.pack(pady=int(10 * self.position_factor_y))
        
        # Bouton pour fermer
        close_button = Button(result_window, text="Fermer", command=result_window.destroy)
        close_button.pack(pady=int(10 * self.position_factor_y))
    
    def show_inventory(self):
        """Affiche une fenêtre avec l'inventaire de tous les joueurs"""
        inventory_window = Toplevel(self)
        inventory_window.title("Inventaires des joueurs")
        
        # Adapter la taille au facteur d'échelle
        inventory_window.geometry(f"{int(400 * self.position_factor_x)}x{int(400 * self.position_factor_y)}")
        
        # Afficher l'inventaire de chaque joueur
        for joueur_id in range(1, 5):
            butin = self.get_butin_joueur(joueur_id)
            
            # Compter les types de butin
            bourse_count = butin.count("bourse")
            bijou_count = butin.count("bijou")
            magot_count = butin.count("magot")
            
            # Calculer la valeur totale
            value = bourse_count * self.bourse + bijou_count * self.bijou + magot_count * self.magot
            
            # Créer le label avec les informations
            label_text = f"Joueur {joueur_id}:\n" + \
                        f"Bourses: {bourse_count} ({bourse_count * self.bourse}€)\n" + \
                        f"Bijoux: {bijou_count} ({bijou_count * self.bijou}€)\n" + \
                        f"Magots: {magot_count} ({magot_count * self.magot}€)\n" + \
                        f"Total: {value}€\n"
            
            Label(inventory_window, text=label_text, 
                 font=("Arial", int(10 * min(self.position_factor_x, self.position_factor_y)))).pack(
                pady=int(10 * self.position_factor_y))
        
        Button(inventory_window, text="Fermer", command=inventory_window.destroy).pack(
            pady=int(10 * self.position_factor_y))


# Code principal pour exécuter le jeu
if __name__ == "__main__":
    # Vérifier et créer les placeholders pour les images manquantes
    required_images = [
        "Fond.jpg", "perso1.png", "perso2.jpeg", "perso3.png", "perso4.jpeg", 
        "marshall.jpg", "joueur1.jpg", "joueur2.jpg", "joueur3.jpg", "joueur4.jpg",
        "menu.jpeg", "rulesdujeu.jpg", "play1.gif", "exit1.gif", "rules.gif", 
        "menu1.gif", "serdaigle.gif", "gryffondor.gif", "poufsouffle.gif", 
        "serpentard.gif", "arrêt.gif"
    ]
    
    for img_file in required_images:
        if not os.path.exists(img_file):
            # Créer une image placeholder si le fichier n'existe pas
            placeholder = Image.new('RGB', (300, 300), color=(200, 200, 200))
            draw = ImageDraw.Draw(placeholder)
            draw.text((150, 150), img_file, fill=(0, 0, 0))
            placeholder.save(img_file)
    
    # Initialiser pygame pour les sons
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"Erreur lors de l'initialisation du mixer: {e}")
    
    # Créer la fenêtre principale
    mon_jeu = Jeu()
    
    # Obtenir la taille de l'écran
    screen_width = mon_jeu.winfo_screenwidth()
    screen_height = mon_jeu.winfo_screenheight()
    
    # Calculer les facteurs d'échelle
    position_factor_x = screen_width / 1530
    position_factor_y = screen_height / 860
    
    # Géométrie des fenêtres adaptée à l'écran
    mon_jeu.withdraw()
    mon_jeu.geometry(f"{screen_width}x{screen_height}")
    mon_jeu.attributes('-fullscreen', True)
    
    # Fenêtre de menu
    a = Toplevel(mon_jeu)
    a.geometry(f"{screen_width}x{screen_height}")
    a.attributes('-fullscreen', True)
    
    # Fenêtre de règles
    b = Toplevel(mon_jeu)
    b.withdraw()
    b.geometry(f"{screen_width}x{screen_height}")
    b.attributes('-fullscreen', True)
    
    # Configurer les titres
    mon_jeu.title("Colt Express")
    a.title("Colt Express - Menu")
    b.title("Colt Express - Règles")

    # Image de fond pour le menu adaptée à l'écran
    try:
        img_menu = Image.open("menu.jpeg")
        resized = img_menu.resize((screen_width, screen_height))
        img_menu = ImageTk.PhotoImage(resized)
        
        page1 = Label(a, image=img_menu)
        page1.place(x=0, y=0)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image du menu: {e}")
        # Créer un fond de couleur en cas d'erreur
        page1 = Canvas(a, bg="lightblue", width=screen_width, height=screen_height)
        page1.place(x=0, y=0)
    
    # Frame pour les boutons du menu
    frame1 = Frame(a)
    frame1.pack(side=RIGHT, padx=int(15 * position_factor_x), pady=int(20 * position_factor_y))
    
    # Image des règles adaptée à l'écran
    try:
        rules = Image.open("rulesdujeu.jpg")
        resized = rules.resize((screen_width, screen_height))
        rules = ImageTk.PhotoImage(resized)
        
        page_rules = Label(b, image=rules)
        page_rules.place(x=0, y=0)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image des règles: {e}")
        # Créer un fond de couleur en cas d'erreur
        page_rules = Canvas(b, bg="beige", width=screen_width, height=screen_height)
        page_rules.place(x=0, y=0)
        page_rules.create_text(screen_width//2, screen_height//2, text="Règles du jeu", font=("Arial", int(20 * min(position_factor_x, position_factor_y))))
    
    # Fonctions de navigation entre les fenêtres
    def lancefen():
        a.withdraw() 
        mon_jeu.deiconify()
    
    def lancefen2():
        a.withdraw() 
        b.deiconify()
        
    def switch():
        mon_jeu.withdraw()
        a.deiconify()
    
    def switch2():
        b.withdraw()
        a.deiconify()
    
    # Gérer les sons du jeu
    sounds = {}
    
    # Essayer de charger les sons
    try:
        sounds["Serdaigle.mp3"] = pygame.mixer.Sound("Serdaigle.mp3")
        sounds["Gryffondor.mp3"] = pygame.mixer.Sound("Gryffondor.mp3")
        sounds["Poufsouffle.mp3"] = pygame.mixer.Sound("Poufsouffle.mp3")
        sounds["Serpentard.mp3"] = pygame.mixer.Sound("Serpentard.mp3")
    except Exception as e:
        print(f"Erreur lors du chargement des sons: {e}")
        # Créer des fichiers vides si nécessaire
        for sound_name in ["Serdaigle.mp3", "Gryffondor.mp3", "Poufsouffle.mp3", "Serpentard.mp3"]:
            if not os.path.exists(sound_name):
                open(sound_name, 'a').close()
            sounds[sound_name] = None
    
    # Fonctions pour les sons
    def play_sound(sound_key, sounds_dict):
        """Joue un son avec gestion d'erreur améliorée"""
        try:
            if sound_key in sounds_dict and sounds_dict[sound_key]:
                sounds_dict[sound_key].play(-1)
                # Arrêter les autres sons
                for key, sound in sounds_dict.items():
                    if key != sound_key and sound:
                        sound.stop()
        except Exception as e:
            print(f"Erreur lors de la lecture du son {sound_key}: {e}")

    def stop_sound(sound_key, sounds_dict):
        """Arrête un son avec gestion d'erreur améliorée"""
        try:
            if sound_key in sounds_dict and sounds_dict[sound_key]:
                sounds_dict[sound_key].stop()
        except Exception as e:
            print(f"Erreur lors de l'arrêt du son {sound_key}: {e}")
    
    def play1():
        play_sound("Serdaigle.mp3", sounds)
        
    def stop1():
        stop_sound("Serdaigle.mp3", sounds)
    
    def play2():
        play_sound("Gryffondor.mp3", sounds)
        
    def stop2():
        stop_sound("Gryffondor.mp3", sounds)
    
    def play3():
        play_sound("Poufsouffle.mp3", sounds)
        
    def stop3():
        stop_sound("Poufsouffle.mp3", sounds)
    
    def play4():
        play_sound("Serpentard.mp3", sounds)
        
    def stop4():
        stop_sound("Serpentard.mp3", sounds)
    
    # Taille des images de boutons ajustée à l'écran
    button_size = int(50 * min(position_factor_x, position_factor_y))
    
    # Charger et redimensionner les images des boutons de manière correcte
    try:
        ser_img = Image.open('serdaigle.gif')
        ser_img = ser_img.resize((button_size, button_size), Image.LANCZOS)
        ser = ImageTk.PhotoImage(ser_img)
        
        gry_img = Image.open('gryffondor.gif')
        gry_img = gry_img.resize((button_size, button_size), Image.LANCZOS)
        gry = ImageTk.PhotoImage(gry_img)
        
        pou_img = Image.open('poufsouffle.gif')
        pou_img = pou_img.resize((button_size, button_size), Image.LANCZOS)
        pou = ImageTk.PhotoImage(pou_img)
        
        serp_img = Image.open('serpentard.gif')
        serp_img = serp_img.resize((button_size, button_size), Image.LANCZOS)
        serp = ImageTk.PhotoImage(serp_img)
        
        arr_img = Image.open('arrêt.gif')
        arr_img = arr_img.resize((button_size, button_size), Image.LANCZOS)
        arr = ImageTk.PhotoImage(arr_img)
        
        play_picture = load_and_resize_image('play1.gif', int(100 * position_factor_x), int(60 * position_factor_y))
        exit_picture = load_and_resize_image('exit1.gif', int(100 * position_factor_x), int(60 * position_factor_y))
        rules_picture = load_and_resize_image('rules.gif', int(100 * position_factor_x), int(60 * position_factor_y))
        menu_picture = load_and_resize_image('menu1.gif', int(100 * position_factor_x), int(60 * position_factor_y))
    except Exception as e:
        print(f"Erreur lors du chargement des images des boutons: {e}")
        # Créer des images vides pour les boutons si nécessaire
        ser = PhotoImage(width=button_size, height=button_size)
        gry = PhotoImage(width=button_size, height=button_size)
        pou = PhotoImage(width=button_size, height=button_size)
        serp = PhotoImage(width=button_size, height=button_size)
        arr = PhotoImage(width=button_size, height=button_size)
        play_picture = PhotoImage(width=int(100 * position_factor_x), height=int(60 * position_factor_y))
        exit_picture = PhotoImage(width=int(100 * position_factor_x), height=int(60 * position_factor_y))
        rules_picture = PhotoImage(width=int(100 * position_factor_x), height=int(60 * position_factor_y))
        menu_picture = PhotoImage(width=int(100 * position_factor_x), height=int(60 * position_factor_y))
    
    # Boutons du menu
    btn_exit = Button(frame1, image=exit_picture, command=mon_jeu.destroy)
    btn_exit.pack(pady=int(10 * position_factor_y))
    
    btn_play = Button(frame1, image=play_picture, command=lancefen)
    btn_play.pack(padx=int(20 * position_factor_x), pady=int(10 * position_factor_y))
    
    btn_rules = Button(frame1, image=rules_picture, command=lancefen2)
    btn_rules.pack(pady=int(10 * position_factor_y))
    
    btn_menu1 = Button(mon_jeu, image=menu_picture, command=switch)
    btn_menu1.place(x=int(screen_width - 105 * position_factor_x), y=0)
    
    btn_menu2 = Button(b, image=menu_picture, command=switch2)
    btn_menu2.place(x=int(screen_width - 105 * position_factor_x), y=0)
    
    # Boutons son
    frame = Frame(a)
    frame.pack(side=LEFT, padx=int(10 * position_factor_x))
    
    btn_play1 = Button(frame, image=ser, command=play1)
    btn_play1.config(width=button_size, height=button_size)
    btn_play1.pack(pady=int(5 * position_factor_y))
    
    btn_play2 = Button(frame, image=gry, command=play2)
    btn_play2.config(width=button_size, height=button_size)
    btn_play2.pack(pady=int(5 * position_factor_y))
    
    btn_play3 = Button(frame, image=pou, command=play3)
    btn_play3.config(width=button_size, height=button_size)
    btn_play3.pack(pady=int(5 * position_factor_y))
    
    btn_play4 = Button(frame, image=serp, command=play4)
    btn_play4.config(width=button_size, height=button_size)
    btn_play4.pack(pady=int(5 * position_factor_y))
    
    frame3 = Frame(a)
    frame3.pack(side=LEFT, padx=int(5 * position_factor_x))
    
    btn_stop1 = Button(frame3, image=arr, command=stop1)
    btn_stop1.config(width=button_size, height=button_size)
    btn_stop1.pack(pady=int(5 * position_factor_y))
    
    btn_stop2 = Button(frame3, image=arr, command=stop2)
    btn_stop2.config(width=button_size, height=button_size)
    btn_stop2.pack(pady=int(5 * position_factor_y))
    
    btn_stop3 = Button(frame3, image=arr, command=stop3)
    btn_stop3.config(width=button_size, height=button_size)
    btn_stop3.pack(pady=int(5 * position_factor_y))
    
    btn_stop4 = Button(frame3, image=arr, command=stop4)
    btn_stop4.config(width=button_size, height=button_size)
    btn_stop4.pack(pady=int(5 * position_factor_y))
    
    # Lancer la boucle principale
    mon_jeu.mainloop()
    a.mainloop()
    b.mainloop()