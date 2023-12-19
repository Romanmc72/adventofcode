/**
 * Need me a way to take the range of source inputs and map them to outputs.
 * Storing and sorting the inner transformers actually makes sense to me so
 * that one can find the transformer that is closes to the input number and
 * check to see if it is actually in range. If it is not in range then we can
 * just return the number and if it is we can return the transformation.
 */
use common::split_text_to_numbers;

mod range;


/// Description
/// -----------
/// The data structure representing one transformer that has a source and
/// destination with a particular ranger attached to it.
pub struct SubTransformer {
    pub source: u64,
    pub destination: u64,
    pub range: u64,
}


/// Description
/// -----------
/// The methods assigned to a sub transformer.
impl SubTransformer {
    /// Description
    /// -----------
    /// Grabs the source number and the range and adds them together to get
    /// the top number allowed in the source range.
    ///
    /// Return
    /// ------
    /// u64
    /// The ceiling of the range that will be in scope for the sub-transformer.
    pub fn top_number(&self) -> u64 {
        self.source + self.range - 1
    }

    /// Description
    /// -----------
    /// Checks to see if a number is within the source range.
    ///
    /// Params
    /// ------
    /// :number: u64
    /// The number to check whether or not is within the range.
    ///
    /// Return
    /// ------
    /// bool
    /// True if the number is in the range.
    /// False if the number is not in the range.
    pub fn is_in_range(&self, number: u64) -> bool {
        self.source <= number && self.top_number() >= number
    }

    /// Description
    /// -----------
    /// Takes the input number, and applies the transformation to that number.
    /// If the number is outside of the range then the number itself is just
    /// returned as is.
    ///
    /// Params
    /// ------
    /// :number: &mut u64
    /// The number to transform in place.
    pub fn transform_number(&self, number: &mut u64) {
        if !self.is_in_range(*number) {
            return;
        }
        let difference: u64 = *number - self.source;
        if difference > self.range {
            panic!(
                "BRO THIS IS NOT EVEN IT THE RANGE WTF??? number {} ; source {} ; range {}",
                number,
                self.source,
                self.range
            );
        }
        *number = self.destination + difference;
    }

    /// Description
    /// -----------
    /// Transforms the numbers from the input range and returns a new
    /// range with the numbers transformed.
    ///
    /// Params
    /// ------
    /// :range: DivisibleRange
    /// The range to transform numbers for.
    ///
    /// Return
    /// ------
    /// DivisibleRange
    /// The divisible range post transformation.
    fn transform_range_numbers(&self, range: range::DivisibleRange) -> range::DivisibleRange {
        let bottom = self.transform_number(*range.bottom);
        let top = self.transform_number(*range.top)
        range::DivisibleRange::new(bottom, top)
    }

    /// Description
    /// -----------
    /// Takes the input number, and applies the transformation to that number.
    /// If the number is outside of the range then the number itself is just
    /// returned as is.
    ///
    /// Params
    /// ------
    /// :range: &mut DivisibleRange
    /// The range to transform.
    ///
    /// Return
    /// ------
    /// (Option<Vec<range::DivisibleRange>>, Option<Vec<range::DivisibleRange>>)
    /// A pair of optional objects. The first is a vector of divisible ranges
    /// and the second is a divisible range. The first signifies ranges that
    /// were transformed by this sub transformer and the second signify a vector
    /// that this sub transformer did not touch mainly because it was out of range.
    pub fn transform_range(&self, range: &mut range::DivisibleRange) -> (
        Option<Vec<range::DivisibleRange>>, Option<range::DivisibleRange>
    ) {
        let transformer_top = self.top_number();
        // TODO Transform 1 range
        // Cases
        // T:           |-------|
        // R: |-------|
        //           OR
        // T: |----------|
        // R:               |-------|
        // Returns: 1
        if range.top < self.source {
            return (Some(vec![*range]), None);
        }
        else if range.bottom > self.top_number() {
            return (None, Some(*range));
        }
        // T:    |-------|
        // R: |-------|
        // Returns: 2
        else if range.top >= self.source && range.top <= transformer_top && range.bottom < self.source {
            let divided_range = range.divide_at(self.source);
            let bottom_range = divided_range.get(0).unwrap();
            let top_range = divided_range.get(1).unwrap();
            let transformed_top_range = self.transform_range_numbers(top_range);
            return (Some(vec![bottom_range]), Some(transformed_top_range));
        }
        // T: |----------|
        // R:   |-------|
        // Returns: 1
        else if range.top <= self.top_number && range.bottom >= self.source {
            let transformed_range = self.transform_range_numbers(range);
            return (Some(vec![transformed_range]), None);
        }
        // T: |----------|
        // R:        |-------|
        // Returns: 2
        else if range.bottom <= transformer_top && range.top > transformer_top {
            let divided_range = range.divide_at(transformer_top);
            let bottom_range = divided_range.get(0).unwrap();
            let top_range = divided_range.get(1).unwrap();
            let transformed_range = self.transform_range_numbers(bottom_range);
            return (Some(vec![transformed_range]), Some(top_range));
        }
        // T:  |----|
        // R: |-------|
        // Returns: 3
        else if range.bottom < self.source && range.top > transformer_top {
            let divided_range = range.divide_at(self.source);
            let bottom_range = divided_range.get(0).unwrap();
            let divide_again_range = divided_range.get(1).unwrap();
            let sub_divided_range = divide_again_range.divide_at(transformer_top);
            let middle_range = sub_divided_range.get(0).unwrap();
            let top_range = sub_divided_range.get(1).unwrap();
            let transformed_range = self.transform_range_numbers(middle_range);
            return (Some(vec![bottom_range, transformed_range]), Some(top_range));
        }
        else {
            panic!("This is not right...");
        }
    }

    /// Description
    /// -----------
    /// Detects whether a DivisibleRange in any way shape or form falls within
    /// the range of numbers that this sub transformer marshalls.
    ///
    /// Params
    /// ------
    /// :range: DivisibleRange
    /// The range to check against this sub transformer.
    ///
    /// Return
    /// ------
    /// bool
    /// True if the DivisibleRange overlaps with the source range of this
    /// sub transformer.
    /// False if the DivisibleRange does not overlaps with the source range
    /// of this sub transformer.
    pub fn is_range_in_range(&self, range: range::DivisibleRange) bool {
        self.is_empty(range.bottom) || self.is_in_range(range.top)
    }

    /// Description
    /// -----------
    /// From a raw line of text, construct the sub transformer.
    ///
    /// Params
    /// ------
    /// :line: &String
    /// The line of text to parse.
    ///
    /// Return
    /// ------
    /// SubTransformer
    /// The sub transformer constructed from this line of text.
    pub fn from_text_line(line: &str) -> SubTransformer {
        let numbers: Vec<u64> = split_text_to_numbers(line);
        let source = numbers.get(1).unwrap();
        let destination = numbers.get(0).unwrap();
        let range = numbers.get(2).unwrap();
        SubTransformer { source: *source, destination: *destination, range: *range }
    }
}


/// Description
/// -----------
/// A transformer with an array of sub transformers inside of it.
pub struct Transformer {
    pub sub_transformers: Vec<SubTransformer>,
}


impl Transformer {
    /// Description
    /// -----------
    /// Instantiates the transformer with nothing inside it.
    pub fn new() -> Transformer {
        Transformer { sub_transformers: vec![] }
    }

    /// Description
    /// -----------
    /// Inserts a sub transformer into the vector of transformers into the
    /// position that it belongs by iterating through the transformers that
    /// exist and adding this transformer after the one that it is bigger than.
    ///
    /// Params
    /// ------
    /// :sub_transformer: SubTransformer
    /// The sub transformer to insert into the list of sub transformers.
    pub fn add_sub_transformer(&mut self, sub_transformer: SubTransformer) {
        let mut insertion_index: usize = 0;
        for sub in self.sub_transformers.iter() {
            if sub_transformer.source > sub.source {
                insertion_index += 1;
            } else {
                break;
            }
        }
        self.sub_transformers.insert(insertion_index, sub_transformer);
    }

    /// Description
    /// -----------
    /// Takes the input number, finds the right transformer for it, and applies
    /// the appropriate transformation to that number using the sub transformer.
    ///
    /// Params
    /// ------
    /// :number: &mut u64
    /// The number to transform in place.
    pub fn transform_number(&mut self, number: &mut u64) {
        for index in 0..self.sub_transformers.len() {
            let sub_transformer = self.sub_transformers.get(index).unwrap();
            let next_sub_transformer = self.sub_transformers.get(index + 1);
            match next_sub_transformer {
                Some(next_sub) => {
                    if *number < next_sub.source && *number >= sub_transformer.source {
                        sub_transformer.transform_number(number);
                        break;
                    } else {
                    } 
                },
                None => {
                    sub_transformer.transform_number(number);
                    break;
                },
            }
        }
    }

    /// Description
    /// -----------
    /// Takes the input range, finds the right transformers for it, and applies
    /// the appropriate transformation to that range using the sub transformers.
    ///
    /// Params
    /// ------
    /// :range: &mut DivisibleRange
    /// The range to transform/divide.
    pub fn transform_range(&mut self, range: &mut range::DivisibleRange) {
        for index in 0..self.sub_transformers.len() {
            let sub_transformer = self.sub_transformers.get(index).unwrap();
            let next_sub_transformer = self.sub_transformers.get(index + 1);
            match next_sub_transformer {
                Some(next_sub) => {
                    if *number < next_sub.source && *number >= sub_transformer.source {
                        sub_transformer.transform_range(number);
                        break;
                    } else {
                    } 
                },
                None => {
                    sub_transformer.transform_range(number);
                    break;
                },
            }
        }
    }

    /// Description
    /// -----------
    /// Transforms the seeds in place using the transformer.
    ///
    /// Params
    /// ------
    /// :transformer:  &mut Transformer
    /// The transformer used to transform the numbers.
    ///
    /// :seeds: &mut Vec<u64>
    /// The seeds to transform with the transformer.
    pub fn transform_seeds(&mut self, seeds: &mut Vec<u64>) {
        println!("Seeds Pre-Transform: {:?}", seeds);
        for seed in seeds.iter_mut() {
            self.transform_number(seed);
        }
        println!("Transformed Seeds: {:?}", seeds);
    }

    /// Description
    /// -----------
    /// Transforms the seeds in place using the transformer.
    ///
    /// Params
    /// ------
    /// :transformer:  &mut Transformer
    /// The transformer used to transform the numbers.
    ///
    /// :seeds: &mut Vec<u64>
    /// The seeds to transform with the transformer.
    pub fn transform_seed_ranges(&mut self, seed_ranges: &mut Vec<range::DivisibleRange>) {
        for seed in seeds.iter_mut() {
            println!("Range Pre-Transform: {:?}", seed_range);
            self.transform_range(seed);
            println!("Transformed Range: {:?}", seeds);
        }
    }
}
