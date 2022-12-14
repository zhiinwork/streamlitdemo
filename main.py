import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import os

def get_log_text(file_selected_path,n_lines = 10):
    file = open(file_selected_path, 'r')
    lines = file.read().splitlines()
    file.close()
    return lines[-n_lines:]

def list_files(directory, extension):
    # list certain extension files in the folder
    return [f for f in os.listdir(directory) if f.endswith('.' + extension)]

def concat_file_path(file_folder, file_selected):
    # handle the folder path with '/' or 'without './'
    # and concat folder path and file path
    if str(file_folder)[-1] != '/':
        file_selected_path = file_folder + '/' + file_selected
    else:
        file_selected_path = file_folder + file_selected
    return file_selected_path

@st.cache(suppress_st_warning=True)
def load_csv(file_selected_path, nrows):
    # load certain rows
    try:
        if nrows == -1:
            df = pd.read_csv(file_selected_path)
        else:
            df = pd.read_csv(file_selected_path, nrows=nrows)
    except Exception as ex:
        df = pd.DataFrame([])
        st.exception(ex)
    return df

def app_main():
    st.set_page_config(page_title="Hello",page_icon="ð",)
    st.write("# Logæ°æ®åæåç»å¾ç¤ºä¾")
    st.sidebar.success("ä¸æ¹éæ©åè½ï¼ä¸æ¹éç½®åæ°")
    st.title("æ°æ®å è½½åç®ååæ")
    if st.sidebar.checkbox('éæ©æ°æ®æº'):
        file_folder = st.sidebar.text_input('æä»¶å¤¹', value="data")
        data_file_list = list_files(file_folder, 'csv')
        if len(data_file_list) ==0:
            st.warning(f'æ­¤è·¯å¾æ å¯ç¨æ°æ®é')
        else:
            file_selected = st.sidebar.selectbox(
                'éæ©æä»¶', data_file_list)
            file_selected_path = concat_file_path(file_folder, file_selected)
            nrows = st.sidebar.number_input('è¯»åè¡æ°(-1è¡¨ç¤ºå¨é¨è¯»åº)', value=-1)
            n_rows_str = 'å¨é¨' if nrows == -1 else str(nrows)
            st.info(f'å·²éæ©æä»¶ï¼{file_selected_path}ï¼è¯»åè¡æ°ä¸º{n_rows_str}')
    else:
        file_selected_path = None
        nrows = 100
        st.warning(f'å½åéæ©æä»¶ä¸ºç©ºï¼è¯·éæ©ã')

    if st.sidebar.checkbox('ç»å¾'):
        if file_selected_path is not None:
            df = load_csv(file_selected_path, nrows)
            n_lines =st.sidebar.slider(label='ç»å¶èå´',min_value=3,max_value=len(df),value=len(df))
            try:
                cols = df.columns.to_list()
                axis_x = st.sidebar.selectbox('xè½´', cols, index=0)
                axis_y = st.sidebar.selectbox('yè½´', cols, index=1)

                tab1, tab2, tab3 = st.tabs(["æçº¿å¾", "æ£ç¹å¾", "ååæ°æ£ç¹"])
                with tab1:
                    st.header("è¿éæ¯æçº¿å¾")
                    st.line_chart(df[:n_lines],x=axis_x,y=axis_y)
                with tab2:
                    st.header("è¿éæ¯æ£ç¹å¾")
                    fig = plt.figure()
                    # ax = fig.add_subplot(111)
                    plt.scatter(df[:n_lines][axis_x], df[:n_lines][axis_y])
                    st.pyplot(fig)
                with tab3:
                    st.header("åæ£ç¹å¾")
                    axis_y2 = st.sidebar.selectbox('yè½´2', cols, index=2)
                    fig = plt.figure()
                    # ax = fig.add_subplot(111)
                    plt.plot(df[:n_lines][axis_x], df[:n_lines][axis_y], 'o', color='orange')
                    plt.plot(df[:n_lines][axis_x], df[:n_lines][axis_y2], 'x', color='blue')
                    plt.legend()
                    st.pyplot(fig)

                st.dataframe(df[:n_lines])
            except BaseException:
               st.sidebar.warning(f'æ°æ®æ ¼å¼æ æ³æ­£ç¡®è¯»å')
               target_col = None

    if st.sidebar.checkbox('æ±æ»åæ'):
        if file_selected_path is not None:
            if st.sidebar.button('çææ¥å'):
                df = load_csv(file_selected_path, nrows)
                st.write('å¤çä¸­ï¼æ¯è¾æ¢ï¼ç¨åâ¦â¦')
                pr = ProfileReport(df, explorative=True)
                st_profile_report(pr)
        else:
            st.info(f'è¯·éæ©æä»¶')

    if st.sidebar.checkbox('æ¾ç¤ºææ¬æ ¼å¼'):
        if file_selected_path is not None:
            n_lines =st.sidebar.slider(label='è¡æ°',min_value=3,max_value=50)
            if st.sidebar.button("æ¥ç"):
                logs = get_log_text(file_selected_path,n_lines=n_lines)
                st.text('æ¥å¿è·¯å¾ï¼'+file_selected_path)
                st.write(logs)
        else:
            st.info(f'è¯·éæ©æä»¶')

if __name__ == '__main__':
    app_main()

