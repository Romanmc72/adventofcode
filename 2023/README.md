# Description

Going back over the 2023 attempt in Rust and realized I have not touched rust since. I definitely wish I had a README to guide myself back through running these examples. So I am writing one now.

## Running this

Each day is its own independent program stored inside the folder name matching the day number. To run one day you will need your rust program to compile for that day. Once in the day's folder, compiling can be accomplished with:

```
rustc ./main.rs
```

after which point you will need to run the `main` program that was just compiled by doing:

```
./main <input file> <part> 
```

where input file is either `input.txt` or `example.txt` and part is either `1` or `2`.

If the program does not compile then you have some bugs to fix!
