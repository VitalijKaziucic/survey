import pandas as pd
import streamlit as st
import time
import os


class Colors:
    green = "green"
    red = "red"


class Survey:

    def __init__(self, projects: list, participants: list):
        self.projects = projects
        self.participants = [""] + participants
        self.respondent = None

    def reset_survey(self):

        names = ["respondent"] + self.projects
        values = [st.session_state.get(key) for key in names]
        dataframe = pd.DataFrame.from_dict({"key": names, "values": values})
        file_name = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {self.respondent}.csv"
        path_name = file_name[:7]
        os.mkdir(path_name)
        file_save = os.path.join(path_name, file_name)
        dataframe.to_csv(file_save, index=False)
        for project in self.projects:
            st.session_state[project] = 0
        st.balloons()
        st.session_state["respondent"] = ""
        st.session_state["submit"] = False

    def fill_table(self):
        col1, col2, col3 = st.columns(3, gap="large")
        columns = {0: col1, 1: col2, 2: col3}
        rows = {0: [], 1: [], 2: []}

        for i in range(0, len(self.projects), 3):
            row = 0
            for j in range(0 + i, i + 3):
                try:
                    rows[row].append(self.projects[j])
                except IndexError:
                    rows[row].append("")
                row += 1

        for column, projects in rows.items():

            with columns.get(column):
                for project in projects:
                    if project:
                        st.number_input(label=project,
                                  min_value=0,
                                  max_value=100,
                                  step=5, key=project)
                    else:
                        st.write(project)

    def run_app(self):

        disable_select_participants = False
        visibility = "visible"
        self.respondent = st.session_state.get("respondent", None)
        if self.respondent:
            disable_select_participants = True
            visibility = "collapsed"

        st.title("LN projects")
        st.selectbox(label="Select your name:",
                     options=self.participants,
                     disabled=disable_select_participants,
                     key="respondent",
                     label_visibility=visibility)

        if disable_select_participants:
            # calc points
            total = sum(value for key, value in st.session_state.items() if key in self.projects)
            submit_disabled = False if total == 100 else True

            # set text color
            color = None
            if total == 100:
                color = Colors.green
            elif total > 100:
                color = Colors.red

            total_string = f'<p style="{f"color: %s;font-size:20px" % color if color else "font-size:20px"}">' \
                           f'Total time: {total}%</p>'

            st.subheader("Determine the percentage of time you spent working on the project per month")
            st.write(total_string, unsafe_allow_html=True)

            if total > 100:
                st.error("Max total value is 100%", icon="⚠️")

            self.fill_table()

            submitted = st.button("Submit", key="submit", disabled=submit_disabled, on_click=self.reset_survey)

            if submitted:
                st.experimental_rerun()
