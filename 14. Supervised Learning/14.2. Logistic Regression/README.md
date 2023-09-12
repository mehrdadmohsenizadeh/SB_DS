<h1> Introduction </h1>

* This notebook is intended to be a general reference that can be used when working on building models for practical applications that are modeled as classification problems. As such, it contains general data science and programming patterns that can be used in many (classification) scenarios. However, it also contains some comments that are applicable to general supervised problems (i.e., regression and classification).

* Having said this, the work that is required from students consists of short exercises marked as <b>Checkup Exercise Set I, II, III, IV</b>.

  1. We recommend that you first read the whole notebook to understand the general context (i.e., classification problems) and then work on giving specific answers to the exercises.

  2. After this, we recommend that you continue using this notebook as a reference when working on other classification problems (e.g., in your capstone projects and other case studies), and consider how/if the patterns presented here can be applied to the specific practical problem at hand.

  3. Do not hesitate to discuss any questions that you might have about this notebook with your mentor and the Springboard community.

<h1> Heart Disease Dataset </h1>
  The <a href="https://archive.ics.uci.edu/dataset/45/heart+disease">original database</a> contains $76$ attributes, but all published experiments refer to using a subset of $14$ of them.  In particular, the Cleveland database is the only one that has been used by ML researchers to date. The <code>goal</code> field refers to the presence of heart disease in the patient.  It is integer valued from <code>0</code> (no presence) to <code>4</code>. Experiments with the Cleveland database have concentrated on simply attempting to distinguish presence (values <code>1</code>, <code>2</code>, <code>3</code>, <code>4</code>) from absence (value <code>0</code>).

<h2> Notes </h2>

* There are multiple datasets available at the original database link. This study starts with the processed Cleveland data (<a href="https://colab.research.google.com/corgiredirector?site=https%3A%2F%2Farchive.ics.uci.edu%2Fml%2Fmachine-learning-databases%2Fheart-disease%2Fprocessed.cleveland.data">UCI heart disease Cleveland</a>).

* The column names have been updated to be more self-explanatory (e.g., the <code>goal</code> column has been updated to <code>heart_disease</code>. Now, instead of having four distinct values, it exclusively includes <code>0=False</code> and <code>1=True</code> values.)

* A small number of observations with missing one or more values has been removed.

<h2> Overview </h2>

<div class="custom-table-container">
  <table>
    <tr>
      <th>Feature</th>
      <th>Description</th>
      <th>Range</th>
      <th>Notes</th>
    </tr>
    <tr>
      <td><code>age_yr</code></td>
      <td>Age of the patient in years</td>
      <td><code>(0, 200)</code></td>
      <td>The age of the patient in years. Age can be a significant factor in assessing the risk of heart disease, as the likelihood of certain cardiac conditions tends to increase with age.</td>
    </tr>
    <tr>
      <td><code>sex_M_F</code></td>
      <td>Sex of the patient</td>
      <td><code>0</code> or <code>1</code></td>
      <td>Indicates the patient's gender, with 1 typically representing males and 0 representing females. Gender can play a role in understanding heart disease risk, as there are some gender-specific differences in cardiac conditions.</td>
    </tr>
    <tr>
      <td><code>chest_pain_value</code></td>
      <td>Chest pain severity.</td>
      <td><code>0</code>, <code>1</code>, <code>2</code>, <code>3</code></td>
      <td>Describes the severity of chest pain experienced by the patient. Chest pain can be indicative of various heart-related issues, and the severity helps assess its seriousness.</td>
    </tr>
    <tr>
      <td><code>resting_BP_mm_Hg</code></td>
      <td>Resting blood pressure</td>
      <td>
        <code>< 90</code><br>(Low)<br><br>
        <code>(90, 119)</code><br>(Normal)<br><br>
        <code>(120, 139)</code><br>(Prehypertension)<br><br>
        <code>(140, 159)</code><br>(Hypertension 1)<br><br>
        <code>> 160</code><br>(Hypertension 2)
      </td>
      <td>Represents the patient's resting blood pressure measured in millimeters of mercury <code>(mm Hg)</code>. High blood pressure is a common risk factor for heart disease.</td>
    </tr>
    <tr>
      <td><code>cholesterol_mg_dl</code></td>
      <td>Cholesterol level</td>
      <td>
        <code>< 200</code><br>(Desirable)<br><br>
        <code>(200, 239)</code><br>(Borderline High)<br><br>
        <code>> 240</code><br>(High)
      </td>
      <td>Indicates the patient's cholesterol level in milligrams per deciliter <code>(mg/dl)</code>. Elevated cholesterol levels can contribute to the development of atherosclerosis, a leading cause of heart disease.</td>
    </tr>
    <tr>
      <td><code>fasting_blood_sugar_high</code></td>
      <td>Fasting blood sugar</td>
      <td><code>0</code> or <code>1</code></td>
      <td>A binary indicator of whether the patient's fasting blood sugar is high. High fasting blood sugar levels may be associated with diabetes, which can increase the risk of heart disease.</td>
    </tr>
    <tr>
      <td><code>ECG_value</code></td>
      <td>Electrocardiogram result</td>
      <td>
      <code>0</code><br>(Normal)<br><br>
      <code>1</code><br>(Mild Abnormal)<br><br>
      <code>2</code><br>(Severe Abnormal)
      </td>
      <td>Represents the result or value from an Electrocardiogram (ECG) test. An ECG measures the electrical activity of the heart and can reveal abnormalities in heart rhythm.</td>
    </tr>
    <tr>
      <td><code>max_HR</code></td>
      <td>Maximum heart rate</td>
      <td>Numeric</td>
      <td>Indicates the maximum heart rate achieved by the patient during a stress test or exercise. This information can be relevant for assessing cardiac fitness.</td>
    </tr>
    <tr>
      <td><code>exercise_angina</code></td>
      <td>Exercise-induced angina</td>
      <td><code>0</code> or <code>1</code></td>
      <td>A binary indicator of whether the patient experienced angina (chest pain) during exercise. Angina during exercise can be a symptom of coronary artery disease.</td>
    </tr>
    <tr>
      <td><code>ST_depresssion_exercise</code></td>
      <td>ST depression during exercise</td>
      <td>Numeric</td>
      <td>Reflects the degree of ST segment depression observed on an ECG during exercise compared to rest. ST depression can be a sign of myocardial ischemia.</td>
    </tr>
    <tr>
      <td><code>ST_slope_peak</code></td>
      <td>ST slope at peak exercise</td>
      <td>Numeric</td>
      <td>Describes the slope of the ST segment on an ECG at the peak of exercise. It provides additional information about heart function during exercise.</td>
    </tr>
    <tr>
      <td><code>number_vessels_involved</code></td>
      <td>Number of vessels involved</td>
      <td>Numeric</td>
      <td>Indicates the number of major blood vessels involved or affected. Multiple vessel involvement can be indicative of more severe coronary artery disease.</td>
    </tr>
    <tr>
      <td><code>defect_diag</code></td>
      <td>Heart defect diagnosis</td>
      <td>Numeric</td>
      <td>Specifies the type of heart defect or diagnosis. This feature can help classify specific cardiac conditions or abnormalities.</td>
    </tr>
    <tr>
      <td><code>heart_disease</code></td>
      <td>Heart disease diagnosis</td>
      <td><code>0</code> or <code>1</code></td>
      <td>A binary indicator that reveals whether the patient has been diagnosed with heart disease. This is the target variable in many heart disease prediction models, with 1 indicating the presence of heart disease and 0 indicating its absence.</td>
    </tr>
  </table>
</div>
