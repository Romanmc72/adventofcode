# Arnold C

Purely for the LOLZ I wanted to write a program in [ArnoldC](https://lhartikk.github.io/ArnoldC/). A programming language that trans-piles to java starting from Arnold Schwarzenegger movie quotes.

It is exclusively an LOL language and I intend to laugh at day 1 with a ridiculously silly looking program.

## Getting Started

Copied from the getting started guide on the Arnold C (linked above) you can `wget` the jar that allows you to compile a `.arnoldc` file.

```
wget http://lhartikk.github.io/ArnoldC.jar
```

then create a file ending in `.arnoldc` and to compile it run

```
java -jar ArnoldC.jar yourProgram.arnoldc
```

which should result in a file named `yourProgram.class` which can be run by

```
java yourProgram
```

## Running This

To actually sanely accomplish the challenge, inputs must only be numeric otherwise I will need to implement the ascii character set in ArnoldC. (Not looking to do that) Additionally ArnoldC programs can only take input from stdin, so I will be passing in input from a `tmux` session in which the program will run and have a very large number be the signal to terminate at the end.

So it will be the above "Getting Started" steps to compile my program then it will be:

```
tmux
```

to start the session in the background followed by

```
java yourProgram
```

to begin the compile program. After that I will press ctrl+B then ctrl+D to detach. Once detached I can iterate through the input.txt file and send its contents to the tmux session as if I were manually entering the inputs myself like so:

```
for line in $(cat input.txt)
do
  tmux send-keys -t 0 $line
  tmux send-keys -t 0 KPEnter
done
```

in the above KPEnter is the "enter key press" keyword from tmux to simulate hitting enter after making an entry. 
