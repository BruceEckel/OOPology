---
title: "The Object-Oriented Conundrum"
label: "Chapter One"
published: true
---

C++ was my first really interesting high-level language.
My first useful language was BASIC, my first "serious job" was assembly language and C.
I learned Pascal on my own.
In C++, though, you could make your own types that had constructors and destructors and operator overloading.
I still remember hearing Bjarne Stroustrup say "user defined data types."
It felt like possibility.

But of course there was more.
There was inheritance.

In 1987 I was working as a research assistant at the University of Washington School of Oceanography.
Tom Keffer had a grant to make computing easier for scientists and engineers.
The idea of overloading operators to do matrix manipulation seemed perfect.
The constructors and destructors would allocate and clean up the matrices.
Our target audience could focus on the equations and not the coding.

To get the code for the C++ compiler we had to ask Bell labs to mail us a magnetic tape.
From the package, I think Stroustrup or Andy Koenig might have personally mailed it.
The tape contained the C source code for `cfront` which compiled C++ code into C code.

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
Modern programmers are more comfortable learning new languages,
but back then many programmers had just begrudgingly made the change from assembly to C
and were quite resistant to learning a language that had higher-level concepts.
C++ provided a more comfortable transition than some of the alternatives available at the time,
and that is probably the biggest reason for its success.
In addition, C++ could immediately access C libraries and projects,
so that work could be utilized without rewriting it.

Backwards compatibility with C had a significant impact on C++.
A programmer familiar with other languages and encountering C++ for the first time
often has a violent reaction to the complexity of some of the features.
These can seem needlessly complicated and even stupid to someone who isn't making the C-to-C++ transition.
Backwards compatibility with C is no longer a particular benefit,
but the complexity of the features that enable C compatibility is still impacting C++ programmers.

A particular impact comes from the fact that C has no automatic memory management.
To dynamically allocate memory, the programmer must call the library function `malloc()`,
and then remember to call `free()` when that memory is no longer needed.
Sometimes a function would do this itself,
and other times it might require the caller to perform memory management.
Some functions could be effortlessly called,
and others required the programmer to know that they were responsible for memory management.
For assembly programmers who had written their own memory management code,
`malloc()` and `free()` were great timesavers.
For programmers who hadn't started in assembly, they were confusing.

Memory managment was a significant issue with operator overloading.
Operator overloading seemed like a straightforward function definition except that the function name was an operator (indeed, in languages with automatic memory management that's how it works).
