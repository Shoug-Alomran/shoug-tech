/* SE423 midterm cheat sheet: memorize lists, question bank, keyword grader.
   Question types:
     mcq   { q, opts: [correct, wrong, wrong, wrong], why }
     tf    { q, a: true|false, why }
     match { q, pairs: [[left, right], ...] }
     list  { q, need, items: [[label, [keywords...]], ...], why }
     short { q, groups: [[label, [keywords...]], ...], model }
   A keyword hits when it appears as a word, a word prefix (4+ letters), or
   within a small typo distance. Multi-word keywords need every word to hit. */
(function () {
  "use strict";

  var HUE = { 1: 262, 1.2: 205, 1.3: 172, 2: 26, 3: 330 };
  var CH_NAME = {
    1: "Ch 1 Introduction",
    1.2: "Ch 1.2 Performance Domains",
    1.3: "Ch 1.3 Tailoring & MMA",
    2: "Ch 2 Org Context",
    3: "Ch 3 Team",
  };
  var CHS = ["1", "1.2", "1.3", "2", "3"];

  /* ------------------------------------------------------------ memorize */
  var MEM = [
    ["1", "PM principles (PMBOK v7)", "Stewards Trust Stakeholders' Value; Systems Leaders Tailor Quality, Complexity, Risk, Adapt & Change", ["Stewardship", "Team", "Stakeholders", "Value", "Systems thinking", "Leadership", "Tailoring", "Quality", "Complexity", "Risk", "Adaptability and resiliency", "Change"]],
    ["1", "PMI Code of Ethics values", "Real Respect For Honesty", ["Responsibility", "Respect", "Fairness", "Honesty"]],
    ["1", "Issues a PM is responsible for", "SBQ-DL", ["Schedule", "Budget", "Quality", "Delivery of products", "Locking in resources"]],
    ["1", "Global issues", "Talent · Techniques · Agile · Benefits", ["Talent development for project/program managers", "Basic PM techniques are core competencies", "More agile approaches", "Benefits realization is a key metric"]],
    ["1", "Skills for project managers", "Change · Organization · Teams", ["Be comfortable with change", "Understand the organizations they work in and with", "Lead teams to accomplish project goals"]],
    ["1", "Ways projects create value", "New · Social · Efficient · Transition · Sustain", ["New product, service or result", "Positive social or environmental contributions", "Improve efficiency, productivity, effectiveness, responsiveness", "Enable organizational transition to future state", "Sustain benefits from previous work"]],
    ["1", "Functions associated with projects", "Oversee, Objectives, Facilitate, Perform, Expertise, Business, Resources, Governance", ["Provide oversight and coordination", "Present objectives and feedback", "Facilitate and support", "Perform work and contribute insights", "Apply expertise", "Provide business direction and insight", "Provide resources and direction", "Maintain governance"]],
    ["1", "Product life cycle", "I Grow Mature, then Retire", ["Introduction", "Growth", "Maturity", "Retirement"]],
    ["1", "Forms of product management", "Program-in-life-cycle · Project-in-life-cycle · Product-in-program", ["Program management within a product life cycle", "Project management within a product life cycle", "Product management within a program"]],
    ["1.2", "Performance domains", "Smart Teams Develop Plans, Produce Deliverables, Measure Uncertainty", ["Stakeholders", "Team", "Development approach and life cycle", "Planning", "Project work", "Delivery", "Measurement", "Uncertainty"]],
    ["1.2", "Common aspects of team development", "Vision, Roles, Operations, Guidance, Growth", ["Vision and objectives", "Roles and responsibilities", "Project team operations", "Guidance", "Growth"]],
    ["1.2", "Behaviors the PM models for team culture", "TIR-PSCC", ["Transparency", "Integrity", "Respect", "Positive discourse", "Support", "Courage", "Celebrating success"]],
    ["1.2", "High-performing team factors", "Open, Shared ×2, Trust, Collaboration, Adapt, Resilient, Empowered, Recognized", ["Open communication", "Shared understanding", "Shared ownership", "Trust", "Collaboration", "Adaptability", "Resilience", "Empowerment", "Recognition"]],
    ["1.2", "Leadership skills", "Vision · Critical thinking · Motivation · Interpersonal", ["Establishing and maintaining vision", "Critical thinking", "Motivation", "Interpersonal skills"]],
    ["1.2", "Emotional intelligence components", "Self ×2, Social ×2", ["Self-awareness", "Self-management", "Social awareness", "Social skill"]],
    ["1.2", "Variables for tailoring leadership style", "Experience · Maturity · Governance · Distributed", ["Experience with the type of project", "Maturity of team members", "Organizational governance structures", "Distributed project teams"]],
    ["1.2", "Product variables for choosing an approach", "Innovation, Certainty, Stability, Change, Delivery, Risk, Safety, Regulations", ["Degree of innovation", "Requirements certainty", "Scope stability", "Ease of change", "Delivery options", "Risk", "Safety requirements", "Regulations"]],
    ["1.2", "Predictive schedule steps", "Decompose → Sequence → Estimate → Allocate → Adjust", ["Decompose scope into activities", "Sequence related activities", "Estimate effort, duration, resources", "Allocate people and resources", "Adjust until an agreed schedule"]],
    ["1.2", "Dependency types", "Must · Might · Outside · Inside", ["Mandatory", "Discretionary", "External", "Internal"]],
    ["1.2", "SMART metrics (this course)", "M = Meaningful", ["Specific", "Meaningful", "Achievable", "Relevant", "Timely"]],
    ["1.2", "What to measure", "Deliverable, Delivery, Baseline, Resources, Business value, Stakeholders, Forecasts", ["Deliverable metrics", "Delivery", "Baseline performance", "Resources", "Business value", "Stakeholders", "Forecasts"]],
    ["1.2", "Presenting information", "Dashboards · Radiators · Visual controls", ["Dashboards", "Information radiators", "Visual controls (task boards, burn charts)"]],
    ["1.2", "Uncertainty terms", "U-A-C-V-R", ["Uncertainty", "Ambiguity (conceptual, situational)", "Complexity", "Volatility", "Risk"]],
    ["1.2", "Ways to handle complexity", "Systems: Decouple, Simulate · Reframe: Diversity, Balance · Process: Iterate, Engage, Fail safe", ["Decoupling", "Simulation", "Diversity", "Balance", "Iterate", "Engage", "Fail safe"]],
    ["1.2", "Threat strategies", "Avoid, Escalate, Transfer, Mitigate, Accept", ["Avoid", "Escalate", "Transfer", "Mitigate", "Accept"]],
    ["1.2", "Opportunity strategies", "Exploit, Escalate, Share, Enhance, Accept", ["Exploit", "Escalate", "Share", "Enhance", "Accept"]],
    ["1.2", "Bid documents", "Info → Proposal → Quote", ["Request for information (RFI)", "Request for proposal (RFP)", "Request for quote (RFQ)"]],
    ["1.3", "Tailoring process", "Some Organizations Prefer Improvement", ["Select initial development approach", "Tailor for the organization", "Tailor for the project", "Implement ongoing improvement"]],
    ["1.3", "What to tailor", "Life cycle, Processes, Engagement, Tools, Methods & artifacts", ["Life cycle and development approach", "Processes", "Engagement", "Tools", "Methods and artifacts"]],
    ["1.3", "Process tailoring actions", "A Man Rarely Buys Apples", ["Added", "Modified", "Removed", "Blended", "Aligned"]],
    ["1.3", "Engagement tailoring", "PEI", ["People", "Empowerment", "Integration"]],
    ["1.3", "Benefits of tailoring", "Commitment · Customer · Efficiency", ["More commitment from team members", "Customer-oriented focus", "More efficient use of resources"]],
    ["1.3", "Project team considerations", "Size, Geography, Distribution, Experience, Customer access", ["Team size", "Team geography", "Organizational distribution", "Team experience", "Access to customer"]],
    ["1.3", "Culture considerations when tailoring", "Buy-in, Trust, Empowerment, Org culture", ["Buy-in", "Trust", "Empowerment", "Organizational culture"]],
    ["1.3", "Avoid any model/method/artifact that", "Duplicates · Useless · Misleading · Individual", ["Duplicates or adds unnecessary effort", "Is not useful", "Produces incorrect or misleading information", "Caters to individual needs over the team's"]],
    ["1.3", "Maslow's hierarchy (bottom up)", "Please Stop Lying, Eat Salad", ["Physiological", "Safety", "Love/belonging", "Esteem", "Self-actualization"]],
    ["1.3", "8-step process for leading change", "Urgency, Coalition, Vision, Army, Barriers, Wins, Acceleration, Institute", ["Create a sense of urgency", "Build a guiding coalition", "Form a strategic vision", "Enlist a volunteer army", "Remove barriers", "Generate short-term wins", "Sustain acceleration", "Institute change"]],
    ["2", "Elements of strategic management", "Vision, Formulate, Cross-functional, Achieve", ["Developing vision and mission statements", "Formulating, implementing, and evaluating", "Making cross-functional decisions", "Achieving objectives"]],
    ["2", "Organizational structure elements", "Reporting · Grouping · Systems", ["Formal reporting relationships", "Groupings of individuals and departments", "Systems for communication, coordination, integration"]],
    ["2", "Internal stakeholders", "Top, Accountant, Functional, Team", ["Top management", "Accountant", "Other functional managers", "Project team members"]],
    ["2", "External stakeholders", "Clients, Competitors, Suppliers, Intervenors", ["Clients", "Competitors", "Suppliers", "Environmental, political, consumer and other intervenor groups"]],
    ["2", "Functional structure weaknesses", "Silo · Customer · Slow · Commitment", ["Functional siloing", "Lack of customer focus", "Longer time to complete projects", "Varying interest or commitment"]],
    ["2", "Project structure strengths", "Authority, Communication, Decisions, Experts, Rapid", ["PM sole authority", "Improved communication", "Effective decision making", "Creation of PM experts", "Rapid response to market opportunities"]],
    ["2", "Matrix structure weaknesses", "Two bosses · Negotiation · Caught between", ["Dual hierarchy means two bosses", "Negotiation required to share resources", "Workers caught between competing demands"]],
    ["2", "PMO forms", "Low · Moderate · High control", ["Supportive", "Controlling", "Directive"]],
    ["2", "PMO models", "Watch · Protect · Supply", ["Weather station", "Control tower", "Resource pool"]],
    ["2", "Culture definition parts", "Unwritten Rules, Held by subset, Taught", ["Unwritten", "Rules of behavior", "Held by some subset", "Taught to all new members"]],
    ["2", "Factors that affect culture", "Tech, Environment, Geography, Rewards, Rules, Key members, Critical incidents", ["Technology", "Environment", "Geographical location", "Reward systems", "Rules and procedures", "Key organizational members", "Critical incidents"]],
    ["2", "Ways culture affects PM", "Departments Expect Planned Performance", ["Departmental interaction", "Employee commitment to goals", "Project planning", "Performance evaluation"]],
    ["3", "Tuckman's stages", "Form, Storm, Norm, Perform, Adjourn", ["Forming", "Storming", "Norming", "Performing", "Adjourning"]],
    ["3", "Types of influence", "Legit Rewards Can Earn Respect", ["Formal (legitimate)", "Reward", "Penalty (coercive)", "Expert", "Referent"]],
    ["3", "Team pyramid (bottom up)", "Trust Makes Commitment Accountable → Results", ["Trust", "Managed conflict", "Commitment", "Accountability", "Results"]],
    ["3", "Team objectives", "Problem · Creativity · Tactical", ["Problem resolution", "Creativity", "Tactical execution"]],
    ["3", "Conflict resolution techniques", "Confront, Compromise, Withdraw, Smooth, Collaborate, Force", ["Confronting (problem solving)", "Compromising", "Withdrawal (avoidance)", "Smoothing (accommodating)", "Collaborating", "Forcing"]],
    ["3", "Problem-solving steps", "Define, Analyze, Identify, Pick, Implement, Review", ["Define the root problem", "Analyze the problem", "Identify solutions", "Pick a solution", "Implement the solution", "Review the solution"]],
    ["3", "RACI", "R does, A owns", ["Responsible", "Accountable", "(Support)", "Consulted", "Informed"]],
    ["3", "Chief programmer team roles", "Backup, Clerk, Admin, Toolsmith, Lawyer", ["Backup programmer (co-pilot)", "Program clerk", "Administrator", "Toolsmith", "Language lawyer"]],
    ["3", "Management activities related to people", "Solve, Motivate, Plan, Estimate, Control, Organize", ["Problem solving", "Motivating", "Planning", "Estimating", "Controlling", "Organizing"]],
    ["3", "Personality types", "Task · Self · Interaction", ["Task-oriented", "Self-oriented", "Interaction-oriented"]],
    ["3", "Staff selection factors", "Domain, Platform, Language, Education, Communication, Adaptability, Attitude, Personality", ["Application domain experience", "Platform experience", "Programming language experience", "Educational background", "Communication ability", "Adaptability", "Attitude", "Personality"]],
    ["3", "Environmental factors", "Privacy · Outside awareness · Personalization", ["Privacy", "Outside awareness", "Personalization"]],
    ["3", "PM's people skills", "Interpersonal, Culture, Managing, Better, Leadership", ["Interpersonal skills", "Shaping project culture", "Managing people", "Making people better", "Leadership"]],
    ["3", "Cultural roles", "Leader, Listener, Complainer, Expert, Charger", ["Leader", "Listener/talker", "Complainer/naysayer", "Expert", "Charger/plodder"]],
    ["3", "Production-line errors", "Squeeze, Hard line, Interchangeable, Steady state, By the book, No experiments", ["Squeeze out error", "Hard line on goofing off", "Interchangeable workers", "Optimize the steady state", "Standardize procedure", "Eliminate experimentation"]],
  ];

  /* ------------------------------------------------------------ question bank */
  var K = {
    // principles
    stew: ["steward"], team: ["team", "collaborat"], stake: ["stakeholder"], value: ["value"],
    sys: ["system"], lead: ["leader", "leadership"], tailor: ["tailor"], qual: ["quality"], cplx: ["complexity", "complex"],
    risk: ["risk"], adapt: ["adapt", "resilien"], change: ["change", "envisioned future"],
  };

  var Q = [
    /* ===================================================== CH 1 */
    { ch: "1", t: "mcq", q: "Which project is considered the first to use \"modern\" project management?", opts: ["The Manhattan Project", "The Great Wall of China", "The Egyptian pyramids", "The Apollo program"], why: "Led by Oppenheimer: 3 years, $2 billion (1946), with a separate project manager and technical manager." },
    { ch: "1", t: "mcq", q: "According to PMI, by 2027 employers will need how many individuals in project management–oriented roles?", opts: ["87.7 million", "2.3 million", "97 million", "24.7 million"], why: "2.3 million is the number of new PM employees needed each year to 2030." },
    { ch: "1", t: "mcq", q: "A Project Management Office (PMO) is:", opts: ["An organizational unit that coordinates the PM function throughout an organization", "A certification PMI awards to experienced project managers who pass an exam", "A group of related projects managed together for benefits not available separately", "A strategic plan that ranks the organization's projects by expected value"], why: "Companies started creating PMOs in the 1990s." },
    { ch: "1", t: "mcq", q: "\"Related projects, subsidiary programs, and program activities managed in a coordinated manner to obtain benefits not available from managing them individually\" defines a:", opts: ["Program", "Portfolio", "Project", "Product"], why: "A portfolio groups projects, programs and operations to achieve strategic objectives." },
    { ch: "1", t: "mcq", q: "Which is NOT one of the four values of PMI's Code of Ethics and Professional Conduct?", opts: ["Integrity", "Respect", "Fairness", "Honesty"], why: "The four values are Responsibility, Respect, Fairness, and Honesty." },
    { ch: "1", t: "mcq", q: "\"Design the project development approach based on the context... using a 'just enough' process\" describes which principle?", opts: ["Tailor based on context", "Focus on value", "Navigate complexity", "Embrace adaptability and resiliency"], why: "Tailoring is iterative and continuous throughout the project." },
    { ch: "1", t: "mcq", q: "According to the principle cards, value is the ultimate indicator of:", opts: ["Project success", "Stakeholder engagement", "Team performance", "Schedule health"] },
    { ch: "1", t: "mcq", q: "In the value delivery chain, outcomes create ____, which in turn create value.", opts: ["Benefits", "Deliverables", "Outputs", "Artifacts"], why: "Components → deliverables → outcomes → benefits → value." },
    { ch: "1", t: "mcq", q: "In the information flow of a value delivery system, who shares strategic information with portfolios?", opts: ["Senior leadership", "Operations", "Programs and projects", "The project team"] },
    { ch: "1", t: "mcq", q: "Information flowing from operations to programs and projects mainly suggests:", opts: ["Adjustments, fixes, and updates to deliverables", "The organization's strategy for the next year", "The desired outcomes, benefits, and value", "Evaluations of overall portfolio performance"] },
    { ch: "1", t: "mcq", q: "\"Hosting meetings, workshops, and stand-ups\" is an example of which function associated with projects?", opts: ["Facilitate and support", "Provide oversight and coordination", "Maintain governance", "Perform work and contribute insights"] },
    { ch: "1", t: "mcq", q: "Which is an EXTERNAL environment factor?", opts: ["Regulatory environment", "Process assets", "Employee capability", "Governance documentation"], why: "The other three come from inside the organization." },
    { ch: "1", t: "mcq", q: "Modernizing a product's UI years after launch, with portfolio governance chartering individual projects as needed, is an example of:", opts: ["Project management within a product life cycle", "Program management within a product life cycle", "Product management within a program", "Portfolio management within a program"] },
    { ch: "1", t: "mcq", q: "\"The ability to absorb impacts and to recover quickly from a setback or failure\" is:", opts: ["Resiliency", "Adaptability", "Stewardship", "Volatility"], why: "Adaptability is the ability to respond to changing conditions." },
    { ch: "1", t: "mcq", q: "According to the Change principle, attempting too much change in a short time can lead to:", opts: ["Change fatigue and/or resistance", "Faster stakeholder adoption", "Higher worker morale", "Lower overall project risk"] },
    { ch: "1", t: "mcq", q: "What share of successful projects were led by experienced project managers?", opts: ["97%", "87%", "75%", "12.4%"] },
    { ch: "1", t: "mcq", q: "Risk responses, per the Risk principle, should be all of the following EXCEPT:", opts: ["Avoided until the risk becomes an issue", "Appropriate for the significance of the risk", "Cost effective and realistic", "Agreed to by stakeholders and owned by a person"] },
    { ch: "1", t: "mcq", q: "Where does most of a project manager's time go, according to the slides?", opts: ["Chasing and collecting the status of tasks", "Writing code and reviewing technical designs", "Negotiating contracts with outside vendors", "Preparing for certification exams"] },
    { ch: "1", t: "tf", q: "The principles of project management are prescriptive: they act like laws or rules.", a: false, why: "They are not prescriptive; they guide behavior." },
    { ch: "1", t: "tf", q: "The project management principles are internally consistent: no principle contradicts another.", a: true },
    { ch: "1", t: "tf", q: "Principles of project management always reflect morals.", a: false, why: "They can, but do not necessarily, reflect morals. A code of ethics is what relates to morals." },
    { ch: "1", t: "tf", q: "Leadership is the same thing as authority.", a: false, why: "\"Leadership is different than authority\" (Leadership principle)." },
    { ch: "1", t: "tf", q: "Value can be realized only after the project is complete.", a: false, why: "Throughout the project, at the end, or after." },
    { ch: "1", t: "tf", q: "Projects can stand alone or be part of a program or portfolio.", a: true },
    { ch: "1", t: "tf", q: "The Standard for Project Management applies regardless of industry, location, size, or delivery approach.", a: true },
    { ch: "1", t: "tf", q: "In the Manhattan Project, one person acted as both project manager and technical manager.", a: false, why: "It had a separate project manager and technical manager." },
    { ch: "1", t: "tf", q: "In decentralized coordination, project team members self-organize and self-manage.", a: true, why: "Centralized coordination uses a designated project manager." },
    { ch: "1", t: "tf", q: "The project management team is a subset of the project team.", a: true, why: "Members directly involved in PM activities." },
    { ch: "1", t: "tf", q: "Principles of project management overlap with general management principles.", a: true },
    { ch: "1", t: "match", q: "Match each term to its definition.", pairs: [["Portfolio", "Projects, programs and operations managed as a group for strategic objectives"], ["Program", "Related projects managed together for benefits not available individually"], ["Project", "A temporary endeavor to create a unique product, service, or result"], ["Product", "A quantifiable artifact: an end item or a component"], ["Outcome", "An end result or consequence of a process or project"]] },
    { ch: "1", t: "match", q: "Match each principle to what its card says.", pairs: [["Stewardship", "Integrity, care, trustworthiness, compliance"], ["Systems thinking", "A project is a system of interdependent domains"], ["Quality", "Meet acceptance criteria for deliverables"], ["Complexity", "Human behavior, system interactions, uncertainty, ambiguity"], ["Change", "Move from the current state to a desired future state"], ["Adaptability and resiliency", "Respond to change and recover from setbacks"]] },
    { ch: "1", t: "match", q: "Match each project function to its example.", pairs: [["Provide oversight and coordination", "Monitoring progress and performance"], ["Present objectives and feedback", "Defining success criteria"], ["Apply expertise", "Advising on technical matters"], ["Provide business direction and insight", "Identifying market trends"], ["Provide resources and direction", "Allocating budget and personnel"], ["Maintain governance", "Enforcing regulatory standards"]] },
    { ch: "1", t: "list", q: "List the 12 principles of project management (PMBOK v7).", need: 12, items: [["Stewardship", K.stew], ["Team", K.team], ["Stakeholders", K.stake], ["Value", K.value], ["Systems thinking", K.sys], ["Leadership", K.lead], ["Tailoring", K.tailor], ["Quality", K.qual], ["Complexity", K.cplx], ["Risk", K.risk], ["Adaptability & resiliency", K.adapt], ["Change", K.change]] },
    { ch: "1", t: "list", q: "List the four values of PMI's Code of Ethics and Professional Conduct.", need: 4, items: [["Responsibility", ["responsib"]], ["Respect", ["respect"]], ["Fairness", ["fair"]], ["Honesty", ["honest"]]] },
    { ch: "1", t: "list", q: "List the common issues a project manager is responsible for.", need: 5, items: [["Schedule", ["schedul", "time"]], ["Budget", ["budget", "cost"]], ["Quality", ["quality"]], ["Delivery of products", ["deliver"]], ["Locking in resources", ["resource", "locking"]]] },
    { ch: "1", t: "list", q: "List any 6 advantages of using formal project management.", need: 6, items: [["Better control of resources", ["control"]], ["Improved customer relations", ["customer"]], ["Shorter development times", ["shorter", "development time", "faster"]], ["Lower costs, improved productivity", ["lower cost", "productiv", "cost"]], ["Higher quality, reliability", ["quality", "reliab"]], ["Higher profit margins", ["profit"]], ["Better internal coordination", ["coordinat"]], ["Meeting strategic goals", ["strateg"]], ["Higher worker morale", ["morale", "less stress"]], ["Less overworked personnel", ["overwork"]]] },
    { ch: "1", t: "list", q: "List the four global issues forcing organizations to rethink their practices.", need: 4, items: [["Talent development", ["talent"]], ["PM techniques are core competencies", ["core competenc", "technique", "competenc"]], ["More agile approaches", ["agile"]], ["Benefits realization is a key metric", ["benefit"]]] },
    { ch: "1", t: "list", q: "List the phases of the product life cycle.", need: 4, items: [["Introduction", ["introduc"]], ["Growth", ["growth", "grow"]], ["Maturity", ["matur"]], ["Retirement", ["retire", "decline"]]] },
    { ch: "1", t: "list", q: "List any 5 internal environment factors that influence a project.", need: 5, items: [["Process assets", ["process asset"]], ["Governance documentation", ["governance"]], ["Data assets", ["data"]], ["Knowledge assets", ["knowledge"]], ["Security and safety", ["security", "safety"]], ["Infrastructure", ["infrastructure"]], ["IT software", ["software", "information technology"]], ["Resource availability", ["resource availab", "availability"]], ["Employee capability", ["employee", "capabilit"]]] },
    { ch: "1", t: "list", q: "List any 5 external environment factors that influence a project.", need: 5, items: [["Marketplace conditions", ["market"]], ["Social and cultural influences", ["social", "cultur"]], ["Regulatory environment", ["regulat", "legal"]], ["Commercial databases", ["commercial", "database"]], ["Academic research", ["academic", "research"]], ["Industry standards", ["industry", "standard"]], ["Financial considerations", ["financ"]], ["Physical environment", ["physical"]]] },
    { ch: "1", t: "list", q: "List the 8 functions associated with projects.", need: 8, items: [["Oversight and coordination", ["oversight"]], ["Objectives and feedback", ["objective", "feedback"]], ["Facilitate and support", ["facilitat"]], ["Perform work and contribute insights", ["perform work", "contribute", "insight"]], ["Apply expertise", ["expertise", "apply"]], ["Business direction and insight", ["business direction", "business"]], ["Resources and direction", ["resource"]], ["Maintain governance", ["governance"]]] },
    { ch: "1", t: "short", q: "Define a project.", groups: [["temporary", ["temporary"]], ["unique", ["unique"]], ["product, service, or result", ["product", "service", "result"]]], model: "A temporary endeavor undertaken to create a unique product, service, or result." },
    { ch: "1", t: "short", q: "Define project management.", groups: [["knowledge, skills", ["knowledge", "skill"]], ["tools, techniques", ["tool", "technique"]], ["project activities", ["activit", "project work"]], ["meet requirements", ["requirement"]]], model: "The application of knowledge, skills, tools, and techniques to project activities to meet project requirements." },
    { ch: "1", t: "short", q: "What is the difference between adaptability and resiliency?", groups: [["adaptability = respond", ["respond", "changing condition"]], ["resiliency = absorb / recover", ["absorb", "recover"]], ["setback or failure", ["setback", "failure", "impact"]]], model: "Adaptability is the ability to respond to changing conditions; resiliency is the ability to absorb impacts and recover quickly from a setback or failure." },
    { ch: "1", t: "short", q: "How do the principles of project management differ from a code of ethics?", groups: [["principles guide behavior", ["guide", "guidance", "behavior"]], ["not necessarily moral", ["not necessarily", "moral"]], ["ethics relates to morals", ["ethic"]]], model: "Principles guide behavior and can, but do not necessarily, reflect morals; a code of ethics relates to morals and sets expectations for moral conduct (PMI: responsibility, respect, fairness, honesty)." },

    /* ===================================================== CH 1.2 */
    { ch: "1.2", t: "mcq", q: "A cost estimate is built from a very detailed breakdown, but the project ends up costing far more. The estimate was:", opts: ["Precise but not accurate", "Accurate but not precise", "Both accurate and precise", "Neither, since precision requires accuracy"], why: "Precision = exactness (detail); accuracy = correctness (close to reality)." },
    { ch: "1.2", t: "mcq", q: "Which dependency is based on best practices or project preferences and may be modified?", opts: ["Discretionary", "Mandatory", "External", "Contractual"] },
    { ch: "1.2", t: "mcq", q: "A relationship between project activities and non-project activities is a(n):", opts: ["External dependency", "Internal dependency", "Discretionary dependency", "Mandatory dependency"] },
    { ch: "1.2", t: "mcq", q: "Funds set aside for identified risks, controlled by the project manager, are the:", opts: ["Contingency reserve", "Management reserve", "Cost baseline", "Project budget"] },
    { ch: "1.2", t: "mcq", q: "In the budget build-up, the cost baseline equals:", opts: ["Work cost estimates plus contingency reserve", "Work cost estimates plus management reserve", "Project budget minus contingency reserve", "Contingency plus management reserve"], why: "Cost baseline + management reserve = project budget." },
    { ch: "1.2", t: "mcq", q: "Which is a LEADING indicator?", opts: ["Rate of scope change requests", "Cost variance", "Number of deliverables completed", "Customer satisfaction scores"], why: "Leading indicators predict trends; the others report after the fact." },
    { ch: "1.2", t: "mcq", q: "In this course's SMART criteria for effective metrics, the M stands for:", opts: ["Meaningful", "Measurable", "Manageable", "Monitored"] },
    { ch: "1.2", t: "mcq", q: "Net Promoter Score, mood chart, morale and turnover belong to which metric category?", opts: ["Stakeholders", "Business value", "Forecasts", "Delivery"] },
    { ch: "1.2", t: "mcq", q: "ETC, EAC, and VAC belong to which metric category?", opts: ["Forecasts", "Baseline performance", "Resources", "Deliverable metrics"] },
    { ch: "1.2", t: "mcq", q: "Lead time is:", opts: ["The total time from identifying a need to delivering the result", "The time a task waits in the backlog before being picked up", "The time between two consecutive releases of the product", "The time needed to train a new team member on the project"] },
    { ch: "1.2", t: "mcq", q: "\"The schedule was reported on track last week\" is an example of:", opts: ["Conceptual ambiguity", "Situational ambiguity", "Volatility", "Systems-based complexity"], why: "It isn't clear whether the schedule was on track last week, or was reported on last week." },
    { ch: "1.2", t: "mcq", q: "Disconnecting parts of a system to simplify it and reduce connected variables is called:", opts: ["Decoupling", "Simulation", "Diversity", "Fail safe"], why: "Decoupling and simulation are systems-based techniques." },
    { ch: "1.2", t: "mcq", q: "Building redundancy into critical elements so functionality degrades gracefully is which complexity technique?", opts: ["Fail safe", "Engage", "Balance", "Decoupling"] },
    { ch: "1.2", t: "mcq", q: "Volatility is addressed mainly through:", opts: ["Alternatives analysis and cost or schedule reserve", "Decoupling and simulation of the whole system", "Diversity of perspectives and balanced data", "Stakeholder engagement and frequent demos"] },
    { ch: "1.2", t: "mcq", q: "Which is NOT a strategy for dealing with threats?", opts: ["Exploit", "Avoid", "Transfer", "Mitigate"], why: "Exploit is an opportunity strategy." },
    { ch: "1.2", t: "mcq", q: "A time-and-materials subcontractor finishes early, lowering cost and saving schedule. This is a(n):", opts: ["Opportunity", "Threat", "Issue", "Constraint"] },
    { ch: "1.2", t: "mcq", q: "Which approach fits best when requirements can be defined, collected and analyzed at the start of the project?", opts: ["Predictive", "Adaptive", "Hybrid", "Iterative"] },
    { ch: "1.2", t: "mcq", q: "A hybrid approach is especially useful when:", opts: ["Deliverables can be modularized or built by different teams", "Requirements are fully known and stable from the very first day", "The team has no access to the customer at all", "There is a single delivery at the end of the project"] },
    { ch: "1.2", t: "mcq", q: "Delivering feature increments immediately to customers using small batches and automation is:", opts: ["Continuous delivery", "Periodic delivery", "A phase gate", "Last responsible moment"] },
    { ch: "1.2", t: "mcq", q: "Deferring a decision until the cost of further delay would exceed the benefit is called:", opts: ["Last responsible moment", "Progressive elaboration", "Timeboxing", "Phase gate review"] },
    { ch: "1.2", t: "mcq", q: "Personal knowledge that is hard to articulate, like beliefs, experience and insights, is:", opts: ["Tacit knowledge", "Explicit knowledge", "Process assets", "Lessons learned"] },
    { ch: "1.2", t: "mcq", q: "A company needs 500 laptops with specific specs and asks vendors for their best price and delivery timeline. It issues a(n):", opts: ["RFQ", "RFP", "RFI", "SOW"] },
    { ch: "1.2", t: "mcq", q: "Meetings with prospective sellers before bids are prepared, so all vendors share a common understanding, are:", opts: ["Bidder conferences", "Phase gate reviews", "Retrospectives", "Steering committees"] },
    { ch: "1.2", t: "mcq", q: "The Definition of Done (DoD) is:", opts: ["A checklist of criteria for a deliverable to be ready for customer use", "The final sign-off document that formally closes the whole project", "The prioritized list of features planned for the next product release", "The approved baseline used to compare actual cost to plan"] },
    { ch: "1.2", t: "mcq", q: "Cost of Quality covers costs of:", opts: ["Prevention, appraisal, and failure", "Planning, execution, and closing", "Labor, materials, and overhead", "Contingency, management, and baseline"] },
    { ch: "1.2", t: "mcq", q: "Which is a characteristic of DECENTRALIZED management and decision making?", opts: ["Faster decision making and more creativity", "More standardization and more control", "Less expensive, with limited creativity", "Authority at the top of the chain of command"] },
    { ch: "1.2", t: "mcq", q: "In an environment where management is centralized, accountability is usually assigned to:", opts: ["One individual, such as the project manager", "The whole team equally, by consensus", "A rotating facilitator chosen each sprint", "The customer and the product owner"] },
    { ch: "1.2", t: "mcq", q: "\"Think before you act; build trust\" describes which emotional intelligence component?", opts: ["Self-management", "Self-awareness", "Social awareness", "Social skill"] },
    { ch: "1.2", t: "mcq", q: "Which is NOT listed as a variable that influences tailoring of leadership styles?", opts: ["Size of the project budget", "Experience with the type of project", "Maturity of the project team members", "Distributed project teams"] },
    { ch: "1.2", t: "tf", q: "Performance domains run concurrently throughout the project, regardless of how value is delivered.", a: true },
    { ch: "1.2", t: "tf", q: "Technical PM skills matter more than interpersonal skills when working with stakeholders.", a: false, why: "Interpersonal and leadership skills are maybe more important." },
    { ch: "1.2", t: "tf", q: "Projects using adaptive methods require significant stakeholder involvement.", a: true },
    { ch: "1.2", t: "tf", q: "Management reserve is set aside for identified risks.", a: false, why: "Management reserve is for unknown, unplanned in-scope work; contingency reserve is for identified risks." },
    { ch: "1.2", t: "tf", q: "Large projects generally have more process than small projects, and critical projects more than less significant ones.", a: true },
    { ch: "1.2", t: "tf", q: "The value of measurement lies in collecting and disseminating the data.", a: false, why: "It lies in the conversations about how to use the data to act." },
    { ch: "1.2", t: "tf", q: "Lagging indicators predict changes or trends in the project.", a: false },
    { ch: "1.2", t: "tf", q: "Mandatory dependencies can usually be modified.", a: false },
    { ch: "1.2", t: "tf", q: "If overall project risk is too high, the organization may choose to cancel the project.", a: true },
    { ch: "1.2", t: "tf", q: "Escalate and Accept are strategies for both threats and opportunities.", a: true },
    { ch: "1.2", t: "tf", q: "In most organizations, project managers have contracting authority.", a: false, why: "They work with contracting officers." },
    { ch: "1.2", t: "tf", q: "In adaptive scheduling, planning for future releases is kept at a high level.", a: true },
    { ch: "1.2", t: "tf", q: "An estimate can be precise without being accurate.", a: true },
    { ch: "1.2", t: "tf", q: "Physical resources include people assigned to the project.", a: false, why: "Physical resources are anything that is not a person." },
    { ch: "1.2", t: "match", q: "Match each dependency type to its description.", pairs: [["Mandatory", "Contractually required or inherent in the work"], ["Discretionary", "Based on best practices or preferences"], ["External", "Between project and non-project activities"], ["Internal", "Between project activities"]] },
    { ch: "1.2", t: "match", q: "Match each uncertainty term to its definition.", pairs: [["Uncertainty", "Lack of understanding and awareness of issues or solutions"], ["Ambiguity", "Unclear, hard to identify causes, multiple options"], ["Complexity", "Hard to manage due to human and system behavior"], ["Volatility", "Possibility of rapid and unpredictable change"], ["Risk", "Uncertain event with a positive or negative effect"]] },
    { ch: "1.2", t: "match", q: "Match each threat strategy to its opportunity counterpart.", pairs: [["Avoid", "Exploit"], ["Transfer", "Share"], ["Mitigate", "Enhance"]] },
    { ch: "1.2", t: "match", q: "Match each metric category to an example.", pairs: [["Deliverable metrics", "Errors or defects"], ["Delivery", "Work in progress, lead time"], ["Baseline performance", "Schedule variance"], ["Resources", "Planned vs actual utilization"], ["Business value", "ROI, NPV"], ["Stakeholders", "Net Promoter Score"], ["Forecasts", "Estimate at completion"]] },
    { ch: "1.2", t: "match", q: "Match each complexity technique to what it does.", pairs: [["Decoupling", "Disconnect parts of the system"], ["Simulation", "Learn from analogous scenarios"], ["Diversity", "View the system from many perspectives"], ["Balance", "Mix forecasting and past data"], ["Iterate", "Add features one at a time"], ["Fail safe", "Build in redundancy"]] },
    { ch: "1.2", t: "match", q: "Match each bid document to its scenario.", pairs: [["RFI", "Learn what technologies and vendors exist"], ["RFP", "Invite vendors to bid on building a solution"], ["RFQ", "Get the best price for a known item"]] },
    { ch: "1.2", t: "list", q: "List the 8 project performance domains.", need: 8, items: [["Stakeholders", ["stakeholder"]], ["Team", ["team"]], ["Development approach & life cycle", ["development approach", "life cycle", "lifecycle", "development"]], ["Planning", ["plan"]], ["Project work", ["project work", "work"]], ["Delivery", ["deliver"]], ["Measurement", ["measur"]], ["Uncertainty", ["uncertain"]]] },
    { ch: "1.2", t: "list", q: "List the five strategies for dealing with threats.", need: 5, items: [["Avoid", ["avoid"]], ["Escalate", ["escalat"]], ["Transfer", ["transfer"]], ["Mitigate", ["mitigat"]], ["Accept", ["accept"]]] },
    { ch: "1.2", t: "list", q: "List the five strategies for dealing with opportunities.", need: 5, items: [["Exploit", ["exploit"]], ["Escalate", ["escalat"]], ["Share", ["share", "sharing"]], ["Enhance", ["enhanc"]], ["Accept", ["accept"]]] },
    { ch: "1.2", t: "list", q: "List any 6 factors associated with high-performing project teams.", need: 6, items: [["Open communication", ["communicat"]], ["Shared understanding", ["understanding"]], ["Shared ownership", ["ownership"]], ["Trust", ["trust"]], ["Collaboration", ["collaborat"]], ["Adaptability", ["adapt"]], ["Resilience", ["resilien"]], ["Empowerment", ["empower"]], ["Recognition", ["recogni"]]] },
    { ch: "1.2", t: "list", q: "List the four components of emotional intelligence.", need: 4, items: [["Self-awareness", ["self awareness"]], ["Self-management", ["self management", "self regulation"]], ["Social awareness", ["social awareness", "empathy"]], ["Social skill", ["social skill"]]] },
    { ch: "1.2", t: "list", q: "List the characteristics of effective metrics (SMART, as defined in this course).", need: 5, items: [["Specific", ["specific"]], ["Meaningful", ["meaningful"]], ["Achievable", ["achievable", "attainable"]], ["Relevant", ["relevant"]], ["Timely", ["timely"]]] },
    { ch: "1.2", t: "list", q: "List the common categories of metrics (what to measure).", need: 7, items: [["Deliverable metrics", ["deliverable"]], ["Delivery", ["delivery"]], ["Baseline performance", ["baseline"]], ["Resources", ["resource"]], ["Business value", ["business value", "value"]], ["Stakeholders", ["stakeholder"]], ["Forecasts", ["forecast"]]] },
    { ch: "1.2", t: "list", q: "List the four types of schedule dependencies.", need: 4, items: [["Mandatory", ["mandatory"]], ["Discretionary", ["discretion"]], ["External", ["external"]], ["Internal", ["internal"]]] },
    { ch: "1.2", t: "list", q: "List the 5 steps of predictive schedule planning in order.", need: 5, items: [["Decompose scope into activities", ["decompos"]], ["Sequence activities", ["sequenc"]], ["Estimate effort, duration, resources", ["estimat"]], ["Allocate people and resources", ["allocat", "assign"]], ["Adjust until agreed", ["adjust", "agreed"]]] },
    { ch: "1.2", t: "list", q: "List the product/service variables that influence the choice of development approach (any 5).", need: 5, items: [["Degree of innovation", ["innovation"]], ["Requirements certainty", ["certainty", "requirement"]], ["Scope stability", ["stability", "scope"]], ["Ease of change", ["ease of change", "ease"]], ["Delivery options", ["delivery option", "delivery"]], ["Risk", ["risk"]], ["Safety requirements", ["safety"]], ["Regulations", ["regulat"]]] },
    { ch: "1.2", t: "list", q: "List the three ways of presenting information in the Measurement domain.", need: 3, items: [["Dashboards", ["dashboard"]], ["Information radiators", ["radiator"]], ["Visual controls", ["visual control", "task board", "burn"]]] },
    { ch: "1.2", t: "list", q: "List the 5 common aspects of project team development.", need: 5, items: [["Vision and objectives", ["vision", "objective"]], ["Roles and responsibilities", ["role", "responsib"]], ["Project team operations", ["operation"]], ["Guidance", ["guidance"]], ["Growth", ["growth", "grow"]]] },
    { ch: "1.2", t: "short", q: "Define a stakeholder (PMBOK).", groups: [["individual, group, or organization", ["individual", "group", "organization"]], ["affect", ["affect"]], ["be affected / perceive", ["affected", "perceive"]], ["decision, activity, or outcome", ["decision", "activity", "outcome"]]], model: "An individual, group, or organization that may affect, be affected by, or perceive itself to be affected by a decision, activity, or outcome of a project, program, or portfolio." },
    { ch: "1.2", t: "short", q: "Differentiate contingency reserve from management reserve.", groups: [["contingency → identified / known risks", ["identified", "known"]], ["management → unknown / unexpected", ["unknown", "unexpected", "unplanned"]], ["PM controls contingency", ["project manager", "pm"]], ["upper management controls management reserve", ["upper management", "senior management", "top management", "sponsor", "upper"]]], model: "Contingency reserve covers identified risks and is controlled by the PM; management reserve covers unknown, unplanned in-scope work and is usually controlled by upper management." },
    { ch: "1.2", t: "short", q: "What is the difference between leading and lagging indicators? Give an example of each.", groups: [["leading → predict / proactive", ["predict", "proactive", "trend"]], ["lagging → after the fact / reactive", ["after", "reactive", "backward"]], ["leading example", ["scope change", "workload"]], ["lagging example", ["cost variance", "deliverables completed", "satisfaction"]]], model: "Leading indicators are proactive and predict changes or trends (rate of scope change requests, workload balance). Lagging indicators are reactive and measure after the fact (cost variance, deliverables completed, customer satisfaction)." },

    /* ===================================================== CH 1.3 */
    { ch: "1.3", t: "mcq", q: "Tailoring is defined as:", opts: ["The deliberate adaptation of the approach, governance and processes to the environment", "The selection of a single standard methodology applied to every project in the firm", "The process of breaking the project scope into smaller, manageable work packages", "The negotiation of contract terms and conditions with external vendors and suppliers"] },
    { ch: "1.3", t: "mcq", q: "What is the correct order of the tailoring process?", opts: ["Select initial approach → tailor for organization → tailor for project → ongoing improvement", "Tailor for project → select initial approach → tailor for organization → ongoing improvement", "Select initial approach → tailor for project → tailor for organization → ongoing improvement", "Tailor for organization → tailor for project → select initial approach → ongoing improvement"] },
    { ch: "1.3", t: "mcq", q: "\"A thinking strategy to explain a process, framework, or phenomenon\" is a(n):", opts: ["Model", "Method", "Artifact", "Baseline"] },
    { ch: "1.3", t: "mcq", q: "A template, document, output, or project deliverable is a(n):", opts: ["Artifact", "Model", "Method", "Principle"] },
    { ch: "1.3", t: "mcq", q: "Which model helps determine whether to use Waterfall, Agile, or a hybrid approach?", opts: ["Stacey matrix", "Salience model", "OSCAR model", "Tuckman ladder"] },
    { ch: "1.3", t: "mcq", q: "Which model is a stakeholder analysis tool used to prioritize stakeholders?", opts: ["Salience model", "Cynefin framework", "ADKAR model", "Drexler/Sibbet model"] },
    { ch: "1.3", t: "mcq", q: "Which model maps seven stages: orientation, trust building, goal clarification, commitment, implementation, high performance, renewal?", opts: ["Drexler/Sibbet team performance", "Tuckman ladder", "Virginia Satir change model", "8-step process for leading change"] },
    { ch: "1.3", t: "mcq", q: "Which change model focuses on individual transformation?", opts: ["ADKAR", "Transition model", "Cynefin", "Stacey matrix"] },
    { ch: "1.3", t: "mcq", q: "Which is a HYGIENE factor rather than a motivational factor?", opts: ["Salary", "Achievement", "Recognition", "Personal growth"] },
    { ch: "1.3", t: "mcq", q: "Building a data center using a predictive approach for construction and an iterative one for computing capabilities is, at project level:", opts: ["A hybrid approach", "A predictive approach", "An adaptive approach", "Continuous delivery"] },
    { ch: "1.3", t: "mcq", q: "The team faces long delays waiting for approvals. The suggested tailoring is:", opts: ["Streamline approvals through fewer people authorized up to value thresholds", "Add more verification steps and feedback loops before each formal approval", "Use value stream mapping and kanban boards to visualize the work", "Explore root causes to find gaps in the project's processes"] },
    { ch: "1.3", t: "mcq", q: "Too much work in progress or high rates of scrap. The suggested tailoring is:", opts: ["Value stream mapping and kanban boards", "More guidance, training, and verification", "Deeper stakeholder engagement", "Fewer people authorized to approve"] },
    { ch: "1.3", t: "mcq", q: "Which is NOT a benefit of tailoring listed in the slides?", opts: ["Strict use of one process for every project", "More commitment from team members", "Customer-oriented focus", "More efficient use of project resources"] },
    { ch: "1.3", t: "mcq", q: "Business case, roadmap, and project vision statement are examples of:", opts: ["Strategy artifacts", "Logs and registers", "Baseline artifacts", "Hierarchy charts"] },
    { ch: "1.3", t: "mcq", q: "Theory X, Theory Y, and Theory Z belong to which family of models?", opts: ["Motivational models", "Change models", "Complexity models", "Communication models"] },
    { ch: "1.3", t: "mcq", q: "Tailoring engagement for the people involved includes:", opts: ["People, empowerment, integration", "Added, modified, removed, blended", "Tools, methods, and artifacts", "Buy-in, trust, and culture"] },
    { ch: "1.3", t: "tf", q: "Tailoring is a single, one-time exercise done at the start of the project.", a: false, why: "Review points, phase gates and retrospectives keep tailoring going (ongoing improvement)." },
    { ch: "1.3", t: "tf", q: "A nuclear reactor project needs more rigor, checks and reporting than a new office building.", a: true },
    { ch: "1.3", t: "tf", q: "The models, methods and artifacts listed are exhaustive and prescriptive.", a: false },
    { ch: "1.3", t: "tf", q: "Teams should avoid models or artifacts that cater to individual needs over the team's.", a: true },
    { ch: "1.3", t: "tf", q: "Organizational leaders can impose tool constraints the project team cannot change.", a: true },
    { ch: "1.3", t: "tf", q: "The Cynefin framework helps avoid applying rigid processes to unpredictable projects.", a: true },
    { ch: "1.3", t: "tf", q: "Using models, methods, and artifacts has no associated cost.", a: false, why: "Costs: time, expertise, impact on productivity." },
    { ch: "1.3", t: "tf", q: "Access to the customer is one of the project team considerations when tailoring.", a: true },
    { ch: "1.3", t: "match", q: "Match each model to its family.", pairs: [["Situational Leadership II", "Situational leadership"], ["Gulf of execution and evaluation", "Communication"], ["Hygiene and motivational factors", "Motivational"], ["ADKAR", "Change"], ["Cynefin framework", "Complexity"], ["Tuckman ladder", "Team development"]] },
    { ch: "1.3", t: "match", q: "Match each situation to the tailoring suggestion.", pairs: [["Poor quality deliverables", "Add feedback verification loops and QA steps"], ["Team unsure how to proceed", "Add guidance, training, verification"], ["Stakeholders not engaged", "Deeper engagement, not just communication"], ["Lack of visibility of progress", "Collect, share and discuss measures"], ["Issues keep surprising the team", "Explore root causes and process gaps"]] },
    { ch: "1.3", t: "match", q: "Match each tailoring step to what happens in it.", pairs: [["Select initial approach", "Choose the approach best suited to the endeavor"], ["Tailor for the organization", "Modify based on organizational modifications"], ["Tailor for the project", "Adjust for size, criticality, other factors"], ["Implement ongoing improvement", "Inspect and adapt"]] },
    { ch: "1.3", t: "list", q: "List the 4 steps of the tailoring process.", need: 4, items: [["Select initial development approach", ["select", "initial"]], ["Tailor for the organization", ["organization"]], ["Tailor for the project", ["for the project", "project"]], ["Implement ongoing improvement", ["improvement", "ongoing"]]] },
    { ch: "1.3", t: "list", q: "List the 5 project aspects that can be tailored.", need: 5, items: [["Life cycle & development approach", ["life cycle", "lifecycle", "development approach"]], ["Processes", ["process"]], ["Engagement", ["engagement"]], ["Tools", ["tool"]], ["Methods & artifacts", ["method", "artifact"]]] },
    { ch: "1.3", t: "list", q: "Process tailoring decides which elements should be... (list 5).", need: 5, items: [["Added", ["add"]], ["Modified", ["modif"]], ["Removed", ["remov"]], ["Blended", ["blend"]], ["Aligned", ["align"]]] },
    { ch: "1.3", t: "list", q: "List the three benefits of tailoring.", need: 3, items: [["Commitment from team members", ["commitment", "commit"]], ["Customer-oriented focus", ["customer"]], ["Efficient use of resources", ["efficien", "resource"]]] },
    { ch: "1.3", t: "list", q: "List any 4 of the competing demands a project must balance.", need: 4, items: [["Deliver quickly", ["quick", "fast", "speed"]], ["Minimize costs", ["cost"]], ["Optimize value", ["value"]], ["High-quality deliverables", ["quality"]], ["Regulatory compliance", ["complian", "regulat"]], ["Stakeholder expectations", ["stakeholder", "expectation"]], ["Adapting to change", ["adapt", "change"]]] },
    { ch: "1.3", t: "list", q: "List any 4 product/deliverable attributes that influence tailoring for the project.", need: 4, items: [["Compliance/criticality", ["complian", "critical"]], ["Type of product", ["type"]], ["Industry market", ["industry", "market"]], ["Technology", ["technolog"]], ["Time frame", ["time frame", "timeframe", "time"]], ["Stability of requirements", ["stabil", "requirement"]], ["Security", ["secur"]]] },
    { ch: "1.3", t: "list", q: "List the 5 project team considerations when tailoring for the project.", need: 5, items: [["Team size", ["size"]], ["Team geography", ["geograph", "location"]], ["Organizational distribution", ["distribut"]], ["Team experience", ["experience"]], ["Access to customer", ["customer", "access"]]] },
    { ch: "1.3", t: "list", q: "List the four things teams should avoid when choosing models, methods, and artifacts.", need: 4, items: [["Duplicates / unnecessary effort", ["duplicat", "unnecessary"]], ["Not useful", ["not useful", "useful"]], ["Incorrect or misleading info", ["incorrect", "misleading"]], ["Caters to individual needs", ["individual"]]] },
    { ch: "1.3", t: "list", q: "List Maslow's hierarchy of needs from bottom to top.", need: 5, items: [["Physiological", ["physiolog"]], ["Safety", ["safety", "security"]], ["Love / belonging", ["love", "belong", "social"]], ["Esteem", ["esteem"]], ["Self-actualization", ["actualization", "self actual", "realization"]]] },
    { ch: "1.3", t: "list", q: "List the four categories of commonly used methods.", need: 4, items: [["Data gathering & analysis", ["data", "analysis", "gathering"]], ["Estimating", ["estimat"]], ["Meetings & events", ["meeting", "event"]], ["Other methods", ["other"]]] },
    { ch: "1.3", t: "short", q: "Define model, method, and artifact.", groups: [["model = thinking strategy", ["thinking", "strategy", "explain"]], ["method = means for achieving", ["means", "achiev"]], ["artifact = template, document, output, deliverable", ["template", "document", "output", "deliverable"]]], model: "A model is a thinking strategy to explain a process, framework, or phenomenon. A method is the means for achieving an outcome, output, result, or deliverable. An artifact is a template, document, output, or project deliverable." },
    { ch: "1.3", t: "short", q: "What does tailoring consider in a project environment?", groups: [["development approach", ["development approach", "approach"]], ["processes", ["process"]], ["life cycle", ["life cycle", "lifecycle"]], ["deliverables", ["deliverable"]], ["people to engage", ["people", "engage"]]], model: "The development approach, processes, project life cycle, deliverables, and the choice of people with whom to engage." },

    /* ===================================================== CH 2 */
    { ch: "2", t: "mcq", q: "Strategic management is:", opts: ["The science of formulating, implementing and evaluating cross-functional decisions", "The process of assigning experienced project managers to the organization's projects", "The control of project budgets by the accountant and top management", "The analysis of stakeholder interests and their influence over projects"] },
    { ch: "2", t: "mcq", q: "In Table 2.1, the strategy \"matching or improving on competitors' products and services\" maps to:", opts: ["Reverse engineering projects", "Concurrent engineering projects", "Reengineering projects", "Enterprise IT efforts"] },
    { ch: "2", t: "mcq", q: "\"New business processes for greater streamlining and efficiency\" maps to which project type?", opts: ["Reengineering projects", "New product lines", "Reverse engineering projects", "Construction of new plants"] },
    { ch: "2", t: "mcq", q: "\"Promotion of cross-functional interaction and streamlining of new product introduction\" maps to:", opts: ["Concurrent engineering projects", "Enterprise IT efforts", "New product development", "Negotiation with supply chain"] },
    { ch: "2", t: "mcq", q: "What went wrong for the Airbus A380?", opts: ["Airbus bet on much bigger planes while traffic favored medium wide-body jets", "Boeing copied the A380 design and released a cheaper version of it first", "Air traffic fell sharply after 2000 instead of doubling as expected", "Airports refused to certify the aircraft because of noise regulations"] },
    { ch: "2", t: "mcq", q: "In the TOWS matrix, projects that use strengths to maximize opportunities follow which strategy?", opts: ["SO, Maxi-Maxi", "ST, Maxi-Mini", "WO, Mini-Maxi", "WT, Mini-Mini"] },
    { ch: "2", t: "mcq", q: "Projects that minimize weaknesses and avoid threats follow which TOWS strategy?", opts: ["WT, Mini-Mini", "WO, Mini-Maxi", "ST, Maxi-Mini", "SO, Maxi-Maxi"] },
    { ch: "2", t: "mcq", q: "External stakeholders with the power to intervene and disrupt a project, like environmental groups opposing Keystone XL, are called:", opts: ["Intervenor groups", "Functional managers", "Parent organizations", "Resource pools"] },
    { ch: "2", t: "mcq", q: "Which stakeholder supports and actively monitors project budgets?", opts: ["Accountant", "Clients", "Top management", "Competitors"] },
    { ch: "2", t: "mcq", q: "Which stakeholder wants the project delivered quickly so the money invested starts generating returns?", opts: ["Clients", "Accountant", "Project team", "Suppliers"] },
    { ch: "2", t: "mcq", q: "Which is an INTERNAL stakeholder?", opts: ["Other functional managers", "Suppliers and distributors", "Competitors", "Environmental intervenor groups"] },
    { ch: "2", t: "mcq", q: "Which structure creates a dual hierarchy where functions and projects have equal prominence?", opts: ["Matrix", "Functional", "Project", "Heavyweight"] },
    { ch: "2", t: "mcq", q: "Which is a WEAKNESS of functional structures?", opts: ["Lack of customer focus", "Rapid response to market opportunities", "Maximizes scarce resources", "Allows for standard career paths"] },
    { ch: "2", t: "mcq", q: "\"Team member concern about the future once the project ends\" is a weakness of:", opts: ["Project structures", "Functional structures", "Matrix structures", "PMOs"] },
    { ch: "2", t: "mcq", q: "Lockheed's small autonomous team of hand-picked experts with a fully empowered PM is known as:", opts: ["Skunk Works", "A weather station PMO", "A controlling PMO", "A balanced matrix"] },
    { ch: "2", t: "mcq", q: "In the survey (Fig 2.8), which structure was rated most effective for construction projects?", opts: ["Project matrix", "Project organization", "Functional matrix", "Functional organization"], why: "For new product development, the project organization was rated highest." },
    { ch: "2", t: "mcq", q: "A PMO situated at the corporate level, serving an overall support function, is at:", opts: ["Level 3", "Level 2", "Level 1", "Level 0"] },
    { ch: "2", t: "mcq", q: "Which PMO form exercises moderate control by requiring compliance with adopted PM standards?", opts: ["Controlling", "Supportive", "Directive", "Weather station"] },
    { ch: "2", t: "mcq", q: "A PMO used only to monitor and track project status, without trying to influence projects, follows which model?", opts: ["Weather station", "Control tower", "Resource pool", "Directive"] },
    { ch: "2", t: "mcq", q: "Which factor affecting culture refers to \"moments when the real culture becomes visible\"?", opts: ["Critical incidents", "Key organizational members", "Reward systems", "Rules and procedures"] },
    { ch: "2", t: "mcq", q: "Team members give wide estimates to protect themselves because the culture punishes lateness. Which effect of culture is this?", opts: ["Project planning", "Departmental interaction", "Performance evaluation", "Employee commitment to goals"] },
    { ch: "2", t: "mcq", q: "Compared with GE's jet engine division, Rolls-Royce's culture is described as:", opts: ["Paternalistic, rewarding loyalty and long tenure", "Competitive and high-pressure with high burnout", "Adversarial between functional departments", "Cautious, rewarding playing it safe"] },
    { ch: "2", t: "tf", q: "Projects are the key ingredients in strategy implementation.", a: true },
    { ch: "2", t: "tf", q: "Matrix structures are suited to dynamic environments.", a: true },
    { ch: "2", t: "tf", q: "Project structures make it easy to maintain a pooled supply of intellectual capital.", a: false, why: "It's a weakness: contractors are hired temporarily and then leave." },
    { ch: "2", t: "tf", q: "In a project organization, each project is a self-contained business unit with a dedicated team.", a: true },
    { ch: "2", t: "tf", q: "A supportive PMO has high control and directly manages projects.", a: false, why: "That is a directive PMO. Supportive = low control, consultative." },
    { ch: "2", t: "tf", q: "An organization's culture is always shared companywide.", a: false, why: "Held by some subset; may or may not be companywide." },
    { ch: "2", t: "tf", q: "Projects developed within a functional structure require no disruption or change to the firm's design.", a: true },
    { ch: "2", t: "tf", q: "Using a PMO as a resource center shifts some PM burden from the project manager to support staff.", a: true },
    { ch: "2", t: "tf", q: "Top management controls project managers and regulates their freedom of action.", a: true },
    { ch: "2", t: "tf", q: "Cultures that adopt a disinterested or adversarial relationship between functional groups and projects are more successful.", a: false },
    { ch: "2", t: "match", q: "Match each organizational structure to its definition.", pairs: [["Functional", "Groups people performing similar activities into departments"], ["Project", "Groups people into teams on temporary assignments"], ["Matrix", "Dual hierarchy with equal prominence for functions and projects"]] },
    { ch: "2", t: "match", q: "Match each strength to its structure.", pairs: [["In-depth knowledge and intellectual capital", "Functional"], ["Rapid response to market opportunities", "Project"], ["Maximizes scarce resources", "Matrix"]] },
    { ch: "2", t: "match", q: "Match each PMO form to its level of control.", pairs: [["Supportive", "Low control: consultative, resources and training"], ["Controlling", "Moderate control: compliance with standards"], ["Directive", "High control: directly manages projects"]] },
    { ch: "2", t: "match", q: "Match each PMO model to its purpose.", pairs: [["Weather station", "Monitoring and tracking only"], ["Control tower", "Protect and improve PM methodology"], ["Resource pool", "Supply skilled project professionals"]] },
    { ch: "2", t: "match", q: "Match each strategy to the project that reflects it (Table 2.1).", pairs: [["Technical or operating initiatives", "New plants or modernized facilities"], ["Greater market penetration", "New product development"], ["New strategic alliances", "Negotiation with supply chain members"], ["Supply chain communication and efficiency", "Enterprise IT efforts"], ["Change in strategic direction", "New product lines"]] },
    { ch: "2", t: "match", q: "Match each TOWS cell to its strategy name.", pairs: [["SO", "Maxi-Maxi"], ["ST", "Maxi-Mini"], ["WO", "Mini-Maxi"], ["WT", "Mini-Mini"]] },
    { ch: "2", t: "list", q: "List the four elements of strategic management.", need: 4, items: [["Vision and mission statements", ["vision", "mission"]], ["Formulating, implementing, evaluating", ["formulat", "implement", "evaluat"]], ["Cross-functional decisions", ["cross functional", "decision"]], ["Achieving objectives", ["achiev", "objective"]]] },
    { ch: "2", t: "list", q: "List the three key elements of organizational structure.", need: 3, items: [["Formal reporting relationships", ["report", "hierarch", "span of control"]], ["Groupings of individuals/departments", ["group", "department"]], ["Systems for communication, coordination, integration", ["communicat", "coordinat", "integrat", "system"]]] },
    { ch: "2", t: "list", q: "List the four internal project stakeholders.", need: 4, items: [["Top management", ["top management", "top"]], ["Accountant", ["accountant", "accounting"]], ["Other functional managers", ["functional manager", "functional"]], ["Project team members", ["team"]]] },
    { ch: "2", t: "list", q: "List the four external project stakeholders.", need: 4, items: [["Clients", ["client", "customer"]], ["Competitors", ["competitor"]], ["Suppliers", ["supplier"]], ["Intervenor groups", ["intervenor", "environmental", "political", "consumer"]]] },
    { ch: "2", t: "list", q: "List the weaknesses of functional structures for project management.", need: 4, items: [["Functional siloing", ["silo"]], ["Lack of customer focus", ["customer"]], ["Longer time to complete projects", ["longer", "time", "slow"]], ["Varying interest or commitment", ["interest", "commitment"]]] },
    { ch: "2", t: "list", q: "List any 4 strengths of project structures.", need: 4, items: [["PM sole authority", ["authority"]], ["Improved communication", ["communicat"]], ["Effective decision making", ["decision"]], ["Creation of PM experts", ["expert"]], ["Rapid response to market", ["rapid", "market"]]] },
    { ch: "2", t: "list", q: "List the weaknesses of matrix structures.", need: 3, items: [["Two bosses (dual hierarchy)", ["two boss", "boss", "dual"]], ["Negotiation to share resources", ["negotiat"]], ["Workers caught between competing demands", ["caught", "competing"]]] },
    { ch: "2", t: "list", q: "List the three forms of PMOs.", need: 3, items: [["Supportive", ["support"]], ["Controlling", ["controlling"]], ["Directive", ["directive"]]] },
    { ch: "2", t: "list", q: "List the three models of PMOs.", need: 3, items: [["Weather station", ["weather"]], ["Control tower", ["tower"]], ["Resource pool", ["pool"]]] },
    { ch: "2", t: "list", q: "List the four parts of the definition of organizational culture.", need: 4, items: [["Unwritten", ["unwritten"]], ["Rules of behavior", ["rules", "behavior", "norm"]], ["Held by some subset", ["subset"]], ["Taught to new members", ["taught", "new member"]]] },
    { ch: "2", t: "list", q: "List any 5 key factors that affect the development of culture.", need: 5, items: [["Technology", ["technolog"]], ["Environment", ["environment"]], ["Geographical location", ["geograph", "location"]], ["Reward systems", ["reward"]], ["Rules and procedures", ["rules", "procedure"]], ["Key organizational members", ["key", "member"]], ["Critical incidents", ["critical", "incident"]]] },
    { ch: "2", t: "list", q: "List the four ways culture affects project management.", need: 4, items: [["Departmental interaction", ["department", "interaction"]], ["Employee commitment to goals", ["commitment", "employee"]], ["Project planning", ["planning", "estimat"]], ["Performance evaluation", ["evaluat", "performance"]]] },
    { ch: "2", t: "list", q: "PMOs act as resource centers for... (list 4).", need: 4, items: [["Technical details", ["technical"]], ["Expertise", ["expertise"]], ["Repository", ["repositor"]], ["Center for excellence", ["excellence"]]] },
    { ch: "2", t: "short", q: "Define project stakeholders (Pinto, chapter 2).", groups: [["individuals or groups", ["individual", "group"]], ["active stake", ["stake"]], ["impact the project", ["impact", "affect", "influence"]], ["positively or negatively", ["positive", "negative"]]], model: "All individuals or groups who have an active stake in the project and can potentially impact, either positively or negatively, its development." },
    { ch: "2", t: "short", q: "Define organizational culture.", groups: [["unwritten rules / norms", ["unwritten", "norm", "rules"]], ["shape and guide behavior", ["behavior"]], ["shared by a subset", ["shared", "subset"]], ["taught to new members", ["taught", "new member"]]], model: "The unwritten rules of behavior, or norms, used to shape and guide behavior, shared by some subset of organizational members and taught to all new members." },

    /* ===================================================== CH 3 */
    { ch: "3", t: "mcq", q: "According to McConnell, software projects fail because the team lacks:", opts: ["The knowledge or the resolve to conduct the project", "A large enough budget or enough calendar time", "Modern tools or a formal methodology", "Executive sponsorship or customer access"] },
    { ch: "3", t: "mcq", q: "Influence based on specialized knowledge or skills is:", opts: ["Expert", "Referent", "Formal (legitimate)", "Reward"] },
    { ch: "3", t: "mcq", q: "Influence based on personal traits, charisma, or likability is:", opts: ["Referent", "Expert", "Penalty (coercive)", "Formal (legitimate)"] },
    { ch: "3", t: "mcq", q: "In Tuckman's model, which stage involves chaotic competing for leadership and trials of group processes?", opts: ["Storming", "Forming", "Norming", "Performing"] },
    { ch: "3", t: "mcq", q: "A team formed to fix a showstopper defect has which objective?", opts: ["Problem resolution", "Creativity", "Tactical execution", "Adjourning"] },
    { ch: "3", t: "mcq", q: "Which structure suits a tactical execution team?", opts: ["Hierarchical or matrix with tight controls", "Looser hierarchy with diverse skills", "Flexible roles in a temporary task force", "Self-organizing with a rotating lead"] },
    { ch: "3", t: "mcq", q: "Vulnerability-based trust means:", opts: ["Admitting mistakes, asking for help, saying \"I don't know\"", "Trusting only teammates who have proven themselves before", "Sharing salaries and performance reviews openly with all", "Letting the manager approve every decision the team makes"] },
    { ch: "3", t: "mcq", q: "Groupthink is best described as:", opts: ["A cohesive group prioritizing harmony over critical thinking", "A team debating issues openly before reaching a decision", "A manager imposing decisions on the group by authority", "Members tracking their own time to improve estimates"] },
    { ch: "3", t: "mcq", q: "\"Reach a middle ground by mutual concessions\" is which conflict technique?", opts: ["Compromising", "Smoothing", "Collaborating", "Forcing"] },
    { ch: "3", t: "mcq", q: "\"Preserve harmony by downplaying differences\" is which conflict technique?", opts: ["Smoothing (accommodating)", "Withdrawal (avoidance)", "Confronting (problem solving)", "Compromising"] },
    { ch: "3", t: "mcq", q: "Conflict differs from disagreement because conflict involves:", opts: ["A hardening of position and intractability", "Two parties with different technical opinions", "A vote that ends in a narrow majority", "A discussion that runs over its timebox"] },
    { ch: "3", t: "mcq", q: "In RACI, the A stands for:", opts: ["Accountable", "Approved", "Assigned", "Assisting"] },
    { ch: "3", t: "mcq", q: "A skills matrix shows:", opts: ["Resources on one axis and skills on the other", "Activities on one axis and RACI roles on the other", "Risks on one axis and their probability on the other", "Tasks on one axis and their durations on the other"] },
    { ch: "3", t: "mcq", q: "The chief programmer (surgical) team came from:", opts: ["IBM in the 1970s", "Lockheed in the 1940s", "Microsoft in the 1990s", "Extreme Programming"] },
    { ch: "3", t: "mcq", q: "In a chief programmer team, who manages documentation, version control, and technical records?", opts: ["Program clerk", "Toolsmith", "Language lawyer", "Administrator"] },
    { ch: "3", t: "mcq", q: "The main drawback of a skunk works team is:", opts: ["Little visibility into team progress", "Low ownership and buy-in", "Too much management oversight", "Skills that don't match the goal"] },
    { ch: "3", t: "mcq", q: "A highly skilled team whose skills tightly match the goal, like a security team, is a:", opts: ["SWAT team", "Skunk works team", "Business team", "Democratic team"] },
    { ch: "3", t: "mcq", q: "With 50 programmers, roughly how many communication paths are possible?", opts: ["1,200", "50", "250", "2,500"] },
    { ch: "3", t: "mcq", q: "The optimal team size given in the slides is:", opts: ["4–6 developers plus a tech lead", "10–12 developers plus a tech lead", "2 developers working in a pair", "Up to 20 if communication is formal"] },
    { ch: "3", t: "mcq", q: "How is an engineer's time distributed, per the slides?", opts: ["50% interaction, 30% alone, 20% non-productive", "30% interaction, 50% alone, 20% non-productive", "20% interaction, 60% alone, 20% non-productive", "40% interaction, 40% alone, 20% non-productive"] },
    { ch: "3", t: "mcq", q: "\"The work is a means to an end, such as getting rich or traveling\" describes which personality type?", opts: ["Self-oriented", "Task-oriented", "Interaction-oriented", "Achievement-oriented"] },
    { ch: "3", t: "mcq", q: "Programming language experience is normally significant only for:", opts: ["Short projects with no time to learn a new language", "Projects involving low-level or embedded programming", "Long projects with many developers on the team", "Projects in a new application domain"] },
    { ch: "3", t: "mcq", q: "\"People prefer to work in natural light\" is which environmental factor?", opts: ["Outside awareness", "Privacy", "Personalization", "Comfort"] },
    { ch: "3", t: "mcq", q: "Saying \"This testing regime lets too many bugs slip through; what can we do?\" instead of blaming people illustrates:", opts: ["Review process and products, not people", "Coordinate, don't manipulate", "Gain visibility without micromanagement", "Channel people, don't dam them"] },
    { ch: "3", t: "mcq", q: "Adaptive leadership is needed when:", opts: ["The problem cannot be solved by known means", "The team already knows the best practice to apply", "The leader has the most technical expertise", "A decision must be made by majority vote"] },
    { ch: "3", t: "mcq", q: "In technical leadership, the main tool for motivation is:", opts: ["Personality (charisma, expertise, confidence)", "Progress (learning, iteration, visible movement)", "Sense of purpose and shared meaning", "Financial incentives and bonuses"] },
    { ch: "3", t: "mcq", q: "Which project role \"produces a superior product\"?", opts: ["Development leader", "Team leader", "Project manager", "Expert"] },
    { ch: "3", t: "mcq", q: "Recognition of achievements and appropriate rewards satisfy which need?", opts: ["Esteem", "Social", "Self-realization", "Safety"] },
    { ch: "3", t: "mcq", q: "\"Estimating\" as a people-related management activity means estimating:", opts: ["How fast people will work", "What people are going to do", "The way in which people work", "People's activities"] },
    { ch: "3", t: "mcq", q: "Passive/aggressive agreement in consensus building is:", opts: ["Subsumed conflict", "True buy-in", "A simple majority", "Healthy debate"] },
    { ch: "3", t: "tf", q: "Lower-level needs must be satisfied before higher-level needs can be addressed.", a: true },
    { ch: "3", t: "tf", q: "Physiological and safety needs are the most significant from a managerial viewpoint.", a: false, why: "They're assumed satisfied; social, esteem and self-realization matter most." },
    { ch: "3", t: "tf", q: "Democratic leadership is more effective than autocratic leadership.", a: true },
    { ch: "3", t: "tf", q: "Democratic teams work best when all members are experienced and competent.", a: true },
    { ch: "3", t: "tf", q: "In XP, programmers work in pairs and take collective responsibility for the code.", a: true },
    { ch: "3", t: "tf", q: "Providing individual offices has been shown to decrease productivity.", a: false, why: "It increases productivity." },
    { ch: "3", t: "tf", q: "Communication channeled through a central coordinator tends to be effective.", a: false },
    { ch: "3", t: "tf", q: "Simple majority rule is the best way to decide on a small team.", a: false, why: "It can be detrimental where everyone's commitment is essential." },
    { ch: "3", t: "tf", q: "Buy-in requires consensus.", a: false, why: "Members can disagree and still commit." },
    { ch: "3", t: "tf", q: "Accountability on a strong team occurs directly among peers.", a: true },
    { ch: "3", t: "tf", q: "There is agreement that psychological and aptitude tests are useful in staff selection.", a: false },
    { ch: "3", t: "tf", q: "Detailed individual time tracking in PSP is a monitoring activity.", a: false, why: "It is awareness-building, not monitoring." },
    { ch: "3", t: "tf", q: "Leadership depends on respect, not titular status.", a: true },
    { ch: "3", t: "tf", q: "Studies show financial incentives are among the most effective motivators.", a: false, why: "Among the least effective." },
    { ch: "3", t: "tf", q: "A group made entirely of task-oriented people works well because everyone focuses on the work.", a: false, why: "Everyone wants to do their own thing; an effective group balances all types." },
    { ch: "3", t: "match", q: "Match each type of influence to its basis.", pairs: [["Formal (legitimate)", "Authority from hierarchy or role"], ["Reward", "Ability to offer incentives"], ["Penalty (coercive)", "Threat or use of punishment"], ["Expert", "Specialized knowledge or skills"], ["Referent", "Charisma or likability"]] },
    { ch: "3", t: "match", q: "Match each Tuckman stage to its description.", pairs: [["Forming", "Members come together and get to know one another"], ["Storming", "Competing for leadership and influence"], ["Norming", "Agreement on how the group operates"], ["Performing", "Effective in meeting objectives"], ["Adjourning", "The group dissolves"]] },
    { ch: "3", t: "match", q: "Match each conflict technique to its description.", pairs: [["Confronting", "Resolve the root cause through open dialogue"], ["Compromising", "Mutual concessions"], ["Withdrawal", "Delay or sidestep"], ["Smoothing", "Downplay differences"], ["Collaborating", "Integrate perspectives for a creative solution"], ["Forcing", "Impose a solution through authority"]] },
    { ch: "3", t: "match", q: "Match each chief programmer team role to its job.", pairs: [["Backup programmer", "Equally skilled co-pilot, ready to step in"], ["Program clerk", "Documentation and version control"], ["Administrator", "Administrative tasks"], ["Toolsmith", "Builds and maintains development tools"], ["Language lawyer", "Expert in the programming language"]] },
    { ch: "3", t: "match", q: "Match each personality type to what happens if a whole group is that type.", pairs: [["Task-oriented", "Everyone wants to do their own thing"], ["Self-oriented", "Everyone wants to be the boss"], ["Interaction-oriented", "Too much chatting, not enough work"]] },
    { ch: "3", t: "match", q: "Match each need to how a manager satisfies it.", pairs: [["Social", "Communal facilities, informal communication"], ["Esteem", "Recognition and appropriate rewards"], ["Self-realization", "Training and responsibility"]] },
    { ch: "3", t: "match", q: "Match each leadership dimension to adaptive leadership.", pairs: [["Approach", "Problems not solved by known means"], ["Motivation driver", "Sense of purpose"], ["Tool for motivation", "Progress"]] },
    { ch: "3", t: "list", q: "List Tuckman's stages of team development.", need: 5, items: [["Forming", ["forming"]], ["Storming", ["storming"]], ["Norming", ["norming"]], ["Performing", ["performing"]], ["Adjourning / dissolving", ["adjourn", "dissolv"]]] },
    { ch: "3", t: "list", q: "List the five types of influence.", need: 5, items: [["Formal / legitimate", ["formal", "legitimate"]], ["Reward", ["reward"]], ["Penalty / coercive", ["penalty", "coercive"]], ["Expert", ["expert"]], ["Referent", ["referent"]]] },
    { ch: "3", t: "list", q: "List the six conflict resolution techniques.", need: 6, items: [["Confronting / problem solving", ["confront", "problem solving"]], ["Compromising", ["compromis"]], ["Withdrawal / avoidance", ["withdraw", "avoid"]], ["Smoothing / accommodating", ["smooth", "accommodat"]], ["Collaborating", ["collaborat"]], ["Forcing", ["forc"]]] },
    { ch: "3", t: "list", q: "List the six problem-solving steps.", need: 6, items: [["Define the root problem", ["define"]], ["Analyze the problem", ["analy"]], ["Identify solutions", ["identify"]], ["Pick a solution", ["pick", "choose", "select"]], ["Implement", ["implement"]], ["Review", ["review", "confirm"]]] },
    { ch: "3", t: "list", q: "List the levels of the team pyramid from bottom to top.", need: 5, items: [["Trust", ["trust"]], ["Managed conflict", ["conflict"]], ["Commitment", ["commitment"]], ["Accountability", ["accountab"]], ["Results", ["result"]]] },
    { ch: "3", t: "list", q: "What does RACI stand for?", need: 4, items: [["Responsible", ["responsible"]], ["Accountable", ["accountable"]], ["Consulted", ["consult"]], ["Informed", ["inform"]]] },
    { ch: "3", t: "list", q: "List the supporting roles in a chief programmer team.", need: 5, items: [["Backup programmer / co-pilot", ["backup", "co pilot", "copilot"]], ["Program clerk", ["clerk"]], ["Administrator", ["administrat"]], ["Toolsmith", ["toolsmith", "tool"]], ["Language lawyer", ["lawyer", "language"]]] },
    { ch: "3", t: "list", q: "List the problems with the chief programmer approach (any 3).", need: 3, items: [["Talented people are hard to find", ["hard to find", "talent", "exceptional"]], ["Others resent the chief", ["resent", "credit", "undermine"]], ["High risk if chief and deputy unavailable", ["unavailable", "risk"]], ["Org structures can't accommodate it", ["organizational", "grade", "structure"]]] },
    { ch: "3", t: "list", q: "List the six management activities related to people.", need: 6, items: [["Problem solving", ["problem"]], ["Motivating", ["motivat"]], ["Planning", ["plan"]], ["Estimating", ["estimat"]], ["Controlling", ["control"]], ["Organizing", ["organiz"]]] },
    { ch: "3", t: "list", q: "List the three personality types.", need: 3, items: [["Task-oriented", ["task"]], ["Self-oriented", ["self"]], ["Interaction-oriented", ["interaction"]]] },
    { ch: "3", t: "list", q: "List any 5 staff selection factors.", need: 5, items: [["Application domain experience", ["domain"]], ["Platform experience", ["platform"]], ["Programming language experience", ["language"]], ["Educational background", ["educat"]], ["Communication ability", ["communicat"]], ["Adaptability", ["adapt"]], ["Attitude", ["attitude"]], ["Personality", ["personalit"]]] },
    { ch: "3", t: "list", q: "List any 4 common errors of applying production-line efficiency to thought workers.", need: 4, items: [["Squeeze out error", ["squeeze", "error"]], ["Hard line on goofing off", ["goof", "hard line"]], ["Interchangeable workers", ["interchangeable"]], ["Optimize the steady state", ["steady"]], ["Standardize procedure", ["standardiz", "by the book"]], ["Eliminate experimentation", ["experiment"]]] },
    { ch: "3", t: "list", q: "List the five people-skill areas a project manager must develop.", need: 5, items: [["Interpersonal skills", ["interpersonal"]], ["Shaping project culture", ["culture"]], ["Managing people", ["managing"]], ["Making people better", ["better"]], ["Leadership", ["leadership"]]] },
    { ch: "3", t: "list", q: "List the five representative cultural roles.", need: 5, items: [["Leader", ["leader"]], ["Listener / talker", ["listener", "talker"]], ["Complainer / naysayer", ["complain", "naysayer"]], ["Expert", ["expert"]], ["Charger / plodder", ["charger", "plodder"]]] },
    { ch: "3", t: "list", q: "List the advantages of a cohesive group.", need: 4, items: [["Group quality standards", ["quality", "standard"]], ["Work closely, fewer inhibitions", ["inhibition", "closely", "ignorance"]], ["Learn from each other", ["learn"]], ["Egoless programming", ["egoless"]]] },
    { ch: "3", t: "list", q: "List the three environmental factors for engineers' workspaces.", need: 3, items: [["Privacy", ["privacy"]], ["Outside awareness", ["outside", "natural light"]], ["Personalization", ["personaliz"]]] },
    { ch: "3", t: "short", q: "Compare technical and adaptive leadership.", groups: [["technical → known means", ["known"]], ["adaptive → not solvable by known means", ["unknown", "not solved", "cannot", "novel", "complex"]], ["vision vs sense of purpose", ["vision", "purpose"]], ["personality vs progress", ["personality", "progress", "charisma"]]], model: "Technical leadership solves problems by known means, driven by the leader's vision and motivating through personality. Adaptive leadership tackles problems not solvable by known means, driven by a sense of purpose and motivating through progress." },
    { ch: "3", t: "short", q: "What two things does commitment require, and does it need consensus?", groups: [["clarity", ["clarity", "clear"]], ["buy-in", ["buy in", "buyin"]], ["no consensus needed", ["not require", "doesn't", "does not", "no consensus", "without"]]], model: "Commitment requires clarity and buy-in. Buy-in does not require consensus: members can disagree and still commit." },
    { ch: "3", t: "short", q: "What is the difference between disagreement and conflict, and what is the goal when resolving conflict?", groups: [["hardening of position", ["harden", "position"]], ["intractability", ["intractab", "insolvab"]], ["reduce to a disagreement", ["reduce", "disagreement"]], ["consensus / reconciliation", ["consensus", "reconcil"]]], model: "Conflict involves a hardening of position and intractability; disagreement does not. The goal is to reduce the conflict to a disagreement that can be addressed through consensus, and to reconcile the parties." },
  ];

  /* ------------------------------------------------------------ helpers */
  function el(tag, attrs, html) {
    var n = document.createElement(tag);
    if (attrs)
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") n.className = attrs[k];
        else n.setAttribute(k, attrs[k]);
      });
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function hash(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }
  function shuffled(arr, seed) {
    var a = arr.slice();
    var s = seed || 1;
    for (var i = a.length - 1; i > 0; i--) {
      s = (Math.imul(s ^ (s >>> 15), 2246822507) + 0x9e3779b9) >>> 0;
      var j = s % (i + 1);
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }

  /* ------------------------------------------------------------ keyword grader */
  function norm(s) {
    return (" " + String(s).toLowerCase() + " ")
      .replace(/&/g, " and ")
      .replace(/[’']/g, "")
      .replace(/[^a-z0-9%$]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }
  function lev(a, b) {
    if (Math.abs(a.length - b.length) > 2) return 9;
    var pp = [],
      prev = [],
      cur = [],
      i,
      j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
        // adjacent swap ("chnage") counts as one edit
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) cur[j] = Math.min(cur[j], pp[j - 2] + 1);
      }
      pp = prev;
      prev = cur;
    }
    return prev[b.length];
  }
  function wordHit(tokens, w) {
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (t === w) return true;
      if (w.length >= 4 && t.indexOf(w) === 0) return true;
      if (w.length >= 5) {
        var d = lev(t.slice(0, w.length + 1), w);
        if (d <= 1 || (w.length >= 8 && d <= 2)) return true;
        if (lev(t, w) <= 1) return true;
      }
    }
    return false;
  }
  function keyHit(tokens, key) {
    var words = norm(key).split(" ").filter(Boolean);
    if (!words.length) return false;
    return words.every(function (w) {
      return wordHit(tokens, w);
    });
  }
  function anyHit(tokens, keys) {
    return keys.some(function (k) {
      return keyHit(tokens, k);
    });
  }
  function tokensOf(text) {
    var n = norm(text);
    return n ? n.split(" ") : [];
  }

  /* ------------------------------------------------------------ state */
  var STORE = "se423-midterm-v1";
  var state = {};
  try {
    state = JSON.parse(localStorage.getItem(STORE) || "{}") || {};
  } catch (e) {
    state = {};
  }
  function save() {
    try {
      localStorage.setItem(STORE, JSON.stringify(state));
    } catch (e) {}
  }

  Q.forEach(function (q, i) {
    q.id = "q" + hash(q.ch + q.t + q.q).toString(36);
    q.n = i + 1;
  });

  /* ------------------------------------------------------------ memorize render */
  var memGrid = document.getElementById("mem-grid");
  MEM.forEach(function (m) {
    var card = el("div", { class: "card", "data-ch": m[0], style: "--hue: " + HUE[m[0]], tabindex: "0" });
    card.innerHTML =
      '<h4><span class="k">CH ' + m[0] + "</span>" + esc(m[1]) + '<span class="count">' + m[3].length + "</span></h4>" +
      '<p class="mnemo">' + esc(m[2]) + "</p><ol>" +
      m[3].map(function (x) {
        return "<li>" + esc(x) + "</li>";
      }).join("") +
      "</ol>";
    card.addEventListener("click", function () {
      card.classList.toggle("peek");
    });
    card.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        card.classList.toggle("peek");
      }
    });
    memGrid.appendChild(card);
  });
  document.querySelectorAll("[data-mem]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-mem");
      document.querySelectorAll("[data-mem]").forEach(function (x) {
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      });
      memGrid.querySelectorAll(".card").forEach(function (c) {
        c.hidden = v !== "all" && c.getAttribute("data-ch") !== v;
      });
    });
  });
  var cover = document.getElementById("cover-toggle");
  cover.addEventListener("click", function () {
    var on = cover.getAttribute("aria-pressed") !== "true";
    cover.setAttribute("aria-pressed", on ? "true" : "false");
    memGrid.classList.toggle("cover", on);
    memGrid.querySelectorAll(".card").forEach(function (c) {
      c.classList.remove("peek");
    });
  });

  /* ------------------------------------------------------------ practice render */
  var qlist = document.getElementById("qlist");
  var TYPE_NAME = { mcq: "MCQ", tf: "True / False", match: "Matching", list: "Listing", short: "Short answer" };
  var filter = { ch: "all", ty: "all", missed: false };

  function maxPts(q) {
    return q.t === "match" ? q.pairs.length : 1;
  }

  function render(q) {
    var card = el("article", { class: "q", id: q.id, style: "--hue: " + HUE[q.ch] });
    var top =
      '<div class="q-top"><span class="tag ch">CH ' + q.ch + '</span><span class="tag">' + TYPE_NAME[q.t] + "</span>" +
      (q.t === "list" ? '<span class="tag">' + q.need + " needed</span>" : "") +
      '<span class="pts" data-pts></span></div><p class="q-text">' + q.n + ". " + esc(q.q) + "</p>";
    var body = "";
    var saved = (state[q.id] && state[q.id].v) || null;
    if (q.t === "mcq") {
      var order = shuffled(q.opts.map(function (_, i) { return i; }), hash(q.q));
      body = '<div class="opts">' + order.map(function (i) {
        return '<label class="opt"><input type="radio" name="' + q.id + '" value="' + i + '"' + (saved === String(i) ? " checked" : "") + "><span>" + esc(q.opts[i]) + "</span></label>";
      }).join("") + "</div>";
    } else if (q.t === "tf") {
      body = '<div class="opts tf">' + ["true", "false"].map(function (v) {
        return '<label class="opt"><input type="radio" name="' + q.id + '" value="' + v + '"' + (saved === v ? " checked" : "") + "><span>" + (v === "true" ? "True" : "False") + "</span></label>";
      }).join("") + "</div>";
    } else if (q.t === "match") {
      var rights = shuffled(q.pairs.map(function (p) { return p[1]; }), hash(q.q) + 7);
      var rows = shuffled(q.pairs.map(function (_, i) { return i; }), hash(q.q) + 3);
      body = '<div class="match">' + rows.map(function (i) {
        var cur = saved && saved[i];
        return '<div class="row" data-i="' + i + '"><span>' + esc(q.pairs[i][0]) + '</span><select aria-label="Match for ' + esc(q.pairs[i][0]) + '"><option value="">Choose…</option>' +
          rights.map(function (r) {
            return '<option value="' + esc(r) + '"' + (cur === r ? " selected" : "") + ">" + esc(r) + "</option>";
          }).join("") + "</select></div>";
      }).join("") + "</div>";
    } else {
      body = '<textarea aria-label="Your answer" placeholder="' + (q.t === "list" ? "Write each item, separated by commas or new lines…" : "Write your answer…") + '">' + (saved ? esc(saved) : "") + "</textarea>";
    }
    card.innerHTML = top + body +
      '<div class="q-actions"><button class="btn primary" type="button" data-check>Check</button><button class="btn" type="button" data-show>Show answer</button></div><div class="feedback" hidden></div>';

    card.addEventListener("change", function () {
      capture(q, card);
    });
    card.addEventListener("input", function () {
      capture(q, card);
    });
    card.querySelector("[data-check]").addEventListener("click", function () {
      grade(q, card, true);
      updateScore();
    });
    card.querySelector("[data-show]").addEventListener("click", function () {
      reveal(q, card);
    });
    if (state[q.id] && state[q.id].g != null) grade(q, card, false);
    return card;
  }

  function capture(q, card) {
    var v;
    if (q.t === "mcq" || q.t === "tf") {
      var r = card.querySelector("input:checked");
      v = r ? r.value : null;
    } else if (q.t === "match") {
      v = {};
      card.querySelectorAll(".row").forEach(function (row) {
        v[row.getAttribute("data-i")] = row.querySelector("select").value;
      });
    } else {
      v = card.querySelector("textarea").value;
    }
    state[q.id] = { v: v };
    save();
  }

  function setVerdict(card, frac, html) {
    card.classList.remove("ok", "part-ok", "no");
    card.classList.add(frac >= 1 ? "ok" : frac > 0 ? "part-ok" : "no");
    var fb = card.querySelector(".feedback");
    fb.hidden = false;
    fb.innerHTML = html;
  }

  function grade(q, card, fresh) {
    var s = state[q.id] || {};
    var v = s.v;
    var pts = 0;
    var max = maxPts(q);
    var html = "";
    var why = q.why ? '<div class="why">' + esc(q.why) + "</div>" : "";

    if (q.t === "mcq" || q.t === "tf") {
      var correct = q.t === "mcq" ? "0" : String(q.a);
      card.querySelectorAll(".opt").forEach(function (o) {
        var val = o.querySelector("input").value;
        o.classList.toggle("right", val === correct);
        o.classList.toggle("wrong", val === v && v !== correct);
      });
      if (v == null) {
        html = '<div class="verdict no">No answer selected.</div>';
      } else {
        pts = v === correct ? 1 : 0;
        var ans = q.t === "mcq" ? q.opts[0] : q.a ? "True" : "False";
        html = pts ? '<div class="verdict ok">Correct.</div>' : '<div class="verdict no">Not quite. Answer: ' + esc(ans) + "</div>";
      }
      html += why;
    } else if (q.t === "match") {
      var got = 0;
      card.querySelectorAll(".row").forEach(function (row) {
        var i = +row.getAttribute("data-i");
        var pick = v && v[i];
        var ok = pick === q.pairs[i][1];
        if (ok) got++;
        row.classList.toggle("right", ok);
        row.classList.toggle("wrong", !ok);
      });
      pts = got;
      html = '<div class="verdict ' + (got === max ? "ok" : got ? "part" : "no") + '">' + got + " of " + max + " pairs correct.</div>";
      if (got < max)
        html += '<ul class="kwlist">' + q.pairs.map(function (p) {
          return '<li class="hit">' + esc(p[0]) + " → " + esc(p[1]) + "</li>";
        }).join("") + "</ul>";
    } else {
      var tokens = tokensOf(v || "");
      var parts = q.t === "list" ? q.items : q.groups;
      var hits = parts.map(function (p) {
        return anyHit(tokens, p[1]);
      });
      var n = hits.filter(Boolean).length;
      var need = q.t === "list" ? Math.min(q.need, parts.length) : parts.length;
      pts = Math.min(n, need) / need;
      var lbl = q.t === "list" ? "items" : "key points";
      html = '<div class="verdict ' + (pts >= 1 ? "ok" : pts > 0 ? "part" : "no") + '">' + Math.min(n, need) + " of " + need + " " + lbl + " found" + (pts >= 1 ? ". Full marks." : ".") + "</div>" +
        '<ul class="kwlist">' + parts.map(function (p, i) {
          return '<li class="' + (hits[i] ? "hit" : "miss") + '">' + (hits[i] ? "✓ " : "✗ ") + esc(p[0]) + "</li>";
        }).join("") + "</ul>";
      if (q.t === "short") html += '<div class="why"><b>Model answer:</b> ' + esc(q.model) + "</div>";
      else html += why;
    }

    state[q.id] = { v: v, g: pts };
    if (fresh) save();
    card.querySelector("[data-pts]").textContent = (Math.round(pts * 100) / 100) + " / " + max;
    setVerdict(card, pts / max, html);
    return pts;
  }

  function reveal(q, card) {
    var fb = card.querySelector(".feedback");
    var html = "";
    if (q.t === "mcq") html = "<b>Answer:</b> " + esc(q.opts[0]);
    else if (q.t === "tf") html = "<b>Answer:</b> " + (q.a ? "True" : "False");
    else if (q.t === "match")
      html = '<ul class="kwlist">' + q.pairs.map(function (p) {
        return '<li class="hit">' + esc(p[0]) + " → " + esc(p[1]) + "</li>";
      }).join("") + "</ul>";
    else if (q.t === "list")
      html = "<b>Any " + q.need + " of:</b><ul class=\"kwlist\">" + q.items.map(function (p) {
        return '<li class="hit">' + esc(p[0]) + "</li>";
      }).join("") + "</ul>";
    else html = "<b>Model answer:</b> " + esc(q.model);
    if (q.why && q.t !== "short") html += '<div class="why">' + esc(q.why) + "</div>";
    fb.hidden = false;
    fb.innerHTML = html;
  }

  var cards = {};
  Q.forEach(function (q) {
    cards[q.id] = render(q);
    qlist.appendChild(cards[q.id]);
  });
  var empty = el("p", { class: "empty", hidden: "" }, "No questions match these filters.");
  qlist.appendChild(empty);

  function visible(q) {
    if (filter.ch !== "all" && q.ch !== filter.ch) return false;
    if (filter.ty !== "all" && q.t !== filter.ty) return false;
    if (filter.missed) {
      var s = state[q.id];
      if (s && s.g != null && s.g >= maxPts(q)) return false;
    }
    return true;
  }
  function applyFilter() {
    var shown = 0;
    Q.forEach(function (q) {
      var on = visible(q);
      cards[q.id].hidden = !on;
      if (on) shown++;
    });
    empty.hidden = shown > 0;
  }

  function updateScore() {
    var tot = 0,
      max = 0,
      done = 0,
      per = {};
    CHS.forEach(function (c) {
      per[c] = { got: 0, max: 0 };
    });
    Q.forEach(function (q) {
      var m = maxPts(q);
      per[q.ch].max += m;
      max += m;
      var s = state[q.id];
      if (s && s.g != null) {
        tot += s.g;
        per[q.ch].got += s.g;
        done++;
      }
    });
    var r = function (x) {
      return Math.round(x * 10) / 10;
    };
    document.getElementById("score-big").innerHTML = r(tot) + "<small> / " + max + "</small>";
    document.getElementById("score-sub").textContent =
      done + " of " + Q.length + " questions checked · " + (max ? Math.round((tot / max) * 100) : 0) + "% overall";
    var bars = document.getElementById("score-bars");
    bars.innerHTML = CHS.map(function (c) {
      var p = per[c].max ? (per[c].got / per[c].max) * 100 : 0;
      return '<div class="bar" style="--hue: ' + HUE[c] + '"><div class="lbl"><span>' + CH_NAME[c] + "</span><span>" + r(per[c].got) + "/" + per[c].max +
        '</span></div><div class="track"><div class="fill" style="width:' + p.toFixed(1) + '%"></div></div></div>';
    }).join("");
  }

  document.querySelectorAll("[data-ch]").forEach(function (b) {
    b.addEventListener("click", function () {
      filter.ch = b.getAttribute("data-ch");
      document.querySelectorAll("[data-ch]").forEach(function (x) {
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      });
      applyFilter();
    });
  });
  document.querySelectorAll("[data-ty]").forEach(function (b) {
    b.addEventListener("click", function () {
      filter.ty = b.getAttribute("data-ty");
      document.querySelectorAll("[data-ty]").forEach(function (x) {
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      });
      applyFilter();
    });
  });
  var missedBtn = document.getElementById("btn-missed");
  missedBtn.addEventListener("click", function () {
    filter.missed = !filter.missed;
    missedBtn.textContent = filter.missed ? "Show all" : "Retry missed";
    applyFilter();
  });
  document.getElementById("btn-grade").addEventListener("click", function () {
    Q.forEach(function (q) {
      if (!cards[q.id].hidden) {
        capture(q, cards[q.id]);
        grade(q, cards[q.id], true);
      }
    });
    updateScore();
  });
  document.getElementById("btn-reset").addEventListener("click", function () {
    if (!confirm("Clear all your answers and scores on this page?")) return;
    state = {};
    save();
    Q.forEach(function (q) {
      var fresh = render(q);
      fresh.hidden = cards[q.id].hidden;
      qlist.replaceChild(fresh, cards[q.id]);
      cards[q.id] = fresh;
    });
    filter.missed = false;
    missedBtn.textContent = "Retry missed";
    applyFilter();
    updateScore();
  });

  /* label table cells so phones can stack rows */
  document.querySelectorAll(".tbl table").forEach(function (t) {
    var heads = Array.prototype.map.call(t.querySelectorAll("thead th"), function (th) {
      return th.textContent.trim();
    });
    t.querySelectorAll("tbody tr").forEach(function (tr) {
      Array.prototype.forEach.call(tr.children, function (td, i) {
        if (heads[i]) td.setAttribute("data-label", heads[i]);
      });
    });
  });

  /* highlight the nav link for the section in view */
  var links = document.querySelectorAll(".topnav a");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (a) {
            a.classList.toggle("on", a.getAttribute("href") === "#" + e.target.id);
          });
        });
      },
      { rootMargin: "-40% 0px -55% 0px" },
    );
    ["summary", "memorize", "practice"].forEach(function (id) {
      var s = document.getElementById(id);
      if (s) io.observe(s);
    });
  }

  applyFilter();
  updateScore();
})();
