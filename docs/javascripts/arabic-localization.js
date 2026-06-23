(function () {
  "use strict";

  var exact = {
    "SYSTEM_DIRECTORY": "دليل_النظام",
    "WORKSHOP_DIRECTORY": "دليل_الورش",
    "ACADEMICS/": "الدراسة/",
    "WORKSHOPS/": "الورش/",
    "Workshops": "الورش",
    "ACADEMIC PLAN": "الخطة الدراسية",
    "COMPUTER SCIENCE/": "علوم الحاسب/",
    "COMPUTER SCIENCE": "علوم الحاسب",
    "SOFTWARE ENGINEERING/": "هندسة البرمجيات/",
    "SOFTWARE ENGINEERING": "هندسة البرمجيات",
    "CYBERSECURITY/": "الأمن السيبراني/",
    "CYBERSECURITY": "الأمن السيبراني",
    "OTHER COURSES/": "مواد أخرى/",
    "OTHER COURSES": "مواد أخرى",
    "OVERVIEW": "نظرة عامة",
    "SLIDE BREAKDOWNS": "تفكيك الشرائح",
    "SLIDES": "الشرائح",
    "SLIDES WITH NOTES": "شرائح مع ملاحظات",
    "SYLLABUS": "الخطة الدراسية",
    "STUDY MATERIAL": "المواد الدراسية",
    "Exams": "الاختبارات",
    "EXAMS": "الاختبارات",
    "EXTRA RESOURCES": "موارد إضافية",
    "WRITING RESOURCES": "موارد الكتابة",
    "MINDMAP": "الخريطة الذهنية",
    "MINDMAPS": "الخرائط الذهنية",
    "SUMMARY": "الملخص",
    "TOPICS": "الموضوعات",
    "SEQ": "الترتيب",
    "DESCRIPTOR": "الوصف",
    "SYS_STATE": "الحالة",
    "SYS_TIME": "وقت_النظام",
    "AVAILABLE": "متاح",
    "IN PROGRESS": "قيد التنفيذ",
    "COMPLETE": "مكتمل",
    "COMING SOON": "قريبا",
    "Content for this section is being prepared and will be available soon.": "يتم تجهيز محتوى هذا القسم وسيكون متاحا قريبا.",
    "PDF": "ملف",
    "Overview": "نظرة عامة",
    "Slide Breakdowns": "تفكيك الشرائح",
    "Slides": "الشرائح",
    "Slides With Notes": "شرائح مع ملاحظات",
    "Slides with Notes": "شرائح مع ملاحظات",
    "Syllabus": "الخطة الدراسية",
    "Study Material": "المواد الدراسية",
    "Quizzes": "الاختبارات",
    "Exams": "الاختبارات",
    "Extra Resources": "موارد إضافية",
    "Writing Resources": "موارد الكتابة",
    "Summary": "الملخص",
    "Topics": "الموضوعات",
    "Mindmap": "الخريطة الذهنية",
    "Mindmaps": "الخرائط الذهنية",
    "Academics": "الدراسة",
    "Computer Science": "علوم الحاسب",
    "Software Engineering": "هندسة البرمجيات",
    "Cybersecurity": "الأمن السيبراني",
    "Other Courses": "مواد أخرى",
    "[ OPEN IN NEW TAB -> ]": "[ فتح في تبويب جديد ← ]",
    "[ VIEW CONTENT -> ]": "[ عرض المحتوى ← ]",
    "[ <- BACK TO INDEX ]": "[ العودة إلى القائمة → ]",
    "[ <- BACK TO WORKSHOP ]": "[ العودة إلى الورشة → ]",
    "<- PREVIOUS": "السابق →",
    "NEXT ->": "← التالي",
    "No slide breakdowns uploaded yet": "لم ترفع تفكيكات الشرائح بعد",
    "No slides uploaded yet": "لم ترفع الشرائح بعد",
    "Quizzes coming soon": "الاختبارات قريبا",
    "Introduction": "المقدمة",
    "Quality": "الجودة",
    "Recursion": "الاستدعاء الذاتي",
    "Lists": "القوائم",
    "Trees": "الأشجار",
    "Heaps": "الأكوام",
    "Hash Tables": "جداول التجزئة",
    "Quick Sort": "الترتيب السريع",
    "Merge Sort": "الترتيب بالدمج",
    "Binary Search Trees": "أشجار البحث الثنائية",
    "Stacks and Queues": "المكدسات والطوابير",
    "Stacks & Queues": "المكدسات والطوابير",
    "Algorithm Analysis": "تحليل الخوارزميات",
    "AVL Trees": "أشجار AVL",
    "Circular Linked Lists": "القوائم المرتبطة الدائرية",
    "Directed Graphs": "الرسوم البيانية الموجهة",
    "Undirected Graphs": "الرسوم البيانية غير الموجهة",
    "Elementary Sorting Algorithms": "خوارزميات الترتيب الأساسية",
    "Heaps and Priority Queues": "الأكوام وطوابير الأولوية",
    "Data Communications and Networking": "اتصالات البيانات والشبكات",
    "Data Link Layer Control": "التحكم في طبقة ربط البيانات",
    "Data Link Layer MAC Protocols": "بروتوكولات MAC في طبقة ربط البيانات",
    "DNS and Application Layer": "نظام DNS وطبقة التطبيقات",
    "Ethernet and LANs": "إيثرنت والشبكات المحلية",
    "Interconnecting Devices and VLANs": "أجهزة الربط والشبكات المحلية الافتراضية",
    "Network Layer Data Transfer": "نقل البيانات في طبقة الشبكة",
    "Network Layer Routing": "التوجيه في طبقة الشبكة",
    "Protocol Layering and Network Models": "طبقات البروتوكولات ونماذج الشبكات",
    "Transport Layer": "طبقة النقل",
    "Application Layer": "طبقة التطبيقات",
    "Ethernet": "إيثرنت",
    "Interconnecting Devices": "أجهزة الربط",
    "Cheat Sheet": "ورقة المراجعة",
    "Full Cheat Sheet": "ورقة المراجعة الكاملة",
    "Final Cheat Sheet": "ورقة مراجعة الاختبار النهائي",
    "Midterm Cheat Sheet": "ورقة مراجعة الاختبار النصفي",
    "Final Mindmap": "الخريطة الذهنية النهائية",
    "Symbols": "الرموز",
    "Formulas": "القوانين",
    "Computer Components": "مكونات الحاسب",
    "Compiled MCQs": "أسئلة الاختيار من متعدد المجمعة",
    "Compiled Mcqs": "أسئلة الاختيار من متعدد المجمعة",
    "Midterm Exam": "الاختبار النصفي",
    "Final Exam 251 Practice": "تدريب الاختبار النهائي 251",
    "Business Ethics": "أخلاقيات الأعمال",
    "Kantianism": "الفلسفة الكانطية",
    "Utilitarianism": "النفعية",
    "Social Contract Theory": "نظرية العقد الاجتماعي",
    "Social Engineering": "الهندسة الاجتماعية",
    "Cyber Laws in Saudi Arabia": "الأنظمة السيبرانية في السعودية",
    "Privacy Issues in Cyberspace": "قضايا الخصوصية في الفضاء السيبراني",
    "Network Security and Privacy": "أمن الشبكات والخصوصية",
    "Intellectual Property Laws": "أنظمة الملكية الفكرية",
    "Argumentative Essay": "المقالة الجدلية",
    "Classification Essay": "مقالة التصنيف",
    "Process Analysis Essay": "مقالة تحليل العمليات",
    "Thesis Statement Guide": "دليل جملة الأطروحة",
    "Transition Signals": "إشارات الانتقال",
    "Grammar Cheat Sheet": "ورقة مراجعة القواعد",
    "Self Editing Checklist": "قائمة المراجعة الذاتية"
    ,"Chapter 1 Software Engineering Practices and Ethics": "الفصل الأول: ممارسات هندسة البرمجيات وأخلاقياتها"
    ,"WORKSHOP // MY JOURNEY AS A STUDENT TUTOR": "ورشة // رحلتي كمدرسة مساندة للطلاب"
    ,"WORKSHOP // CYBERSECURITY CRASH COURSE": "ورشة // دورة مكثفة في الأمن السيبراني"
    ,"My Journey As A Student Tutor": "رحلتي كمدرسة مساندة للطلاب"
    ,"My Journey as a Student Tutor": "رحلتي كمدرسة مساندة للطلاب"
    ,"Cybersecurity Crash Course": "دورة مكثفة في الأمن السيبراني"
    ,"Schedule & Agenda": "الجدول والمحاور"
    ,"Topics & Learning Outcomes": "الموضوعات ومخرجات التعلم"
    ,"Handouts": "المذكرات"
    ,"Labs & Bandit Notes": "المختبرات وملاحظات بانديت"
    ,"Reflection & Impact": "التأمل والأثر"
    ,"Agenda": "المحاور"
    ,"Timeline": "الخط الزمني"
    ,"Skills": "المهارات"
    ,"Growth": "التطور"
    ,"Feedback": "التغذية الراجعة"
    ,"Tips": "النصائح"
    ,"Reflection": "التأمل"
    ,"Video": "الفيديو"
  };

  var words = {
    "Chapter": "الفصل", "Ch": "الفصل", "Part": "الجزء", "Lecture": "المحاضرة",
    "Introduction": "مقدمة", "Foundations": "أساسيات", "Fundamentals": "أساسيات",
    "Basics": "أساسيات", "Advanced": "متقدم", "Extra": "إضافي", "Supplement": "ملحق",
    "Handouts": "ملخصات", "Guide": "دليل", "Notes": "ملاحظات", "Practice": "تدريب",
    "Quiz": "اختبار", "Exam": "اختبار", "Midterm": "نصفي", "Final": "نهائي",
    "Cheat": "مراجعة", "Sheet": "ورقة", "Mind": "ذهنية", "Map": "خريطة",
    "Communications": "اتصالات", "Communication": "اتصال", "Data": "بيانات",
    "Networking": "شبكات", "Network": "شبكة", "Layer": "طبقة", "Control": "تحكم",
    "Protocols": "بروتوكولات", "Protocol": "بروتوكول", "Application": "تطبيقات",
    "Applications": "تطبيقات", "Transport": "نقل", "Routing": "توجيه",
    "Transfer": "نقل", "Devices": "أجهزة", "Models": "نماذج",
    "Systems": "أنظمة", "System": "نظام", "Architecture": "معمارية",
    "Design": "تصميم", "Patterns": "أنماط", "Pattern": "نمط", "Principles": "مبادئ",
    "Requirements": "متطلبات", "Requirement": "متطلب", "Engineering": "هندسة",
    "Software": "برمجيات", "Processes": "عمليات", "Process": "عملية",
    "Agile": "رشيقة", "Project": "مشروع", "Management": "إدارة",
    "Construction": "بناء", "Implementation": "تنفيذ", "Testing": "اختبار",
    "Test": "اختبار", "Quality": "جودة", "Metrics": "مقاييس", "Tools": "أدوات",
    "Techniques": "تقنيات", "Coverage": "تغطية", "Regression": "انحدار",
    "Unit": "وحدة", "Code": "شفرة", "Throughout": "خلال", "Development": "تطوير",
    "Approach": "منهج", "Scheduling": "جدولة", "Tracking": "تتبع",
    "Change": "تغيير", "Team": "فريق", "Risk": "مخاطر", "Estimation": "تقدير",
    "Stakeholders": "أصحاب المصلحة", "Performance": "أداء", "Domains": "مجالات",
    "Methods": "أساليب", "Artifacts": "مخرجات", "Tailoring": "تخصيص",
    "Documentation": "توثيق", "Standards": "معايير", "Inception": "بدء",
    "Elicitation": "استنباط", "Analysis": "تحليل", "Specification": "مواصفات",
    "Validation": "تحقق", "Prioritization": "تحديد الأولويات", "Nonfunctional": "غير وظيفية",
    "Writing": "كتابة", "Excellent": "ممتازة", "Domain": "مجال", "Modeling": "نمذجة",
    "Database": "قواعد البيانات", "Databases": "قواعد البيانات", "Relational": "علائقي",
    "Normalization": "تطبيع", "Mapping": "تحويل", "Concepts": "مفاهيم",
    "Conceptual": "مفاهيمي", "Objects": "كائنات", "Object": "كائن",
    "Oriented": "موجه", "Basic": "أساسي", "Fundamentals": "أساسيات",
    "Cryptography": "تشفير", "Asymmetric": "غير متماثل", "Authentication": "مصادقة",
    "Access": "وصول", "Security": "أمن", "Cybersecurity": "أمن سيبراني",
    "Threat": "تهديد", "Threats": "تهديدات", "Vulnerabilities": "ثغرات",
    "Countermeasures": "إجراءات مضادة", "Protection": "حماية", "Information": "معلومات",
    "Assets": "أصول", "Capabilities": "قدرات", "Computer": "حاسب",
    "Operating": "تشغيل", "Services": "خدمات", "Threads": "خيوط",
    "Scheduling": "جدولة", "Synchronization": "تزامن", "Memory": "ذاكرة",
    "Virtual": "افتراضية", "Mass": "ضخم", "Storage": "تخزين", "File": "ملفات",
    "Interface": "واجهة", "Deadlocks": "تعطل متبادل", "Textbook": "الكتاب",
    "Logic": "منطق", "Proof": "برهان", "Proofs": "براهين", "Sets": "مجموعات",
    "Functions": "دوال", "Sequences": "متتاليات", "Sums": "مجاميع",
    "Number": "أعداد", "Theory": "نظرية", "Mathematical": "رياضي",
    "Induction": "استقراء", "Counting": "عد", "Relations": "علاقات",
    "Classes": "فئات", "Comparable": "قابل للمقارنة", "Comparator": "مقارن",
    "Interfaces": "واجهات", "Files": "ملفات", "Generic": "عامة",
    "Inheritance": "وراثة", "Polymorphism": "تعدد الأشكال", "Collection": "تجميع",
    "Framework": "إطار عمل", "Linked": "مرتبطة", "Lists": "قوائم",
    "Circular": "دائرية", "Directed": "موجهة", "Undirected": "غير موجهة",
    "Graphs": "رسوم بيانية", "Elementary": "أساسية", "Sorting": "ترتيب",
    "Algorithms": "خوارزميات", "Priority": "أولوية", "Queues": "طوابير",
    "Stacks": "مكدسات", "Search": "بحث", "Trees": "أشجار", "Quick": "سريع",
    "Merge": "دمج", "Hash": "تجزئة", "Heaps": "أكوام", "Recursion": "استدعاء ذاتي",
    "Ethical": "أخلاقية", "Ethics": "أخلاقيات", "Moral": "أخلاقية",
    "Practices": "ممارسات", "Practice": "تدريب", "Learning": "تعلم",
    "Outcomes": "مخرجات", "Schedule": "جدول", "Agenda": "محاور",
    "Labs": "مختبرات", "Notes": "ملاحظات", "Reflection": "تأمل",
    "Impact": "أثر", "Timeline": "خط زمني", "Skills": "مهارات",
    "Growth": "تطور", "Feedback": "تغذية راجعة", "Tips": "نصائح",
    "Video": "فيديو", "Journey": "رحلة", "Student": "طالب", "Tutor": "مدرس",
    "Workshop": "ورشة", "Crash": "مكثفة", "Course": "دورة",
    "Privacy": "خصوصية", "Cloud": "سحابية", "Computing": "حوسبة",
    "Legal": "قانونية", "Laws": "أنظمة", "Saudi": "السعودية", "Arabia": "",
    "Media": "إعلام", "Business": "أعمال", "Contract": "عقد", "Theory": "نظرية",
    "Intellectual": "فكرية", "Property": "ملكية", "Hacking": "اختراق",
    "Essay": "مقالة", "Compare": "مقارنة", "Contrast": "مقابلة", "Cause": "سبب",
    "Effect": "نتيجة", "Classification": "تصنيف", "Argumentative": "جدلية",
    "Punctuation": "ترقيم", "Transition": "انتقال", "Transitions": "انتقالات",
    "Thesis": "أطروحة", "Statement": "جملة", "Worksheet": "ورقة عمل",
    "Assignment": "واجب", "Overview": "نظرة عامة", "Materials": "مواد",
    "Electric": "كهربائية", "Charge": "شحنة", "Fields": "مجالات", "Potential": "جهد",
    "Capacitance": "سعة", "Current": "تيار", "Resistance": "مقاومة",
    "Circuits": "دوائر", "Magnetic": "مغناطيسية", "Induction": "حث",
    "and": "و", "And": "و", "of": "ل", "Of": "ل", "to": "إلى", "To": "إلى",
    "in": "في", "In": "في", "the": "", "The": "", "for": "ل", "For": "ل",
    "Using": "باستخدام", "Throughout": "خلال", "with": "مع", "Without": "بدون"
  };

  var selectors = [
    ".sidebar .sidebar-title", ".sidebar .tree-course-link", ".sidebar .tree-file",
    ".academic-sidebar .sidebar-title", ".academic-sidebar .tree-file",
    ".breadcrumb a", ".breadcrumb .current", ".type-label", ".tab", ".sub-nav-item",
    ".quick-link-btn", ".dir-header span", ".dir-title", ".status-tag", ".ch-label",
    ".ch-title", ".action-buttons .btn", ".nav-strip .nav-link", ".hero-label",
    ".section-label", ".data-block-label", ".meta-key", ".coming-soon-title",
    ".coming-soon-text"
  ].join(",");

  function normalize(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function transliterate(word) {
    // Course identifiers are proper codes, not words. Keep their canonical
    // Latin spelling in Arabic mode instead of transliterating the letters.
    if (/^(?:CS|SE|CYS|ETHCS|ISLM|ISC|SCI|PHY|ENGL|ENG)\d+$/i.test(word)) {
      return word.toUpperCase();
    }
    var pairs = {
      "sh": "ش", "ch": "تش", "th": "ث", "ph": "ف", "kh": "خ", "gh": "غ",
      "ck": "ك", "qu": "كو", "tion": "شن", "ing": "ينغ"
    };
    var output = word.toLowerCase();
    Object.keys(pairs).sort(function (a, b) { return b.length - a.length; }).forEach(function (key) {
      output = output.split(key).join(pairs[key]);
    });
    var letters = {
      a: "ا", b: "ب", c: "ك", d: "د", e: "ي", f: "ف", g: "ج", h: "ه",
      i: "ي", j: "ج", k: "ك", l: "ل", m: "م", n: "ن", o: "و", p: "ب",
      q: "ق", r: "ر", s: "س", t: "ت", u: "و", v: "ف", w: "و", x: "كس",
      y: "ي", z: "ز"
    };
    return output.replace(/[a-z]/g, function (letter) { return letters[letter] || letter; });
  }

  function translate(value) {
    var text = normalize(value);
    if (!text || !/[A-Za-z]/.test(text)) return text;
    var marker = text.match(/^(\[[+-]\]\s*)?(.*?)(\/)?$/);
    var core = marker ? marker[2] : text;
    var exactKey = Object.keys(exact).find(function (key) { return key.toLowerCase() === core.toLowerCase(); });
    if (exactKey) return (marker && marker[1] ? marker[1] : "") + exact[exactKey] + (marker && marker[3] && !exact[exactKey].endsWith("/") ? "/" : "");
    text = text.replace(/^ITEM_(\d+)\s*\/\/\s*(.+)$/i, function (_, n, section) {
      return "العنصر_" + n + " // " + translate(section);
    });
    text = text.replace(/\b(Chapter|Ch)\s*(\d+)\b/gi, "الفصل $2");
    text = text.replace(/\b(Quiz)\s*(\d+)\b/gi, "الاختبار $2");
    Object.keys(words).sort(function (a, b) { return b.length - a.length; }).forEach(function (word) {
      text = text.replace(new RegExp("\\b" + word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b", "g"), words[word]);
    });
    text = text.replace(/[A-Za-z]+(?:[.-][A-Za-z]+)*\d*/g, transliterate);
    return normalize(text);
  }

  function findTrailingTextNode(node) {
    for (var i = 0; i < node.childNodes.length; i++) {
      var child = node.childNodes[i];
      if (child.nodeType === 3 && child.textContent.trim()) return child;
    }
    return null;
  }

  function applyArabic() {
    document.querySelectorAll(selectors).forEach(function (node) {
      var textNode = node.children.length ? findTrailingTextNode(node) : null;
      if (textNode) {
        if (!node.dataset.arOriginal) node.dataset.arOriginal = textNode.textContent;
        textNode.textContent = translate(node.dataset.arOriginal);
      } else {
        if (!node.dataset.arOriginal) node.dataset.arOriginal = node.textContent;
        node.textContent = translate(node.dataset.arOriginal);
      }
    });
    document.querySelectorAll('[data-ar-text]').forEach(function (node) {
      var textNode = node.children.length ? findTrailingTextNode(node) : null;
      if (textNode) {
        if (!node.dataset.arOriginal) node.dataset.arOriginal = textNode.textContent;
        textNode.textContent = node.getAttribute('data-ar-text');
      } else {
        if (!node.dataset.arOriginal) node.dataset.arOriginal = node.textContent;
        node.textContent = node.getAttribute('data-ar-text');
      }
    });
    document.querySelectorAll(".sys-time").forEach(function (node) {
      if (!node.dataset.arOriginal) node.dataset.arOriginal = node.textContent;
      node.textContent = node.textContent.replace("SYS_TIME", "وقت_النظام");
    });
  }

  function restoreEnglish() {
    document.querySelectorAll("[data-ar-original]").forEach(function (node) {
      var textNode = node.children.length ? findTrailingTextNode(node) : null;
      if (textNode) {
        textNode.textContent = node.dataset.arOriginal;
      } else {
        node.textContent = node.dataset.arOriginal;
      }
    });
  }

  function requestedLanguage() {
    try {
      var queryLang = new URLSearchParams(window.location.search).get("lang");
      if (queryLang === "ar" || queryLang === "en") return queryLang;
      var storedLang = localStorage.getItem("shoug-lang");
      if (storedLang === "ar" || storedLang === "en") return storedLang;
    } catch (error) {
      // Ignore storage/query failures and fall back to the document language.
    }
    return String(document.documentElement.lang || "").toLowerCase().indexOf("ar") === 0 ? "ar" : "en";
  }

  function setDocumentLanguage(lang) {
    document.documentElement.lang = lang === "ar" ? "ar-SA" : "en";
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    if (document.body) document.body.classList.toggle("shoug-arabic-mode", lang === "ar");
  }

  function ensureLanguageToggle() {
    return document.querySelector("[data-lang-toggle]");
  }

  function syncToggleLabel() {
    var toggle = ensureLanguageToggle();
    if (!toggle) return;
    var isArabic = String(document.documentElement.lang || "").toLowerCase().indexOf("ar") === 0;
    toggle.textContent = isArabic ? "EN" : "AR";
    toggle.setAttribute("aria-label", isArabic ? "حوّل إلى الإنجليزية" : "Switch to Arabic");
  }

  function showAiWarning() {
    if (!document.body) return;
    var banner = document.getElementById("shoug-ar-ai-warning");
    if (!banner) {
      banner = document.createElement("div");
      banner.id = "shoug-ar-ai-warning";
      banner.setAttribute("dir", "rtl");
      banner.setAttribute("lang", "ar");
      banner.textContent = "إنذار : تم ترجمة هذه الصفحة باستخدام الذكاء الاصطناعي.";
      banner.title = "إخفاء";
      banner.style.cssText = [
        "position:fixed", "bottom:16px", "right:16px", "z-index:99999",
        "background:#ff2e2e", "color:#fff", "font-family:'JetBrains Mono',monospace",
        "font-weight:700", "font-size:12px", "letter-spacing:0.01em", "line-height:1.6",
        "padding:10px 16px", "border-radius:6px", "max-width:280px",
        "box-shadow:0 8px 24px rgba(255,46,46,0.45)", "cursor:pointer",
        "text-align:right"
      ].join(";");
      banner.addEventListener("click", function () { banner.style.display = "none"; });
      document.body.appendChild(banner);
    }
    banner.style.display = "block";
  }

  function hideAiWarning() {
    var banner = document.getElementById("shoug-ar-ai-warning");
    if (banner) banner.style.display = "none";
  }

  function sync() {
    if (String(document.documentElement.lang || "").toLowerCase().indexOf("ar") === 0) {
      applyArabic();
      showAiWarning();
    } else {
      restoreEnglish();
      hideAiWarning();
    }
    syncToggleLabel();
  }

  setDocumentLanguage(requestedLanguage());
  sync();
  document.addEventListener("DOMContentLoaded", function () {
    setDocumentLanguage(requestedLanguage());
    sync();
  });
  window.addEventListener("storage", function (event) {
    if (event.key === "shoug-lang") {
      setDocumentLanguage(requestedLanguage());
      setTimeout(sync, 0);
    }
  });
  new MutationObserver(function (mutations) {
    if (mutations.some(function (mutation) { return mutation.attributeName === "lang"; })) {
      setTimeout(sync, 0);
    }
  }).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  window.__shougTranslateArabic = translate;
  window.__shougArabicGlossary = { exact: exact, words: words };
  document.documentElement.setAttribute("data-ar-localization-ready", "true");
})();
