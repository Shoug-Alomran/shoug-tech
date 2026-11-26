"""SE423 Old Chapter 2 — Software Engineering (all 77 slides of slides/software-engineering/software-engineering.pdf),
plus the agile, CI/CD and improvement material the earlier breakdown carried (used by the Old Ch 2 quiz)."""
from . import sec, hook, box, strip, sub, col, two, table, qa, bullets, cheat, mistakes, quiz

PAGE = {
    "brand": "Software Engineering<span>·</span>Playbook",
    "chapter": "Old Chapter 2",
    "footer": "SE423 · Software Project Management · Old Chapter 2 — Software Engineering",
    "eyebrow": "SE423 · Software Project Management · Old Chapter 2",
    "title": "Build the product right,<br /><em>and build the right product.</em>",
    "lead": ("Software engineering covers every aspect of software production, from early specification to maintaining the system after it "
             "goes into use, with project management running across all of it. This chapter contrasts project-based and product-based "
             "engineering, walks the process models and life cycles from waterfall to agile and DevOps, and then turns to product "
             "engineering: quality attributes, the product vision, product management, prototyping and customer value."),
    "badges": ["Project vs product SE", "Process models &amp; CMM", "Life cycles &amp; Stacey", "Product vision (Moore)", "Customer value"],
    "nav": [("foundation", "Foundation"), ("product-project", "Product vs Project"), ("process", "Process Models"),
            ("lifecycles", "Life Cycles"), ("devops", "DevOps"), ("product", "Product Engineering"), ("vision", "Product Vision"),
            ("pm", "Product Management"), ("prototyping", "Prototyping"), ("value", "Customer Value"), ("agile", "Agile &amp; Improvement"),
            ("cheat", "Cheat Sheet"), ("mistakes", "Mistakes"), ("quiz", "Pop Quiz")],
}

S = []

S.append(sec("foundation", "§ 01 — SOFTWARE ENGINEERING", "An engineering discipline for all of software production",
    "Software engineering is concerned with all aspects of software production, from the early stages of system specification through to "
    "maintaining the system after it has gone into use.",
    two(col(sub("Software engineering and project management"),
            box("The engineering flow is <b>Analyze → Design → Build → Test → Deliver</b>: requirements definition; system and software design; "
                "implementation and unit testing; integration and system testing; operation and maintenance. <b>Project management spans all "
                "five</b> stages.")),
        col(sub("Core activities and constraints"),
            box("<b>Specification</b> defines need and constraints · <b>development</b> designs and implements · <b>validation</b> checks fitness · "
                "<b>evolution</b> adapts after delivery.<br /><br />The three constraints, <b>scope, time and cost</b>, interact, with quality and risk "
                "across all three: changing one needs an explicit trade-off."),
            strip("<b>Exam lens:</b> verification asks “did we build the product right?” Validation asks “did we build the right product?”"))),
))

S.append(sec("product-project", "§ 02 — PRODUCT VS PROJECT SOFTWARE ENGINEERING", "Who owns the requirements?",
    "<b>Software products</b> are generic systems that provide functionality useful to a range of customers: large business systems "
    "(MS Excel), personal products (Evernote), simple apps and games (Sudoku). Product engineering methods evolved from techniques for "
    "one-off <b>custom systems</b>, which large businesses, government and public bodies still need, developed in dedicated projects. "
    "A <b>project</b> is a temporary endeavor undertaken to create a unique product, service or result.",
    two(col(sub("Project-based software engineering"),
            box("Triangle: the <b>customer's problem</b> generates <b>requirements</b> (owned by customer and developer), which are implemented by "
                "<b>software</b> (the developer) that helps with the problem.<br /><br />"
                "• the starting point is a set of <b>software requirements owned by an external client</b><br />"
                "• a software company (the <b>contractor</b>) designs and implements the system to meet them<br />"
                "• the customer may change requirements at any time, and usually does; the contractor must follow<br />"
                "• custom software usually has a <b>long lifetime (10+ years)</b> and must be supported over it")),
        col(sub("Product-based software engineering"),
            box("Triangle: an <b>opportunity</b> inspires <b>product features</b>, implemented by <b>software</b> that realizes the opportunity, "
                "and the <b>developer owns all three</b>.<br /><br />"
                "• the starting point is a <b>business opportunity</b> spotted by people or a company<br />"
                "• the company designs and implements features that will be useful to customers<br />"
                "• the developer decides the timescale, which features to include and when the product changes<br />"
                "• <b>rapid delivery</b> is essential to capture the market"))),
    qa("Software execution models", "where the software runs", None,
       table(["Model", "What runs where"], [
           ["<b>Stand-alone</b>", "The software runs entirely on the customer's computers; the vendor's servers only provide product updates"],
           ["<b>Hybrid</b>", "Part of the functionality runs on the customer's computer and some on the developer's servers (e.g. backups, extra features)"],
           ["<b>Software as a service</b>", "All functionality runs on the developer's servers; customers use a browser or mobile app"]])),
    qa("Product manager vs project manager", "different jobs", None,
       table(["Product manager", "Project manager"], [
           ["Idea validation, setting the vision, product planning and strategy", "Scope planning, budgeting"],
           ["Market analysis, marketing strategy, technology roadmap", "Team organization, task management, progress updates"],
           ["User needs analysis, product launch", "Management of resources, risks and issues"]]),
       strip("They overlap on things like communication with the team and customers, but the product manager owns <b>what</b> and <b>why</b>, "
             "the project manager owns <b>how</b> and <b>when</b>."), accent="accent-2"),
))

S.append(sec("process", "§ 03 — SOFTWARE PROCESS MODELS", "Waterfall, incremental, reuse, prototyping and improvement",
    None,
    table(["Model", "Idea"], [
        ["<b>Waterfall</b>", "Takes specification, development, validation and evolution and makes them separate phases: requirements definition → "
         "system and software design → implementation and unit testing → integration and system testing → operation and maintenance"],
        ["<b>Incremental development</b>", "Interleaves specification, development and validation, running concurrently from an outline description; "
         "the system grows as a series of versions (initial → intermediate → final), each adding functionality"],
        ["<b>Integration and configuration</b>", "Relies on reusable components or systems; development configures them for a new setting and integrates them"]]),
    two(col(sub("Incremental delivery"),
            box("Define outline requirements → assign requirements to increments → design the system architecture → develop an increment → "
                "validate, integrate and validate the system → deploy the increment. If the system is incomplete, develop the next increment; "
                "when complete, it is the final system."),
            sub("Reuse-oriented software engineering"),
            box("Requirements specification → software discovery and evaluation → requirements refinement. Then, if an application system is "
                "available, <b>configure</b> it; if components are available, <b>adapt</b> them or <b>develop new</b> ones, and <b>integrate</b> the system.")),
        col(sub("Prototype development"),
            table(["Step", "Output"], [
                ["Establish prototype objectives", "Prototyping plan"],
                ["Define prototype functionality", "Outline definition"],
                ["Develop prototype", "Executable prototype"],
                ["Evaluate prototype", "Evaluation report"]]),
            sub("Plan-based vs agile"),
            box("<b>Plan-based:</b> requirements engineering produces a requirements specification that drives design and implementation; changes "
                "come back as change requests.<br /><b>Agile:</b> requirements engineering and design/implementation loop together continuously."))),
    qa("Process improvement and capability maturity", "measure · analyze · change", None,
       two(col(box("The <b>process improvement model</b> is a cycle: <b>process measure → process analyze → process change</b>, then measure again.")),
           col(table(["Level", "Name"], [["1", "Initial"], ["2", "Managed"], ["3", "Defined"], ["4", "Quantitatively defined"], ["5", "Optimizing"]]))),
       accent="accent-2"),
))

S.append(sec("lifecycles", "§ 04 — LIFE CYCLES", "From predictive to agile",
    None,
    two(col(sub("Four shapes"),
            box("<b>Predictive:</b> analyze → design → build → test → deliver, once.<br />"
                "<b>Iterative:</b> analyze, then repeated analyze/design (prototype) and build/test (refine) loops, then deliver.<br />"
                "<b>Varying-sized increments:</b> each increment runs the whole analyze→deliver cycle and ships something.<br />"
                "<b>Agile:</b> short, repeated, delivering cycles.")),
        col(sub("Iteration-based vs flow-based agile"),
            box("<b>Iteration-based:</b> fixed time-boxes, each doing requirements, analysis, design, build and test for the work selected.<br />"
                "<b>Flow-based:</b> no fixed time-box; work moves through the same steps limited by the number of features in the "
                "<b>WIP (work in progress) limit</b>, repeating as needed."))),
    two(col(sub("The continuum of life cycles"),
            box("Plotted on <b>degree of change</b> (x) and <b>frequency of delivery</b> (y): <b>predictive</b> is low/low, <b>iterative</b> high change "
                "but low delivery, <b>incremental</b> frequent delivery but low change, <b>agile</b> high on both.")),
        col(sub("Uncertainty and complexity (Stacey model)"),
            box("Axes: requirements uncertainty and technical uncertainty. <b>Simple</b> (low/low) suits linear approaches; <b>complicated</b> and "
                "<b>complex</b> suit adaptive approaches; <b>chaos</b> (high/high) is fundamentally risky."))),
    qa("Characteristics of the four categories", "know this table", None,
       table(["Approach", "Requirements", "Activities", "Delivery", "Goal"], [
           ["Predictive", "Fixed", "Performed once for the entire project", "Single delivery", "Manage cost"],
           ["Iterative", "Dynamic", "Repeated until correct", "Single delivery", "Correctness of solution"],
           ["Incremental", "Dynamic", "Performed once for a given increment", "Frequent smaller deliveries", "Speed"],
           ["Agile", "Dynamic", "Repeated until correct", "Frequent smaller deliveries", "Customer value via frequent deliveries and feedback"]]),
       accent="accent-2"),
))

S.append(sec("devops", "§ 05 — DEVOPS", "One multi-skilled team for development, deployment and support",
    "DevOps joins development and operations through shared ownership, automation, measurement and learning.",
    two(col(sub("DevOps automation"),
            box("<b>Continuous integration</b>: integrate small changes often; each triggers an automated build and tests.<br />"
                "<b>Continuous delivery</b>: every passing change is deployable; production release stays a business decision.<br />"
                "<b>Continuous deployment</b>: passing changes go to production automatically; monitoring and rollback are essential.<br />"
                "<b>Infrastructure as code</b>: environments defined and created from code.")),
        col(sub("Code management and measurement"),
            box("The <b>code management system</b> around a code repository: branching and merging, recovering version information, saving and "
                "retrieving versions, transferring code to and from developers' file stores.<br /><br />"
                "<b>DevOps measurement:</b> data collection → data analysis → report generation. Useful measures: lead time, deployment "
                "frequency, change failure rate, recovery time."))),
    box("<b>CI/CD pipeline:</b> commit → build → automated tests → security checks → deploy → observe.", style="margin-top: 14px"),
))

S.append(sec("product", "§ 06 — PRODUCT ENGINEERING", "Quality attributes, product lines and platforms",
    None,
    two(col(sub("Seven software product quality attributes"),
            box("1. <b>Reliability</b> · 2. <b>Availability</b> · 3. <b>Resilience</b> · 4. <b>Maintainability</b> · 5. <b>Responsiveness</b> · "
                "6. <b>Usability</b> · 7. <b>Security</b>")),
        col(sub("Software product line"),
            box("A set of products that <b>share a common core</b>; each member adds customer-specific adaptations. Product lines can implement a custom "
                "system for a customer whose needs a generic product can't meet."))),
    two(col(sub("Platform"),
            box("A software (or software + hardware) product with functionality that lets <b>new applications be built on it</b>. Example: Facebook, "
                "which offers product features and also supports “Facebook apps” that businesses or interest groups use.")),
        col(sub("Comparable software development"),
            box("The key feature of product development: <b>no external customer</b> generates requirements or pays. Comparable cases: "
                "<b>student projects</b> (the group decides the features), <b>research software</b> (built to answer research questions), and "
                "<b>internal tool development</b> (for your own organization's employees)."))),
))

S.append(sec("vision", "§ 07 — THE PRODUCT VISION", "Every product starts with one",
    "The starting point for product development is a <b>product vision</b>: a simple statement of the essence of the product.",
    hook("🎯", "What · Who · Why",
         "The vision answers three questions: <b>what</b> is the product to be developed? <b>Who</b> are the target customers and users? "
         "<b>Why</b> should customers buy this product?"),
    two(col(sub("Moore's vision template"),
            box("<b>FOR</b> (target customer)<br /><b>WHO</b> (statement of the need or opportunity)<br />"
                "<b>The</b> (product name) <b>is a</b> (product category)<br /><b>THAT</b> (key benefit, compelling reason to buy)<br />"
                "<b>UNLIKE</b> (primary competitive alternative)<br /><b>OUR PRODUCT</b> (statement of primary differentiation)")),
        col(sub("Example: CRM-Innovator"),
            box("“<b>FOR</b> a mid-sized company's marketing and sales departments <b>WHO</b> need basic CRM functionality, <b>THE</b> CRM-Innovator "
                "<b>is</b> a web-based service <b>THAT</b> provides sales tracking, lead generation and sales representative support features that "
                "improve customer relationships at critical touch points. <b>UNLIKE</b> other services or packaged software, <b>OUR</b> product "
                "provides very capable services at a moderate cost.”"))),
    qa("Information sources for a product vision", "four sources", None,
       table(["Source", "How it helps"], [
           ["Domain experience", "Developers who work in an area (say marketing and sales) know what software support it needs, and may be frustrated "
            "by gaps in the software they use"],
           ["Product experience", "Users of existing software see simpler, better ways to provide the same functionality; new products can use new "
            "technology such as speech interfaces"],
           ["Customer experience", "Discussions with prospective customers reveal their problems, constraints such as interoperability, and the "
            "critical attributes they need"],
           ["Prototyping and playing around", "Build a prototype to understand an idea better and experiment with variations on it as a platform"]]),
       strip("<b>iLearn vision:</b> “FOR teachers and educators WHO need a way to help students use web-based learning resources and applications, "
             "THE iLearn system is an open learning environment THAT allows the resources used by classes and students to be easily configured by "
             "teachers. UNLIKE virtual learning environments such as Moodle, the focus of iLearn is the learning process rather than administering "
             "materials, assessments and coursework. OUR product lets teachers create subject- and age-specific environments using any web-based resources.”"),
       accent="accent-2"),
))

S.append(sec("pm", "§ 08 — SOFTWARE PRODUCT MANAGEMENT", "The product manager sits between business, customers and developers",
    "Software product management is a business activity focused on the products a business develops and sells. <b>Product managers (PMs)</b> "
    "take overall responsibility for the product and are involved in planning, development and marketing, from first conception to withdrawal "
    "from the market. They look outward to customers rather than at the software itself.",
    two(col(sub("Product management concerns"),
            box("<b>Business needs</b>: the software must meet the company's business goals.<br />"
                "<b>Technology constraints</b>: make developers aware of technology issues that matter to customers.<br />"
                "<b>Customer experience</b>: stay in regular contact with customers to understand what they want, who the users are and how the "
                "product will be used.")),
        col(sub("Technical interactions of product managers"),
            box("• <b>Product vision management</b>: help develop the vision, assess changes against it, prevent <b>vision drift</b><br />"
                "• <b>Product roadmap development</b>: the plan for development, release and marketing; the PM is the final authority on changes<br />"
                "• <b>User stories and scenarios</b>: refine the vision and identify features; the PM leads them<br />"
                "• <b>Product backlog</b>: the prioritized to-do list; the PM helps create, refine and prioritize it<br />"
                "• <b>Acceptance testing</b>: verify a release meets the roadmap's goals and is efficient and reliable<br />"
                "• <b>Customer testing</b>: give customers a release and gather feedback on features, usability and business fit<br />"
                "• <b>User interface design</b>: act as a surrogate user so features aren't needlessly complex"))),
))

S.append(sec("prototyping", "§ 09 — PRODUCT PROTOTYPING", "Build something people can react to",
    "Product prototyping is developing an early version of a product to test your ideas and convince yourself and funders that it has real "
    "market potential.",
    two(col(sub("Why prototype"),
            box("• users only really relate to a product when they see a working version, then say what they like and suggest features<br />"
                "• a prototype helps identify fundamental components or services and test technology<br />"
                "• building one should be the <b>first thing</b> you do, aiming for a version that demonstrates the key features<br />"
                "• always plan to <b>throw it away</b> and re-implement properly, taking account of security and reliability")),
        col(sub("Two-stage prototyping"),
            box("<b>1. Feasibility demonstration</b>: an executable system that shows the new ideas work, and shows funders or management the features "
                "that beat competitors.<br /><br /><b>2. Customer demonstration</b>: extend the feasibility prototype with ideas for specific customer "
                "features and how they are realized. First do user studies so you know your users and scenarios."))),
))

S.append(sec("value", "§ 10 — CUSTOMER VALUE AND THE BUSINESS MODEL", "Value is benefits minus costs, as the customer sees them",
    "<b>Value</b> is the sum of the tangible and intangible benefits and costs.",
    two(col(sub("Customer perceived value"),
            box("<b>Customer perceived value</b> = total customer <b>benefit</b> − total customer <b>cost</b>.<br /><br />"
                "<b>Benefits:</b> product, services, personnel, image.<br /><b>Costs:</b> monetary, time, energy, psychological.")),
        col(sub("Business model canvas (in filling order)"),
            box("1 Customer segments · 2 Value proposition · 3 Channels · 4 Customer relationships · 5 Revenue streams · 6 Key resources · "
                "7 Key activities · 8 Key partners · 9 Cost structure"))),
    box("<b>Summary of the chapter:</b> products may be stand-alone, hybrid or service-based; in product engineering the same company decides the "
        "features and implements them. A product vision says what is being built, for whom, and why they'd buy it, drawing on domain, product and "
        "customer experience and prototypes. Product managers own the vision and roadmap, user stories and backlog, customer and acceptance testing "
        "and UI design, and they connect the business, the developers and the customers. Always prototype to refine ideas and demonstrate features.",
        style="margin-top: 18px"),
))

S.append(sec("agile", "§ 11 — AGILE DELIVERY AND IMPROVEMENT", "Scrum in brief, and Plan-Do-Check-Act",
    "Material from class that goes with this chapter (and the Old Chapter 2 quiz).",
    two(col(sub("Scrum roles and artifacts"),
            box("<b>Product Owner</b>: value and backlog order · <b>Scrum Master</b>: team effectiveness and removing impediments · <b>Developers</b>: "
                "create a done increment.<br /><br />Product backlog → product goal · sprint backlog → sprint goal · increment → definition of done.<br /><br />"
                "Agile is <b>not</b> “no plan, no documentation, no architecture”: planning is continuous and design evolves with feedback.")),
        col(sub("Lifecycle trade-offs"),
            table(["Approach", "Best fit", "Main risk"], [
                ["Waterfall", "Stable requirements, regulated gates", "Late feedback, costly change"],
                ["Incremental", "Value can ship in slices", "Architecture can erode"],
                ["Iterative", "Solution needs refinement", "Convergence is not automatic"],
                ["Spiral", "Large, high-risk work", "Complex and management-heavy"],
                ["Agile", "High change, close customer access", "Needs discipline and engagement"]]))),
    box("<b>Plan-Do-Check-Act:</b> <b>Plan</b> a measurable problem and a small experiment · <b>Do</b> it on a limited scope and capture evidence · "
        "<b>Check</b> the results against the hypothesis · <b>Act</b>: standardize, adapt or abandon, then repeat.", style="margin-top: 14px"),
))

S.append(cheat([
    ["Software engineering", "All aspects of software production, from specification to maintenance"],
    ["Project-based SE", "Client owns the requirements; contractor builds; long-lived custom software"],
    ["Product-based SE", "Business opportunity; developer owns features and timing; rapid delivery"],
    ["Execution models", "Stand-alone · hybrid · software as a service"],
    ["Process models", "Waterfall · incremental · integration and configuration (reuse)"],
    ["Improvement cycle", "Measure → analyze → change"],
    ["CMM levels", "Initial · managed · defined · quantitatively defined · optimizing"],
    ["Four life cycles", "Predictive (manage cost) · iterative (correctness) · incremental (speed) · agile (customer value)"],
    ["Stacey", "Simple → linear; complicated/complex → adaptive; chaos → fundamentally risky"],
    ["Quality attributes", "Reliability · availability · resilience · maintainability · responsiveness · usability · security"],
    ["Product vision", "What · who · why; Moore: FOR · WHO · THE … IS A · THAT · UNLIKE · OUR PRODUCT"],
    ["Vision sources", "Domain · product · customer experience · prototyping"],
    ["PM concerns", "Business needs · technology constraints · customer experience"],
    ["Two-stage prototyping", "Feasibility demonstration → customer demonstration"],
    ["Perceived value", "Total benefit (product, services, personnel, image) − total cost (monetary, time, energy, psychological)"],
    ["V&V", "Verification: built it right · validation: built the right thing"],
]))

S.append(mistakes([
    ("Who owns the requirements", "“In product-based SE the customer owns the requirements.”", "In project-based SE the external client owns them; in product-based SE the developer owns the features."),
    ("Product vs project manager", "Treating product manager and project manager as the same role.", "The product manager owns the vision, roadmap and market; the project manager owns scope, budget, schedule and resources."),
    ("Hybrid vs SaaS", "“Hybrid means the software runs in the cloud.”", "Hybrid splits functionality between the customer's computer and the vendor's servers; SaaS runs everything on the vendor's servers."),
    ("Iterative vs incremental", "Using the two words interchangeably.", "Iterative refines the solution through repetition (single delivery); incremental ships usable slices (frequent deliveries)."),
    ("Goal of each life cycle", "“Agile's goal is speed.”", "Incremental's goal is speed; agile's is customer value through frequent deliveries and feedback."),
    ("Keeping the prototype", "Shipping the prototype as the product.", "Plan to throw the prototype away and re-implement, accounting for security and reliability."),
]))

S.append(quiz([
    ("Define software engineering.", "An engineering discipline concerned with all aspects of software production, from early specification to maintenance after delivery."),
    ("What is the starting point of project-based vs product-based SE?", "Project-based: requirements owned by an external client. Product-based: a business opportunity."),
    ("Name the three software execution models.", "Stand-alone, hybrid, software as a service."),
    ("List the five capability maturity levels.", "Initial, managed, defined, quantitatively defined, optimizing."),
    ("What is the goal of each of the four life cycle categories?", "Predictive: manage cost · iterative: correctness of the solution · incremental: speed · agile: customer value."),
    ("Which three questions must a product vision answer?", "What is the product, who are the target customers and users, and why would they buy it."),
    ("Fill in Moore's template keywords.", "FOR · WHO · THE (product) IS A (category) · THAT · UNLIKE · OUR PRODUCT."),
    ("What is vision drift, and who prevents it?", "The product gradually moving away from its vision; the product manager, by assessing changes against the vision."),
    ("What are the two stages of prototyping?", "Feasibility demonstration, then customer demonstration."),
    ("How is customer perceived value calculated?", "Total customer benefit minus total customer cost."),
    ("Name the seven product quality attributes.", "Reliability, availability, resilience, maintainability, responsiveness, usability, security."),
    ("Distinguish continuous delivery from continuous deployment.", "Delivery: every passing change is deployable but release is a business decision. Deployment: passing changes go to production automatically."),
]))

SECTIONS = S
