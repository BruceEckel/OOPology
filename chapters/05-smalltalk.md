---
title: "Smalltalk"
label: "Chapter Five"
published: true
---

Smalltalk is extremely dynamic.
A Smalltalk program runs inside a live image of objects that can be modified during execution.
Every component of the system--classes, methods, even control structures--is an object that can be inspected and altered at runtime.
This produces a highly interactive development experience: developers change code and see the effects immediately, without restarting.
New methods or classes can be added on the fly, and objects respond to new messages accordingly.
This open-ended dynamism promised much greater developer productivity, and it made Smalltalk a pioneer in object-oriented design.

When C++ was created, its designers hoped that OOP developer productivity could be tied to the ideas of objects and inheritance,
and were _not_ essentially bound to the rest of Smalltalk's features and development environment.
What we slowly discovered over subsequent decades is that the fluid, open object model that Smalltalk enjoys
cannot be replicated in statically typed languages.

In effect, Smalltalk has no type system in the way that term is usually meant.
You can send any message to any object, and the system attempts to find a matching method on the object at runtime.
If none exists, the runtime sends the object a `doesNotUnderstand:` message, which by default raises a runtime "message not understood" error.
The only way to know whether an object will understand a given message is to send the message and see if the object responds.

Statically typed languages require that an object's type--its class, interface, or trait--explicitly declare all the methods it supports.
Any call to a nonexistent method is caught at compile time as a type error.
Static languages trade away Smalltalk's on-the-fly flexibility for the guarantee that method calls won't go astray.
Idioms common in Smalltalk--adding methods to objects at runtime, or relying on duck typing--are impractical or impossible to express in a statically typed language.

In Smalltalk, the set of messages an object can respond to essentially defines its type at that moment.
But this "type" is not a formal, static annotation; it is just the object's current behavior, which can change as the program runs.
Two objects are effectively the same type if they handle the same messages, regardless of their class lineage or internal representation.
Smalltalk is strongly *dynamically* typed: every object's type is well-defined at runtime, and objects do not change types arbitrarily,
but the language does not check types until a message is sent.

Because Smalltalk has no static way to encode expectations (types), the community invented test-driven development to catch errors;
xUnit testing was prototyped in Smalltalk.

## The Smalltalk Programming Experience

Smalltalk isn't just a language--it's a way of programming.
Rather than designing everything up front, Smalltalk encourages programmers to build systems interactively, incrementally, and dynamically.
The key ideas:

- Everything is an object.
- You send messages to objects.
- It's OK for an object not to understand a message.
- Objects can learn new behaviors at runtime.
- The system evolves as you work.

The entire session mirrors the experience of working in a Smalltalk image: there is no compile-run-edit loop.
You interact with objects directly, teach them behavior, and the system grows and adapts as you explore it.
When you are unsure what messages an object supports, you can literally ask the object or its class at runtime.
The system can list an object's method selectors or browse its class hierarchy.
This introspective capability--possible because everything is alive in the image--gives you a form of "live documentation."

When you make a mistake--say you send a message an object doesn't understand--it's not usually a silent failure.
In a typical Smalltalk IDE, a debugger pops up at the point of error.
This is not just an error message; it's an opportunity.
You can inspect the object that failed, figure out why it didn't have the method, and often define the missing method right there in the debugger and continue execution.
The program is malleable and can be fixed or extended on the fly.

## Building by Inheriting and Adding

The defining workflow of Smalltalk development is not "design a class and then instantiate it."
It is "find the closest existing class, subclass it, and add the methods you need."
The system arrives as an enormous library of live classes, and you grow your program by grafting onto that tree.
You subclass `Object`, or `Collection`, or `Model`, and then you _add_ methods--often one at a time, in the browser, while the system is running.

This is the heart of Smalltalk's productivity, and it depends entirely on the dynamic model.
Because a class is just a live object holding a dictionary of methods, adding a method is a runtime operation, not a recompilation.
You can add a method to a class you wrote, to a library class, or even to `Object` itself, and every existing instance in the image immediately gains the new behavior.
Inheritance in Smalltalk is therefore *additive and open-ended*: a subclass starts with everything the superclass can do, and you extend it incrementally.
You never have to anticipate the full interface in advance.
The superclass does not need to know about the messages you will later add to the subclass.

This is what makes inheritance feel natural in Smalltalk.
The subclass is a place to *accumulate* behavior.
You inherit a working object and pile new capabilities on top of it, message by message, without disturbing the superclass or the rest of the system.

## Inheritance Forces You to Deal with the Base Class

The same inheritance that feels liberating in Smalltalk becomes a constraint once a static type system is involved.
When you inherit, you _must_ make your new class a "type of" the base class, with everything that entails, including overriding methods you don't care about.
Your new class _belongs_ to the base class.

> With composition, the object does what _you_ want; with inheritance, you must do what the base class wants.

In Smalltalk this obligation is soft, because the base class's "interface" is just whatever methods happen to be in its dictionary, and you are free to add more.
In a statically typed language the obligation is hard and enforced by the compiler, which leads directly to the principle that governs inheritance in those languages.

## The Liskov Substitution Principle

The Liskov Substitution Principle (LSP) states that an object of a base class should be replaceable by an object of any derived class without breaking the program.
If code is written against the base class, then any subclass must be usable wherever the base class is expected, honoring the base class's contract.

The crucial consequence for our purposes: **every message a caller is allowed to send must appear on the base class.**
A static type system only knows the base type.
If a variable is declared as `Shape`, the compiler permits only the messages declared on `Shape`.
A method that exists *only* on a subclass is invisible through a base-class reference, because the compiler has no way to know the object is really that subclass.
To use a behavior polymorphically, you must declare it on the base class up front.

This is the exact inverse of the Smalltalk workflow.
In Smalltalk, you inherit a base object and *add* new messages to the subclass as you go, and callers can send those new messages freely--the system will find them at runtime.
Under LSP and static typing, the interface must be planned at the base class before any subclass is written.
You cannot grow the usable interface from the leaves of the hierarchy upward; it must be declared at the root and merely *implemented* by the subclasses.

So the two models pull in opposite directions:

- **Smalltalk:** the base class is a starting point, and subclasses extend the set of messages that can be sent. The interface grows downward and outward, at runtime, as you work.
- **LSP / static typing:** the base class is a contract, and subclasses may only refine or implement what the base already declares. The interface is fixed at the top, at compile time, before the subclasses exist.

Smalltalk's "subclass and add methods" style is precisely the thing a Liskov-respecting static type system cannot accommodate,
because the new methods are not visible through the base type that the rest of the program was written against.

## Why Smalltalk OOP Didn't Become Statically Compiled OOP

A proof-of-concept is not a product, and the dynamism that made Smalltalk so productive could not be tied down.
The fluid object model--adding methods at runtime, sending any message to any object, growing interfaces from the subclasses--is the source of Smalltalk's power,
and it is exactly what a static type checker must forbid.

Arguably the only real success story in carrying the Smalltalk spirit forward is Ruby, which is itself a kind of Smalltalk.

## "Type" in Smalltalk: A Dynamic, Message-Driven Perspective

In Smalltalk, an object's identity and capabilities are not described by an explicit static type annotation.
Instead, an object is defined by the messages it can respond to.
An object's *protocol*--the collection of message selectors it understands--is effectively its "type."
You determine what an object can do by the messages you send it and how it responds, not by checking a formal type label.

This message-centric view is fundamental.
All computation in Smalltalk is performed by sending messages to objects.
There are no free functions or primitive operations outside of this model--every operation is a message sent to some object.
The result of a message depends entirely on the receiver: the same selector might do something completely different on another object, because each class provides its own method for that message.
The object itself decides how to fulfill a request, reinforcing the idea that what matters is the object's behavior, not an external static description.

### "Type" as an Emergent Set of Behaviors (Duck Typing)

Because there are no declared types on variables or method arguments in Smalltalk, "type" becomes an emergent property of an object's behavior.
An object's type can be thought of as "the set of messages to which it can meaningfully respond."
In modern parlance, this is duck typing: "if it walks like a duck and quacks like a duck, it's a duck."
Smalltalkers don't ask "Is this object of type `Duck`?"--there is no formal type check or interface to query.
Instead, they ask "Can this object respond to the messages we associate with a duck, like `quack` or `swim`?"
If yes, then for all intents and purposes it can play the role of a duck.
Different classes can implement the same set of messages, thereby conforming to the same "duck type."
This gives Smalltalk tremendous flexibility and polymorphism: any object that implements the expected messages can be used in a given context, regardless of its class.

Smalltalk is not "weakly typed" or "untyped."
It is strongly typed at runtime: if you send a message an object doesn't understand, the system throws a runtime error rather than blindly misinterpreting it.
Strong typing only means type errors are prevented; it does not require that they be prevented at compile time.
A `MessageNotUnderstood` error halts a misuse, analogous to a type error in a static system, but occurring at runtime.
Every object has a type in the sense of a well-defined set of messages; what Smalltalk lacks is a static type checker to verify those at compile time.
A value's type is an intrinsic property of the object, not of the variable referencing it.
Any variable can refer to any object, so the "type" lives with the object, not the variable.

### Handling the Unknown: `doesNotUnderstand:`

One fascinating aspect of Smalltalk's message-centric design is how it handles an unknown message.
If you send an object a message for which it has no defined method, the runtime doesn't immediately crash.
Instead, it sends a special message `doesNotUnderstand:` to that object, passing along a description of the original message.
By default, `Object>>doesNotUnderstand:` raises a `MessageNotUnderstood` error (often opening a debugger),
but critically, developers can override this method to change the behavior.
An object can be designed to gracefully handle any message at all, even ones not originally defined in its class.

For example, you can create a proxy object that intercepts all messages via `doesNotUnderstand:` and forwards them to another object,
or a stub that logs all unknown messages for testing.
Smalltalk was the first language to introduce this kind of open-ended message handling, and it unlocks a great deal of power:
remote method invocation proxies, lazy-loaded objects, futures, and other patterns that require catching arbitrary messages at runtime.
The existence of `doesNotUnderstand:` underscores that an object's "type"--its message-handling ability--isn't necessarily fixed by its class; it can be extended or altered at runtime.

The flip side is that you truly don't know whether a given message will be handled until you send it.
In practice, Smalltalk programmers cope with this by testing and by building systems where the expectations are clear,
using the interactive tools to inspect an object's class and protocol.
Type in Smalltalk is something an object *does*, not something it *declares*.

### Classes as Behavioral Templates, Not Compile-Time Constraints

Smalltalk is a class-based language, and every object is an instance of some class.
However, a class in Smalltalk is not a "type" in the static sense; it's more like a template that defines behavior and structure.
A class specifies which messages its instances understand and defines the internal state structure.
Two different classes can implement the same protocol--thus the same behavioral type--while remaining distinct classes with different internal representations.
Smalltalk has no separate notion of an interface or protocol type distinct from classes; classes are how you organize and advertise what messages exist.
But the system never restricts you to using only a particular class in a given variable or call.
There's no static type checker insisting "this variable must contain an instance of class X."
The class is a property of the object itself, not a restriction on its use by others.
A seasoned Smalltalker might say an object's true "type" is simply the set of messages it knows how to handle, regardless of its class name.

### The Programmer's Mindset

From a philosophical standpoint, a Smalltalk programmer thinks in terms of objects and messages first, and types (in the classical sense) hardly at all.
Alan Kay, the father of Smalltalk, famously remarked that "OOP to me means only messaging, local retention and protection and hiding
of state-process, and extreme late-binding of all things."
Late-binding here refers to deciding at run-time what method to invoke for a given message--precisely what dynamic typing entails.
This mindset puts the focus on behavior rather than classification.
If you ask a Smalltalker "what type is this object?" they are likely to answer in terms of its responsibilities--
"this is a kind of stream object; it can `next`, `nextPut:`, and so on"--
rather than enumerate a static type name with a fixed interface contract.

To crystallize the difference:

- **Types as explicit contracts (static languages):** A type is a blueprint for both the compiler and the programmer.
  The programmer leans on the compiler to enforce the contract; calling a non-existent method is caught at compile time.
  You design software by starting with type definitions and using them as constraints to prevent incorrect usage.
  You can't accidentally call `v.turnPurple()` on a `Vector` if that method isn't in its type--but you also can't pass a `Matrix` to a function expecting a `Vector`
  unless `Matrix` is formally declared compatible, even if it happens to support every operation needed.

- **Types as descriptions of behavior (Smalltalk):** Types are implicit descriptions of behavior.
  If a method expects a "duck-like" object, you pass it an object and trust it knows how to quack; there is no `IDuck` interface to check against.
  As long as the object can handle the messages used inside the method, it works; otherwise a runtime error occurs.
  The emphasis is on what an object can do, not what it is declared to be.
  The trade-off is that mistakes show up at runtime, so thorough testing is essential.

### Summary

"Type" in Smalltalk is less a label and more a dynamic quality of an object's behavior: the set of messages it can handle--its protocol.
Smalltalk's class system provides the structure for those protocols, but it doesn't impose the strict borders that static type systems do.
Instead of types as fences that keep misuse at bay, Smalltalk offers open pastures where objects roam freely as long as they know how to handle the messages that come their way.
This shifts the notion of type from an abstract compile-time idea to a tangible runtime reality.
In statically typed systems, type is often treated as essence; in Smalltalk, type is experience.
