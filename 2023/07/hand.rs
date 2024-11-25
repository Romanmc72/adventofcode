use std::collections::{HashMap, HashSet};

mod cards;


/// Description
/// -----------
pub struct Hand {
    hand_type: u32,
    cards: u32,
    bid: u32,
}


impl Hand {
    /// Description
    /// -----------
    /// Creates a Hand using the line of text that represents that hand.
    ///
    /// Param
    /// -----
    /// :line: &String
    /// The string representing the line in the input data.
    ///
    /// Return
    /// ------
    /// Hand
    /// The hand that results from that line of text being parsed.
    pub fn from_line(line: &String) -> Hand {
        let mut hand_type = 0;
        let mut cards = 0;
        let mut hand_map: HashMap<char, usize> = HashMap::new();
        let mut hand_set: HashSet<usize> = HashSet::new();
        let halves = line.split(" ").collect();
        let card_letters = halves.get(0).unwrap();
        let bid: u32 = halves.get(1).unwrap().parse().expect("Should be numeric").unwrap();
        let positions = card_letters.len();
        for (position, letter) in card_letters.chars().enumerate() {
            let number = card_to_number(letter);
            cards += number * 12.pow(positions - position);
            *hand_map.entry(&letter).or_default(0) += 1;
            // match hand_map.get(&letter) {
            //     Some(count) => { hand_map.insert(letter, count + 1); },
            //     None => { hand_map.insert(letter, 1); },
            // }
        }
        let different_cards = 0;
        for value in hand_map.values() {
            different_cards += 1;
            hand_set.add(value);
        }
    }
}

fn get_hand_type(hand_set: HashSet<usize>, different_cards: usize) -> u32 {
    let mut five_of_a_kind = HashSet<usize>::new();
    five_of_a_kind.add(5);
    match hand_set
}


/// Description
/// -----------
/// Converts the card character string into a number
///
/// Params
/// ------
/// :card: char
/// The individual character representing a card.
///
/// Return
/// ------
/// u32
/// The numeric value tied to that card (lower number is a better card)
fn card_to_number(card: char) -> u32 {
    let mut number;
    match card {
        'A' =>{ number = 0 },
        'K' =>{ number = 1 },
        'Q' =>{ number = 2 },
        'J' =>{ number = 3 },
        'T' =>{ number = 4 },
        '9' =>{ number = 5 },
        '8' =>{ number = 6 },
        '7' =>{ number = 7 },
        '6' =>{ number = 8 },
        '5' =>{ number = 9 },
        '4' =>{ number = 10 },
        '3' =>{ number = 11 },
        '2' =>{ number = 12 },
        _ => panic!("Invalid input symbol of {}", card),
    }
    number
}
