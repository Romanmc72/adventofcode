# AOC 2024

Another year doing advent of code!

This time with many friends <3

The first year I did this was 2022 and I used Python. Last year I did it in Rust and enjoyed the challenge of learning a new language. This year I want to sharpen my golang skills! I have used golang at work and on some side projects, but will be using it very heavily coming up in my next role.

## Layout

There will be a days folder containing a go file for every day of the challenge. There will be a data subfolder inside that folder containing the inputs for the problem and the example provided.

The last 2 years I made each day be its own standalone program, but this year I think I will try to make the whole thing be one big program with command line parsing capabilities to input what day and what part of that day to run. We will see how it goes!

## Running a Particular Day

Running a particular day should possible using the `-day` flag when running the program and the part will be the `-part` flag. To use the example data, pass in the `-example` flag otherwise the "real data" will be used by default.

The program can be run either by being compiled or by running it with `go run main.go -day ## -part 1|2 -example`. Compiling will produce single executable binary that has all of the inputs and examples embedded in the program itself. So the compiled program will be large, but also will not require anything to actually be able to run it.

## Recreating a Golang AoC Package

Start with finding the github location you will be saving it to (mine was `github.com/Romanmc72/adventofcode/2024`) then run 

```
go mod init <that location>
```

Next you are going to want to use the `make_days.sh` script here to pre-populate the days. Replace the name of the github location within the script with yours. The approach I took was to have all the days stored inside a the `days` package with their data in a separate subdirectory within that folder, then to embed each day's data inside the program itself so when it is compiled it will not need to look up the data from on disk. If you have a better way then do that or write your own script.

Next I had to make a main.go file which will import the `Solutions` map from the `day/all_days.go` file that contains a mapping of each day number to the actual solution for that day. There is a uniform type signature for the solution within every day folder which this `map[int]Solution` borrows from. Each solution takes the part and the example flag as input and calls the program accordingly on its data to create the solution. There will likely be more parsing utilities developed as a part of this challenges that will go either in the utils package or in its own parsing package to aide in parsing the files themselves into golang data types.

Besides that I do have a utils folder with a translator that left-pads numbers to ensure it is always at least 2 digits. Besides that there is a JSON logging utility that will leverage the env var for `LOG_LEVEL` to switch between logging levels. The levels are pretty standard. See the file for details.
