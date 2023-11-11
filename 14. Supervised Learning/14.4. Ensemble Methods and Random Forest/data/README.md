<h1>About dataset</h1>

<p>
This dataset provides comprehensive information on patients affected by the coronavirus (COVID-19). It includes various demographic, geographic, and medical details, offering insights into the spread, impact, and outcomes of the virus on individual patients. The data can be invaluable for researchers, epidemiologists, and public health professionals analyzing the patterns of COVID-19 infection, response to treatment, and effectiveness of containment measures. Each variable in the dataset is meticulously recorded, ensuring a robust resource for in-depth analysis.
</p>
<table>
<thead>
<tr>
<th>Variable Name</th>
<th>Description</th>
<th>Accepted Values/Formats</th>
</tr>
</thead>
<tbody>
<tr><td><code><b>patient_id</b></code></td><td>Unique identifier for each patient</td><td>Numeric ID</td></tr>
<tr><td><code><b>global_num</b></code></td><td>Global identification number</td><td>Numeric value</td></tr>
<tr><td><code><b>sex</b></code></td><td>Gender of the patient</td><td><code>'male'</code>, <code>'female'</code></td></tr>
<tr><td><code><b>birth_year</b></code></td><td>Year of birth of the patient</td><td>Year (YYYY)</td></tr>
<tr><td><code><b>age</b></code></td><td>Age group of the patient</td><td>Age range (e.g., <code>'20s'</code>, <code>'30s'</code>)</td></tr>
<tr><td><code><b>country</b></code></td><td>Country of origin of the patient</td><td>Country name</td></tr>
<tr><td><code><b>province</b></code></td><td>Province where the patient is located</td><td>Province name</td></tr>
<tr><td><code><b>city</b></code></td><td>City where the patient is located</td><td>City name</td></tr>
<tr><td><code><b>disease</b></code></td><td>Information about any disease the patient may have</td><td>Textual description, if applicable</td></tr>
<tr><td><code><b>infection_case</b></code></td><td>The case of infection</td><td>Textual description (e.g., <code>'overseas inflow'</code>, <code>'contact with patient'</code>)</td></tr>
<tr><td><code><b>infection_order</b></code></td><td>The order of infection</td><td>Numeric value</td></tr>
<tr><td><code><b>infected_by</b></code></td><td>ID of the patient who might have infected this patient</td><td>Numeric ID</td></tr>
<tr><td><code><b>contact_number</b></code></td><td>Number of people the patient has been in contact with</td><td>Numeric value</td></tr>
<tr><td><code><b>symptom_onset_date</b></code></td><td>Date when symptoms began</td><td>Date (MM/DD/YYYY)</td></tr>
<tr><td><code><b>confirmed_date</b></code></td><td>Date when the patient was confirmed with the condition</td><td>Date (MM/DD/YYYY)</td></tr>
<tr><td><code><b>released_date</b></code></td><td>Date when the patient was released</td><td>Date (MM/DD/YYYY), if applicable</td></tr>
<tr><td><code><b>deceased_date</b></code></td><td>Date of decease, if applicable</td><td>Date (MM/DD/YYYY), if applicable</td></tr>
<tr><td><code><b>state</b></code></td><td>Current state of the patient (e.g., released, deceased)</td><td><code>'isolated'</code>, <code>'released'</code>, <code>'deceased'</code></td></tr>
</tbody>
</table>
