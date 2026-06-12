---
title: "Simula"
label: "Chapter Four"
published: true
---

Every word we use to talk about objects was coined from a language that tried to simulate the world.

Class, object, subclass, inheritance, virtual method, instance: this entire vocabulary arrived more or less complete in a single language.
It was designed in Oslo in the 1960s by Ole-Johan Dahl and Kristen Nygaard.
They did not set out to invent object-oriented programming.
They set out to write simulations, and OOP emerged.
The name says it: *Simula*, the simulation language.

The fact that the first object-oriented language was a simulation language, and that it was statically typed, shaped everything that followed.
The tools we still reach for when we structure a program, classes arranged in inheritance hierarchies, were designed to describe a particular kind of thing: a world of interacting entities that can be sorted into a clean taxonomy.
When the problem in front of you really is that kind of world, the tools fit beautifully.
When it isn't, you question the value of OOP.

## Nygaard's Problem

Kristen Nygaard was an operations researcher.
Before he was a language designer he spent years building Monte Carlo simulations of physical systems: the flow of ships through a port, customers through a queue, jobs through a factory.
These are *discrete-event simulations*: you model a system as a collection of distinct entities, each with its own state, each behaving according to its own rules, and you let simulated time advance while they interact.

The difficulty was never the arithmetic.
The difficulty was *description*.
ALGOL and FORTRAN gave you procedures and arrays, but a port full of ships is not naturally a procedure or an array.
It is a population of things, each of which is *like* the others in kind but distinct in identity and state.
This tanker and that tanker are both ships; they share behavior; they differ in where they are and what they carry.
Nygaard needed a way to say "a ship" once, as a kind, and then bring as many individual ships into being as the simulation required, each remembering its own situation.

That sentence is the definition of a class and its instances.
The class is the *kind*; the objects are the individuals.
Dahl, the more rigorous language designer of the pair, gave Nygaard's modeling need a precise form on top of ALGOL 60.
Simula I appeared in the mid-1960s as a simulation tool; Simula 67 generalized the machinery into a full programming language.
By 1967 every essential idea of class-based OOP was in place, decades before most of the industry noticed.

## Simulation Shaped the Design

It is worth being concrete about *how* the simulation goal produced the features we now treat as universal.

**Objects are autonomous actors.**
In a simulation, each entity is a little independent agent: it owns its state, it owns the procedures that act on that state, and the outside world is not supposed to reach in and meddle.
Encapsulation, bundling data with the operations on it and hiding the internals, is exactly what you want when each object is meant to be a self-contained participant in a larger world.
It was not invented as a software-engineering discipline; it was invented because that is what a ship, or a customer, or a server *is* in a model.

**Inheritance is taxonomy.**
A simulated world comes pre-sorted.
A tanker is a kind of ship; a ship is a kind of vessel.
A passenger car and a truck are kinds of vehicle.
The domains Nygaard modeled were full of these "is-a" relationships, because the physical and organizational world really does organize itself into hierarchies of kinds.
Subclassing let him capture a general kind once and then specialize it: a truck is everything a vehicle is, plus a cargo capacity, plus its own behavior at a loading dock.
Inheritance is, in its birthplace, a *classification* mechanism, and classification is genuinely how simulation domains are structured.
This is the single most important fact in this book, and we will return to it: inheritance was born to model taxonomies, and it works wonderfully when the problem is a taxonomy.

**Virtual methods are the actors deciding for themselves.**
When the scheduler tells "the next ship" to advance, it should not have to know whether that ship is a tanker or a ferry; the ship itself should know how it behaves.
Simula introduced *virtual* procedures so that a call made through the general kind would dispatch to the specific kind's behavior at runtime.
This is dynamic binding, or polymorphism, and again it falls directly out of the simulation picture: the scheduler holds a population of "ships" and lets each one act according to what it actually is.

**Coroutines are quasi-parallel time.**
Here is the Simula feature the mainstream forgot.
A discrete-event simulation is full of entities that run "at the same time": each ship is living its own life, suspending when it has nothing to do and resuming when its turn comes.
Simula gave its objects the ability to behave as *coroutines*: processes that suspend and resume, carrying their place in their own story with them.
An object was not just a passive bundle of data and methods; it could be an active process with a life of its own.
The OO languages that followed mostly dropped this, keeping the class-and-inheritance half of Simula and throwing away the active-process half.
We have spent the decades since reinventing it under other names (threads, generators, async/await) without remembering that the first object was already a little autonomous process, because the first objects were simulated actors that all ran at once.

## The Original Object Was Statically Typed

Simula was built on ALGOL 60, and ALGOL was statically typed, so Simula was statically typed.
A variable declared to hold a `Ship` held a `Ship`; the compiler knew the kind of every object before the program ran, and checked the calls you made against the kind you declared.
**The original object-oriented language was static.**

This was not a reluctant compromise.
It fit the simulation worldview perfectly, because a simulation is a *closed, known world*.
Before you run a port simulation you already know the complete cast of characters: ships, berths, tugs, cargo, the clock.
The ontology is fixed in advance, by you, as part of designing the model.
There is no moment at runtime when a genuinely new *kind* of thing wanders into the harbor that the modeler never conceived of.
When the set of kinds is known up front, declaring those kinds up front and letting the compiler enforce them costs you nothing and buys you safety.
Static typing and simulation are made for each other: both assume a universe whose categories are settled before the action starts.

The effect of that choice on programming was enormous, and it is the reason the two halves of this book exist.
Static typing welds an object to a contract fixed at compile time.
Through a `Ship` reference you may send only the messages `Ship` declares, no more, no matter what the object underneath really is.
Inheritance under static typing therefore becomes a *promise*: to be a subclass is to commit to honoring the base class's interface everywhere the base class is expected.
That is the seed of everything we will later call the Liskov Substitution Principle (LSP): the rigidity of inheritance, and the argument about whether a `Square` is a type of `Rectangle`.
None of those constraints are inherent to "objects."
They are inherited from the decision, natural for a simulation language, to know all the types in advance.

## The Effect on C++ and Smalltalk

Bjarne Stroustrup used Simula for his doctoral work at Cambridge, simulating distributed systems.
He loved what its classes did for the *structure* of his programs and hated what they did for their *speed*: Simula was too slow for the scale he needed.
So he set out to graft Simula's class concept onto C, a language with no overhead and an aggressively static, compile-it-all-down-to-the-metal philosophy.
"C with Classes" became C++.
Crucially, Stroustrup kept Simula's static typing and made it sharper: classes, inheritance, and virtual functions, all checked at compile time, all compiled away to nothing at runtime.
The static, taxonomy-shaped OOP of Simula flowed almost directly into C++, and from C++ into Java, and from there into the mainstream's whole idea of what an object is.

Alan Kay went the other way.
He encountered Simula early, famously puzzling over a listing of it, and had the opposite epiphany.
Where Stroustrup saw a structuring tool to be made efficient, Kay saw *biology*: objects as independent cells communicating only by messages, with no fixed contract about what a cell could be asked.
Smalltalk kept Simula's objects and threw away its static types, replacing the compile-time class contract with runtime message passing and extreme late binding.
Everything in the next chapter on Smalltalk (duck typing, `doesNotUnderstand:`, growing an object's interface at runtime) is Kay deciding that the *closed world* assumption of simulation was the part to discard.

C++ kept Simula's static, classified, closed world and made it fast.
Smalltalk kept Simula's autonomous objects and made the world open.
Nearly every argument in OOP involves which half of Simula a language chose to keep.

## What Doesn't Fit Inside a Simulation

Simula's machinery is the machinery for modeling a world of classified, interacting, identity-bearing entities.
We then took that machinery and declared it the way to structure *all* software.
But most programs are not simulations of such a world, and the parts of a program that aren't fight the mold.

Consider the things that have no comfortable place in the simulation picture:

- **Values without identity.**
  A complex number, a date, a sum of money, a point in the plane: these are not actors in a world.
  Two `3`s are the same `3`; there is no "this three" as distinct from "that three."
  Identity, the thing a simulated ship has and needs, is precisely what a value does not have, and the whole apparatus of objects-with-state is overhead when modeling a value.

- **Computation and transformation.**
  A great deal of programming is turning input into output: parsing, compiling, rendering, aggregating, mapping a function over a stream.
  These are processes, not populations.
  There is no taxonomy of interacting entities to discover, and forcing one, a `ParserManager` owning a `TokenStrategy`, adds ceremony without adding meaning.
  This is the work functional programming describes naturally and OOP describes awkwardly.

- **Abstractions that don't classify.**
  Is a stack a kind of list?
  Is a square a kind of rectangle?
  The "is-a" relationship that is so reliable for ships and trucks turns treacherous the moment you leave the physical world for mathematical or designed abstractions, where surface similarity and behavioral substitutability come apart.
  The famous puzzles of inheritance are all cases where something looks like a subtype but cannot honor the contract of one.

- **Things that play several roles at once.**
  A real object in a program is often simultaneously serializable, comparable, drawable, and persistable.
  These are not a *kind* it belongs to; they are capabilities it happens to have.
  A single-rooted taxonomy, one base class and one lineage, cannot express "is several unrelated things at once," which is why static OO languages had to bolt on interfaces, traits, and mixins to recover what the strict tree forbids.
  The world is not actually a tree, but inheritance assumes it is, because the simulated worlds it came from largely were.

- **Cross-cutting concerns.**
  Things like logging, security, transactions,
  and caching run *across* the entire population of objects and belong to no single kind.
  There is no entity in the harbor called "logging."
  Every attempt to force such concerns into the class hierarchy distorts it.
  This eventually drove people to aspects, decorators, and middleware.
  These approaches admit that not everything is a noun in a taxonomy.

The pattern behind all of these is one mistake, made early and repeated everywhere.
Simula gave us a superb tool for one job, describing a closed world of classified, interacting, identity-bearing actors, and we mistook it for a tool for every job.
Where your problem genuinely is such a world (and graphical user interfaces, with their nested widgets, were exactly such a world, which is why early OOP and GUIs fit like a hand in a glove), the tool is a joy.
Where your problem is values, or transformations, or capabilities, or concerns that cut across the whole system, the tool makes you build a simulation of something that was never a simulation to begin with.

> Inheritance was invented to model a world that is already organized into kinds. Most of programming is not that world.

Object-oriented programming, then, did not begin as a theory of how to structure software.
It began as a way to make a computer pretend to be a harbor.
The pretense was so successful, and the vocabulary so vivid, that we adopted it for everything, and inherited, along with the genuine gift of user-defined types, a static, taxonomic, closed-world model that fits some problems perfectly and quietly deforms the rest.
The chapters that follow are, in large part, the story of discovering which was which.
