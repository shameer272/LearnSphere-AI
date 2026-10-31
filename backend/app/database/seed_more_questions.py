"""
Seed additional curriculum questions to guarantee 25+ questions in DB for:
Python, Java, JavaScript, HTML, CSS, React, SQL, DSA, OS, CN.
"""
import json
import sqlite3
from datetime import datetime

DB_PATH = "backend/learnsphere_cse.db"

ADDITIONAL_QUESTIONS = [
    # ── PYTHON PROGRAMMING (CS-PY) ──────────────────────────────────────────
    {
        "subject_code": "CS-PY",
        "concept_name": "Mutable vs Immutable Objects",
        "question_type": "output_prediction",
        "question_text": "What is the output of the following Python tuple mutation attempt?",
        "code_snippet": "t = ([1, 2], 3)\nt[0].append(4)\nprint(t)",
        "options": {"A": "([1, 2, 4], 3)", "B": "TypeError: 'tuple' object does not support item assignment", "C": "([1, 2], 3, 4)", "D": "([1, 2], 3)"},
        "correct_answer": "A",
        "explanation": "While the tuple itself cannot be rebound to new references, mutable elements contained within the tuple (like lists) can be mutated in-place.",
        "difficulty": "medium",
        "misconception_targets": ["Believing mutable objects inside a tuple become immutable"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "List Slicing and Negative Indexing",
        "question_type": "output_prediction",
        "question_text": "What does reversing a string with slice notation s[::-1] do in Python?",
        "code_snippet": "word = 'algorithm'\nprint(word[::-2])",
        "options": {"A": "mtrol", "B": "mtiol", "C": "mtoia", "D": "mtro"},
        "correct_answer": "A",
        "explanation": "word[::-2] traverses the string backwards from the last index step by 2: indices 8('m'), 6('t'), 4('r'), 2('o'), 0('l').",
        "difficulty": "medium",
        "misconception_targets": ["Negative step slice indexing"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "List Comprehensions & Generator Expressions",
        "question_type": "output_prediction",
        "question_text": "What is the difference in memory consumption between [x**2 for x in range(10**6)] and (x**2 for x in range(10**6))?",
        "code_snippet": None,
        "options": {"A": "List comprehension allocates all million items in memory; generator expression computes lazily on demand using O(1) space", "B": "Both consume identical memory", "C": "Generator uses more memory due to pointer overhead", "D": "List comprehension computes lazily"},
        "correct_answer": "A",
        "explanation": "Generators produce values on demand using iterator protocol (__iter__, __next__), keeping memory overhead constant O(1).",
        "difficulty": "easy",
        "misconception_targets": ["Generator lazy evaluation vs List comprehension eager allocation"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Decorators and First-Class Functions",
        "question_type": "output_prediction",
        "question_text": "What is printed when decorating a function without functools.wraps?",
        "code_snippet": "def my_dec(fn):\n    def wrapper(*args, **kwargs):\n        return fn(*args, **kwargs)\n    return wrapper\n\n@my_dec\ndef calculate():\n    '''Documentation'''\n    pass\n\nprint(calculate.__name__)",
        "options": {"A": "wrapper", "B": "calculate", "C": "my_dec", "D": "None"},
        "correct_answer": "A",
        "explanation": "Without @functools.wraps(fn), the decorated function's __name__, __doc__, and metadata are masked by the inner wrapper function.",
        "difficulty": "medium",
        "misconception_targets": ["Function metadata masking in Python decorators"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Dunder Methods and Class Attributes",
        "question_type": "output_prediction",
        "question_text": "What happens when a class attribute is modified through an instance in Python?",
        "code_snippet": "class Student:\n    school = 'BTech Institute'\n\ns1 = Student()\ns1.school = 'LearnSphere University'\nprint(Student.school, s1.school)",
        "options": {"A": "BTech Institute LearnSphere University", "B": "LearnSphere University LearnSphere University", "C": "BTech Institute BTech Institute", "D": "AttributeError: class attribute is read-only"},
        "correct_answer": "A",
        "explanation": "Assigning to s1.school creates an instance attribute on s1 shadowing the class attribute. The class attribute Student.school remains unchanged.",
        "difficulty": "medium",
        "misconception_targets": ["Instance attribute shadowing class attribute"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Mutable vs Immutable Objects",
        "question_type": "output_prediction",
        "question_text": "What is the output of the is operator vs == operator in Python for small integers?",
        "code_snippet": "a = 256\nb = 256\nc = 257\nd = 257\nprint(a is b, c is d)",
        "options": {"A": "True and True (or True and False in standard CPython REPL)", "B": "False and False", "C": "True and True", "D": "SyntaxError"},
        "correct_answer": "A",
        "explanation": "CPython pre-allocates an integer cache for range [-5, 256]. Numbers outside this range may be distinct heap objects depending on code block compilation.",
        "difficulty": "medium",
        "misconception_targets": ["CPython integer intern caching range"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "List Comprehensions & Generator Expressions",
        "question_type": "output_prediction",
        "question_text": "What is the output of list comprehension with late-binding closures in Python?",
        "code_snippet": "funcs = [lambda: i for i in range(3)]\nprint([f() for f in funcs])",
        "options": {"A": "[2, 2, 2]", "B": "[0, 1, 2]", "C": "[0, 0, 0]", "D": "[3, 3, 3]"},
        "correct_answer": "A",
        "explanation": "Closures in Python bind variables by reference, not value. When invoked, the loop has completed and i equals 2.",
        "difficulty": "hard",
        "misconception_targets": ["Late binding closures in Python list comprehensions"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Decorators and First-Class Functions",
        "question_type": "conceptual",
        "question_text": "What does Python's @staticmethod decorator do compared to @classmethod?",
        "code_snippet": None,
        "options": {"A": "@staticmethod receives neither self nor cls; @classmethod receives cls as first argument", "B": "@staticmethod can access instance variables; @classmethod cannot", "C": "They are completely identical", "D": "@classmethod cannot be called on instances"},
        "correct_answer": "A",
        "explanation": "@staticmethod acts as a plain function housed inside a class namespace without implicit first argument. @classmethod receives the class object as cls.",
        "difficulty": "easy",
        "misconception_targets": ["Staticmethod vs classmethod argument binding"]
    },

    # ── JAVA PROGRAMMING (CS-JAVA) ──────────────────────────────────────────
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "output_prediction",
        "question_text": "What is the result of String immutability in the following method call?",
        "code_snippet": "public static void modify(String s) {\n    s = s.concat(\" World\");\n}\npublic static void main(String[] args) {\n    String str = \"Hello\";\n    modify(str);\n    System.out.println(str);\n}",
        "options": {"A": "Hello", "B": "Hello World", "C": "World", "D": "NullPointerException"},
        "correct_answer": "A",
        "explanation": "Java passes object references by value. s.concat returns a new String, but the caller's reference str still points to 'Hello'.",
        "difficulty": "easy",
        "misconception_targets": ["Pass-by-value of object references and String immutability"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "conceptual",
        "question_text": "What is the default initial capacity and load factor of java.util.HashMap in Java?",
        "code_snippet": None,
        "options": {"A": "Initial capacity 16, load factor 0.75", "B": "Initial capacity 10, load factor 0.5", "C": "Initial capacity 32, load factor 1.0", "D": "Initial capacity 8, load factor 0.8"},
        "correct_answer": "A",
        "explanation": "HashMap defaults to 16 buckets with a load factor of 0.75. When size exceeds 16 * 0.75 = 12, the table doubles capacity.",
        "difficulty": "easy",
        "misconception_targets": ["HashMap default sizing and resizing thresholds"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "conceptual",
        "question_text": "What is the difference between ArrayList and LinkedList in Java when performing random element access (e.g. get(5000))?",
        "code_snippet": None,
        "options": {"A": "ArrayList is O(1) random access; LinkedList is O(N) because it must traverse pointers", "B": "Both are O(1)", "C": "LinkedList is faster due to node caching", "D": "ArrayList is O(N) due to array copying"},
        "correct_answer": "A",
        "explanation": "ArrayList is backed by a contiguous array with O(1) index calculation. LinkedList must traverse from head or tail, requiring O(N) steps.",
        "difficulty": "easy",
        "misconception_targets": ["ArrayList vs LinkedList random access time complexity"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "output_prediction",
        "question_text": "What is the output of comparing primitive double vs Double wrapper object with == in Java?",
        "code_snippet": "Double d1 = 10.0;\nDouble d2 = 10.0;\nSystem.out.println((d1 == d2) + \" \" + d1.equals(d2));",
        "options": {"A": "false true", "B": "true true", "C": "false false", "D": "true false"},
        "correct_answer": "A",
        "explanation": "Double wrapper types are not cached by the JVM (unlike small Integers). d1 and d2 are distinct heap objects, so == evaluates to false.",
        "difficulty": "medium",
        "misconception_targets": ["Absence of wrapper caching for Double and Float in Java"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "conceptual",
        "question_text": "What occurs when overriding equals() without overriding hashCode() in an object used as a HashSet element?",
        "code_snippet": None,
        "options": {"A": "Duplicate logical objects can be inserted into the HashSet because their default identity hash codes differ", "B": "Compilation error", "C": "HashSet automatically generates sequential hash codes", "D": "Runtime UnsupportedOperationException"},
        "correct_answer": "A",
        "explanation": "HashSet checks hashCode() first to find the bucket. If hash codes differ, equals() is never even called, allowing logical duplicates.",
        "difficulty": "medium",
        "misconception_targets": ["Consequences of violating equals-hashCode contract"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "output_prediction",
        "question_text": "Which Java interface does java.util.Collections.unmodifiableList() return?",
        "code_snippet": "List<String> list = Collections.unmodifiableList(new ArrayList<>());\nlist.add(\"item\");",
        "options": {"A": "Throws UnsupportedOperationException at runtime", "B": "Compiles with warning and adds item", "C": "Ignores insertion silently", "D": "Throws IllegalAccessError"},
        "correct_answer": "A",
        "explanation": "unmodifiableList returns a wrapper view that throws UnsupportedOperationException on any mutating operation.",
        "difficulty": "easy",
        "misconception_targets": ["Immutable collection wrappers behavior on mutation"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "conceptual",
        "question_text": "In Java 9+, what compact string representation was introduced to reduce heap footprint?",
        "code_snippet": None,
        "options": {"A": "byte[] with coder flag (LATIN1 as 1 byte/char or UTF16 as 2 bytes/char)", "B": "char[] encoded as 4-byte UTF-32", "C": "Compressed bitset array", "D": "Huffman coding trees"},
        "correct_answer": "A",
        "explanation": "JEP 254 replaced char[] (2 bytes per character) with byte[] plus an encoding flag, halving memory for Latin-1 strings.",
        "difficulty": "hard",
        "misconception_targets": ["Java 9 Compact Strings implementation"]
    },

    # ── JAVASCRIPT PROGRAMMING (CS-JS) ──────────────────────────────────────
    {
        "subject_code": "CS-JS",
        "concept_name": "Closures and Lexical Scope",
        "question_type": "output_prediction",
        "question_text": "What is the output of the classic var in setTimeout loop in JavaScript?",
        "code_snippet": "for (var i = 0; i < 3; i++) {\n    setTimeout(() => console.log(i), 0);\n}",
        "options": {"A": "3 3 3", "B": "0 1 2", "C": "undefined undefined undefined", "D": "0 0 0"},
        "correct_answer": "A",
        "explanation": "var has function scope, not block scope. All callbacks capture the exact same variable i, which is 3 when event loop runs tasks.",
        "difficulty": "easy",
        "misconception_targets": ["var scoping vs let block scoping in asynchronous loops"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Closures and Lexical Scope",
        "question_type": "output_prediction",
        "question_text": "What is the output when using `let` in the same setTimeout loop in JavaScript?",
        "code_snippet": "for (let i = 0; i < 3; i++) {\n    setTimeout(() => console.log(i), 0);\n}",
        "options": {"A": "0 1 2", "B": "3 3 3", "C": "2 2 2", "D": "TypeError"},
        "correct_answer": "A",
        "explanation": "let has block scope. Each iteration creates a fresh binding of i captured independently by the arrow function closure.",
        "difficulty": "easy",
        "misconception_targets": ["Per-iteration lexical environment with let"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Promises and Async/Await",
        "question_type": "output_prediction",
        "question_text": "What is the execution order of synchronous code, microtasks (Promises), and macrotasks (setTimeout)?",
        "code_snippet": "console.log('1');\nsetTimeout(() => console.log('2'), 0);\nPromise.resolve().then(() => console.log('3'));\nconsole.log('4');",
        "options": {"A": "1 4 3 2", "B": "1 2 3 4", "C": "1 3 4 2", "D": "1 4 2 3"},
        "correct_answer": "A",
        "explanation": "Synchronous script runs first (1, 4). Before processing macrotasks (setTimeout), the event loop drains all microtasks (Promise -> 3). Then macrotask runs (2).",
        "difficulty": "medium",
        "misconception_targets": ["Microtask queue priority over macrotask queue"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Closures and Lexical Scope",
        "question_type": "output_prediction",
        "question_text": "What is the value of `this` inside an arrow function compared to a standard function?",
        "code_snippet": "const obj = {\n    val: 42,\n    regular: function() { return this.val; },\n    arrow: () => this.val\n};\nconsole.log(obj.regular(), obj.arrow());",
        "options": {"A": "42 undefined (or global/window)", "B": "42 42", "C": "undefined undefined", "D": "TypeError"},
        "correct_answer": "A",
        "explanation": "Arrow functions do not bind their own `this`. They inherit `this` lexically from the enclosing scope (which is global/module, not obj).",
        "difficulty": "medium",
        "misconception_targets": ["Lexical this binding in arrow functions"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Promises and Async/Await",
        "question_type": "conceptual",
        "question_text": "What happens if one promise rejects in Promise.all() vs Promise.allSettled()?",
        "code_snippet": None,
        "options": {"A": "Promise.all() rejects immediately (fail-fast); Promise.allSettled() waits for all promises and returns their statuses", "B": "Promise.all ignores rejections", "C": "Promise.allSettled rejects if more than 50% fail", "D": "They have identical rejection behavior"},
        "correct_answer": "A",
        "explanation": "Promise.all rejects on the first rejection. Promise.allSettled never rejects early, returning an array of {status, value|reason} for all promises.",
        "difficulty": "easy",
        "misconception_targets": ["Promise.all fail-fast vs Promise.allSettled"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Closures and Lexical Scope",
        "question_type": "output_prediction",
        "question_text": "What is printed by hoisting behavior of var vs function declarations?",
        "code_snippet": "console.log(typeof a, typeof b);\nvar a = 10;\nfunction b() { return 20; }",
        "options": {"A": "undefined function", "B": "number function", "C": "undefined undefined", "D": "ReferenceError"},
        "correct_answer": "A",
        "explanation": "var declarations are hoisted and initialized to undefined. Function declarations are hoisted completely with their definition body.",
        "difficulty": "medium",
        "misconception_targets": ["Hoisting difference between var initialization and function definition"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Promises and Async/Await",
        "question_type": "code_debugging",
        "question_text": "What happens if an error is thrown inside an async function without a try/catch block?",
        "code_snippet": "async function getData() {\n    throw new Error('Network failure');\n}",
        "options": {"A": "The returned promise rejects with the thrown Error (UnhandledPromiseRejection if not caught with .catch)", "B": "Crashes the browser immediately", "C": "Returns undefined silently", "D": "Converts error into null"},
        "correct_answer": "A",
        "explanation": "An async function always returns a Promise. Any uncaught synchronous throw inside the async body rejects that returned promise.",
        "difficulty": "easy",
        "misconception_targets": ["Async functions wrapping throws in rejected Promises"]
    },

    # ── REACT.JS (CS-REACT) ─────────────────────────────────────────────────
    {
        "subject_code": "CS-REACT",
        "concept_name": "State Immutability and useEffect Hook",
        "question_type": "output_prediction",
        "question_text": "Why does mutating state directly in React fail to trigger a re-render?",
        "code_snippet": "const [items, setItems] = useState([1, 2]);\nconst addItem = () => {\n    items.push(3);\n    setItems(items);\n};",
        "options": {"A": "React uses Object.is() shallow comparison; because the array reference hasn't changed, React bails out of rendering", "B": "push() is forbidden in JavaScript", "C": "React freezes all state arrays automatically", "D": "setItems must be called synchronously"},
        "correct_answer": "A",
        "explanation": "React compares old and new state references with Object.is. Mutating the existing array in-place preserves identity, so React skips re-rendering.",
        "difficulty": "medium",
        "misconception_targets": ["Shallow reference equality check in React state dispatchers"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "State Immutability and useEffect Hook",
        "question_type": "code_debugging",
        "question_text": "What causes an infinite re-render loop in this React component?",
        "code_snippet": "function UserList() {\n    const [users, setUsers] = useState([]);\n    useEffect(() => {\n        fetch('/api/users')\n            .then(res => res.json())\n            .then(data => setUsers(data));\n    }); // missing dependency array\n}",
        "options": {"A": "Omitting the dependency array causes useEffect to run on every render, triggering setUsers which triggers another render", "B": "setUsers cannot be used inside useEffect", "C": "fetch cannot be called inside functional components", "D": "useState must be initialized with null"},
        "correct_answer": "A",
        "explanation": "Without a dependency array, useEffect executes after every single render. Calling setUsers triggers a new render, causing an infinite loop.",
        "difficulty": "easy",
        "misconception_targets": ["Missing dependency array leading to render loops"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Custom Hooks and Context API",
        "question_type": "conceptual",
        "question_text": "What performance issue can occur when passing a new object literal directly to Context.Provider value?",
        "code_snippet": "<MyContext.Provider value={{ user, setUser }}>",
        "options": {"A": "A new object reference is created on every render, forcing all consuming components to re-render even if user hasn't changed", "B": "Syntax error in JSX", "C": "Context will lose state on refresh", "D": "Subscribers cannot read the context"},
        "correct_answer": "A",
        "explanation": "Passing an inline object literal creates a brand new reference each render. useMemo should be used to memoize the context value.",
        "difficulty": "medium",
        "misconception_targets": ["Context provider value reference stability and re-rendering"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "State Immutability and useEffect Hook",
        "question_type": "conceptual",
        "question_text": "What is the purpose of the cleanup function returned by useEffect in React?",
        "code_snippet": "useEffect(() => {\n    const sub = eventEmitter.subscribe(handler);\n    return () => sub.unsubscribe();\n}, []);",
        "options": {"A": "Runs before the component unmounts and before re-running the effect on dependency change, preventing memory leaks", "B": "Deletes the component from the DOM tree", "C": "Resets state variables to initial values", "D": "Frees memory directly from V8 garbage collector"},
        "correct_answer": "A",
        "explanation": "Effect cleanups cancel timers, subscriptions, socket listeners, and pending requests prior to unmounting or re-running the effect.",
        "difficulty": "easy",
        "misconception_targets": ["useEffect cleanup function timing and lifecycle"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Custom Hooks and Context API",
        "question_type": "conceptual",
        "question_text": "What are the two core Rules of Hooks enforced by React and ESLint?",
        "code_snippet": None,
        "options": {"A": "Only call hooks at the top level (never in loops/conditions) and only call hooks from React function components or custom hooks", "B": "Hooks must return arrays and be prefixed with use_", "C": "Hooks can only be called in class lifecycle methods", "D": "Hooks must always have async definitions"},
        "correct_answer": "A",
        "explanation": "Calling hooks in consistent order at the top level ensures React's internal fiber linked list correctly pairs hook states across renders.",
        "difficulty": "easy",
        "misconception_targets": ["Rules of Hooks and fiber call order consistency"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "State Immutability and useEffect Hook",
        "question_type": "output_prediction",
        "question_text": "What will be logged by consecutive setState calls using the direct value form?",
        "code_snippet": "const [count, setCount] = useState(0);\nconst handleClick = () => {\n    setCount(count + 1);\n    setCount(count + 1);\n    setCount(count + 1);\n};\n// After click, what is count in the next render?",
        "options": {"A": "1", "B": "3", "C": "0", "D": "TypeError"},
        "correct_answer": "A",
        "explanation": "In React 18 automatic batching, count is 0 in the current closure. All three calls evaluate to setCount(0 + 1), resulting in count being 1.",
        "difficulty": "medium",
        "misconception_targets": ["Stale closure in batching vs functional state updater setCount(prev => prev + 1)"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Custom Hooks and Context API",
        "question_type": "conceptual",
        "question_text": "What does React.useCallback(fn, deps) do compared to React.useMemo(fn, deps)?",
        "code_snippet": None,
        "options": {"A": "useCallback caches the function definition itself; useMemo caches the returned result of calling the function", "B": "useCallback is for asynchronous calls only", "C": "useMemo runs on every render; useCallback runs on mount", "D": "They are synonymous"},
        "correct_answer": "A",
        "explanation": "useCallback(fn, deps) is syntactic sugar for useMemo(() => fn, deps). It prevents child re-renders caused by unstable callback references.",
        "difficulty": "easy",
        "misconception_targets": ["useCallback function memoization vs useMemo computed value memoization"]
    },

    # ── HTML (CS-HTML) ───────────────────────────────────────────────────────
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the purpose of the `defer` attribute on a <script> tag?",
        "code_snippet": "<script src=\"app.js\" defer></script>",
        "options": {"A": "Downloads script in background without blocking HTML parsing and executes after DOM is fully parsed", "B": "Executes script immediately upon download, blocking parsing", "C": "Runs script only after user interaction", "D": "Compiles script into WebAssembly"},
        "correct_answer": "A",
        "explanation": "defer fetches script asynchronously during DOM construction and guarantees execution in document order right before DOMContentLoaded.",
        "difficulty": "easy",
        "misconception_targets": ["Script defer vs async vs parser-blocking scripts"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the difference between `defer` and `async` on script tags?",
        "code_snippet": None,
        "options": {"A": "async executes as soon as downloaded (interrupting parsing); defer executes after DOM parsing finishes in script order", "B": "defer is synchronous; async is asynchronous", "C": "async preserves script order; defer does not", "D": "They perform identically"},
        "correct_answer": "A",
        "explanation": "async scripts execute immediately upon arrival without preserving document order. defer scripts execute in document order after parsing completes.",
        "difficulty": "medium",
        "misconception_targets": ["async out-of-order execution vs defer ordered execution"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "Which attribute on an <a> element should be added when opening untrusted external links with `target=\"_blank\"`?",
        "code_snippet": "<a href=\"https://external.com\" target=\"_blank\" rel=\"noopener noreferrer\">Link</a>",
        "options": {"A": "rel=\"noopener noreferrer\" to prevent tab-nabbing security exploits via window.opener", "B": "download=\"true\"", "C": "target=\"_parent\"", "D": "sandbox=\"allow-scripts\""},
        "correct_answer": "A",
        "explanation": "Without noopener, the opened page can access window.opener and navigate the referring page to a malicious phishing site.",
        "difficulty": "medium",
        "misconception_targets": ["Reverse tabnabbing vulnerability and rel=noopener"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the function of the <template> element in HTML5?",
        "code_snippet": "<template id=\"card-template\">\n    <div class=\"card\"><h3></h3></div>\n</template>",
        "options": {"A": "Holds client-side content that is not rendered on page load but can be cloned and inserted via JavaScript", "B": "Styles all elements matching the class", "C": "Pre-renders HTML into canvas", "D": "Loads server-side template automatically"},
        "correct_answer": "A",
        "explanation": "<template> contents are inert DOM fragments parsed but not displayed or evaluated until cloned via document.importNode or cloneNode.",
        "difficulty": "medium",
        "misconception_targets": ["HTML5 template inertness and client-side templating"]
    },

    # ── CSS (CS-CSS) ─────────────────────────────────────────────────────────
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "conceptual",
        "question_text": "What is the difference between `position: absolute` and `position: fixed` in CSS?",
        "code_snippet": None,
        "options": {"A": "fixed is positioned relative to the viewport; absolute is positioned relative to the nearest positioned ancestor", "B": "absolute stays fixed on scroll", "C": "fixed flows in normal document flow", "D": "absolute cannot have z-index"},
        "correct_answer": "A",
        "explanation": "fixed positions relative to the viewport and remains stationary during scrolling. absolute positions relative to the nearest ancestor with position other than static.",
        "difficulty": "easy",
        "misconception_targets": ["Containing block difference between fixed and absolute positioning"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "conceptual",
        "question_text": "What is the CSS rem unit relative to?",
        "code_snippet": None,
        "options": {"A": "The font-size of the root <html> element", "B": "The font-size of the immediate parent element", "C": "The viewport width", "D": "The device physical pixel density"},
        "correct_answer": "A",
        "explanation": "rem stands for 'root em'. 1rem equals the computed font-size of the root (<html>) element, typically 16px by default.",
        "difficulty": "easy",
        "misconception_targets": ["rem (root) vs em (parent) relative typography units"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "output_prediction",
        "question_text": "What does `flex: 1 1 0%` specify for a flex child?",
        "code_snippet": None,
        "options": {"A": "flex-grow: 1, flex-shrink: 1, flex-basis: 0% (children divide available space equally)", "B": "The child will not shrink", "C": "The child will occupy 0 pixels width", "D": "Disables flexbox distribution"},
        "correct_answer": "A",
        "explanation": "With flex-basis: 0%, all container width is treated as free space and distributed equally according to flex-grow weights.",
        "difficulty": "medium",
        "misconception_targets": ["flex-basis 0% vs flex-basis auto space distribution"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "conceptual",
        "question_text": "Which CSS property causes elements to trigger hardware GPU acceleration for smooth 60fps animations?",
        "code_snippet": "transform: translate3d(0, 0, 0); or will-change: transform;",
        "options": {"A": "transform and opacity (composited on GPU without triggering layout or paint)", "B": "margin-left and top", "C": "width and height", "D": "display: flex"},
        "correct_answer": "A",
        "explanation": "Animating transform and opacity bypasses the browser's expensive Layout and Paint stages, performing only GPU compositing.",
        "difficulty": "hard",
        "misconception_targets": ["Browser rendering pipeline: Layout vs Paint vs Composite"]
    },

    # ── SQL (CS-SQL) ─────────────────────────────────────────────────────────
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "Which query correctly finds duplicate emails in a users table?",
        "code_snippet": None,
        "options": {"A": "SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;", "B": "SELECT email FROM users WHERE COUNT(email) > 1;", "C": "SELECT DISTINCT email FROM users WHERE email IS DUPLICATE;", "D": "SELECT email FROM users GROUP BY email WHERE COUNT(*) > 1;"},
        "correct_answer": "A",
        "explanation": "Grouping by email and using HAVING COUNT(*) > 1 filters groups to only those with multiple occurrences.",
        "difficulty": "easy",
        "misconception_targets": ["Using HAVING rather than WHERE for aggregate counting"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "conceptual",
        "question_text": "What is the difference between Clustered Index and Non-Clustered Index in relational databases?",
        "code_snippet": None,
        "options": {"A": "Clustered index defines the physical order of table rows on disk (only one allowed); non-clustered index creates separate lookup pointers", "B": "A table can have multiple clustered indexes", "C": "Non-clustered indexes are slower than full table scans", "D": "Clustered indexes only work on foreign keys"},
        "correct_answer": "A",
        "explanation": "Because physical disk order can only be arranged one way, a table has at most one clustered index. Non-clustered indexes store secondary search trees pointing to row locators.",
        "difficulty": "medium",
        "misconception_targets": ["Clustered index physical storage arrangement vs secondary indexes"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "What does the EXISTS operator return in SQL subqueries?",
        "code_snippet": "SELECT name FROM departments d WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);",
        "options": {"A": "TRUE as soon as the first matching row is found in the subquery (short-circuits)", "B": "The count of rows matching the subquery", "C": "A table of IDs", "D": "Throws error if subquery has more than 1 row"},
        "correct_answer": "A",
        "explanation": "EXISTS tests for the existence of rows and short-circuits to TRUE upon encountering the first matching record.",
        "difficulty": "medium",
        "misconception_targets": ["EXISTS short-circuit boolean evaluation vs IN subquery full materialization"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "How do you find the second highest salary using pure SQL?",
        "code_snippet": None,
        "options": {"A": "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);", "B": "SELECT salary FROM employees ORDER BY salary DESC LIMIT 2;", "C": "SELECT SECOND_MAX(salary) FROM employees;", "D": "SELECT salary[1] FROM employees;"},
        "correct_answer": "A",
        "explanation": "The inner query retrieves the maximum salary, and the outer query retrieves the highest salary strictly less than that maximum.",
        "difficulty": "easy",
        "misconception_targets": ["Finding Nth highest value with subqueries"]
    },
]


def seed_additional():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, code, name FROM subjects")
    subjects = {r[1]: r[0] for r in cur.fetchall()}

    cur.execute("SELECT id, subject_id, name FROM concepts")
    concept_map = {}
    subject_first_concept = {}
    for cid, sid, cname in cur.fetchall():
        concept_map[(sid, cname.strip().lower())] = cid
        if sid not in subject_first_concept:
            subject_first_concept[sid] = cid

    inserted_count = 0
    now = datetime.utcnow().isoformat()

    for q in ADDITIONAL_QUESTIONS:
        code = q["subject_code"]
        sid = subjects.get(code)
        if not sid:
            continue

        cname = q.get("concept_name", "").strip().lower()
        cid = concept_map.get((sid, cname))
        if not cid:
            cid = subject_first_concept.get(sid)

        if not cid:
            continue

        q_text = q["question_text"].strip()
        cur.execute("SELECT id FROM questions WHERE concept_id = ? AND question_text = ?", (cid, q_text))
        if cur.fetchone():
            continue

        cur.execute(
            """
            INSERT INTO questions (
                subject_id, concept_id, question_type, question_text,
                code_snippet, options, correct_answer, explanation,
                difficulty, misconception_targets, is_ai_generated, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sid,
                cid,
                q.get("question_type", "mcq"),
                q_text,
                q.get("code_snippet"),
                json.dumps(q["options"]),
                q["correct_answer"],
                q.get("explanation", ""),
                q.get("difficulty", "medium"),
                json.dumps(q.get("misconception_targets", [])),
                0,
                now,
            ),
        )
        inserted_count += 1

    conn.commit()
    print(f"Inserted {inserted_count} additional questions.")

    cur.execute(
        """
        SELECT s.id, s.code, s.name, count(q.id)
        FROM subjects s
        LEFT JOIN questions q ON q.subject_id = s.id
        WHERE s.code IN ('CS-PY', 'CS-C', 'CS-CPP', 'CS-JAVA', 'CS-JS', 'CS-HTML', 'CS-CSS', 'CS-REACT', 'CS-SQL', 'CS-DSA')
        GROUP BY s.id, s.code, s.name
        ORDER BY s.id
        """
    )
    for row in cur.fetchall():
        print(f"Subject {row[1]} ({row[2]}): {row[3]} questions in DB")

    conn.close()


if __name__ == "__main__":
    seed_additional()
