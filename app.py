import pandas as pd
import streamlit as st
import urllib.parse
import io

# Streamlit app setup
st.set_page_config(page_title="WhatsApp Link Generator", layout="centered")

# Custom image + title layout
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 16px;">
        <img src="https://raw.githubusercontent.com/Astronone/dekssswablast/main/gadjah.png" alt="Logo" width="128">
        <h1 style="margin: 0;">Dekss WhatsApp Link Generator</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Upload file  `.xlsx` dengan isi kolom 1 dan row 1  `Nomor` (phone number) dan kolom 2 row 1 `Pesan` (message). Lalu nomor telepon sudah dalam format nomor menggunakan kode negara 628*******.")

# Example file and table
st.markdown("### 📊 Format Excell")
st.write("Row pertama pada kolom A diberi nama `Nomor` dan kolom B diberi nama `Pesan` (tampa tanda petik). Kolom A berisikan nomor menggunakan kode negara 628 (tanpa tanda +), dan kolom B berisikan pesan. ")
example_df = pd.DataFrame({
    "Nomor": ["6281234567890", "6289876543210"],
    "Pesan": ["Halo! Ini pesan pertama.\nBaris kedua.", "Selamat pagi!"]
})

st.image(
    "https://raw.githubusercontent.com/Astronone/dekssswablast/main/contoh.png",
    caption="Contoh Format File Excel",
    use_container_width=True
)
st.write("klik browser file dan pilih file. Jika ingin mengganti file klik tanda silang bagian bawah setelah drag and drop file ")

st.dataframe(example_df)

# File uploader (CSV and Excel)
uploaded_file = st.file_uploader("Upload file `.xlsx` file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Detect file type and read
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, delimiter=';', dtype=str)
        else:
            df = pd.read_excel(uploaded_file, dtype=str)

        # Drop empty rows
        df.dropna(subset=['Pesan', 'Nomor'], inplace=True)

        # Ensure 'Nomor' is string
        df['Nomor'] = df['Nomor'].apply(str)

        # Generate WhatsApp links
        def create_link(row):
            number = row['Nomor'].strip()
            message = str(row['Pesan']).replace("\\n", "\n")
            encoded_message = urllib.parse.quote(message)
            return f"https://wa.me/{number}?text={encoded_message}"

        df['WhatsApp_Link'] = df.apply(create_link, axis=1)

        # Clickable HTML links
        df['Clickable_Link'] = df['WhatsApp_Link'].apply(
            lambda url: f'<a href="{url}" target="_blank">Open Chat</a>'
        )

        # Display preview
        st.success("✅ WhatsApp links generated!")
        st.write("### Preview Table")
        st.markdown(
            df[['Pesan', 'Nomor', 'Clickable_Link']].to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # Download CSV (preserve formatting)
        csv = df.to_csv(index=False, float_format='%.0f')
        st.download_button("📥 Download Result CSV", data=csv, file_name="whatsapp_links.csv", mime="text/csv")

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")

else:
    st.info("📂 Tolong upload file dengan format `.xlsx`.")
