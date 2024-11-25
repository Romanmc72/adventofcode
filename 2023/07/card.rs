/// Description
/// -----------
pub struct Card {
    symbol: char,
    value: u8,
}

impl Card {
    /// Description
    /// -----------
    pub fn from_char(character: char) -> Card {
        match character {
            'A' => Card { symbol: character, value: 0 },
            'K' => Card { symbol: character, value: 1 },
            'Q' => Card { symbol: character, value: 2 },
            'J' => Card { symbol: character, value: 3 },
            'T' => Card { symbol: character, value: 4 },
            '9' => Card { symbol: character, value: 5 },
            '8' => Card { symbol: character, value: 6 },
            '7' => Card { symbol: character, value: 7 },
            '6' => Card { symbol: character, value: 8 },
            '5' => Card { symbol: character, value: 9 },
            '4' => Card { symbol: character, value: 10 },
            '3' => Card { symbol: character, value: 11 },
            '2' => Card { symbol: character, value: 12 },
            _ => panic!("Invalid input symbol of {}", character),
        }
    }
}