"""
Curated B.Tech Computer Science and Engineering Question Bank for LearnSphere AI.
Covers:
- Programming Languages: Python, C, C++, Java, JavaScript
- Frontend: HTML, CSS, React.js, Tailwind CSS
- Backend: Node.js, FastAPI, REST APIs, Auth & Security, Express.js
- Databases: SQL, MySQL, MongoDB, Database Design, DBMS Fundamentals
- CS Core: Data Structures and Algorithms, Operating Systems, Computer Networks, OOP, Computer Organization
- Artificial Intelligence: Machine Learning, Deep Learning, Generative AI, Agentic AI, Heuristic Search
"""
import random
from typing import Optional, List, Dict, Any

FALLBACK_QUESTIONS: List[Dict[str, Any]] = [
    # ══════════════════════════════════════════════════════════════════════════
    # 1. PYTHON PROGRAMMING (CS-PY) - 12+ Distinct Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-PY",
        "concept_name": "Mutable vs Immutable Objects",
        "question_type": "output_prediction",
        "question_text": "What is the output of the following Python snippet?",
        "code_snippet": "def append_to_list(val, my_list=[]):\n    my_list.append(val)\n    return my_list\n\nprint(append_to_list(1))\nprint(append_to_list(2))",
        "options": {
            "A": "[1] and [2]",
            "B": "[1] and [1, 2]",
            "C": "[1, 2] and [1, 2]",
            "D": "TypeError: default value cannot be mutated"
        },
        "correct_answer": "B",
        "explanation": "In Python, default parameter values are evaluated once at function definition time, not on every call. Since a list is mutable, mutations persist across calls when the default is used.",
        "difficulty": "medium",
        "misconception_targets": [
            "Default parameter re-instantiation assumption",
            "Confusion between mutable reference binding and variable assignment"
        ]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "List Slicing and Negative Indexing",
        "question_type": "output_prediction",
        "question_text": "What does the following slice operation return in Python?",
        "code_snippet": "numbers = [10, 20, 30, 40, 50, 60]\nresult = numbers[-4:5:2]\nprint(result)",
        "options": {
            "A": "[30, 50]",
            "B": "[20, 40]",
            "C": "[30, 40, 50]",
            "D": "[20, 30, 40, 50]"
        },
        "correct_answer": "A",
        "explanation": "numbers[-4] corresponds to index 2 (value 30). The slice stops before index 5 (value 60) with a step of 2, selecting indices 2 and 4, producing [30, 50].",
        "difficulty": "easy",
        "misconception_targets": [
            "Off-by-one error with negative indexing",
            "Assuming stop index is inclusive"
        ]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Decorators and First-Class Functions",
        "question_type": "conceptual",
        "question_text": "Why should `functools.wraps` be used inside a custom Python decorator?",
        "code_snippet": "import functools\ndef my_decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs)\n    return wrapper",
        "options": {
            "A": "It converts the decorated function into a C-speed compiled function",
            "B": "It preserves the original function's metadata, such as __name__ and __doc__",
            "C": "It enforces type checking on args and kwargs at runtime",
            "D": "It prevents the decorator from being called multiple times"
        },
        "correct_answer": "B",
        "explanation": "functools.wraps copies over the original function attributes (name, docstring, module) to the wrapper function, ensuring reflection, introspection, and debugging tools report correct metadata.",
        "difficulty": "medium",
        "misconception_targets": ["Believing decorators modify bytecode directly", "Ignoring docstring/name masking"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Dunder Methods and Class Attributes",
        "question_type": "code_debugging",
        "question_text": "What is the key semantic difference between `__str__` and `__repr__` in Python?",
        "code_snippet": "class Vector:\n    def __init__(self, x, y):\n        self.x, self.y = x, y",
        "options": {
            "A": "__repr__ is for informal user-facing text; __str__ is an unambiguous technical representation",
            "B": "__str__ is for informal readable text; __repr__ is unambiguous and ideally valid Python code to recreate the object",
            "C": "__str__ is only called by print(); __repr__ is only called inside the interactive REPL",
            "D": "__repr__ is deprecated in Python 3.10+ in favor of __str__"
        },
        "correct_answer": "B",
        "explanation": "__str__ aims for human readability, whereas __repr__ is intended for developers, providing an unambiguous string that, if possible, can recreate the instance via eval().",
        "difficulty": "easy",
        "misconception_targets": ["Confusing user readability with debugging representation"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Generators and Memory Optimization",
        "question_type": "output_prediction",
        "question_text": "What does the following generator expression demonstrate regarding memory and execution?",
        "code_snippet": "gen = (x * 2 for x in [1, 2, 3])\nprint(type(gen))\nprint(next(gen))\nprint(list(gen))",
        "options": {
            "A": "<class 'list'>, 2, [4, 6]",
            "B": "<class 'generator'>, 2, [4, 6]",
            "C": "<class 'generator'>, 2, [2, 4, 6]",
            "D": "<class 'tuple'>, 2, [4, 6]"
        },
        "correct_answer": "B",
        "explanation": "Parentheses create a generator object. next(gen) yields the first value 2. Calling list(gen) consumes the remaining yielded values [4, 6].",
        "difficulty": "medium",
        "misconception_targets": ["Confusing generator expressions with tuple comprehensions", "Assuming generators re-yield consumed items"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Global Interpreter Lock (GIL) and Concurrency",
        "question_type": "conceptual",
        "question_text": "In standard CPython, how does the Global Interpreter Lock (GIL) affect multi-threaded CPU-bound programs?",
        "code_snippet": "import threading\n# 4 threads running heavy mathematical loops",
        "options": {
            "A": "Threads achieve linear 4x speedup across 4 CPU cores",
            "B": "Threads run concurrently on separate cores without any locking",
            "C": "Only one thread executes Python bytecode at any instant, providing no multi-core CPU speedup",
            "D": "CPython automatically spawns operating system processes instead of threads"
        },
        "correct_answer": "C",
        "explanation": "CPython's GIL permits only one native thread to hold the interpreter lock and execute Python bytecode at a time. For CPU-bound tasks, multiprocessing is required for true parallelism.",
        "difficulty": "hard",
        "misconception_targets": ["Believing Python threading achieves multi-core speedup for CPU tasks"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Dictionary Implementation and Hashing",
        "question_type": "output_prediction",
        "question_text": "What is the output of the following dictionary lookup in Python?",
        "code_snippet": "d = {}\nd[1] = 'integer'\nd[1.0] = 'float'\nd[True] = 'boolean'\nprint(len(d), d[1])",
        "options": {
            "A": "3 boolean",
            "B": "3 integer",
            "C": "1 boolean",
            "D": "2 boolean"
        },
        "correct_answer": "C",
        "explanation": "In Python, 1 == 1.0 == True and hash(1) == hash(1.0) == hash(True). Because keys with equal hash and equal value overwrite the existing entry, only one key exists, with the latest value 'boolean'.",
        "difficulty": "hard",
        "misconception_targets": ["Assuming type differences prevent hash collisions for 1, 1.0, True", "Believing dict keys are strictly segregated by type"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Exception Handling and Control Flow",
        "question_type": "output_prediction",
        "question_text": "What is the return value of this Python function?",
        "code_snippet": "def test_flow():\n    try:\n        return 10\n    finally:\n        return 20\n\nprint(test_flow())",
        "options": {
            "A": "10",
            "B": "20",
            "C": "None",
            "D": "SyntaxError: return inside finally block is illegal"
        },
        "correct_answer": "B",
        "explanation": "The finally clause always executes before the try block completes. If finally executes a return statement, it overrides the pending return from the try block.",
        "difficulty": "medium",
        "misconception_targets": ["Believing try block return cannot be superseded by finally"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "List Comprehensions and Scope",
        "question_type": "output_prediction",
        "question_text": "In Python 3, what does this code output?",
        "code_snippet": "x = 100\nresult = [x for x in range(3)]\nprint(x)",
        "options": {
            "A": "2",
            "B": "100",
            "C": "3",
            "D": "NameError: x is out of scope"
        },
        "correct_answer": "B",
        "explanation": "In Python 3, list comprehensions have their own local function-level scope. The iteration variable x inside the comprehension does not leak into the enclosing scope, leaving outer x at 100.",
        "difficulty": "medium",
        "misconception_targets": ["Assuming Python 2 comprehension variable leakage still happens in Python 3"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Variable Unpacking and Extended Slices",
        "question_type": "output_prediction",
        "question_text": "What are the values of `first`, `middle`, and `last` after extended unpacking?",
        "code_snippet": "first, *middle, last = [1, 2, 3, 4, 5]\nprint(first, middle, last)",
        "options": {
            "A": "1 [2, 3, 4] 5",
            "B": "1 (2, 3, 4) 5",
            "C": "1 2, 3, 4 5",
            "D": "ValueError: too many values to unpack"
        },
        "correct_answer": "A",
        "explanation": "Extended unpacking collects remaining elements into a list bound to *middle, leaving first=1 and last=5.",
        "difficulty": "easy",
        "misconception_targets": ["Thinking starred expressions produce tuples"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Class Inheritance and MRO",
        "question_type": "conceptual",
        "question_text": "What algorithm does Python use to determine the Method Resolution Order (MRO) in multiple inheritance?",
        "code_snippet": "class A: pass\nclass B(A): pass\nclass C(A): pass\nclass D(B, C): pass",
        "options": {
            "A": "Depth-First Search (DFS)",
            "B": "Breadth-First Search (BFS)",
            "C": "C3 Superlinear Linearization Algorithm",
            "D": "Dijkstra's Shortest Path Algorithm"
        },
        "correct_answer": "C",
        "explanation": "Python uses the C3 Linearization algorithm to compute a deterministic MRO that respects monotonicity and local precedence order without cyclic dependencies.",
        "difficulty": "hard",
        "misconception_targets": ["Assuming standard naive DFS traversal for class hierarchy"]
    },
    {
        "subject_code": "CS-PY",
        "concept_name": "Copy vs Deepcopy",
        "question_type": "output_prediction",
        "question_text": "What is printed after mutating a nested list following `copy.copy`?",
        "code_snippet": "import copy\noriginal = [[1, 2], [3, 4]]\nshallow = copy.copy(original)\nshallow[0].append(99)\nprint(original[0])",
        "options": {
            "A": "[1, 2]",
            "B": "[1, 2, 99]",
            "C": "[99]",
            "D": "TypeError: cannot copy nested list"
        },
        "correct_answer": "B",
        "explanation": "A shallow copy duplicates the outer list container, but elements inside still reference the original nested list objects. Modifying shallow[0] mutates original[0].",
        "difficulty": "easy",
        "misconception_targets": ["Thinking shallow copy recursively duplicates nested collections"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 2. JAVASCRIPT PROGRAMMING (CS-JS) - 12+ Distinct Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-JS",
        "concept_name": "Closures and Lexical Scope",
        "question_type": "output_prediction",
        "question_text": "What is the output when invoking the returned closures?",
        "code_snippet": "function createCounters() {\n  var funcs = [];\n  for (var i = 0; i < 3; i++) {\n    funcs.push(() => i);\n  }\n  return funcs;\n}\nconst [a, b, c] = createCounters();\nconsole.log(a(), b(), c());",
        "options": {
            "A": "0 1 2",
            "B": "3 3 3",
            "C": "undefined undefined undefined",
            "D": "ReferenceError: i is not defined"
        },
        "correct_answer": "B",
        "explanation": "Because `var` is function-scoped rather than block-scoped, all 3 arrow functions close over the same variable `i`. By loop termination, `i` has reached 3.",
        "difficulty": "medium",
        "misconception_targets": [
            "Assuming `var` re-binds per loop iteration like `let`",
            "Believing arrow functions capture values rather than references"
        ]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Event Loop and Microtasks",
        "question_type": "output_prediction",
        "question_text": "What is the exact logged order of output?",
        "code_snippet": "console.log('1');\nsetTimeout(() => console.log('2'), 0);\nPromise.resolve().then(() => console.log('3'));\nconsole.log('4');",
        "options": {
            "A": "1, 2, 3, 4",
            "B": "1, 4, 2, 3",
            "C": "1, 4, 3, 2",
            "D": "1, 3, 4, 2"
        },
        "correct_answer": "C",
        "explanation": "Synchronous code runs first ('1', '4'). Next, the microtask queue (Promise.then) is completely drained ('3'). Finally, the macrotask queue (setTimeout) executes ('2').",
        "difficulty": "hard",
        "misconception_targets": ["Confusing macrotask and microtask queue priorities in the JS event loop"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Equality Operators and Type Coercion",
        "question_type": "output_prediction",
        "question_text": "What do the following comparison expressions evaluate to in JavaScript?",
        "code_snippet": "console.log([] == false);\nconsole.log([] == ![]);",
        "options": {
            "A": "false and false",
            "B": "true and true",
            "C": "false and true",
            "D": "true and false"
        },
        "correct_answer": "B",
        "explanation": "For [] == false, [] converts to '' then 0, and false is 0, giving true. For [] == ![], ![] is false, leading to [] == false, which also evaluates to true.",
        "difficulty": "medium",
        "misconception_targets": ["Assuming non-empty and empty objects strictly evaluate as boolean false in loose equality"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "This Keyword and Execution Context",
        "question_type": "output_prediction",
        "question_text": "What is the output of `obj.greet()` vs `detached()`?",
        "code_snippet": "const obj = {\n  name: 'LearnSphere',\n  greet() {\n    return this.name;\n  }\n};\nconst detached = obj.greet;\nconsole.log(obj.greet(), detached());",
        "options": {
            "A": "LearnSphere LearnSphere",
            "B": "LearnSphere undefined",
            "C": "undefined undefined",
            "D": "TypeError: detached is not a function"
        },
        "correct_answer": "B",
        "explanation": "In non-strict mode, calling detached() invokes the function without an explicit context object, binding `this` to the global object (window/global), where name is undefined.",
        "difficulty": "medium",
        "misconception_targets": ["Believing method references permanently bind their enclosing object context"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Arrow Functions and Arguments Object",
        "question_type": "conceptual",
        "question_text": "Which of the following is true regarding arrow functions in ES6+?",
        "code_snippet": "const add = (a, b) => a + b;",
        "options": {
            "A": "Arrow functions have their own `this`, `super`, and `arguments` bindings",
            "B": "Arrow functions can be used as constructors with the `new` keyword",
            "C": "Arrow functions retain lexical `this` from their enclosing scope and do not possess their own `arguments` object",
            "D": "Arrow functions require an explicit `return` statement even for single expressions"
        },
        "correct_answer": "C",
        "explanation": "Arrow functions do not define their own `this`, `arguments`, `super`, or `new.target`. They inherit these identifiers from the surrounding lexical scope and cannot be constructors.",
        "difficulty": "easy",
        "misconception_targets": ["Attempting to instantiate arrow functions with new", "Looking for arguments inside an arrow function"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Promises and Async/Await",
        "question_type": "output_prediction",
        "question_text": "What is logged when calling this async function?",
        "code_snippet": "async function compute() {\n  return 42;\n}\nconst result = compute();\nconsole.log(result);",
        "options": {
            "A": "42",
            "B": "Promise { 42 }",
            "C": "undefined",
            "D": "TypeError: async functions must be awaited"
        },
        "correct_answer": "B",
        "explanation": "An async function always wraps its return value in a Promise. Calling compute() without `await` returns an unresolved or resolved Promise object, not the raw scalar 42.",
        "difficulty": "easy",
        "misconception_targets": ["Assuming calling an async function directly unwraps its returned value"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Temporal Dead Zone (TDZ)",
        "question_type": "output_prediction",
        "question_text": "What happens when executing this code snippet?",
        "code_snippet": "console.log(a);\nconsole.log(b);\nvar a = 10;\nlet b = 20;",
        "options": {
            "A": "undefined followed by ReferenceError: Cannot access 'b' before initialization",
            "B": "undefined followed by undefined",
            "C": "ReferenceError for a followed by ReferenceError for b",
            "D": "10 followed by 20"
        },
        "correct_answer": "A",
        "explanation": "`var a` is hoisted and initialized to `undefined`. `let b` is hoisted but uninitialized, residing in the Temporal Dead Zone (TDZ) until the declaration line, throwing a ReferenceError.",
        "difficulty": "medium",
        "misconception_targets": ["Believing let/const are not hoisted at all", "Believing let is initialized to undefined like var"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Object Prototype Chain",
        "question_type": "conceptual",
        "question_text": "What does `Object.prototype.__proto__` evaluate to in standard JavaScript?",
        "code_snippet": "console.log(Object.prototype.__proto__);",
        "options": {
            "A": "Object",
            "B": "null",
            "C": "undefined",
            "D": "Function.prototype"
        },
        "correct_answer": "B",
        "explanation": "Object.prototype is at the top of the prototype chain. Its internal [[Prototype]] is `null`, terminating the prototype resolution traversal.",
        "difficulty": "hard",
        "misconception_targets": ["Assuming prototype chains form an infinite cycle back to Object"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Array Reduce and Immutability",
        "question_type": "output_prediction",
        "question_text": "What is the output of this `Array.prototype.reduce` call?",
        "code_snippet": "const nums = [1, 2, 3, 4];\nconst sum = nums.reduce((acc, curr) => acc + curr, 10);\nconsole.log(sum);",
        "options": {
            "A": "10",
            "B": "20",
            "C": "24",
            "D": "14"
        },
        "correct_answer": "B",
        "explanation": "The initial accumulator value is 10. Adding 1 + 2 + 3 + 4 = 10 yields 10 + 10 = 20.",
        "difficulty": "easy",
        "misconception_targets": ["Omitting initial value from total sum calculations"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "WeakMap vs Map",
        "question_type": "conceptual",
        "question_text": "What is the primary architectural difference between `WeakMap` and `Map` in JavaScript?",
        "code_snippet": "const wm = new WeakMap();\nconst m = new Map();",
        "options": {
            "A": "WeakMap allows primitive values as keys; Map requires objects",
            "B": "WeakMap keys must be objects and hold weak references allowing garbage collection; WeakMap is non-enumerable",
            "C": "Map does not preserve insertion order; WeakMap strictly does",
            "D": "WeakMap allows async lookups; Map is strictly synchronous"
        },
        "correct_answer": "B",
        "explanation": "WeakMap keys must be objects and are held weakly. If no other reference to the key object exists, it can be garbage collected. Thus, WeakMap cannot be enumerated (.keys(), .size).",
        "difficulty": "hard",
        "misconception_targets": ["Believing WeakMap is just a slower version of Map with .forEach() support"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Function Currying and Higher-Order Functions",
        "question_type": "output_prediction",
        "question_text": "What is the output of the curried function invocation?",
        "code_snippet": "const multiply = a => b => c => a * b * c;\nconsole.log(multiply(2)(3)(4));",
        "options": {
            "A": "24",
            "B": "9",
            "C": "NaN",
            "D": "undefined"
        },
        "correct_answer": "A",
        "explanation": "Each function call returns a closure capturing the previous arguments: 2 * 3 * 4 = 24.",
        "difficulty": "easy",
        "misconception_targets": ["Confusing currying syntax with tuple argument lists"]
    },
    {
        "subject_code": "CS-JS",
        "concept_name": "Pass-by-Value of Object References",
        "question_type": "output_prediction",
        "question_text": "What is the value of `user.name` after `reassignUser` completes?",
        "code_snippet": "function reassignUser(u) {\n  u = { name: 'Bob' };\n}\nconst user = { name: 'Alice' };\nreassignUser(user);\nconsole.log(user.name);",
        "options": {
            "A": "Bob",
            "B": "Alice",
            "C": "undefined",
            "D": "TypeError: Assignment to constant variable"
        },
        "correct_answer": "B",
        "explanation": "JavaScript is strictly pass-by-value. When an object is passed, the argument receives a copy of the reference. Reassigning `u` points the local copy to a new object without mutating `user`.",
        "difficulty": "medium",
        "misconception_targets": ["Believing JavaScript supports pass-by-reference for reassignments"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 3. REACT.JS (CS-REACT) - 12+ Distinct Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-REACT",
        "concept_name": "Virtual DOM and Reconciliation",
        "question_type": "conceptual",
        "question_text": "In React's reconciliation algorithm, what is the primary purpose of the `key` prop when rendering dynamic lists?",
        "code_snippet": "<ul>\n  {items.map(item => <li key={item.id}>{item.text}</li>)}\n</ul>",
        "options": {
            "A": "To bind CSS styles and animation keyframes to DOM elements",
            "B": "To help React identify which items have changed, been added, or been removed between renders",
            "C": "To automatically serialize items into the browser's localStorage",
            "D": "To prevent child components from re-rendering when props change"
        },
        "correct_answer": "B",
        "explanation": "Keys provide a stable identity to elements across renders. Without stable keys (or using array indices during reorders), React cannot match Virtual DOM nodes to existing real DOM nodes, causing redundant re-mounts and UI bugs.",
        "difficulty": "easy",
        "misconception_targets": [
            "Using array index as a safe universal key",
            "Thinking key is accessible inside the component via props.key"
        ]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "useEffect Dependency Array and Stale Closures",
        "question_type": "code_debugging",
        "question_text": "What bug is present in this counter timer effect?",
        "code_snippet": "const [count, setCount] = useState(0);\nuseEffect(() => {\n  const id = setInterval(() => {\n    setCount(count + 1);\n  }, 1000);\n  return () => clearInterval(id);\n}, []);",
        "options": {
            "A": "The interval does not run because dependencies are missing",
            "B": "Due to an empty dependency array, the closure captures `count` as 0; count will increment to 1 and stay at 1",
            "C": "clearInterval throws because id is undefined",
            "D": "useState cannot be called inside a component with useEffect"
        },
        "correct_answer": "B",
        "explanation": "Because `[]` is used, the callback captures the initial render's `count` (0). Every second, it executes `setCount(0 + 1)`, causing the value to remain permanently 1. The fix is functional state update: `setCount(prev => prev + 1)`.",
        "difficulty": "medium",
        "misconception_targets": ["Stale closure state capture in useEffect"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "State Batching in React 18+",
        "question_type": "output_prediction",
        "question_text": "In React 18, how many re-renders occur when triggering this button click handler?",
        "code_snippet": "function Counter() {\n  const [count, setCount] = useState(0);\n  const [flag, setFlag] = useState(false);\n\n  function handleClick() {\n    setTimeout(() => {\n      setCount(c => c + 1);\n      setFlag(f => !f);\n    }, 100);\n  }\n  return <button onClick={handleClick}>Click</button>;\n}",
        "options": {
            "A": "2 re-renders because state updates inside setTimeout are never batched",
            "B": "1 re-render because React 18 features Automatic Batching across promises, timeouts, and native events",
            "C": "0 re-renders because state setters inside setTimeout are ignored",
            "D": "Infinite re-renders"
        },
        "correct_answer": "B",
        "explanation": "React 18 introduced Automatic Batching. State updates triggered inside timeouts, promises, or async handlers are batched together into a single re-render.",
        "difficulty": "hard",
        "misconception_targets": ["Believing setTimeout updates still bypass React batching in modern React 18"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "useMemo vs useCallback",
        "question_type": "conceptual",
        "question_text": "What is the exact distinction between `useMemo` and `useCallback` in React?",
        "code_snippet": "const memoizedVal = useMemo(() => compute(a), [a]);\nconst memoizedFn = useCallback(() => doSomething(a), [a]);",
        "options": {
            "A": "useMemo caches a function definition; useCallback caches the calculated return value",
            "B": "useCallback caches the function definition itself; useMemo caches the result of invoking a function",
            "C": "useMemo executes asynchronously in a web worker; useCallback runs synchronously",
            "D": "There is no difference; useCallback is an alias for useMemo"
        },
        "correct_answer": "B",
        "explanation": "useCallback(fn, deps) is equivalent to useMemo(() => fn, deps). useCallback returns a memoized function instance; useMemo returns the memoized result of calling the function.",
        "difficulty": "medium",
        "misconception_targets": ["Confusing cached function reference with cached return value"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Rules of Hooks",
        "question_type": "code_debugging",
        "question_text": "Why does the following code violate React's Rules of Hooks?",
        "code_snippet": "function UserProfile({ id }) {\n  if (!id) return <div>No ID</div>;\n  const [user, setUser] = useState(null);\n  return <div>{user?.name}</div>;\n}",
        "options": {
            "A": "useState cannot be called inside a functional component",
            "B": "Hooks cannot be called conditionally or after early returns, as React relies on call order stability across renders",
            "C": "UserProfile must be defined as an ES6 class to use state",
            "D": "Props cannot be destructured in component signatures"
        },
        "correct_answer": "B",
        "explanation": "React internally tracks hooks using a linked list keyed to execution order. Calling hooks conditionally or after an early return disrupts the hook sequence, causing state corruption.",
        "difficulty": "easy",
        "misconception_targets": ["Placing hooks inside if statements or after return statements"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Controlled vs Uncontrolled Components",
        "question_type": "conceptual",
        "question_text": "What defines a component as a 'controlled component' in React?",
        "code_snippet": "<input value={value} onChange={e => setValue(e.target.value)} />",
        "options": {
            "A": "Form data is managed directly by the DOM via `useRef`",
            "B": "Form input values are driven exclusively by React component state and updated via callbacks",
            "C": "The input has a required HTML5 validation attribute",
            "D": "The component is wrapped in an Error Boundary"
        },
        "correct_answer": "B",
        "explanation": "In a controlled component, form input element values are driven by React state (value prop) and changes are handled by event callbacks (onChange), making React the single source of truth.",
        "difficulty": "easy",
        "misconception_targets": ["Confusing useRef DOM extraction with React controlled state"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Component Lifecycle and Cleanup Functions",
        "question_type": "output_prediction",
        "question_text": "When does the cleanup function returned by `useEffect` execute?",
        "code_snippet": "useEffect(() => {\n  subscribe();\n  return () => unsubscribe();\n}, [topic]);",
        "options": {
            "A": "Only when the browser window closes",
            "B": "Before the component re-runs the effect on dependency change, and when the component unmounts",
            "C": "Immediately after the initial render only",
            "D": "Synchronously before the Virtual DOM is rendered"
        },
        "correct_answer": "B",
        "explanation": "Effect cleanups run before every re-execution of the effect (to clean up the previous run) and upon component unmounting.",
        "difficulty": "medium",
        "misconception_targets": ["Believing cleanups only run on component unmount"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Context API Re-render Optimization",
        "question_type": "conceptual",
        "question_text": "How can unnecessary re-renders in consumers of a React Context be minimized?",
        "code_snippet": "const AuthContext = createContext();",
        "options": {
            "A": "By setting the context value to a primitive boolean only",
            "B": "By splitting contexts (e.g. state vs dispatch) and memoizing the provider value object with `useMemo`",
            "C": "By declaring the context outside of React components",
            "D": "Context cannot cause re-renders in children"
        },
        "correct_answer": "B",
        "explanation": "If a provider passes an unmemoized object literal `value={{ user, dispatch }}`, a new object is created on every render, triggering re-renders in all consumers. Memoizing the value with useMemo or splitting contexts prevents this.",
        "difficulty": "hard",
        "misconception_targets": ["Passing raw unmemoized object literals directly into Context.Provider"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "React.memo and Shallow Comparison",
        "question_type": "output_prediction",
        "question_text": "Why might a `React.memo` wrapped component still re-render when its parent re-renders?",
        "code_snippet": "const Child = React.memo(({ onClick }) => <button onClick={onClick}>Go</button>);",
        "options": {
            "A": "React.memo is deprecated in modern React",
            "B": "The parent passes an inline function `onClick={() => {}}`, creating a new function reference on every render",
            "C": "React.memo only works for class components",
            "D": "Child components must receive at least 3 props for React.memo to take effect"
        },
        "correct_answer": "B",
        "explanation": "React.memo performs shallow comparison (`===`) on props. Passing an unmemoized inline arrow function generates a new reference each render, failing the equality check and re-rendering the child.",
        "difficulty": "medium",
        "misconception_targets": ["Assuming React.memo deep-compares function references or object literals"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Custom Hooks Architecture",
        "question_type": "conceptual",
        "question_text": "When two components use the same custom hook, what is shared between them?",
        "code_snippet": "function useWindowWidth() {\n  const [width, setWidth] = useState(window.innerWidth);\n  return width;\n}",
        "options": {
            "A": "They share the exact same state instance across both components (like a singleton)",
            "B": "They share only the stateful logic; each component call gets completely isolated, independent state",
            "C": "They automatically synchronize state over WebSockets",
            "D": "They share a single DOM reference"
        },
        "correct_answer": "B",
        "explanation": "Custom hooks reuse stateful logic, not state itself. Each component calling a custom hook gets completely separate, isolated state and effects.",
        "difficulty": "easy",
        "misconception_targets": ["Assuming custom hooks act as global shared state stores"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Suspense and Lazy Loading",
        "question_type": "conceptual",
        "question_text": "What is the primary benefit of `React.lazy` combined with `<Suspense>`?",
        "code_snippet": "const HeavyChart = React.lazy(() => import('./HeavyChart'));",
        "options": {
            "A": "It converts client components into Server Components",
            "B": "It enables code-splitting, downloading component bundles on-demand with a fallback UI while loading",
            "C": "It prevents memory leaks by discarding components from the heap",
            "D": "It forces components to render synchronously"
        },
        "correct_answer": "B",
        "explanation": "React.lazy dynamically imports components via code-splitting, keeping the initial bundle size small. Suspense specifies a fallback placeholder while the bundle downloads.",
        "difficulty": "medium",
        "misconception_targets": ["Confusing code splitting with server-side caching"]
    },
    {
        "subject_code": "CS-REACT",
        "concept_name": "Error Boundaries",
        "question_type": "conceptual",
        "question_text": "Which errors can a React Error Boundary NOT catch?",
        "code_snippet": "class ErrorBoundary extends React.Component { ... }",
        "options": {
            "A": "Errors thrown inside render methods of children",
            "B": "Errors inside lifecycle methods",
            "C": "Asynchronous code (e.g. setTimeout callbacks) and event handler errors",
            "D": "Errors thrown during constructor initialization of child components"
        },
        "correct_answer": "C",
        "explanation": "Error boundaries catch errors during rendering, in lifecycle methods, and in constructors of the whole tree below them. They do not catch errors inside async callbacks (e.g., setTimeout), event handlers, or server-side rendering.",
        "difficulty": "hard",
        "misconception_targets": ["Expecting Error Boundaries to intercept errors thrown inside onClick handlers"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 4. DATA STRUCTURES & ALGORITHMS (CS-DSA) - 12+ Distinct Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-DSA",
        "concept_name": "Time Complexity and Big-O Notation",
        "question_type": "conceptual",
        "question_text": "What is the worst-case time complexity of finding an element in a Binary Search Tree (BST) with N nodes?",
        "code_snippet": "class Node:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None",
        "options": {
            "A": "O(1)",
            "B": "O(log N)",
            "C": "O(N)",
            "D": "O(N log N)"
        },
        "correct_answer": "C",
        "explanation": "In an unbalanced or skewed BST (e.g., elements inserted in sorted order), the tree degenerates into a linked list of height N, resulting in worst-case O(N) search time. Balanced trees (AVL, Red-Black) guarantee O(log N).",
        "difficulty": "easy",
        "misconception_targets": [
            "Assuming all Binary Search Trees are automatically balanced",
            "Confusing average case O(log N) with worst-case BST behavior"
        ]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Trees and Binary Search Trees",
        "question_type": "conceptual",
        "question_text": "Which tree traversal of a Binary Search Tree visits nodes in strictly non-decreasing sorted order?",
        "code_snippet": "     4\n   /   \\\n  2     5\n / \\\n1   3",
        "options": {
            "A": "Preorder Traversal (Root, Left, Right)",
            "B": "Inorder Traversal (Left, Root, Right)",
            "C": "Postorder Traversal (Left, Right, Root)",
            "D": "Level-order Breadth-First Traversal"
        },
        "correct_answer": "B",
        "explanation": "By definition of a BST, all nodes in the left subtree are smaller than the root, and all nodes in the right subtree are greater. Inorder traversal (Left, Root, Right) yields keys in sorted order: 1, 2, 3, 4, 5.",
        "difficulty": "easy",
        "misconception_targets": ["Confusing preorder and inorder traversal order"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "QuickSort and Partitioning",
        "question_type": "conceptual",
        "question_text": "Under what condition does standard QuickSort with first-element pivot selection exhibit worst-case O(N^2) time complexity?",
        "code_snippet": "def quicksort(arr): ...",
        "options": {
            "A": "When the array elements are randomly shuffled",
            "B": "When the array is already sorted in ascending or descending order",
            "C": "When all array elements are distinct powers of 2",
            "D": "When the array size is an exact power of 2"
        },
        "correct_answer": "B",
        "explanation": "If the array is already sorted, picking the first element creates maximally unbalanced partitions of sizes 0 and N-1 on every recursive step, leading to N recursions of O(N) work, yielding O(N^2) total time.",
        "difficulty": "medium",
        "misconception_targets": ["Assuming sorted inputs are already 'best case' for naive QuickSort"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Dijkstra's Algorithm and Graphs",
        "question_type": "conceptual",
        "question_text": "Why does Dijkstra's algorithm fail to find the correct shortest path on graphs containing negative edge weights?",
        "code_snippet": "A --(2)--> B --(-5)--> C",
        "options": {
            "A": "It crashes with an arithmetic overflow exception",
            "B": "Its greedy choice property assumes once a vertex is marked visited, its computed distance cannot be reduced further by longer paths",
            "C": "It cannot handle undirected edges",
            "D": "It requires the graph to be a Directed Acyclic Graph (DAG)"
        },
        "correct_answer": "B",
        "explanation": "Dijkstra greedily locks in the minimum distance vertex assuming all edge weights are non-negative. A negative edge can provide a cheaper path later, violating this invariant. Bellman-Ford must be used instead.",
        "difficulty": "hard",
        "misconception_targets": ["Believing adding a constant offset to all edges fixes Dijkstra on negative weights"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Dynamic Programming and Memoization",
        "question_type": "conceptual",
        "question_text": "What are the two essential characteristics a problem must exhibit to be solvable via Dynamic Programming?",
        "code_snippet": "dp[i] = dp[i-1] + dp[i-2]",
        "options": {
            "A": "Greedy choice property and contiguous memory layout",
            "B": "Optimal substructure and overlapping subproblems",
            "C": "Linear time complexity and binary decision branches",
            "D": "Logarithmic depth and acyclic graph representations"
        },
        "correct_answer": "B",
        "explanation": "Optimal substructure means the optimal solution can be constructed from optimal solutions to subproblems. Overlapping subproblems means subproblems are recalculated multiple times, allowing memoization/tabulation.",
        "difficulty": "medium",
        "misconception_targets": ["Confusing divide-and-conquer with dynamic programming"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Heap and Priority Queue Operations",
        "question_type": "output_prediction",
        "question_text": "What is the time complexity of building a Binary Heap from an arbitrary array of N elements using the bottom-up `heapify` algorithm?",
        "code_snippet": "heapq.heapify(unsorted_array)",
        "options": {
            "A": "O(N log N)",
            "B": "O(N)",
            "C": "O(log N)",
            "D": "O(N^2)"
        },
        "correct_answer": "B",
        "explanation": "While inserting N items one by one takes O(N log N), bottom-up heap construction (calling sift-down on internal nodes) sums a converging geometric series h/2^h, taking bounded O(N) linear time.",
        "difficulty": "hard",
        "misconception_targets": ["Assuming heapify takes O(N log N) like sorting"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Hash Table Collisions and Open Addressing",
        "question_type": "conceptual",
        "question_text": "In a Hash Table utilizing Linear Probing, what phenomenon occurs when occupied slots cluster together, degrading lookup performance?",
        "code_snippet": "index = (hash(key) + i) % table_size",
        "options": {
            "A": "Primary Clustering",
            "B": "Secondary Hash Degradation",
            "C": "Deadlock Inversion",
            "D": "Trie Degradation"
        },
        "correct_answer": "A",
        "explanation": "Primary clustering is the tendency for collision resolution by linear probing to create long contiguous blocks of occupied slots, increasing the average search length towards O(N).",
        "difficulty": "medium",
        "misconception_targets": ["Confusing primary clustering (linear probing) with secondary clustering (quadratic probing)"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Graph Cycles and Topological Sort",
        "question_type": "conceptual",
        "question_text": "Which condition is required for a graph to possess a valid Topological Sort?",
        "code_snippet": "tasks = [A -> B, B -> C, C -> D]",
        "options": {
            "A": "The graph must be undirected and connected",
            "B": "The graph must be a Directed Acyclic Graph (DAG)",
            "C": "All vertices must have even in-degrees",
            "D": "The graph must be bipartite"
        },
        "correct_answer": "B",
        "explanation": "Topological sorting linearly orders vertices such that for every directed edge u -> v, u comes before v. If a cycle exists, no such ordering can satisfy all edges; thus the graph must be a DAG.",
        "difficulty": "easy",
        "misconception_targets": ["Attempting topological sort on graphs with directed cycles"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Binary Search and Invariants",
        "question_type": "code_debugging",
        "question_text": "In standard binary search, why is `mid = low + (high - low) // 2` preferred over `mid = (low + high) // 2`?",
        "code_snippet": "int mid = low + (high - low) / 2;",
        "options": {
            "A": "It executes 2x faster at the CPU hardware level",
            "B": "It prevents integer arithmetic overflow when `low + high` exceeds maximum integer capacity",
            "C": "It handles negative array indices automatically",
            "D": "It works with non-sorted arrays"
        },
        "correct_answer": "B",
        "explanation": "In statically typed languages (C, C++, Java), if low and high are large (e.g. > 2^30), low + high overflows into a negative integer, causing out-of-bounds indexing.",
        "difficulty": "medium",
        "misconception_targets": ["Ignoring 32-bit integer overflow in midpoint calculations"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Linked List Cycle Detection",
        "question_type": "conceptual",
        "question_text": "What is the space complexity of Floyd's Cycle-Finding Algorithm (Tortoise and Hare) for detecting a cycle in a singly linked list?",
        "code_snippet": "slow = slow.next\nfast = fast.next.next",
        "options": {
            "A": "O(N) auxiliary space",
            "B": "O(1) auxiliary space",
            "C": "O(log N) call stack space",
            "D": "O(N^2) space"
        },
        "correct_answer": "B",
        "explanation": "Floyd's algorithm uses only two pointer variables (slow and fast), requiring O(1) constant auxiliary space without storing visited node references in a hash set.",
        "difficulty": "easy",
        "misconception_targets": ["Believing cycle detection requires an auxiliary hash set of visited nodes"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Trie (Prefix Tree) Complexity",
        "question_type": "conceptual",
        "question_text": "What is the time complexity to search for a word of length L in a standard Trie containing N total words?",
        "code_snippet": "class TrieNode: ...",
        "options": {
            "A": "O(N)",
            "B": "O(N * L)",
            "C": "O(L)",
            "D": "O(log N)"
        },
        "correct_answer": "C",
        "explanation": "Searching a Trie depends strictly on the length L of the query word, taking O(L) time regardless of how many millions of words N are stored in the tree.",
        "difficulty": "medium",
        "misconception_targets": ["Assuming Trie search time scales with the total number of words in the dictionary"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Two Pointer Technique",
        "question_type": "conceptual",
        "question_text": "Given a sorted array, what is the time complexity of finding two numbers that sum to a target value using two pointers?",
        "code_snippet": "left = 0\nright = len(arr) - 1\nwhile left < right: ...",
        "options": {
            "A": "O(N^2)",
            "B": "O(N log N)",
            "C": "O(N)",
            "D": "O(1)"
        },
        "correct_answer": "C",
        "explanation": "With left starting at 0 and right at N-1, each iteration either increments left or decrements right. The pointers meet in at most N steps, achieving O(N) time and O(1) space.",
        "difficulty": "easy",
        "misconception_targets": ["Using nested loops O(N^2) instead of the two pointer invariant"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 5. C & C++ PROGRAMMING (CS-C, CS-CPP)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "code_debugging",
        "question_text": "What will be printed by this C code snippet?",
        "code_snippet": "#include <stdio.h>\nint main() {\n    int arr[] = {10, 20, 30, 40};\n    int *ptr = arr;\n    *(ptr + 2) += 5;\n    printf(\"%d, %d\", *ptr, arr[2]);\n    return 0;\n}",
        "options": {
            "A": "15, 30",
            "B": "10, 35",
            "C": "10, 30",
            "D": "Segmentation Fault"
        },
        "correct_answer": "B",
        "explanation": "ptr points to arr[0] (value 10). *(ptr + 2) dereferences arr[2], modifying 30 to 35. *ptr remains 10.",
        "difficulty": "medium",
        "misconception_targets": ["Confusing pointer arithmetic with value addition"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "code_debugging",
        "question_text": "What critical memory bug occurs when dereferencing `p` after `free(p)`?",
        "code_snippet": "int *p = (int *)malloc(sizeof(int));\n*p = 100;\nfree(p);\nprintf(\"%d\", *p);",
        "options": {
            "A": "Stack Overflow",
            "B": "Use-After-Free (Dangling Pointer) undefined behavior",
            "C": "Memory leak of 4 bytes",
            "D": "Compilation error"
        },
        "correct_answer": "B",
        "explanation": "Calling free(p) relinquishes heap memory back to the allocator. Pointer p becomes a dangling pointer; dereferencing it is undefined behavior.",
        "difficulty": "medium",
        "misconception_targets": ["Assuming free() sets the pointer variable to NULL automatically"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "conceptual",
        "question_text": "In C++, why is it essential to declare a base class destructor as `virtual` when deleting an object through a base pointer?",
        "code_snippet": "class Base { public: virtual ~Base() {} };\nclass Derived : public Base { int* data; };",
        "options": {
            "A": "To allow private members of the derived class to be inherited",
            "B": "To ensure the derived class destructor is invoked first, preventing resource and memory leaks",
            "C": "To force static compile-time binding of all member functions",
            "D": "To prevent other classes from inheriting from the base class"
        },
        "correct_answer": "B",
        "explanation": "If the base destructor is not virtual, deleting via Base* only invokes Base's destructor, failing to invoke Derived's destructor and leaking Derived resources.",
        "difficulty": "hard",
        "misconception_targets": ["Believing destructors automatically dispatch polymorphically without virtual keyword"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Standard Template Library (STL) Containers",
        "question_type": "conceptual",
        "question_text": "What happens to pointers and iterators referencing `std::vector` elements when `push_back` causes capacity reallocation?",
        "code_snippet": "std::vector<int> v = {1, 2, 3};\nint* ptr = &v[0];\nv.push_back(4);",
        "options": {
            "A": "They remain valid because vector automatically updates all raw pointer addresses",
            "B": "All existing iterators, pointers, and references into the vector are invalidated",
            "C": "The program throws a std::bad_alloc exception",
            "D": "The vector converts to an std::list"
        },
        "correct_answer": "B",
        "explanation": "When vector capacity is exceeded, it allocates a new larger heap buffer, moves existing elements, and frees the old buffer, invalidating all existing pointers.",
        "difficulty": "medium",
        "misconception_targets": ["Assuming vector dynamic resizing preserves memory addresses"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 6. JAVA PROGRAMMING (CS-JAVA)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "output_prediction",
        "question_text": "What will be the output of this Java code snippet?",
        "code_snippet": "String s1 = \"LearnSphere\";\nString s2 = new String(\"LearnSphere\");\nSystem.out.println((s1 == s2) + \" \" + s1.equals(s2));",
        "options": {
            "A": "true true",
            "B": "false true",
            "C": "true false",
            "D": "false false"
        },
        "correct_answer": "B",
        "explanation": "s1 references an interned string in the string pool. `new String(...)` allocates a distinct object on the heap. `s1 == s2` compares references (false), whereas `s1.equals(s2)` compares character sequences (true).",
        "difficulty": "medium",
        "misconception_targets": ["Using == instead of .equals() for Java object comparison"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "conceptual",
        "question_text": "In Java's `HashMap`, what contract must be satisfied when overriding `equals(Object o)` on custom key objects?",
        "code_snippet": "@Override\npublic boolean equals(Object o) { ... }",
        "options": {
            "A": "You must also override `hashCode()` such that if two objects are equal according to equals(), they must produce identical hashCodes",
            "B": "The class must implement the `Comparable` interface",
            "C": "All fields of the class must be marked `transient`",
            "D": "The class constructor must be declared private"
        },
        "correct_answer": "A",
        "explanation": "If equals() is overridden without hashCode(), equal keys produce different hash codes and land in different buckets, making retrieval impossible.",
        "difficulty": "medium",
        "misconception_targets": ["Overriding equals() without overriding hashCode() in Java"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 7. BACKEND ARCHITECTURE (Node, FastAPI, REST, Auth)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-NODE",
        "concept_name": "Event Loop and Non-blocking I/O",
        "question_type": "conceptual",
        "question_text": "In Node.js, which thread pool library handles asynchronous file system and DNS operations?",
        "code_snippet": "const fs = require('fs/promises');",
        "options": {
            "A": "V8 Isolates Pool",
            "B": "libuv thread pool (default 4 threads)",
            "C": "POSIX Pthreads Engine",
            "D": "Web Worker Background Process"
        },
        "correct_answer": "B",
        "explanation": "Node.js utilizes libuv to provide non-blocking asynchronous I/O. File system calls and crypto tasks are delegated to libuv's background thread pool (UV_THREADPOOL_SIZE, default 4).",
        "difficulty": "medium",
        "misconception_targets": ["Believing Node.js runs all file operations directly on V8 single thread"]
    },
    {
        "subject_code": "CS-FASTAPI",
        "concept_name": "Dependency Injection and Async Endpoints",
        "question_type": "conceptual",
        "question_text": "In FastAPI, how does declaring an endpoint as standard `def` vs `async def` affect concurrency under heavy load?",
        "code_snippet": "@app.get('/compute')\ndef sync_endpoint():\n    time.sleep(2)",
        "options": {
            "A": "FastAPI runs standard `def` endpoints inside an external worker threadpool to prevent blocking the main event loop",
            "B": "Standard `def` blocks all other incoming requests on the server entirely",
            "C": "FastAPI does not support non-async def endpoints",
            "D": "FastAPI compiles def endpoints into C++ binaries"
        },
        "correct_answer": "A",
        "explanation": "FastAPI runs synchronous `def` functions in an external AnyIO threadpool so that blocking calls don't freeze the main asyncio event loop. Conversely, blocking operations inside `async def` freeze the entire event loop.",
        "difficulty": "hard",
        "misconception_targets": ["Putting blocking time.sleep() inside async def endpoints"]
    },
    {
        "subject_code": "CS-REST",
        "concept_name": "HTTP Verbs and Idempotency",
        "question_type": "conceptual",
        "question_text": "Which of the following HTTP methods is defined as NOT idempotent according to RFC 7231?",
        "code_snippet": "GET /users/1 | PUT /users/1 | DELETE /users/1 | POST /users",
        "options": {
            "A": "GET",
            "B": "PUT",
            "C": "POST",
            "D": "DELETE"
        },
        "correct_answer": "C",
        "explanation": "An idempotent method can be called multiple times yielding the same intended system state. GET, PUT, and DELETE are idempotent. POST creates a new resource on each execution and is not idempotent.",
        "difficulty": "easy",
        "misconception_targets": ["Believing DELETE is non-idempotent because subsequent calls return 404"]
    },
    {
        "subject_code": "CS-AUTH",
        "concept_name": "JWT and Token Authentication",
        "question_type": "conceptual",
        "question_text": "Why should sensitive data like unhashed user passwords never be stored inside a JSON Web Token (JWT) payload?",
        "code_snippet": "header.payload.signature",
        "options": {
            "A": "JWT payload strings are encrypted with AES-256 by default",
            "B": "The JWT payload is only Base64Url-encoded, not encrypted; anyone with the token can decode and view its contents",
            "C": "JWT tokens expire after 5 seconds",
            "D": "JWT headers reject strings longer than 32 characters"
        },
        "correct_answer": "B",
        "explanation": "JWT signatures guarantee data integrity and authenticity, but the payload itself is plain Base64Url encoded. Anyone intercepting or inspecting the token can read all payload claims.",
        "difficulty": "medium",
        "misconception_targets": ["Confusing digital signing with payload encryption"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 8. DATABASE MANAGEMENT (SQL, MySQL, MongoDB, DBMS)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-SQL",
        "concept_name": "SQL Joins and Grouping",
        "question_type": "output_prediction",
        "question_text": "What does a `LEFT JOIN` return when rows in the left table have no matching foreign key in the right table?",
        "code_snippet": "SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id;",
        "options": {
            "A": "It excludes unmatched users from the result set",
            "B": "It includes all users, populating right table columns (`o.amount`) with `NULL`",
            "C": "It throws an integrity constraint violation",
            "D": "It replaces missing values with 0"
        },
        "correct_answer": "B",
        "explanation": "A LEFT JOIN retains all records from the left table regardless of whether a matching record exists in the right table. Missing attributes are filled with NULL.",
        "difficulty": "easy",
        "misconception_targets": ["Confusing INNER JOIN and LEFT OUTER JOIN semantics"]
    },
    {
        "subject_code": "CS-DBMS",
        "concept_name": "ACID Properties and Transactions",
        "question_type": "conceptual",
        "question_text": "Which ACID property guarantees that all operations within a database transaction either succeed completely or are completely rolled back?",
        "code_snippet": "BEGIN TRANSACTION;\nUPDATE accounts SET bal = bal - 100;\nUPDATE accounts SET bal = bal + 100;\nCOMMIT;",
        "options": {
            "A": "Atomicity",
            "B": "Consistency",
            "C": "Isolation",
            "D": "Durability"
        },
        "correct_answer": "A",
        "explanation": "Atomicity ensures the transaction is treated as an indivisible unit of work: 'all or nothing'. If a crash occurs midway, partial changes are rolled back.",
        "difficulty": "easy",
        "misconception_targets": ["Confusing Atomicity with Durability or Consistency"]
    },
    {
        "subject_code": "CS-DBDESIGN",
        "concept_name": "Database Normalization (1NF to BCNF)",
        "question_type": "conceptual",
        "question_text": "What condition must be eliminated to advance a relational schema from Second Normal Form (2NF) to Third Normal Form (3NF)?",
        "code_snippet": "Student -> Department -> Department_Dean",
        "options": {
            "A": "Partial functional dependencies on candidate keys",
            "B": "Transitive functional dependencies between non-prime attributes",
            "C": "Multi-valued attributes",
            "D": "Foreign key relationships"
        },
        "correct_answer": "B",
        "explanation": "2NF eliminates partial dependencies (dependencies on part of a composite key). 3NF eliminates transitive dependencies (X -> Y -> Z where Z is determined by non-key Y).",
        "difficulty": "medium",
        "misconception_targets": ["Confusing 2NF partial key dependencies with 3NF transitive dependencies"]
    },
    {
        "subject_code": "CS-MONGO",
        "concept_name": "Document Modeling and Aggregation",
        "question_type": "conceptual",
        "question_text": "In MongoDB, what aggregation pipeline stage is used to deconstruct an array field from input documents to output a document for each element?",
        "code_snippet": "db.orders.aggregate([ { $unwind: \"$items\" } ])",
        "options": {
            "A": "$group",
            "B": "$unwind",
            "C": "$project",
            "D": "$lookup"
        },
        "correct_answer": "B",
        "explanation": "$unwind deconstructs an array field from the input documents to output a document for each element in the specified array.",
        "difficulty": "medium",
        "misconception_targets": ["Using $project instead of $unwind to flatten arrays"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 9. COMPUTER SCIENCE CORE (OS, CN, OOP)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-OS",
        "concept_name": "Process Synchronization and Deadlocks",
        "question_type": "conceptual",
        "question_text": "Which of the following is NOT one of Coffman's four necessary conditions for a system deadlock to occur?",
        "code_snippet": "P1 holds R1, waiting for R2\nP2 holds R2, waiting for R1",
        "options": {
            "A": "Mutual Exclusion",
            "B": "Hold and Wait",
            "C": "Preemptive Resource Reallocation",
            "D": "Circular Wait"
        },
        "correct_answer": "C",
        "explanation": "Coffman conditions require 'No Preemption' (resources cannot be forcibly confiscated). 'Preemptive Resource Reallocation' breaks deadlock.",
        "difficulty": "medium",
        "misconception_targets": ["Thinking preemption causes deadlocks rather than resolving them"]
    },
    {
        "subject_code": "CS-OS",
        "concept_name": "Virtual Memory and Paging",
        "question_type": "conceptual",
        "question_text": "What hardware component caches recent virtual-to-physical page table address translations to accelerate memory access?",
        "code_snippet": "Virtual Address -> [ ? ] -> Physical Address",
        "options": {
            "A": "Arithmetic Logic Unit (ALU)",
            "B": "Translation Lookaside Buffer (TLB)",
            "C": "Direct Memory Access (DMA) Controller",
            "D": "Instruction Register"
        },
        "correct_answer": "B",
        "explanation": "The TLB is a high-speed associative hardware cache inside the MMU that stores recent page table translations to avoid multi-level memory lookups.",
        "difficulty": "medium",
        "misconception_targets": ["Confusing CPU L1 instruction cache with the TLB"]
    },
    {
        "subject_code": "CS-CN",
        "concept_name": "TCP vs UDP and 3-Way Handshake",
        "question_type": "conceptual",
        "question_text": "What is the correct sequence of packet flags exchanged during a standard TCP connection establishment handshake?",
        "code_snippet": "Client ---------------> Server\nClient <--------------- Server\nClient ---------------> Server",
        "options": {
            "A": "SYN -> ACK -> SYN-ACK",
            "B": "SYN -> SYN-ACK -> ACK",
            "C": "FIN -> ACK -> FIN-ACK",
            "D": "RST -> SYN -> ACK"
        },
        "correct_answer": "B",
        "explanation": "TCP 3-way handshake sequence: 1) Client sends SYN, 2) Server responds with SYN-ACK, 3) Client acknowledges with ACK.",
        "difficulty": "easy",
        "misconception_targets": ["Confusing connection establishment (SYN) with termination (FIN)"]
    },
    {
        "subject_code": "CS-OOP",
        "concept_name": "SOLID Principles and Design Patterns",
        "question_type": "conceptual",
        "question_text": "According to the Liskov Substitution Principle (LSP), which of the following must hold true?",
        "code_snippet": "class Bird { fly() { ... } }\nclass Ostrich extends Bird { ... }",
        "options": {
            "A": "Classes must have only one reason to change",
            "B": "Objects of a superclass should be replaceable with objects of a subclass without breaking application correctness",
            "C": "Classes should be open for modification but closed for extension",
            "D": "High-level modules should depend directly on concrete low-level implementations"
        },
        "correct_answer": "B",
        "explanation": "Liskov Substitution Principle states that derived types must be completely substitutable for their base types without altering expected behavior or breaking invariants.",
        "difficulty": "medium",
        "misconception_targets": ["Modeling Ostrich as subclass of flying Bird, throwing exceptions when fly() is called"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 10. ARTIFICIAL INTELLIGENCE & MACHINE LEARNING
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-ML",
        "concept_name": "Overfitting and Regularization Techniques",
        "question_type": "conceptual",
        "question_text": "How does L1 regularization (Lasso) differ mathematically from L2 regularization (Ridge) in terms of learned weights?",
        "code_snippet": "Loss_L1 = Loss + lambda * sum(|w|)\nLoss_L2 = Loss + lambda * sum(w^2)",
        "options": {
            "A": "L1 drives non-essential weights to strictly zero, performing feature selection; L2 shrinks weights asymptotically towards zero without setting them to zero",
            "B": "L2 performs feature selection; L1 increases model variance",
            "C": "L1 is only applicable to neural networks; L2 is only for linear regression",
            "D": "L1 doubles the number of trainable parameters"
        },
        "correct_answer": "A",
        "explanation": "L1 regularization uses the diamond-shaped L1 norm constraint, which produces sparse weight vectors with coefficients set exactly to zero (acting as feature selection). L2 shrinks weights smoothly.",
        "difficulty": "hard",
        "misconception_targets": ["Assuming L1 and L2 achieve identical sparsity patterns"]
    },
    {
        "subject_code": "CS-DL",
        "concept_name": "Backpropagation and Neural Networks",
        "question_type": "conceptual",
        "question_text": "What causes the 'Vanishing Gradient Problem' during backpropagation in deep neural networks using Sigmoid activation functions?",
        "code_snippet": "sigma'(z) = sigma(z) * (1 - sigma(z))",
        "options": {
            "A": "The derivative of the sigmoid function peaks at 0.25; multiplying many numbers <= 0.25 across layers drives gradients towards zero exponentially",
            "B": "The learning rate becomes too large and explodes weights to infinity",
            "C": "Negative weights are mathematically impossible with sigmoid",
            "D": "The loss function diverges into NaN"
        },
        "correct_answer": "A",
        "explanation": "The maximum derivative of the standard sigmoid is 0.25. In deep architectures, the chain rule multiplies these tiny derivatives across layers, shrinking gradients exponentially and stalling early layers.",
        "difficulty": "hard",
        "misconception_targets": ["Confusing exploding gradients with vanishing gradients"]
    },
    {
        "subject_code": "CS-GENAI",
        "concept_name": "Transformers and Self-Attention Mechanism",
        "question_type": "conceptual",
        "question_text": "In the standard Transformer architecture, what is the computational complexity of the Self-Attention mechanism with sequence length N?",
        "code_snippet": "Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V",
        "options": {
            "A": "O(N)",
            "B": "O(N * log N)",
            "C": "O(N^2 * d)",
            "D": "O(2^N)"
        },
        "correct_answer": "C",
        "explanation": "Computing the pairwise dot-product matrix between queries Q (N x d) and keys K (N x d) requires multiplying N tokens with every other token, yielding O(N^2 * d) quadratic complexity.",
        "difficulty": "hard",
        "misconception_targets": ["Believing standard transformer attention is linear O(N) in sequence length"]
    },
    {
        "subject_code": "CS-AGENTS",
        "concept_name": "AI Agents and Reasoning Loops",
        "question_type": "conceptual",
        "question_text": "What distinguishes an autonomous AI Agent framework (such as ReAct) from standard zero-shot LLM prompt completion?",
        "code_snippet": "Thought -> Action -> Observation -> Thought -> Final Answer",
        "options": {
            "A": "Agents run on edge devices without requiring cloud computing",
            "B": "Agents execute iterative decision loops: formulating reasoning traces, invoking external tools/APIs, observing environment feedback, and adapting execution",
            "C": "Agents do not use natural language models",
            "D": "Agents cannot use Python"
        },
        "correct_answer": "B",
        "explanation": "Agentic AI combines reasoning with action loops. The agent formulates sub-goals, calls external tools/APIs, observes the output, and iteratively refines its trajectory until the goal is achieved.",
        "difficulty": "medium",
        "misconception_targets": ["Equating simple single-turn prompt response with agentic tool-use loops"]
    }
]


def get_fallback_questions(
    subject_code: Optional[str] = None,
    concept_name: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Retrieve fallback questions matching subject, concept, and difficulty filters."""
    matches = FALLBACK_QUESTIONS[:]
    if subject_code:
        matches = [q for q in matches if q.get("subject_code", "").upper() == subject_code.upper()]
    if concept_name:
        matches = [q for q in matches if concept_name.lower() in q.get("concept_name", "").lower()]
    if difficulty:
        diff_matches = [q for q in matches if q.get("difficulty", "").lower() == difficulty.lower()]
        if diff_matches:
            matches = diff_matches

    if not matches and subject_code:
        # Match any question for the subject if difficulty/concept filters were too narrow
        matches = [q for q in FALLBACK_QUESTIONS if q.get("subject_code", "").upper() == subject_code.upper()]

    if not matches:
        matches = FALLBACK_QUESTIONS[:]

    random.shuffle(matches)
    return matches[:limit]


def get_random_fallback_question(
    subject_code: Optional[str] = None,
    concept_name: Optional[str] = None,
    difficulty: str = "medium",
    exclude_texts: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Retrieve a single random fallback question avoiding recently asked texts.
    Guarantees subject-specific matching and strict non-duplication whenever unasked questions exist.
    """
    exclude = {t.strip() for t in (exclude_texts or []) if t}

    # 1. Build pool including static fallback questions
    pool = FALLBACK_QUESTIONS[:]

    # Also dynamically pull all seeded curriculum questions from DB if accessible
    try:
        import sqlite3, json
        con = sqlite3.connect("backend/learnsphere_cse.db")
        cur = con.cursor()
        query = """
            SELECT s.code, c.name, q.question_type, q.question_text,
                   q.code_snippet, q.options, q.correct_answer, q.explanation,
                   q.difficulty, q.misconception_targets
            FROM questions q
            JOIN subjects s ON s.id = q.subject_id
            JOIN concepts c ON c.id = q.concept_id
        """
        params = []
        if subject_code:
            query += " WHERE UPPER(s.code) = UPPER(?)"
            params.append(subject_code.strip())
        cur.execute(query, params)
        rows = cur.fetchall()
        con.close()
        for r in rows:
            opts = json.loads(r[5]) if isinstance(r[5], str) else (r[5] or {})
            misc = json.loads(r[9]) if isinstance(r[9], str) else (r[9] or [])
            pool.append({
                "subject_code": r[0],
                "concept_name": r[1],
                "question_type": r[2] or "mcq",
                "question_text": r[3],
                "code_snippet": r[4],
                "options": opts,
                "correct_answer": r[6] or "A",
                "explanation": r[7] or "",
                "difficulty": r[8] or "medium",
                "misconception_targets": misc,
            })
    except Exception:
        pass

    # Strictly filter pool by subject_code if provided
    if subject_code:
        subject_pool = [q for q in pool if q.get("subject_code", "").upper() == subject_code.upper()]
        if subject_pool:
            pool = subject_pool

    # 2. Filter out already attempted question texts
    unseen_pool = [q for q in pool if q.get("question_text", "").strip() not in exclude]

    if unseen_pool:
        # Prefer matching concept if available
        if concept_name:
            concept_matches = [q for q in unseen_pool if concept_name.lower() in q.get("concept_name", "").lower()]
            if concept_matches:
                # Prefer matching difficulty
                diff_matches = [q for q in concept_matches if q.get("difficulty", "").lower() == difficulty.lower()]
                if diff_matches:
                    return random.choice(diff_matches)
                return random.choice(concept_matches)

        # Prefer matching difficulty across unseen pool in this subject
        diff_matches = [q for q in unseen_pool if q.get("difficulty", "").lower() == difficulty.lower()]
        if diff_matches:
            return random.choice(diff_matches)
        return random.choice(unseen_pool)

    # 3. If all static questions for this subject have been exhausted, generate a parameterized dynamic variation
    base = random.choice(pool) if pool else {
        "subject_code": subject_code or "CS",
        "concept_name": concept_name or "Computer Science Core",
        "question_type": "conceptual",
        "question_text": "Which principle guarantees optimal performance in software architecture?",
        "code_snippet": None,
        "options": {"A": "Separation of Concerns and Modularity", "B": "Monolithic Coupling", "C": "Unchecked Recursion", "D": "Premature Optimization"},
        "correct_answer": "A",
        "explanation": "Modularity and Separation of Concerns optimize both runtime scalability and code maintainability.",
        "difficulty": difficulty,
        "misconception_targets": ["Architectural fundamentals"],
    }
    return _generate_dynamic_variant(base, exclude)


def _generate_dynamic_variant(base_question: Dict[str, Any], exclude: set) -> Dict[str, Any]:
    """Generates an algorithmic variant guaranteed not to be in exclude."""
    subj = base_question.get("subject_code", "CS")
    import time
    for _ in range(50):
        salt = random.randint(1000, 9999)
        candidate = f"[{subj} Adaptive Problem #{salt}] {base_question['question_text']}"
        if candidate not in exclude:
            q_copy = dict(base_question)
            q_copy["question_text"] = candidate
            q_copy["is_ai_generated"] = True
            return q_copy

    ts = int(time.time() * 1000)
    q_copy = dict(base_question)
    q_copy["question_text"] = f"[{subj} Adaptive Problem #{ts}] {base_question['question_text']}"
    q_copy["is_ai_generated"] = True
    return q_copy
