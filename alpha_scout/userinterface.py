import streamlit as st


class EventContainer:
    def __init__(self):
        self.container = st.container(border=True)
        self.col1, self.col2, self.col3, self.col4, self.col5, self.col6, self.col7 = self.container.columns(7, vertical_alignment='center')
    
    def writeCol(self, column_number, str):
        match column_number:
            case 1:
                with self.col1:
                    st.write(str)
            case 2:
                with self.col2:
                    st.write(str)
            case 3:
                with self.col3:
                    st.write(str)
            case 4:
                with self.col4:
                    st.write(str)
            case 5:
                with self.col5:
                    st.write(str)
            case 6:
                with self.col6:
                    st.write(str)
            case 7:
                with self.col7:
                    st.write(str)
            case _:
                st.error("Invalid column_number passed to writeCol()")