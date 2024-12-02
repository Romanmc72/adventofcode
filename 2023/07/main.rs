use std::cmp::Ordering;
use std::convert::TryInto;
use hand::Hand;

mod common;
mod hand;

/// Description
/// -----------
/// Parts 1 and 2 for day 7!
///
/// I will have the cards stored with 2 scores
fn main() {
    let (lines, part) = common::get_file_and_part();
    let mut hands: Vec<Hand> = vec![];
    for line in lines {
        hands.push(Hand::from_line(&line, part));
    }
    hands.sort_by(|a, b| {
        match i64::from(b.hand_type) - i64::from(a.hand_type) {
            diff if diff > 0 => Ordering::Greater,
            diff if diff < 0 => Ordering::Less,
            _ => {
                match i64::from(b.cards) - i64::from(a.cards) {
                    diff if diff > 0 => Ordering::Greater,
                    diff if diff < 0 => Ordering::Less,
                    _ => Ordering::Equal,
                }
            },
        }
    });
    let mut winnings: u32 = 0;
    for (rank, hand) in hands.iter().enumerate() {
        let actual_rank: u32 = (rank + 1).try_into().unwrap();
        println!("Cards: {} Rank: {} Bid: {}", hand.card_letters, actual_rank, hand.bid);
        winnings += actual_rank * hand.bid;
    }
    println!("Winnings: {}", winnings);
}
