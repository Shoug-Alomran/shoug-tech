<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shoug Alomran - Resume</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            line-height: 1.4;
        }
        
        .container {
            max-width: 210mm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        .header {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            color: white;
            padding: 25px 40px;
            text-align: center;
            border-bottom: 5px solid #d4af37;
        }
        
        .header h1 {
            font-size: 2.2em;
            margin-bottom: 10px;
            letter-spacing: 3px;
            font-weight: 300;
        }
        
        .contact-info {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 0.9em;
        }
        
        .contact-info a {
            color: white;
            text-decoration: none;
        }
        
        .content {
            padding: 25px 40px;
        }
        
        .section {
            margin-bottom: 20px;
            page-break-inside: avoid;
        }
        
        .section-title {
            font-size: 1.2em;
            color: #1e3c72;
            border-bottom: 3px solid #2a5298;
            padding-bottom: 4px;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .item {
            margin-bottom: 15px;
            page-break-inside: avoid;
        }
        
        .item-title {
            font-size: 1.05em;
            font-weight: bold;
            color: #2a5298;
            margin-bottom: 3px;
        }
        
        .item-company {
            font-weight: 600;
            color: #555;
            margin-bottom: 2px;
        }
        
        .item-date {
            color: #777;
            font-style: italic;
            font-size: 0.85em;
            margin-bottom: 6px;
        }
        
        .item ul {
            margin-left: 20px;
            margin-top: 5px;
            margin-bottom: 0;
        }
        
        .item li {
            margin-bottom: 3px;
            font-size: 0.88em;
            line-height: 1.4;
        }
        
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 10px;
        }
        
        .skill-box {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 5px;
            border-left: 4px solid #2a5298;
        }
        
        .skill-box h4 {
            color: #1e3c72;
            margin-bottom: 8px;
            font-size: 1em;
        }
        
        .skill-box ul {
            list-style: none;
        }
        
        .skill-box li {
            padding: 2px 0;
            font-size: 0.85em;
            color: #555;
        }
        
        .skill-box li:before {
            content: "▹ ";
            color: #2a5298;
            font-weight: bold;
        }
        
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        
        .tag {
            background: #e8f0fe;
            color: #1e3c72;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }
        
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .box {
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 5px;
            border-left: 4px solid #2a5298;
            font-size: 0.9em;
        }
        
        .download-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2a5298;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        
        .download-btn:hover {
            background: #1e3c72;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
                margin: 0;
            }
            
            .container {
                box-shadow: none;
                max-width: 100%;
                margin: 0;
            }
            
            .download-btn {
                display: none;
            }
            
            .header {
                padding: 20px 30px;
            }
            
            .header h1 {
                font-size: 2em;
                margin-bottom: 8px;
            }
            
            .content {
                padding: 20px 30px;
            }
            
            .section {
                margin-bottom: 15px;
                page-break-inside: avoid;
            }
            
            .section-title {
                font-size: 1.1em;
                margin-bottom: 10px;
                padding-bottom: 3px;
            }
            
            .item {
                margin-bottom: 10px;
                page-break-inside: avoid;
            }
            
            .item ul {
                margin-top: 3px;
                margin-bottom: 0;
            }
            
            .item li {
                margin-bottom: 2px;
                font-size: 0.82em;
                line-height: 1.3;
            }
            
            @page {
                margin: 0.4in 0.5in;
                size: letter;
            }
        }
    </style>
</head>
<body>
    <button class="download-btn" onclick="window.print()">📥 Download PDF</button>
    
    <div class="container">
        <div class="header">
            <h1>SHOUG ALOMRAN</h1>
            <div class="contact-info">
                <span>shoug.alomran@hotmail.com</span>
                <span>|</span>
                <a href="https://Shoug-Tech.com/">Portfolio</a>
                <span>|</span>
                <a href="https://www.linkedin.com/in/shoug-alomran">LinkedIn</a>
                <span>|</span>
                <span>Riyadh, Saudi Arabia</span>
            </div>
        </div>
        
        <div class="content">
            <!-- Education -->
            <div class="section">
                <h2 class="section-title">Education</h2>
                <div class="item">
                    <div class="item-title">Bachelor's Degree in Software Engineering/Cybersecurity</div>
                    <div class="item-company">Prince Sultan University</div>
                    <div class="item-date">September 2023 - December 2028 | Riyadh, Saudi Arabia</div>
                    <div class="item-desc">
                        <strong>Activities and Societies:</strong> Software Engineering Club (September 2023 - September 2024), The Mental Health and Well-Being Club (May 2023 - Present), Peer Tutor (January 2025 - Present)
                    </div>
                </div>
                <div class="item">
                    <div class="item-title">High School Diploma</div>
                    <div class="item-company">AlRowad Private Schools</div>
                    <div class="item-date">2023 | Grade: 12</div>
                </div>
            </div>
            
            <!-- Professional Experience -->
            <div class="section">
                <h2 class="section-title">Professional Experience</h2>
                
                <div class="item">
                    <div class="item-title">Liaison Officer</div>
                    <div class="item-company">ACM Student Chapter</div>
                    <div class="item-date">November 2025 – Present | Riyadh, Saudi Arabia</div>
                    <ul>
                        <li>Recruited new members to support the growth of the ACM Student Chapter</li>
                        <li>Promoted ACM events, resources, and opportunities to increase student engagement</li>
                        <li>Collaborated with chapter officers to communicate upcoming initiatives and activities</li>
                        <li>Contributed to strengthening the chapter's presence on campus through early-stage outreach efforts</li>
                    </ul>
                </div>
                
                <div class="item">
                    <div class="item-title">Course Instructor</div>
                    <div class="item-company">Qimah | قمة</div>
                    <div class="item-date">August 2025 - Present | Riyadh, Saudi Arabia</div>
                    <ul>
                        <li>Designed and developed comprehensive Psychology 101 learning resources covering all major topics</li>
                        <li>Created structured lecture slides with examples, case studies, and real-life applications</li>
                        <li>Produced educational podcasts to simplify complex psychological concepts</li>
                        <li>Designed mind maps and summaries for efficient review and exam preparation</li>
                        <li>Compiled and analyzed past exam questions to build targeted practice resources</li>
                        <li>Developed mock exams and practice quizzes aligned with university assessments</li>
                        <li>Integrated interactive learning aids such as Quizlet sets, flashcards, and WhatsApp study groups</li>
                    </ul>
                </div>
                
                <div class="item">
                    <div class="item-title">Trainee in Cybersecurity</div>
                    <div class="item-company">MDD</div>
                    <div class="item-date">March 2025 - Present | Riyadh, Saudi Arabia</div>
                    <ul>
                        <li>Researched third-party spam filtering applications and provided recommendations</li>
                        <li>Learned to identify and mitigate spam email threats</li>
                        <li>Gained hands-on experience with Linux systems</li>
                        <li>Completed The Fundamentals of Linux course on Hack The Box</li>
                        <li>Performed web application tests using Burp Suite under mentor supervision</li>
                        <li>Used GitHub for version control on a university project with proper documentation</li>
                    </ul>
                </div>
                
                <div class="item">
                    <div class="item-title">Peer Tutor</div>
                    <div class="item-company">Prince Sultan University - Writing and Tutoring Center (WTC)</div>
                    <div class="item-date">January 2025 - Present | Riyadh, Saudi Arabia</div>
                    <ul>
                        <li>Help students understand challenging concepts and develop study strategies</li>
                        <li>Break down complex topics into simpler, manageable parts</li>
                        <li>Create a supportive environment for academic growth</li>
                        <li>Encourage independent learning and critical thinking</li>
                    </ul>
                </div>
                
                <div class="item">
                    <div class="item-title">Event Management Member</div>
                    <div class="item-company">Mental Health & Well-Being Club</div>
                    <div class="item-date">May 2023 - Present | Riyadh, Saudi Arabia</div>
                    <ul>
                        <li>Organize events promoting mental health and well-being</li>
                        <li>Generate creative event ideas and manage logistics</li>
                        <li>Collaborate with team members to ensure smooth execution</li>
                    </ul>
                </div>
                
                <div class="item">
                    <div class="item-title">Administrative Assistant</div>
                    <div class="item-company">حكايه اثر</div>
                    <div class="item-date">July 2022 - August 2022 | Riyadh, Saudi Arabia</div>
                    <ul>
                        <li>Organized and summarized documents and data</li>
                        <li>Managed social media accounts</li>
                        <li>Created and revised documents using Microsoft Office</li>
                        <li>Maintained records and reports</li>
                        <li>Proofread and edited correspondence</li>
                    </ul>
                </div>
            </div>
            
            <!-- Volunteer Experience -->
            <div class="section">
                <h2 class="section-title">Volunteer Experience</h2>
                
                <div class="item">
                    <div class="item-title">Student Volunteer</div>
                    <div class="item-company">Wafaa Center for Day Care | Social Services</div>
                    <div class="item-date">December 2022</div>
                    <ul>
                        <li>Created and demonstrated fun activities</li>
                        <li>Assisted staff in distributing items</li>
                        <li>Maintained a calm environment</li>
                    </ul>
                </div>
                
                <div class="item">
                    <div class="item-title">Eye-Tracking Experiment Subject</div>
                    <div class="item-company">Prince Sultan University | Education</div>
                    <div class="item-date">February 2024</div>
                    <ul>
                        <li>Participated in a research study on eye movements and comprehension</li>
                    </ul>
                </div>
                
                <div class="item">
                    <div class="item-title">Research Participant - Career & Personality Study</div>
                    <div class="item-company">Prince Sultan University | Education</div>
                    <div class="item-date">January 2024</div>
                    <ul>
                        <li>Contributed to research on career indecision and personality traits</li>
                    </ul>
                </div>
                
                <div class="item">
                    <div class="item-title">Research Participant - Linguistic Experiment</div>
                    <div class="item-company">Prince Sultan University | Education</div>
                    <div class="item-date">July 2025</div>
                    <ul>
                        <li>Participated in a linguistic experiment exploring cognitive bias</li>
                    </ul>
                </div>
            </div>
            
            <!-- Certifications -->
            <div class="section">
                <h2 class="section-title">Certifications</h2>
                <div class="two-column">
                    <div class="box">
                        <strong>Second Place - PSU Capture The Flag 1.0</strong><br>
                        Prince Sultan University - CCIS<br>
                        <span style="font-size: 0.85em; color: #777;">November 2025</span>
                    </div>
                    <div class="box">
                        <strong>Administration Assistant Certification</strong><br>
                        حكايه اثر
                    </div>
                    <div class="box">
                        <strong>First Aid Provider</strong><br>
                        Saudi Red Crescent Authority
                    </div>
                    <div class="box">
                        <strong>AI in Robotics Bootcamp 2025</strong><br>
                        Prince Sultan University
                    </div>
                </div>
            </div>
            
            <!-- Technical Skills -->
            <div class="section">
                <h2 class="section-title">Technical Skills</h2>
                <div class="skills-grid">
                    <div class="skill-box">
                        <h4>Cybersecurity & Technical</h4>
                        <ul>
                            <li>Penetration Testing</li>
                            <li>Spam Filtering</li>
                            <li>Burp Suite</li>
                            <li>Linux Systems</li>
                            <li>GitHub & Version Control</li>
                        </ul>
                    </div>
                    <div class="skill-box">
                        <h4>Development & Technology</h4>
                        <ul>
                            <li>Arduino</li>
                            <li>Robotics</li>
                            <li>Artificial Intelligence (AI)</li>
                            <li>Problem Analysis</li>
                        </ul>
                    </div>
                    <div class="skill-box">
                        <h4>Software Proficiency</h4>
                        <ul>
                            <li>Microsoft Office Suite</li>
                            <li>Document Management</li>
                            <li>Data Organization</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- Core Competencies -->
            <div class="section">
                <h2 class="section-title">Core Competencies</h2>
                <div class="tags">
                    <span class="tag">Bilingual Communications</span>
                    <span class="tag">Teamwork</span>
                    <span class="tag">Collaborative Problem Solving</span>
                    <span class="tag">Peer Development</span>
                    <span class="tag">Online Tutoring</span>
                    <span class="tag">Strategic Planning</span>
                    <span class="tag">Event Management</span>
                    <span class="tag">Analytical Skills</span>
                    <span class="tag">Creative Problem Solving</span>
                    <span class="tag">Research Skills</span>
                    <span class="tag">Empathy</span>
                    <span class="tag">Time Management</span>
                    <span class="tag">Social Media Management</span>
                    <span class="tag">Creative Writing</span>
                </div>
            </div>
            
            <!-- Languages -->
            <div class="section">
                <h2 class="section-title">Languages</h2>
                <div class="two-column">
                    <div class="box">
                        <strong>English</strong> - Fluent (IELTS: 7.5)
                    </div>
                    <div class="box">
                        <strong>Arabic</strong> - Native
                    </div>
                </div>
            </div>
            
            <!-- Interests -->
            <div class="section">
                <h2 class="section-title">Interests</h2>
                <div class="tags">
                    <span class="tag">Penetration Testing</span>
                    <span class="tag">Red Team Operations</span>
                    <span class="tag">Cybersecurity Research</span>
                    <span class="tag">Vulnerability Assessment</span>
                    <span class="tag">Ethical Hacking</span>
                    <span class="tag">Network Security</span>
                    <span class="tag">Psychology</span>
                    <span class="tag">Mental Health Advocacy</span>
                    <span class="tag">Community Service</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>