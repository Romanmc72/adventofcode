use std::env;
use std::fs::File;
use std::io::prelude::*;

/// Description
/// -----------
/// Initial function to parse out whether this is part 1 or part 2 as
/// well as the contents of the file that is requested.
///
/// Return
/// ------
/// (Vec<String>, u32)
/// A tuple of 2 values, the first one is the array of lines found
/// in the requested file. The second one is the "part" which is
/// either 1 or 2 otherwise the program will panic and exit.
pub fn get_file_and_part() -> (Vec<String>, u32) {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];
    let part_str = &args[2];
    let radix = 10;
    let part = part_str.chars()
        .next()
        .expect("I was looking for an integer here, 1 or 2")
        .to_digit(radix)
        .unwrap();
    if part != 1 && part != 2 {
        panic!("Invalid Part # selection, expected 1 or 2 but got {}", part);
    }
    let mut file = File::open(file_name).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    // let lines = contents.split("\n").map(str::to_string).collect();
    let lines = split_str_to_vec(&contents, "\n");

    // Putting the returned value on a line by itself without a semi-colon
    // is the same as doing `return ();`
    (lines, part)
}

/// Description
/// -----------
/// The default string split mechanism is going to return an iterator, but
/// sometimes you want to split a string and use it as a vector of substrings
/// found within the parent string after being split. This is a thing that I
/// do so often it is easier to just write this out once and reuse it
/// everywhere.
///
/// Params
/// ------
/// :string_to_split: String
/// The string that will be split into a vector.
///
/// :delimiter: String
/// The delimiter to split the string on wherever it is found.
///
/// Return
/// ------
/// The string but split up into a vector of substrings found on either side
/// of the delimiter.
pub fn split_str_to_vec(string_to_split: &str, delimiter: &str) -> Vec<String> {
    string_to_split.split(delimiter).map(str::to_string).collect()
}
