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
      <th>Notes</th>
    </tr>
    <tr>
      <td><code>age_yr</code></td>
      <td>Age of the patient in years</td>
      <td>The age of the patient in years. Age can be a significant factor in assessing the risk of heart disease, as the likelihood of certain cardiac conditions tends to increase with age.</td>
    </tr>
    <tr>
      <td><code>sex_M_F</code></td>
      <td>Sex of the patient</td>
      <td>A binary (<code>0</code> or <code>1</code>) indicator representing the gender of the patient (typically, <code>0</code> means females and <code>1</code> represents males. Gender can play a role in understanding heart disease risk, as there are some gender-specific differences in cardiac conditions.</td>
    </tr>
    <tr>
      <td><code>chest_pain_value</code></td>
      <td>Chest pain severity.</td>
      <td>
        Describes the severity of chest pain experienced by the patient. Chest pain can be indicative of various heart-related issues, and the severity helps assess its seriousness. Here's a description of each of the four distinct values:<br><br>
      <code>1</code> <b>Typical Angina:</b><br>Typical angina is chest pain or discomfort that occurs when the heart muscle doesn't receive enough oxygen-rich blood. It is often described as a tight, squeezing, or pressure-like sensation in the chest. This type of chest pain is usually triggered by physical activity or emotional stress and tends to improve with rest or medication.<br><br>

<code>2</code> <b>Atypical Angina:</b><br>Atypical angina refers to chest pain that doesn't fit the classic pattern of typical angina. It may present with different or less specific symptoms and can be challenging to diagnose. Atypical angina may still be related to heart problems but is not as characteristic as typical angina.<br><br>

<code>3</code> <b>Non-Anginal Pain:</b><br> Non-anginal chest pain is chest discomfort or pain that is not related to the heart. It can have various causes, such as musculoskeletal issues, gastrointestinal problems, or anxiety. This type of chest pain is typically not associated with coronary artery disease.<br><br>

<code>4</code> <b>Asymptomatic:</b><br> Patients with a value of 4 in the "chest_pain_value" column are considered asymptomatic, meaning they do not experience any chest pain or discomfort. This category indicates that the patient does not report chest pain as a symptom.
      </td>
    </tr>
    <tr>
      <td><code>resting_BP_mm_Hg</code></td>
      <td>Resting blood pressure</td>
      <td>
      Represents the patient's resting blood pressure measured in millimeters of mercury or <code>(mmHg</code>. High blood pressure is a common risk factor for heart disease.<br><br>
      <code>< 90</code> <b>Low:</b><br><br>
      <code>(90, 119)</code> <b>Normal:</b><br><br>
      <code>(120, 139)</code> <b>Prehypertension:</b><br><br>
      <code>(140, 159)</code> <b>Hypertension (stage 1):</b><br><br>
      <code>> 160</code> <b>Hypertension (stage 2):</b>
      </td>
    </tr>
    <tr>
      <td><code>cholesterol_mg_dl</code></td>
      <td>Cholesterol level</td>
      <td>
      Indicates the patient's cholesterol level in milligrams per deciliter or <code>mg/dl</code>. Elevated cholesterol levels can contribute to the development of atherosclerosis, a leading cause of heart disease.<br><br>
      <code>< 200</code> <b>Desirable:</b><br><br>
      <code>(200, 239)</code> <b>Borderline High:</b><br><br>
      <code>> 240</code> <b>High:</b>
      </td>
    </tr>
    <tr>
      <td><code>fasting_blood_sugar_high</code></td>
      <td>Fasting blood sugar</td>
      <td>A binary (<code>0</code> or <code>1</code>) indicator of whether the patient's fasting blood sugar is high. High fasting blood sugar levels may be associated with diabetes, which can increase the risk of heart disease.</td>
    </tr>
    <tr>
      <td><code>ECG_value</code></td>
      <td>Electrocardiogram result</td>
      <td>
          Represents the result or value from an Electrocardiogram (ECG) test. An ECG measures the electrical activity of the heart and can reveal abnormalities in heart rhythm.<br><br>
        <code>0</code> <b>Normal ECG</b>:<br>
        P wave, QRS complex, and T wave within normal limits.<br><br>
        <code>1</code>  <b>Abnormal ECG (Mild Abnormality)</b>:<br>
        Minor deviations in waveforms, intervals, or segments.<br><br>
        <code>2</code> <b>Severe Abnormal ECG</b>:<br>
        Significant deviations or abnormalities indicating potential heart issues.
      </td>
    </tr>
    <tr>
      <td><code>max_HR</code></td>
      <td>Maximum heart rate</td>
      <td>Indicates the maximum heart rate in <code>bpm</code> achieved by the patient during a stress test or exercise. This information can be relevant for assessing cardiac fitness.<br><br>During a stress test (also known as an exercise stress test or treadmill test), the goal is to increase the heart rate through physical activity while monitoring the heart's response to stress. The test typically involves walking or running on a treadmill, and the heart rate is continuously monitored using an electrocardiogram (ECG or EKG).<br><br>The test may be terminated if the individual reaches a target heart rate (usually a percentage of their estimated maximum heart rate), experiences symptoms such as chest pain or severe fatigue, or if there are abnormal changes in the ECG that suggest a cardiac issue. The maximum heart rate achieved during the test is an important parameter used in assessing cardiac fitness and diagnosing heart conditions.</td>
    </tr>
    <tr>
      <td><code>exercise_angina</code></td>
      <td>Exercise-induced angina</td>
      <td>A binary (<code>0</code> or <code>1</code>) indicator of whether the patient experienced angina (chest pain) during exercise. Angina during exercise can be a symptom of coronary artery disease.</td>
    </tr>
    <tr>
      <td><code>ST_depresssion_exercise</code></td>
      <td>ST depression during exercise</td>
      <td>Reflects the degree of ST segment depression observed on an ECG during exercise compared to rest. ST depression can be a sign of myocardial ischemia.</td>
    </tr>
    <tr>
      <td><code>ST_slope_peak</code></td>
      <td>ST slope at peak exercise</td>
      <td>
        Describes the slope of the ST segment on an Electrocardiogram (ECG) at the peak of exercise. This feature can provide valuable information about heart function during exercise. Here are the explanations for each of the three distinct values:<br><br>
        <code>1</code><b> Upsloping</b> or <b>Normal:</b><br>An upsloping ST segment indicates that the ST segment on the ECG shows a gradual and positive slope as the heart rate increases during exercise. This pattern is generally considered normal and may not be indicative of significant cardiac abnormalities. It suggests that the heart's blood supply is well-maintained during physical exertion.<br><br>

<code>2</code><b> Flat:</b><br> A flat ST segment means that there is little to no change in the ST segment's elevation during exercise. This can be a less common pattern and might warrant further evaluation. While it may not necessarily indicate a specific issue, it could be a sign of potential cardiac stress or abnormalities that require closer examination.

<code>3</code><b> Downsloping:</b><br> A downsloping ST segment indicates that the ST segment on the ECG shows a negative slope as the heart rate increases during exercise. This pattern can be concerning as it may suggest myocardial ischemia, which is a condition where the heart muscle isn't receiving enough blood supply during exercise. Downsloping ST-segment depression is often considered a significant finding that requires medical attention and further testing.
      </td>
    </tr>
    <tr>
      <td><code>number_vessels_involved</code></td>
      <td>Number of vessels involved</td>
      <td>Indicates the number of major blood vessels involved or affected. Multiple vessel involvement can be indicative of more severe coronary artery disease.</td>
    </tr>
    <tr>
      <td><code>defect_diag</code></td>
      <td>Heart defect diagnosis</td>
      <td>Specifies the type of heart defect or diagnosis. This feature can help classify specific cardiac conditions or abnormalities.</td>
    </tr>
    <tr>
      <td><code>heart_disease</code></td>
      <td>Heart disease diagnosis</td>
      <td>A binary (<code>0</code> or <code>1</code>) indicator that reveals whether the patient has been diagnosed with heart disease. This is the target variable in many heart disease prediction models, with 1 indicating the presence of heart disease and 0 indicating its absence.</td>
    </tr>
  </table>
</div>
