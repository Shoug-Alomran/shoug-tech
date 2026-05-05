!!! warning "تنبيه"
    إنذار : تم ترجمة هذه الصفحة باستخدام الذكاء الاصطناعي.

# OverTheWire Bandit — شرح كامل للمستويات (0 ← 33)

← [رجوع إلى نظرة عامة على الورشة](overview.md)

**لعبة Bandit:** [overthewire.org/wargames/bandit](https://overthewire.org/wargames/bandit/)  
**تاريخ الإكمال:** يناير 2026 · **المستويات:** 0 ← 33

**الهدف:** التعرف على أوامر لينكس، الشبكات، صلاحيات الملفات، أنظمة التحكم بالنسخ (Git)، وتصعيد الصلاحيات من خلال تحديات متدرجة.

---

## تصفح سريع

| المستويات | التركيز |
|---|---|
| [0 – 3](#level-0) | اتصال SSH، قراءة الملفات الأساسية، الملفات المخفية |
| [4 – 6](#level-4-5) | أنواع الملفات، أمر find، البحث في نظام الملفات |
| [7 – 9](#level-7-8) | grep، sort/uniq، strings |
| [10 – 12](#level-10-11) | Base64، ROT13، طبقات الضغط |
| [13 – 16](#level-13-14) | مفاتيح SSH، netcat، SSL/TLS، مسح المنافذ |
| [17 – 20](#level-17-18) | diff، تجاوز bashrc، برامج setuid |
| [21 – 24](#level-21-22) | مهام cron، تشفير MD5، هجوم تخمين |
| [25 – 27](#level-25-26) | الهروب من الشل، استغلال vim، SUID |
| [27 – 31](#level-27-28) | تاريخ Git، الفروع، العلامات، hooks |
| [32 – 33](#level-32-33) | تجاوز شل الأحرف الكبيرة |

---

## المستوى 0 { #level-0 .level-hero }

**الهدف**
الاتصال بسيرفر Bandit باستخدام SSH واسترجاع كلمة المرور للمستوى التالي.

**الأوامر المستخدمة**
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```

**شرح الحل**

- أمر `ssh` ينشئ اتصال آمن (Secure Shell) بالنظام البعيد
- `bandit0@bandit.labs.overthewire.org` يحدد اسم المستخدم والجهاز المستهدف
- الخيار `-p 2220` يتصل عبر المنفذ 2220 (مطلوب في Bandit بدلاً من المنفذ الافتراضي 22)
- كلمة مرور المستوى 0 معطاة مباشرة: `bandit0`

**كلمة المرور للمستوى التالي**
`bandit0`

??? example "لقطة شاشة"
    ![المستوى 0](/career-development/Workshops/cybersecurity-crash-course/pics/Level-0.png)


---

## المستوى 0 ← المستوى 1 { #level-0-1 .level-hero }

**الهدف**
تحديد موقع الملف الذي يحتوي على كلمة مرور المستوى التالي واستخدامها للدخول كمستخدم bandit1.

**الأوامر المستخدمة**
```bash
ls
cat readme
```

**شرح الحل**

- أمر `ls` عرض الملفات في المجلد الحالي، وأكد وجود ملف اسمه `readme`
- أمر `cat readme` طبع محتويات ملف readme على الشاشة، وظهرت كلمة المرور

**أخطاء شائعة**
- محاولة استخدام `cd readme` (التعامل معه كمجلد بدلاً من ملف)

**كلمة المرور للمستوى التالي**
`ZjLjTmM6FvvyrNrb2rfNWOZ0TA6ip5If`

??? example "لقطة شاشة"
    ![المستوى 0 ← المستوى 1](/career-development/Workshops/cybersecurity-crash-course/pics/Level-0-→-Level-1.png)

---

## المستوى 1 ← المستوى 2 { #level-1-2 .level-hero }

**الهدف**
قراءة ملف اسمه `-` ويتطلب معاملة خاصة بسبب وجود الرمز الخاص.

**الأوامر المستخدمة**
```bash
ls
cat ./-
```

**شرح الحل**

- أمر `ls` أظهر ملفًا اسمه `-`
- الأمر `cat ./-` عرض محتويات الملف
- البادئة `./` مطلوبة لأن `-` لوحده يتم تفسيره كمؤشر للإدخال القياسي (stdin)، لذا `./-` تحدد أنه اسم ملف في المجلد الحالي

**كلمة المرور للمستوى التالي**
`263JGJPfgU6LdtEvgfWU1XP5yac29mFx`

??? example "لقطة شاشة"
    ![المستوى 1 ← المستوى 2](/career-development/Workshops/cybersecurity-crash-course/pics/Level-1-→-Level-2.png)

---

## المستوى 2 ← المستوى 3 { #level-2-3 .level-hero }

**الهدف**
قراءة ملف يحتوي على مسافات في اسمه ويبدأ بشرطات.

**الأوامر المستخدمة**
```bash
ls
cat -- "--spaces in this filename--"
```

**شرح الحل**

- أمر `ls` أظهر ملفًا اسمه `--spaces in this filename--`
- لأن اسم الملف يبدأ بـ `--` ويحتوي على مسافات، الأمر استخدم:
  - أول `--` للإشارة إلى نهاية الخيارات
  - علامات اقتباس حول اسم الملف للتعامل مع المسافات
- هذا يضمن معاملة اسم الملف كوسيط ملف عادي

**كلمة المرور للمستوى التالي**
`MNk8KNH3USiio41PRUEoDFPqFxLPlSmx`

??? example "لقطة شاشة"
    ![المستوى 2 ←المستوى 3](/career-development/Workshops/cybersecurity-crash-course/pics/Level-2-→Level-3.png)

---

## المستوى 3 ← المستوى 4 { #level-3-4 .level-hero }

**الهدف**
تحديد موقع وقراءة ملف مخفي داخل مجلد `inhere`.

**الأوامر المستخدمة**
```bash
ls
cd inhere
ls -a
cat "...Hiding-From-You"
```

**شرح الحل**

- أمر `ls` حدد وجود مجلد `inhere`
- بعد الدخول للمجلد، أمر `ls` ثاني أظهر عدم وجود ملفات مرئية
- `ls -a` استُخدم لعرض كل الملفات، بما فيها المخفية (الملفات التي تبدأ بـ `.`)
- الملف المخفي `...Hiding-From-You` ظهر وتمت قراءته بـ `cat`
- تم استخدام علامات اقتباس لأن اسم الملف يبدأ بعدة نقاط

**كلمة المرور للمستوى التالي**
`2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ`

---

## المستوى 4 ← المستوى 5 { #level-4-5 .level-hero }

**الهدف**
تحديد موقع وقراءة كلمة المرور من الملف الوحيد المقروء (نص بشري) بين عدة ملفات في مجلد `inhere`.

**الأوامر المستخدمة**
```bash
cd inhere
ls
file ./*
cat ./-file07
```

**شرح الحل**

- أمر `ls` أظهر عدة ملفات مسماة ببادئة شرطة (`-file00`, `-file01`, إلخ)
- `file ./*` استُخدم لتحديد نوع كل ملف
- فقط `-file07` كان نص ASCII (نص بشري مقروء)
- `cat ./-file07` عرض المحتويات (البادئة `./` تمنع تفسير `-` كخيار)

**كلمة المرور للمستوى التالي**
`4oQYVPkXZOOEO5pTW8IFB8jLXxXGUQw`

??? example "لقطة شاشة"
    ![المستوى 4 ← المستوى 5](/career-development/Workshops/cybersecurity-crash-course/pics/Level-4-→-Level-5.png)

---

## المستوى 5 ← المستوى 6 { #level-5-6 .level-hero }

**الهدف**
إيجاد كلمة المرور المخزنة في ملف بخصائص محددة: مقروء بشريًا، حجمه 1033 بايت، وغير قابل للتنفيذ.

**الأوامر المستخدمة**
```bash
cd inhere
ls
find . -type f -size 1033c
cat ./maybehere07/.file2
```

**شرح الحل**

- أمر `ls` عرض عدة مجلدات فرعية (`maybehere00` إلى `maybehere19`)
- بدلاً من فحص كل مجلد يدويًا، `find . -type f -size 1033c` بحث بشكل متكرر عن ملفات حجمها بالضبط 1033 بايت
- الأمر أرجع `./maybehere07/.file2`
- `cat` عرض محتوياته وكلمة المرور

**كلمة المرور للمستوى التالي**
`HWasnPhtq9AVKe0dmk45knq0vcUahz0E6G`

??? example "لقطة شاشة"
    ![المستوى 5 ← المستوى 6](/career-development/Workshops/cybersecurity-crash-course/pics/Level-5-→-Level-6.png)

---

## المستوى 6 ← المستوى 7 { #level-6-7 .level-hero }

**الهدف**
تحديد موقع ملف في أي مكان بالنظام مملوك للمستخدم `bandit7` والمجموعة `bandit6` وحجمه بالضبط 33 بايت.

**الأوامر المستخدمة**
```bash
find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat /var/lib/dpkg/info/bandit7.password
```

**شرح الحل**

- أمر `find` بحث في نظام الملفات بالكامل (`/`) عن ملفات تطابق المعايير الثلاثة
- `2>/dev/null` أخفى أخطاء رفض الصلاحية
- الأمر أرجع `/var/lib/dpkg/info/bandit7.password`
- `cat` عرض كلمة المرور

**كلمة المرور للمستوى التالي**
`z7WtoNQU2XfjmMtKjX3iql6i6cA99Ce`

??? example "لقطة شاشة"
    ![المستوى 6 ← المستوى 7](/career-development/Workshops/cybersecurity-crash-course/pics/Level-6-→-Level-7.png)

---

## المستوى 7 ← المستوى 8 { #level-7-8 .level-hero }

**الهدف**
إيجاد كلمة المرور المخزنة في `data.txt` بجانب كلمة "millionth".

**الأوامر المستخدمة**
```bash
ls
grep "millionth" data.txt
```

**شرح الحل**

- أمر `grep` يبحث عن أنماط داخل الملفات
- `grep "millionth" data.txt` حدد بسرعة السطر الذي يحتوي على "millionth"
- كلمة المرور ظهرت في نفس السطر بعد الكلمة

**كلمة المرور للمستوى التالي**
`dfwvzFQi4mU0wFnNbFOe9ROwskMLg7eEc`

??? example "لقطة شاشة"
    ![المستوى 7 ← المستوى 8](/career-development/Workshops/cybersecurity-crash-course/pics/Level-7-→-Level-8.png)

---

## المستوى 8 ← المستوى 9 { #level-8-9 .level-hero }

**الهدف**
إيجاد كلمة المرور في `data.txt` التي هي السطر الوحيد الذي يتكرر مرة واحدة بالضبط.

**الأوامر المستخدمة**
```bash
sort data.txt | uniq -u
```

**شرح الحل**

- `sort data.txt` يعيد ترتيب كل الأسطر بحيث تظهر التكرارات متجاورة
- `uniq -u` يصفى ويعرض فقط الأسطر التي تحدث مرة واحدة بالضبط
- السطر الفريد هو كلمة المرور

**كلمة المرور للمستوى التالي**
`4CKMh1Jl9IbUIZZPXDQGamal4xvAgOJIM`

??? example "لقطة شاشة"
    ![المستوى 8 ← المستوى 9](/career-development/Workshops/cybersecurity-crash-course/pics/Level-8-→-Level-9.png)

---

## المستوى 9 ← المستوى 10 { #level-9-10 .level-hero }

**الهدف**
استخراج كلمة المرور من ملف ثنائي. كلمة المرور نص بشري مقروء وتسبقها عدة علامات `=`.

**الأوامر المستخدمة**
```bash
ls
strings data.txt | grep '='
```

**شرح الحل**

- `cat data.txt` يعطي محتوى ثنائي غير مقروء
- `strings data.txt` يستخرج النص المقروء بشريًا من الملف الثنائي
- `grep '='` يصفى للأسطر التي تحتوي على علامات `=`
- كلمة المرور ظهرت بعد عدة علامات `=`

**كلمة المرور للمستوى التالي**
`FGUVW5ilLVJrxX9kMYMMnlN4MgbpfMiqey`

??? example "لقطة شاشة"
    ![المستوى 9 ← المستوى 10](/career-development/Workshops/cybersecurity-crash-course/pics/Level-9-→-Level-10.png)

---

## المستوى 10 ← المستوى 11 { #level-10-11 .level-hero }

**الهدف**
استخراج كلمة المرور من ملف يحتوي على بيانات مشفرة بـ Base64.

**الأوامر المستخدمة**
```bash
cat data.txt
cat data.txt | base64 -d
```

**شرح الحل**

- عرض الملف بـ `cat` يظهر نصًا مشفرًا بـ Base64
- `base64 -d` يفك تشفير البيانات إلى نص مقروء
- المخرجات المفكوكة تظهر كلمة المرور

**أخطاء شائعة**
- افتراض أن مخرجات Base64 هي كلمة المرور نفسها (ما زالت بحاجة لفك التشفير)

**كلمة المرور للمستوى التالي**
`dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr`

??? example "لقطة شاشة"
    ![المستوى 10 ← المستوى 11](/career-development/Workshops/cybersecurity-crash-course/pics/Level-10-→-Level-11.png)

---

## المستوى 11 ← المستوى 12 { #level-11-12 .level-hero }

**الهدف**
فك تشفير نص مخزن في `data.txt` مشفر باستخدام ROT13.

**الأوامر المستخدمة**
```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

**شرح الحل**

- الملف يحتوي على نص حيث الحروف الأبجدية منقولة 13 موضعًا
- أمر `tr` يدور الحروف الكبيرة والصغيرة 13 موضعًا
- هذا يظهر كلمة المرور

**أخطاء شائعة**
- محاولة استخدام `sort` الذي لا يفك تشفير ROT13

**كلمة المرور للمستوى التالي**
`7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4`

??? example "لقطة شاشة"
    ![المستوى 11 ← المستوى 12](/career-development/Workshops/cybersecurity-crash-course/pics/Level-11-→-Level-12.png)

---

## المستوى 12 ← المستوى 13 { #level-12-13 .level-hero }

**الهدف**
استخراج كلمة المرور من ملف مضغوط بشكل متكرر وتم تفريغه بصيغة hex dump.

**الأوامر المستخدمة**
```bash
xxd -r data.txt > data.bin
file data.bin
# فك الضغط المتكرر باستخدام gzip, bzip2, tar, إلخ
```

**شرح الحل**

- البيانات معطاة كـ hex dump وتحتاج لعكسها لملف ثنائي باستخدام `xxd -r`
- الملف الناتج مر بعدة طبقات من الضغط
- كل طبقة ضغط تم تحديدها باستخدام `file`، ثم فك ضغطها بشكل مناسب

**دليل الأوامر**

| إذا أظهر `file`... | إذن افعل... |
|---|---|
| ASCII text | اعرض باستخدام `cat` |
| gzip compressed data | غيّر الاسم إلى `.gz` وفك الضغط بـ `gzip -d` |
| bzip2 compressed data | غيّر الاسم إلى `.bz2` وفك الضغط بـ `bzip2 -d` |
| POSIX tar archive | غيّر الاسم إلى `.tar` واستخرج بـ `tar -xf` |

**أخطاء شائعة**
- محاولة فك الضغط دون تحديد نوع الملف أولاً
- تغيير الامتداد إلى امتدادات غير صحيحة

**كلمة المرور للمستوى التالي**
`FO9dwdCWjbaiIh0h8J2eUKs2vdTDwAn`

??? example "لقطة شاشة"
    ![المستوى 12 ← المستوى 13](/career-development/Workshops/cybersecurity-crash-course/pics/Level-12-→-Level-13.png)

---

## المستوى 13 ← المستوى 14 { #level-13-14 .level-hero }

**الهدف**
استخدام مفتاح SSH الخاص المُعطى للدخول كمستخدم bandit14.

**الأوامر المستخدمة**
```bash
ls -l
chmod 600 sshkey.private
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220
```

**شرح الحل**

- عرض الملفات ووجدنا `sshkey.private`
- تعديل صلاحيات الملف باستخدام `chmod 600` (مطلوب من SSH للمفاتيح الخاصة)
- تم تسجيل الدخول بنجاح كمستخدم bandit14 باستخدام المفتاح الخاص مع الخيار `-i`
- ملاحظة: الاتصال بـ localhost محظور، لذا يجب استخدام اسم الجهاز البعيد

**كلمة المرور للمستوى التالي**
لا توجد كلمة مرور — الوصول لحساب bandit14 هو الهدف.

---

## المستوى 14 ← المستوى 15 { #level-14-15 .level-hero }

**الهدف**
استرجاع كلمة مرور bandit15 بإرسال كلمة مرور المستوى الحالي إلى المنفذ 30000 على الجهاز المحلي (localhost).

**الأوامر المستخدمة**
```bash
cat /etc/bandit_pass/bandit14
nc localhost 30000
```

**شرح الحل**

- قراءة كلمة المرور الحالية من `/etc/bandit_pass/bandit14`
- الاتصال بالمنفذ 30000 باستخدام netcat (`nc`)
- إرسال كلمة المرور الحالية كمدخلات
- استلام كلمة مرور المستوى التالي

**كلمة المرور للمستوى التالي**
`8xCjnmgoKbgGLhHFAZ1GE5Tmu4M2tKJQo`

??? example "لقطة شاشة"
    ![المستوى 14 ← المستوى 15](/career-development/Workshops/cybersecurity-crash-course/pics/Level-14-→-Level-15.png)

---

## المستوى 15 ← المستوى 16 { #level-15-16 .level-hero }

**الهدف**
استرجاع كلمة مرور المستوى 16 بإرسال كلمة المرور الحالية إلى المنفذ 30001 باستخدام تشفير SSL/TLS.

**الأوامر المستخدمة**
```bash
cat /etc/bandit_pass/bandit15
openssl s_client -connect localhost:30001
```

**شرح الحل**

- قراءة كلمة المرور الحالية
- إنشاء اتصال SSL/TLS باستخدام `openssl s_client`
- إدخال كلمة المرور يدويًا في جلسة SSL
- استلام كلمة مرور المستوى التالي

**أخطاء شائعة**
- استخدام netcat العادي (التشفير مطلوب على هذا المنفذ)

**كلمة المرور للمستوى التالي**
`kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx`

??? example "لقطة شاشة"
    ![المستوى 15 ← المستوى 16](/career-development/Workshops/cybersecurity-crash-course/pics/Level-15-→-Level-16.png)

---

## المستوى 16 ← المستوى 17 { #level-16-17 .level-hero }

**الهدف**
إيجاد المنفذ الصحيح الذي يدعم SSL بين 31000–32000 وإرسال كلمة المرور لاسترجاع بيانات الدخول لـ bandit17.

**الأوامر المستخدمة**
```bash
cat /etc/bandit_pass/bandit16
nmap -sV -p31000-32000 localhost
openssl s_client -connect localhost:31790
```

**شرح الحل**

- فحص المنافذ 31000–32000 باستخدام `nmap` مع كشف الخدمات
- Nmap أظهر عدة منافذ مفتوحة، مع 31518 و 31790 يتحدثان SSL
- المنفذ 31518 أعاد فقط صدى مع KEYUPDATE
- المنفذ 31790 أعاد مفتاح RSA خاص لـ bandit17 بعد إرسال كلمة المرور
- حفظ المفتاح RSA محليًا، تعديل الصلاحيات إلى 600، واستخدامه للدخول SSH إلى bandit17

**نتائج Nmap**

| المنفذ | الحالة | الخدمة |
|---|---|---|
| 31046 | مفتوح | echo |
| 31518 | مفتوح | ssl/echo |
| 31691 | مفتوح | echo |
| 31790 | مفتوح | ssl/unknown |
| 31960 | مفتوح | echo |

**كلمة المرور للمستوى التالي**
مفتاح RSA خاص (يستخدم للدخول عبر SSH)

??? example "لقطة شاشة"
    ![المستوى 16 ← المستوى 17](/career-development/Workshops/cybersecurity-crash-course/pics/Level-16-→-Level-17.png)

---

## المستوى 17 ← المستوى 18 { #level-17-18 .level-hero }

**الهدف**
مقارنة ملفين لإيجاد كلمة المرور التي تغيرت.

**الأوامر المستخدمة**
```bash
ls
diff passwords.old passwords.new
```

**شرح الحل**

- عرض الملفات للعثور على `passwords.old` و `passwords.new`
- استخدام `diff` لمقارنة الملفين
- السطر المختلف يشير إلى كلمة المرور الجديدة

**كلمة المرور للمستوى التالي**
`x2gLTTjFwMOhQ8oWNbMN362QKxfRqGl0`

**لقطات شاشة**
![المستوى 17 ← المستوى 18 لقطة 1](/career-development/Workshops/cybersecurity-crash-course/pics/Level-17-→-Level-18.png)
![المستوى 17 ← المستوى 18 لقطة 2](/career-development/Workshops/cybersecurity-crash-course/pics/Level-17-→-Level-18_2.png)

---

## المستوى 18 ← المستوى 19 { #level-18-19 .level-hero }

**الهدف**
كلمة المرور في ملف اسمه `readme`، لكن تسجيل الدخول العادي يشغل `.bashrc` معدلاً ينهي الجلسة فورًا.

**الأوامر المستخدمة**
```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme
```

**شرح الحل**

- تسجيل الدخول العادي عبر SSH غير ممكن لأن `.bashrc` ينفذ `exit`
- أوامر SSH غير التفاعلية تتجاوز `.bashrc`
- تنفيذ `cat readme` مباشرة عبر SSH يسترجع كلمة المرور دون تشغيل أمر الخروج

**كلمة المرور للمستوى التالي**
`cGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8`

??? example "لقطة شاشة"
    ![المستوى 18 ← المستوى 19](/career-development/Workshops/cybersecurity-crash-course/pics/Level-18-→-Level-19.png)

---

## المستوى 19 ← المستوى 20 { #level-19-20 .level-hero }

**الهدف**
استخدام برنامج setuid للوصول لكلمة مرور المستوى التالي.

**الأوامر المستخدمة**
```bash
ls -l
./bandit20-do cat /etc/bandit_pass/bandit20
```

**شرح الحل**

- الملف `bandit20-do` لديه بت setuid (`rws`) وهو مملوك لـ bandit20
- هذا البرنامج ينفذ الأوامر بصلاحيات bandit20
- تم استخدامه لقراءة ملف كلمة المرور لـ bandit20

**مفاهيم أساسية**

- **برنامج setuid:** برنامج يعمل بصلاحيات مالكه بدلاً من صلاحيات المستخدم المنفذ
- **تصعيد الصلاحيات:** استخدام آليات مسموح بها لتشغيل أوامر كمستخدم آخر

**كلمة المرور للمستوى التالي**
`0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO`

??? example "لقطة شاشة"
    ![المستوى 19 ← المستوى 20](/career-development/Workshops/cybersecurity-crash-course/pics/Level-19-→-Level-20.png)

---

## المستوى 20 ← المستوى 21 { #level-20-21 .level-hero }

**الهدف**
استخدام برنامج `suconnect` لاسترجاع كلمة المرور بإعداد مستمع واتصال عميل.

**الأوامر المستخدمة**
```bash
# الطرفية 1
nc -l -p 1234

# الطرفية 2
./suconnect 1234
```

**شرح الحل**

- برنامج `suconnect` يتصل بمنفذ TCP محلي كعميل
- يستقبل كلمة مرور، يتحقق منها مع كلمة مرور المستوى الحالي
- إذا كانت صحيحة، يرسل كلمة مرور المستوى التالي
- تحتاج طرفيتين: واحدة تشغل مستمعًا (`nc -l -p 1234`)، والأخرى تشغل `./suconnect 1234`
- بعد إنشاء الاتصال، أرسل كلمة المرور الحالية عبر المستمع لاستقبال كلمة مرور bandit21

**أخطاء شائعة**
- تشغيل `./suconnect <port>` قبل بدء المستمع (يسبب خطأ "Could not connect")

**كلمة المرور للمستوى التالي**
`EeoULMCra2q0dSkYj561DX7s1CpBuOBt`

??? example "لقطة شاشة"
    ![المستوى 20 ← المستوى 21](/career-development/Workshops/cybersecurity-crash-course/pics/Level-20-→-Level-21.png)

---

## المستوى 21 ← المستوى 22 { #level-21-22 .level-hero }

**الهدف**
التحقق من مهمة cron تعمل تلقائيًا واسترجاع كلمة المرور التي تكتبها.

**الأوامر المستخدمة**
```bash
cd /etc/cron.d
ls
cat cronjob_bandit22
cat /usr/bin/cronjob_bandit22.sh
cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

**شرح الحل**

- ملف تهيئة cron `cronjob_bandit22` في `/etc/cron.d` يظهر سكريبت يعمل كل دقيقة كمستخدم bandit22
- السكريبت `/usr/bin/cronjob_bandit22.sh` يضبط الصلاحيات على ملف في `/tmp/` وينسخ كلمة المرور هناك
- قراءة الملف المُنشأ في `/tmp/` تظهر كلمة المرور

**كلمة المرور للمستوى التالي**
`tRae0UfB9v0UzbCdn9cY0gQnds9GF58Q`

??? example "لقطة شاشة"
    ![المستوى 21 ← المستوى 22](/career-development/Workshops/cybersecurity-crash-course/pics/Level-21-→-Level-22.png)

---

## المستوى 22 ← المستوى 23 { #level-22-23 .level-hero }

**الهدف**
فهم سكريبت cron يستخدم تشفير MD5 لإنشاء أسماء ملفات ديناميكية، ثم استرجاع كلمة المرور.

**الأوامر المستخدمة**
```bash
cd /etc/cron.d
cat cronjob_bandit23
cat /usr/bin/cronjob_bandit23.sh
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
cat /tmp/<hash>
```

**شرح الحل**

- سكريبت cron يحسب تجزئة MD5 للنص "I am user `<username>`"
- يستخدم هذه التجزئة كاسم ملف في `/tmp/` وينسخ كلمة المرور هناك
- توليد التجزئة يدويًا لـ "I am user bandit23" وقراءة الملف المقابل يظهر كلمة المرور

**أخطاء شائعة**
- البحث عن ملف ثابت في `/tmp/` بدلاً من توليد اسم التجزئة
- مسافات غير صحيحة في أمر echo (المسافات مهمة لـ MD5)

**كلمة المرور للمستوى التالي**
`0Zf11ioIjMVN551jX3CmStKLYqjk54Ga`

??? example "لقطة شاشة"
    ![المستوى 22 ← المستوى 23](/career-development/Workshops/cybersecurity-crash-course/pics/Level-22-→-Level-23.png)

---

## المستوى 23 ← المستوى 24 { #level-23-24 .level-hero }

**الهدف**
استغلال مهمة cron تنفذ وتحذف السكريبتات من مجلد محدد.

**الأوامر المستخدمة**
```bash
cd /etc/cron.d
cat cronjob_bandit24
cat /usr/bin/cronjob_bandit24.sh
echo '#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/b24pass' > exploit.sh
chmod +x exploit.sh
cp exploit.sh /var/spool/bandit24/foo/
sleep 90
cat /tmp/b24pass
```

**شرح الحل**

- مهمة cron تعمل كمستخدم bandit24 وتنفذ أي سكريبت مملوك لـ bandit23 في `/var/spool/bandit24/foo/`
- تم إنشاء سكريبت يقرأ `/etc/bandit_pass/bandit24` ويكتبه في مكان مقروء
- نسخ السكريبت للمجلد المراقب (الملكية تبقى لـ bandit23)
- انتظار حتى ينفذه cron (يعمل كل دقيقة)
- قراءة ملف المخرجات للحصول على كلمة المرور

**أخطاء شائعة**
- وضع السكريبتات في مجلد خاطئ (يجب أن يكون في `/var/spool/bandit24/foo/`)
- عدم الانتظار كافيًا لتنفيذ cron
- عدم التحقق من ملكية الملف

**كلمة المرور للمستوى التالي**
`gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8`

??? example "لقطة شاشة"
    ![المستوى 23 ← المستوى 24](/career-development/Workshops/cybersecurity-crash-course/pics/Level-23-→-Level-24.png)

---

## المستوى 24 ← المستوى 25 { #level-24-25 .level-hero }

**الهدف**
تخمين رمز PIN من 4 أرقام بإرسال تركيبات كلمة المرور والرقم السري لخدمة على المنفذ 30002.

**الأوامر المستخدمة**
```bash
PW="gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8"
for i in $(seq -w 0000 9999); do
  echo "$PW $i"
done | nc localhost 30002
```

**شرح الحل**

- خدمة على المنفذ 30002 تطلب كلمة المرور الحالية ورقم PIN سري من 4 أرقام (0000–9999)
- استخدام حلقة for مع `seq -w 0000 9999` لتوليد رموز PIN معبأة بالأصفار
- تمرير 10,000 محاولة عبر اتصال netcat واحد
- في النهاية استلام: "Correct! The password of user bandit25 is..."

**أخطاء شائعة**
- محاولة التجربة والخطأ يدويًا (10,000 تركيبة)
- بدء اتصال جديد لكل PIN (غير فعال)
- نسيان تعبئة الأصفار (الخدمة تتوقع 4 أرقام بالضبط)

**كلمة المرور للمستوى التالي**
`iCi86ttT4KSNe1armKiwbQNmB3YJP3q4`

**لقطات شاشة**
![المستوى 24 ← المستوى 25 لقطة 1](/career-development/Workshops/cybersecurity-crash-course/pics/Level-24-→-Level-25.png)
![المستوى 24 ← المستوى 25 لقطة 2](/career-development/Workshops/cybersecurity-crash-course/pics/Level-24-→-Level-25_2.png)

---

## المستوى 25 ← المستوى 26 { #level-25-26 .level-hero }

**الهدف**
الوصول لحساب bandit26 الذي يستخدم شل مخصص يخرج فورًا. استغلال حجم الطرفية وسلوك برنامج الصفح (pager) للوصول.

!!! tip "سلسلة استغلال ملحوظة"
    هذا المستوى يربط ثلاث عمليات هروب معًا:
    التحكم بحجم الطرفية ← برنامج الصفح `more` ← `vim` ← `bash`.
    كل خطوة تستغل ميزة شرعية في أداة بطريقة غير مقصودة.

**الأوامر المستخدمة**
```bash
# جعل الطرفية صغيرة جدًا (تصغير حجم النافذة)
ssh bandit26@bandit.labs.overthewire.org -p 2220 -i bandit26.sshkey

# عندما يتوقف more:
v                     # فتح vim
:set shell=/bin/bash  # تعيين الشل في vim
:shell                # تشغيل الشل
cat /etc/bandit_pass/bandit26
```

**شرح الحل**

- شل bandit26 هو `/usr/bin/showtext` الذي يعرض نصًا عبر `more` ثم يخرج
- جعل الطرفية صغيرة جدًا حتى لا يتسع المحتوى في شاشة واحدة
- هذا يجبر `more` على عرض `--More--` وانتظار إدخال
- الضغط على `v` لفتح vim من more
- في vim، تعيين الشل إلى bash وتشغيل شل
- الآن لدينا وصول كامل bash كمستخدم bandit26

**سلسلة الاستغلال**

1. التحكم بحجم الطرفية → تشغيل `more` التفاعلي
2. `more` → الهروب إلى vim (الضغط على `v`)
3. `vim` → الهروب إلى bash (`:set shell=/bin/bash` ثم `:shell`)
4. `bash` → الوصول لكلمة المرور

**كلمة المرور للمستوى التالي**
`s0773xxkk0MXfdqOfPRVr9L3jJBUOgCZ`

??? example "لقطة شاشة"
    ![المستوى 25 ← المستوى 26](/career-development/Workshops/cybersecurity-crash-course/pics/Level-25-→-Level-26.png)

---

## المستوى 26 ← المستوى 27 { #level-26-27 .level-hero }

**الهدف**
بعد الهروب من الشل المقيد، استخدام برنامج setuid لاسترجاع كلمة مرور bandit27.

**الأوامر المستخدمة**
```bash
ls -la
./bandit27-do cat /etc/bandit_pass/bandit27
```

**شرح الحل**

- الملف `bandit27-do` لديه بت SUID ومملوك لـ bandit27
- عند تنفيذه، يعمل كمستخدم bandit27 رغم أنه شُغل بواسطة bandit26
- استخدامه لقراءة ملف كلمة المرور لـ bandit27

**كلمة المرور للمستوى التالي**
`upsNCc7vzaRDx6oZC6GiR6ERwe1MowGB`

??? example "لقطة شاشة"
    ![المستوى 26 ← المستوى 27](/career-development/Workshops/cybersecurity-crash-course/pics/Level-26-→-Level-27.png)

---

## المستوى 27 ← المستوى 28 { #level-27-28 .level-hero }

**الهدف**
استنساخ مستودع Git واسترجاع كلمة المرور من محتوياته.

**الأوامر المستخدمة**
```bash
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
cd repo
ls
cat README
```

**شرح الحل**

- استنساخ المستودع من الجهاز المحلي (ليس من داخل اتصال SSH لـ Bandit)
- المستودع يحتوي على ملف README بكلمة المرور ظاهرة مباشرة
- هذا المستوى يقدم Git كآلية لتوزيع الأسرار

**كلمة المرور للمستوى التالي**
`Yz9IpL0sBcCeuG7m9uQFt8ZNpS4HZRcN`

??? example "لقطة شاشة"
    ![المستوى 27 ← المستوى 28](/career-development/Workshops/cybersecurity-crash-course/pics/Level-27-→-Level-28.png)

---

## المستوى 28 ← المستوى 29 { #level-28-29 .level-hero }

**الهدف**
استنساخ مستودع Git وتحليل تاريخ التعديلات (commit history) لإيجاد كلمة مرور مسربة.

!!! warning "أهمية واقعية"
    هذه مشكلة أمنية حقيقية في أنظمة الإنتاج — بيانات الدخول التي تُرسل إلى Git ثم تُحذف لا تزال قابلة للاسترجاع بالكامل عبر `git log`. استخدم دائمًا متغيرات البيئة أو أدوات إدارة الأسرار. لا ترسل بيانات الدخول مباشرة أبدًا.

**الأوامر المستخدمة**
```bash
git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo
cd repo
cat README.md
git log -p
```

**شرح الحل**

- README الحالي يظهر كلمة المرور كـ `xxxxxxxx` (مخفية)
- استخدام `git log -p` لفحص تاريخ التعديلات والفروق
- العثور على تعديل سابق كان يحتوي على كلمة المرور الفعلية قبل إزالتها
- هذا يوضح أن تاريخ Git يمكن أن يسرب بيانات حساسة حتى بعد إزالتها

**كلمة المرور للمستوى التالي**
`4pT1t5DENaYuqnqvadYs1oE4QLCdjmJ7`

??? example "لقطة شاشة"
    ![المستوى 28 ← المستوى 29](/career-development/Workshops/cybersecurity-crash-course/pics/Level-28-→-Level-29.png)

---

## المستوى 29 ← المستوى 30 { #level-29-30 .level-hero }

**الهدف**
استنساخ مستودع Git وفحص الفروع غير الافتراضية للعثور على كلمة المرور.

**الأوامر المستخدمة**
```bash
git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo
cd repo
cat README.md
git branch -r
git checkout dev
cat README.md
```

**شرح الحل**

- README في الفرع الرئيسي (master) يحتوي: `password: <no passwords in production!>`
- استخدام `git branch -r` لعرض الفروع البعيدة، وكشف `origin/dev`
- الانتقال للفرع dev باستخدام `git checkout dev`
- README في فرع dev يحتوي على كلمة المرور الفعلية

**أخطاء شائعة**
- فحص الفرع الرئيسي فقط
- افتراض أن كلمة المرور في تاريخ التعديلات (مثل المستوى 28)

**كلمة المرور للمستوى التالي**
`qp30ex3VLz5MDG1n91YowTv4Q8l7CDZL`

??? example "لقطة شاشة"
    ![المستوى 29 ← المستوى 30](/career-development/Workshops/cybersecurity-crash-course/pics/Level-29-→-Level-30.png)

---

## المستوى 30 ← المستوى 31 { #level-30-31 .level-hero }

**الهدف**
استنساخ مستودع Git وفحص علامات Git (tags) للعثور على كلمة المرور.

**الأوامر المستخدمة**
```bash
git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo
cd repo
cat README.md
git tag
git show secret
```

**شرح الحل**

- README يحتوي فقط: `just an empty file... muahaha`
- استخدام `git tag` لعرض العلامات، وكشف علامة باسم `secret`
- `git show secret` عرض محتوى العلامة، الذي احتوى على كلمة المرور
- هذا يوضح أن علامات Git يمكن أن تحتوي على بيانات حساسة غير ظاهرة في شجرة العمل

**كلمة المرور للمستوى التالي**
`fb5S2xb7bRyFmAvQYQGEqsbhVyJqhnDy`

??? example "لقطة شاشة"
    ![المستوى 30 ← المستوى 31](/career-development/Workshops/cybersecurity-crash-course/pics/Level-30-→-Level-31.png)

---

## المستوى 31 ← المستوى 32 { #level-31-32 .level-hero }

**الهدف**
دفع ملف محدد إلى مستودع Git بعيد لتشغيل خطاف تحقق (validation hook) يعيد كلمة المرور.

**الأوامر المستخدمة**
```bash
git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo
cd repo
cat README.md
echo "May I come in?" > key.txt
git add -f key.txt
git commit -m "Force adding key.txt"
git push origin master
```

**شرح الحل**

- README يحدد إنشاء `key.txt` بمحتوى "May I come in؟" ودفعه للفرع الرئيسي
- الملف متجاهل بواسطة `.gitignore`، لذا `git add -f` مطلوب لإضافته قسريًا
- بعد الدفع، الخادم البعيد يشغل خطاف تحقق ويعيد كلمة المرور
- الدفع مرفوض بعد التحقق، لكن كلمة المرور ما زالت مطبوعة

**أخطاء شائعة**
- عدم استخدام `-f` عندما يمنع `.gitignore` الملف
- التوقف عند رؤية رفض الدفع (كلمة المرور لا تزال تظهر)

**كلمة المرور للمستوى التالي**
`3O9RfhqyAlVBEZpVb6LYStshZoqoSx5K`

??? example "لقطة شاشة"
    ![المستوى 31 ← المستوى 32](/career-development/Workshops/cybersecurity-crash-course/pics/Level-31-→-Level-32.png)

---

## المستوى 32 ← المستوى 33 { #level-32-33 .level-hero }

**الهدف**
الهروب من "شل الأحرف الكبيرة" الذي يحول كل الإدخال لأحرف كبيرة، مما يمنع تنفيذ الأوامر العادية.

!!! tip "نقطة أساسية"
    `$0` يتم توسيعه إلى مسار الشل الحالي قبل معالجة مرشح الأحرف الكبيرة — مما يجعله الطريقة الوحيدة للإشارة إلى أمر دون تحويله لأحرف كبيرة إلى صيغة غير صالحة.

**الأوامر المستخدمة**
```bash
$0
whoami
cat /etc/bandit_pass/bandit33
```

**شرح الحل**

- تسجيل الدخول إلى bandit32 يضع المستخدم في شل مقيد يجبر تحويل الأحرف إلى كبيرة
- الأوامر العادية مثل `ls` تصبح `LS` (غير صالحة)
- البرنامج `uppershell` هو SUID ومملوك لـ bandit33
- استخدام `$0` الذي يتوسع إلى مسار الشل ولا يتأثر بمرشح الأحرف الكبيرة
- هذا أنزلني إلى جلسة `sh` عادية بصلاحيات bandit33
- من هناك، الأوامر العادية عملت وأصبح ملف كلمة المرور مقروءًا

**أخطاء شائعة**
- محاولة تشغيل أوامر مثل `ls`, `cat`, `sh`, أو `bash` مباشرة (كلها تتحول لأحرف كبيرة)

**كلمة المرور للمستوى التالي**
`tQdtbs5D5i2vJwkO8mEyYEyTL8izoeJ0`

??? example "لقطة شاشة"
    ![المستوى 32 ← المستوى 33](/career-development/Workshops/cybersecurity-crash-course/pics/Level-32-→-Level-33.png)

---

## إكمال التحدي

**المستويات المكتملة:** 0 ← 33 ✓

---

## ملخص المفاهيم الأساسية

### أساسيات لينكس
- التنقل في الملفات والتعامل معها
- الملفات المخفية والأحرف الخاصة في أسماء الملفات
- صلاحيات الملفات والملكية
- صلاحيات العمليات وبرامج setuid

### معالجة النصوص
- البحث عن الأنماط بـ `grep`
- الترتيب والتصفية بـ `sort` و `uniq`
- استخراج النصوص من الملفات الثنائية
- التشفير وفك التشفير (Base64، ROT13)

### الضغط والأرشفة
- صيغ ضغط متعددة (gzip، bzip2، tar)
- عكس تفريغ hex
- فك ضغط متكرر

### الشبكات
- اتصالات TCP مع netcat
- اتصالات SSL/TLS مع OpenSSL
- فحص المنافذ بـ nmap
- اتصال خادم-عميل

### الأتمتة والجدولة
- تحليل مهام cron
- تصعيد الصلاحيات عبر السكريبتات
- أتمتة التخمين

### أنظمة التحكم بالنسخ (Git)
- استنساخ المستودعات
- تحليل تاريخ التعديلات
- إدارة الفروع
- فحص العلامات
- التفاعل مع المستودعات البعيدة

### تصعيد الصلاحيات
- استغلال برامج setuid
- تقنيات الهروب من الشل
- تجاوز الشل المقيد
- استغلال برامج الصفح والمحررات

---

**الكاتبة:** شوق العمران · **تاريخ الإكمال:** يناير 2026
