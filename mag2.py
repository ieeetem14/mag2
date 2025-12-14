import streamlit as st
import pandas as pd

# --- Konfiguracja i Inicjalizacja Danych ---

def inicjalizuj_stan():
    """Inicjalizuje stan sesji dla magazynu, jeśli jeszcze nie istnieje."""
    if 'magazyn' not in st.session_state:
        # Struktura: lista słowników
        st.session_state['magazyn'] = []
    
    if 'next_id' not in st.session_state:
        # Unikalne ID dla każdego towaru (ułatwia usuwanie)
        st.session_state['next_id'] = 1

def dodaj_towar(nazwa: str, ilosc: int, cena: float):
    """Dodaje towar do magazynu i zwiększa unikalne ID."""
    if not nazwa or ilosc <= 0 or cena <= 0:
        st.error("Wszystkie pola muszą być wypełnione, a ilość/cena muszą być większe niż 0.")
        return

    nowy_towar = {
        "id": st.session_state['next_id'],
        "Nazwa": nazwa.strip(),
        "Ilość": ilosc,
        "Cena (PLN)": cena
    }
    st.session_state['magazyn'].append(nowy_towar)
    st.session_state['next_id'] += 1
    st.success(f"Dodano '{nazwa.strip()}' (ID: {nowy_towar['id']}) do magazynu.")

def usun_towar(towar_id: int):
    """Usuwa towar z magazynu na podstawie unikalnego ID."""
    
    # Używamy list comprehension do stworzenia nowej listy bez usuniętego elementu
    st.session_state['magazyn'] = [
        item for item in st.session_state['magazyn'] if item['id'] != towar_id
    ]
    st.success(f"Usunięto towar o ID: {towar_id}.")

def pokaz_magazyn():
    """Wyświetla aktualny stan magazynu."""
    st.subheader("📦 Aktualny Stan Magazynu")

    magazyn = st.session_state['magazyn']
    
    if magazyn:
        # Konwersja listy słowników na DataFrame dla ładniejszego wyświetlania
        df = pd.DataFrame(magazyn)
        
        # Obliczanie wartości całkowitej
        df['Wartość Całkowita'] = df['Ilość'] * df['Cena (PLN)']
        
        st.dataframe(df, use_container_width=True)

        # Podsumowanie
        wartosc_calkowita = df['Wartość Całkowita'].sum()
        st.metric(label="Całkowita Wartość Magazynu", value=f"{wartosc_calkowita:,.2f} PLN")
    else:
        st.info("Magazyn jest pusty.")

# --- Główna Funkcja Aplikacji ---
def main():
    inicjalizuj_stan()
    
    st.set_page_config(page_title="Magazyn", layout="wide")
    st.title("🛒 Stabilny System Magazynowy (z Session State)")
    st.markdown("---")

    # Kolumny dla formularzy i widok magazynu
    col_input, col_display = st.columns([1, 2])

    with col_input:
        # 1. Panel Dodawania Towaru
        st.header("➕ Dodaj Towar")
        with st.form("form_dodaj"):
            nazwa_towaru = st.text_input("Nazwa Towaru")
            
            col_in1, col_in2 = st.columns(2)
            ilosc_towaru = col_in1.number_input("Ilość", min_value=1, step=1, value=1, key="ilosc_input")
            cena_towaru = col_in2.number_input("Cena Jednostkowa (PLN)", min_value=0.01, step=0.01, format="%.2f", value=1.00, key="cena_input")

            przycisk_dodaj = st.form_submit_button("Dodaj do Magazynu")

            if przycisk_dodaj:
                dodaj_towar(nazwa_towaru, ilosc_towaru, cena_towaru)

        st.markdown("---")
        
        # 3. Panel Usuwania Towaru
        st.header("➖ Usuń Towar")
        magazyn_do_usuniecia = st.session_state['magazyn']
        
        if magazyn_do_usuniecia:
            # Tworzymy opcje: "ID: Nazwa Towaru"
            opcje_usun = {
                item['id']: f"ID {item['id']}: {item['Nazwa']}"
                for item in magazyn_do_usuniecia
            }

            wybrany_id = st.selectbox(
                "Wybierz towar do usunięcia:",
                options=list(opcje_usun.keys()),
                format_func=lambda x: opcje_usun[x]
            )
            
            przycisk_usun = st.button("Usuń Wybrany Towar z Magazynu")

            if przycisk_usun and wybrany_id is not None:
                usun_towar(wybrany_id)
                # Ponowne uruchomienie aplikacji, aby odświeżyć widok
                st.rerun() 
        else:
            st.info("Brak towarów do usunięcia.")

    with col_display:
        # 2. Panel Wyświetlania Magazynu
        pokaz_magazyn()

if __name__ == "__main__":
    main()
