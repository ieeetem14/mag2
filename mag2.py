import streamlit as st

# **UWAGA:** Ponieważ nie używamy stanów sesji ani trwałego zapisu danych,
# ta globalna lista zostanie zresetowana przy każdym ponownym uruchomieniu
# lub ponownym załadowaniu aplikacji Streamlit.
STAN_MAGAZYNU = []

def dodaj_towar(nazwa: str, ilosc: int, cena: float):
    """Dodaje towar do magazynu, jeśli wszystkie pola są poprawne."""
    try:
        if not nazwa or ilosc <= 0 or cena <= 0:
            st.error("Wszystkie pola muszą być wypełnione, a ilość/cena muszą być większe niż 0.")
            return

        nowy_towar = {
            "nazwa": nazwa.strip(),
            "ilosc": ilosc,
            "cena": cena
        }
        STAN_MAGAZYNU.append(nowy_towar)
        st.success(f"Dodano '{nazwa.strip()}' do magazynu.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas dodawania towaru: {e}")

def usun_towar(indeks: int):
    """Usuwa towar z magazynu na podstawie jego indeksu."""
    try:
        if 0 <= indeks < len(STAN_MAGAZYNU):
            nazwa = STAN_MAGAZYNU[indeks]['nazwa']
            del STAN_MAGAZYNU[indeks]
            st.success(f"Usunięto '{nazwa}' z magazynu.")
        else:
            st.error("Niepoprawny indeks towaru.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas usuwania towaru: {e}")

def pokaz_magazyn():
    """Wyświetla aktualną zawartość magazynu jako tabelę Streamlit."""
    st.subheader("📦 Aktualny Stan Magazynu")

    if STAN_MAGAZYNU:
        # Konwertujemy listę słowników na listę wyświetlaną w tabeli z indeksami
        dane_do_wyswietlenia = []
        for i, towar in enumerate(STAN_MAGAZYNU):
            dane_do_wyswietlenia.append({
                "ID": i,
                "Nazwa": towar['nazwa'],
                "Ilość": towar['ilosc'],
                "Cena (PLN)": f"{towar['cena']:.2f}"
            })

        st.dataframe(dane_do_wyswietlenia, use_container_width=True)

        # Opcjonalne podsumowanie
        wartosc_calkowita = sum(item['ilosc'] * item['cena'] for item in STAN_MAGAZYNU)
        st.metric(label="Całkowita Wartość Magazynu", value=f"{wartosc_calkowita:,.2f} PLN")
    else:
        st.info("Magazyn jest pusty.")

# --- Główna Funkcja Aplikacji ---
def main():
    st.title("🛒 Prosty System Magazynowy (Lista-bazowy)")
    st.markdown("---")

    # 1. Panel Dodawania Towaru
    st.header("➕ Dodaj Towar")
    with st.form("form_dodaj"):
        col1, col2, col3 = st.columns(3)
        nazwa_towaru = col1.text_input("Nazwa Towaru")
        ilosc_towaru = col2.number_input("Ilość", min_value=1, step=1, value=1)
        cena_towaru = col3.number_input("Cena Jednostkowa (PLN)", min_value=0.01, step=0.01, format="%.2f", value=1.00)

        przycisk_dodaj = st.form_submit_button("Dodaj do Magazynu")

        if przycisk_dodaj:
            dodaj_towar(nazwa_towaru, ilosc_towaru, cena_towaru)

    st.markdown("---")

    # 2. Panel Wyświetlania Magazynu
    pokaz_magazyn()

    st.markdown("---")

    # 3. Panel Usuwania Towaru
    st.header("➖ Usuń Towar")
    if STAN_MAGAZYNU:
        # Tworzymy słownik dla pola selectbox: ID -> Nazwa
        opcje_usun = {
            i: f"ID {i}: {item['nazwa']} (Ilość: {item['ilosc']})"
            for i, item in enumerate(STAN_MAGAZYNU)
        }

        # Wymuszamy wybór klucza (ID), a wyświetlamy pełną nazwę
        wybrany_klucz = st.selectbox(
            "Wybierz towar do usunięcia (wg ID):",
            options=list(opcje_usun.keys()),
            format_func=lambda x: opcje_usun[x]
        )
        
        przycisk_usun = st.button("Usuń Wybrany Towar")

        if przycisk_usun and wybrany_klucz is not None:
            usun_towar(wybrany_klucz)
    else:
        st.info("Brak towarów do usunięcia.")

if __name__ == "__main__":
    main()
