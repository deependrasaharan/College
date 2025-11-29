# RuleML Job Screening System - Core Logic Diagrams

## 1. RuleML Structure & Organization

```mermaid
graph TB
    Root[RuleML XML Root]
    
    Root --> Job[Job Definition]
    Root --> Rules[Rule Categories]
    
    Job --> Title[Title: Senior Software Developer]
    Job --> ReqSkills[Required Skills: 5]
    Job --> OptSkills[Optional Skills: 5]
    
    Rules --> AcceptRules[Acceptance Rules<br/>3 rules]
    Rules --> RejectRules[Rejection Rules<br/>4 rules]
    Rules --> ReviewRules[Review Rules<br/>5 rules]
    
    AcceptRules --> AR1[Rule: Excellent Candidate<br/>Priority 1]
    AcceptRules --> AR2[Rule: All Skills Match<br/>Priority 2]
    AcceptRules --> AR3[Rule: Advanced Degree<br/>Priority 3]
    
    RejectRules --> RR1[Rule: Education Insufficient<br/>Priority 1]
    RejectRules --> RR2[Rule: Low Experience<br/>Priority 2]
    RejectRules --> RR3[Rule: Missing Skills<br/>Priority 3]
    
    ReviewRules --> RevR1[Rule: Career Changer<br/>Priority 1]
    ReviewRules --> RevR2[Rule: Missing Some Skills<br/>Priority 2]
    ReviewRules --> RevR3[Rule: Borderline<br/>Priority 5]
    
    subgraph RuleStructure["Individual Rule Structure"]
        RuleElem[Rule Element]
        RuleElem --> Condition[Condition Block<br/>AND/OR Logic]
        RuleElem --> Action[Action Block]
        
        Condition --> Req[Requirements<br/>field, operator, value]
        Action --> Dec[Decision: ACCEPT/REVIEW/REJECT]
        Action --> Reason[Reason: Explanation]
        Action --> Pri[Priority: 1-N]
    end
    
    style Root fill:#667eea,color:#fff
    style Job fill:#764ba2,color:#fff
    style Rules fill:#764ba2,color:#fff
    style AcceptRules fill:#11998e,color:#fff
    style RejectRules fill:#fa709a,color:#fff
    style ReviewRules fill:#f093fb,color:#fff
    style RuleStructure fill:#e1f5ff
```

## 2. RuleML Evaluation Flow (Complete Process)

```mermaid
flowchart TD
    Start([Applicant Submits Form]) --> Parse[Parse RuleML XML<br/>Remove Namespaces]
    Parse --> Extract[Extract Applicant Data<br/>Name, Education, Experience, Skills]
    Extract --> Count[Count Skill Matches<br/>Required: X/5<br/>Optional: Y/5]
    
    Count --> BuildObj[Build Applicant Object<br/>education: value<br/>experience: value<br/>required_skills_match: X<br/>relevant_experience: true/false]
    
    BuildObj --> Priority{Check Rules by Priority<br/>REJECT → ACCEPT → REVIEW}
    
    Priority --> CheckReject[Evaluate REJECTION Rules]
    
    CheckReject --> RejectMatch{Rule<br/>Matched?}
    RejectMatch -->|YES| RejectAction[Execute Action Block]
    RejectAction --> RejectResult[❌ REJECT<br/>+ Reason<br/>+ Rule ID<br/>+ Priority]
    
    RejectMatch -->|NO| CheckAccept[Evaluate ACCEPTANCE Rules]
    
    CheckAccept --> AcceptMatch{Rule<br/>Matched?}
    AcceptMatch -->|YES| AcceptAction[Execute Action Block]
    AcceptAction --> AcceptResult[✅ ACCEPT<br/>+ Reason<br/>+ Rule ID<br/>+ Priority]
    
    AcceptMatch -->|NO| CheckReview[Evaluate REVIEW Rules]
    
    CheckReview --> ReviewMatch{Rule<br/>Matched?}
    ReviewMatch -->|YES| ReviewAction[Execute Action Block]
    ReviewAction --> ReviewResult[👀 REVIEW<br/>+ Reason<br/>+ Rule ID<br/>+ Priority]
    
    ReviewMatch -->|NO| DefaultReview[Default: REVIEW<br/>Manual review required]
    
    RejectResult --> Display[Display Result Page]
    AcceptResult --> Display
    ReviewResult --> Display
    DefaultReview --> Display
    
    Display --> End([End])
    
    style Start fill:#90EE90,color:#000
    style Parse fill:#87CEEB,color:#000
    style Priority fill:#764ba2,color:#fff
    style RejectResult fill:#FFB6C1,color:#000
    style AcceptResult fill:#98FB98,color:#000
    style ReviewResult fill:#FFD700,color:#000
    style DefaultReview fill:#FFD700,color:#000
    style Display fill:#87CEEB,color:#000
    style End fill:#90EE90,color:#000
```

## 3. Rule Condition Evaluation Logic (AND/OR)

```mermaid
flowchart TD
    Start([Single Rule Evaluation]) --> GetRule[Get Rule Element<br/>id, condition, action]
    
    GetRule --> CondType{Condition<br/>Type?}
    
    CondType -->|AND| ANDLogic[AND Logic<br/>All requirements must be TRUE]
    CondType -->|OR| ORLogic[OR Logic<br/>At least one must be TRUE]
    
    ANDLogic --> GetReqA[Get All Requirements<br/>Req1, Req2, ..., ReqN]
    ORLogic --> GetReqO[Get All Requirements<br/>Req1, Req2, ..., ReqN]
    
    GetReqA --> EvalA[Evaluate Each Requirement]
    GetReqO --> EvalO[Evaluate Each Requirement]
    
    EvalA --> CheckField[Check Field Value<br/>education, experience, etc]
    EvalO --> CheckField
    
    CheckField --> ApplyOp{Apply<br/>Operator}
    
    ApplyOp -->|eq| Equal[Equals<br/>value == expected]
    ApplyOp -->|gte| GreaterEqual[Greater or Equal<br/>value >= expected]
    ApplyOp -->|lt| LessThan[Less Than<br/>value < expected]
    ApplyOp -->|in| InList[In List<br/>value IN list]
    
    Equal --> ReqResult[Requirement Result<br/>TRUE or FALSE]
    GreaterEqual --> ReqResult
    LessThan --> ReqResult
    InList --> ReqResult
    
    ReqResult --> ANDCheck{AND:<br/>All TRUE?}
    ReqResult --> ORCheck{OR:<br/>Any TRUE?}
    
    ANDCheck -->|YES| Match[Rule MATCHES]
    ANDCheck -->|NO| NoMatch[Rule DOESN'T MATCH]
    
    ORCheck -->|YES| Match
    ORCheck -->|NO| NoMatch
    
    Match --> ExecuteAction[Execute Action Block]
    NoMatch --> SkipRule[Skip to Next Rule]
    
    ExecuteAction --> GetDecision[Get Decision]
    ExecuteAction --> GetReason[Get Reason]
    ExecuteAction --> GetPriority[Get Priority]
    
    GetDecision --> Return[Return Result<br/>decision, reason, priority, rule_id]
    GetReason --> Return
    GetPriority --> Return
    
    SkipRule --> NextRule([Try Next Rule])
    Return --> Done([Rule Matched - Stop])
    
    style Start fill:#667eea,color:#fff
    style CondType fill:#764ba2,color:#fff
    style ANDLogic fill:#11998e,color:#fff
    style ORLogic fill:#f093fb,color:#fff
    style Match fill:#98FB98,color:#000
    style NoMatch fill:#FFB6C1,color:#000
    style Return fill:#FFD700,color:#000
    style Done fill:#90EE90,color:#000
    
    subgraph Operators["Supported Operators"]
        Equal
        GreaterEqual
        LessThan
        InList
    end
    
    style Operators fill:#e1f5ff
```

---

## How to View These Diagrams

### In VS Code:
1. Install extension: **"Markdown Preview Mermaid Support"**
2. Open this file and press `Ctrl+Shift+V` (Preview)

### Online:
Visit **https://mermaid.live/** and paste diagram code

### In Report:
Take screenshots of rendered diagrams for inclusion in practical report

---

## Diagram Explanations

**Diagram 1 - RuleML Structure:**
Shows the complete XML structure with 3 rule categories (Accept/Reject/Review), job definition, and the anatomy of a single rule element with conditions and actions.

**Diagram 2 - Evaluation Flow:**
Complete step-by-step process from form submission to final decision, showing priority-based evaluation (Reject → Accept → Review) and how each rule category is checked sequentially.

**Diagram 3 - Condition Logic:**
Details how individual rules evaluate conditions using AND/OR logic, the 4 supported operators (eq, gte, lt, in), and how requirement results determine rule matching.

---

**Color Legend:**
- 🟢 Green: Success/Start/End
- 🟡 Yellow: Review/Default paths
- 🔴 Pink: Reject paths  
- � Blue: Process steps
- 🟣 Purple: Decision points
- 🟩 Teal: Accept paths
