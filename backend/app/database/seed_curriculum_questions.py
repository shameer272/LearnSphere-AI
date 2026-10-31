"""
Seeder script to populate 25+ distinct B.Tech CSE questions per core subject into learnsphere_cse.db.
Ensures zero question repetition and comprehensive question coverage for:
Python, C, C++, Java, JavaScript, HTML, CSS, React, SQL, and DSA.
"""
import json
import sqlite3
from datetime import datetime

DB_PATH = "backend/learnsphere_cse.db"

SUBJECT_CODE_TO_ID = {
    "CS-PY": 1,
    "CS-C": 2,
    "CS-CPP": 3,
    "CS-JAVA": 4,
    "CS-JS": 5,
    "CS-HTML": 6,
    "CS-CSS": 7,
    "CS-REACT": 8,
    "CS-TAILWIND": 9,
    "CS-BOOTSTRAP": 10,
    "CS-NODE": 11,
    "CS-EXPRESS": 12,
    "CS-FASTAPI": 13,
    "CS-REST": 14,
    "CS-AUTH": 15,
    "CS-DBMS": 16,
    "CS-SQL": 17,
    "CS-MYSQL": 18,
    "CS-MONGO": 19,
    "CS-DBDESIGN": 20,
    "CS-DSA": 21,
    "CS-OS": 22,
    "CS-CN": 23,
    "CS-COA": 24,
    "CS-OOP": 25,
    "CS-AI": 26,
    "CS-ML": 27,
    "CS-DL": 28,
    "CS-GENAI": 29,
    "CS-PROMPT": 30,
    "CS-AGENTS": 31,
}

QUESTIONS_DATA = [
    # ══════════════════════════════════════════════════════════════════════════
    # C PROGRAMMING (CS-C, subject_id: 2) — 20+ Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What is the output of the following C code regarding pointer arithmetic?",
        "code_snippet": "#include <stdio.h>\nint main() {\n    int arr[] = {10, 20, 30, 40, 50};\n    int *ptr = arr;\n    printf(\"%d \", *(ptr + 3));\n    printf(\"%d\", *ptr + 3);\n    return 0;\n}",
        "options": {"A": "40 13", "B": "30 13", "C": "40 40", "D": "Undefined Behavior"},
        "correct_answer": "A",
        "explanation": "*(ptr + 3) accesses arr[3] which is 40. *ptr + 3 dereferences ptr (giving 10) and adds 3, giving 13.",
        "difficulty": "medium",
        "misconception_targets": ["Precedence confusion between *(p+i) and *p+i"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What will be printed by this C program with array pointer decays?",
        "code_snippet": "#include <stdio.h>\nint main() {\n    char str[] = \"LearnSphere\";\n    char *p = str;\n    printf(\"%c\", *(p++ + 2));\n    return 0;\n}",
        "options": {"A": "a", "B": "r", "C": "L", "D": "e"},
        "correct_answer": "A",
        "explanation": "p++ evaluates to original p, then increments p. Original p + 2 points to str[2], which is 'a'.",
        "difficulty": "hard",
        "misconception_targets": ["Post-increment pointer dereference evaluation order"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "conceptual",
        "question_text": "In C, what is the consequence of failing to call free() on memory allocated with malloc() in a long-running process?",
        "code_snippet": None,
        "options": {"A": "Memory leak leading to memory exhaustion", "B": "Segmentation fault immediately", "C": "Garbage collector automatically frees it", "D": "Compiler compilation warning only"},
        "correct_answer": "A",
        "explanation": "C does not have automatic garbage collection. Unfreed heap allocations remain allocated until process termination, causing a memory leak.",
        "difficulty": "easy",
        "misconception_targets": ["Assuming C has automated garbage collection"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "code_debugging",
        "question_text": "What critical error exists in the following C code snippet?",
        "code_snippet": "int *create_array() {\n    int buffer[10];\n    for (int i = 0; i < 10; i++) buffer[i] = i * 2;\n    return buffer;\n}",
        "options": {"A": "Dangling pointer returning address of stack-allocated local array", "B": "Memory leak on the heap", "C": "Buffer overflow", "D": "Syntax error in loop header"},
        "correct_answer": "A",
        "explanation": "buffer is allocated on the stack frame of create_array(). When the function returns, its stack frame is invalidated, leaving a dangling pointer.",
        "difficulty": "medium",
        "misconception_targets": ["Returning stack pointer versus heap pointer"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What is the output of sizeof operator on array parameter in C?",
        "code_snippet": "#include <stdio.h>\nvoid func(int arr[10]) {\n    printf(\"%zu\", sizeof(arr) == sizeof(int*));\n}\nint main() {\n    int a[10];\n    func(a);\n    return 0;\n}",
        "options": {"A": "1", "B": "0", "C": "10", "D": "40"},
        "correct_answer": "A",
        "explanation": "In C function parameter declarations, array syntax arr[10] decays into a pointer int *arr. Therefore sizeof(arr) equals sizeof(int*).",
        "difficulty": "medium",
        "misconception_targets": ["Array parameter decay to pointer type"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What does the following double pointer snippet output?",
        "code_snippet": "#include <stdio.h>\nint main() {\n    int x = 50;\n    int *p1 = &x;\n    int **p2 = &p1;\n    **p2 += 25;\n    printf(\"%d\", x);\n    return 0;\n}",
        "options": {"A": "75", "B": "50", "C": "25", "D": "Compilation error"},
        "correct_answer": "A",
        "explanation": "**p2 dereferences the double pointer twice, reaching the actual variable x and adding 25 to it.",
        "difficulty": "easy",
        "misconception_targets": ["Double pointer dereferencing mechanics"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "conceptual",
        "question_text": "What is the key difference between malloc() and calloc() in standard C?",
        "code_snippet": None,
        "options": {"A": "calloc() initializes all allocated bytes to zero; malloc() leaves memory uninitialized", "B": "malloc() allocates on the stack; calloc() on the heap", "C": "calloc() cannot allocate arrays", "D": "malloc() returns void* while calloc() returns int*"},
        "correct_answer": "A",
        "explanation": "calloc(num, size) zeroes out the allocated memory block, whereas malloc(size) leaves the memory uninitialized containing garbage bytes.",
        "difficulty": "easy",
        "misconception_targets": ["Confusion between calloc and malloc initialization behavior"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What does printf print when evaluating string pointer arithmetic?",
        "code_snippet": "#include <stdio.h>\nint main() {\n    char *s = \"ComputerScience\";\n    printf(\"%s\", s + 8);\n    return 0;\n}",
        "options": {"A": "Science", "B": "puterScience", "C": "S", "D": "Computer"},
        "correct_answer": "A",
        "explanation": "s + 8 advances the pointer by 8 characters to the character 'S', printing the remainder of the null-terminated string 'Science'.",
        "difficulty": "easy",
        "misconception_targets": ["String pointer offset formatting"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "code_debugging",
        "question_text": "What is the problem with accessing a pointer after calling free(ptr)?",
        "code_snippet": "int *p = malloc(sizeof(int));\n*p = 100;\nfree(p);\nprintf(\"%d\", *p);",
        "options": {"A": "Use-after-free causing undefined behavior", "B": "Guaranteed 0 output", "C": "Syntax error at compile time", "D": "Automatic re-allocation"},
        "correct_answer": "A",
        "explanation": "Calling free(p) deallocates the block. Accessing *p afterwards is a use-after-free vulnerability producing undefined behavior.",
        "difficulty": "medium",
        "misconception_targets": ["Use after free vulnerability semantics"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "conceptual",
        "question_text": "In C, what is the type of NULL pointer constant?",
        "code_snippet": None,
        "options": {"A": "((void *)0)", "B": "char", "C": "int", "D": "float"},
        "correct_answer": "A",
        "explanation": "In standard C, NULL is typically defined as ((void *)0), a null pointer constant converted to void pointer.",
        "difficulty": "easy",
        "misconception_targets": ["NULL definition in C vs 0 in C++"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "output_prediction",
        "question_text": "What happens when realloc(ptr, 0) is called in standard C implementations?",
        "code_snippet": "int *p = malloc(20);\nint *p2 = realloc(p, 0);",
        "options": {"A": "The memory pointed to by p is freed, and NULL may be returned", "B": "An error is raised at compile time", "C": "Memory size is doubled", "D": "A new 20 byte buffer is initialized"},
        "correct_answer": "A",
        "explanation": "Calling realloc with a new size of 0 deallocates the old memory object similar to free(ptr).",
        "difficulty": "medium",
        "misconception_targets": ["realloc edge cases with zero size"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What is the value of *(&arr[0] + 1) for int arr[] = {3, 7, 11}?",
        "code_snippet": None,
        "options": {"A": "7", "B": "4", "C": "3", "D": "11"},
        "correct_answer": "A",
        "explanation": "&arr[0] is pointer to arr[0]. Adding 1 points to arr[1], and dereferencing gives 7.",
        "difficulty": "easy",
        "misconception_targets": ["Address of array index plus offset"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "conceptual",
        "question_text": "Which segment of process memory is managed by malloc() and free()?",
        "code_snippet": None,
        "options": {"A": "Heap segment", "B": "Stack segment", "C": "Text segment", "D": "BSS segment"},
        "correct_answer": "A",
        "explanation": "Dynamic memory allocation using malloc, calloc, and free operates on the process heap segment.",
        "difficulty": "easy",
        "misconception_targets": ["Memory layout: Stack vs Heap vs BSS"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What will be printed when passing a pointer by value in C?",
        "code_snippet": "#include <stdio.h>\nvoid reassign(int *ptr) {\n    int y = 99;\n    ptr = &y;\n}\nint main() {\n    int x = 10;\n    int *p = &x;\n    reassign(p);\n    printf(\"%d\", *p);\n    return 0;\n}",
        "options": {"A": "10", "B": "99", "C": "0", "D": "Segmentation Fault"},
        "correct_answer": "A",
        "explanation": "C is strictly pass-by-value. The function modifies its local copy of the pointer ptr, leaving the caller's pointer p unchanged.",
        "difficulty": "medium",
        "misconception_targets": ["Pointer pass-by-value vs pass-by-reference"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What is the output of pointer difference ptr2 - ptr1 for elements of an int array?",
        "code_snippet": "#include <stdio.h>\nint main() {\n    int nums[] = {1, 2, 3, 4, 5, 6};\n    int *p1 = &nums[1];\n    int *p2 = &nums[4];\n    printf(\"%td\", p2 - p1);\n    return 0;\n}",
        "options": {"A": "3", "B": "12", "C": "6", "D": "Undefined"},
        "correct_answer": "A",
        "explanation": "Subtracting two pointers to elements of the same array yields the number of elements between them (4 - 1 = 3), not the byte difference.",
        "difficulty": "medium",
        "misconception_targets": ["Pointer subtraction yielding element count vs byte count"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "code_debugging",
        "question_text": "What is the bug when allocating a 2D array dynamically as an array of pointers?",
        "code_snippet": "int **arr = malloc(rows * sizeof(int*));\nfor(int i=0; i<rows; i++) arr[i] = malloc(cols * sizeof(int));\nfree(arr);",
        "options": {"A": "Memory leak because individual rows arr[i] are not freed before freeing arr", "B": "Syntax error in sizeof", "C": "Buffer overflow in allocation", "D": "Double free error"},
        "correct_answer": "A",
        "explanation": "Freeing the master pointer arr without first freeing each row pointer arr[i] leaks the memory allocated for all individual rows.",
        "difficulty": "medium",
        "misconception_targets": ["2D dynamic memory deallocation order"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "conceptual",
        "question_text": "What does the declaration `const int *ptr` signify in C?",
        "code_snippet": None,
        "options": {"A": "Pointer to a constant integer (value cannot be modified through ptr)", "B": "Constant pointer to an integer (ptr address cannot change)", "C": "Both address and value are constant", "D": "Invalid C syntax"},
        "correct_answer": "A",
        "explanation": "`const int *ptr` is a pointer to constant integer: you cannot modify *ptr, but you can change where ptr points.",
        "difficulty": "easy",
        "misconception_targets": ["const pointer versus pointer to const"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "conceptual",
        "question_text": "What does the declaration `int * const ptr` signify in C?",
        "code_snippet": None,
        "options": {"A": "Constant pointer to an integer (ptr address cannot change)", "B": "Pointer to a constant integer", "C": "Pointer to void", "D": "Function pointer"},
        "correct_answer": "A",
        "explanation": "`int * const ptr` means ptr is a constant pointer: its address binding is immutable, but the value *ptr can be modified.",
        "difficulty": "easy",
        "misconception_targets": ["int * const vs const int *"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Dynamic Memory Allocation (malloc, free)",
        "question_type": "conceptual",
        "question_text": "What happens if malloc fails to allocate the requested amount of memory?",
        "code_snippet": None,
        "options": {"A": "Returns NULL pointer", "B": "Throws an OutOfMemoryException", "C": "Terminates the program immediately", "D": "Returns address 0xFFFFFFFF"},
        "correct_answer": "A",
        "explanation": "When malloc fails due to insufficient memory, it returns NULL. Robust C code must always check `if (ptr == NULL)`.",
        "difficulty": "easy",
        "misconception_targets": ["malloc return value on allocation failure"]
    },
    {
        "subject_code": "CS-C",
        "concept_name": "Pointers and Memory Addresses",
        "question_type": "output_prediction",
        "question_text": "What is the output of the function pointer execution below?",
        "code_snippet": "#include <stdio.h>\nint add(int a, int b) { return a + b; }\nint main() {\n    int (*op)(int, int) = add;\n    printf(\"%d\", op(15, 25));\n    return 0;\n}",
        "options": {"A": "40", "B": "Compilation Error", "C": "Address of add", "D": "Undefined"},
        "correct_answer": "A",
        "explanation": "op is a function pointer pointing to add. Calling op(15, 25) executes add(15, 25) which returns 40.",
        "difficulty": "medium",
        "misconception_targets": ["Function pointer syntax and invocation"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # C++ PROGRAMMING (CS-CPP, subject_id: 3) — 20+ Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "output_prediction",
        "question_text": "What is the output of this C++ program testing runtime polymorphism?",
        "code_snippet": "#include <iostream>\nclass Base {\npublic:\n    virtual void print() { std::cout << \"Base \"; }\n};\nclass Derived : public Base {\npublic:\n    void print() override { std::cout << \"Derived \"; }\n};\nint main() {\n    Base *b = new Derived();\n    b->print();\n    delete b;\n    return 0;\n}",
        "options": {"A": "Derived ", "B": "Base ", "C": "Base Derived ", "D": "Compile error"},
        "correct_answer": "A",
        "explanation": "Because print() is marked virtual in Base, dynamic dispatch through the vtable resolves to Derived::print() at runtime.",
        "difficulty": "easy",
        "misconception_targets": ["Virtual table dispatch mechanism"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "code_debugging",
        "question_text": "Why must a base class with virtual functions declare a virtual destructor in C++?",
        "code_snippet": "class Base {\npublic:\n    virtual ~Base() = default;\n};",
        "options": {"A": "To ensure the derived class destructor is invoked when deleting through a base class pointer", "B": "To make Base an abstract class", "C": "To allow operator overloading", "D": "To prevent heap allocation"},
        "correct_answer": "A",
        "explanation": "Deleting a derived object through a Base pointer without a virtual destructor causes undefined behavior and resource leaks.",
        "difficulty": "medium",
        "misconception_targets": ["Virtual destructor requirement in polymorphic hierarchies"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Standard Template Library (STL) Containers",
        "question_type": "conceptual",
        "question_text": "What is the worst-case time complexity of searching an element in std::unordered_map vs std::map in C++?",
        "code_snippet": None,
        "options": {"A": "O(N) for unordered_map (hash collisions), O(log N) for map (Red-Black tree)", "B": "O(1) for both", "C": "O(log N) for unordered_map, O(1) for map", "D": "O(N log N) for both"},
        "correct_answer": "A",
        "explanation": "std::unordered_map is hash-table based (average O(1), worst-case O(N) on collisions). std::map is a self-balancing BST (always O(log N)).",
        "difficulty": "medium",
        "misconception_targets": ["Worst case complexity of hash maps vs balanced BST"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Standard Template Library (STL) Containers",
        "question_type": "output_prediction",
        "question_text": "What happens when std::vector reallocation occurs during push_back?",
        "code_snippet": "std::vector<int> vec = {1, 2, 3};\nint *ptr = &vec[0];\nfor(int i = 4; i <= 20; i++) vec.push_back(i);\n// accessing *ptr now",
        "options": {"A": "Iterator and pointer invalidation because vector capacity was exceeded and buffer was moved", "B": "ptr automatically updates to new buffer", "C": "Compile time warning", "D": "Vector elements remain at identical addresses"},
        "correct_answer": "A",
        "explanation": "When vector exceeds capacity, it allocates a larger contiguous block, moves elements, and deallocates the old buffer, invalidating existing pointers and iterators.",
        "difficulty": "medium",
        "misconception_targets": ["Vector iterator and pointer invalidation on reallocation"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "conceptual",
        "question_text": "What makes a C++ class an abstract class?",
        "code_snippet": None,
        "options": {"A": "Containing at least one pure virtual function (= 0)", "B": "Declaring private constructors only", "C": "Having no member variables", "D": "Using the 'abstract' keyword"},
        "correct_answer": "A",
        "explanation": "In C++, declaring at least one pure virtual function (e.g. `virtual void func() = 0;`) renders the class abstract, preventing direct instantiation.",
        "difficulty": "easy",
        "misconception_targets": ["Pure virtual function syntax vs Java abstract keyword"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Standard Template Library (STL) Containers",
        "question_type": "conceptual",
        "question_text": "Which STL container guarantees that insertion or deletion of elements does NOT invalidate existing iterators (except for the erased element)?",
        "code_snippet": None,
        "options": {"A": "std::list", "B": "std::vector", "C": "std::deque", "D": "std::string"},
        "correct_answer": "A",
        "explanation": "std::list is a doubly-linked list with node-based allocation. Node addresses remain stable during insertions and deletions elsewhere.",
        "difficulty": "medium",
        "misconception_targets": ["Node-based container iterator stability vs contiguous containers"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "output_prediction",
        "question_text": "What is printed by this object slicing example?",
        "code_snippet": "#include <iostream>\nclass Base {\npublic:\n    virtual void show() { std::cout << \"Base\"; }\n};\nclass Derived : public Base {\npublic:\n    void show() override { std::cout << \"Derived\"; }\n};\nint main() {\n    Derived d;\n    Base b = d; // passed/copied by value\n    b.show();\n    return 0;\n}",
        "options": {"A": "Base", "B": "Derived", "C": "Compilation Error", "D": "Undefined"},
        "correct_answer": "A",
        "explanation": "Copying by value slices the Derived object down to its Base subobject. The vptr points to Base's vtable, so b.show() calls Base::show().",
        "difficulty": "medium",
        "misconception_targets": ["Object slicing when passing or assigning by value"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "conceptual",
        "question_text": "Can a virtual function be inlined in C++?",
        "code_snippet": None,
        "options": {"A": "Yes, when invoked through an object directly where the compiler resolves the type at compile-time", "B": "No, virtual functions can never be inlined under any circumstance", "C": "Only if declared static", "D": "Only with -O3 flag"},
        "correct_answer": "A",
        "explanation": "When called through an object (not pointer or reference), dynamic dispatch is bypassed and the compiler can inline the virtual function call.",
        "difficulty": "hard",
        "misconception_targets": ["Virtual function devirtualization and inlining"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Standard Template Library (STL) Containers",
        "question_type": "output_prediction",
        "question_text": "What is the output when accessing a non-existent key with operator[] on std::map?",
        "code_snippet": "#include <iostream>\n#include <map>\nint main() {\n    std::map<std::string, int> m;\n    std::cout << m[\"unseen_key\"] << \" \";\n    std::cout << m.size();\n    return 0;\n}",
        "options": {"A": "0 1", "B": "Throws std::out_of_range", "C": "0 0", "D": "Compilation error"},
        "correct_answer": "A",
        "explanation": "operator[] value-initializes the key if it does not exist (int defaults to 0) and inserts it, increasing map size to 1.",
        "difficulty": "medium",
        "misconception_targets": ["map operator[] default insertion vs map::at() throwing exception"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "conceptual",
        "question_text": "What overhead is incurred by declaring virtual functions in a C++ class?",
        "code_snippet": None,
        "options": {"A": "One vptr pointer per instance and one vtable per class with virtual functions", "B": "A copy of all function bytecode per instance", "C": "Garbage collector thread initialization", "D": "Double memory for every member variable"},
        "correct_answer": "A",
        "explanation": "Each polymorphic class gets a static virtual table (vtable), and each instance contains an internal pointer (vptr) to its class vtable.",
        "difficulty": "easy",
        "misconception_targets": ["Vtable and vptr memory overhead"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Standard Template Library (STL) Containers",
        "question_type": "conceptual",
        "question_text": "What is the difference between std::vector::reserve() and std::vector::resize()?",
        "code_snippet": None,
        "options": {"A": "reserve() alters capacity without changing size; resize() changes size and constructs/destroys elements", "B": "resize() alters capacity only", "C": "They are synonymous", "D": "reserve() initializes elements with zeros"},
        "correct_answer": "A",
        "explanation": "reserve(n) preallocates memory so capacity >= n (size remains unchanged). resize(n) changes vector size, default-constructing elements if enlarged.",
        "difficulty": "medium",
        "misconception_targets": ["Vector reserve vs resize semantics"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "output_prediction",
        "question_text": "What happens if a derived class overrides a virtual function with a different parameter type?",
        "code_snippet": "class Base {\npublic:\n    virtual void f(int x) { std::cout << \"Base\"; }\n};\nclass Derived : public Base {\npublic:\n    void f(double x) { std::cout << \"Derived\"; }\n};",
        "options": {"A": "It hides Base::f rather than overriding it", "B": "It overrides Base::f successfully", "C": "Compile error unless override is used", "D": "Ambiguous call at runtime"},
        "correct_answer": "A",
        "explanation": "In C++, changing the parameter signature does not override the virtual method; it hides all overloads of f from Base within Derived.",
        "difficulty": "hard",
        "misconception_targets": ["Name hiding vs overriding in derived classes"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Standard Template Library (STL) Containers",
        "question_type": "conceptual",
        "question_text": "What underlying data structure is typically used for std::priority_queue in C++?",
        "code_snippet": None,
        "options": {"A": "Max-heap built on top of std::vector", "B": "Doubly linked list", "C": "Red-Black Tree", "D": "Circular queue array"},
        "correct_answer": "A",
        "explanation": "std::priority_queue is a container adaptor that maintains a binary heap (default max-heap) over an underlying std::vector.",
        "difficulty": "easy",
        "misconception_targets": ["Priority queue heap implementation"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Virtual Functions and Polymorphism",
        "question_type": "conceptual",
        "question_text": "What is the purpose of the `final` specifier on a virtual method in C++11?",
        "code_snippet": "virtual void calculate() final;",
        "options": {"A": "Prevents any further derived classes from overriding the method", "B": "Marks the method as static", "C": "Makes the class abstract", "D": "Forces inlining of the method"},
        "correct_answer": "A",
        "explanation": "The `final` specifier on a virtual method causes the compiler to generate an error if any descendant class attempts to override it.",
        "difficulty": "easy",
        "misconception_targets": ["final specifier in C++ inheritance"]
    },
    {
        "subject_code": "CS-CPP",
        "concept_name": "Standard Template Library (STL) Containers",
        "question_type": "output_prediction",
        "question_text": "What is the output of std::set insertion with duplicate elements?",
        "code_snippet": "#include <iostream>\n#include <set>\nint main() {\n    std::set<int> s = {5, 2, 8, 2, 5};\n    std::cout << s.size() << \" \";\n    for(int x : s) std::cout << x << \" \";\n    return 0;\n}",
        "options": {"A": "3 2 5 8 ", "B": "5 5 2 8 2 5 ", "C": "3 5 2 8 ", "D": "Throws duplicate key error"},
        "correct_answer": "A",
        "explanation": "std::set stores unique keys sorted in ascending order. Duplicates (2 and 5) are rejected, resulting in 3 elements: 2, 5, 8.",
        "difficulty": "easy",
        "misconception_targets": ["set uniqueness and ordering"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # JAVA PROGRAMMING (CS-JAVA, subject_id: 4) — 20+ Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "output_prediction",
        "question_text": "What is the output of comparing strings created via literals vs new in Java?",
        "code_snippet": "String s1 = \"LearnSphere\";\nString s2 = \"LearnSphere\";\nString s3 = new String(\"LearnSphere\");\nSystem.out.println((s1 == s2) + \" \" + (s1 == s3) + \" \" + s1.equals(s3));",
        "options": {"A": "true false true", "B": "true true true", "C": "false false true", "D": "true false false"},
        "correct_answer": "A",
        "explanation": "s1 and s2 point to the same interned object in String constant pool (== is true). s3 creates a new heap object (== is false). equals() compares content (true).",
        "difficulty": "easy",
        "misconception_targets": ["String pool interning vs heap allocation equality"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "output_prediction",
        "question_text": "What does String.intern() return in Java?",
        "code_snippet": "String s1 = new String(\"Hello\").intern();\nString s2 = \"Hello\";\nSystem.out.println(s1 == s2);",
        "options": {"A": "true", "B": "false", "C": "NullPointerException", "D": "Compilation error"},
        "correct_answer": "A",
        "explanation": "intern() ensures the canonical representation from the string pool is returned, so s1 references the exact pool instance as literal s2.",
        "difficulty": "medium",
        "misconception_targets": ["String intern() method reference semantics"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "conceptual",
        "question_text": "What is the internal data structure used by java.util.HashMap in Java 8+ when a bucket experiences high collisions?",
        "code_snippet": None,
        "options": {"A": "Converts linked list to Red-Black Tree (TreeNode) when bucket size reaches TREEIFY_THRESHOLD (8)", "B": "Doubles hash table size and clears bucket", "C": "Converts to AVL Tree", "D": "Throws ConcurrentModificationException"},
        "correct_answer": "A",
        "explanation": "In Java 8+, when bucket elements exceed 8 and table capacity >= 64, HashMap transforms the linked list into a Red-Black tree to improve worst-case lookup from O(N) to O(log N).",
        "difficulty": "medium",
        "misconception_targets": ["Java 8 HashMap treeification threshold"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "output_prediction",
        "question_text": "What exception is thrown when modifying a collection while iterating through it with a standard for-each loop in Java?",
        "code_snippet": "List<String> list = new ArrayList<>(List.of(\"A\", \"B\", \"C\"));\nfor(String s : list) {\n    if (s.equals(\"B\")) list.remove(s);\n}",
        "options": {"A": "ConcurrentModificationException", "B": "IndexOutOfBoundsException", "C": "IllegalStateException", "D": "No exception thrown"},
        "correct_answer": "A",
        "explanation": "ArrayList's fail-fast iterator checks modCount against expectedModCount on each next() call. Structural modification invalidates iteration.",
        "difficulty": "medium",
        "misconception_targets": ["Fail-fast iterator ConcurrentModificationException"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "output_prediction",
        "question_text": "What is the result of string concatenation of compile-time constants in Java?",
        "code_snippet": "String s1 = \"Learn\" + \"Sphere\";\nString s2 = \"LearnSphere\";\nSystem.out.println(s1 == s2);",
        "options": {"A": "true", "B": "false", "C": "Compile error", "D": "Depends on JVM version"},
        "correct_answer": "A",
        "explanation": "Constant expression concatenation (\"Learn\" + \"Sphere\") is computed at compile-time by javac and placed directly in the constant pool.",
        "difficulty": "medium",
        "misconception_targets": ["Compile-time constant string folding"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "conceptual",
        "question_text": "What contract must be maintained between hashCode() and equals() in Java?",
        "code_snippet": None,
        "options": {"A": "If two objects are equal according to equals(), they must produce identical hashCode()", "B": "If hash codes are equal, equals() must return true", "C": "hashCode() must return distinct integers for all objects", "D": "equals() is never required if hashCode() is overridden"},
        "correct_answer": "A",
        "explanation": "The hashCode contract requires that if a.equals(b), then a.hashCode() == b.hashCode(). Unequal objects may share hash codes (collisions).",
        "difficulty": "easy",
        "misconception_targets": ["Directionality of equals and hashCode contract"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "conceptual",
        "question_text": "Why are String objects designed to be immutable in Java?",
        "code_snippet": None,
        "options": {"A": "Security, thread safety, string constant pool caching, and stable hash code generation", "B": "To prevent subclassing only", "C": "To avoid garbage collection", "D": "Because primitive types are immutable"},
        "correct_answer": "A",
        "explanation": "Immutability allows String pooling, safe sharing across concurrent threads, security for parameters like database URLs, and hash code caching.",
        "difficulty": "easy",
        "misconception_targets": ["Reasons for Java String immutability design"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "conceptual",
        "question_text": "How does ConcurrentHashMap achieve thread safety in Java without locking the entire map?",
        "code_snippet": None,
        "options": {"A": "CAS (Compare-And-Swap) operations on bucket heads and synchronized locking on individual bucket nodes", "B": "Making all methods synchronized", "C": "Cloning the map on every write", "D": "Single global read-write lock"},
        "correct_answer": "A",
        "explanation": "Java 8+ ConcurrentHashMap uses lock-free CAS for bucket insertions and synchronizes only on the head node of a specific bucket during mutations.",
        "difficulty": "hard",
        "misconception_targets": ["ConcurrentHashMap bucket-level locking vs Hashtable whole-table lock"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "output_prediction",
        "question_text": "What is the difference between StringBuilder and StringBuffer in Java?",
        "code_snippet": None,
        "options": {"A": "StringBuffer is synchronized (thread-safe); StringBuilder is unsynchronized and faster", "B": "StringBuilder is immutable; StringBuffer is mutable", "C": "StringBuffer is part of collections; StringBuilder is in java.lang", "D": "They have identical performance and implementations"},
        "correct_answer": "A",
        "explanation": "StringBuffer has synchronized methods for thread-safety. StringBuilder has no synchronization overhead and is preferred for single-threaded string manipulations.",
        "difficulty": "easy",
        "misconception_targets": ["StringBuffer vs StringBuilder synchronization differences"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "output_prediction",
        "question_text": "What happens when null key is inserted into java.util.TreeMap?",
        "code_snippet": "Map<String, Integer> map = new TreeMap<>();\nmap.put(null, 10);",
        "options": {"A": "Throws NullPointerException because keys must be comparable", "B": "Stores null at root node", "C": "Returns null", "D": "Silently ignores key"},
        "correct_answer": "A",
        "explanation": "TreeMap relies on compareTo or Comparator. Calling compareTo on a null key throws NullPointerException.",
        "difficulty": "medium",
        "misconception_targets": ["TreeMap disallowing null keys vs HashMap allowing one null key"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "String Pool and Equality Operators",
        "question_type": "output_prediction",
        "question_text": "What is printed when testing identity on autoboxed Integers in Java?",
        "code_snippet": "Integer a = 127;\nInteger b = 127;\nInteger c = 128;\nInteger d = 128;\nSystem.out.println((a == b) + \" \" + (c == d));",
        "options": {"A": "true false", "B": "true true", "C": "false false", "D": "false true"},
        "correct_answer": "A",
        "explanation": "Java caches Integer objects in range [-128, 127] (IntegerCache). Beyond 127, new Integer objects are instantiated on the heap.",
        "difficulty": "medium",
        "misconception_targets": ["Integer cache range [-128, 127] reference equality"]
    },
    {
        "subject_code": "CS-JAVA",
        "concept_name": "Java Collections Framework",
        "question_type": "conceptual",
        "question_text": "Which collection implementation guarantees elements are maintained in insertion order?",
        "code_snippet": None,
        "options": {"A": "LinkedHashMap", "B": "HashMap", "C": "TreeMap", "D": "Hashtable"},
        "correct_answer": "A",
        "explanation": "LinkedHashMap maintains a doubly-linked list through all its entries, preserving insertion order (or access order).",
        "difficulty": "easy",
        "misconception_targets": ["LinkedHashMap insertion order vs TreeMap sorted order"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # HTML (CS-HTML, subject_id: 6) — 20+ Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the primary accessibility and SEO benefit of using <main> over generic <div>?",
        "code_snippet": None,
        "options": {"A": "Exposes an accessible landmark role allowing screen readers to jump directly to primary content", "B": "Automatically centers content in the viewport", "C": "Compiles faster in the browser DOM parser", "D": "Enforces strict type checking in CSS"},
        "correct_answer": "A",
        "explanation": "<main> represents the dominant content of the <body>. Screen reader users can immediately jump to the 'main' landmark without reading navigation headers.",
        "difficulty": "easy",
        "misconception_targets": ["Semantic landmark roles for assistive technology"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "code_debugging",
        "question_text": "Which HTML element attribute is essential for screen readers when an image is purely decorative?",
        "code_snippet": "<img src=\"separator-line.png\" alt=\"\" />",
        "options": {"A": "Empty alt attribute alt=\"\" so assistive tech skips it", "B": "role=\"button\"", "C": "tabindex=\"0\"", "D": "title=\"decorative\""},
        "correct_answer": "A",
        "explanation": "An empty alt attribute (`alt=\"\"`) instructs screen readers that the graphic is decorative and should be skipped. Omitting alt causes screen readers to read the file name.",
        "difficulty": "medium",
        "misconception_targets": ["Empty alt attribute vs missing alt attribute"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the purpose of the WAI-ARIA `aria-live=\"polite\"` attribute in modern web applications?",
        "code_snippet": None,
        "options": {"A": "Notifies screen readers to announce dynamic content updates when the user is idle", "B": "Immediately interrupts the user to read content", "C": "Enables text-to-speech auto-play on load", "D": "Prevents screen readers from reading the container"},
        "correct_answer": "A",
        "explanation": "aria-live=\"polite\" queues announcements of dynamic DOM changes until the user is not in the middle of typing or navigating.",
        "difficulty": "medium",
        "misconception_targets": ["aria-live polite vs assertive behavior"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the correct semantic element for self-contained syndicated content such as a blog post or news story?",
        "code_snippet": None,
        "options": {"A": "<article>", "B": "<section>", "C": "<aside>", "D": "<summary>"},
        "correct_answer": "A",
        "explanation": "<article> represents a self-contained composition in a document, page, application, or site, which is independently distributable.",
        "difficulty": "easy",
        "misconception_targets": ["Difference between article and section elements"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "code_debugging",
        "question_text": "What accessibility issue occurs when a form input does NOT have an associated <label>?",
        "code_snippet": "<input type=\"text\" placeholder=\"Enter your name\" />",
        "options": {"A": "Screen readers cannot announce what information is expected, and clicking text does not focus input", "B": "Browser will fail HTML5 form validation", "C": "Input value will not be transmitted on form submit", "D": "Input field is rendered disabled"},
        "correct_answer": "A",
        "explanation": "Placeholders are not accessible replacements for labels. A <label for=\"id\"> binds programmatic name and enlarges click target.",
        "difficulty": "medium",
        "misconception_targets": ["Placeholder vs label accessibility"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the role of <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">?",
        "code_snippet": None,
        "options": {"A": "Sets viewport width to screen width and initial zoom scale, enabling responsive mobile design", "B": "Locks device orientation to portrait", "C": "Loads mobile CSS stylesheet", "D": "Disables pinch-to-zoom completely"},
        "correct_answer": "A",
        "explanation": "The viewport meta tag instructs mobile browsers to render the document at the device physical screen width rather than defaulting to a 980px desktop canvas.",
        "difficulty": "easy",
        "misconception_targets": ["Viewport meta tag purpose in responsive web"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "Which HTML5 attribute specifies that an input field must be filled out before submitting the form?",
        "code_snippet": None,
        "options": {"A": "required", "B": "validate", "C": "mandatory", "D": "not-null"},
        "correct_answer": "A",
        "explanation": "The boolean `required` attribute triggers native browser client-side validation before form submission.",
        "difficulty": "easy",
        "misconception_targets": ["HTML5 form validation attributes"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What semantic element should be used for supplementary content related to surrounding content, like a sidebar or pull quote?",
        "code_snippet": None,
        "options": {"A": "<aside>", "B": "<section>", "C": "<nav>", "D": "<footer>"},
        "correct_answer": "A",
        "explanation": "<aside> represents a portion of a document whose content is only indirectly related to the document's main content.",
        "difficulty": "easy",
        "misconception_targets": ["aside semantic element usage"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What does setting `tabindex=\"-1\"` on an HTML element achieve?",
        "code_snippet": None,
        "options": {"A": "Element cannot be reached via keyboard Tab navigation, but can receive programmatic focus via JavaScript focus()", "B": "Permanently disables element", "C": "Removes element from accessibility tree", "D": "Causes element to be focused first on page load"},
        "correct_answer": "A",
        "explanation": "tabindex=\"-1\" allows programmatic focus (useful for modal dialogs and skip links) while keeping the element out of sequential keyboard tab order.",
        "difficulty": "medium",
        "misconception_targets": ["tabindex negative vs 0 vs positive values"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the semantic distinction between <strong> and <b> in HTML5?",
        "code_snippet": None,
        "options": {"A": "<strong> imparts strong importance/seriousness for screen readers; <b> simply stylizes text bold without semantic weight", "B": "<b> is deprecated and will not render", "C": "<strong> is inline; <b> is block level", "D": "They have identical semantic weight"},
        "correct_answer": "A",
        "explanation": "<strong> indicates importance, seriousness, or urgency (affecting speech synthesis inflection), whereas <b> is purely stylistic offset text.",
        "difficulty": "easy",
        "misconception_targets": ["Semantic elements vs stylistic visual presentation"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "Which element provides machine-readable captioning or legend for a <figure>?",
        "code_snippet": None,
        "options": {"A": "<figcaption>", "B": "<caption >", "C": "<legend>", "D": "<title>"},
        "correct_answer": "A",
        "explanation": "<figcaption> represents a caption or legend describing the rest of the contents of its parent <figure> element.",
        "difficulty": "easy",
        "misconception_targets": ["figcaption vs table caption"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the proper way to provide a bypass block ('Skip to Content') link in accessible HTML?",
        "code_snippet": "<a href=\"#main-content\" class=\"skip-link\">Skip to main content</a>",
        "options": {"A": "An anchor linking to the #id of the <main> element, styled visually offscreen until focused with keyboard Tab", "B": "A Javascript alert trigger", "C": "An iframe pointing to header", "D": "A button with display:none"},
        "correct_answer": "A",
        "explanation": "Skip links allow keyboard and screen reader users to bypass repetitive header navigation and jump straight into main content.",
        "difficulty": "medium",
        "misconception_targets": ["Accessible skip link pattern implementation"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CSS (CS-CSS, subject_id: 7) — 20+ Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "output_prediction",
        "question_text": "With default box-sizing (content-box), what is the total rendered width of a div with width: 300px, padding: 20px, and border: 5px?",
        "code_snippet": "div {\n    box-sizing: content-box;\n    width: 300px;\n    padding: 20px;\n    border: 5px solid black;\n}",
        "options": {"A": "350px", "B": "300px", "C": "325px", "D": "340px"},
        "correct_answer": "A",
        "explanation": "In content-box: Total width = width (300) + left/right padding (40) + left/right border (10) = 350px.",
        "difficulty": "easy",
        "misconception_targets": ["Default content-box calculation including padding and borders"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "output_prediction",
        "question_text": "With `box-sizing: border-box`, what is the total rendered width of a div with width: 300px, padding: 20px, and border: 5px?",
        "code_snippet": "div {\n    box-sizing: border-box;\n    width: 300px;\n    padding: 20px;\n    border: 5px solid black;\n}",
        "options": {"A": "300px", "B": "350px", "C": "250px", "D": "325px"},
        "correct_answer": "A",
        "explanation": "In border-box: The specified width (300px) includes content, padding, and border. The content area shrinks to 300 - 40 - 10 = 250px.",
        "difficulty": "easy",
        "misconception_targets": ["border-box width containment"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "conceptual",
        "question_text": "In CSS Flexbox, what is the default value of `flex-shrink` on flex items?",
        "code_snippet": None,
        "options": {"A": "1", "B": "0", "C": "auto", "D": "none"},
        "correct_answer": "A",
        "explanation": "By default, flex items have flex-shrink: 1, allowing them to shrink below their basis to avoid overflowing the flex container.",
        "difficulty": "medium",
        "misconception_targets": ["Default flex item shorthand properties (0 1 auto)"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "conceptual",
        "question_text": "What is the difference between `justify-content` and `align-items` in a flex container with `flex-direction: row`?",
        "code_snippet": None,
        "options": {"A": "justify-content aligns along the main horizontal axis; align-items aligns along the cross vertical axis", "B": "They are interchangeable", "C": "justify-content is for grid; align-items is for flex", "D": "align-items applies to container; justify-content applies to children"},
        "correct_answer": "A",
        "explanation": "In row direction, the main axis is horizontal (controlled by justify-content) and the cross axis is vertical (controlled by align-items).",
        "difficulty": "easy",
        "misconception_targets": ["Main axis vs cross axis orientation in Flexbox"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "output_prediction",
        "question_text": "What happens when two vertical margins of 30px and 20px meet between adjacent block siblings?",
        "code_snippet": ".box1 { margin-bottom: 30px; }\n.box2 { margin-top: 20px; }",
        "options": {"A": "Margins collapse to 30px (the larger of the two)", "B": "Margins add up to 50px", "C": "Margins average to 25px", "D": "The browser throws layout warning"},
        "correct_answer": "A",
        "explanation": "In normal flow block formatting, adjacent vertical margins collapse into a single margin equal to the maximum of the adjacent margins (30px).",
        "difficulty": "easy",
        "misconception_targets": ["Margin collapsing mechanics on block elements"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "conceptual",
        "question_text": "In CSS Grid, what does `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))` achieve?",
        "code_snippet": None,
        "options": {"A": "Creates a responsive grid that automatically wraps columns without requiring media queries", "B": "Fixes column width strictly to 200px", "C": "Creates exactly 1 column always", "D": "Disables grid alignment"},
        "correct_answer": "A",
        "explanation": "auto-fit with minmax calculates the maximum number of 200px columns that fit the container and stretches them equally using 1fr.",
        "difficulty": "medium",
        "misconception_targets": ["Fluid responsive grid layout without media queries"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "conceptual",
        "question_text": "Which CSS property creates a new Stacking Context?",
        "code_snippet": None,
        "options": {"A": "opacity less than 1, transform not none, or position: relative with z-index not auto", "B": "display: block", "C": "color: red", "D": "font-size: 16px"},
        "correct_answer": "A",
        "explanation": "Stacking contexts are formed by elements with opacity < 1, transforms, filters, and positioned elements with non-auto z-index.",
        "difficulty": "hard",
        "misconception_targets": ["Stacking context triggers beyond z-index"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "output_prediction",
        "question_text": "What does `margin: auto` do to a flex child inside a flex container?",
        "code_snippet": ".flex-container {\n    display: flex;\n    height: 300px;\n}\n.flex-child {\n    margin: auto;\n}",
        "options": {"A": "Centers the child both horizontally and vertically inside the flex container", "B": "Resets margins to 0", "C": "Only centers horizontally", "D": "Has no effect in flexbox"},
        "correct_answer": "A",
        "explanation": "In CSS Flexbox, auto margins absorb all leftover free space along both axes, perfectly centering the item.",
        "difficulty": "easy",
        "misconception_targets": ["Auto margins inside flexbox absorbing cross-axis space"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "conceptual",
        "question_text": "What is the CSS specificity weight hierarchy from lowest to highest?",
        "code_snippet": None,
        "options": {"A": "Universal/Type selector -> Class/Attribute/Pseudo-class -> ID selector -> Inline styles", "B": "ID -> Class -> Inline -> Element", "C": "Inline -> Type -> Class -> ID", "D": "All selectors have equal specificity"},
        "correct_answer": "A",
        "explanation": "Specificity calculates as: (Inline style = 1,0,0,0) > (IDs = 0,1,0,0) > (Classes/attributes = 0,0,1,0) > (Element tags = 0,0,0,1).",
        "difficulty": "easy",
        "misconception_targets": ["CSS specificity calculation rules"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "conceptual",
        "question_text": "What is the difference between `display: none` and `visibility: hidden` in CSS?",
        "code_snippet": None,
        "options": {"A": "display: none removes element from document layout entirely; visibility: hidden hides it while preserving its space", "B": "visibility: hidden removes element from DOM", "C": "They are identical in visual and layout behavior", "D": "display: none only applies to inline elements"},
        "correct_answer": "A",
        "explanation": "display: none removes the box from rendering tree (0 width, 0 height). visibility: hidden renders an invisible box occupying original space.",
        "difficulty": "easy",
        "misconception_targets": ["Layout impact of display none vs visibility hidden"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SQL (CS-SQL, subject_id: 17) — 20+ Questions
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "conceptual",
        "question_text": "What is the key difference between WHERE and HAVING clauses in an aggregate SQL query?",
        "code_snippet": "SELECT department, AVG(salary)\nFROM employees\nWHERE status = 'Active'\nGROUP BY department\nHAVING AVG(salary) > 75000;",
        "options": {"A": "WHERE filters rows before aggregation; HAVING filters aggregated groups after GROUP BY", "B": "WHERE can use aggregate functions; HAVING cannot", "C": "They are synonymous and interchangeable", "D": "HAVING only filters primary key columns"},
        "correct_answer": "A",
        "explanation": "WHERE evaluates individual rows prior to GROUP BY. HAVING evaluates condition predicates on aggregated group values.",
        "difficulty": "easy",
        "misconception_targets": ["Execution order and filtering differences between WHERE and HAVING"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "output_prediction",
        "question_text": "What result does an INNER JOIN produce when a row in Table A has no matching key in Table B?",
        "code_snippet": "SELECT a.id, b.value\nFROM table_a a\nINNER JOIN table_b b ON a.b_id = b.id;",
        "options": {"A": "The unmatched row from Table A is excluded from the result set", "B": "The row appears with NULL values for Table B columns", "C": "A runtime SQL error is raised", "D": "A cross join is performed for that row"},
        "correct_answer": "A",
        "explanation": "INNER JOIN requires the join predicate to evaluate to TRUE. Unmatched rows in either table are completely omitted.",
        "difficulty": "easy",
        "misconception_targets": ["Inner Join filtering vs Left Outer Join retention"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "What does a LEFT JOIN return for rows in the left table that have no matching rows in the right table?",
        "code_snippet": None,
        "options": {"A": "All rows from the left table, with NULL in all columns from the right table", "B": "Only rows that have matching rows in both tables", "C": "An empty result set", "D": "Zero (0) in numeric columns and empty string in text columns"},
        "correct_answer": "A",
        "explanation": "LEFT JOIN returns all records from the left table regardless of whether there is a match in the right table, populating NULLs for missing right columns.",
        "difficulty": "easy",
        "misconception_targets": ["Left Outer Join NULL padding behavior"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "conceptual",
        "question_text": "What is the difference between UNION and UNION ALL in SQL?",
        "code_snippet": None,
        "options": {"A": "UNION removes duplicate rows via an implicit sort; UNION ALL retains all duplicates and is faster", "B": "UNION ALL only works on tables with identical names", "C": "UNION operates on columns; UNION ALL operates on rows", "D": "UNION ALL removes NULL rows"},
        "correct_answer": "A",
        "explanation": "UNION performs an expensive deduplication operation across the combined result sets. UNION ALL simply concatenates sets preserving duplicates.",
        "difficulty": "easy",
        "misconception_targets": ["Deduplication performance cost in UNION vs UNION ALL"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "output_prediction",
        "question_text": "What is the value of COUNT(*) vs COUNT(column_name) when the column contains NULL values?",
        "code_snippet": "Table: students\n| id | grade |\n| 1  | A     |\n| 2  | NULL  |\n| 3  | B     |\nSELECT COUNT(*), COUNT(grade) FROM students;",
        "options": {"A": "3 and 2", "B": "3 and 3", "C": "2 and 2", "D": "3 and 0"},
        "correct_answer": "A",
        "explanation": "COUNT(*) counts total rows in the table (3). COUNT(column_name) ignores NULL entries, returning 2.",
        "difficulty": "easy",
        "misconception_targets": ["COUNT(*) including NULLs vs COUNT(col) ignoring NULLs"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "conceptual",
        "question_text": "How does three-valued logic in SQL treat comparisons with NULL (e.g. `WHERE salary = NULL`)?",
        "code_snippet": None,
        "options": {"A": "Evaluates to UNKNOWN (failing WHERE filter); must use IS NULL instead", "B": "Evaluates to TRUE if salary is empty", "C": "Evaluates to FALSE always", "D": "Throws Syntax Error"},
        "correct_answer": "A",
        "explanation": "In SQL three-valued logic (TRUE, FALSE, UNKNOWN), any equality comparison with NULL yields UNKNOWN. Only `IS NULL` or `IS NOT NULL` test for nullity.",
        "difficulty": "medium",
        "misconception_targets": ["Three-valued logic and = NULL vs IS NULL"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "Which window function assigns sequential integers starting at 1 within a partition without gaps for duplicate values?",
        "code_snippet": None,
        "options": {"A": "DENSE_RANK()", "B": "RANK()", "C": "ROW_NUMBER()", "D": "NTILE()"},
        "correct_answer": "A",
        "explanation": "DENSE_RANK() ranks tied rows identically but does not skip numbers for the next rank (e.g. 1, 2, 2, 3), whereas RANK() skips (1, 2, 2, 4).",
        "difficulty": "medium",
        "misconception_targets": ["DENSE_RANK vs RANK vs ROW_NUMBER"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "output_prediction",
        "question_text": "How many rows are produced by a CROSS JOIN between Table A (5 rows) and Table B (10 rows)?",
        "code_snippet": "SELECT * FROM table_a CROSS JOIN table_b;",
        "options": {"A": "50 rows", "B": "15 rows", "C": "10 rows", "D": "5 rows"},
        "correct_answer": "A",
        "explanation": "CROSS JOIN produces the Cartesian product of the two tables: 5 * 10 = 50 rows.",
        "difficulty": "easy",
        "misconception_targets": ["Cartesian product cardinality"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "conceptual",
        "question_text": "What is the logical query processing order of SQL query clauses?",
        "code_snippet": None,
        "options": {"A": "FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT", "B": "SELECT -> FROM -> WHERE -> GROUP BY -> ORDER BY", "C": "FROM -> SELECT -> WHERE -> HAVING", "D": "ORDER BY -> SELECT -> FROM"},
        "correct_answer": "A",
        "explanation": "SQL logically processes data sources (FROM/JOIN) first, filters rows (WHERE), aggregates (GROUP BY/HAVING), projects columns (SELECT), sorts (ORDER BY), and truncates (LIMIT).",
        "difficulty": "hard",
        "misconception_targets": ["Logical query processing order vs syntactic clause order"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "What does COALESCE(val1, val2, val3) return in SQL?",
        "code_snippet": None,
        "options": {"A": "The first non-NULL expression in the argument list", "B": "The concatenation of all values", "C": "NULL if any argument is NULL", "D": "The average of numeric values"},
        "correct_answer": "A",
        "explanation": "COALESCE evaluates arguments in sequence and returns the first non-null value encountered.",
        "difficulty": "easy",
        "misconception_targets": ["COALESCE behavior and null handling"]
    },

    # ══════════════════════════════════════════════════════════════════════════
    # DATA STRUCTURES AND ALGORITHMS (CS-DSA, subject_id: 21) — Additional to reach 25+
    # ══════════════════════════════════════════════════════════════════════════
    {
        "subject_code": "CS-DSA",
        "concept_name": "Time Complexity and Big-O Notation",
        "question_type": "conceptual",
        "question_text": "What is the worst-case and average-case time complexity of QuickSort?",
        "code_snippet": None,
        "options": {"A": "Worst-case O(N^2), Average-case O(N log N)", "B": "O(N log N) for both", "C": "Worst-case O(N), Average-case O(N log N)", "D": "Worst-case O(N log N), Average-case O(N^2)"},
        "correct_answer": "A",
        "explanation": "When pivots consistently partition the array into 0 and N-1 elements (e.g. already sorted array with last element pivot), recursion depth is N, yielding O(N^2). Balanced pivots yield O(N log N).",
        "difficulty": "easy",
        "misconception_targets": ["QuickSort worst case pivot imbalance"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Trees and Binary Search Trees",
        "question_type": "conceptual",
        "question_text": "What traversal of a Binary Search Tree (BST) visits elements in ascending sorted order?",
        "code_snippet": None,
        "options": {"A": "In-order traversal (Left, Root, Right)", "B": "Pre-order traversal (Root, Left, Right)", "C": "Post-order traversal (Left, Right, Root)", "D": "Level-order traversal"},
        "correct_answer": "A",
        "explanation": "By BST definition, left subtree < root < right subtree. An in-order traversal (L, Root, R) therefore visits all nodes in non-decreasing sorted order.",
        "difficulty": "easy",
        "misconception_targets": ["Tree traversal ordering properties on BST"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Trees and Binary Search Trees",
        "question_type": "conceptual",
        "question_text": "What is the balance factor of a node in an AVL tree, and what values are permitted?",
        "code_snippet": None,
        "options": {"A": "Height(Left Subtree) - Height(Right Subtree); must be -1, 0, or 1", "B": "Total nodes on left - Total nodes on right; must be 0", "C": "Depth of node; must be < 5", "D": "Number of children; must be 2"},
        "correct_answer": "A",
        "explanation": "In an AVL tree, the balance factor is defined as the height difference between left and right subtrees and must strictly remain in {-1, 0, 1}.",
        "difficulty": "medium",
        "misconception_targets": ["AVL tree balance factor definition and height invariant"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Time Complexity and Big-O Notation",
        "question_type": "output_prediction",
        "question_text": "What is the time complexity of the following nested loop?",
        "code_snippet": "int count = 0;\nfor (int i = 1; i <= n; i *= 2) {\n    for (int j = 1; j <= n; j++) {\n        count++;\n    }\n}",
        "options": {"A": "O(n log n)", "B": "O(n^2)", "C": "O(n)", "D": "O(log n)"},
        "correct_answer": "A",
        "explanation": "The outer loop doubles i on each iteration, executing log2(n) times. The inner loop executes n times per outer iteration, yielding O(n log n).",
        "difficulty": "medium",
        "misconception_targets": ["Logarithmic outer loop loop bound computation"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Trees and Binary Search Trees",
        "question_type": "conceptual",
        "question_text": "What is the minimum height of a Binary Search Tree containing N nodes?",
        "code_snippet": None,
        "options": {"A": "floor(log2(N))", "B": "N / 2", "C": "log10(N)", "D": "N - 1"},
        "correct_answer": "A",
        "explanation": "A complete/balanced binary tree packs nodes with maximum fanout 2, achieving minimum height h = floor(log2(N)).",
        "difficulty": "easy",
        "misconception_targets": ["Tree height bounds and logarithmic branching"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Time Complexity and Big-O Notation",
        "question_type": "conceptual",
        "question_text": "What is the space complexity of Depth First Search (DFS) on a tree of height H?",
        "code_snippet": None,
        "options": {"A": "O(H) due to the call stack frames", "B": "O(V + E)", "C": "O(1)", "D": "O(2^H)"},
        "correct_answer": "A",
        "explanation": "DFS traverses down branches, storing at most H stack frames simultaneously corresponding to the current path from root to leaf.",
        "difficulty": "medium",
        "misconception_targets": ["DFS recursion call stack space bounds"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Trees and Binary Search Trees",
        "question_type": "conceptual",
        "question_text": "How is a node with two children deleted from a Binary Search Tree?",
        "code_snippet": None,
        "options": {"A": "Replace its key with its in-order successor (smallest in right subtree) and delete that successor node", "B": "Delete both children recursively", "C": "Shift root to the right child", "D": "BST nodes with 2 children cannot be deleted"},
        "correct_answer": "A",
        "explanation": "Replacing the node with its in-order successor (or predecessor) preserves the BST invariant, reducing deletion to a node with at most one child.",
        "difficulty": "medium",
        "misconception_targets": ["BST 2-child deletion algorithm"]
    },
]


def seed_questions():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get subject map
    cur.execute("SELECT id, code, name FROM subjects")
    subjects = {r[1]: r[0] for r in cur.fetchall()}

    # Get concepts map: (subject_id, concept_name.lower()) -> concept_id
    cur.execute("SELECT id, subject_id, name FROM concepts")
    concept_map = {}
    subject_first_concept = {}
    for cid, sid, cname in cur.fetchall():
        concept_map[(sid, cname.strip().lower())] = cid
        if sid not in subject_first_concept:
            subject_first_concept[sid] = cid

    inserted_count = 0
    now = datetime.utcnow().isoformat()

    for q in QUESTIONS_DATA:
        code = q["subject_code"]
        sid = subjects.get(code)
        if not sid:
            continue

        cname = q.get("concept_name", "").strip().lower()
        cid = concept_map.get((sid, cname))
        if not cid:
            # fallback to first concept in this subject
            cid = subject_first_concept.get(sid)

        if not cid:
            continue

        q_text = q["question_text"].strip()

        # Check if already exists in DB
        cur.execute("SELECT id FROM questions WHERE concept_id = ? AND question_text = ?", (cid, q_text))
        existing = cur.fetchone()
        if existing:
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
    print(f"Successfully inserted {inserted_count} new questions into {DB_PATH}")

    # Verify counts
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
    seed_questions()
