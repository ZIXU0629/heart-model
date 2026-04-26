import os
os.system('python -m pip install streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple')
import streamlit as st
import pandas as pd
import joblib

# 1. 页面标题
st.title("临床心脏病风险预测系统")
st.write("请输入患者生理指标：")

# 2. 加载模型
model = joblib.load('heart_disease_model.pkl')

# 3. 创建输入表单（根据你的 heart.csv 特征）
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("年龄 (Age)", value=50)
    sex = st.selectbox("性别 (Sex)", options=[("男", 1), ("女", 0)], format_func=lambda x: x[0])[1]
    resting_bp = st.number_input("静息血压 (RestingBP)", value=130)
    cholesterol = st.number_input("胆固醇 (Cholesterol)", value=200)

with col2:
    fasting_bs = st.selectbox("空腹血糖 > 120 (FastingBS)", options=[("是", 1), ("否", 0)], format_func=lambda x: x[0])[1]
    max_hr = st.number_input("最大心率 (MaxHR)", value=150)
    ex_angina = st.selectbox("运动诱发心绞痛 (ExerciseAngina)", options=[("是", 1), ("否", 0)], format_func=lambda x: x[0])[1]
    oldpeak = st.number_input("ST段压低 (Oldpeak)", value=1.0)

# 4. 预测逻辑
if st.button("开始评估"):
    # 构建 DataFrame，顺序必须与训练时一致
    input_data = pd.DataFrame([[age, sex, resting_bp, cholesterol, fasting_bs, max_hr, ex_angina, oldpeak]],
                              columns=['Age', 'Sex', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'ExerciseAngina', 'Oldpeak'])
    
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.error("结果：高风险。建议进行进一步临床检查。")
    else:
        st.success("结果：低风险。")
