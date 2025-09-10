import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta

genai.configure(api_key="AIzaSyBm1B4u9uwVA8colQxb3ZehK1Wl9v5CLGs")
model = genai.GenerativeModel("gemini-2.5-flash")


#Budget_Planner
def get_saving_tips(income, expenses):
    prompt = f"""
    I earn ₹{income:.2f} per month and spend ₹{expenses:.2f}. 
    Give me one smart, practical saving tip tailored to this situation. 
    Keep it friendly and beginner-friendly.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Oops! Couldn't fetch a tip right now. Error: {e}"


def budget_planner():
    st.header("💰Budget Planer")
    st.markdown("Let’s help you understand where your money is going and how much you’re saving each month.")
    income = st.number_input("📥Enter your monthly income here:", min_value=0.0, format="%.2f")
    expenses = st.number_input("📥Enter your monthly expenses here:", min_value=0.0, format="%.2f")

    st.markdown("### 🧾 Optional: Expense Breakdown")
    rent = st.number_input("🏠 Rent/Mortgage", min_value=0.0, format="%.2f")
    groceries = st.number_input("🛒 Groceries", min_value=0.0, format="%.2f")
    transport = st.number_input("🚗 Transport", min_value=0.0, format="%.2f")
    others = st.number_input("📦 Other Expenses", min_value=0.0, format="%.2f")

    if "ai_tip" not in st.session_state:
        st.session_state.ai_tip = None

    if st.button("📊Calculate Budget"):
        total_breakdown = rent + groceries + transport + others
        if total_breakdown > 0:
            expenses = total_breakdown

        balance = income - expenses

        st.markdown("---")
        if balance > 0:
            st.success(f"🎉 Great job! You’re saving ₹{balance:,.2f} this month.")
            st.progress(min(balance / income, 1.0))
            with st.spinner("Thinking of a smart saving tips for you ..."):
                st.session_state.ai_tip = get_saving_tips(income,expenses)

        elif balance == 0:
            st.warning("⚖️ You’re breaking even. Consider trimming some expenses to build savings.")
            st.session_state.ai_tip = None
        else:
            st.error(f"🚨 You’re overspending by ₹{abs(balance):,.2f}. Let’s fix that together.")
            st.session_state.ai_tip = None

        if st.session_state.ai_tip:
            st.markdown("### 🧠 Smart Saving Tip")
            st.info(st.session_state.ai_tip)


    st.markdown("---")
    st.markdown("✅ Next Steps:")
    st.button("📅 Plan Savings Goal")
    st.button("📘 View Financial Tips")


#Saving_Goal-Planner
def get_motivation_tip(goal, monthly_savings):
    prompt = f"""
    I want to save ₹{goal:.2f} and can save ₹{monthly_savings:.2f} per month.
    Give me a short, motivating tip to stay consistent with my savings.
    Keep it friendly and beginner-focused.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Couldn't fetch a tip right now. Error: {e}"

def savings_goal_planner():
    st.header("🎯 Savings Goal Planner")
    st.markdown("Set your goal, track your progress, and stay motivated to reach it!")

    goal = st.number_input("💰 Your savings goal (₹):", min_value=0.0, format="%.2f")
    monthly_savings = st.number_input("📥 Monthly savings amount (₹):", min_value=0.0, format="%.2f")

    st.markdown("### 🧾 Optional: Where will your savings come from?")
    salary = st.number_input("👨‍💼 From salary", min_value=0.0, format="%.2f")
    side_income = st.number_input("🛍️ From side income", min_value=0.0, format="%.2f")
    cutbacks = st.number_input("✂️ From expense cutbacks", min_value=0.0, format="%.2f")

    if "strategy" not in st.session_state:
        st.session_state.strategy = None

    if st.button("📊 Show Savings Plan"):
        total_sources = salary + side_income + cutbacks
        if total_sources > 0:
            monthly_savings = total_sources

        if monthly_savings > 0:
            months = goal / monthly_savings
            completion_date = datetime.today() + timedelta(days=months * 30)

            st.success(f"✅ You’ll reach ₹{goal:,.2f} in approx. {months:.1f} months.")
            st.info(f"🎯 Estimated completion: {completion_date.strftime('%B %Y')}")
            st.progress(min(monthly_savings / goal, 1.0))
            with st.spinner("Crafting your saving strategy ..."):
                st.session_state.strategy = get_motivation_tip(goal, monthly_savings)
        else:
            st.warning("Please enter a valid monthly savings amount.")
            st.session_state.strategy = None

        if st.session_state.strategy:
            st.markdown("### 🧠 Saving Strategy")
            st.info(st.session_state.strategy)


    st.markdown("---")
    st.markdown("📘 Suggested Strategies:")
    st.button("📅 Automate monthly transfers")
    st.button("📦 Use a separate savings account")
    st.button("📈 Track progress weekly")

    
    
#Financial_Tips
def financial_tips():
    st.header("💡 Financial Tips")
    st.markdown("Ask for beginner-friendly advice on saving, budgeting, debt, or anything money-related.")

    # Optional dropdown for guided topics
    popular_topics = ["Saving Money", "Budgeting", "Debt Management", "Emergency Fund", "Smart Spending"]
    selected_topic = st.selectbox("📚 Or choose a topic:", popular_topics)
    custom_topic = st.text_input("🔍 Or type your own:", placeholder="e.g., investing basics, credit score tips")

    topic = custom_topic if custom_topic else selected_topic

    # Session state for storing tip and checklist
    if "tip" not in st.session_state:
        st.session_state.tip = None
    if "checklist" not in st.session_state:
        st.session_state.checklist = []

    if st.button("🧠 Get Tips") and topic:
        with st.spinner("Thinking of the best advice for you..."):
            prompt = f"""
            You are a friendly financial advisor helping beginners build smart money habits.
            Give 3 practical, beginner-friendly financial tips on the topic: {topic}.
            Each tip should:
            - Be short and clear (10–15 sentences max)
            - Include a relatable example or analogy
            - End with a motivational nudge or call to action

            Then, generate a checklist of 3–5 simple actions the user can take this week to apply those tips.
            Use a warm, encouraging tone. Avoid jargon. Make the user feel confident and capable.
            """

            response = model.generate_content(prompt)
            full_text = response.text

            # Split tips and checklist
            if "Checklist:" in full_text:
                tips, checklist_raw = full_text.split("Checklist:", 1)
                checklist_items = [item.strip("-• ") for item in checklist_raw.strip().split("\n") if item.strip()]
            else:
                tips = full_text
                checklist_items = []

            st.session_state.tip = tips
            st.session_state.checklist = checklist_items

    # Display tips
    if st.session_state.tip:
        st.markdown("### 🧾 Your Tips")
        st.info(st.session_state.tip)

    # Display checklist
    if st.session_state.checklist:
        st.markdown("### ✅ Weekly Action Plan")
        for item in st.session_state.checklist:
            st.checkbox(item)

    # Reset button
    if st.session_state.tip and st.button("🔄 Reset"):
        st.session_state.tip = None
        st.session_state.checklist = []



#Debt_Payoff_Calculator
def get_debt_strategy(debt_amount, monthly_payment):
    prompt = f"""
    I have ₹{debt_amount:.2f} in debt and can pay ₹{monthly_payment:.2f} per month.
    Give me 3 practical, beginner-friendly strategies to stay consistent and pay off this debt faster.
    Include one motivational tip at the end. Keep it warm, clear, and jargon-free.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Couldn't fetch strategy. Error: {e}"

# Debt Payoff Calculator UI
def debt_payoff_calculator():
    st.header("💳 Debt Payoff Calculator")
    st.markdown("Calculate how long it will take to pay off your debt and get smart strategies to stay on track.")

    debt_amount = st.number_input("💰 Total Debt Amount (₹)", min_value=0.0, format="%.2f")
    monthly_payment = st.number_input("📤 Monthly Payment (₹)", min_value=0.0, format="%.2f")

    if "strategy" not in st.session_state:
        st.session_state.strategy = None

    if st.button("📊 Calculate Payoff Time"):
        if monthly_payment > 0:
            months = debt_amount / monthly_payment
            completion_date = datetime.today() + timedelta(days=months * 30)

            st.success(f"✅ You’ll be debt-free in approximately {months:.1f} months.")
            st.info(f"🎯 Estimated completion: {completion_date.strftime('%B %Y')}")
           
            with st.spinner("Crafting your payoff strategy..."):
                st.session_state.strategy = get_debt_strategy(debt_amount, monthly_payment)
        else:
            st.warning("⚠️ Please enter a valid monthly payment.")
            st.session_state.strategy = None

    # Show AI strategy
        if st.session_state.strategy:
            st.markdown("### 🧠 Smart Payoff Strategy")
            st.info(st.session_state.strategy)

    # Reset button
    if st.session_state.strategy and st.button("🔄 Reset Strategy"):
        st.session_state.strategy = None




#Main.py
st.set_page_config(page_title="FinMate", page_icon="💼", layout="wide")


st.markdown("""
    <style>
        .center-text {text-align: center;}
        .small-text {font-size: 14px; text-align: center; color: gray;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.header("📂 Select a Feature")

PAGES = {
    "🏠 Home": "Home",
    "📊 Budget Planner": budget_planner,
    "🎯 Savings Goal Planner": savings_goal_planner,
    "💡 Financial Tips": financial_tips,
    "💳 Debt Payoff Calculator": debt_payoff_calculator,
}

selected = st.sidebar.radio("Go to:", list(PAGES.keys()))


if selected == "🏠 Home":
    st.markdown("<h1 class='center-text' style='color:#4CAF50;'>Welcome to FinMate 💼</h1>", unsafe_allow_html=True)
    st.markdown("<p class='center-text'>Your all-in-one personal finance assistant</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🌟 What FinMate Offers")
    st.markdown("""
    Whether you're budgeting, saving, tackling debt, or just looking for smart money tips — you're in the right place.

    **Core Features:**
    - 📊 Budget Planner: Track income and expenses
    - 🎯 Savings Goal Planner: Set goals and stay motivated
    - 💡 Financial Tips: Get AI-powered advice tailored to you
    - 💳 Debt Payoff Calculator: Plan your way to financial freedom
    """)

    col1, col2, col3 = st.columns([1,2,1])  
    with col2:
        st.image(
        "Finmate_logo.png",use_container_width=False,
        caption="Smart finance starts here"
    )

    st.markdown("---")

    st.markdown("### 🚀 Quick Start")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("👉 Use the sidebar to access:")
        st.markdown("- 📊 **Budget Planner**")
        st.markdown("- 🎯 **Savings Goal Planner**")

    with col2:
        st.markdown("👉 And also:")
        st.markdown("- 💡 **Financial Tips**")
        st.markdown("- 💳 **Debt Payoff Calculator**")

    st.markdown("---")
    st.markdown("<p class='small-text'>Built by Shoaib | Powered by Gemini Pro</p>", unsafe_allow_html=True)

else:
    page_func = PAGES[selected]
    if callable(page_func):
        page_func()