from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

class RuleMLParser:
    """Parser for RuleML-based job screening rules"""
    
    def __init__(self, rules_file):
        self.rules_file = rules_file
        self.tree = ET.parse(rules_file)
        self.root = self.tree.getroot()
        # Remove namespace if present to simplify XPath queries
        for elem in self.root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        
    def get_required_skills(self):
        """Extract required skills from RuleML"""
        skills = []
        required_skills = self.root.find('.//required_skills')
        if required_skills:
            for skill in required_skills.findall('skill'):
                if skill.text:
                    skills.append(skill.text)
        return skills
    
    def get_optional_skills(self):
        """Extract optional skills from RuleML"""
        skills = []
        optional_skills = self.root.find('.//optional_skills')
        if optional_skills:
            for skill in optional_skills.findall('skill'):
                if skill.text:
                    skills.append(skill.text)
        return skills
    
    def get_job_info(self):
        """Get job title and description"""
        job = self.root.find('.//job')
        if job is None:
            return {'title': 'Senior Software Developer', 'description': 'Backend development role'}
        
        title_elem = job.find('title')
        desc_elem = job.find('description')
        
        return {
            'title': title_elem.text if title_elem is not None and title_elem.text else 'Unknown',
            'description': desc_elem.text if desc_elem is not None and desc_elem.text else ''
        }
    
    def evaluate_condition(self, condition, applicant_data):
        """Evaluate a single condition element"""
        condition_type = condition.get('type', 'AND')
        requirements = condition.findall('requirement')
        
        if len(requirements) == 0:
            return False
        
        results = []
        for req in requirements:
            field = req.get('field')
            operator = req.get('operator')
            value = req.get('value')
            
            # Get applicant value for this field
            applicant_value = applicant_data.get(field)
            
            # Evaluate based on operator
            if operator == 'eq':
                results.append(str(applicant_value) == str(value))
            elif operator == 'gte':
                results.append(float(applicant_value) >= float(value))
            elif operator == 'lt':
                results.append(float(applicant_value) < float(value))
            elif operator == 'in':
                valid_values = value.split(',')
                results.append(str(applicant_value) in valid_values)
            else:
                results.append(False)
        
        # Apply logical operator
        if condition_type == 'AND':
            return all(results)
        elif condition_type == 'OR':
            return any(results)
        else:
            return all(results)  # Default to AND
    
    def screen_applicant(self, applicant_data):
        """Screen applicant against all rules"""
        
        # Priority order: Check rejection rules first, then acceptance, then review
        
        # 1. Check REJECTION rules
        rejection_rules = self.root.find('.//rejection_rules')
        if rejection_rules:
            for rule in rejection_rules.findall('rule'):
                condition = rule.find('condition')
                if self.evaluate_condition(condition, applicant_data):
                    action = rule.find('action')
                    return {
                        'decision': action.find('decision').text,
                        'reason': action.find('reason').text,
                        'rule_id': rule.get('id'),
                        'priority': action.find('priority').text
                    }
        
        # 2. Check ACCEPTANCE rules
        acceptance_rules = self.root.find('.//acceptance_rules')
        if acceptance_rules:
            for rule in acceptance_rules.findall('rule'):
                condition = rule.find('condition')
                if self.evaluate_condition(condition, applicant_data):
                    action = rule.find('action')
                    return {
                        'decision': action.find('decision').text,
                        'reason': action.find('reason').text,
                        'rule_id': rule.get('id'),
                        'priority': action.find('priority').text
                    }
        
        # 3. Check REVIEW rules
        review_rules = self.root.find('.//review_rules')
        if review_rules:
            for rule in review_rules.findall('rule'):
                condition = rule.find('condition')
                if self.evaluate_condition(condition, applicant_data):
                    action = rule.find('action')
                    return {
                        'decision': action.find('decision').text,
                        'reason': action.find('reason').text,
                        'rule_id': rule.get('id'),
                        'priority': action.find('priority').text
                    }
        
        # Default: No rule matched - send for review
        return {
            'decision': 'REVIEW',
            'reason': 'Application does not match standard criteria - manual review required',
            'rule_id': 'default',
            'priority': '99'
        }


# Initialize parser
rules_path = os.path.join(os.path.dirname(__file__), 'rules', 'job_screening_rules.xml')
parser = RuleMLParser(rules_path)

@app.route('/')
def index():
    """Render main application form"""
    job_info = parser.get_job_info()
    required_skills = parser.get_required_skills()
    optional_skills = parser.get_optional_skills()
    
    return render_template('index.html', 
                         job_info=job_info,
                         required_skills=required_skills,
                         optional_skills=optional_skills)

@app.route('/screen', methods=['POST'])
def screen():
    """Process job application screening"""
    
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    education = request.form.get('education')
    experience = float(request.form.get('experience', 0))
    
    # Get selected skills
    selected_required = request.form.getlist('required_skills')
    selected_optional = request.form.getlist('optional_skills')
    
    # Check for relevant experience
    has_relevant = request.form.get('relevant_experience') == 'yes'
    
    # Count skill matches
    all_required_skills = parser.get_required_skills()
    required_skills_match = len(selected_required)
    optional_skills_match = len(selected_optional)
    
    # Build applicant data for rule evaluation
    applicant_data = {
        'name': name,
        'email': email,
        'education': education,
        'experience': experience,
        'required_skills_match': required_skills_match,
        'optional_skills_match': optional_skills_match,
        'relevant_experience': 'true' if has_relevant else 'false',
        'selected_required_skills': selected_required,
        'selected_optional_skills': selected_optional
    }
    
    # Screen using RuleML
    result = parser.screen_applicant(applicant_data)
    
    # Add additional info for display
    result['applicant'] = {
        'name': name,
        'email': email,
        'education': education,
        'experience': experience,
        'required_skills': selected_required,
        'optional_skills': selected_optional,
        'required_skills_match': f"{required_skills_match}/{len(all_required_skills)}",
        'relevant_experience': 'Yes' if has_relevant else 'No'
    }
    
    result['job_info'] = parser.get_job_info()
    
    return render_template('result.html', result=result)

@app.route('/api/screen', methods=['POST'])
def api_screen():
    """API endpoint for screening (JSON)"""
    data = request.json
    
    applicant_data = {
        'education': data.get('education'),
        'experience': float(data.get('experience', 0)),
        'required_skills_match': int(data.get('required_skills_match', 0)),
        'optional_skills_match': int(data.get('optional_skills_match', 0)),
        'relevant_experience': str(data.get('relevant_experience', False)).lower()
    }
    
    result = parser.screen_applicant(applicant_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
