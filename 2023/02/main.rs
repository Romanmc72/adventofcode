use std::cmp;

mod common;

/// Description
/// -----------
/// The day 2 solution (both parts)!
/// Takes the dice games played with the elf and splits up the text, iterating
/// over the pieces to get the totals and the "power" score for the games to find
/// 1) what games are impossible with a given configuration and
/// 2) what the minimum required dice count for each color is multiplied together
/// per game then added all up!
fn main() -> std::io::Result<()> {
    let (lines, _) = common::get_file_and_part();
    let mut total = 0;
    let mut power = 0;
    let max_red = 12;
    let max_green = 13;
    let max_blue = 14;
    for line in lines {
        let (game_number, latter_half) = get_game_number_and_remainder(&line);
        let mut red: u32 = 0;
        let mut green: u32 = 0;
        let mut blue: u32 = 0;
        for random_pull_string in latter_half.split("; ") {
            for each_category in random_pull_string.split(", ") {
                pull_number(each_category, "red", &mut red);
                pull_number(each_category, "green", &mut green);
                pull_number(each_category, "blue", &mut blue);
            }
        }
        if red > max_red || green > max_green || blue > max_blue {
            println!("Game Number={}; Red={}; Blue={}; Green={} IS IMPOSSIBLE!", game_number, red, blue, green);
        } else {
            total += game_number;
        }
        power += red * green * blue;
    }
    println!("Game totals are {}", total);
    println!("Game power totals are {}", power);
    Ok(())
}


/// Description
/// -----------
/// Separated tbe parsing of the game number/rest of the data to its own function.
///
/// Params
/// ------
/// :line: &str
/// The line to split up.
///
/// Return
/// ------
/// (u32, String)
/// The game number and the rest of the line.
fn get_game_number_and_remainder(line: &str) -> (u32, String) {
    let split_line: Vec<String> = common::split_str_to_vec(line, ": ");
    let game_portion = split_line.get(0).unwrap();
    let game_portion_split: Vec<String> = common::split_str_to_vec(game_portion, " ");
    let game_number_string = game_portion_split.get(1).unwrap();
    let game_number: u32 = game_number_string.parse().unwrap();
    let latter_half = split_line.get(1).unwrap().to_string();
    (game_number, latter_half)
}


/// Description
/// -----------
/// Pull the number out of the substring given the particular color then set
/// the value of the input min and max numbers to be the new value
/// (where appropriate).
///
/// Params
/// ------
/// :input_string: str
///
/// :color: &str
/// The color to try to extract from the text (if it matches)
///
/// :max_to_set: &u32
/// The variable holding a number which will take on the value of either
/// itself or the parsed number, whichever is higher.
fn pull_number(input_string: &str, color: &str, max_to_set: &mut u32) {
    if input_string.contains(color) {
        let delimiter = " ".to_owned() + color;
        let split_string = common::split_str_to_vec(input_string, &delimiter);
        let num: u32 = split_string.get(0).unwrap().parse().unwrap();
        *max_to_set = cmp::max(*max_to_set, num);
    }
}
