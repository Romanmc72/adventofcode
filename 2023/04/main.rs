use std::collections::HashMap;
use std::convert::TryInto;

mod common;


/// Description
/// -----------
/// Parses the scratch card number into 2 halves and checks to see if any
/// number in the second half exists in the first. For each number the card
/// total is doubled (starting at 1). The total of all totals is then added
/// up and returned.
fn main() {
    let (lines, part) = common::get_file_and_part();
    let mut total: u32 = 0;
    let mut cards: Vec<u32> = vec![];
    for line in lines.iter() {
        let mut wins: u32 = 0;
        let split_line: Vec<&str> = line.split(": ").collect();
        let game = split_line.get(1).unwrap();
        let winners_and_actual: Vec<&str> = game.split(" | ").collect();
        let winners = string_to_numbers(winners_and_actual.first().unwrap());
        let actual = string_to_numbers(winners_and_actual.get(1).unwrap());
        for number in actual {
            if winners.contains(&number) {
                wins += 1;
            }
        }
        if wins == 0 || wins == 1 {
            total += wins;
        } else {
            total += 2_u32.pow(wins - 1);
        }
        cards.push(wins);
    }
    if part == 1 {
        println!("Part 1 Scratch ScratchCard Winnings = {}", total);
    }
    if part == 2 {
        total = 0;
        // Card number as the key and the count of times that card 
        let mut times_map: HashMap<usize, u32> = HashMap::new();
        for (card_number, card) in cards.iter().enumerate() {
            let card_deref: u32 = *card;
            let card_score: usize = card_deref.try_into().unwrap();
            let next_card_number: usize = card_number + 1;
            let last_card_number: usize = card_number + card_score + 1;
            let current_card_multiplier: &u32 = times_map.get(&card_number).unwrap_or(&1);
            let current_card_multiplier_value = *current_card_multiplier;
            for following_card_number in (next_card_number)..(last_card_number) {
                match times_map.get(&following_card_number) {
                    Some(count) => {
                        times_map.insert(
                            following_card_number,
                            count + current_card_multiplier_value
                        );
                    },
                    None => {
                        times_map.insert(
                            following_card_number,
                            1 + current_card_multiplier_value
                        );
                    },
                }
            }
            match times_map.get(&card_number) {
                Some(count) => {
                    total += count;
                    println!("card: {}, wins={}, cards={}", card_number + 1, card, count);
                },
                None => {
                    total += 1;
                    println!("card: {}, wins={}, cards={}", card_number + 1, card, 1);
                },
            }
        }
        println!("Part 2 Scratch ScratchCard Winnings = {}", total);
    }
}


/// Description
/// -----------
/// Takes string of numbers separated by spaces and returns the array of u32
/// numbers.
///
/// Params
/// ------
/// :string: &str
/// The string to parse out and split up into numbers.
///
/// Return
/// ------
/// Vec<u32>
/// The vector of numbers parsed out of the string.
fn string_to_numbers(string: &str) -> Vec<u32> {
    let numbers: Vec<u32> = string.split(" ")
        .map(|each_string| each_string.trim())
        .filter(|each_string| !each_string.is_empty())
        .map(|each_string| each_string.parse().unwrap())
        .collect();
    numbers
}
