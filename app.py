import random
import pandas as pd
import streamlit as st

def job_order_simulation():
    st.set_page_config(page_title="Job Order Simulation", layout="wide")
    st.title("📊 Job Order Simulation using Probability Distribution")

    with st.sidebar:
        st.header("⚙️ Simulation Configuration")
        num_jobs = st.number_input("Enter the number of job orders", min_value=1, step=1)
        run_sim = st.checkbox("Ready to simulate?")

    jobs = []
    frequencies = []
    processing_times = []

    if num_jobs and run_sim:
        st.subheader("Step 1: Enter Job Order Details")

        with st.form("job_input_form"):
            for i in range(int(num_jobs)):
                st.markdown(f"### 🧾 Job {i + 1}")
                cols = st.columns(3)
                job_name = cols[0].text_input(f"Job name {i + 1}", key=f"name_{i}")
                freq = cols[1].number_input(f"Frequency", min_value=1, key=f"freq_{i}")
                proc_time = cols[2].number_input(f"Processing time (min)", min_value=1, key=f"time_{i}")

                jobs.append(job_name)
                frequencies.append(freq)
                processing_times.append(proc_time)

            submitted = st.form_submit_button("🔁 Generate Simulation")

        if submitted:
            st.subheader("Step 2: Generated Job Table with Probabilities")

            df = pd.DataFrame({
                'Job Order': jobs,
                'Frequency': frequencies,
                'Processing Time': processing_times
            })

            total_freq = df['Frequency'].sum()
            df['Probability'] = df['Frequency'] / total_freq
            df['Cumulative Probability'] = df['Probability'].cumsum()

            df['Random Start'] = (df['Cumulative Probability'].shift(1, fill_value=0) * 100).round().astype(int)
            df['Random End'] = (df['Cumulative Probability'] * 100).round().astype(int) - 1
            df.at[df.index[-1], 'Random End'] = 99

            st.dataframe(df[['Job Order', 'Frequency', 'Processing Time', 'Probability', 'Cumulative Probability', 'Random Start', 'Random End']])

            st.subheader("Step 3: Run Simulations")
            num_simulations = st.number_input("Number of simulations to run", min_value=1, value=20, step=1)
            run_button = st.button("🎲 Run Simulation")

            if run_button:
                random_numbers = [random.randint(0, 99) for _ in range(num_simulations)]

                sequence = []
                job_processing_times = []
                makespan = 0

                for rand_num in random_numbers:
                    mask = (df['Random Start'] <= rand_num) & (rand_num <= df['Random End'])
                    job = df.loc[mask, 'Job Order'].values[0] if any(mask) else 'Unknown'
                    sequence.append(job)
                    proc_time = df.loc[df['Job Order'] == job, 'Processing Time'].values[0]
                    job_processing_times.append(proc_time)
                    makespan += proc_time

                results_df = pd.DataFrame({
                    'Random Number': random_numbers,
                    'Job Order': sequence,
                    'Processing Time': job_processing_times
                })

                st.subheader("📋 Simulation Results")
                st.dataframe(results_df)

                st.subheader("🧮 Job Order Sequence")
                st.write(" → ".join(sequence))

                st.success(f"✅ Total Makespan Time: **{makespan} minutes**")

                with st.expander("📈 Probability Table with Full Data"):
                    prob_display = df.copy()
                    prob_display['Probability'] = prob_display['Probability'].map('{:.4f}'.format)
                    prob_display['Cumulative Probability'] = prob_display['Cumulative Probability'].map('{:.4f}'.format)
                    st.dataframe(prob_display)

if __name__ == "__main__":
    job_order_simulation()
