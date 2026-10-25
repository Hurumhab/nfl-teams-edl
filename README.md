# NFL-joukkueiden URL EDL

Kaikkien 32 NFL-joukkueen viralliset verkkotunnukset Palo Alto PAN-OS:n perinteiseen, ulkoiselta HTTPS-palvelimelta noudettavaan **URL External Dynamic List** -objektiin. Tämä julkaisu käyttää GitHub Pagesia, ei SCM Hosted EDL -palvelua.

**Palomuurin Source-osoite:**

```text
https://hurumhab.github.io/nfl-teams-edl/nfl-teams.txt
```

- [Raakatekstinä julkaistu EDL](https://hurumhab.github.io/nfl-teams-edl/nfl-teams.txt)
- [Esittelysivu](https://hurumhab.github.io/nfl-teams-edl/)
- [Joukkuekohtaiset lähteet](SOURCES.md)

## Sisältö

64 domainriviä: 32 juuridomainia ja niiden 32 `www`-hostia. NFL:n virallisen hakemiston kaikki 32 **View Full Site** -linkkiä tarkistettiin 25.10.2026. [Lähdetaulukko](SOURCES.md) yhdistää jokaisen joukkueen domainiin.

Tiedosto `docs/nfl-teams.txt` on ASCII/UTF-8-tekstiä ilman BOMia, LF-rivinvaihdoilla ja yhdellä domainilla per rivi. Ei protokollaprefiksejä, polkuja, HTML:ää, JSONia, kommentteja, jokerimerkkejä tai tyhjiä rivejä.

Lista kattaa pääsivustojen juuri- ja www-hostit. Muut alidomainit, kaupat, lipunmyyjät, CDN:t ja ulkoiset videopalvelut eivät sisälly siihen. Tämä ei siis ole täydellinen verkkosivujen kaikkien riippuvuuksien sallintalista. Lista ei yksin muuta palomuurin liikennekäytäntöä.

## Käyttöönotto PAN-OS:ssa tai Panoramassa

1. Avaa **Objects → External Dynamic Lists → Add** oikeassa vsysissä tai Panorama Device Groupissa.
2. Anna nimeksi `NFL-Teams-URL-EDL` ja valitse **Type: URL List**. `Domain List` on DNS-sinkhole-käyttöön; tähän käyttötapaan valitaan URL List.
3. Aseta **Source** yllä olevaan `.txt`-osoitteeseen. Älä käytä repon GitHub-sivua, `blob`-osoitetta tai esittelysivua.
4. Valitse päivitysväliksi esimerkiksi **Hourly**. Julkinen tiedosto ei tarvitse Client Authentication -tunnuksia.
5. Valitse HTTPS-palvelimen varmentamiseen **Certificate Profile**, joka luottaa Pages-palvelimen voimassa olevan varmenneketjun myöntäjään. Varmista palomuurin DNS, kellonaika ja EDL-haun verkkoyhteys; käytössä voi olla MGT-liitäntä tai määritetty palvelureitti.
6. Käytä **Test Source URL** -toimintoa. Liitä EDL haluttuun URL Filtering -profiiliin ja valitse sille tarkoituksesi mukainen toiminto, esimerkiksi `alert` tai `block`. Liitä profiili asianomaiseen Security-sääntöön.
7. Tee **Commit** ja Panoramasta tarvittaessa **Push**. Pelkkä EDL-objektin luonti ei vielä estä sivustoja.

[Valmistajan käyttöönotto-ohje](https://docs.paloaltonetworks.com/network-security/security-policy/administration/objects/external-dynamic-lists/configure-the-firewall-to-access-an-external-dynamic-list) ja [URL Filtering -ohje](https://docs.paloaltonetworks.com/advanced-url-filtering/administration/configuring-url-filtering/url-category-exceptions/use-an-external-dynamic-list-in-a-url-filtering-profile).

### Osumasäännöt

PAN-OS erottaa `example.com`- ja `www.example.com`-merkinnät. Siksi molemmat ovat tässä listassa. Pidä **Device → Setup → Content-ID → URL Filtering → Append Ending Token** käytössä: se rajaa domainmerkinnän loppua. Vanhemmissa PAN-OS-versioissa tarkista vastaava asetus valmistajan ohjeesta. Lista jätetään pyynnön mukaisesti ilman kauttaviivoja.

Lue [PAN-OS:n osumasäännöt](https://docs.paloaltonetworks.com/advanced-url-filtering/administration/configuring-url-filtering/url-category-exceptions/guidelines-for-url-category-exceptions). Testaa omalla versiollasi sekä juuri- että www-osoite ja tarkista **Monitor → Logs → URL Filtering**. Tuotantopalomuurilla tehtävä osumatesti on erillinen verkkopalvelun lataustestistä.

### Tarkista ladattu lista palomuurilta

```text
request system external-list refresh type url name NFL-Teams-URL-EDL
request system external-list show type url name NFL-Teams-URL-EDL
```

Odotus: `Valid: Yes`, **64 valid entries**, **0 invalid entries**. Tarkista myös `Referenced: Yes` ja HTTPS-todennuksen tila. Jos oman PAN-OS-version CLI-syntaksi poikkeaa, käytä komentojen `?`-ohjetta tai EDL:n **List Entries** -näkymää.

## Julkaisu ja ylläpito

GitHub Pages: **Settings → Pages → Deploy from a branch → main → /docs**. `docs/.nojekyll` pitää tiedostot staattisina. `.txt` on EDL; `index.html` on ihmisille tarkoitettu esittelysivu.

Muuta domainit ja lähdetaulukko yhdessä. Listaa ei päivitetä automaattisesti NFL:stä. Tarkista muutokset ennen julkaisua:

```console
python validate_edl.py
```

Julkaisun jälkeen varmista myös HTTPS-vastaus ja täsmällinen sisältö:

```console
python validate_edl.py --url https://hurumhab.github.io/nfl-teams-edl/nfl-teams.txt
```

Tarkistus vaatii HTTP 200:n, `text/plain`-sisältötyypin, suoran osoitteen ilman uudelleenohjausta sekä tavuntarkan vastaavuuden paikalliseen listaan. Vaihtoehtoinen saman repon tekstiosoite on [raw.githubusercontent.com](https://raw.githubusercontent.com/Hurumhab/nfl-teams-edl/main/docs/nfl-teams.txt).
