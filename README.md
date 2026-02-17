# Backend Monely - Django REST API

Backend de l'application Monely

 construit avec Django REST Framework et Supabase PostgreSQL.

## 🚀 Installation Rapide

```bash
# 1. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos identifiants Supabase

# 4. Lancer les migrations
python manage.py makemigrations
python manage.py migrate

# 5. Créer un superuser
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

## 📦 Structure du Projet

```
server/
├── config/                 # Configuration Django
│   ├── settings.py        # Settings (Supabase, DRF, JWT, CORS)
│   ├── urls.py            # Routes principales
│   └── wsgi.py            # WSGI app
├── authentication/         # App authentification
│   ├── models.py          # User personnalisé
│   ├── serializers.py     # UserSerializer, RegistrationSerializer
│   └── admin.py           # Admin config
├── transactions/           # App transactions
│   ├── models.py          # Transaction
│   ├── serializers.py     # TransactionSerializer
│   └── admin.py           # Admin config
├── wallets/               # App portefeuilles
│   ├── models.py          # Wallet, SavingGoal
│   ├── serializers.py     # WalletSerializer, SavingGoalSerializer
│   └── admin.py           # Admin config
├── analytics/             # App analytiques
│   └── (À implémenter)
├── ai_insights/           # App Gemini AI
│   └── (À implémenter)
├── requirements.txt
├── .env.example
├── .gitignore
└── manage.py
```

## 🛠️ Stack Technique

- **Django** 5.0.14
- **Django REST Framework** 3.16.1
- **PostgreSQL** (via Supabase)
- **JWT** (djangorestframework-simplejwt)
- **Gemini AI** (google-generativeai)

## 📊 Modèles de Données

### User (Custom)
- email, name, username
- avatar_url, currency, language
- dates: created_at, updated_at

### Transaction
- wallet (FK), user (FK)
- name, amount, category
- type (income/expense), status (pending/completed)
- date, icon
- **Auto-update wallet balance**

### Wallet
- user (FK)
- name, type (checking/savings/credit)
- balance, currency
- color, icon

### SavingGoal
- user (FK)
- name, target_amount, current_amount
- deadline, color
- **Property**: progress_percentage

## 🔌 API Endpoints (Planifiés)

### Authentication
```
POST   /api/auth/register/      # S'inscrire
POST   /api/auth/login/         # Se connecter (JWT)
POST   /api/auth/refresh/       # Rafraîchir token
POST   /api/auth/logout/        # Se déconnecter
GET    /api/auth/me/            # Profil actuel
```

### Transactions
```
GET    /api/transactions/       # Liste (paginée)
POST   /api/transactions/       # Créer
GET    /api/transactions/{id}/  # Détail
PUT    /api/transactions/{id}/  # Modifier
DELETE /api/transactions/{id}/  # Supprimer
```

### Wallets
```
GET    /api/wallets/            # Liste
POST   /api/wallets/            # Créer
GET    /api/wallets/{id}/       # Détail
PUT    /api/wallets/{id}/       # Modifier
DELETE /api/wallets/{id}/       # Supprimer
GET    /api/wallets/{id}/balance/  # Solde actuel
```

### Saving Goals
```
GET    /api/saving-goals/       # Liste
POST   /api/saving-goals/       # Créer
GET    /api/saving-goals/{id}/  # Détail
PUT    /api/saving-goals/{id}/  # Modifier
DELETE /api/saving-goals/{id}/  # Supprimer
```

### Analytics
```
GET    /api/analytics/dashboard/   # Données dashboard
GET    /api/analytics/trends/      # Tendances mensuelles
GET    /api/analytics/categories/  # Répartition catégories
```

### AI Insights
```
POST   /api/ai/insights/        # Générer insights
POST   /api/ai/predictions/     # Prédictions
```

## ⚙️ Configuration

### Variables d'Environnement (.env)

```env
# Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase Database
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your_password
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432

# Gemini AI
GEMINI_API_KEY=your_api_key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## 🧪 Commandes Utiles

```bash
# Développement
python manage.py runserver        # Serveur dev

# Base de données
python manage.py makemigrations   # Créer migrations
python manage.py migrate          # Appliquer migrations
python manage.py showmigrations   # Voir statut migrations

# Shell Django
python manage.py shell            # REPL Python

# Admin
python manage.py createsuperuser  # Créer admin

# Tests
python manage.py test             # Lancer tests
```

## 📝 Statut d'Implémentation

### ✅ Fait
- [x] Structure du projet Django
- [x] Configuration Supabase PostgreSQL
- [x] Modèles de données (User, Transaction, Wallet, SavingGoal)
- [x] Serializers DRF
- [x] Configuration REST Framework
- [x] Configuration JWT
- [x] Configuration CORS
- [x] Admin Django configuré

### 🔜 À Faire
- [ ] ViewSets et API endpoints
- [ ] URLs routing
- [ ] Permissions personnalisées
- [ ] Service Analytics
- [ ] Intégration Gemini AI
- [ ] Tests unitaires
- [ ] Documentation API (Swagger)

## 🤝 Contribution

1. Créer une branche
2. Faire les modifications
3. Lancer les tests
4. Créer une PR

## 📄 Licence

MIT
# Monely-back
