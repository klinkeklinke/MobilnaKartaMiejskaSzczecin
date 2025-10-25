# Mobilna Karta Miejska Szczecin
## Projekt aplikacji smart city

**Wersja:** 1.0 | **Data:** 2025-10-25

---

## 🧭 Kontekst i cel projektu

### Wizja
Miasto Szczecin chce stworzyć **nowoczesną, przyjazną użytkownikowi aplikację mobilną**, która zintegruje transport publiczny, płatności miejskie, parkingi, wydarzenia i turystykę w jednym miejscu.

### Misja
Celem projektu jest **uproszczenie poruszania się po mieście** i **cyfryzacja miejskich usług** w duchu idei smart city, wspierając Szczecin jako **lidera 15-minute city w Polsce**.

---

## 🎯 Kluczowe problemy do rozwiązania

| Problem | Konsekwencje | Rozwiązanie w aplikacji |
|---------|--------------|-------------------------|
| **Rozproszenie usług** | Osobne systemy do biletów, parkingów, eventów, map | Jeden ekosystem cyfrowy |
| **Trudność w zakupie biletu** | Turyści (2,2 mln/rok) nie wiedzą jak kupić bilet | Guest checkout <30 sekund |
| **Brak integracji** | Transport, wydarzenia i informacje miejskie działają oddzielnie | API-first architecture |
| **Niewykorzystany potencjał** | Dane lokalizacyjne nie służą promocji usług | Geo-targeting i smart notifications |

---

## 🌟 Szczecin jako 15-Minute City

### Osiągnięcia
- 🏆 **#1 w Polsce** - 40,6% mieszkańców ma potrzeby codzienne w zasięgu 15 minut
- 🥈 **#2 w Europie Środkowo-Wschodniej** (Friendly City Index 2025)
- 📊 **Dla porównania:** Kraków 30,3%, Wrocław 26,8%, Warszawa 15,8%

### Co to oznacza dla aplikacji?
- **Transport publiczny jest kluczowy** - integracja z ZDiTM to must-have
- **Walkability** - promujemy opcje pieszo i rowerem, nie tylko autem
- **Lokalne usługi** - pokazujemy co jest blisko użytkownika
- **Smart routing** - multimodalne planowanie tras (pieszo + tram + bike)

**Źródła:**
- [SSOM - Szczecin liderem w Polsce](https://som.szczecin.pl/2025/09/23/szczecin-liderem-w-polsce-w-dazeniu-do-miasta-15-minutowego/)
- [TVP World - Poland's Szczecin closest to ideal of 15-minute city](https://tvpworld.com/89074562/polands-szczecin-closest-to-ideal-of-15-minute-city)

---

## 🎁 Value Proposition

### Jedno cyfrowe narzędzie miejskie, które:

✅ **Ułatwia mieszkańcom codzienne funkcjonowanie**
- Zakup biletów bez kolejek
- Real-time informacje o opóźnieniach
- Personalizowane powiadomienia o zmianach w trasach

✅ **Pozwala turystom szybko kupić bilet i zaplanować trasę**
- Guest checkout (bez rejestracji)
- Międzynarodowe metody płatności (PayPal, Apple Pay, Google Pay)
- Interfejs w 3 językach: PL, DE, EN

✅ **Wspiera miasto w zarządzaniu mobilnością i promocją**
- Dashboard analytics dla ZDiTM (load balancing, hot spots)
- Targetowanie komunikatów miejskich
- Promocja wydarzeń kulturalnych (Filharmonia, Teatry, Sail Szczecin)

---

## 📊 Target Audience - dane faktyczne

### Turyści (2,2 mln rocznie w 2024)
- **82% z Polski** (głównie: dolnośląskie, śląskie, wielkopolskie)
- **900k z Niemiec** (61% wszystkich zagranicznych)
- **City break travelers** - pobyty krótkie, potrzebują szybkiej orientacji
- **Wielkie wydarzenia:** Sail Szczecin (390k w weekend!), The Tall Ships Races

### Mieszkańcy
- **40,6% ma usługi w zasięgu 15 minut** (#1 w Polsce!)
- Regularne korzystanie z transportu publicznego
- Potrzeba integracji z Kartą Mieszkańca (zniżki, benefity)

**Źródła:**
- [Głos Szczeciński - 2,2 mln turystów w 2024](https://gs24.pl/od-poczatku-roku-szczecin-odwiedzilo-ponad-2-miliony-turystow-najwiecej-na-final-regat-the-tall-ships-races/ar/c1-18929345)
- [Visit Szczecin - Tourism Statistics](https://visitszczecin.eu/en/news/874-more-and-more-tourists-visit-szczecin)

---

## 👥 Persony użytkowników

### Persona 1: **Ania - Mieszkanka Szczecina** 👩‍💼
**Wiek:** 32 lata | **Zawód:** Marketing Manager | **Mieszka:** Niebuszewo

**Potrzeby:**
- Szybki zakup biletu w drodze do pracy (tramwaj linia 3)
- Powiadomienia o opóźnieniach ZANIM wyjdzie z domu
- Integracja z parkingami P&R (jeździ autem + komunikacja)
- Karta Mieszkańca ze zniżkami do Filharmonii

**Pain points:**
- Osobne aplikacje do biletów, parkingów, wydarzeń
- Nie wie o opóźnieniach dopóki nie stoi na przystanku

**User journey:**
1. Rano sprawdza aplikację → widzi 5 min opóźnienia na linii 3
2. Wychodzi 5 min później z domu (oszczędza czas!)
3. Kupuje bilet miesięczny w 3 kliknięcia
4. Dostaje powiadomienie o koncercie w Filharmonii (geo-targeted)
5. Kupuje bilet ze zniżką Karty Mieszkańca

---

### Persona 2: **Hans - Turysta z Berlina** 🇩🇪
**Wiek:** 45 lat | **Zawód:** Architekt | **Wizyta:** City break weekend

**Potrzeby:**
- Kupić bilet komunikacji **BEZ rejestracji** (nie zna polskiego)
- Płatność PayPal/Apple Pay (nie ma polskiej karty)
- Odkryć Szczecin (Filharmonia, Wały Chrobrego, Arkonka)
- Prosty routing: z hotelu → Stare Miasto → Arkonka

**Pain points:**
- Nie wie jak kupić bilet (automaty po polsku, nie przyjmują kart zagranicznych)
- Google Maps nie pokazuje real-time transportu Szczecina
- Nie wie co warto zobaczyć

**User journey:**
1. Ląduje w Szczecinie → otwiera aplikację
2. Wybiera "Guest / Tourist" mode (interfejs EN/DE)
3. Kupuje bilet 24h w <30 sekund (Apple Pay)
4. Widzi na mapie: Filharmonię, Arkonkę, Teatr Współczesny
5. Klika "Kup bilet" → kupuje wstęp do Arkonki
6. Routing multimodalny: hotel → pieszo 5 min → tram 12 → Arkonka

---

### Persona 3: **Kasia - Studentka (19 lat)** 🎓
**Uczelnia:** Uniwersytet Szczeciński | **Mieszka:** Akademik Gumieńce

**Potrzeby:**
- Bilety ulgowe
- Powiadomienia o zmianach tras do uczelni
- Integracja z eventami studenckimi (koncerty, kino)
- Tracking budżetu na transport

**Pain points:**
- Zapomina kupić bilet → mandat
- Nie wie o zmianach w kursach (remonty)

**User journey:**
1. Ustawia alert: "Powiadom mnie o zmianach na linii 60"
2. Dostaje push: "Linia 60 objazd 15-20.10"
3. Kupuje bilet miesięczny ulgowy
4. Aplikacja pokazuje: "Wydałaś 100 zł na transport w tym miesiącu"
5. Dostaje ofertę: "Kup karnet Fabryka Wody -20% dla studentów"

🧩 Kluczowe moduły i priorytety
🏆 Priorytetowe (MVP)

Sprzedaż biletów – prosty, intuicyjny zakup, także bez konta, z potwierdzeniem QR.

Trasowanie i planowanie podróży – dynamiczne trasy (GPS, mapa, multi-modalność).

Targetowanie lokalizacyjne – inteligentne rekomendacje biletów i wydarzeń w okolicy.

Powiadomienia miejskie – utrudnienia, komunikaty, alerty.

Płatności zintegrowane – Swish, Klarna, PayPal, Apple Pay, Google Pay, karty.

🚀 Dodatkowe (faza 2)

Mapa miejska z usługami i atrakcjami,

Karta mieszkańca ze zniżkami i benefitami,

Turystyka i przewodnik,

Zielona mobilność (rowery, hulajnogi, EV).

💡 Styl wizualny i UX/UI

Kolory Szczecina: granat #0A2740, błękit #00AEEF, złoto akcentowe, biel.

Typografia nowoczesna, czytelna (Inter lub Poppins).

Styl: smart city, eco, lekki, intuicyjny, dostępny (WCAG).

Layout modułowy – mapa + skrót funkcji.

Onboarding z wyborem: „Mieszkaniec / Turysta”.

Mikrointerakcje przy kliknięciach i transakcjach.

🧮 Cele biznesowe / funkcjonalne

Skrócić czas zakupu biletu (turysta) do 30 sekund.

Zwiększyć konwersję guest checkout > 80 %.

Zwiększyć udział płatności mobilnych o 20 % w 6 miesięcy.

Zapewnić zgodność z PSD2/SCA i RODO.

🧠 Dla Figma Make — instrukcje

Na podstawie opisu stwórz spójną strukturę interfejsu,

Samodzielnie zaproponuj zestaw ekranów i interakcji odpowiadających tym celom,

Zachowaj spójność stylistyczną i czytelność UX dla dwóch grup użytkowników (mieszkaniec i turysta),

Zwróć uwagę na flow płatności, trasowania i targetowania lokalizacyjnego,

Uwzględnij możliwość późniejszej integracji z design tokens i React / TypeScript.
