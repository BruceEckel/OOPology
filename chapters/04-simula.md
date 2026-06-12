---
title: "Simula"
label: "Chapter Four"
published: true
---

Every word we use to talk about objects came from a language built to simulate the world.

Class, object, subclass, inheritance, virtual method, instance.
This entire vocabulary arrived nearly complete in a single language.
It was designed in Oslo in the 1960s by Ole-Johan Dahl and Kristen Nygaard.
They did not set out to invent object-oriented programming.
They set out to write simulations.
OOP emerged from the attempt.
The name says it: *Simula*, the simulation language.

The first object-oriented language was a simulation language.
It was also statically typed.
Both facts shaped everything that followed.
The tools we still reach for were built to describe one kind of thing.
That thing is a world of interacting entities, sorted into a clean taxonomy.
When your problem really is such a world, the tools fit beautifully.
When it isn't, you question the value of OOP.

## Nygaard's Problem

Kristen Nygaard was an operations researcher.
Before he designed languages, he built Monte Carlo simulations of physical systems.
He modeled the flow of ships through a port, customers through a queue, jobs through a factory.
These are *discrete-event simulations*.
You model a system as a collection of distinct entities.
Each entity has its own state and its own rules.
Then you let simulated time advance while they interact.

The difficulty was never the arithmetic.
The difficulty was description.
ALGOL and FORTRAN gave you procedures and arrays.
But a port full of ships is not naturally a procedure or an array.
It is a population of things.
Each one is like the others in kind, yet distinct in identity and state.
This tanker and that tanker are both ships.
They share behavior.
They differ in where they are and what they carry.
Nygaard needed to say "a ship" once, as a kind.
Then he needed to create as many individual ships as the simulation required.
Each one had to remember its own situation.

That is the definition of a class and its instances.
The class is the kind.
The objects are the individuals.
Dahl was the more rigorous language designer of the pair.
He gave Nygaard's modeling a precise form on top of ALGOL 60.
Simula I appeared in the mid-1960s as a simulation tool.
Simula 67 generalized the machinery into a full programming language.
By 1967 every essential idea of class-based OOP was in place.
This was decades before most of the industry noticed.

## Simulation Shaped the Design

It is worth seeing exactly how the simulation goal produced the features we now treat as universal.

**Objects are autonomous actors.**
In a simulation, each entity is an independent agent.
It owns its state.
It owns the procedures that act on that state.
The outside world is not supposed to reach in and meddle.
That is what encapsulation is: data bundled with its operations, internals hidden.
It is exactly what you want when each object is a self-contained participant in a larger world.
It was not invented as a software-engineering discipline.
It was invented because that is what a ship, or a customer, or a server is in a model.

**Inheritance is taxonomy.**
A simulated world comes pre-sorted.
A tanker is a kind of ship.
A ship is a kind of vessel.
A passenger car and a truck are kinds of vehicle.
Nygaard's domains were full of these "is-a" relationships.
The physical and organizational world really does sort itself into hierarchies of kinds.
Subclassing let him capture a general kind once and then specialize it.
A truck is everything a vehicle is, plus a cargo capacity and its own behavior at a loading dock.
So inheritance, in its birthplace, is a classification mechanism.
And classification is genuinely how simulation domains are structured.
This is the single most important fact in this book.
We will return to it.
Inheritance was born to model taxonomies.
It works wonderfully when the problem is a taxonomy.

**Virtual methods are the actors deciding for themselves.**
The scheduler tells "the next ship" to advance.
It should not have to know whether that ship is a tanker or a ferry.
The ship itself should know how it behaves.
So Simula introduced *virtual* procedures.
A call made through the general kind dispatches to the specific kind's behavior at runtime.
This is dynamic binding, a type of polymorphism.
Again it falls directly out of the simulation picture.
The scheduler holds a population of "ships" and lets each one act according to what it actually is.

**Coroutines are quasi-parallel.**
A discrete-event simulation is full of entities that run "at the same time."
Each ship is living its own life.
It suspends when it has nothing to do and resumes when its turn comes.
Simula let its objects behave as *coroutines*: processes that suspend and resume.
Each one carries its own place in its own story.
An object was not just a passive bundle of data and methods.
It could be an active process with a life of its own.
The OO languages that followed mostly dropped this.
They kept the class-and-inheritance half of Simula and threw away the active-process half.
We have spent the decades since reinventing it under other names: threads, generators, async/await.
We forgot that the first object was an autonomous process.
The first objects were simulated actors that all ran at once.

## Original OOP Was Statically Typed

Simula was built on ALGOL 60.
ALGOL was statically typed, so Simula was statically typed.
A variable declared to hold a `Ship` held a `Ship`.
The compiler knew the kind of every object before the program ran.
It checked the calls you made against the kind you declared.

This was not a reluctant compromise.
It fit the simulation worldview perfectly.
A simulation is a closed, known world.
Before you run a port simulation, you already know the complete cast.
There are ships, berths, tugs, cargo, the clock.
The ontology is fixed in advance, by you, as you design the model.
No genuinely new kind of thing wanders into the harbor at runtime.
When the set of kinds is known up front, you can declare those kinds up front.
Letting the compiler enforce them costs you nothing and buys you safety.
Static typing and simulation are made for each other.
Both assume a universe whose categories are settled before the action starts.

The effect of that choice was enormous.
Static typing welds an object to a contract fixed at compile time.
Through a `Ship` reference you may send only the messages `Ship` declares.
No more, no matter what the object underneath really is.
So inheritance under static typing becomes a promise.
To be a subclass is to honor the base class's interface everywhere the base class is expected.
This is the seed of the Liskov Substitution Principle (LSP) and the rigidity of inheritance.
It is the seed of the argument about whether a `Square` is a type of `Rectangle`.
None of those constraints are inherent to "objects."
They come from one decision: to know all the types in advance.
That decision was natural for a simulation language.

## The Effect on C++ and Smalltalk

Bjarne Stroustrup used Simula for his doctoral work at Cambridge.
He was simulating distributed systems.
Classes improved the structure of his programs, but Simula was too slow for the scale he needed.
So he grafted Simula's class concept onto C, the most efficient language at the time.
"C with Classes" became C++.
Stroustrup kept Simula's static typing and made it sharper.
Classes, inheritance, and virtual functions were checked at compile time, then compiled away at runtime.
The static, taxonomy-shaped OOP of Simula flowed almost directly into C++.
From C++ it flowed into Java.
From there it flowed into the mainstream idea of an object.

Before that, Alan Kay went the other way.
He encountered Simula and had the opposite epiphany.
Stroustrup saw a structuring tool to be made efficient.
Kay saw biology.
He saw objects as independent cells that communicate only by messages.
No fixed contract said what a cell could be asked.

While C++ kept Simula's static, classified, closed world and made it fast,
Smalltalk kept Simula's autonomous objects and threw away its static types, making the world open.
Simula's compile-time class contract gave way to runtime message passing and extreme late binding.
All of it is Kay discarding the closed world assumption of simulation.

Nearly every argument in OOP involves which half of Simula a language chose to keep.

## What Doesn't Fit Inside a Simulation

Simula's machinery models a world of classified, interacting, identity-bearing entities.
OOP ideology takes that machinery and declares it the way to structure all software.
But most programs are not simulations of such a world.
And the parts that aren't fight the mold.

Consider the things with no comfortable place in the simulation picture.

- **Values without identity.**
  A complex number, a date, a sum of money, a point in the plane.
  None of these are actors in a world.
  Two `3`s are the same `3`.
  There is no "this three" as distinct from "that three."
  A simulated ship has identity and needs it.
  A value does not.
  So the whole apparatus of objects-with-state is overhead when you model a value.

- **Computation and transformation.**
  A great deal of programming turns input into output.
  Think of parsing, compiling, rendering, aggregating, and mapping a function over a stream.
  These are processes, not populations.
  There is no taxonomy of interacting entities to discover.
  Forcing one, like a `ParserManager` owning a `TokenStrategy`, adds ceremony without meaning.
  This is the work functional programming describes naturally and OOP describes awkwardly.

- **Abstractions that don't classify.**
  Is a stack a kind of list?
  Is a square a kind of rectangle?
  The "is-a" relationship is reliable for ships and trucks.
  It turns treacherous once you leave the physical world for mathematical or designed abstractions.
  There, surface similarity and behavioral substitutability come apart.
  The famous puzzles of inheritance are all the same case.
  Something looks like a subtype but cannot honor the contract of one.

- **Things that play several roles at once.**
  A real object is often serializable, comparable, drawable, and persistable, all at the same time.
  These are not a kind it belongs to.
  They are capabilities it happens to have.
  A single-rooted taxonomy has one base class and one lineage.
  It cannot express "is several unrelated things at once."
  That is why static OO languages had to bolt on interfaces, traits, and mixins.
  They needed to recover what the strict tree forbids.
  The world is not actually a tree.
  But inheritance assumes it is, because the simulated worlds it came from largely were.

- **Cross-cutting concerns.**
  Things like logging, security, transactions, and caching run across the entire population of objects.
  They belong to no single kind.
  There is no entity in the harbor called "logging."
  Every attempt to force such concerns into the class hierarchy distorts it.
  This eventually drove people to aspects, decorators, and middleware.
  These approaches admit that not everything is a noun in a taxonomy.

The pattern behind all of these is one mistake, made early and repeated everywhere.
Simula gave us a superb tool for one job.
That job was describing a closed world of classified, interacting, identity-bearing actors.
We mistook it for a tool for every job.
Sometimes your problem genuinely is such a world.
Graphical user interfaces, with their nested widgets, were exactly such a world.
That is why early OOP and GUIs fit like a hand in a glove.
There, the tool is a joy.
But your problem may be values, or transformations, or capabilities, or concerns that cut across the whole system.
Then the tool makes you build a simulation of something that was never a simulation to begin with.

> Inheritance was invented to model a world that is already organized into kinds. Most of programming is not that world.

So object-oriented programming did not begin as a theory of how to structure software.
It began as a way to make a computer pretend to be a harbor.
The pretense was wildly successful, and the vocabulary was vivid.
So we adopted it for everything.
Along with the genuine gift of user-defined types, we inherited something else.
We inherited a static, taxonomic, closed-world model.
It fits some problems perfectly and quietly deforms the rest.
The chapters that follow are, in large part, the story of discovering which was which.
