use std::env;
use std::fs::File;
use std::io::prelude::*;

fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];
    let part_str = &args[2];
    let radix = 10;
    let part = part_str.chars()
        .nth(0)
        .expect("I was looking for an integer here, 1 or 2")
        .to_digit(radix)
        .unwrap();
    if part != 1 && part != 2 {
        panic!("Invalid Part # selection, expected 1 or 2 but got {}", part);
    }
    let mut file = File::open(file_name)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    let lines = contents.split("\n");

    let mut total = 0;
    for line in lines {
        let mut first_num = true;
        let mut first = 0;
        let mut last = 0;

        for (index, character) in line.chars().enumerate() {
            let mut number = character.to_digit(radix);

            // Holy shit this is ugly, need me a separate function
            let mut found_num = !number.is_none();
            if !found_num && part == 2 {
                let mut substring = String::from(character);
                let next1 = line.chars().nth(index + 1);
                if !next1.is_none() {
                    substring.push(next1.unwrap());
                    let next2 = line.chars().nth(index + 2);
                    if !next2.is_none() {
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
                        if !next3.is_none() {
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
                            if !next4.is_none() {
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
        total = total + new_num;
        println!("=================\nLine:   {}\nBecame: {}\nTotal:  {}", line, new_num, total);
    }
    println!("=================\nThe answer is! {}", total);
    Ok(())
}
