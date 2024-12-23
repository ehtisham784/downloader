import pandas as pd
import numpy as np
from random import choice, randint, uniform
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel

# Random departments, job roles, and access levels
departments = ['IT', 'HR', 'Finance', 'Marketing', 'Legal']
job_roles = ['IT Specialist', 'HR Manager', 'Finance Analyst', 'Marketing Coordinator', 'Network Engineer', 'Legal Advisor']
access_levels = ['Low', 'Medium', 'High']

# Function to generate random date within a year range
def random_date(start, end):
    return start + timedelta(days=randint(0, (end - start).days))

# Generate Data
np.random.seed(42)
n = 150  # Number of employees
employee_ids = [f"{i+1:03d}" for i in range(n)]
departments_col = [choice(departments) for _ in range(n)]
training_status = [randint(0, 1) for _ in range(n)]
pre_training_scores = [round(uniform(30, 70), 2) for _ in range(n)]
post_training_scores = [round(pre_score + uniform(10, 30), 2) if status == 1 else None for pre_score, status in zip(pre_training_scores, training_status)]
training_dates = [random_date(datetime(2023, 1, 1), datetime(2024, 1, 1)) if status == 1 else None for status in training_status]
incidents = [randint(0, 1) for _ in range(n)]
incident_severity = [randint(1, 3) if incident == 1 else None for incident in incidents]
duration_after_training = [randint(1, 12) if status == 1 else randint(1, 12) for status in training_status]
job_roles_col = [choice(job_roles) for _ in range(n)]
access_levels_col = [choice(access_levels) for _ in range(n)]
post_training_incident_frequency = [randint(0, 2) if incident == 1 else 0 for incident in incidents]

# Create DataFrame
data = {
    'Employee ID': employee_ids,
    'Department': departments_col,
    'Training Status': training_status,
    'Training Date': training_dates,
    'Pre-Training Awareness Score': pre_training_scores,
    'Post-Training Awareness Score': post_training_scores,
    'Insider Threat Incident': incidents,
    'Incident Severity': incident_severity,
    'Duration After Training (Months)': duration_after_training,
    'Job Role': job_roles_col,
    'Access Level': access_levels_col,
    'Post-Training Incident Frequency': post_training_incident_frequency
}

df = pd.DataFrame(data)

# Show the first few rows
df.head()

# Save as CSV if needed
df.to_csv('cybersecurity_training_effectiveness.csv', index=False)



# Set up seaborn style
sns.set(style="whitegrid")

# 1. Training Effectiveness (Pre vs Post Training Awareness Score)
# Reshape the data into long format using melt
df_long = pd.melt(df, id_vars=['Department'], value_vars=['Pre-Training Awareness Score', 'Post-Training Awareness Score'],
                  var_name='Training Phase', value_name='Awareness Score')

plt.figure(figsize=(10, 6))
sns.barplot(x='Department', y='Awareness Score', hue='Training Phase', data=df_long, estimator=np.mean, ci=None)
plt.title('Training Effectiveness by Department')
plt.ylabel('Average Awareness Score')
plt.xlabel('Department')
plt.legend(title='Training Phase')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 2. Insider Threat Incidents by Severity
# Set the Seaborn style
sns.set(style='whitegrid')

# Create the count plot
plt.figure(figsize=(10, 6))
ax = sns.countplot(x='Department', hue='Incident Severity', data=df, palette='coolwarm')

# Add title and labels
plt.title('Insider Threat Incidents by Severity and Department', fontsize=14)
plt.ylabel('Number of Incidents', fontsize=12)
plt.xlabel('Department', fontsize=12)

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)

# Add count labels on top of the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=12, color='black', xytext=(0, 5),
                textcoords='offset points')

# Show the plot
plt.tight_layout()
plt.show()

# 3. Correlation of Training Status vs Insider Threat Incidents
plt.figure(figsize=(10, 6))
sns.countplot(x='Training Status', hue='Insider Threat Incident', data=df)
plt.title('Training Status vs Insider Threat Incidents')
plt.ylabel('Count of Incidents')
plt.xlabel('Training Status (0 = Not Trained, 1 = Trained)')
plt.tight_layout()
plt.show()

# 4. Post-Training Awareness Score vs Post-Training Incident Frequency
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Post-Training Awareness Score', y='Post-Training Incident Frequency', data=df)
plt.title('Post-Training Awareness Score vs Post-Training Incident Frequency')
plt.xlabel('Post-Training Awareness Score')
plt.ylabel('Post-Training Incident Frequency')
plt.tight_layout()
plt.show()

# 5. Duration After Training vs Insider Threat Incidents
plt.figure(figsize=(10, 6))
sns.histplot(df[df['Training Status'] == 1]['Duration After Training (Months)'], kde=True, color="blue", label="Trained Employees", stat="density")
sns.histplot(df[df['Training Status'] == 0]['Duration After Training (Months)'], kde=True, color="red", label="Non-Trained Employees", stat="density")
plt.title('Duration After Training vs Insider Threat Incidents')
plt.xlabel('Duration After Training (Months)')
plt.ylabel('Density')
plt.legend()
plt.tight_layout()
plt.show()

# 6. Boxplot of Post-Training Incident Frequency by Department
plt.figure(figsize=(10, 6))
sns.boxplot(x='Department', y='Post-Training Incident Frequency', data=df)
plt.title('Post-Training Incident Frequency by Department')
plt.ylabel('Post-Training Incident Frequency')
plt.xlabel('Department')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 7. Correlation Heatmap (Pre-Training, Post-Training, Incident Frequency)
corr = df[['Pre-Training Awareness Score', 'Post-Training Awareness Score', 'Post-Training Incident Frequency', 'Duration After Training (Months)']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()

grouped = df.groupby('Department').agg({
    'Insider Threat Incident': 'sum',
    'Pre-Training Awareness Score': 'mean',
    'Post-Training Awareness Score': 'mean',
    'Post-Training Incident Frequency': 'mean'
}).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='Department', y='Post-Training Incident Frequency', data=grouped, palette='coolwarm')
plt.title('Average Post-Training Incident Frequency by Department')
plt.xlabel('Department')
plt.ylabel('Average Post-Training Incident Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 1. One-Sample T-Test: Compare Pre-Training Scores to a Population Mean (e.g., 50)
t_stat_one, p_val_one = ttest_1samp(df['Pre-Training Awareness Score'], 50)
print(f"One-Sample T-Test: t-statistic={t_stat_one}, p-value={p_val_one}")

# 2. Independent T-Test: Compare Pre-Training Scores of Trained vs Non-Trained Employees
trained_scores = df[df['Training Status'] == 1]['Pre-Training Awareness Score']
non_trained_scores = df[df['Training Status'] == 0]['Pre-Training Awareness Score']
t_stat_ind, p_val_ind = ttest_ind(trained_scores, non_trained_scores)
print(f"Independent T-Test: t-statistic={t_stat_ind}, p-value={p_val_ind}")

# 3. Paired T-Test: Compare Pre and Post-Training Awareness Scores for Trained Employees
paired_scores = df.dropna(subset=['Post-Training Awareness Score'])
t_stat_paired, p_val_paired = ttest_rel(paired_scores['Pre-Training Awareness Score'], paired_scores['Post-Training Awareness Score'])
print(f"Paired T-Test: t-statistic={t_stat_paired}, p-value={p_val_paired}")

# --- Visualizations ---
sns.set(style="whitegrid")

# 1. Training Effectiveness by Department
df_long = pd.melt(df, id_vars=['Department'], value_vars=['Pre-Training Awareness Score', 'Post-Training Awareness Score'],
                  var_name='Training Phase', value_name='Awareness Score')

plt.figure(figsize=(10, 6))
sns.barplot(x='Department', y='Awareness Score', hue='Training Phase', data=df_long, estimator=np.mean, ci=None)
plt.title('Training Effectiveness by Department')
plt.ylabel('Average Awareness Score')
plt.xlabel('Department')
plt.legend(title='Training Phase')
plt.tight_layout()
plt.show()

# 2. T-Test Results: Visualizing Comparison
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# One-Sample T-Test Visualization
sns.violinplot(y=df['Pre-Training Awareness Score'], ax=axes[0], color='skyblue')
axes[0].axhline(50, color='red', linestyle='--')
axes[0].set_title('One-Sample T-Test (Mean = 50)')
axes[0].set_ylabel('Pre-Training Awareness Score')

# Independent T-Test Visualization
sns.boxplot(data=[trained_scores, non_trained_scores], ax=axes[1])
axes[1].set_xticklabels(['Trained', 'Non-Trained'])
axes[1].set_title('Independent T-Test: Trained vs Non-Trained')
axes[1].set_ylabel('Pre-Training Awareness Score')

# Paired T-Test Visualization
sns.boxplot(data=[paired_scores['Pre-Training Awareness Score'], paired_scores['Post-Training Awareness Score']], ax=axes[2])
axes[2].set_xticklabels(['Pre-Training', 'Post-Training'])
axes[2].set_title('Paired T-Test: Pre vs Post Training')
axes[2].set_ylabel('Awareness Score')

plt.tight_layout()
plt.show()
