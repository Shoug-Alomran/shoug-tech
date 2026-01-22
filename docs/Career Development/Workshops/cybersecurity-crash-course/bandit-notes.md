# OverTheWire Bandit – Documentation (Level 0 → Level 33)

Wargame: https://overthewire.org/wargames/bandit/

Objective: Gain familiarity with Linux commands, networking, file permissions, and privilege mechanisms through incremental challenges.

## Level 0 → Level 1

**Level Goal**  
Log in via SSH and read the `readme` file.

**Commands Used**
```
ssh bandit0@bandit.labs.overthewire.org
 -p 2220
cat readme
```

**Solution Explanation**  
Connected to the server via SSH, then displayed the contents of `readme`.

**Password for Next Level**  
`ZjLjTmM6FvvyrNrb2rfNWOZ0TA6ip5If`

**Screenshot**  
![Level 0 Screenshot](../pics/Level 0.png)
![Level 0 Screenshot](../pics/Level 0 → Level 1.png)

---

## Level 1 → Level 2

**Level Goal**  
Read a file named `-`.

**Commands Used**
```
ls -a
cat ./-
```

**Solution Explanation**  
`./` ensures `-` is treated as a filename instead of an option.

**Password for Next Level**  
`263JGJPfgU6LdtEvgfWU1XP5yac29mFx`

**Screenshot**  
![Level 1 Screenshot](../pics/Level 1 → Level 2.png)

---

## Level 2 → Level 3

**Level Goal**  
Read a file containing spaces in its name.

**Commands Used**
```
ls
cat "spaces in this filename"
```

**Solution Explanation**  
Quotation prevents word splitting.

**Password for Next Level**  
`MNk8KNH3USiio41PRUEoDFPqFxLPlSmx`

**Screenshot**  
![Level 2 Screenshot]((../pics/Level 2 → Level 3.png)

---

## Level 3 → Level 4

**Level Goal**  
Find and read a hidden file in `inhere`.

**Commands Used**
```
cd inhere
ls -a
cat .hidden
```

**Solution Explanation**  
`ls -a` reveals hidden files.

**Password for Next Level**  
`2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ`

---

## Level 4 → Level 5

**Level Goal**  
Identify human-readable file among binary files.

**Commands Used**
```
cd inhere
file ./*
cat ./-file07
```

**Solution Explanation**  
`file` identifies readable data.

**Password for Next Level**  
`4oQYVPkXZOOEO5pTW8IFB8jLXxXGUQw`

**Screenshot**  
![Level 4 Screenshot](../pics/Level 4 → Level 5.png)

---

## Level 5 → Level 6

**Level Goal**  
Find a file that is human-readable, 1033 bytes, and non-executable.

**Commands Used**
```
find . -type f -size 1033c ! -executable
cat ./maybehere07/.file2
```

**Solution Explanation**  
`find` filters files based on criteria.

**Password for Next Level**  
`HWasnPhtq9AVKe0dmk45knq0vcUahz0E6G`

**Screenshot**  
![Level 5 Screenshot](../pics/Level 5 → Level 6.png)

---

## Level 6 → Level 7

**Level Goal**  
Find a 33-byte file owned by `bandit7` and group `bandit6`.

**Commands Used**
```
find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat /var/lib/dpkg/info/bandit7.password
```

**Solution Explanation**  
Filtered by size, owner, and group.

**Password for Next Level**  
`z7WtoNQU7NDBdjH8R3TaUUOFd1VtY79s`

**Screenshot**  
![Level 6 Screenshot](../pics/Level 6 → Level 7.png)

---

## Level 7 → Level 8

**Level Goal**  
Find password next to the word `millionth`.

**Commands Used**
```
grep "millionth" data.txt
```

**Solution Explanation**  
`grep` finds the matching line.

**Password for Next Level**  
`dfwvzFQi4mU0wFnNbFOe9ROwskMLg7eEc`

**Screenshot**  
![Level 7 Screenshot](../pics/Level 7 → Level 8.png)

---

## Level 8 → Level 9

**Level Goal**  
Find unique line in file.

**Commands Used**
```
sort data.txt | uniq -u
```

**Solution Explanation**  
`uniq -u` prints non-duplicate line.

**Password for Next Level**  
`4CKMh1Jl9IbUIZZPXDQGamal4xvAgOJIM`

**Screenshot**  
![Level 8 Screenshot](../pics/Level 8 → Level 9.png)

---

## Level 9 → Level 10

**Level Goal**  
Extract human-readable strings from binary.

**Commands Used**

**Solution Explanation**  
`uniq -u` prints non-duplicate line.

**Password for Next Level**  
`4CKMh1Jl9IbUIZZPXDQGamal4xvAgOJIM`

**Screenshot**  
![Level 8 Screenshot](../pics/Level 9 → Level 10.png)

---

## Level 9 → Level 10

**Level Goal**  
Extract human-readable strings from binary.

**Commands Used**
```
strings data.txt | grep '='
```

**Solution Explanation**  
`strings` prints readable sequences.

**Password for Next Level**  
`FGUVW5ilLVJrxX9kMYMMnlN4MgbpfMiqey`

**Screenshot**  
![Level 9 Screenshot](../pics/Level 9 → Level 10.png)

---

## Level 10 → Level 11

**Level Goal**  
Base64 decode data.

**Commands Used**

**Solution Explanation**  
`strings` prints readable sequences.

**Password for Next Level**  
`FGUVW5ilLVJrxX9kMYMMnlN4MgbpfMiqey`

**Screenshot**  
![Level 9 Screenshot](../pics/Level 10 → Level 11.png)

---

## Level 10 → Level 11

**Level Goal**  
Base64 decode data.

**Commands Used**
```
base64 -d data.txt
```

**Solution Explanation**  
Identified base64 encoding and decoded.

**Password for Next Level**  
`NU5P2RAyE6SBNpBuLktgVWnhDd2U6l7Q`

**Screenshot**  
![Level 10 Screenshot](../pics/Level 10 → Level 11.png)

---

## Level 11 → Level 12

**Level Goal**  
Decode ROT13 encoded text.

**Commands Used**
```
tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt
```

**Solution Explanation**  
ROT13 shifts letters by 13 positions.

**Password for Next Level**  
`5GX7M8S1LKP4E3CA6J75FHD9C2ZVXB1`

**Screenshot**  
![Level 11 Screenshot](../pics/Level 11 → Level 12.png)

---

## Level 12 → Level 13

**Level Goal**  
Unpack nested compressed file.

**Commands Used**
```
xxd -r data.txt > data.bin
file data.bin
```
repeated extraction (gzip, bzip2, tar, etc.)

**Solution Explanation**  
Extracted repeatedly until plaintext password retrieved.

**Password for Next Level**  
`8xCjnmgoKbgGLhHFAZ1GE5Tmu4M2tKJQo`

**Screenshot**  
![Level 12 Screenshot](../pics/Level 12 → Level 13.png)

---

## Level 13 → Level 14

**Level Goal**  
Login using provided SSH private key.

**Commands Used**
```
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org
 -p 2220
 ```

**Solution Explanation**  
Authenticated via RSA private key instead of password.

**Password for Next Level**  
(Password not displayed in this level)

---

## Level 14 → Level 15

**Level Goal**  
Send password to port `30000` via TCP.

**Commands Used**
```
nc localhost 30000
```

**Solution Explanation**  
Server validates input and returns password.

**Password for Next Level**  
`BfMYroe26WYalil77FoDi9qh59eK5xNr`

**Screenshot**  
![Level 14 Screenshot](../pics/Level 14 → Level 15.png)

---

## Level 15 → Level 16

**Level Goal**  
Establish SSL connection and submit password.

**Commands Used**
```
openssl s_client -connect localhost:30001
```

**Solution Explanation**  
Encrypted channel required to receive password.

**Password for Next Level**  
`kSkVUpMQ7lBYyCM4GBPvcvT1BfWRy0Dx`

**Screenshot**  
![Level 15 Screenshot](../pics/Level 15 → Level 16.png)

---

## Level 16 → Level 17

**Level Goal**  
Find SSL-enabled port between 31000–32000 and submit password.

**Commands Used**
```
nmap -sV -p31000-32000 localhost
openssl s_client -connect localhost:31790
```

**Solution Explanation**  
Port `31790` returns RSA private key for bandit17.

**Password for Next Level**  
RSA Private Key (used for SSH auth)

**Screenshot**  
![Level 16 Screenshot](../pics/Level 16 → Level 17.png)

---

## Level 17 → Level 18

**Level Goal**  
Compare two files to find difference.

**Commands Used**
```
diff passwords.new passwords.old
```

**Solution Explanation**  
The changed line indicates the password.

**Password for Next Level**  
`x2gLTTjFwMOhQ8oWNbMN362QKxfRqGl0`

**Screenshot**  
![Level 17 Screenshot](../pics/Level 17 → Level 18.png)
![Level 17 Screenshot](../pics/Level 17 → Level 18_2.png)


---

## Level 18 → Level 19

**Level Goal**  
`.bashrc` logs out interactive shell, so read file non-interactively.

**Commands Used**
```
ssh bandit18@bandit.labs.overthewire.org
 -p 2220 cat readme
```

**Solution Explanation**  
Command executes before logout triggers.

**Password for Next Level**  
`cGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8`

**Screenshot**  
![Level 18 Screenshot](../pics/Level 18 → Level 19.png)

---

## Level 19 → Level 20

**Level Goal**  
Use setuid binary to read bandit20 password.

**Commands Used**
```
./bandit20-do cat /etc/bandit_pass/bandit20
```

**Solution Explanation**  
`bandit20-do` executes command with bandit20 privileges.

**Password for Next Level**  
`0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO`

**Screenshot**  
![Level 19 Screenshot](../pics/Level 19 → Level 20.png)

---

## Completion Status

Completed Levels: **0 → 20**