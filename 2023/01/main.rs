mod common;

/// Description
/// -----------
/// Solves Day 1 2023 which has its own separate examples for each part, but
/// the same input for the puzzle in both parts. The goal is to take the
/// first number that appears in a string and the last number, combine them
/// as a first and second digit in a 2 digit number then to total up all 2
/// digit numbers in the list of strings. If only 1 number appears in the
/// string then that number is both the first and second digit.
///
/// Params
/// ------
/// The arguments for this `main()` program are picked up from the command line
/// when the program is executed and are based on the argument's position.
/// :filename: String [arg 1]
/// The name of the file on disk to read and split into lines of Vec<String>
///
/// :part: u32 [arg 2]
/// The part of the question that this input is being processed for. (1 or 2)
///
/// Return
/// ------
/// Prints out the numbers parsed from each line along with the line that
/// it came from and the running total. After all lines have been processed
/// the program prints out the total for all of the numbers.
fn main() -> std::io::Result<()> {
    let (lines, part) = common::get_file_and_part();

    let radix = 10;
    let mut total = 0;
    for line in lines {
        let mut first_num = true;
        let mut first = 0;
        let mut last = 0;

        for (index, character) in line.chars().enumerate() {
            let mut number = character.to_digit(radix);

            // Holy shit this is ugly, need me a separate function
            let mut found_num = number.is_some();
            if !found_num && part == 2 {
                let mut substring = String::from(character);
                let next1 = line.chars().nth(index + 1);
                if next1.is_some() {
                    substring.push(next1.unwrap());
                    let next2 = line.chars().nth(index + 2);
                    if next2.is_some() {
                        substring.push(next2.unwrap());
                        if substring == "one" {
                            number = Some(1);
                            found_num = true;
                        } else if substring == "two" {
                            number = Some(2);
                            found_num = true;
                        } else if substring == "six" {
                            number = Some(6);
                            found_num = true;
                        }
                        let next3 = line.chars().nth(index + 3);
                        if next3.is_some() {
                            substring.push(next3.unwrap());
                            if substring == "nine" {
                                number = Some(9);
                                found_num = true;
                            }  else if substring == "four" {
                                number = Some(4);
                                found_num = true;
                            } else if substring == "five" {
                                number = Some(5);
                                found_num = true;
                            }
                            let next4 = line.chars().nth(index + 4);
                            if next4.is_some() {
                                substring.push(next4.unwrap());
                                if substring == "seven" {
                                    number = Some(7);
                                    found_num = true;
                                } else if substring == "eight" {
                                    number = Some(8);
                                    found_num = true;
                                } else if substring == "three" {
                                    number = Some(3);
                                    found_num = true;
                                }
                            }
                        }
                    }
                }
            }

            if first_num & found_num {
                first = number.unwrap();
                last = first;
                first_num = false;
            } else if !first_num & found_num {
                last = number.unwrap();
            }
        }
        let new_num = first * 10 + last;
        total += new_num;
        println!("=================\nLine:   {}\nBecame: {}\nTotal:  {}", line, new_num, total);
    }
    println!("=================\nThe answer is! {}", total);
    Ok(())
}
