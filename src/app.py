######  👉 run with "streamlit run app.py" from cli 👈

# Importing the libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.errors import StreamlitAPIException

# Configuring the app
st.set_page_config(page_title="Visualiza — Aarmort", page_icon="📈", layout="wide")

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# User input
st.sidebar.title("Settings: ")

graph_type = st.sidebar.multiselect(
    "Graph Type",
    ["Default", "Table", "Bar Graph", "Line Graph", "Pie Chart", "Scatter Plot"],
    default=["Default"],
)

header = st.header("Visualiza - Visualize Data Easily")

# Reading
excel_types = ["xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt"]
uploaded_file = st.file_uploader(
    "Upload data:", type=["csv", "json", "xml", "html"] + excel_types
)

@st.cache(allow_output_mutation=True, show_spinner=False, persist=True)
def read(data=uploaded_file) -> pd.DataFrame:
    """Reads file and returns a pandas dataframe object"""
    extention = data.name.rsplit(".", 1)[1].lower()

    if extention == "csv":
        try:
            delimiter = st.sidebar.text_input("CSV delimiter", ",")
            return pd.read_csv(data, delimiter=delimiter, engine="python")
        except Exception as error:
            st.error("An error occured while trying to read data:")
            st.exception(error)
            st.stop()
    elif extention == "json":
        try:
            return pd.read_json(data)
        except Exception as error:
            st.error("An error occured while trying to read data:")
            st.exception(error)
            st.stop()
    elif extention == "xml":
        try:
            return pd.read_xml(data)
        except Exception as error:
            st.error("An error occured while trying to read data:")
            st.exception(error)
            st.stop()
    elif extention == "html":
        try:
            return pd.read_html(data)
        except Exception as error:
            st.error("An error occured while trying to read data:")
            st.exception(error)
            st.stop()
    elif extention in excel_types:
        try:
            return pd.read_excel(data)
        except Exception as error:
            st.error("An error occured while trying to read data:")
            st.exception(error)
            st.stop()
    else:
        st.error("This file is not supported.")
        st.stop()


if uploaded_file is not None:
    submit_placeholder = st.empty()
    if uploaded_file.getbuffer().nbytes >= 5000000:
        big_size_warning = st.empty()
        big_size_warning.warning(
            "Files with big sizes can take a while to process, please be patient when program is plotting."
        )
    df = read(data=uploaded_file)

# Plotting
if uploaded_file is not None:
    try:
        if df.isnull().values.any():
            df.fillna("", inplace=True)
        columns = list(df.columns)
        file_name = uploaded_file.name.rsplit(".", 1)[0].lower()

    except Exception:
        pass

    class Plot:
        def bar():
            """Plots a bar graph"""
            st.sidebar.header("Bar Graph:")
            st.header("Bar Chart:")
            title = st.sidebar.text_input("Title", value=file_name, key="bar_title")
            dimentions = st.sidebar.radio(
                "Dimensions", ["2D", "3D"], key="bar_dimentions"
            )
            y_axis = st.sidebar.selectbox("Y-Axis", columns, key="bar_y_axis")
            x_axis = st.sidebar.selectbox("X-Axis", columns, key="bar_x_axis")
            z_axis_holder = st.sidebar.empty()
            checkbox_color = st.sidebar.checkbox(
                "Color code chart?", key="bar_color_checkbox"
            )
            color_column = st.sidebar.empty()
            st.sidebar.subheader("Measurements:")
            height = st.sidebar.slider(
                "Height", min_value=400, max_value=1200, value=800, key="bar_height"
            )
            width = st.sidebar.slider(
                "Width", min_value=200, max_value=1500, value=1350, key="bar_width"
            )
            if dimentions == "2D":
                if checkbox_color:
                    color_column_value = color_column.selectbox(
                        "Column to color by [eg countries in covid-19 data]:",
                        columns,
                        key="bar_color_selectbox",
                    )
                    plot = px.bar(
                        df,
                        title=title,
                        x=x_axis,
                        y=y_axis,
                        color=color_column_value,
                        height=height,
                        width=width,
                    )
                else:
                    plot = px.bar(
                        df, x=x_axis, y=y_axis, title=title, height=height, width=width
                    )

            elif dimentions == "3D":
                z_axis = z_axis_holder.selectbox("Z-Axis", columns, key="bar_z_axis")
                if checkbox_color:
                    color_column_value = color_column.selectbox(
                        "Column to color by [eg countries in covid-19 data]:",
                        columns,
                        key="bar_color_selectbox",
                    )
                    plot = px.scatter_3d(
                        df,
                        x=x_axis,
                        y=y_axis,
                        z=z_axis,
                        color=color_column_value,
                        title=title,
                        height=height,
                        width=width,
                    )
                else:
                    plot = px.scatter_3d(
                        df,
                        x=x_axis,
                        y=y_axis,
                        z=z_axis,
                        title=title,
                        height=height,
                        width=width,
                    )
            st.plotly_chart(plot)

        def line():
            """Plots a line graph"""
            st.sidebar.header("Line Graph:")
            st.header("Line Chart:")
            title = st.sidebar.text_input("Title", value=file_name, key="line_title")
            dimentions = st.sidebar.radio(
                "Dimensions", ["2D", "3D"], key="line_dimentions"
            )
            y_axis = st.sidebar.selectbox("Y-Axis", columns, key="line_y_axis")
            x_axis = st.sidebar.selectbox("X-Axis", columns, key="line_x_axis")
            z_axis_holder = st.sidebar.empty()
            checkbox_color = st.sidebar.checkbox(
                "Color code chart?", key="line_color_checkbox"
            )
            color_column = st.sidebar.empty()
            st.sidebar.subheader("Measurements:")
            height = st.sidebar.slider(
                "Height", min_value=400, max_value=1200, value=800, key="line_height"
            )
            width = st.sidebar.slider(
                "Width", min_value=200, max_value=1500, value=1350, key="line_width"
            )
            if dimentions == "2D":
                if checkbox_color:
                    color_column_value = color_column.selectbox(
                        "Column to color by [eg countries in covid-19 data]:",
                        columns,
                        key="line_color_selectbox",
                    )
                    plot = px.line(
                        df,
                        title=title,
                        x=x_axis,
                        y=y_axis,
                        color=color_column_value,
                        height=height,
                        width=width,
                    )
                else:
                    plot = px.line(
                        df, x=x_axis, y=y_axis, title=title, height=height, width=width
                    )

            elif dimentions == "3D":
                z_axis = z_axis_holder.selectbox("Z-Axis", columns, key="line_z_axis")
                if checkbox_color:
                    color_column_value = color_column.selectbox(
                        "Column to color by [eg countries in covid-19 data]:",
                        columns,
                        key="line_color_selectbox",
                    )
                    plot = px.scatter_3d(
                        df,
                        x=x_axis,
                        y=y_axis,
                        z=z_axis,
                        color=color_column_value,
                        title=title,
                        height=height,
                        width=width,
                    )
                else:
                    plot = px.scatter_3d(
                        df,
                        x=x_axis,
                        y=y_axis,
                        z=z_axis,
                        title=title,
                        height=height,
                        width=width,
                    )
            st.plotly_chart(plot)

        def pie():
            st.sidebar.header("Pie Chart:")
            st.header("Pie Chart:")
            numeric_columns = list(df.select_dtypes(include=["int", "float"]).columns)
            normal_columns = list(df.select_dtypes(exclude=["int", "float"]).columns)
            title = st.sidebar.text_input("Title", value=file_name, key="pie_title")
            names = st.sidebar.selectbox("Column to plot", normal_columns)
            values = st.sidebar.selectbox(
                "Value of column to be considered", numeric_columns
            )
            height = st.sidebar.slider(
                "Height", min_value=400, max_value=1200, value=800, key="pie_height"
            )
            width = st.sidebar.slider(
                "Width", min_value=200, max_value=1500, value=1350, key="pie_width"
            )
            plot = px.pie(
                df, title=title, names=names, values=values, height=height, width=width
            )
            st.plotly_chart(plot)

        def scatter():
            """Plots a scatter graph"""
            st.sidebar.header("Scatter Graph:")
            st.header("Scatter Chart:")
            title = st.sidebar.text_input("Title", value=file_name, key="scatter_title")
            dimentions = st.sidebar.radio(
                "Dimensions", ["2D", "3D"], key="scatter_dimentions"
            )
            y_axis = st.sidebar.selectbox("Y-Axis", columns, key="scatter_y_axis")
            x_axis = st.sidebar.selectbox("X-Axis", columns, key="scatter_x_axis")
            z_axis_holder = st.sidebar.empty()
            checkbox_color = st.sidebar.checkbox(
                "Color code chart?", key="scatter_color_checkbox"
            )
            color_column = st.sidebar.empty()
            st.sidebar.subheader("Measurements:")
            height = st.sidebar.slider(
                "Height", min_value=400, max_value=1200, value=800, key="scatter_height"
            )
            width = st.sidebar.slider(
                "Width", min_value=200, max_value=1500, value=1350, key="scatter_width"
            )
            if dimentions == "2D":
                if checkbox_color:
                    color_column_value = color_column.selectbox(
                        "Column to color by [eg countries in covid-19 data]:",
                        columns,
                        key="scatter_color_selectbox",
                    )
                    plot = px.scatter(
                        df,
                        title=title,
                        x=x_axis,
                        y=y_axis,
                        color=color_column_value,
                        height=height,
                        width=width,
                    )
                else:
                    plot = px.scatter(
                        df, x=x_axis, y=y_axis, title=title, height=height, width=width
                    )

            elif dimentions == "3D":
                z_axis = z_axis_holder.selectbox(
                    "Z-Axis", columns, key="scatter_z_axis"
                )
                if checkbox_color:
                    color_column_value = color_column.selectbox(
                        "Column to color by [eg countries in covid-19 data]:",
                        columns,
                        key="scatter_color_selectbox",
                    )
                    plot = px.scatter_3d(
                        df,
                        x=x_axis,
                        y=y_axis,
                        z=z_axis,
                        color=color_column_value,
                        title=title,
                        height=height,
                        width=width,
                    )
                else:
                    plot = px.scatter_3d(
                        df,
                        x=x_axis,
                        y=y_axis,
                        z=z_axis,
                        title=title,
                        height=height,
                        width=width,
                    )
            st.plotly_chart(plot)

        def table():
            """Plots a table"""
            rows = st.slider(
                "Number of rows to show: ", value=5, min_value=1, max_value=len(df)
            )
            st.table(df.head(rows))


    try:
        if "Bar Graph" in graph_type:
            Plot.bar()

        if "Line Graph" in graph_type:
            Plot.line()

        if "Pie Chart" in graph_type:
            Plot.pie()

        if "Scatter Plot" in graph_type:
            Plot.scatter()

        if "Table" in graph_type:
            Plot.table()
        try:
            if "Default" in graph_type:
                st.write(df)
        except StreamlitAPIException:
            Plot.table()

    except Exception as exception:
        st.error("An error occured while trying to plot data:")
        st.exception(exception)
        
    finally:
        if uploaded_file is not None:
            if uploaded_file.getbuffer().nbytes >= 5000000:
                big_size_warning.empty()
