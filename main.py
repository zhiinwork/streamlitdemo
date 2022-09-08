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
    st.set_page_config(page_title="Hello",page_icon="👋",)
    st.write("# Log数据分析和绘图示例")
    st.sidebar.success("上方选择功能，下方配置参数")
    st.title("数据加载和简单分析")
    if st.sidebar.checkbox('选择数据源'):
        file_folder = st.sidebar.text_input('文件夹', value="data")
        data_file_list = list_files(file_folder, 'csv')
        if len(data_file_list) ==0:
            st.warning(f'此路径无可用数据集')
        else:
            file_selected = st.sidebar.selectbox(
                '选择文件', data_file_list)
            file_selected_path = concat_file_path(file_folder, file_selected)
            nrows = st.sidebar.number_input('读取行数(-1表示全部读出)', value=-1)
            n_rows_str = '全部' if nrows == -1 else str(nrows)
            st.info(f'已选择文件：{file_selected_path}，读取行数为{n_rows_str}')
    else:
        file_selected_path = None
        nrows = 100
        st.warning(f'当前选择文件为空，请选择。')

    if st.sidebar.checkbox('绘图'):
        if file_selected_path is not None:
            df = load_csv(file_selected_path, nrows)
            n_lines =st.sidebar.slider(label='绘制范围',min_value=3,max_value=len(df),value=len(df))
            try:
                cols = df.columns.to_list()
                axis_x = st.sidebar.selectbox('x轴', cols, index=0)
                axis_y = st.sidebar.selectbox('y轴', cols, index=1)

                tab1, tab2, tab3 = st.tabs(["折线图", "散点图", "双参数散点"])
                with tab1:
                    st.header("这里是折线图")
                    st.line_chart(df[:n_lines],x=axis_x,y=axis_y)
                with tab2:
                    st.header("这里是散点图")
                    fig = plt.figure()
                    # ax = fig.add_subplot(111)
                    plt.scatter(df[:n_lines][axis_x], df[:n_lines][axis_y])
                    st.pyplot(fig)
                with tab3:
                    st.header("双散点图")
                    axis_y2 = st.sidebar.selectbox('y轴2', cols, index=2)
                    fig = plt.figure()
                    # ax = fig.add_subplot(111)
                    plt.plot(df[:n_lines][axis_x], df[:n_lines][axis_y], 'o', color='orange')
                    plt.plot(df[:n_lines][axis_x], df[:n_lines][axis_y2], 'x', color='blue')
                    plt.legend()
                    st.pyplot(fig)

                st.dataframe(df[:n_lines])
            except BaseException:
               st.sidebar.warning(f'数据格式无法正确读取')
               target_col = None

    if st.sidebar.checkbox('汇总分析'):
        if file_selected_path is not None:
            if st.sidebar.button('生成报告'):
                df = load_csv(file_selected_path, nrows)
                st.write('处理中，比较慢，稍候……')
                pr = ProfileReport(df, explorative=True)
                st_profile_report(pr)
        else:
            st.info(f'请选择文件')

    if st.sidebar.checkbox('显示文本格式'):
        if file_selected_path is not None:
            n_lines =st.sidebar.slider(label='行数',min_value=3,max_value=50)
            if st.sidebar.button("查看"):
                logs = get_log_text(file_selected_path,n_lines=n_lines)
                st.text('日志路径：'+file_selected_path)
                st.write(logs)
        else:
            st.info(f'请选择文件')

if __name__ == '__main__':
    app_main()

