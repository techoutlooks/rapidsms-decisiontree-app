Advanced Tree Example
===================================

Here we will expand on the previous tree example to contain branches based on varying
answers. We will continue to work from the Monty Python questions.


New Questions
------------------------------------

First will add new questions for the addition branches::

    # Questions
    pk: 4
    text: What is the capital of Assyria?

    pk: 5
    text: What is the air-speed velocity of an unladen swallow?


New Answers
------------------------------------

In the same logic of the movie we will ask the questions based on the name of the 
knight::

    # Answers
    pk: 2
    name: Sir Robin
    type: Regular Expression
    answer: .*Robin.*

    pk: 3
    name: King Arthur
    type: Regular Expression
    answer: .*Arthur.*


New States and Transitions
------------------------------------

We need additional states to handle these trees. Since the final question is the
only thing different we still need multiple states which point to the same second
question::

    # Tree States
    pk: 4
    question: 4

    pk: 5
    question: 5

    pk: 6
    question: 2

    pk: 7
    question: 2


Now we need the transitions between the questions based on the first answer. First
we will do Sir Robin::

    # Transitions
    pk: 3
    current state: 1
    answer: 2
    next state: 6

    pk: 4
    current state: 6
    answer: 1
    next state: 4

    pk: 5
    current state: 4
    answer: 1
    next state: null

Then King Arthur::

    # Transitions
    pk: 6
    current state: 1
    answer: 3
    next state: 7

    pk: 7
    current state: 7
    answer: 1
    next state: 5

    pk: 8
    current state: 5
    answer: 1
    next state: null

The tree itself does not need to be modified. An example SMS workflow is given below::

    555-555-1234 >>> #test
    555-555-1234 <<< What is your name? # This is state 1, question 1
    555-555-1234 >>> Sir Robin
    555-555-1234 <<< What is your quest? # This is state 6, question 2
    555-555-1234 >>> To seek the Holy Grail.
    555-555-1234 <<< What is the capital of Assyria? # This is state 4, question 4
    555-555-1234 >>> I don't know that.
    555-555-1234 <<< Go on. Off you go. # End of questions

So this isn't perfect to movie but it should demonstrate the difference from the
simple example.
