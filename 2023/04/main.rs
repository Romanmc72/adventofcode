use std::convert::TryInto;

mod common;

#[derive(Debug, Clone)]
struct ScratchCard {
    score: u32,
    times: u32,
}

impl ScratchCard {
    pub fn new(score: u32) -> ScratchCard {
        ScratchCard { score, times: 1 }
    }

    pub fn set_score(&mut self, score: u32) {
        self.score = score;
    }

    pub fn increment(&mut self, times: u32) {
        self.times += times;
    }

    pub fn get_total(&self) -> u32 {
        self.score * self.times
    }
}

/// Description
/// -----------
/// Parses the scratch card number into 2 halves and checks to see if any
/// number in the second half exists in the first. For each number the card
/// total is doubled (starting at 1). The total of all totals is then added
/// up and returned.
fn main() {
    let (lines, part) = common::get_file_and_part();
    let mut total: u32 = 0;
    let mut cards: Vec<ScratchCard> = vec![];
    for line in lines.iter() {
        let mut game_total = 0;
        let split_line: Vec<&str> = line.split(": ").collect();
        let game = split_line.get(1).unwrap();
        let winners_and_actual: Vec<&str> = game.split(" | ").collect();
        let winners = string_to_numbers(winners_and_actual.first().unwrap());
        let actual = string_to_numbers(winners_and_actual.get(1).unwrap());
        for number in actual {
            if winners.contains(&number) {
                if game_total == 0 {
                    game_total = 1;
                } else {
                    game_total *= 2;
                }
            }
        }
        cards.push(ScratchCard::new(game_total));
        total += game_total;
    }
    if part == 1 {
        println!("Part 1 Scratch ScratchCard Winnings = {}", total);
    }
    if part == 2 {
        total = 0;
        for (card_number, card) in cards.iter().enumerate() {
            let card_score: usize = card.score.try_into().unwrap();
            let next_card_number: usize = card_number + 1;
            let last_card_number: usize = card_number + card_score + 1;
            for following_card_number in (next_card_number)..(last_card_number) {
                let following_card = &cards[following_card_number];
                // let mut p = following_card;
                // p.increment(card.times);
                following_card.increment(card.times);
            }
            total += card.get_total();
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
