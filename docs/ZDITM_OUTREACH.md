# Komunikacja z ZDiTM Szczecin
## Propozycja współpracy i request o parking API

**Data:** 2025-10-25
**Status:** DRAFT - gotowe do wysłania

---

## 1. Email Template - Parking API Request

### Subject / Temat
```
Zapytanie o API dla danych Park & Ride - projekt smart city
```

---

### Email Body / Treść

```
Szanowni Państwo,

Nazywam się [IMIĘ NAZWISKO] i jestem [członkiem zespołu deweloperskiego /
studentem / programistą] pracującym nad projektem demonstracyjnym aplikacji
smart city dla Szczecina, integrującej transport publiczny z usługami miejskimi.

=== POCHWAŁA OBECNEGO API ===

Przede wszystkim chciałbym pogratulować doskonale przygotowanego API dla
programistów! Korzystamy z:

✅ /api/v1/vehicles - real-time tracking pojazdów (aktualizacja co ~10s)
✅ /api/v1/stops - lokalizacje przystanków
✅ /api/v1/lines - informacje o liniach
✅ /api/v1/trajectories - trajektorie w GeoJSON
✅ GTFS Static + GTFS-RT - pełne dane rozkładowe

Jakość danych, dokumentacja i brak konieczności rejestracji sprawiają,
że ZDiTM Szczecin jest wzorem dla innych polskich miast!

=== NASZA PROŚBA ===

W ramach projektu chcemy także pokazać stan parkingów Park & Ride w czasie
rzeczywistym. Zauważyliśmy, że:

• Endpoint /api/v1/stops zawiera pole park_and_ride: true/false ✅
• Fizyczne tablice na parkingach pokazują wolne miejsca ✅
• Brakuje jednak endpointu API zwracającego dane o obłożeniu ❌

Czy planują Państwo udostępnienie API dla danych parkingowych zawierającego:

📊 Dane real-time:
  • Liczba miejsc ogółem (capacity)
  • Liczba miejsc zajętych (occupied)
  • Liczba miejsc wolnych (available)
  • % obłożenia (occupancy_percent)
  • Timestamp ostatniej aktualizacji

Przykładowy format odpowiedzi (propozycja):
```json
{
  "data": [
    {
      "id": 1,
      "name": "P&R Pomorzany",
      "latitude": 53.4284,
      "longitude": 14.4833,
      "capacity": {
        "total": 150,
        "occupied": 87,
        "available": 63,
        "occupancy_percent": 58
      },
      "last_updated": "2025-10-25T20:30:15Z",
      "status": "open"
    }
  ]
}
```

=== PRZYKŁADY Z INNYCH MIAST ===

Podobne API funkcjonują już m.in. w:

🌍 Sydney (Transport for NSW):
   https://opendata.transport.nsw.gov.au/dataset/car-park-api

🇵🇱 Rzeszów (Smart City System):
   2,200 miejsc parkingowych z real-time occupancy

🌍 Parkopedia (komercyjne):
   71 krajów, API dla developerów

=== DLACZEGO TO WAŻNE? ===

Dane o obłożeniu parkingów w czasie rzeczywistym pozwolą:

👥 Mieszkańcom:
  • Uniknąć jazdy na pełny parking (oszczędność czasu, paliwa)
  • Lepiej planować dojazd do pracy (P&R + tramwaj)

🚗 Miastu:
  • Lepsze zarządzanie ruchem (mniej aut szukających parkingu)
  • Analytics (kiedy parkingi się zapełniają, trendy)
  • Wsparcie dla polityki 15-minute city (Szczecin #1 w Polsce!)

🏆 Szczecin Smart City:
  • Pokazanie innowacyjności (dane otwarte dla developerów)
  • Wsparcie dla ekosystemu aplikacji miejskich
  • Marketing: "Najlepsze API transportowe w Polsce"

=== NASZA OFERTA WSPÓŁPRACY ===

Jesteśmy gotowi:

💻 Dostarczyć feedback jako early adopters API
📊 Podzielić się analytics (jak użytkownicy korzystają z danych)
📖 Udokumentować use cases (case study dla innych miast)
🤝 Promować ZDiTM API jako best practice w Polsce

=== CO DALEJ? ===

Czy moglibyśmy umówić się na krótkie spotkanie (online lub stacjonarne)
aby omówić:

1. Czy takie API jest w planach ZDiTM?
2. Jaki jest timeline (jeśli planowane)?
3. Czy możemy w jakiś sposób pomóc w jego uruchomieniu?
4. Jakie dane moglibyśmy otrzymać w fazie testowej?

=== PROJEKT - WIĘCEJ INFO ===

Nasz projekt demonstracyjny:
• GitHub: [LINK DO REPO]
• Technologia: Python, Streamlit, Leaflet.js, OpenStreetMap
• Status: Dokumentacja kompletna, implementacja w toku
• Cel: Proof of concept dla Szczecin smart city app
• Licencja: Open source (planowane)

Dokumentacja techniczna:
• TECH_SPEC.md - analiza API ZDiTM, struktura danych
• IMPLEMENTATION.md - architektura aplikacji
• GAPS_ANALYSIS.md - analiza braków w dostępnych API
• RESEARCH_FINDINGS.md - Szczecin jako 15-minute city (#1 PL!)

=== KONTAKT ===

Najlepszy sposób kontaktu:
📧 Email: [TWÓJ EMAIL]
📱 Tel: [TWÓJ TELEFON] (opcjonalnie)
💼 LinkedIn: [LINK] (opcjonalnie)
🐙 GitHub: [LINK]

Bardzo dziękuję za uwagę i za świetne API, z którego już korzystamy!
Z niecierpliwością czekam na odpowiedź.

Z poważaniem,
[IMIĘ NAZWISKO]
[Tytuł / Rola w projekcie]
[Data]

---

P.S. Jeśli parking API nie jest obecnie w planach, czy moglibyśmy
otrzymać dane historyczne (CSV/JSON) do analizy trendów dla celów
edukacyjnych? To także byłoby bardzo pomocne dla naszego projektu!
```

---

## 2. Adresy kontaktowe ZDiTM

### Oficjalne kanały

| Kanał | Adres | Notatki |
|-------|-------|---------|
| **Główny email** | zditm@zditm.szczecin.pl | Ogólne zapytania |
| **Strona WWW** | https://www.zditm.szczecin.pl/ | Formularz kontaktowy |
| **Dla programistów** | https://www.zditm.szczecin.pl/pl/zditm/dla-programistow | Brak dedykowanego emaila |
| **Telefon** | +48 91 48 59 259 | Centrala |
| **Adres** | ul. Klonowica 1, 71-241 Szczecin | Dla korespondencji pisemnej |

### Potencjalni adresaci (do znalezienia)

- **IT Department** - najbardziej właściwy
- **Dział Rozwoju / Innowacji**
- **Rzecznik prasowy** (jeśli projekt ma potencjał medialny)
- **Dyrektor ZDiTM** (jeśli projekt strategiczny)

**Strategia:** Start od głównego emaila, zapytać o przekierowanie do właściwej osoby.

---

## 3. Follow-up Strategy

### Timeline

| Dzień | Akcja |
|-------|-------|
| **D+0** | Wysłanie emaila |
| **D+7** | Jeśli brak odpowiedzi: Gentle reminder email |
| **D+14** | Jeśli brak odpowiedzi: Telefon na centralę + pytanie o właściwą osobę |
| **D+21** | Jeśli brak odpowiedzi: LinkedIn outreach (CTO/IT Manager ZDiTM) |
| **D+30** | Jeśli brak odpowiedzi: Plan B (mock data permanent) |

---

### Reminder Email Template (D+7)

```
Temat: Re: Zapytanie o API dla danych Park & Ride - gentle reminder

Dzień dobry,

Wysłałem tydzień temu zapytanie dotyczące możliwości udostępnienia
API dla danych o obłożeniu parkingów Park & Ride (email poniżej).

Rozumiem, że mogliście Państwo być zajęci - pozwolę sobie grzecznie
przypomnieć o mojej prośbie.

Jeśli to niewłaściwy adres, byłbym wdzięczny za przekierowanie do
odpowiedniej osoby w ZDiTM zajmującej się API dla developerów.

Dziękuję i pozdrawiam,
[IMIĘ NAZWISKO]

--- Original Message ---
[FORWARD ORYGINALNEGO EMAILA]
```

---

## 4. Alternative Approaches

### Jeśli email nie działa

#### Opcja A: Social Media

**LinkedIn:**
1. Znajdź profil ZDiTM Szczecin
2. Znajdź pracowników (IT, Development, Innovation)
3. Wysłaj connection request z custom message
4. Po akceptacji: krótka wiadomość o projekcie

**Twitter/X:**
```
@ZDiTM_Szczecin Pracujemy nad projektem smart city app dla Szczecina
wykorzystując Wasze świetne API! 🚊📱 Czy jest szansa na API dla
danych Park&Ride? Chętnie pomożemy w testach! #SzczecinSmartCity
#OpenData
```

---

#### Opcja B: Participation w wydarzeniach

**Hackathony / Konferencje:**
- Smart City Forum Szczecin (jeśli istnieje)
- Dni Otwarte ZDiTM
- Konsultacje społeczne (transport publiczny)

**Korzyść:** Bezpośredni kontakt face-to-face

---

#### Opcja C: Via Miasto Szczecin

**Urząd Miasta Szczecin:**
- Wydział Innowacji / Smart City (jeśli istnieje)
- Wydział Transportu
- Rada Miasta (radni zainteresowani smart city)

**Email pitch:**
```
Temat: Projekt smart city app - prośba o wsparcie w kontakcie z ZDiTM

Szanowni Państwo,

Pracujemy nad aplikacją demonstracyjną wspierającą Szczecin jako
lidera 15-minute city w Polsce (#1! wg Friendly City Index 2025).

Chcielibyśmy porozmawiać z ZDiTM o rozszerzeniu ich API o dane
parkingowe. Czy moglibyście Państwo pomóc w nawiązaniu kontaktu
lub rekomendacji projektu?

[... dalej jak w głównym emailu ...]
```

---

## 5. Pitch Deck (if meeting happens)

### Slajdy do przygotowania

1. **Cover:** "Szczecin Smart Mobility Platform"
2. **Problem:** Rozproszenie usług miejskich, trudność dla turystów
3. **Szczecin #1:** 15-minute city leader w Polsce (40,6%)
4. **Turystyka:** 2,2M rocznie, 900k Niemców - potencjał wzrostu
5. **Rozwiązanie:** Jedna aplikacja - transport, parkingi, bilety, POI
6. **Tech Stack:** ZDiTM API + Leaflet + OSM (open source, darmowe)
7. **Demo:** Live mapa z real-time tramwajami
8. **Gap:** Brak parking API - mock data obecnie
9. **Propozycja:** Współpraca przy parking API
10. **Korzyści dla ZDiTM:** Analytics, feedback, case study, marketing
11. **Timeline:** MVP (gotowe), Beta (3 mc), Production (6 mc)
12. **Q&A:** Pytania i dyskusja

**Format:** PDF, 10-15 slajdów, max 10 min prezentacji

---

## 6. Expected Outcomes & Responses

### Scenario A: ✅ Pozytywna odpowiedź

**ZDiTM odpowiada: "Tak, planujemy parking API w Q2 2025"**

**Nasze działania:**
1. ✅ Dziękujemy i prosimy o beta access
2. ✅ Oferujemy feedback podczas testów
3. ✅ Zobowiązujemy się do case study
4. ⏳ Czekamy, w międzyczasie mock data
5. 🚀 Migracja do real API gdy dostępne

---

### Scenario B: 🤔 "Możliwe, ale nie priorytet"

**ZDiTM: "Nie mamy w planach najbliższych, ale rozważymy"**

**Nasze działania:**
1. 📊 Przedstawiamy business case (oszczędność czasu, less traffic)
2. 📈 Pokazujemy dane z innych miast (Sydney, Rzeszów)
3. 🤝 Oferujemy pomoc techniczną (np. stworzenie specyfikacji API)
4. 💡 Sugerujemy pilot program (1 parking jako test)
5. ⏰ Prosimy o ponowną rozmowę za 3-6 miesięcy

---

### Scenario C: ❌ Odmowa

**ZDiTM: "Nie, nie planujemy udostępniać takich danych"**

**Nasze działania:**
1. 😊 Dziękujemy za odpowiedź (bez presji!)
2. ❓ Pytamy o powody (privacy? technical? priorities?)
3. 🔄 Proponujemy alternatywy:
   - Dane historyczne (CSV) do analizy trendów?
   - Agregowane dane (bez real-time)?
   - Status "open/closed" bez liczb?
4. 📝 Dokumentujemy decyzję (GAPS_ANALYSIS.md update)
5. ✅ Kontynuujemy projekt z mock data
6. 🔮 Rozważamy crowdsourced data (v3.0)

---

### Scenario D: 🤷 Brak odpowiedzi

**Po 30 dniach i 3 follow-upach - cisza**

**Nasze działania:**
1. 📋 Akceptujemy brak odpowiedzi
2. ✅ Kontynuujemy z mock data (permanent)
3. 📢 Dokumentujemy publicznie:
   ```
   "Parking data are simulated. We requested real-time API
   from ZDiTM Szczecin but didn't receive response. If you're
   from ZDiTM and interested in collaboration, please contact us!"
   ```
4. 🔄 Ponawiamy contact za 6-12 miesięcy (może sytuacja się zmieni)

---

## 7. Talking Points - Key Arguments

### Dlaczego parking API jest ważny?

#### 1. User Experience (mieszkańcy)
```
"Ania jedzie do pracy o 7:45. Bez API:
 • Jedzie na P&R Pomorzany
 • Parking PEŁNY (8:00 rush hour)
 • Szuka innego P&R (20 min stracone)
 • SPÓŹNIENIE do pracy

Z API:
 • Sprawdza app o 7:40: 'Pomorzany 95% zajęte'
 • Jedzie od razu na P&R Kijewo (30% zajęte)
 • NA CZAS w pracy ✅

Oszczędność: 20 minut × 250 dni roboczych = 83 godziny rocznie!"
```

---

#### 2.Reducja ruchu (ekologia)

```
"Auta szukające parkingu = zbędny ruch:
 • Spalanie paliwa
 • Emisja CO₂
 • Hałas
 • Korki

Badania (UCLA): 30% ruchu w centrach miast to auta SZUKAJĄCE parkingu!

Real-time parking API:
 → Kierujesz kierowców od razu do wolnych miejsc
 → Mniej kilometrów niepotrzebnych
 → Lepsza jakość powietrza
 → Wsparcie dla Szczecin 2050 Floating Garden vision"
```

---

#### 3. Smart City Leadership

```
"Szczecin już jest #1 w Polsce (15-minute city)!

Parking API to kolejny krok:
 ✅ Open Data pioneer (wzór dla innych miast)
 ✅ Developer ecosystem (więcej aplikacji = lepszy UX)
 ✅ Marketing: 'Najlepsze API transportowe w PL'
 ✅ Attrakcyjność dla turystów (2,2M rocznie!)

Przykłady miast z parking API:
 • Sydney (2019)
 • Rzeszów (2020) 🇵🇱
 • Barcelona
 • San Francisco

Szczecin może być PIERWSZY dużym miastem w PL z pełnym API!"
```

---

#### 4. Dane dla miasta (analytics)

```
"API to nie tylko dla użytkowników - też dla ZDiTM!

Analytics z API pokażą:
 📊 Kiedy parkingi się zapełniają (trendy godzinowe, dzienne)
 📊 Które P&R najpopularniejsze (investment priorities)
 📊 Seasonal patterns (wakacje vs rok szkolny)
 📊 Impact of events (Sail Szczecin → parking demand spike?)

→ Data-driven decisions dla rozwoju infrastruktury
→ Lepsze planowanie pojemności parkingów
→ ROI calculation dla nowych P&R"
```

---

## 8. Post-Meeting Actions

### Jeśli meeting się odbędzie

**Immediately after (D+0):**
- [ ] Wysłać thank you email
- [ ] Podsumować ustalone punkty
- [ ] Załączyć slajdy prezentacji
- [ ] Zaproponować next steps

**Follow-up (D+7):**
- [ ] Status update (czy decyzje zostały podjęte?)
- [ ] Odpowiedzieć na ewentualne pytania techniczne
- [ ] Dostarczyć dodatkowe materiały (jeśli prosili)

**Long-term:**
- [ ] Keep them updated o progress projektu
- [ ] Share analytics / user feedback
- [ ] Invite to demo / launch event

---

## 9. Legal & Compliance

### Checklist przed wysłaniem emaila

- [ ] ✅ Nie prosimy o dane poufne
- [ ] ✅ Nie oferujemy pieniędzy (public procurement issues)
- [ ] ✅ Open source approach (transparent)
- [ ] ✅ Educational / research context (non-commercial)
- [ ] ✅ Compliance with RODO (nie gromadzimy danych osobowych)
- [ ] ✅ Respect ToS obecnego API ZDiTM

### Disclaimer w projekcie

```
"This project is an independent technical demonstration
created for educational purposes. It is not affiliated with,
endorsed by, or officially supported by ZDiTM Szczecin or
the City of Szczecin.

All data displayed is either:
• Obtained via public APIs (ZDiTM)
• Simulated for demonstration purposes (parking data)
• Aggregated from public sources (tourism statistics)

For official information, please visit:
https://www.zditm.szczecin.pl/"
```

---

## 10. Summary Checklist

### Przed wysłaniem emaila:

- [ ] Przeczytaj template kilka razy (typos?)
- [ ] Dostosuj tone (formalny ale friendly)
- [ ] Dodaj link do GitHub repo
- [ ] Dodaj swoje dane kontaktowe
- [ ] Sprawdź adres email ZDiTM (aktualny?)
- [ ] CC do siebie (backup)
- [ ] Subject line jasny i konkretny
- [ ] Email < 500 słów (zwięzły!)

### Po wysłaniu:

- [ ] Zapisz email w CRM / notes
- [ ] Ustaw reminder (D+7 follow-up)
- [ ] Kontynuuj projekt (nie czekaj na odpowiedź!)
- [ ] Przygotuj Plan B (permanent mock data)

---

**Document Status:** ✅ READY TO USE
**Last Updated:** 2025-10-25
**Next Action:** Send email to ZDiTM! 📧

---

## Appendix: Quick Wins (if they say YES)

### Co możemy dostarczyć ZDiTM w zamian?

1. **📊 Analytics Dashboard**
   - Pokazujemy jak użytkownicy używają parking data
   - Heatmapy (które parkingi, kiedy)
   - User journey analysis

2. **📝 Case Study**
   - "How Szczecin became the first Polish city with full mobility API"
   - Publikacja na Medium / Dev.to
   - Prezentacja na konferencjach (Smart City Forum)

3. **🐛 Bug Reports**
   - Early testing parking API
   - Feedback o edge cases
   - Suggestions for improvements

4. **📚 Documentation**
   - Example code (Python, JavaScript)
   - Tutorial: "How to integrate ZDiTM parking API"
   - Postman collection

5. **🎨 Promotion**
   - Social media mentions
   - GitHub stars / forks
   - Developer community engagement

**Win-Win!** 🤝
