---
title: "C++"
label: "Chapter Two"
published: true
---

C++ was my first really interesting high-level language.
My first useful language was BASIC, my first "serious job" was assembly language and C.
I learned Pascal on my own.
In C++, though, you could make your own types that had constructors and destructors and operator overloading.
I still remember hearing Bjarne Stroustrup say "user defined data types."
It felt like possibility.

To get the code for the C++ compiler we had to ask Bell labs to mail us a magnetic tape.
From the package, I think Stroustrup or Andy Koenig might have personally mailed it.
The tape contained the C source code for `cfront` which compiled C++ code into C code.

## "Portable Assembly"

This was years before the C standard was published.
C, and the very concept of portable programs, was still catching on.
Before C, you would write programs in the assembly language for the target machine.
If another customer wanted your program on a different type of machine,
you rewrote it in the assembly language for that machine.
If the program was written in C you could hypothetically compile it with your machine's C compiler.

C was often called "portable assembly language."
It generated the assembly that you might write by hand, and it automated many common, tedious, and easily confused tasks.
One of my early uses for C was to generate assembly for function definitions and calls,
which I could then reproduce for a machine that didn't have a C compiler.

When C first became popular, C compilers were written in each machine's assembly language,
by people who understood that machine (typically the manufacturer).
As there was no standard, these compilers often didn't behave the same.
The compiler writers would guess at what the particular language features meant,
and would sometimes not implement features they didn't agree with.
In order for `cfront` to be useful,
it had to compile on all the target machines *and* generate code that compiled on all the target machines.

The `cfront` team had to adapt to the various C compilers.
Sometimes this meant using a subset of C features, and sometimes it required a lot of `#IFDEF` preprocessing.
This made the `cfront` source code messy and challenging to follow.
But it was a brilliant way to adapt C++ to any machine that had a C compiler.

We were using Sun workstations, high-end machines in 1987.
The tape was 10.5" in diameter and had to be loaded on a tape reader like the ones you see in old movies.
All we were doing is copying the files to build `cfront` onto our Sun system.
We ran `make cfront`.
There might have been bugs which we had to sort out via email (The University of Washington was on the Arpanet).
But eventually there was an executable `cfront` that would take C++ code and emit C code that implemented the C++ program.

## Learning C++ in the Stone Age

To learn C++ I started creating example programs while going through the only book available,
Stroustrup's *The C++ Programming Language* (October 14, 1985, Addison-Wesley).
Stroustrup said that he could either write an introduction,
an expert's guide or a language reference.
He decided an expert's guide would best serve the target audience of early adopters.
This was a good choice, but made it challenging for beginners like me.

The brilliance of C++ was that it adapted to its current environment:
it was a superset of C, so it could compile any standard C program.
Thus, a C programmer could start using C++ right away,
and learn C++ features at their convenience.
Modern programmers are comfortable learning new languages,
but back then many programmers had only begrudgingly made the change from assembly to C
and were quite resistant to learning a language that had higher-level concepts.
C++ provided a more comfortable transition than some of the alternatives available at the time,
and that is probably the biggest reason for its success.
In addition, C++ could immediately access C libraries and projects,
so that work could be utilized without rewriting it.

C compatibility significantly impacted C++.
A programmer familiar with other languages and encountering C++ for the first time
often has a violent reaction to the complexity of some features.
These can seem needlessly complicated and even stupid to someone who isn't making the C-to-C++ transition.
Today, backwards compatibility with C is no longer a benefit.
The complexity of the features that enable C compatibility still impacts C++ programmers.

C has no automatic memory management, which puts a burden on the programmer.
To dynamically allocate memory, the programmer must call the library function `malloc()`,
and then remember to call `free()` when that memory is no longer needed.
Sometimes a function does this itself,
and other times it requires the caller to perform memory management.
Some functions could be effortlessly called,
and others required the programmer to know that they were responsible for memory management.
For assembly programmers who had written their own memory management code,
`malloc()` and `free()` were great timesavers.
For programmers who hadn't started in assembly, they were confusing.

C++ offered improved memory management using constructors, destructors, `new` and `delete`.
In C, if you want to create an object-like entity,
you allocate the storage, then call a function to initialize that storage.
When you're done with that storage, you must release it by calling `free()`:

```C
// memory_management.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct point_t {
    double x;
    double y;
    char label[32];
} Point;

Point* Point_new(double x, double y, const char* label) {
    Point* p = malloc(sizeof(Point));
    if (!p) {
        fprintf(stderr, "malloc failed\n");
        return NULL;
    }
    p->x = x;
    p->y = y;
    strncpy(p->label, label, sizeof(p->label) - 1);
    p->label[sizeof(p->label) - 1] = '\0';
    return p;
}

void Point_print(const Point* p) {
    printf("Point '%s': (%.2f, %.2f)\n", p->label, p->x, p->y);
}

int main(void) {
    Point* p = Point_new(3.14, 2.71, "My Label");
    if (!p) return 1;
    Point_print(p);
    // free(p);  // No consequences in main()
    return 0;
}
```

Note the definition of `Point`. In C, to refer to `struct Point` you had to spell it out every time.
Just defining `struct Point` did not make something called `Point`.
The `typedef` creates a `Point` that aliases to `struct Point` so we don't need all the extra `struct` keywords.

In C, just as in assembly, the programmer is responsible for every byte of memory.
You must know exactly how everything works, and if you forget (or you haven't learned yet),
you'll forget to release memory and cause leaks.
This example shows a particular pitfall:
if you test using `main()` you won't find out whether you've forgotten to release memory,
because `main()` will, in effect, clean everything up when the program terminates.
Thus, if you don't call `free(p)` in `main()`, there are no consequences.

Because it seems to work, you later turn that `main()` into a function.
Now every time you call that function it allocates a `Point` on the heap that it never releases.
If you run that program long enough these leaks might fill up the heap, stopping the program with a heap overflow.
But initially the program might not work,
and it could be years before some condition changes so the program starts crashing.
The poor programmer that must fix this crash has no idea where to start looking.

Here's another situation that shows the scaling limitations of C
(Scaling problems limit system size and complexity).
`Point_new` uses `strncpy` which has surprising behavior.
`n` is the third argument of `strncpy`: the maximum number of characters to copy.
If the source string is shorter than `n`, the destination is padded with null bytes.
If the source string is equal to or longer than `n`, no null terminator is written.
As shown, the programmer must explicitly add a null terminator for the cases where the source string
is longer that the destination storage.
Because the source string may not be longer,
it's possible that you (again) don't discover the problem until much later.

## C++ as "A Better C"

Translating the example into C++ shows numerous benefits:

```cpp
// memory_management.cpp
#include <iostream>
#include <string>

struct Point {
    double x;
    double y;
    std::string label;

    Point(double x, double y, std::string label)
        : x(x), y(y), label(std::move(label)) {}

    void print() const {
        std::cout << "Point '" << label << "': ("
                  << x << ", " << y << ")\n";
    }
};

int main() {
    // Heap allocated - must manage lifetime manually
    Point* p = new Point(3.14, 2.71, "Point p on heap");
    p->print();
    delete p;

    // Stack allocated - destroyed automatically when main() exits
    Point p2(2.71, 3.14, "Point p2 on stack");
    p2.print();
}
```

When a structure is as simple as `Point` it is recommended to use `struct` rather than `class`.
Both keywords produce a scoped namespace for `Point`, with a constructor and a member function `print()`.

All the initialization happens in the constructor initializer list.
`std::move` ensures proper initialization of `label` without worrying about potentially losing the string terminator.
`print()` is a function that is explicitly attached to `Point`.

The `new` keyword both allocates storage and calls the constructor for `Point`.
You must still remember to call `delete` but it can call a destructor to perform cleanup before it releases the storage.

Note that with stack-based objects you don't call `new` and `delete` because these objects have statically-determined lifetimes.
The compiler allocates storage and calls `new` and `delete` for you.
The ideal C++ program allocates all objects on the stack,
and any heap-based objects are created and destroyed by the stack objects.
This way, the application programmer doesn't worry about object lifetime.

## Operator Overloading

Memory managment was a significant issue with operator overloading.
Operator overloading seemed like a straightforward function definition except that the function name was an operator (indeed, in languages with automatic memory management that's how it works).

## The Puzzle of Dynamic Binding

## The Benefits of C++

In the end, C++ moved us *towards* high-level languages by wrapping the portable-assembly nature of C with some beneficial concepts.
But C++ also had to be backwards compatible with C, so we could never fully escape the rawness of C.
We had to juggle these new object-oriented concepts while still managing the low-level details.
This turned out to be a lot to ask.

I first heard the maxim "all computer science problems can be solved with another level of abstraction"
from Andrew Koenig.
It contains a certain tongue-in-cheek irony, suggesting that abstraction is the tool we reflexively grab.
Sometimes the abstraction doesn't work out: it hides something important or produces questionable benefits.
One group at Sun Microsystems decided that C++ was too confusing and difficult.
They decided a new level of abstraction was needed, one that would solve the problems they saw in C++.
But before we can understand Java, we must first explore the (conflicting) origins of object-oriented programming.
