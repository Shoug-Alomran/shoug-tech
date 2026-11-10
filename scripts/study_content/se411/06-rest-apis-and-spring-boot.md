@head Chapter 6
@title REST APIs and Spring Boot
@sources chapter-6-rest-apis-and-spring-boot
@count 96
@tldr A REST API lets clients manage resources over HTTP: POST creates, GET reads, PUT updates, DELETE removes, each with a standard status code. Spring Boot builds one with a few annotations and a repository interface it implements for you.
@why Exams here ask for the CRUD table (method, URI, status code), the six REST principles, which methods are idempotent, the error codes 400/401/403/404/500, and a handler method to fill in. The handler code below follows the slides line by line.
@connect Chapter 3's Maven brings in Spring with one dependency. Chapter 4's "program to an interface" is exactly how CrudRepository works, and records are Chapter 4's immutable classes in one line. Chapter 7 secures this same API.
@goals
- Explain Spring, Spring Boot, IoC and dependency injection
- Define an API contract and read JSON
- Map CRUD to HTTP methods, URIs and status codes
- State the six REST principles and the REST best practices
- Explain idempotency and which methods have it
- Write Spring controller handlers with @GetMapping, @PostMapping, @PutMapping, @DeleteMapping
- Use records, CrudRepository, pagination, and hard vs soft delete
@vocab
API contract | A formal agreement on how a provider and consumer interact.
Resource | A thing the API manages, such as a Product, represented in JSON.
Endpoint | A URI that receives requests, such as /v1/products/52.
IoC | Inversion of Control: the framework calls your code.
Dependency injection | An object receives its dependencies instead of creating them.
Bean | An object Spring creates and stores in its IoC container.
Idempotent | Doing it once or many times has the same effect.
Soft delete | Marking a record as deleted instead of removing it.
@map
3-9 | Spring, Spring Boot, IoC | MEMORIZE | DI vs new
10-16 | API contracts and JSON | MEMORIZE | Contract definition
17-20 | REST, CRUD, HTTP | MEMORIZE | The CRUD table
21-27 | Six REST principles | MEMORIZE | ACCLUC
28-35 | Best practices, idempotency | MEMORIZE | Status codes
36-49 | Spring annotations, controllers | WRITE | GET handler
50-60 | Records, repositories, databases | MEMORIZE | CrudRepository
61-76 | POST and pagination | WRITE | 201 + Location
77-87 | PUT, DELETE, soft delete, audit | WRITE | 204 / 404
88-95 | Switching to MySQL | SKIM | Dependency and properties

## Spring, Spring Boot and Inversion of Control | Slides 3-9 | must
**Spring** is a giant toolbox of modules: Spring MVC (web apps), Spring Data (databases), Spring Security (authentication, authorization, protection) and more. **Spring Boot** is an **opinionated** version with sensible preconfigured settings and an **embedded server** (Tomcat), so you can start quickly without setting everything up.

**Inversion of Control (IoC)**: instead of your code calling a library, **the framework calls your code** at the right time. Two common forms:

| Form | Example |
|---|---|
| **Dependency injection** (most common) | An object is *given* its dependencies by a container instead of creating them with `new` |
| Event-driven callbacks | A web framework calls your handler when a request arrives |

::code java
public interface GreetingService { String greet(); }
public class HelloService implements GreetingService { public String greet() { return "Hello"; } }
public class SelemService implements GreetingService { public String greet() { return "Selem"; } }

public class Greeter {
    private final GreetingService service;
    public Greeter(GreetingService service) { this.service = service; }   // injected
    public void run() { System.out.println(service.greet()); }
}
::

Greeter never says `new HelloService()`, so you can swap in SelemService (or a test fake) without touching Greeter. Spring's IoC container does this injection for you, which also lets you use one database in development and another in production.

::analogy A restaurant kitchen
Without IoC, the chef goes shopping for ingredients. With dependency injection, a supplier delivers whatever the menu needs, and the chef just cooks. Change supplier, and the chef doesn't change.
::

**Spring Initializr** (start.spring.io) generates a project. Adding **Spring Web** gives REST support, controllers, Spring MVC and embedded Tomcat.

::key
- Spring is a modular framework; Spring Boot is preconfigured, opinionated Spring
- Spring Boot has an embedded server
- IoC: the framework calls your code
- Dependency injection: objects receive dependencies instead of using new
- Spring Initializr creates a project with chosen dependencies
::

## API contracts, JSON and REST | Slides 10-20 | must
An **API contract** is a formal agreement between a provider and a consumer about how to interact: what data to send, what comes back, and how success and failure are reported. The two sides **don't need the same programming language**, only the same contract.

**JSON** (JavaScript Object Notation) represents objects as readable text. Compared with XML it is quicker to read and write, easier to use, and smaller.

::code json
{
  "name": "France",
  "capital": "Paris",
  "population": 67364357,
  "languages": ["French"]
}
::

**REST** (Representational State Transfer): data objects (resources) have **representations**, such as JSON. "State" means the resource's values. A REST API manages the state of resources. **HTTP** carries it: a **request** has a method, a URI and a body; a **response** has a status code and a body.

| Operation | Endpoint | Method | Success status |
|---|---|---|---|
| **Create** | `/v1/products` | **POST** | **201 CREATED** |
| **Read** | `/v1/products/{id}` | **GET** | **200 OK** |
| **Update** | `/v1/products/{id}` | **PUT** | **204 NO CONTENT** |
| **Delete** | `/v1/products/{id}` | **DELETE** | **204 NO CONTENT** |

Create has **no ID** in the URI, because the server assigns the new ID. Create and update send a **request body**.

::mnemonic Post-Get-Put-Delete = "Please Give People Directions"
Create **P**OST, Read **G**ET, Update **P**UT, Delete **D**ELETE, the CRUD order.
::
::trap 200 vs 201 vs 204
GET returns **200** with the resource. POST returns **201** with a Location header. PUT and DELETE return **204** with an **empty body**, because the client already knows what it sent.
::
::key
- An API contract defines how provider and consumer interact
- JSON is the usual representation, lighter than XML
- POST /v1/products → 201; GET /{id} → 200; PUT /{id} → 204; DELETE /{id} → 204
- Create has no ID in the URI; the server assigns it
::

## REST principles and best practices | Slides 21-35, 61-62 | must
### Six principles
| Principle | Meaning |
|---|---|
| **Uniform interface** | Each resource has one unique URI; requests for it look the same wherever they come from |
| **Client-server decoupling** | Client and server are independent; the client only knows the URI |
| **Statelessness** | Each request carries everything needed; no server-side sessions (except authentication) |
| **Cacheability** | Responses say whether they may be cached, improving client speed and server scalability |
| **Layered system** | There may be intermediaries; neither side can tell whether it talks directly to the other |
| **Code on demand** (optional) | Responses may sometimes include executable code |

::mnemonic Use Clean Stateless Caches, Layered Code
**U**niform, **C**lient-server, **S**tateless, **C**acheable, **L**ayered, **C**ode on demand.
::

### Best practices
| Practice | Example |
|---|---|
| Accept and respond with JSON | Except when sending files |
| **Nouns, not verbs**, in paths | `GET /articles`, not `GET /getArticles`; the HTTP method is the verb |
| Logical nesting | `/articles/:articleId/comments` |
| Standard error codes | See below |
| Filtering, sorting, pagination | Don't return a huge table at once |
| **Versioning** | `/v1/...` stays for old clients while `/v2/...` adds changes |

| Code | Meaning |
|---|---|
| **400** Bad Request | Client input fails validation |
| **401** Unauthorized | **Not authenticated** (not logged in) |
| **403** Forbidden | Authenticated, but **not allowed** |
| **404** Not Found | Resource doesn't exist |
| **500** Internal Server Error | Generic server error |
| 502 Bad Gateway | Invalid response from an upstream server |
| 503 Service Unavailable | Overloaded or partly down |

::trap 401 vs 403
**401**: "Who are you?", meaning log in first. **403**: "I know who you are, and the answer is no."
::

### Idempotency
A request is **idempotent** if doing it **once or many times has the same effect** on the server. Clients retry after timeouts and network errors, so duplicates must not break the system. Idempotent requests can also be **cached** (for example in Redis).

| Idempotent | Not idempotent |
|---|---|
| **GET, PUT, DELETE** | **POST** (each call creates another resource), **PATCH** (such as "increment by 1") |

::analogy Elevator button vs vending machine
Pressing the elevator button five times still calls one elevator: idempotent (PUT "set price to 50"). Pressing a vending-machine button five times buys five drinks: not idempotent (POST).
::
::key
- Six principles: uniform, client-server, stateless, cacheable, layered, code on demand
- Use nouns in paths; the HTTP method is the verb
- 400 bad input, 401 not authenticated, 403 not allowed, 404 missing, 500 server error
- Version APIs as /v1, /v2
- GET, PUT and DELETE are idempotent; POST and PATCH are not
::

## Spring controllers and handlers | Slides 36-49 | must
Spring creates objects called **beans** and stores them in its **IoC container**. Annotating a class makes Spring create it during the **component scan** at startup and inject it wherever needed.

| Annotation | Role |
|---|---|
| `@SpringBootApplication` | Main class: configuration, auto-configuration and component scan |
| `@RestController` | A class that handles HTTP requests and returns data (JSON) |
| `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping` | Route one HTTP method and path to a handler method |
| `@RequestMapping` | Base path for the whole controller |
| `@PathVariable` | Takes a value from the URI, such as `{requestedId}` |
| `@RequestBody` | Converts the JSON body into a Java object |
| `@RequestParam` | Reads a query parameter, such as `?page=1` |

::code java
@RestController
@RequestMapping("/v1/products")
class ProductController {
    private final ProductRepository productRepository;
    ProductController(ProductRepository repo) { this.productRepository = repo; }  // injected

    @GetMapping("/{requestedId}")
    private ResponseEntity<Product> findById(@PathVariable Integer requestedId) {
        Optional<Product> product = productRepository.findById(requestedId);
        if (product.isPresent()) return ResponseEntity.ok(product.get());   // 200
        else return ResponseEntity.notFound().build();                      // 404
    }
}
::

`{requestedId}` in the path matches the parameter name, so Spring fills it in. **ResponseEntity** represents the whole HTTP response: status code, headers and body.

**MVC plus a service layer**: keep controllers **thin**. The controller handles HTTP; a **service** (an interface such as IUserService plus an implementation) holds business logic such as validation and calculations; a **repository** handles data. The service is injected into the controller's constructor.

::key
- Beans are objects Spring creates and injects from the IoC container
- @RestController plus @GetMapping and friends route requests to methods
- @PathVariable reads the URI; @RequestBody reads the JSON body
- ResponseEntity holds status, headers and body
- Keep controllers thin; business logic goes in a service layer
::

## Records, repositories and databases | Slides 50-60, 88-95 | must
A **record** (Java 14) creates an immutable data class in one line:

::code java
public record Product(Integer id, String name, String description, Double price) { }
::

It generates the constructor, accessors (`name()`, not `getName()`), `equals`, `hashCode` and `toString`. Records are **immutable by design** and suit **DTOs** (data transfer objects).

**Spring Data** follows **separation of concerns** (presentation, business and data layers).

::code java
interface ProductRepository extends CrudRepository<Product, Integer> { }
::

That's the whole repository. You get `findById`, `findAll`, `save`, `delete` and more. **Where's the implementation?** CrudRepository is only an interface; Spring Data generates the implementation at IoC container startup and injects it.

| Database type | Example | Notes |
|---|---|---|
| **Embedded, in-memory** | H2 | A Java library dependency; data lives in memory only, ideal for testing |
| **Persistent** | MySQL, SQL Server | Durable; accessed with JDBC and SQL |

Dependencies: `spring-boot-starter-data-jdbc` plus `h2`. Put the table definition in `schema.sql` and mock data in `data.sql` in the resources folder, and Spring runs them at startup. Switching to **MySQL** means three changes: adjust the SQL dialect (such as `auto_increment`), swap the H2 dependency for the MySQL connector, and add connection settings (`spring.datasource.url`, username, password) to `application.properties`.

::trap Credentials in properties files
The slides put a database password in application.properties to keep the demo simple. In a real project that is a leaked secret (Chapter 1: never commit secrets; Chapter 7). Use environment variables or a secrets store.
::
::key
- A record is an immutable data class with generated methods
- Extending CrudRepository<Product, Integer> gives full CRUD
- Spring Data implements the repository interface at startup
- H2 is in-memory for testing; MySQL is persistent
- schema.sql defines tables; data.sql loads mock data
::

## Implementing POST and pagination | Slides 61-76 | must
Before writing POST, answer: **who sets the ID?** (usually the database; sometimes the controller when objects already have one, such as 966 for KSA), **which method?** (POST), and **what response?** (**201 CREATED** plus a **Location** header pointing at the new resource, as HTTP requires).

::code java
@PostMapping
public ResponseEntity<Void> createProduct(@RequestBody Product newProductRequest,
                                          UriComponentsBuilder ucb) {
    try {
        Product newProduct = productRepository.save(newProductRequest);
        URI location = ucb.path("/v1/products/{id}")
                          .buildAndExpand(newProduct.id()).toUri();
        return ResponseEntity.created(location).build();       // 201 + Location
    } catch (Exception ex) {
        return ResponseEntity.internalServerError().build();   // 500
    }
}
::

`save()` returns the saved object **with its new ID**. If the client sends an ID that doesn't exist, `save` tries to **update** it and throws IncorrectUpdateSemanticsDataAccessException, which is why the slides wrap it in try/catch.

### Pagination and sorting
An API must never return an unlimited response. Extend **PagingAndSortingRepository** and accept a `Pageable`:

| URI | Meaning |
|---|---|
| `/v1/products?page=1` | Second page (indexing starts at **0**) |
| `?page=1&size=10` | 10 items per page |
| `?page=1&size=10&sort=price,desc` | Sorted by price, descending |

::code java
@GetMapping
public ResponseEntity<List<Product>> findAll(Pageable pageable) {
    if (pageable.getPageSize() > 100) return ResponseEntity.badRequest().build();   // limit size
    Page<Product> page = productRepository.findAll(PageRequest.of(
        pageable.getPageNumber(), pageable.getPageSize(),
        pageable.getSortOr(Sort.by(Sort.Direction.ASC, "price"))));
    return ResponseEntity.ok(page.getContent());
}
::

The default page size is 20.

::check A client requests `?page=0&size=5&sort=price,desc`. What do they get?
The first 5 products, most expensive first.
::
::key
- POST returns 201 CREATED with a Location header
- save() returns the object with its generated ID
- Pages are numbered from 0; size and sort are query parameters
- Limit page size to protect the server
::

## Implementing PUT and DELETE | Slides 77-87 | must
**PUT** (whole update) or **PATCH** (partial, such as incrementing a value) uses the same URI as create **plus the ID**, with a JSON body.

| Outcome | Status |
|---|---|
| Updated | **204 NO CONTENT**, empty body |
| ID doesn't exist | **404 NOT FOUND** |
| Server error | **500** |

::code java
@PutMapping("/{requestedId}")
public ResponseEntity<Void> updateProduct(@PathVariable Integer requestedId,
                                          @RequestBody Product productUpdate) {
    Optional<Product> product = productRepository.findById(requestedId);
    if (product.isPresent()) {
        Product updated = new Product(product.get().id(), productUpdate.name(),
                                      productUpdate.description(), productUpdate.price());
        productRepository.save(updated);
        return ResponseEntity.noContent().build();     // 204
    }
    return ResponseEntity.notFound().build();          // 404
}
::

A new Product object is built because records are immutable. **DELETE** has the same shape: find by ID; if present, `delete` and return 204; otherwise 404.

| | Hard delete | Soft delete |
|---|---|---|
| How | Remove the row | Set an `IS_DELETED` flag or `DELETED_DATE` column |
| Recover later? | No, gone forever | Yes |
| Repository changes | None | Must exclude deleted rows from reads |

**Audit trail and archiving**: keep a record of changes (who deleted what and when) for customer service and data-retention regulations. **Audit fields** on a record capture only the latest operation; an **audit trail** records every event.

::key
- PUT replaces, PATCH updates part; both use /{id}
- Update and delete return 204, or 404 for a missing ID
- Records are immutable, so build a new object to update
- Soft delete marks rows deleted so data can be recovered
- An audit trail records every change; audit fields only the latest
::
@cheat
### Spring
- Spring Boot: opinionated, embedded Tomcat
- IoC: framework calls your code
- DI: dependencies given, not new
- Bean: object in IoC container
### CRUD
- POST /v1/products → 201 + Location
- GET /{id} → 200 (404 if missing)
- PUT /{id} → 204
- DELETE /{id} → 204
### REST principles
- Uniform interface, client-server
- Stateless, cacheable
- Layered, code on demand
- Nouns in paths, versioning, pagination
### Codes
- 400 bad input
- 401 not authenticated
- 403 not allowed
- 404 not found, 500 server
- Idempotent: GET, PUT, DELETE
### Annotations
- @RestController, @RequestMapping
- @Get/Post/Put/DeleteMapping
- @PathVariable, @RequestBody, @RequestParam
- ResponseEntity
### Data
- record = immutable data class
- extends CrudRepository<Product, Integer>
- PagingAndSortingRepository, page from 0
- H2 in-memory; MySQL persistent
- Soft delete; audit trail
@mcq 6
Inversion of Control means:
+ The framework calls your code instead of your code calling the library
- Your code calls every library routine directly
- Objects create all their dependencies with new
- The client controls the server
> Slide 6.
@mcq 6
With dependency injection, an object:
+ Receives its dependencies from an external container
- Creates its dependencies itself
- Has no dependencies
- Must extend Thread
> Slide 6.
@mcq 18
The correct endpoint and method to create a product is:
+ POST /v1/products
- POST /v1/products/52
- GET /v1/products/create
- PUT /v1/products
> No ID: the server assigns it.
@mcq 18
A successful PUT update should return:
+ 204 NO CONTENT
- 201 CREATED
- 200 with the full list
- 404 NOT FOUND
> Slide 78.
@mcq 63
A successful POST that creates a resource should return:
+ 201 CREATED with a Location header
- 200 OK with no body
- 204 NO CONTENT
- 302 FOUND
> Slides 63-66.
@mcq 24
"Each request must include all the information needed to process it" describes:
+ Statelessness
- Cacheability
- Layered system
- Code on demand
> Slide 24.
@mcq 29
Which endpoint follows REST best practice?
+ GET /articles
- GET /getArticles
- POST /createArticle
- GET /articles/delete/5
> Use nouns; the method is the verb.
@mcq 31
A logged-in user tries to open an admin-only resource. The correct code is:
+ 403 Forbidden
- 401 Unauthorized
- 404 Not Found
- 400 Bad Request
> Authenticated but not allowed.
@mcq 62
Which HTTP method is NOT idempotent?
+ POST
- GET
- PUT
- DELETE
> Each POST creates a new resource.
@mcq 47
In `findById(@PathVariable Integer requestedId)` mapped to "/{requestedId}", the annotation:
+ Takes the value from the URI path
- Reads the JSON body
- Reads a query parameter
- Sets the status code
> Slide 47.
@mcq 57
`interface ProductRepository extends CrudRepository<Product, Integer> {}`. Where is findById implemented?
+ Spring Data generates the implementation at startup
- You must write it in the interface
- In the Product record
- It isn't available
> Slide 57.
@mcq 52
A Java record automatically provides:
+ A constructor, accessors, equals, hashCode and toString
- Setters for every field
- A database table
- A REST controller
> And it is immutable.
@mcq 74
`/v1/products?page=1&size=10` returns:
+ The second page of 10 products
- The first page of 10 products
- Product number 1
- 10 pages
> Page indexing starts at 0.
@mcq 84
Marking a record with an IS_DELETED flag instead of removing it is:
+ Soft delete
- Hard delete
- An audit field
- Pagination
> Slide 84.
@short 18
Give the HTTP method, endpoint and success status code for each CRUD operation on products.
~ POST 201, GET 200, PUT 204, DELETE 204, /v1/products/{id}
> Create: POST /v1/products, 201 CREATED. Read: GET /v1/products/{id}, 200 OK. Update: PUT /v1/products/{id}, 204 NO CONTENT. Delete: DELETE /v1/products/{id}, 204 NO CONTENT.
@short 34
Define idempotency and explain why it matters for REST APIs.
~ same effect, duplicate requests, retry, cache, GET PUT DELETE
> A request is idempotent if executing it once or many times has the same effect on the server. Clients may send duplicates after timeouts or network errors, so idempotent operations keep the system stable, and their results can be cached. GET, PUT and DELETE are idempotent; POST and PATCH are not.
@short 46
Write a GET handler that returns a product by ID, or 404 if it doesn't exist.
~ @GetMapping, @PathVariable, findById, Optional, ResponseEntity.ok, notFound
> @GetMapping("/{requestedId}") ResponseEntity<Product> findById(@PathVariable Integer requestedId) { Optional<Product> p = productRepository.findById(requestedId); if (p.isPresent()) return ResponseEntity.ok(p.get()); return ResponseEntity.notFound().build(); }
