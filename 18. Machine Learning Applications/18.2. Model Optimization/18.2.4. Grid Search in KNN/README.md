# About Dataset
## Context
This dataset is originally from the <b>National Institute of Diabetes and Digestive and Kidney Diseases</b>. The objective of the dataset is to diagnostically predict whether or not a patient has diabetes, based on certain diagnostic measurements included in the dataset. Several constraints were placed on the selection of these instances from a larger database. In particular, all patients here are females at least 21 years old of Pima Indian heritage.

## Content
The datasets consists of several medical predictor variables and one target variable, Outcome. Predictor variables includes the number of pregnancies the patient has had, their BMI, insulin level, age, and so on.

<table>
  <tr>
    <th>Predictor/Target Variables</th>
    <th>Description</th>
    <th>Examples</th>
  </tr>
  <tr>
    <td><b><code>Pregnancies</code></b></td>
    <td>Number of times a patient has been pregnant. Frequent pregnancies can influence glucose tolerance and are a consideration in diabetes studies.</td>
    <td><b><code>0</code></b>, <b><code>1</code></b>, <b><code>2</code></b></td>
  </tr>
  <tr>
    <td><b><code>Glucose</code></b></td>
    <td>Concentration of glucose in the blood after a period of fasting (usually 8 hours). It's a critical measure for diagnosing diabetes, with higher levels potentially indicating diabetes.</td>
    <td><b><code>85</code></b>, <b><code>110</code></b>, <b><code>145</code></b></td>
  </tr>
  <tr>
    <td><b><code>BloodPressure</code></b></td>
    <td>Pressure in the arteries during the contraction of the heart muscle. Consistently high blood pressure can be a risk factor for diabetes and cardiovascular diseases.</td>
    <td><b><code>70</code></b>, <b><code>80</code></b>, <b><code>90</code></b></td>
  </tr>
  <tr>
    <td><b><code>SkinThickness</code></b></td>
    <td>Triceps skin fold thickness (in millimeters), a measure used to estimate body fat. In the context of diabetes, it can help assess insulin resistance.</td>
    <td><b><code>20</code></b>, <b><code>25</code></b>, <b><code>30</code></b></td>
  </tr>
  <tr>
    <td><b><code>Insulin</code></b></td>
    <td>Two-hour serum insulin level after a glucose challenge. This can indicate how the body responds to glucose intake and may reflect insulin resistance or deficiency, both of which are important in diabetes.</td>
    <td><b><code>80</code></b>, <b><code>155</code></b>, <b><code>230</code></b></td>
  </tr>
  <tr>
    <td><b><code>BMI</code></b></td>
    <td>Body Mass Index, a measure of body fat based on height and weight. It is a person's weight in kilograms divided by the square of height in meters. A high BMI can indicate obesity, which is a risk factor for diabetes.</td>
    <td><b><code>22.0</code></b>, <b><code>28.5</code></b>, <b><code>35.1</code></b></td>
  </tr>
  <tr>
    <td><b><code>DiabetesPedigreeFunction</code></b></td>
    <td>A function representing diabetes history in relatives and genetic relationship. A higher value could indicate a higher genetic predisposition to diabetes.</td>
    <td><b><code>0.500</code></b>, <b><code>1.251</code></b>, <b><code>2.000</code></b></td>
  </tr>
  <tr>
    <td><b><code>Age</code></b></td>
    <td>Age of the patient. Age is a factor in the development of type 2 diabetes, with risk increasing as people get older.</td>
    <td><b><code>21</code></b>, <b><code>35</code></b>, <b><code>50</code></b></td>
  </tr>
  <tr>
    <td><b><code>Outcome</code></b></td>
    <td>Categorical variable indicating diagnosis of diabetes (1) or not (0).</td>
    <td><b><code>0</code></b> (No diabetes), <b><code>1</code></b> (Diabetes)</td>
  </tr>
</table>

## Acknowledgements
Smith, J.W., Everhart, J.E., Dickson, W.C., Knowler, W.C., & Johannes, R.S. (1988). Using the ADAP learning algorithm to forecast the onset of diabetes mellitus.<br><i>In Proceedings of the Symposium on Computer Applications and Medical Care (pp. 261--265). IEEE Computer Society Press.</i>
