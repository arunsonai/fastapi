"""Dependencies¶
FastAPI has a very powerful but intuitive Dependency Injection system.

It is designed to be very simple to use, and to make it very easy for any developer to integrate other components with FastAPI.

What is "Dependency Injection"¶
"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code with those needed dependencies ("inject" the dependencies).

This is very useful when you need to:

Have shared logic (the same code logic again and again).
Share database connections.
Enforce security, authentication, role requirements, etc.
And many other things...
All these, while minimizing code repetition.

First Steps¶
Let's see a very simple example. It will be so simple that it is not very useful, for now.

But this way we can focus on how the Dependency Injection system works.

Create a dependency, or "dependable"¶
Let's first focus on the dependency.

It is just a function that can take all the same parameters that a path operation function can take:


"""