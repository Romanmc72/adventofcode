use std::collections::{HashMap, HashSet};
use std::convert::TryInto;


/// Description
/// -----------
/// A representation of a hand where in the hand type is a number
/// representing how good the hand is and the cards are a number
/// that represents the order of the cards in the hand as a number.
/// Because there are 13 cards, the hand's order of cards can be represented
/// in u32 integer by taking the cards numeric value and multiplying it by
/// 13 tot he power of the card's position in the hand. This will create a
/// numeric representation of the hand that acts as a hash in which the only
/// collisions will be identical hands.
pub struct Hand {
    pub hand_type: u32,
    pub cards: u32,
    pub bid: u32,
    pub card_letters: String,
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
    pub fn from_line(line: &String, part: u32) -> Hand {
        let mut cards = 0;
        let mut hand_map: HashMap<char, usize> = HashMap::new();
        let mut hand_set: HashSet<usize> = HashSet::new();
        let halves: Vec<&str> = line.split(" ").collect();
        let card_letters = halves.get(0).unwrap();
        let bid: u32 = halves.get(1).unwrap().parse::<u32>().unwrap();
        let positions = card_letters.len();
        let mut jacks = 0;
        for (position, letter) in card_letters.chars().enumerate() {
            if letter == 'J' {
                jacks += 1;
            }
            let number = match part {
                1 => card_to_number(letter),
                2 => card_to_number_part2(letter),
                _ => panic!("invalid part selection!"),
            };
            cards += number * 13_u32.pow((positions - position).try_into().unwrap());
            *hand_map.entry(letter).or_default() += 1;
        }
        let mut different_cards = 0;
        for value in hand_map.values() {
            different_cards += 1;
            hand_set.insert(*value);
        }
        let hand_type = match part {
            1 => get_hand_type(hand_set, different_cards),
            // use the hash map entry instead of a separate jacks counter
            2 => get_hand_type_part_2(hand_set, different_cards, jacks),
            _ => panic!("You need to pick a valid part number brutha."),
        };
        Hand {
            hand_type: hand_type,
            cards: cards,
            bid: bid,
            card_letters: card_letters.to_string(),
        }
    }
}

/// Description
/// -----------
/// Given the set of combinations of cards present in a hand as well as the
/// number of unique cards in a hand, return the "strength" of the hand as a
/// number from 0-6.
///
/// Params
/// ------
/// :hand_set: HashSet<usize>
/// The set of matches that were found.
/// e.g.
///   AAA99
///   would return a HashSet(3, 2)
///
///  233TT
///  would return HashSet(1, 2)
///
/// :different_cards" usize
/// The number of unique cards found in the hand. (1-5)
///
/// Return
/// ------
/// u32
/// The numeric value of the hand with lower hands being stronger.
fn get_hand_type(hand_set: HashSet<usize>, different_cards: usize) -> u32 {
    if hand_set.contains(&5) {
        return 0
    }
    if hand_set.contains(&4) {
        return 1
    }
    if hand_set.contains(&3) {
        if hand_set.contains(&2) {
            return 2
        }
        return 3
    }
    if hand_set.contains(&2) {
        if different_cards == 3 {
            return 4
        }
        return 5
    }
    6
}

/// Same thing but for part 2
fn get_hand_type_part_2(hand_set: HashSet<usize>, different_cards: usize, jacks: usize) -> u32 {
    if hand_set.contains(&5) {
        return 0
    }
    if hand_set.contains(&4) {
        if jacks > 0 {
            return 0
        }
        return 1
    }
    if hand_set.contains(&3) {
        if hand_set.contains(&2) {
            // either all of the 2 pair or all of the 3 pair
            // is jacks so you can get a 5 either way
            if jacks > 0 {
                return 0
            }
            return 2
        }
        // this would mean the 3 pair is all jacks, or one of the 
        // odd ones is a jack so either way you can get a 4 pair but not 5
        if jacks > 0 {
            return 1
        }
        return 3
    }
    if hand_set.contains(&2) {
        // 2 pair
        if different_cards == 3 {
            // jump straight to 4 pair because 2 of the 2 pair are jacks
            if jacks > 1 {
                return 1
            }
            // the off card is a jack so you get a full house
            if jacks > 0 {
                return 2
            }
            return 4
        }
        // one pair
        if jacks > 1 {
            // jacks are the pair or the jack is an off
            // card so you get a 3 pair either way
            return 3
        }
        return 5
    }
    // one jack so you get a single pair
    if jacks > 0 {
        return 5
    }
    // all different cards
    6
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
    match card {
        'A' => 0,
        'K' => 1,
        'Q' => 2,
        'J' => 3,
        'T' => 4,
        '9' => 5,
        '8' => 6,
        '7' => 7,
        '6' => 8,
        '5' => 9,
        '4' => 10,
        '3' => 11,
        '2' => 12,
        _ => panic!("Invalid input symbol of {}", card),
    }
}

/// Same thing but for part 2
fn card_to_number_part2(card: char) -> u32 {
    match card {
        'A' => 0,
        'K' => 1,
        'Q' => 2,
        'T' => 3,
        '9' => 4,
        '8' => 5,
        '7' => 6,
        '6' => 7,
        '5' => 8,
        '4' => 9,
        '3' => 10,
        '2' => 11,
        'J' => 12,
        _ => panic!("Invalid input symbol of {}", card),
    }
}
