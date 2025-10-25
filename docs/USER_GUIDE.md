# User Guide
## Interaktywna Mapa Real-Time Szczecin

### Wersja: 1.0
**Data aktualizacji:** 2025-10-25

---

## Spis treści

1. [Wprowadzenie](#1-wprowadzenie)
2. [Wymagania systemowe](#2-wymagania-systemowe)
3. [Instalacja](#3-instalacja)
4. [Uruchomienie](#4-uruchomienie)
5. [Funkcje aplikacji](#5-funkcje-aplikacji)
6. [FAQ](#6-faq)
7. [Troubleshooting](#7-troubleshooting)
8. [Wsparcie](#8-wsparcie)

---

## 1. Wprowadzenie

### Co to jest?

**Szczecin Live Map** to interaktywna demonstracja technologiczna pokazująca możliwości wizualizacji danych transportu publicznego w czasie rzeczywistym.

### Co pokazuje aplikacja?

- 🚌 **Live tracking** pojazdów komunikacji miejskiej (autobusy, tramwaje)
- ⚠️ **Opóźnienia** w transporcie publicznym (pulsujące czerwone ikony)
- 🅿️ **Dostępność parkingów** Park & Ride (mock data)
- 🏊 **Punkty POI** - baseny, teatry, filharmonia (możliwość "zakupu biletu")

### Dla kogo?

- 👨‍💼 **Stakeholderzy** - demonstracja możliwości technologii
- 👨‍💻 **Deweloperzy** - proof of concept integracji API ZDiTM
- 🏛️ **Miasto Szczecin** - wizja smart city solutions

---

## 2. Wymagania systemowe

### System operacyjny
- ✅ **macOS** 10.15+
- ✅ **Windows** 10+
- ✅ **Linux** (Ubuntu 20.04+, Debian, Fedora)

### Python
- **Wymagana wersja:** Python 3.9 lub nowsza
- **Sprawdzenie wersji:**
  ```bash
  python --version
  # lub
  python3 --version
  ```

### Połączenie internetowe
- **Wymagane:** Tak (do pobrania danych z API ZDiTM)
- **Minimalna prędkość:** 1 Mbps (zalecane: 5+ Mbps)

### Przeglądarka (dla Streamlit)
- ✅ **Chrome** 90+
- ✅ **Firefox** 88+
- ✅ **Safari** 14+
- ✅ **Edge** 90+

---

## 3. Instalacja

### Krok 1: Sklonuj repozytorium

```bash
git clone https://github.com/[username]/MobilnaKartaMiejskaSzczecin.git
cd MobilnaKartaMiejskaSzczecin
```

### Krok 2: Utwórz wirtualne środowisko (zalecane)

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**Potwierdzenie:** Powinieneś zobaczyć `(venv)` przed promptem w terminalu.

### Krok 3: Zainstaluj zależności

```bash
pip install -r requirements.txt
```

**Spodziewane pakiety:**
- `streamlit` - framework aplikacji
- `folium` - mapy interaktywne
- `streamlit-folium` - integracja Folium z Streamlit
- `requests` - komunikacja z API
- `pandas` - (opcjonalnie) przetwarzanie danych

### Krok 4: Weryfikacja instalacji

```bash
streamlit --version
```

**Oczekiwany output:**
```
Streamlit, version 1.XX.X
```

---

## 4. Uruchomienie

### Metoda podstawowa

```bash
streamlit run app.py
```

### Co się stanie?

1. **Terminal pokaże:**
   ```
   You can now view your Streamlit app in your browser.

   Local URL: http://localhost:8501
   Network URL: http://192.168.1.X:8501
   ```

2. **Przeglądarka otworzy się automatycznie** na `http://localhost:8501`

3. **Ładowanie może potrwać 5-10 sekund** (pierwsze uruchomienie)

### Zatrzymanie aplikacji

- **Naciśnij:** `Ctrl + C` w terminalu
- **Lub:** Zamknij terminal

---

## 5. Funkcje aplikacji

### 5.1 Interfejs główny

```
┌─────────────────────────────────────────────────────┐
│  🗺️ SZCZECIN LIVE MAP          Last update: 20:06  │
├──────────┬──────────────────────────────────────────┤
│ SIDEBAR  │                                          │
│          │                                          │
│ WARSTWY: │               MAPA                       │
│ ☑ Transport                                         │
│ ☑ Parkingi│          (interaktywna)                 │
│ ☑ POI     │                                          │
│          │                                          │
│ ────────│                                          │
│ Odświeżanie:                                        │
│  ▢▢▢▬▢ 15s│                                          │
│          │                                          │
│ ────────│                                          │
│ STATUS:  │                                          │
│ 🟢 Live  │                                          │
└──────────┴──────────────────────────────────────────┘
```

### 5.2 Sidebar - Kontrolki

#### A. Toggle warstw

**☑ Transport publiczny**
- **Włączone:** Pokazuje autobusy i tramwaje na mapie
- **Wyłączone:** Ukrywa pojazdy

**☑ Parkingi P&R**
- **Włączone:** Pokazuje parkingi Park & Ride z obłożeniem
- **Wyłączone:** Ukrywa parkingi

**☑ POI (Points of Interest)**
- **Włączone:** Pokazuje baseny, teatry, filharmonię
- **Wyłączone:** Ukrywa POI

#### B. Slider odświeżania

```
Odświeżanie (sekundy):
|────▬─────────| 15s
10            60
```

- **Zakres:** 10-60 sekund
- **Domyślnie:** 15 sekund
- **Zalecane:** 15-20s (optymalny balans fresh data vs. rate limits)

#### C. Status indicator

- **🟢 Live** - Połączenie OK, dane aktualne
- **🟡 Cached** - Używam ostatnich zapisanych danych
- **🔴 Error** - Problem z API, sprawdź połączenie

### 5.3 Mapa - Legenda ikon

#### Transport publiczny

| Ikona | Opis | Tooltip |
|-------|------|---------|
| 🚌 niebieski | Autobus **bez opóźnienia** | Klik → linia, kierunek, prędkość |
| 🚌 czerwony (pulsujący) | Autobus **opóźniony** | Klik → **opóźnienie w minutach** |
| 🚊 niebieski | Tramwaj **bez opóźnienia** | Klik → linia, kierunek, prędkość |
| 🚊 czerwony (pulsujący) | Tramwaj **opóźniony** | Klik → **opóźnienie w minutach** |

**Przykład tooltip:**
```
Linia 75
Kierunek: Osiedle Zawadzkiego
⚠️ Opóźnienie: 2 min
Prędkość: 15 km/h
```

#### Parkingi P&R

| Kolor | Obłożenie | Przykład |
|-------|-----------|----------|
| 🟢 Zielony | 0-50% | "45/150 zajętych (30%)" |
| 🟡 Żółty | 50-80% | "120/200 zajętych (60%)" |
| 🔴 Czerwony | 80-100% | "165/200 zajętych (82%)" |

**Klik na marker** → tooltip z dokładnymi liczbami

#### POI (Points of Interest)

| Ikona | Kategoria | Lokalizacje |
|-------|-----------|-------------|
| 🏊 Niebieski | Aquapark/Basen | Arkonka, Fabryka Wody |
| 🎭 Fioletowy | Kultura | Filharmonia, Teatr Współczesny |
| 🏛️ Brązowy | Dziedzictwo | Cmentarz Centralny |

**Klik na marker** → Popup z:
- Nazwa obiektu
- Krótki opis
- Adres
- **Przycisk "🎫 Kup bilet"** (otwiera stronę zewnętrzną)

### 5.4 Nawigacja po mapie

#### Przybliżanie/oddalanie
- **Scroll myszy** - zoom in/out
- **Przyciski +/-** (lewy górny róg mapy)
- **Double-click** - przybliż do punktu

#### Przesuwanie
- **Przeciągnij myszą** (drag)
- **Strzałki na klawiaturze** (jeśli obsługiwane)

#### Reset widoku
- **Odśwież stronę** (`F5`) - wraca do centrum Szczecina

---

## 6. FAQ

### Q: Jak często aktualizują się dane?

**A:** Dane z API ZDiTM odświeżają się co ~10 sekund. Aplikacja pobiera je zgodnie z ustawionym interwałem (domyślnie 15s).

---

### Q: Dlaczego tramwaje "skaczą" zamiast płynnie jechać?

**A:** To wersja demonstracyjna z "basic animation". Aplikacja odświeża całą mapę co X sekund, co powoduje "skok" pozycji. Smooth animation będzie w wersji 2.0.

---

### Q: Czy dane parkingów są prawdziwe?

**A:** **NIE.** ZDiTM nie udostępnia publicznego API dla danych parkingowych. Obecnie używamy **mock data** (symulowanych danych). Struktura jest gotowa do podmiany na prawdziwe API w przyszłości.

---

### Q: Jak kupić bilet w aplikacji?

**A:** Aktualnie **"Kup bilet" to mockup** - kliknięcie otwiera oficjalną stronę obiektu (np. Filharmonia, Arkonka). To proof of concept - w pełnej wersji byłaby integracja z systemem sprzedaży.

---

### Q: Aplikacja pokazuje "Cached data" - co to znaczy?

**A:** API ZDiTM jest tymczasowo niedostępne lub przekroczono limit requestów. Aplikacja używa ostatnich zapisanych danych (max. 30s starych).

---

### Q: Mapa się nie ładuje / błąd połączenia

**A:** Sprawdź:
1. ✅ Połączenie internetowe
2. ✅ Czy API ZDiTM działa: https://www.zditm.szczecin.pl/api/v1/vehicles
3. ✅ Firewall nie blokuje Streamlit (port 8501)

---

### Q: Jak zmienić centrum mapy (np. na inną dzielnicę)?

**A:** Obecnie centrum jest fixed na `[53.4285, 14.5528]` (centrum Szczecina). Możesz:
- Przesunąć mapę ręcznie
- **Lub:** Zmodyfikuj `SZCZECIN_CENTER` w `utils/map_builder.py`

---

### Q: Czy mogę hostować to publicznie?

**A:** Tak! Opcje:
- **Streamlit Cloud** (darmowe) - push na GitHub + deploy
- **Docker** - patrz `IMPLEMENTATION.md` sekcja 9
- **Heroku/AWS/GCP** - wymaga dodatkowej konfiguracji

⚠️ **Uwaga:** Sprawdź Terms of Service API ZDiTM przed publicznym deploymentem.

---

## 7. Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'streamlit'`

**Rozwiązanie:**
```bash
# Sprawdź czy venv jest aktywny
which python  # macOS/Linux
where python  # Windows

# Jeśli nie pokazuje ścieżki z venv/, aktywuj:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Zainstaluj zależności ponownie:
pip install -r requirements.txt
```

---

### Problem: Aplikacja ładuje się wiecznie

**Możliwe przyczyny:**
1. **Brak połączenia z API ZDiTM**
   - Sprawdź: https://www.zditm.szczecin.pl/api/v1/vehicles
   - Rozwiązanie: Aplikacja powinna pokazać cached data po timeout

2. **Firewall blokuje request**
   - Windows: Dodaj wyjątek dla Python/Streamlit
   - macOS: Sprawdź Security & Privacy settings

3. **Wolne połączenie internetowe**
   - Zwiększ timeout w `utils/zditm_api.py` (domyślnie 10s)

---

### Problem: `Address already in use` (port 8501)

**Rozwiązanie:**

**macOS/Linux:**
```bash
# Znajdź proces na porcie 8501
lsof -i :8501

# Kill procesu (zastąp PID numerem z powyższego)
kill -9 PID
```

**Windows:**
```bash
# Znajdź proces
netstat -ano | findstr :8501

# Kill procesu (zastąp PID numerem)
taskkill /PID <PID> /F
```

**Lub uruchom na innym porcie:**
```bash
streamlit run app.py --server.port 8502
```

---

### Problem: Mapa pokazuje tylko szarą siatkę

**Przyczyna:** Brak połączenia z OpenStreetMap tile servers

**Rozwiązanie:**
1. Sprawdź połączenie internetowe
2. Sprawdź czy firewall nie blokuje tile.openstreetmap.org
3. Spróbuj innego tile providera (edytuj `map_builder.py`):
   ```python
   tiles="CartoDB positron"  # zamiast "OpenStreetMap"
   ```

---

### Problem: `JSONDecodeError` w konsoli

**Przyczyna:** API ZDiTM zwróciło nieprawidłowy JSON (rzadkie)

**Rozwiązanie:**
- Zazwyczaj rozwiązuje się automatycznie (retry logic)
- Jeśli powtarza się: sprawdź status API na stronie ZDiTM
- Check if API changed format: https://www.zditm.szczecin.pl/en/zditm/for-developers

---

### Problem: Brak ikon FontAwesome (puste kwadraty)

**Rozwiązanie:**
```bash
# Zainstaluj/update folium
pip install --upgrade folium streamlit-folium
```

---

## 8. Wsparcie

### Dokumentacja techniczna

- **TECH_SPEC.md** - szczegóły API, struktura danych
- **IMPLEMENTATION.md** - architektura, wybór technologii

### API ZDiTM

- **Dokumentacja:** https://www.zditm.szczecin.pl/en/zditm/for-developers
- **Status API:** https://www.zditm.szczecin.pl/api/v1/vehicles (sprawdź w przeglądarce)

### Streamlit

- **Docs:** https://docs.streamlit.io
- **Forum:** https://discuss.streamlit.io
- **GitHub:** https://github.com/streamlit/streamlit

### Folium

- **Docs:** https://python-visualization.github.io/folium/
- **Examples:** https://nbviewer.org/github/python-visualization/folium/tree/main/examples/

### Zgłaszanie błędów

**GitHub Issues:** (link do repo)

**Template zgłoszenia:**
```markdown
**Describe the bug:**
Krótki opis problemu

**To Reproduce:**
1. Uruchomiam aplikację
2. Klikam na...
3. Widzę błąd...

**Expected behavior:**
Co powinno się stać

**Screenshots:**
Jeśli dotyczy

**Environment:**
- OS: [macOS 14.0 / Windows 11 / Ubuntu 22.04]
- Python version: 3.9.6
- Streamlit version: 1.XX.X

**Console output:**
```
Paste error message here
```
```

---

## Appendix A: Skróty klawiszowe

| Akcja | Skrót |
|-------|-------|
| Odśwież stronę | `F5` lub `Cmd+R` (Mac) / `Ctrl+R` (Win) |
| Zoom in (mapa) | `+` lub scroll up |
| Zoom out (mapa) | `-` lub scroll down |
| Pełny ekran przeglądarki | `F11` |
| Otwórz DevTools (debug) | `F12` lub `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Win) |

---

## Appendix B: Komendy szybkiego startu

```bash
# Clone + setup + run (all-in-one)
git clone https://github.com/[username]/MobilnaKartaMiejskaSzczecin.git && \
cd MobilnaKartaMiejskaSzczecin && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
streamlit run app.py
```

---

**Ostatnia aktualizacja:** 2025-10-25
**Wersja dokumentu:** 1.0
**Status:** ✅ READY FOR USERS

**Enjoy exploring Szczecin in real-time! 🗺️🚊**
