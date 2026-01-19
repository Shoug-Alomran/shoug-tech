# Bandit Lab Notes (Offensive Security Workshop)

This page contains my OverTheWire Bandit wargame documentation completed during the Cybersecurity Crash Course workshop.  
Each level documents the goal, the commands used, the solution explanation, and the obtained password.
**Game Link:** https://overthewire.org/wargames/bandit/

---

## Table of Contents

1. [Level 0 → Level 1](#level-0--level-1)
2. [Level 1 → Level 2](#level-1--level-2)
3. [Level 2 → Level 3](#level-2--level-3)
4. [Level 3 → Level 4](#level-3--level-4)
5. [Level 4 → Level 5](#level-4--level-5)
6. [Level 5 → Level 6](#level-5--level-6)
7. [Level 6 → Level 7](#level-6--level-7)
8. [Level 7 → Level 8](#level-7--level-8)
9. [Level 8 → Level 9](#level-8--level-9)
10. [Level 9 → Level 10](#level-9--level-10)

---

## Level 0 → Level 1

**Goal**  
Log in using SSH and obtain the password from the `readme` file.

**Commands Used**
```
ssh bandit0@bandit.labs.overthewire.org -p 2220
cat readme
```

**Explanation**  
Connected via SSH to the Bandit server on port 2220. The password for the next level was stored in the `readme` file in the home directory and displayed using `cat`.

**Password Obtained**  
`ZjLjTmM6FvvyrNrb2rfNWOZ0TA6ip5If`

---

## Level 1 → Level 2

**Goal**  
Retrieve the password stored in a file named `-`.

**Commands Used**
```
cd bandit1
ls -a
cat ./-
```

**Explanation**  
The file name `-` conflicts with command flags. Prefixing with `./` ensures the shell treats it as a filename rather than an option.

**Password Obtained**  
`263JGJPfgU6LdtEvgfWU1XP5yac29mFx`

---

## Level 2 → Level 3

**Goal**  
Read a file with spaces and leading dashes in its name.

**Commands Used**
```
cd bandit2
ls
cat -- "--spaces in this filename--"
```

**Explanation**  
Quoting handles spaces in filenames. The `--` indicates the end of command options so `cat` treats the remaining argument as a filename.

**Password Obtained**  
`MNk8KNH3USiio41PRUEoDFPqFxLPlSmx`

---

## Level 3 → Level 4

**Goal**  
Find the hidden file in the `inhere` directory containing the password.

**Commands Used**
```
ls
cd inhere
ls -a
cat "...Hiding-From-You"
```

**Explanation**  
The target file was hidden and revealed using `ls -a`. The filename beginning with dots was quoted to avoid shell parsing issues.

**Password Obtained**  
`2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ`

---

## Level 4 → Level 5

**Goal**  
Identify the only human-readable file within the `inhere` directory that contains the password.

**Commands Used**
```
cd bandit4
cd inhere
ls
file ./*
cat ./-file07
```

**Explanation**  
The `file` command determines file types. Only `-file07` was human-readable, and was displayed with `cat`. The leading dash required prefixing with `./`.

**Password Obtained**  
`4oQYVPkXZOOEO5pTW8IFB8jLXxXGUQw`

---

## Level 5 → Level 6

**Goal**  
Find the file that is human-readable, exactly 1033 bytes in size, and not executable.

**Commands Used**
```
cd bandit5
cd inhere
find . -type f -size 1033c
cat ./maybehere07/.file2
```

**Explanation**  
`find` searched recursively for files matching size 1033 bytes. The resulting file was displayed with `cat`, revealing the password.

**Password Obtained**  
`HWasnPhtq9AVKe0dmk45knq0vcUahz0E6G`

---

## Level 6 → Level 7

**Goal**  
Find a 33-byte file owned by user `bandit7` and group `bandit6`.

**Commands Used**
```
find / -type f -user bandit7 -group bandit6 -size 33c
cat /var/lib/dpkg/info/bandit7.password
```

**Explanation**  
Searched the entire filesystem for files matching the ownership and size requirements. The valid file was located in `/var/lib/dpkg/info` and contained the password.

**Password Obtained**  
`z7WtoNQU7NDBdjH8R3TaUUOFd1VtY79s`

---

## Level 7 → Level 8

**Goal**  
Extract the password located next to the word `millionth` in `data.txt`.

**Commands Used**
```
ls
grep "millionth" data.txt
```

**Explanation**  
`grep` filtered the file for the matching word and returned the password located on the same line.

**Password Obtained**  
`dfwvzFQi4mU0wFnNbFOe9ROwskMLg7eEc`

---

## Level 8 → Level 9

**Goal**  
Find the only line in `data.txt` that occurs exactly once.

**Commands Used**
```
sort data.txt | uniq -u
```

**Explanation**  
`sort` grouped duplicate lines together. `uniq -u` printed lines that appear only once. The result was the unique password.

**Password Obtained**  
`4CKMh1Jl9IbUIZZPXDQGamal4xvAgOJIM`

---

## Level 9 → Level 10

**Goal**  
Extract human-readable strings from a binary file and identify the line where the password is preceded by multiple equal signs.

**Commands Used**
```
strings data.txt | grep '='
```

**Explanation**  
`strings` extracted readable text from binary data. Filtering with `grep '='` isolated lines containing equals signs, revealing the password.

**Password Obtained**  
`FGUVW5ilLVJrxX9kMYMMnlN4MgbpfMiqey`

---