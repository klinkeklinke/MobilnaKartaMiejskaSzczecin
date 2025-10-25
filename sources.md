# Źródła i Założenia Projektowe
## Mobilna Karta Miejska Szczecin

**Data aktualizacji:** 2025-10-25

---

## Kategorie

1. [Płatności mobilne i e-commerce](#1-płatności-mobilne-i-e-commerce)
2. [Turystyka w Szczecinie](#2-turystyka-w-szczecinie)
3. [15-Minute City i zrównoważony rozwój](#3-15-minute-city-i-zrównoważony-rozwój)
4. [Smart City i mobilność miejska](#4-smart-city-i-mobilność-miejska)

---

## 1. Płatności mobilne i e-commerce

### Płatności mobilne w Szwecji (Swish)

| ID | Założenie | Źródło |
|----|-----------|--------|
| 1 | W Szwecji metoda płatności Swish jest bardzo popularna — rośnie udział płatności mobilnych. | [Sveriges Riksbank - The Swedish payments market is almost entirely digital](https://www.riksbank.se/en-gb/payments--cash/payments-in-sweden/payments-report-2025/trends-on-the-payments-market/the-swedish-payments-market-is-almost-entirely-digital/) |
| 2 | Swish ma już dużą penetrację użytkowników i jest ważnym kanałem płatności online/na urządzeniach mobilnych w Szwecji. | [Riksbank - Swish on the rise in e‑commerce](https://www.riksbank.se/en-gb/payments--cash/payments-in-sweden/payments-report--2024/trends-in-the-payments-market/payment-habits-in-sweden/swish-on-the-rise-in-e-commerce/) |

**Implikacje dla projektu:**
- Model płatności mobilnych sprawdza się w krajach nordyckich
- Warto zainspirować się doświadczeniami Swish przy projektowaniu płatności w Polsce
- Niemcy (główni turyści w Szczecinie) mogą preferować znane im metody (PayPal, karty)

---

### Guest Checkout i konwersja

| ID | Założenie | Źródło |
|----|-----------|--------|
| 3 | Zakupy bez konieczności logowania („guest checkout") zwiększają konwersję w procesach e‑commerce. | [PayPal - Guest Checkout: Drive E‑commerce Conversion](https://www.paypal.com/us/brc/article/importance-of-guest-checkout-for-ecommerce-conversion) |
| 4 | Skomplikowany checkout na urządzeniu mobilnym zwiększa współczynnik porzuceń koszyka / spadek konwersji. | [SolveIt Blog - How App Design Impacts Checkout Conversion Rates](https://solveit.dev/blog/how-app-design-impacts-conversion) |

**Implikacje dla projektu:**
- **Priorytet:** Guest checkout dla turystów (bez rejestracji!)
- Maksymalne uproszczenie procesu zakupu biletu
- Cel: zakup biletu w <30 sekund

---

### Geo-marketing i targetowanie

| ID | Założenie | Źródło |
|----|-----------|--------|
| 5 | Targetowanie ofert w oparciu o lokalizację użytkownika (geo‑marketing) ma uzasadnienie i wpływa na skuteczność komunikatów. | [FinTech Magazine - In the right place at the right time: mobile location‑based marketing](https://fintechmagazine.com/articles/are-payment-method-gaps-holding-back-e-commerce-conversion) |

**Implikacje dla projektu:**
- Push notifications o wydarzeniach w pobliżu
- Rekomendacje biletów zależne od lokalizacji (np. "Jesteś przy Arkonka, kup bilet!")
- Smart pricing (zniżki w godzinach poza szczytem)

---

## 2. Turystyka w Szczecinie

### Statystyki turystyczne 2024

| ID | Założenie | Źródło |
|----|-----------|--------|
| 6 | 82% turystów odwiedzających Szczecin pochodzi z Polski. | [Visit Szczecin - More and more tourists visit Szczecin](https://visitszczecin.eu/en/news/874-more-and-more-tourists-visit-szczecin) |
| 7 | 11% turystów odwiedzających Szczecin pochodzi z Niemiec. | [Visit Szczecin - More and more tourists visit Szczecin](https://visitszczecin.eu/en/news/874-more-and-more-tourists-visit-szczecin) |
| 8 | 61% zagranicznych turystów odwiedzających Szczecin to Niemcy. | [ResearchGate - Urban Tourism in Szczecin and its Impact on the Functioning of the Urban Transport System](https://www.researchgate.net/publication/277583292_Urban_Tourism_in_Szczecin_and_its_Impact_on_the_Functioning_of_the_Urban_Transport_System) |

**Kluczowe wnioski:**
- **Główni odbiorcy:** Polacy (82%) + Niemcy (61% zagranicznych)
- **Języki w aplikacji:** PL > DE > EN
- **Płatności:** polskie standardy + niemieckie preferencje (PayPal, EC-Karte)

---

### Wielkie wydarzenia

| ID | Założenie | Źródło |
|----|-----------|--------|
| 9 | Wydarzenie Sail Szczecin przyciągnęło prawie 390 000 turystów w jeden weekend sierpnia. | [Visit Szczecin - More and more tourists visit Szczecin](https://visitszczecin.eu/en/news/874-more-and-more-tourists-visit-szczecin) |
| 10 | Port Szczecin obsłużył 4 906 pasażerów w 2022 roku. | [Wikipedia - Port of Szczecin](https://en.wikipedia.org/wiki/Port_of_Szczecin) |

**Implikacje:**
- Skalowalność aplikacji (Sail Szczecin: 390k w weekend!)
- Event-driven notifications (The Tall Ships Races, koncerty)
- Integracja z kalendarzem wydarzeń miejskich

---

### Wzrost liczby turystów (2024)

| ID | Założenie | Źródło |
|----|-----------|--------|
| 11 | W 2024 roku Szczecin odwiedziło ponad 2,2 miliona turystów. | [Głos Szczeciński - Over 2 million tourists visited Szczecin in 2024](https://gs24.pl/od-poczatku-roku-szczecin-odwiedzilo-ponad-2-miliony-turystow-najwiecej-na-final-regat-the-tall-ships-races/ar/c1-18929345) |
| 12 | Najwięcej krajowych turystów przybyło z województw: dolnośląskiego (117,5 tys.), śląskiego (91,4 tys.), wielkopolskiego (74,9 tys.), łódzkiego. | [Głos Szczeciński - Over 2 million tourists visited Szczecin in 2024](https://gs24.pl/od-poczatku-roku-szczecin-odwiedzilo-ponad-2-miliony-turystow-najwiecej-na-final-regat-the-tall-ships-races/ar/c1-18929345) |
| 13 | Wśród turystów zagranicznych najwięcej przybyło z Niemiec (około 900 tys.), Czech (30 tys.) i Wielkiej Brytanii (43,5 tys.). | [Głos Szczeciński - Over 2 million tourists visited Szczecin in 2024](https://gs24.pl/od-poczatku-roku-szczecin-odwiedzilo-ponad-2-miliony-turystow-najwiecej-na-final-regat-the-tall-ships-races/ar/c1-18929345) |
| 14 | W sierpniu 2024 roku Szczecin odwiedziło ponad pół miliona turystów jednodniowych oraz 470 tys. osób, które zdecydowały się na nocleg w mieście. | [Szczecin Portal - Szczecin coraz bardziej popularny wśród turystów](https://szczecinportal.pl/co-przyciaga-turystow-do-szczecina/) |
| 15 | W 2024 roku w województwie zachodniopomorskim obiekty noclegowe stanowiły 14,1% krajowej bazy noclegowej. | [GUS - Turystyka w województwie zachodniopomorskim w 2024 r.](https://szczecin.stat.gov.pl/opracowania-biezace/opracowania-sygnalne/sport-turystyka/turystyka-w-wojewodztwie-zachodniopomorskim-w-2024-r-informacja-sygnalna%2C2%2C18.html) |

---

### Trendy turystyczne

| ID | Założenie | Źródło |
|----|-----------|--------|
| 16 | W 2024 roku Szczecin odnotował rekordowy wzrost liczby turystów, z 2,2 mln odwiedzających. | [Głos Szczeciński - Over 2 million tourists visited Szczecin in 2024](https://gs24.pl/od-poczatku-roku-szczecin-odwiedzilo-ponad-2-miliony-turystow-najwiecej-na-final-regat-the-tall-ships-races/ar/c1-18929345) |
| 17 | W 2024 roku Szczecin stał się atrakcyjnym celem na city break oraz krótkie wyjazdy, z coraz dłuższym sezonem turystycznym. | [Szczecin Portal - Szczecin coraz bardziej popularny wśród turystów](https://szczecinportal.pl/co-przyciaga-turystow-do-szczecina/) |

**Implikacje:**
- **City break focus:** Turyści potrzebują szybkiej orientacji (gdzie co jest, jak dojechać)
- **Weekend visitors:** Krótkie wizyty = potrzeba instant access (guest checkout!)
- **Rosnący trend:** Potencjał dla wieloletniego ROI aplikacji

---

## 3. 15-Minute City i zrównoważony rozwój

### Szczecin liderem w Polsce! 🏆

| ID | Założenie | Źródło |
|----|-----------|--------|
| **18** | **Szczecin jest liderem w Polsce w dążeniu do miasta 15-minutowego** - 40,6% mieszkańców deklaruje, że potrzeby codzienne mają w zasięgu 15 minut. | [SSOM - Szczecin liderem w Polsce w dążeniu do miasta 15-minutowego](https://som.szczecin.pl/2025/09/23/szczecin-liderem-w-polsce-w-dazeniu-do-miasta-15-minutowego/) |
| **19** | **Szczecin zajmuje 2. miejsce w Europie Środkowo-Wschodniej** w realizacji koncepcji 15-minute city (Friendly City Index 2025, badanie 54 miast z 9 krajów). | [TVP World - Meet the Polish town closest to ideal of '15-minute city'](https://tvpworld.com/89074562/polands-szczecin-closest-to-ideal-of-15-minute-city) |
| 20 | Dla porównania: w Krakowie odsetek ten wynosi około 30,3%, we Wrocławiu – 26,8%, a w Warszawie – tylko 15,8%. | [SSOM - Szczecin liderem w Polsce](https://som.szczecin.pl/2025/09/23/szczecin-liderem-w-polsce-w-dazeniu-do-miasta-15-minutowego/) |
| 21 | Koncepcja 15-minute city zakłada, że mieszkańcy powinni mieć dostęp w maksymalnie 15 minut (pieszo, rowerem, transportem publicznym) do najważniejszych usług codziennych. | [Bulletin of Geography - The 15-minute city: assumptions, opportunities and limitations](https://apcz.umk.pl/BGSS/article/view/57156) |

**Implikacje dla aplikacji:**
- ✅ **Szczecin JEST już 15-minute city** - aplikacja wspiera tę wizję!
- ✅ **Transport publiczny kluczowy** - integracja z ZDiTM to must-have
- ✅ **Walkowalność** - pokazuj dystanse pieszo/rowerem, nie tylko autem
- ✅ **Marketing:** "Wspieramy Szczecin #1 w Polsce dla 15-minute city!"

---

### Walkability i Smart Mobility

| ID | Założenie | Źródło |
|----|-----------|--------|
| 22 | Szczecin jest wymieniany wśród polskich miast (obok Łodzi, Rybnika, Gdyni, Wrocławia, Katowic) jako przykład dobrych praktyk w zakresie walkowalności. | [ResearchGate - The concept of a walkable city as an alternative form of urban mobility](https://www.researchgate.net/publication/318251451_The_concept_of_a_walkable_city_as_an_alternative_form_of_urban_mobility) |
| 23 | Aby miasto uznano za "walkable", musi spełniać cztery podstawowe warunki: bezpieczeństwo, funkcjonalność, atrakcyjność i wygodę. | [ResearchGate - The concept of a walkable city](https://www.researchgate.net/publication/318251451_The_concept_of_a_walkable_city_as_an_alternative_form_of_urban_mobility) |
| 24 | Walkowalność wiąże się z jakością życia, zdrowiem mieszkańców oraz korzyściami środowiskowymi i ekonomicznymi. | [ResearchGate - The concept of a walkable city](https://www.researchgate.net/publication/318251451_The_concept_of_a_walkable_city_as_an_alternative_form_of_urban_mobility) |

---

### Szczecin 2050 - wizja zrównoważonego rozwoju

| ID | Założenie | Źródło |
|----|-----------|--------|
| 25 | Szczecin realizuje projekt "Floating Garden 2050" - wizjonerską inicjatywę przekształcającą miasto w nowoczesne, eko-przyjazne miejsce łączące zieleń, drogi wodne i smart technologies. | [See Beautiful Places - Szczecin 2050: A Floating Garden](https://www.seebeautifulplaces.com/2017/12/szczecin-2050-floating-garden.html) |
| 26 | Do 2050 roku Szczecin ma być globalnym modelem zrównoważonego rozwoju miejskiego. | [See Beautiful Places - Szczecin 2050](https://www.seebeautifulplaces.com/2017/12/szczecin-2050-floating-garden.html) |
| 27 | Szczecin Metropolitan Railway ma być główną osią systemu transportu publicznego Szczecińskiego Obszaru Metropolitalnego. | [MDPI - Achieving Sustainable Mobility in the Szczecin Metropolitan Area](https://www.mdpi.com/2071-1050/13/22/12672) |

**Implikacje:**
- 🌱 **Green focus:** Promuj opcje eko (rower, pieszo, transport publiczny)
- 🚊 **Kolej metropolitalna:** Przyszła integracja z SKM
- 🎯 **Długoterminowa wizja:** Aplikacja jako część smart city ecosystem

---

## 4. Smart City i mobilność miejska

### Transport zrównoważony

| ID | Założenie | Źródło |
|----|-----------|--------|
| 28 | Szczecin jest badany jako case study zrównoważonego miejskiego transportu towarowego, uznając potrzebę zarządzania przepływami cargo i pasażerskimi jako spójnym elementem Sustainable Urban Development (SUD). | [ScienceDirect - Cargo tram in freight handling in urban areas in Poland](https://www.sciencedirect.com/science/article/abs/pii/S2210670721001906) |
| 29 | Prowadzone są badania nad potrzebami mieszkańców dotyczące mobilności miejskiej i rozwoju systemu transportowego Szczecina, wspierając zrównoważony rozwój transportu miejskiego. | [MDPI - Achieving Sustainable Mobility in the Szczecin Metropolitan Area](https://www.mdpi.com/2071-1050/13/22/12672) |

---

## Podsumowanie - Kluczowe wnioski dla projektu

### 🎯 Target audience
- **82% Polacy** (głównie z dolnośląskiego, śląskiego, wielkopolskiego)
- **61% zagranicznych to Niemcy** (900k rocznie!)
- **City break travelers** - potrzebują szybkiej orientacji

### 💳 Płatności
- **Must-have:** Guest checkout (bez rejestracji)
- **Priorytet:** PayPal, Apple Pay, Google Pay, Klarna (dla Niemców)
- **Cel:** Zakup biletu <30 sekund

### 🗺️ 15-Minute City
- **Szczecin #1 w Polsce** (40,6% mieszkańców w zasięgu 15 min od usług)
- **#2 w CEE** (Europa Środkowo-Wschodnia)
- **Transport publiczny kluczowy** - integracja z ZDiTM strategiczna

### 🌱 Sustainability
- **Floating Garden 2050** - wizja eko-miasta
- **Walkability** - promuj opcje pieszo/rower
- **Smart mobility** - aplikacja jako część większego ekosystemu

### 📈 Skalowalność
- **2,2 mln turystów/rok** (2024)
- **Sail Szczecin: 390k w weekend!**
- Aplikacja musi być gotowa na traffic spikes

---

**Ostatnia aktualizacja:** 2025-10-25
**Liczba źródeł:** 29 (nowe: 11 o 15-minute city i smart city)
**Status:** ✅ UPDATED WITH 15-MINUTE CITY DATA
