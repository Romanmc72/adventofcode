use ranges::DivisibleRange;
use common::split_text_to_numbers;

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

    fn get_updated_number(&self, number: &u64) -> u64 {
        let difference: u64 = *number - self.source;
        if difference > self.range {
            panic!(
                "BRO THIS IS NOT EVEN IT THE RANGE WTF??? number {} ; source {} ; range {}",
                number,
                self.source,
                self.range
            );
        }
        self.destination + difference
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
        *number = self.get_updated_number(number);
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
    /// Returns the transformed divisible range.
    fn transform_range_numbers(&self, range: &DivisibleRange) -> DivisibleRange {
        if !self.is_range_in_range(range.clone()) {
            return range.clone();
        }
        let bottom = self.get_updated_number(&range.bottom);
        let top = self.get_updated_number(&range.top);
        if bottom > top {
            panic!("I think I fucked this up");
        }
        DivisibleRange::new(bottom, top)
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
    /// (Option<Vec<DivisibleRange>>, Option<Vec<DivisibleRange>>)
    /// A pair of optional objects. The first is a vector of divisible ranges
    /// and the second is a divisible range. The first signifies ranges that
    /// were transformed by this sub transformer and the second signify a vector
    /// that this sub transformer did not touch mainly because it was out of range.
    pub fn transform_range(&self, range: &mut DivisibleRange) -> (
        Option<Vec<DivisibleRange>>, Option<DivisibleRange>
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
            return (Some(vec![range.clone()]), None);
        }
        else if range.bottom > self.top_number() {
            return (None, Some(range.clone()));
        }
        // T:    |-------|
        // R: |-------|
        // Returns: 2
        else if range.top >= self.source && range.top <= transformer_top && range.bottom < self.source {
            let divided_range = range.divide_at(self.source - 1);
            let bottom_range = divided_range.get(0).unwrap();
            let top_range = divided_range.get(1).unwrap();
            let transformed_top_range = self.transform_range_numbers(top_range);
            return (Some(vec![bottom_range.clone()]), Some(transformed_top_range.clone()));
        }
        // T: |----------|
        // R:   |-------|
        // Returns: 1
        else if range.top <= transformer_top && range.bottom >= self.source {
            let transformed_range = self.transform_range_numbers(range);
            return (Some(vec![transformed_range.clone()]), None);
        }
        // T: |----------|
        // R:        |-------|
        // Returns: 2
        else if range.bottom <= transformer_top && range.top > transformer_top {
            let divided_range = range.divide_at(transformer_top);
            let bottom_range = divided_range.get(0).unwrap();
            let top_range = divided_range.get(1).unwrap();
            let transformed_range = self.transform_range_numbers(bottom_range);
            return (Some(vec![transformed_range.clone()]), Some(top_range.clone()));
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
            return (Some(vec![bottom_range.clone(), transformed_range.clone()]), Some(top_range.clone()));
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
    pub fn is_range_in_range(&self, range: DivisibleRange) -> bool {
        self.is_in_range(range.bottom) || self.is_in_range(range.top)
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
