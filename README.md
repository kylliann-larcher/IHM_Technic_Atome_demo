
# IHM Technic Atome - Dashboard Multi-Données

Ce projet est une application Python complète avec interface graphique (Tkinter), permettant de :
- Charger plusieurs fichiers CSV contenant des données techniques (ex : chaufferies nucléaires)
- Visualiser, comparer, trier et enrichir les données
- Générer des statistiques avancées
- Comparer plusieurs fichiers sur les colonnes communes

---

## 📦 Fonctionnalités principales

- ✅ Chargement de plusieurs fichiers CSV avec choix de séparateur
- ✅ Ajout dynamique de nouveaux fichiers via bouton
- ✅ Sélecteur pour basculer entre les fichiers
- ✅ Affichage de tableau interactif avec tri par colonne
- ✅ Ajout manuel de données ligne par ligne
- ✅ Visualisation avancée avec :
  - Barres
  - Lignes
  - Nuages de points
  - Camemberts
  - Tooltips interactifs (valeurs exactes)
- ✅ Statistiques avancées :
  - Moyennes
  - Médianes (boxplot)
  - Écart-type
  - Données manquantes (heatmap)
  - Histogrammes globaux
- ✅ Comparaison multi-fichiers :
  - Moyennes
  - Écart-types
  - Distributions KDE
  - Boxplots sur colonne commune
  - Valeurs manquantes
- ✅ Architecture modulaire (data/ui)
- ✅ Possibilité d’ajouter d’autres vues, filtres, exports

---

## 🛠️ Démarrage

Lancer l’application avec :

```bash
python main.py
```

Prérequis :
```bash
pip install pandas matplotlib seaborn mplcursors
```

---

## 🧠 Philosophie de développement

- Interface simple et inspirée des outils type Power BI
- Composants modulaires (chaque fenêtre dans son fichier)
- Extensible : nouvelles vues, filtres, export possible
- Optimisé pour des utilisateurs métier (techniciens, ingénieurs)

---

## 🔄 Étapes de développement

1. Conception d'une structure modulaire
2. Développement de l’interface de chargement CSV
3. Ajout du tri, de l’édition, et du tableau
4. Création de la visualisation avancée dynamique
5. Intégration des statistiques visuelles
6. Ajout d’un comparateur de fichiers multi-vues
7. Amélioration de l’interactivité (tooltips, switch dynamique)
8. Nettoyage de code et amélioration UX

---

## 📁 Arborescence

```
IHM_Technic_Atome_demo/
│
├── main.py
├── data/
│   └── data_loader.py
├── ui/
│   ├── gui.py
│   ├── visualizer_window.py
│   ├── statistics_window.py
│   └── comparator_window.py
└── assets/ (fichiers CSV à charger)
```

---

## 🚀 Possibilités d’amélioration

- Export PDF / Excel
- Filtres dynamiques par colonne
- Suppression de fichiers
- Interface moderne (dark mode)
- Sauvegarde / rechargement de vues personnalisées
