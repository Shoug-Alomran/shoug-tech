@head Chapter 1
@title Introduction to AI and Data Science
@sources chapter-1-introduction-to-ai-and-data-science
@count 55
@tldr AI is about making machines behave intelligently, data is the fuel, and data science is the step-by-step process that turns raw data into decisions.
@why This chapter has almost no maths, so it is tempting to skip. Do not. It hands you the **vocabulary the whole course uses**: when Chapter 3 says "model" or Chapter 7 says "features", it assumes you already know what those words are doing. It is also a favourite source of easy definition marks, such as naming the four approaches to AI or the four Vs of big data.
@connect This is the map of the course. Chapters 2.x teach the _clean and explore_ part of the process, Chapters 3 to 8 teach _modelling and evaluating_, and Chapters 9 and 10 teach the statistics that tell you whether a result is real.
@goals

- Place any AI system in one of the four approaches to AI
- Explain how AI, machine learning and deep learning nest inside each other
- Sort data into structured, unstructured, semi-structured or sequence
- Walk through the data science process in the right order
- Tell descriptive, predictive and prescriptive analytics apart
  @vocab
  Model | A function learned from data that takes an input and gives back an answer. "House size in, price out."
  Feature | One input column the model looks at, such as number of bedrooms.
  Label or target | The answer column you want predicted, such as price.
  Training | Showing the model examples so it can learn the input-to-answer pattern.
  Algorithm | The recipe that does the learning.
  Agent | Anything that perceives its surroundings and takes actions.
  @map
  3-4 | Outline and AI's economic value | SKIM | Know the headline: $13-22 trillion by 2033, of which generative AI is $3-4 trillion
  5-19 | What AI is: the four approaches | MEMORIZE | The 2 by 2 grid, the Turing test and its four skills
  20-21 | AI vs ML vs deep learning | MEMORIZE | The nesting picture, plus traditional programming vs ML
  22-24 | Applications of AI | SKIM | Have two examples ready
  25-34 | Data, its types, and big data | MEMORIZE | The four data types and the four Vs
  35-43 | Data science and its process | MEMORIZE | Definition, five components, and the seven steps in order
  44-47 | Exploratory data analysis | WRITE | Why EDA happens before modelling, and its three techniques
  48-52 | Analytics types with examples | MEMORIZE | Descriptive, predictive, prescriptive and an example of each
  53-55 | How the course runs | SKIM | Nothing to memorize

## The four ways to define AI | Slides 5-19 | must

For decades, people could not agree on what "intelligent machine" even means. The slides settle it with one grid. Ask two questions: are we judging how the machine **thinks** or how it **acts**? And is the standard to be like a **human** or to be **rational** (correct)? Two questions with two answers each gives four approaches.

|              | Measured against humans                       | Measured against ideal correctness                   |
| ------------ | --------------------------------------------- | ---------------------------------------------------- |
| **Thinking** | Thinking humanly (copy how the brain reasons) | Thinking rationally (follow the laws of logic)       |
| **Acting**   | Acting humanly (the Turing test)              | Acting rationally (do whatever gets the best result) |

Now go through each one in plain language.

**Acting humanly** is the Turing test. A person chats with a hidden partner. If they cannot tell whether it is a machine, the machine passes. Notice what is _not_ being tested: nobody opens the machine to check how it thinks. Only its behaviour counts.

**Thinking humanly** goes further. It says real intelligence means thinking like us, so first we must understand how humans think, then build programs that copy it.

**Thinking rationally** replaces human thought with perfect thought: the "laws of thought". The slides use Aristotle's syllogism: Socrates is a man; all men are mortal; therefore Socrates is mortal. This idea started formal logic.

**Acting rationally** drops all interest in the inner process. A rational agent simply acts to achieve the best outcome. Pulling your hand off a hot stove is not careful reasoning, yet it is clearly the right action. The slides call this approach more general than thinking rationally, and mathematically principled, because rationality can be defined and proven in a way that human behaviour cannot.

::analogy Birds and aeroplanes (slide 19)
People spent centuries trying to fly by copying birds and flapping. Flight only worked when engineers stopped imitating and focused on the _result_: lift. Modern AI is mostly the aeroplane. It does not need to be brain-like. It just needs to work.
::
::mnemonic Talk, Remember, Reason, Learn
The four skills needed to pass the Turing test, in the order a chat would use them. **Talk** is natural language processing, **Remember** is knowledge representation, **Reason** is automated reasoning, and **Learn** is machine learning.
::
::says Slide 15 | "These are the main branches of AI"
The four Turing skills are not just a checklist for one test. They are also how the field divides its work, which is why an exam can ask you to "name the main branches of AI" using this same slide.
::
::check A car's emergency brake stops the car the moment it detects an obstacle. Which approach is that closest to, and why?
**Acting rationally.** It takes the action that gives the best outcome, and nobody cares whether it reasons like a person or works through logic first. Compare it to the hot stove example on slide 18.
::
::trap Passing the Turing test does not prove a machine can think
The test only observes behaviour, so it belongs to **acting humanly**. If a question says "the program _reasons the same way people do_", the answer is thinking humanly, not the Turing test.
::
::key

- Two questions make the grid: think or act, human or rational
- Turing test = acting humanly: judged only on behaviour
- Thinking rationally = laws of logic, from Aristotle's syllogism
- Acting rationally = achieve the best outcome, however you get there
- Turing test needs NLP, knowledge representation, automated reasoning and machine learning
  ::

## AI, machine learning and deep learning | Slides 20-21 | must

These three terms are used as if they mean the same thing. They do not. They are **circles inside circles**.

**Artificial intelligence** is the umbrella: any technique that makes machines more humanlike, from smart assistants to self-driving cars. **Machine learning** is one branch under that umbrella: algorithms that learn patterns from historical data and then do a task _without explicit instructions_. **Deep learning** sits inside machine learning and uses neural networks with many layers.

::graph AI contains ML, and ML contains deep learning | directed
n ai 0 0 Artificial Intelligence\nany humanlike behaviour
n ml 0 95 Machine Learning\nlearns patterns from data *
n dl 0 190 Deep Learning\nmany-layered neural networks
e ai ml contains
e ml dl contains
::

The slide's key sentence is: _"While machine learning is AI, not all AI activities are machine learning."_ A chess program written entirely from hand-coded rules is AI, but it is not machine learning, because it learned nothing from data.

### Traditional programming versus machine learning

This comparison (slide 21) is the idea to carry into every later chapter.

::graph The arrows flip: ML receives the answers and produces the rules | directed
n d1 0 0 Data
n r1 0 80 Rules
n p1 170 40 Traditional\nprogram *
n a1 340 40 Answers
e d1 p1
e r1 p1
e p1 a1
n d2 0 190 Data
n a2 0 270 Answers
n p2 170 230 Machine\nlearning *
n r2 340 230 Rules
e d2 p2
e a2 p2
e p2 r2
::

::example Spam filter, built both ways
**Traditional:** you write the rule yourself: `if "free money" in email: mark_spam()`. Spammers write "fr3e m0ney" and you are beaten until you add another rule.

**Machine learning:** you hand over 100,000 emails already labelled spam or not spam. The algorithm works out which patterns predict spam. New spam tricks are handled by retraining on newer examples.
::
::trap "All AI is machine learning" is false
It is the reverse that holds: all machine learning is AI. Expect a true or false on this. Rule-based expert systems are AI without any learning.
::
::key

- AI is the umbrella, ML is inside AI, deep learning is inside ML
- ML learns from historical data rather than explicit instructions
- Machine learning is AI, but not all AI is machine learning
- Traditional: data + rules give answers. ML: data + answers give rules
  ::

## What data is, and its four shapes | Slides 25-33 | must

The slides define data by what AI does with it: an AI system **learns a mapping from A to B**. For a house-price system, A is the house details and B is the price. Data is simply the collected examples of A and B.

Data comes in shapes, and the shape decides which tools you can use.

| Type                | What it looks like                        | Example                                                 | Tool you would reach for |
| ------------------- | ----------------------------------------- | ------------------------------------------------------- | ------------------------ |
| **Structured**      | Neat rows and columns with a fixed format | Grade sheet, bank transactions                          | Excel, SQL, Pandas       |
| **Unstructured**    | No predefined format                      | Photos, audio, video, free text, social media posts     | Deep learning, NLP       |
| **Semi-structured** | Tagged but flexible; not a strict table   | JSON, XML, emails (headers are structured, body is not) | Parsers, then Pandas     |
| **Sequence**        | Order is the meaning                      | Stock prices over time, DNA, sentences                  | Time-series models       |

::analogy The filing cabinet test
**Structured** data is a spreadsheet: every row has the same boxes. **Semi-structured** data is a folder of forms where each sheet has labels but people added or skipped different fields. **Unstructured** data is a drawer full of photos and voice notes. **Sequence** data is a diary: shuffle the pages and the meaning is destroyed.
::
::tip The quick way to classify
Ask in order: "Would shuffling the rows destroy the meaning?" If yes, it is sequence data. "Are there labels or tags but no rigid table?" Semi-structured. "Rows and columns?" Structured. Otherwise, unstructured.
::
::check Which type is an email?
Semi-structured. The sender, date and subject follow a fixed format, while the body is free text. That mix of tagged and free content is exactly what semi-structured means.
::
::key

- AI learns a mapping from input A to output B
- Structured: fixed rows and columns, as in spreadsheets and SQL tables
- Unstructured: no format, as in images, audio, video and free text
- Semi-structured: tags without a rigid table, as in JSON, XML and email
- Sequence: order carries the meaning, as in time series and DNA
  ::

## Big data and the four Vs | Slide 34 | must

"Big" does not only mean a lot. The slide's definition: datasets **too complex, large and dynamic for traditional data processing tools** to handle efficiently. A 50 GB tidy table might be fine in a normal database; a smaller but constantly streaming mix of video and text might not be.

The challenges are the four Vs:

| V            | Question it answers      | Example: a ride-hailing app                            |
| ------------ | ------------------------ | ------------------------------------------------------ |
| **Volume**   | How much?                | Billions of trips stored                               |
| **Velocity** | How fast does it arrive? | GPS pings from every car, every few seconds            |
| **Variety**  | How many kinds?          | Tables of payments, map data, chat text, driver photos |
| **Veracity** | Can we trust it?         | GPS drift in tunnels, fake accounts                    |

::mnemonic Very Vast, Very Fast, Very Mixed, Very Doubtful
Say it aloud and the four Vs fall out in slide order: **vast** is Volume, **fast** is Velocity, **mixed** is Variety and **doubtful** is Veracity.
::
::trap Veracity is about quality, not truth in general
Students swap Variety and Veracity. **Variety** is different _types_ of data. **Veracity** is _uncertainty about data quality_, which is the slide's wording.
::
::key

- Big data: too complex, large and dynamic for traditional tools
- Volume = amount, Velocity = speed, Variety = types, Veracity = quality
  ::

## Data science and its seven-step process | Slides 35-43 | must

**Data science** is an interdisciplinary field that uses scientific methods, algorithms and systems to extract knowledge and insights from structured and unstructured data. In short: _questions in, evidence-based answers out_.

It is built from five components.

::mnemonic MEDS + V
A data scientist takes their **MEDS** and needs good **V**ision: **M**achine learning, data **E**ngineering, **D**omain expertise, **S**tatistics, and **V**isualization.
::
::why Why domain expertise is on the list
A model can find that ice cream sales predict drowning. Only someone who understands the domain says: both rise in summer. Without it, you ship nonsense with confidence.
::

The process is where marks live. Slide 42 lists seven steps, and they must be in order because each one feeds the next.

::steps The data science process, on a student-grades project
**Data collection.** Gather raw data from databases, APIs and sensors. _Pull grades, attendance and major from the university system._
**Data cleaning.** Handle missing data, outliers and formatting problems. _One student has a blank quiz grade and another has 110 out of 100._
**Data exploration.** Study patterns and distributions with statistics and charts. _Do Software Engineering majors score higher on the final?_
**Feature engineering.** Turn raw columns into useful inputs. _Combine six assignments into one "assignment average"._
**Model building.** Build predictive or inferential models. _Predict the final grade from the assignment average and quiz scores._
**Model evaluation.** Measure performance with metrics such as accuracy, precision and recall. _How far off are our predictions on students the model never saw?_
**Deployment and monitoring.** Put it into production and keep watching it. _Advisors get an early warning list, and you check it still works next term._
::
::mnemonic Clever Cats Explore Fish Markets Every Day
**C**ollection, **C**leaning, **E**xploration, **F**eature engineering, **M**odel building, **E**valuation, **D**eployment. The order matters here, so the sentence keeps it.
::
::trap Two slides, two lists
Slide 40 shows a six-part workflow that starts at _business understanding_ and ends at _data visualization_. Slide 42 shows the seven-step process. If a question says "according to the data science process", use the seven steps on slide 42. If it asks where the work begins in a real project, business understanding comes first.
::
::check Your model is 99% accurate on data it trained on and fails in real use. Which step did you do badly?
**Model evaluation.** It must be measured on data the model has not seen. Chapter 3 calls this the gap between training loss and test loss.
::
::key

- Data science extracts knowledge from structured and unstructured data
- Five components: machine learning, data engineering, domain expertise, statistics, visualization
- Seven steps: collection, cleaning, exploration, features, modelling, evaluation, deployment
- Tools: Python, Pandas, NumPy and Matplotlib for programming; Power BI and Tableau for analytics
  ::

## Exploratory data analysis (EDA) | Slides 44-47 | must

**EDA means getting to know your data before you model it.** The slide's purpose statement is exactly that: understand data characteristics before modelling.

::analogy Meeting the patient before the surgery
No surgeon operates on a stranger without checking their charts and scans. EDA is the check-up: the averages are the vitals, charts are the scans, and correlations show which symptoms travel together.
::

It uses three techniques:

| Technique                  | What you compute or draw             | What it tells you                                      |
| -------------------------- | ------------------------------------ | ------------------------------------------------------ |
| **Descriptive statistics** | Mean, median, variance               | Where values centre and how spread out they are        |
| **Data visualization**     | Histograms, scatter plots, box plots | Shape, outliers and clusters you would miss in numbers |
| **Correlation analysis**   | How pairs of variables move together | Which features are worth using in a model              |

The tools named are Pandas, Matplotlib and Seaborn in Python, and ggplot2 and dplyr in R. Chapter 2.2 teaches these properly.

::example What EDA catches (slides 43, 46)
Take the course grade sheet on slide 43. Its average looks healthy. A histogram shows two humps: one group near 90 and another near 60. The single average described nobody. A student with a dash instead of a number also appears, which would crash a model or silently skew it.
::
::trap Correlation is not causation
A heatmap shows that two variables move together. It never says one causes the other. If a question offers "the heatmap proves that attendance causes higher grades", it is wrong.
::
::key

- EDA is done before modelling to understand the data
- Three techniques: descriptive statistics, visualization, correlation analysis
- Python tools: Pandas, Matplotlib, Seaborn. R tools: ggplot2, dplyr
  ::

## Three kinds of analytics | Slides 48-52 | must

All analytics answers one of three questions. They move from the past, to the future, to action, and each is harder and more valuable than the one before.

| Type             | Question                | Field                 | Real example on the slides                                |
| ---------------- | ----------------------- | --------------------- | --------------------------------------------------------- |
| **Descriptive**  | What happened?          | Business intelligence | YouTube's dashboard showing your views last month         |
| **Predictive**   | What will happen?       | Machine learning      | Forecasting what a customer will buy next                 |
| **Prescriptive** | What should we do next? | Decision science      | A ride app picking which driver to send to which customer |

::mnemonic Was, Will, Should
**Was** it? Descriptive. **Will** it? Predictive. **Should** we? Prescriptive. If you can rephrase the question with one of those three words, you have your answer.
::
::check A hospital system recommends moving two nurses to the emergency ward tonight, given forecast demand. Which type?
**Prescriptive.** The word to look for is the recommendation. A system that only said "we expect 40 patients tonight" would be predictive.
::
::trap Predictive stops at the forecast
The moment a system tells you what to _do_ about the forecast, it has become prescriptive. Exam options often describe a forecast and a recommendation side by side.
::
::key

- Descriptive = what happened, business intelligence, historical trends
- Predictive = what will happen, machine learning and statistical models
- Prescriptive = what to do next, decision science, recommendations
- Examples: YouTube analytics, purchase forecast, driver-customer matching
  ::
