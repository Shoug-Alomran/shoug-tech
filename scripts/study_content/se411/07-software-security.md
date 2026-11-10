@head Chapter 7
@title Software Security
@sources chapter-7-software-security
@count 92
@tldr Authentication proves who you are, authorization decides what you may do, and Spring Security locks down a REST API by default: every request needs credentials, responses carry protective headers, and CSRF tokens guard anything that changes data. JWTs let a stateless API recognise users without sessions.
@why Exams in this chapter are mostly "match the attack to its defence" and "which status code / header / token": authentication vs authorization, 401 vs 403, SOP vs CORS, CSRF vs XSS, the Spring Security defaults, the three parts of a JWT, and where to store tokens. This page puts each one side by side.
@connect It secures Chapter 6's Product API. Filters run before the controllers from Chapter 6, the UserPrincipal adapter uses Chapter 4's interfaces, and "never put secrets in tokens or logs" repeats Chapters 1 and 3.
@goals

- Distinguish authentication from authorization and explain sessions and cookies
- Explain role-based access control in Spring
- Explain the Same Origin Policy and CORS
- Explain CSRF and XSS attacks and their defences
- List Spring Security's secure defaults and the headers it adds
- Explain why unknown endpoints return 401 instead of 404
- Configure a SecurityFilterChain and a UserDetailsService
- Describe a JWT's structure, flow and best practices
  @vocab
  Principal | The user of an API: a person or another program.
  Authentication | A principal proving its identity, such as with a password.
  Authorization | Deciding what an authenticated principal may do.
  Session token | A random string, stored in a cookie, proving you already logged in.
  Origin | Protocol + domain + port.
  CSRF | Cross-Site Request Forgery: another site makes your browser send a request you didn't intend.
  XSS | Cross-Site Scripting: an attacker's script runs inside the victim site.
  Filter chain | A sequence of checks every request passes through before the controller.
  JWT | JSON Web Token: a signed token carrying claims about the user.
  @map
  2-8 | Authentication, sessions, authorization | MEMORIZE | 401 vs 403, RBAC
  9-13 | Same Origin Policy and CORS | MEMORIZE | Response can't be read
  14-16 | CSRF and XSS | MEMORIZE | Attack and defence
  17-24 | Why the chapter 6 API is unsafe, secure defaults | MEMORIZE | Public, anonymous, unprotected
  25-39 | Spring Security defaults and headers | MEMORIZE | 401 for unknown URLs
  40-70 | Configuring Spring Security | WRITE | Filter chain, users, adapter
  71-91 | JWT | MEMORIZE | Header.Payload.Signature

## Authentication, sessions and authorization | Slides 2-8 | must

A user of an API may be a person or a program, so security texts call it a **principal**.

|              | Authentication                                          | Authorization         |
| ------------ | ------------------------------------------------------- | --------------------- |
| Question     | **Who are you?**                                        | **What may you do?**  |
| How          | Credentials, such as username and password (HTTP Basic) | Roles and permissions |
| Order        | First                                                   | After authentication  |
| Failure code | **401 Unauthorized**                                    | **403 Forbidden**     |

HTTP is **stateless**, so every request needs proof of identity. Sending the password every time is slow (and risky), so after login the server creates an **authentication session**: a random **session token** placed in a **cookie**. The browser sends cookies **automatically** with every request to that site, and the server rejects requests whose token is invalid. Cookies can persist after the page closes.

**Role-based access control (RBAC)**: each principal has roles; each resource says which roles may use it.

::code java
.requestMatchers("/admin/**").hasRole("ADMIN")
.requestMatchers("/products/**").hasRole("PRODUCT_OWNER")
::

Example roles: User (view products, place orders), Product Owner (add and update products), Administrator (manage users, products and settings). Spring supports this globally (URL patterns) and per method.

::analogy A hotel
Authentication is showing your passport at check-in. The key card you get is the session token, so you don't show your passport at every door. Authorization is which doors the card opens: your room and the gym, not the staff office.
::

Spring Security implements authentication as a **filter chain**: a series of checks called **before the controller**. Each filter decides whether processing continues.

::key

- Authentication = who you are; authorization = what you may do
- Authentication comes first
- A session token in a cookie avoids resending credentials
- RBAC grants access by role
- Spring Security checks requests in a filter chain before the controller
  ::

## Same Origin Policy and CORS | Slides 9-13 | must

An **origin** is **protocol + domain + port**. The **Same Origin Policy (SOP)**, enforced by browsers, stops a script from one origin **reading responses** from another. Without it, a malicious page in another tab could fetch your bank page (with your cookies attached) and read your balance.

::trap SOP blocks reading, not sending
SOP does **not** stop a cross-origin request from being **sent**; it stops the **response from being read**. So SOP alone doesn't stop CSRF, which only needs the request to be sent.
::

**CORS** (Cross-Origin Resource Sharing) lets a server **relax** SOP on purpose, for example for microservices on different URIs. The server lists **allowed origins** in headers such as `Access-Control-Allow-Origin`, and the **browser enforces** it. For some requests the browser first sends a **preflight OPTIONS** request.

::code java
@CrossOrigin(origins = "http://localhost:3000")
::

::trap @CrossOrigin with no arguments
It allows **all** origins, which is bad practice. Always list the allowed sites.
::
::steps CORS blocking evil.com
evil.com's script calls fetch('https://api.company.com/data').
The browser sends a preflight OPTIONS request with Origin: evil.com.
The server replies Access-Control-Allow-Origin: app.company.com.
The browser sees evil.com isn't allowed and blocks the script from proceeding.
::
::key

- Origin = protocol + domain + port
- SOP stops scripts reading other origins' responses
- SOP doesn't stop requests being sent, so it doesn't stop CSRF
- CORS lets a server allow specific origins; the browser enforces it
- Never use @CrossOrigin without listing origins
  ::

## CSRF and XSS | Slides 14-16, 36 | must

### CSRF: Cross-Site Request Forgery ("sea-surf", session riding)

Browsers attach a site's cookies to **every** request to that site, even when the request starts on another site. So a malicious page can make you perform an action on a site where you're logged in:

::code html
<img src="https://mybank.example.org/account/32?transfer=25&toAccount=45" />
::

The browser fetches the "image", sends your bank cookies, and the bank sees a valid session. By the time it's clear this isn't an image, the transfer has happened.

**Defence: a CSRF token.** The server puts a random token in the page (such as a hidden `_csrf` form field). Unlike the session cookie, it is **not sent automatically**, and SOP stops the attacker reading it, so they can't forge a valid request. Spring Security enables this **by default** for requests with side effects (**POST, PUT, DELETE**). The **SameSite** cookie attribute also helps.

### XSS: Cross-Site Scripting

The attacker gets the victim site to **run their script**. Example: a comment containing `<script>...</script>` is saved in the database and later rendered on a page, so the script runs for every visitor.

XSS is **more dangerous than CSRF**: the script runs on the real site's origin, so it can read CSRF tokens and non-HttpOnly cookies. **XSS can bypass CSRF protection.**

| Defence against XSS                | How                                                                        |
| ---------------------------------- | -------------------------------------------------------------------------- |
| **Escape output / sanitize input** | Render `<` as `&lt;` so it shows as text                                   |
| **Content Security Policy** header | Controls which scripts may run                                             |
| **HttpOnly cookies**               | JavaScript can't read them, so they can't be stolen                        |
| **Subresource integrity**          | A hash on CDN `<script>` tags, in case the library itself is tampered with |

|                  | CSRF                                  | XSS                                 |
| ---------------- | ------------------------------------- | ----------------------------------- |
| Attacker's trick | Makes **your browser send** a request | Makes **the site run** their script |
| Relies on        | Cookies sent automatically            | Unescaped external data             |
| Main defence     | CSRF token, SameSite                  | Escaping, CSP, HttpOnly             |

::mnemonic CSRF Sends, XSS eXecutes
CSRF forges a **request that gets sent**. XSS gets a **script executed** on the site.
::
::key

- CSRF: another site makes your browser send a request with your cookies
- Defend with CSRF tokens, on by default for POST, PUT and DELETE
- XSS: an attacker's script runs on the victim site
- Defend with escaping, CSP and HttpOnly cookies
- XSS is more dangerous and can bypass CSRF protection
  ::

## Spring Security's secure defaults | Slides 17-39 | must

The Chapter 6 API had three problems:

| Problem         | Meaning                                                                  |
| --------------- | ------------------------------------------------------------------------ |
| **Public**      | Anyone who can reach it sees the data                                    |
| **Anonymous**   | We can't tell who's asking, so we can't restrict users to their own data |
| **Unprotected** | Exposed to CSRF, XSS and man-in-the-middle attacks                       |

Two principles guide the fix: **Secure by Default** (the default settings are already safe, so shipping the defaults isn't a vulnerability) and **Least Privilege** (give each user the lowest privileges that let them do their job).

Adding `spring-boot-starter-security` to Maven automatically:

| Default                                      | Detail                                                                                |
| -------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Requires authentication for all requests** | Even endpoints Spring Boot generated, and even ones that don't exist                  |
| **Secure headers on every response**         | See table below                                                                       |
| **CSRF protection** on side-effect requests  | POST, PUT, DELETE                                                                     |
| **HTTP Basic with a default user**           | Username `user`; a **new random password on every startup**, printed in the log       |
| **RESTful failures**                         | 401 for missing or wrong credentials; 403 for good credentials but no permission      |
| **Application firewall**                     | Rejects double encoding and unsafe characters such as carriage returns and line feeds |

::trap Why an unknown URL returns 401, not 404
Without security, `/admin` might give 404 while a real page gives 200, telling an attacker which endpoints exist (**fingerprinting**, enumeration, directory traversal). With Spring Security, the filter rejects **every** unauthenticated request with 401 before any controller runs, so existence leaks nothing.
::

| Header                                                         | Protects against                                                             |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `X-Content-Type-Options: nosniff`                              | **MIME sniffing**: the browser guessing a .txt is HTML or script             |
| `X-Frame-Options: DENY`                                        | **Clickjacking**: your site loaded in an invisible iframe under fake buttons |
| `Cache-Control: no-cache, no-store...`, `Pragma`, `Expires: 0` | Sensitive data being cached                                                  |
| `Strict-Transport-Security`                                    | Forces HTTPS (only sent over HTTPS)                                          |
| `Content-Security-Policy`                                      | XSS and injection                                                            |
| `X-XSS-Protection`                                             | Turns on the browser's XSS filter                                            |

::analogy A building with a front desk
Spring Security is the front desk. It doesn't matter who built a room (you, Spring Boot or a third party): nobody gets past the desk without a badge, and the receptionist won't even say whether room 404 exists.
::
::key

- The unsecured API was public, anonymous and unprotected
- Secure by Default and Least Privilege
- Spring Security requires authentication for every request
- Unknown endpoints return 401, hiding which ones exist
- Default user "user" with a new password each startup
- Headers: nosniff, X-Frame-Options DENY, no-cache, HSTS, CSP
  ::

## Configuring Spring Security | Slides 40-70 | know

Requests pass through **servlet filters** before reaching a servlet (controller). Spring Security's filter sits there, so it protects **every** endpoint whoever created it.

::code java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
@Bean
public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
return http
.csrf(csrf -> csrf.disable()) // stateless API: no sessions
.authorizeHttpRequests(r -> r.anyRequest().authenticated())
.httpBasic(Customizer.withDefaults())
.sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
.build();
}
}
::

| Piece                        | Role                                                                                         |
| ---------------------------- | -------------------------------------------------------------------------------------------- |
| `@EnableWebSecurity`         | Registers the security filter chain (FilterChainProxy)                                       |
| `@Bean`                      | Marks a method whose return value Spring manages as a bean                                   |
| **SecurityFilterChain** bean | Which paths need authentication (for example "/" public, everything else authenticated)      |
| **UserDetailsService** bean  | Loads a user's details (hashed password, roles) by username, from memory, JDBC or a database |

The chained calls (`http.a().b().build()`) are the **Builder pattern**. With **stateless** sessions a new session is used per request, so the CSRF token isn't needed and form login is turned off (users would be sent back to the login page every time); HTTP Basic is used instead.

**Users in a database**: Spring expects a `UserDetails` object, but your `User` record has its own shape. A **UserPrincipal** class implements `UserDetails` and wraps a `User`: the **Adapter pattern**.

**Passwords** are stored hashed with **BCrypt** (`new BCryptPasswordEncoder(12)`), never in plain text.

The default login page includes a hidden **\_csrf** token, and logging in creates a **session ID**.

::trap Disabling CSRF is only safe without cookies
The slides disable CSRF because the API is **stateless** (credentials or a token in a header, not a session cookie). If you authenticate with cookies, keep CSRF protection on.
::
::key

- @EnableWebSecurity plus a SecurityFilterChain bean configures the rules
- UserDetailsService loads users and roles
- UserPrincipal adapts your User to Spring's UserDetails
- Hash passwords with BCrypt
- Stateless APIs disable sessions, form login and CSRF and use Basic or JWT
  ::

## JSON Web Tokens | Slides 71-91 | must

A **JWT** is an open standard for sending claims as a compact JSON object that is **digitally signed**, with a secret (HMAC) or a public/private key pair (RSA, ECDSA), so it can be verified and trusted.

::formula Structure: xxxxx.yyyyy.zzzzz
Header {"alg": "HS256", "typ": "JWT"} token type + algorithm
Payload {"sub": "1234567890", "admin": true} claims about the user
Signature sign(header + payload, secret) proves nothing was changed
::

::steps The JWT flow
The user logs in with username and password.
The server checks them and generates a JWT with claims, an expiry time and a signature.
The token is returned in the response body or as an HttpOnly cookie.
Each later request sends Authorization: Bearer <token> (or the cookie).
A JwtFilter, placed before UsernamePasswordAuthenticationFilter, validates the signature and expiry and sets the user's authentication.
Authorized requests reach the controller; others get 401 or 403.
::

It's **stateless**: the server stores no session, which suits microservices and scales well. In Spring, a `JwtService` generates and validates tokens (using the jjwt library), `JwtFilter extends OncePerRequestFilter` checks each request, and `AuthenticationManager` hands login attempts to the right provider.

::trap Signed is not encrypted
Anyone can decode a JWT's payload and read it. The signature only stops it being **changed**. Never put secrets (passwords, private data) in a token.
::

| Where the client stores it | Risk                          | Notes                                                                 |
| -------------------------- | ----------------------------- | --------------------------------------------------------------------- |
| **localStorage**           | **Stolen by XSS**             | Script adds the Authorization header itself                           |
| **HttpOnly cookie**        | **CSRF** (sent automatically) | JavaScript can't read it; use `secure(true)` and `sameSite("Strict")` |

| JWT best practice                                                      |
| ---------------------------------------------------------------------- |
| Keep the signing key private (then tokens can't be altered)            |
| Never put secrets in the token: it's signed, not encrypted             |
| Short validity, such as 15 minutes                                     |
| Prefer HttpOnly cookies; add a Content Security Policy; sanitize input |
| Use subresource integrity on CDN scripts                               |

::mnemonic HPS: Header, Payload, Signature
"**H**ow **P**eople **S**ign": the three dot-separated parts in order.
::
::analogy A festival wristband
At the gate (login) you get a tamper-proof wristband (JWT) printed with your ticket type (claims) and date (expiry). Staff at each stage just check the band is genuine and valid, with no need to call the gate. But anyone can read what's printed on it, so don't print your PIN there.
::
::key

- A JWT has a header, payload (claims) and signature
- It's signed, not encrypted: never put secrets in it
- Sent as Authorization: Bearer <token>
- Stateless: no server sessions, good for scaling
- localStorage risks XSS; HttpOnly cookies risk CSRF
- Keep tokens short-lived and the key private
  ::
  @cheat

### Identity

- Authentication: who → 401
- Authorization: what → 403
- Session token in cookie
- RBAC: hasRole("ADMIN")

### Browser rules

- Origin = protocol + domain + port
- SOP: can't READ other origin
- CORS: server allows origins
- @CrossOrigin(origins = ...), never empty

### Attacks

- CSRF: forged request with your cookies
- → CSRF token, SameSite
- XSS: attacker script runs on site
- → escape, CSP, HttpOnly
- XSS can bypass CSRF tokens

### Spring defaults

- Auth on all requests
- Unknown URL → 401, not 404
- CSRF on POST/PUT/DELETE
- Default user, new password each start
- Firewall rejects unsafe characters

### Headers

- nosniff: MIME sniffing
- X-Frame-Options DENY: clickjacking
- Cache-Control no-store
- HSTS: HTTPS only
- CSP: XSS

### Config and JWT

- SecurityFilterChain, UserDetailsService
- UserPrincipal = adapter; BCrypt
- JWT = Header.Payload.Signature
- Signed, not encrypted
- Bearer header; short expiry
  @mcq 3
  Proving your identity to a system is called:

* Authentication

- Authorization
- Encryption
- Serialization

> Slide 3.
> @mcq 38
> A logged-in customer requests an admin-only endpoint. Spring Security returns:

- 403 Forbidden

* 401 Unauthorized
* 404 Not Found
* 200 OK

> Good credentials, not authorized.
> @mcq 9
> The Same Origin Policy prevents:

- A script from reading responses from another origin

* Any cross-origin request from being sent
* All cookies from being stored
* Servers from using HTTPS

> It blocks reading, not sending.
> @mcq 11
> CORS allows:

- A server to permit specific other origins to read its responses

* A browser to ignore all security
* An attacker to bypass CSRF tokens
* Servers to store sessions

> Slide 11.
> @mcq 14
> CSRF attacks work mainly because:

- Browsers automatically send cookies with requests to a site

* Passwords are stored in plain text
* Servers use JSON
* SOP blocks all requests

> Slide 14.
> @mcq 14
> The main defence against CSRF is:

- A CSRF token that the attacker can't read

* Disabling HTTPS
* Using GET for all changes
* Storing tokens in localStorage

> Slide 14.
> @mcq 16
> Which best prevents an XSS attack from a stored `<script>` comment?

- Escaping special HTML characters when rendering

* Adding a CSRF token
* Using a longer password
* Returning 404

> Slide 16.
> @mcq 29
> Why does Spring Security return 401 for a non-existent endpoint instead of 404?

- So attackers can't learn which endpoints exist

* Because 404 is deprecated
* Because the controller crashed
* To make caching work

> Prevents fingerprinting.
> @mcq 34
> The header `X-Frame-Options: DENY` protects against:

- Clickjacking

* MIME sniffing
* SQL injection
* Race conditions

> It stops your site being framed.
> @mcq 37
> Spring Security's default user password:

- Is randomly generated on each startup

* Is always "password"
* Is stored in pom.xml
* Never changes

> Secure by default.
> @mcq 56
> UserPrincipal implements UserDetails and wraps a User. This is the:

- Adapter pattern

* Builder pattern
* Factory pattern
* Singleton pattern

> Slide 55.
> @mcq 74
> The three parts of a JWT are:

- Header, payload, signature

* Username, password, role
* Request, response, status
* Key, value, expiry

> Separated by dots.
> @mcq 91
> Which statement about JWTs is true?

- They are signed, not encrypted, so secrets must not be put in them

* They are encrypted, so passwords can be stored in them
* They never expire
* They must be stored in plain localStorage

> Slide 91.
> @mcq 90
> Storing a JWT in an HttpOnly cookie protects against XSS theft but requires protection against:

- CSRF

* Clickjacking only
* Deadlock
* MIME sniffing

> Cookies are sent automatically.
> @short 14
> Explain a CSRF attack and how a CSRF token prevents it.
> ~ cookies, automatically, forged request, token, hidden field, SOP
> A malicious page makes the victim's browser send a state-changing request, such as a transfer, to a site where they're logged in; the browser attaches the session cookie automatically. A CSRF token is embedded in the real page and must be sent with the request. It isn't sent automatically and SOP stops the attacker reading it, so forged requests fail.
> @short 16
> Compare CSRF and XSS, with one defence for each.
> ~ request sent, script executes, token, escaping, CSP, HttpOnly
> CSRF tricks the browser into sending a request with the user's cookies; it's defended with CSRF tokens or SameSite cookies. XSS gets an attacker's script to run on the victim site, where it can read tokens and cookies; it's defended by escaping or sanitizing external data, a Content Security Policy and HttpOnly cookies.
> @short 75
> Describe how JWT authentication works in a Spring API.
> ~ login, generate, signature, Bearer, filter, validate, stateless
> After a successful login, the server generates a signed JWT containing claims and an expiry and returns it. The client sends it in the Authorization: Bearer header with each request. A JwtFilter validates the signature and expiry and sets the user's authentication before the controller runs. No session is stored, so it is stateless.
