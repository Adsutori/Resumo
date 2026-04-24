# ![Resumo](static/media/logo/favicon.ico) Resumo

> Nowoczesny kreator CV w stylu SaaS — twórz, edytuj i pobieraj profesjonalne CV w kilka minut.

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue?style=flat-square&logo=postgresql)
![Status](https://img.shields.io/badge/Status-W%20budowie-orange?style=flat-square)

---

## ✨ Funkcje

- 🔐 **Rejestracja i logowanie** — weryfikacja e-mail, "zapamiętaj mnie", reset hasła
- 📝 **Kreator CV** — intuicyjny edytor krok po kroku
- 🎨 **3 szablony** — Klasyczny, Minimalistyczny, Nowoczesny
- 📥 **Eksport PDF** — pobierz gotowe CV jednym kliknięciem
- 🔗 **Udostępnianie** — publiczny link do CV
- 📊 **Dashboard** — zarządzaj wszystkimi swoimi dokumentami
- 🤖 **Analiza AI** *(wkrótce)* — ocena i sugestie poprawy CV
- 💼 **Śledzenie aplikacji** *(wkrótce)* — monitoruj swoje aplikacje o pracę

---

## 🛠️ Tech Stack

| Warstwa | Technologia |
|---|---|
| Backend | Django 6.0, Python 3.14 |
| Baza danych | PostgreSQL (Neon) |
| Frontend | HTML5, CSS3 (BEM), Vanilla JS |
| Ikony | Lucide Icons |
| Fonty | Inter (Google Fonts) |
| Harmonogram zadań | APScheduler |
| Generowanie PDF | WeasyPrint |
| Hosting DB | Neon (serverless PostgreSQL) |

---

## 🚀 Uruchomienie lokalne

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/twoj-nick/resumo.git
cd resumo
```

### 2. Środowisko wirtualne

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Instalacja zależności

```bash
pip install -r requirements.txt
```

### 4. Plik `.env`

Utwórz plik `.env` w folderze głównym projektu:

```env
SECRET_KEY=twoj-tajny-klucz-django

# Baza danych (PostgreSQL / Neon)
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=twoje-haslo
DB_HOST=twoj-host.neon.tech
DB_PORT=5432

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=twoj@email.com
EMAIL_HOST_PASSWORD=twoje-haslo-aplikacji
```

### 5. Migracje

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Uruchomienie serwera

```bash
python manage.py runserver
```

Aplikacja dostępna pod adresem: **http://127.0.0.1:8000**

---

## 📁 Struktura projektu

```
Resumo/
├── Resumo/                  # Główna konfiguracja Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── Users/                   # Moduł autentykacji
│   ├── models.py            # CustomUser
│   ├── views.py             # login, register, verify, logout
│   ├── forms.py             # RegisterForm, LoginForm
│   ├── urls.py
│   ├── templates/
│   │   └── users/
│   │       ├── login.html
│   │       ├── register.html
│   │       └── verify.html
│   └── management/
│       └── commands/
│           └── delete_unverified_users.py
│
├── Dashboard/               # Moduł dashboardu i CV
│   ├── models.py            # CV, Template
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── dashboard-layout.html
│       └── dashboard/
│           └── dashboard.html
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/               # Globalne szablony
│   └── landing/
│
├── .env                     # ⚠️ Nie commitować!
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 🗺️ Roadmapa

### ✅ Gotowe
- [x] System rejestracji z weryfikacją e-mail
- [x] Logowanie z opcją "zapamiętaj mnie"
- [x] Automatyczne usuwanie niezweryfikowanych kont (15 min)
- [x] Layout dashboardu (sidebar, topbar, responsywność)
- [x] UI dashboardu (szybkie akcje, karty CV, szablony, statystyki)

### 🔧 W trakcie
- [ ] Model CV i dynamiczne dane w dashboardzie
- [ ] Kreator / edytor CV
- [ ] Generowanie PDF

### 📅 Planowane
- [ ] Udostępnianie CV przez publiczny link
- [ ] Ustawienia konta (avatar, zmiana hasła)
- [ ] Powiadomienia
- [ ] Analiza CV przez AI (OpenAI API)
- [ ] Śledzenie aplikacji o pracę
- [ ] Import danych z LinkedIn

---

## 🔐 Zmienne środowiskowe

| Zmienna | Opis | Wymagana |
|---|---|---|
| `SECRET_KEY` | Klucz Django | ✅ |
| `DB_NAME` | Nazwa bazy danych | ✅ |
| `DB_USER` | Użytkownik bazy | ✅ |
| `DB_PASSWORD` | Hasło do bazy | ✅ |
| `DB_HOST` | Host bazy danych | ✅ |
| `EMAIL_HOST_USER` | Adres e-mail do wysyłki | ✅ |
| `EMAIL_HOST_PASSWORD` | Hasło aplikacji Gmail | ✅ |

---

## 📝 Licencja

Ten projekt jest objęty licencją **MIT** — szczegóły w pliku [LICENSE](LICENSE).

---

<p align="center">
  Zbudowane z ❤️ przy użyciu Django
</p>