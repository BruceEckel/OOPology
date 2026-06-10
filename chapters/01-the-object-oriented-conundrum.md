---
title: "The Object-Oriented Conundrum"
label: "Chapter One"
published: true
---

C++ was my first really interesting high-level language.
My first useful language was BASIC, my first "serious job" was assembly language and C.
I learned Pascal on my own.
In C++, though, you could make your own types with constructors and destructors and operator overloading.
I still remember hearing Bjarne Stroustrup say "user defined data types."
It felt like possibility.

But of course there was more.
There was inheritance.

I was working as a research assistant at the University of Washington School of Oceanography.
Tom Keffer had a grant to make computing easier for scientists and engineers.
The idea of overloading operators to do matrix manipulation seemed perfect.
The constructors and destructors would allocate and clean up the matrices.
Our target audience could focus on the equations and not the coding.

We were using Sun workstations (this was 1987).
To get the code for the C++ compiler we had to ask Bell labs to mail us a magnetic tape.
From the package, I think Stroustrup or Andy Koenig might have personally mailed it.
The tape contained the C source code for `cfront` which compiled C++ code into C code.

This was years before the C standard was published.
C, and the very concept of portable programs, was still catching on.
Before C, you would write programs in the assembly language for the target machine.
If another customer wanted your program on a different type of machine,
you rewrote it in the assembly language for that machine.
If the program was written in C you could hypothetically compile it with your machine's C compiler.

When C first became popular, C compilers were written in each machine's assembly language,
by people who understood that machine (typically the manufacturer).
As there was no standard, these compilers often didn't behave the same.
The compiler writers would guess at what the particular language features meant,
and would sometimes not implement features they didn't agree with.
In order for `cfront` to be useful,
it had to compile on all the target machines *and* generate code that compiled on all the target machines.
To achieve this the `cfront` team had to understand the various C compilers.
Sometimes this meant using a subset of C features, and sometimes it required a lot of `#IFDEF` preprocessing.

It was a lot of work, and it made the `cfront` source code messy and challenging to follow.
But it was a brilliant way to adapt C++ to any machine that had a C compiler.

This was a big tape, 10.5" in diameter and had to be loaded on a tape reader like the ones you see in old movies.
All we were doing is copying the files for building `cfront` onto our Sun system.
Then we did something like `make cfront`.
There might have been bugs which we had to sort out via email (The University of Washington was on the Arpanet).
But eventually there was an executable `cfront` that would take C++ code and emit C code that implemented the C++ program.

At this point I started creating example programs while going through the only book available,
Stroustrup's *The C++ Programming Language* (October 14, 1985, Addison-Wesley).
About the book Stroustrup said that he could either write an introduction, an expert's guide or a language reference.
He decided an expert's guide would best serve the target audience of early adopters.
This was a good choice, but made it challenging for beginners like me.
