# 🚀 Job Application Screener with RuleML

A modern web application that uses **RuleML (Rule Markup Language)** to automatically screen job applications based on predefined business rules.

## 📋 Overview

This intelligent screening system evaluates job applications using rule-based logic encoded in RuleML XML format. It provides instant decisions:
- ✅ **ACCEPT** - Candidate meets all requirements
- 👀 **REVIEW** - Requires manual evaluation
- ❌ **REJECT** - Does not meet minimum requirements

## 🎯 Features

- **RuleML-powered screening engine** - XML-based rule evaluation
- **Modern, responsive UI** - Built with Tailwind CSS
- **Instant feedback** - Real-time application screening
- **Detailed explanations** - Transparent decision reasoning
- **Multiple rule types** - Acceptance, rejection, and review rules
- **Skill matching** - Required and optional skills evaluation
- **Experience validation** - Years of experience and relevance checking

## 🏗️ Project Structure

```
practical-5-ruleml/
├── app.py                          # Flask backend application
├── requirements.txt                 # Python dependencies
├── rules/
│   └── job_screening_rules.xml     # RuleML rules definition
├── templates/
│   ├── index.html                  # Application form
│   └── result.html                 # Results page
└── static/                          # Static assets (if any)
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Navigate to project directory:**
   ```bash
   cd practical-5-ruleml
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

## 📝 How It Works

### RuleML Rule Structure

The system uses XML-based RuleML rules with three categories:

1. **Acceptance Rules** - Auto-accept qualified candidates
   - Excellent qualifications (5+ years, 4+ skills, degree)
   - All required skills with good experience
   - Advanced degree holders

2. **Rejection Rules** - Auto-reject unqualified candidates
   - Insufficient education (below Bachelor's)
   - Inadequate experience (< 2 years for Bachelor's)
   - Missing too many required skills (< 2 out of 5)

3. **Review Rules** - Flag for manual evaluation
   - Career changers with potential
   - Experienced candidates missing some skills
   - Recent graduates with strong skills
   - Borderline cases

### Rule Evaluation Process

```
1. Parse applicant data from form
2. Calculate skill matches
3. Check REJECTION rules first (highest priority)
4. Then check ACCEPTANCE rules
5. Finally check REVIEW rules
6. Return decision with explanation
```

### Sample Rule (RuleML XML)

```xml
<rule id="auto_accept_excellent">
  <condition type="AND">
    <requirement field="education" operator="in" value="Bachelor,Master,PhD"/>
    <requirement field="experience" operator="gte" value="5"/>
    <requirement field="required_skills_match" operator="gte" value="4"/>
  </condition>
  <action>
    <decision>ACCEPT</decision>
    <reason>Excellent candidate with strong qualifications</reason>
    <priority>1</priority>
  </action>
</rule>
```

## 🧪 Testing Scenarios

### Scenario 1: Accepted Candidate
- Education: Master's Degree
- Experience: 6 years
- Required Skills: 4 out of 5
- Result: ✅ **ACCEPTED**

### Scenario 2: Rejected Candidate
- Education: High School
- Experience: 1 year
- Required Skills: 1 out of 5
- Result: ❌ **REJECTED** (Education requirement not met)

### Scenario 3: Review Required
- Education: Bachelor's Degree
- Experience: 2.5 years
- Required Skills: 3 out of 5
- Result: 👀 **REVIEW** (Good potential but limited experience)

## 🎨 UI Features

- **Gradient backgrounds** - Modern visual appeal
- **Animated elements** - Smooth fade-in effects
- **Responsive design** - Works on all devices
- **Interactive checkboxes** - Visual skill selection
- **Color-coded results** - Green (accept), Yellow (review), Red (reject)

## 📊 RuleML Components Used

- `<RuleML>` - Root element
- `<rule>` - Individual rule definition
- `<condition>` - Rule conditions with AND/OR logic
- `<requirement>` - Field-level requirements with operators
- `<action>` - Decision and reasoning
- `<priority>` - Rule precedence

## 🔧 Customization

### Adding New Rules

Edit `rules/job_screening_rules.xml` and add new rule elements:

```xml
<rule id="custom_rule">
  <condition type="AND">
    <!-- Add your conditions -->
  </condition>
  <action>
    <decision>ACCEPT|REVIEW|REJECT</decision>
    <reason>Your explanation</reason>
    <priority>1</priority>
  </action>
</rule>
```

### Modifying Skills

Update the `<required_skills>` and `<optional_skills>` sections in the XML file.

## 🚀 API Endpoint

The application also provides a JSON API:

**POST** `/api/screen`

Request body:
```json
{
  "education": "Bachelor",
  "experience": 5,
  "required_skills_match": 4,
  "optional_skills_match": 2,
  "relevant_experience": true
}
```

Response:
```json
{
  "decision": "ACCEPT",
  "reason": "Excellent candidate with strong qualifications",
  "rule_id": "auto_accept_excellent",
  "priority": "1"
}
```

## 📚 Technologies Used

- **Backend:** Python Flask
- **Frontend:** HTML5, Tailwind CSS
- **Rule Engine:** Custom RuleML XML Parser
- **Data Format:** XML (RuleML)

## 🎓 Educational Value

This project demonstrates:
- Rule-based AI systems
- Knowledge representation using RuleML
- Business logic separation from application code
- XML parsing and rule evaluation
- Modern web development practices

## 📄 License

This is an educational project for AI Lab Practical 5.

## 👤 Author

AI Lab Practical 5 - RuleML Implementation

---

**Note:** This is a demonstration project for educational purposes. For production use, consider additional features like database integration, user authentication, and more sophisticated rule engines.
