import streamlit as st

st.html('''
<style>
div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    max-height: 114px !important; /* Fix the height */
    overflow: auto !important;
}
</style>
''')

available_options = [i for i in range(-1, 10000)]
c1, c2, c3 = st.columns((1, 2, 1))
c2.multiselect(
    label="Select an Option",
    options=available_options,
    key="selected_options",
    format_func=lambda x: "All" if x == -1 else f"Option {x}",
)
st.write(st.session_state["selected_options"])
